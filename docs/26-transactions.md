# 26 — Insufficient transaction validation

**Target:** Devom. Source-inspected; not runtime-tested. Complete [common setup](00-common-setup.md). Use only two instructor-approved disposable lab accounts.

## Objective and challenge
Record both starting balances. Make a small transfer and check the resulting balances and transaction record. Then try a controlled invalid amount, such as a small negative value. Check whether the server rejects it or changes either balance unexpectedly. Stop after one clear demonstration and tell the instructor so they can restore the test data.

## Before you begin

Follow [common setup](00-common-setup.md). Obtain two dedicated test user IDs, an authenticated session for the sender, and permission to alter their balances. Do not use real financial data. Source-based outcomes are unverified.

## Guided walkthrough

**Tools:** an API client such as Burp Repeater or Postman, plus the two approved account IDs. For a captured request, use `POST /transfer`, header `Authorization: Bearer <LAB_TOKEN>`, header `User-Agent: Postman`, and a JSON body containing `from_id`, `to_id` and `amount`. Replace the values with the instructor's test accounts:

```json
{"from_id":"ACCOUNT_A_ID","to_id":"ACCOUNT_B_ID","amount":1}
```

Send once for the positive baseline. For the controlled negative-value test, change only `amount` to `-1` after the instructor approves the change. These requests have not been piloted; record the actual response and balances.

1. Record both starting balances using the instructor-approved account views or API. Note each account's ID and owner.
2. Capture a normal `POST /transfer` request. Identify the `from_id`, `to_id`, and `amount` fields and the bearer token. Send one small positive transfer between the assigned accounts.
3. Record the response, both resulting balances and the transaction record. Check that the change matches the amount.
4. Repeat with one small negative amount, keeping both IDs within the assigned lab accounts. Compare the HTTP response, both balances and transaction record with your baseline. Stop after one clear result.
5. Inspect the server handler and identify where amount validation, ownership and balance checks would need to occur. Do not assume a success response alone means the balances changed.

## Troubleshooting

If the request is rejected, check the token, JSON fields and account IDs. If the response is unreadable, use the User-Agent described in common setup. Record unexpected behavior rather than repeating transactions indefinitely.

<details markdown="1">
<summary>Hints</summary>

1. Compare validation at the client and `/transfer` server handler.
2. Check the ownership of the source account and whether funds and amount are validated, not just the HTTP status.

</details>

## Evidence
Provide sanitized before/after balances, request and response, transaction record, business impact and recommendations for server-side validation, ownership checks and atomic accounting.

## Cleanup and review

Give the instructor the transaction IDs and starting balances so the disposable dataset can be restored. What invariant should hold for every transfer? How should the server handle invalid amounts and insufficient funds?
