# 10 — OTP authentication logic

**Target:** Devom. Source-inspected; not runtime-tested. Complete [common setup](00-common-setup.md) using the disposable mobile account.

## Objective and challenge
Follow the login and OTP flow. Can you reach a protected endpoint before completing OTP verification? Compare a normal login, an invalid OTP attempt, and a protected request using the session issued at login. Then check whether verification accepts a predictable or disclosed value. Do not brute-force the code.

## Before you begin

Follow [common setup](00-common-setup.md). Use the assigned disposable account and an API client configured with `User-Agent: Postman`. The sequence below is based on source and has not been run.

## Guided walkthrough

**Tools:** Bash, `curl` and an API client. Use your instructor-assigned account. These commands target only the host-local Devom service and are unverified against a running instance.

1. Send a login request. Replace the sample values with lab credentials that contain no JSON-special characters, or use an API client to enter credentials safely. The response may contain a session token and OTP, so do not share the output.

    ```bash
    BASE='http://127.0.0.1:8443'
    curl -i -A 'Postman' -H 'Content-Type: application/json' \
      --data '{"username":"LAB_USERNAME","password":"LAB_PASSWORD"}' "$BASE/login"
    ```

    Copy the returned `user_id` and `session_token` into the next variables.

    ```bash
    USER_ID='LAB_USER_ID'
    TOKEN='LAB_SESSION_TOKEN'
    curl -i -A 'Postman' -H "Authorization: Bearer $TOKEN" "$BASE/profile/$USER_ID"
    ```

    Record whether the protected profile is accessible before OTP verification. The source suggests it may be; a pilot must confirm the actual response.

2. Send an incorrect OTP in your API client: `POST /verify_login_2fa`, header `Content-Type: application/json`, body `{"user_id":"LAB_USER_ID","token":"0000"}`. Replace the ID and choose an incorrect value that differs from the disclosed OTP. Compare this response with the protected request above.

3. Inspect the returned login fields and the `verify_2fa` function in the pinned server source. If you identify an accepted value, send one verification request in the isolated lab and record the result. Do not guess repeatedly.

4. Compare the sequence: token issuance, failed or accepted verification, and profile access. A verification success response alone does not prove a protected endpoint enforces the second factor.


## Troubleshooting

Use the same user ID throughout. If the response is encrypted, check the User-Agent. If login fails, verify the lab account's status before changing any test data.

<details markdown="1">
<summary>Hints</summary>

1. Compare when the session token is issued with when the second factor is checked.
2. Inspect `/login` and `/verify_login_2fa`, including debug fields and verification conditions.

</details>

## Evidence
Provide a sanitized sequence and response codes, showing whether protected access occurred before OTP verification. Explain whether each finding is OTP disclosure, a fixed bypass, or failure to bind authentication state to the token; propose separate fixes.

## Cleanup and review

Discard local token copies according to lab policy. When was the session token issued? What server-side state would distinguish a password-only session from one that completed OTP verification?
