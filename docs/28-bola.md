# 28 — Broken object-level authorization

**Target:** Devom. Source-inspected; not runtime-tested. Complete [Common prerequisites](00-common-setup.md) and [Devom setup](01-devom-setup.md). Use two disposable accounts assigned by the instructor.

## Objective and challenge
Sign in as account A and request its profile. Then use the same session to request lab account B's profile. Compare the response and returned fields with the expected access rules. Access only the two assigned accounts.

## Before you begin

Obtain two instructor-assigned synthetic users, A and B, and their IDs. Use only those accounts. The steps and expected behavior are based on source, not a completed pilot.

## Guided walkthrough

**Tools:** Bash, `curl` and an API client. The commands use two instructor-assigned synthetic accounts and have not been runtime-tested.

After logging in as A, set these variables from the lab response and the instructor's account list. Replace every placeholder; never use an ID belonging to an unapproved account.

```bash
BASE='https://127.0.0.1:8080'
A_ID='ACCOUNT_A_ID'
B_ID='ACCOUNT_B_ID'
TOKEN='ACCOUNT_A_SESSION_TOKEN'
curl --insecure -i -A 'Postman' -H "Authorization: Bearer $TOKEN" "$BASE/profile/$A_ID"
curl --insecure -i -A 'Postman' -H "Authorization: Bearer $TOKEN" "$BASE/profile/$B_ID"
```

The first request establishes A's baseline; the second changes only the path ID. A response containing B's synthetic profile would support the finding. Redact sensitive fields before storing either response.

1. Send `POST /login` with account A's username and password. Save the returned session token and user ID locally; do not submit the token in your report.
2. Send `GET /profile/<A_ID>` with `Authorization: Bearer <A_TOKEN>` and `User-Agent: Postman`. Record the status and selected non-sensitive fields. This is the authorized baseline.
3. Change only the path to `GET /profile/<B_ID>`, keeping A's token. Send the request and compare the response with the baseline and the expected denial.
4. If B's synthetic profile appears, record which fields establish the identity and redact passwords, tokens and other sensitive fields. The inspected source does not compare the requested ID with the token subject; confirm the behavior on the running lab.
5. Inspect the profile handler and describe where an object ownership check belongs. If the response denies access or errors, record the actual result and check account IDs before drawing conclusions.

## Troubleshooting

If login or the baseline fails, check that A is active and that the bearer header is intact. If the response is encrypted, check the User-Agent.

<details markdown="1">
<summary>Hints</summary>

1. Compare the authenticated subject with the user ID in `/profile/<user_id>`.
2. A valid token proves authentication, not ownership of the requested object.

</details>

## Evidence
Provide redacted requests and responses, the two lab identities, whether cross-account data was returned, impact, and a server-side object authorization fix with a negative test case.

## Cleanup and review

Discard local session tokens according to lab policy. This exercise should not change account state. Why does a valid token not establish permission to read every profile? What should a cross-account negative test assert?
