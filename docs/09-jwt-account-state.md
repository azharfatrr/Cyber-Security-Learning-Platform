# 09 — JWT-based account-state bypass

**Target:** Devom. Source-inspected; not runtime-tested. Complete [Common prerequisites](00-common-setup.md) and [Devom setup](01-devom-setup.md). Obtain instructor approval to block and restore a disposable test account.

## Objective and challenge
Find out whether the server checks the account's current status or relies on a claim in the token. Log in and request your profile to establish a baseline. Ask the instructor to block the lab account, then log in again and compare the tokens and responses. Test whether an appropriately signed lab token changes the result. Use a harmless profile request to confirm any access, then restore the account.

## Before you begin

Use a dedicated account whose status the instructor can change. You need its username, password and user ID, plus an API client. Set `User-Agent: Postman` on API requests so the inspected server returns plaintext JSON. Keep tokens private. The steps below are derived from source and have not been piloted.

## Guided walkthrough

**Tools:** Bash, `curl`, a local JWT inspection tool and an API client. After the baseline login, set the returned values locally:

```bash
BASE='https://127.0.0.1:8080'
USER_ID='LAB_USER_ID'
TOKEN='LAB_SESSION_TOKEN'
curl --insecure -i -A 'Postman' -H "Authorization: Bearer $TOKEN" "$BASE/profile/$USER_ID"
```

Replace the placeholders with the assigned account's values. Use a local JWT tool so lab tokens are not sent to an external website. These commands are not yet runtime-tested.

1. **Establish a baseline.** Send `POST /login` with JSON containing `username` and `password`. Record the returned `user_id`, `session_token` and status. Call `GET /profile/<user_id>` with `Authorization: Bearer <session_token>`; save the status and a redacted response.
2. **Change the account state.** Ask the instructor to block the same disposable user through the admin portal. Repeat the profile request with the *original* token. Source-based expectation: the server checks the token's `locked` claim, so a token issued while active may still be accepted. This is a hypothesis until tested.
3. **Compare a new token.** Log in again and inspect the new token's payload locally. Compare its `locked` claim with the original and repeat the protected request with the new token. A rejection is the expected source-based outcome for a token carrying `locked: true`.
4. **Investigate the trust boundary.** In the isolated lab only, inspect how the lab signing key is supplied and how `validate_jwt` verifies a signature. If you can legitimately produce a signed lab token with a changed claim, test it with the same profile endpoint. A payload edit without a valid signature is not a valid control.

## Troubleshooting

If login fails, confirm the account and server URL. If the response is opaque, check the User-Agent. If the old token expires or is missing, repeat the baseline before blocking the user. Do not share tokens or reuse lab keys elsewhere.

<details markdown="1">
<summary>Hints</summary>

1. Examine the login response and the `locked` claim separately from the database status.
2. Inspect `generate_jwt`, `validate_jwt`, and the Compose-created lab key. A modified claim without a valid signature should not be treated as proof.

</details>

## Evidence
Submit redacted baseline and changed-state requests, token claims, response codes, observed access, root cause and a server-side remediation. Distinguish bypassing the mobile screen from accessing an authenticated endpoint.

## Cleanup and review

Have the instructor restore the original account status. Remove local token copies according to lab policy. Which test shows stale account state, and which depends on access to the signing key? How could the server enforce suspension for already-issued tokens?
