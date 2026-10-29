# 27 — Cloud database misconfiguration

*Can a client read or change a Firebase record it should not reach?*

!!! danger "This lab requires an authorized Firebase environment"
    BugBazaar's README lists a misconfigured Firebase Firestore instance, but the upstream project's cloud resources belong to someone else. This lab therefore needs a separately authorized, isolated project or local emulator. Do not contact any Firebase project or cloud resource embedded in the upstream app.

## What this lab does

When the environment is available, you will:

1. Confirm that the app and your client both point at the approved project or emulator identifier.
2. Read one designated synthetic record with the authorized identity.
3. Repeat the same read with an unauthenticated or lower-privilege identity.
4. Compare the result with the rules deployed in that environment.

A lower-privilege read or write of that record would show that the database rules do not enforce the intended boundary. This page records the environment requirements, the test steps, and the evidence to collect.

**Target:** BugBazaar `v1.2.1` from source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9), plus a separately authorized Firebase project or emulator. Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md).

## Environment requirements

Your organization must supply, in writing:

- an organization-owned disposable Firebase project **or** a local Firebase emulator, with its identifier;
- explicit authorization to test it, with the scope limited to one synthetic record;
- the synthetic record's collection, document ID, and field values;
- a test identity for the authorized read and one for the lower-privilege read;
- the deployed security rules, which must be deliberately permissive for the lab;
- confirmation that the installed app connects to this environment and not to the upstream project.

If any item is missing, stop. Do not guess a project ID, reuse a key from the APK, or point the app at a real service.

## Before you begin

Do not start with the app. First confirm the scope document and the environment identifier, then confirm that the app's configuration matches that identifier. Keep the emulator offline as described in BugBazaar setup unless the approved environment requires a specific, restricted network path.

## Tools needed

- The approved Firebase project or local emulator and its client tooling, supplied with the environment.
- The two test identities.
- The installed BugBazaar APK, if the exercise includes checking the app's own read.

Exact commands depend on whether the environment is a project or an emulator, so this page does not include any. The environment owner supplies them with the environment.

## Guided walkthrough

### 1. Confirm the target

Record the approved project or emulator identifier and compare it with the identifier the app uses. If they differ, stop: the app is pointing somewhere else and the test would be out of scope.

!!! warning "Expected"
    The identifiers match. A mismatch means the app cannot be used for this exercise.

### 2. Read the synthetic record as the authorized identity

Using the provided client and the authorized test identity, read only the designated document. Record the field values and the response.

!!! warning "Expected"
    The authorized read returns the designated record. This is the baseline; without it, a later failure cannot be interpreted.

### 3. Repeat the read with the lower-privilege identity

Use the second identity, which should have no legitimate access to that document. Send one read for the same document only.

!!! warning "Expected"
    If the record is returned, the rules do not enforce the boundary. If the read is denied, record the denial; that is the secure outcome and it is still a valid result to report.

### 4. Compare with the deployed rules

Read the rules provided with the environment and identify which rule is supposed to allow or deny the read. Quote the specific match condition. A result without the corresponding rule is not evidence of a misconfiguration, only of an unexpected response.

!!! important "Key observation"
    A misconfiguration finding needs both a lower-privilege read of the designated record and a deployed rule that should deny that read. A denial is a valid secure result; a response alone, without the relevant rule, is not enough to claim a vulnerability. No Firebase environment is included with this guide, so it does not claim a tested outcome.

### 5. Write only if the scope allows it

If, and only if, the environment scope authorizes a write test, change one designated synthetic field and verify it with the authorized identity. Restore the original value immediately. Otherwise, stop after the read tests.

!!! warning "Expected"
    Any write stays inside the single synthetic document and is reverted in the same session.

## Troubleshooting

- **The app or client cannot reach the approved environment:** stop and check the configuration with the environment owner. Do not redirect traffic to an unapproved service.
- **The identifier is not the one you were given:** the client or APK is misconfigured. Do not continue.
- **Every identity is denied:** the rules may already be correct, or the identity is not the one intended. Record the denial and check the identity before drawing a conclusion.
- **The rules mention a different collection or field:** the scope does not match the test. Request the correct rules rather than testing around them.

<details markdown="1">
<summary>Hints</summary>

1. Identify which Firebase product the app actually uses; Storage and Firestore have separate rules.
2. Compare an authorized baseline with a minimally privileged client, then read the deployed rules.
3. A permissive rule is a configuration finding; a working exploit path also needs a client that can reach the document.

</details>

## Evidence

Submit these five items:

- **Environment:** the approved project or emulator identifier, and confirmation that it is not the upstream project.
- **Baseline:** the authorized read of the synthetic record, with field values redacted if required.
- **Lower-privilege result:** the exact request and response, including a denial if that is what happened.
- **Rules:** the relevant rule text, quoted.
- **Limits:** which identity should have access, which rule enforces that decision, and whether any write was authorized and performed.

Never submit API keys, service-account files, tokens, or real data.

## Vulnerability and Impact

This lab is about database rules, not the mobile screen. If a lower-privilege identity can read or write a record it should not reach, the impact is direct disclosure or modification of stored data for every user the rules cover, independent of the app. That is a server-side configuration weakness.

No instance is included with this guide, so it claims no result. The impact remains potential until you run the tests above in an authorized environment.

## Cleanup and review

- Restore any modified synthetic record.
- Remove temporary identities and client configuration according to lab policy.
- Confirm that the temporary environment is shut down when the lab ends.

Which identity should have access to the record, which rule enforces that, and how would you test the same decision again after changing the rules?
