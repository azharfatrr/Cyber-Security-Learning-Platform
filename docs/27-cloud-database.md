# 27 — Cloud database misconfiguration

**Target:** BugBazaar, conditional. Its README lists misconfigured Firebase Firestore, but the existence, ownership, accessibility and behavior of a suitable isolated instance have **not** been verified. Complete [common setup](00-common-setup.md).

## Blocking prerequisite
Do not contact any Firebase project or cloud resource embedded in the upstream application. The instructor must provide an organization-owned disposable Firebase project or local emulator, explicit authorization, synthetic records, connection details, and deliberately insecure rules. Until then this is **not a runnable lab**.

## Before you begin

Complete [common setup](00-common-setup.md). Before proceeding, obtain written scope, the approved project or emulator identifier, test identities, a synthetic record and the intended access rules. The instructor must confirm that the app actually connects to the approved environment. Stop if any of these are missing.

## Guided walkthrough (blocked pending environment)

**Tools:** the instructor's approved Firebase or emulator client and test identities. The project identifier, connection commands and access rules depend on the environment and cannot be supplied safely until it has been provisioned and authorized.

1. Check the supplied connection details against the approved project or emulator identifier. Do not use upstream cloud settings as a target.
2. With the authorized identity, read the designated synthetic record and record the expected result. This establishes the baseline.
3. Use the instructor-provided unauthenticated or lower-privilege identity to attempt the same operation on that record. Record the result and compare it with the intended rules.
4. If a write test is explicitly authorized, change only the designated synthetic value and verify the result using the authorized identity. Otherwise, limit the exercise to the approved read test.
5. Compare observed access with the lab rules and identify which rule should enforce the intended boundary. Actual commands and results depend on the environment and remain unverified.

## Troubleshooting

If the application cannot reach the approved emulator or project, stop and ask the instructor to check configuration. Do not redirect requests to an unapproved service.

## Objective and challenge
In the provided environment, identify how the app accesses the database. Test whether an unauthenticated or lower-privilege identity can read or change a designated synthetic record beyond its authorization. Compare the result with the instructor's intended rules. Stop if the target is not the approved project.

<details markdown="1">
<summary>Hints</summary>

1. Identify which Firebase product is actually used; storage and Firestore rules are different.
2. Compare an authorized baseline and a minimally privileged client, then review the deployed lab rules.

</details>

## Evidence
Record the approved project or emulator identifier, sanitized requests and results, affected synthetic data, rules and remediation. Do not submit API keys, tokens, or real data.

## Cleanup and review

Ask the instructor to restore any modified synthetic record and remove the temporary environment according to lab policy. Which identity should have access, and which rule enforces that decision?
