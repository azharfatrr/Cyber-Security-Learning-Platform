# 29 — Unauthorized access to Android components

**Target:** BugBazaar. Manifest inspected; runtime behavior unverified. Complete [common setup](00-common-setup.md); use a disposable emulator with synthetic data.

## Objective and challenge
List the installed package's exported activities, providers, receivers, and services. Choose an instructor-approved component that can expose or change synthetic data. Identify its intended access controls, then test whether another app or ADB can invoke it without the expected permission. Explain the impact of the result; an exported declaration alone does not establish a vulnerability.

## Before you begin

Follow [common setup](00-common-setup.md). The instructor must supply a working BugBazaar build, a disposable emulator, a synthetic address and an ordinary unprivileged test app. The manifest and provider source have been inspected; runtime behavior is unverified.

## Guided walkthrough

**Tools:** Android SDK Platform Tools (`adb`), Android Studio or a manifest viewer, and an instructor-provided unprivileged test app. Confirm the lab device and inspect the package:

```bash
adb devices
adb shell pm list packages com.BugBazaar
adb shell dumpsys package com.BugBazaar
```

Package output depends on the installed build. The package name comes from the inspected build configuration. Shell access is useful for investigation but does not by itself prove access from an ordinary third-party app.

1. Start BugBazaar on the emulator and confirm that the instructor's synthetic address exists. Record the emulator's Android version and app build.
2. Inspect the installed app's manifest or the pinned source manifest. List exported components and note any permissions protecting them.
3. Locate `AddressContentProvider` and its authority `com.bugbazaar.provider.addresses`. Inspect its `query` and `insert` methods and identify which operations might expose or change address data.
4. From the separate unprivileged test app, attempt the instructor-approved read of the synthetic address through the provider. Record the URI, caller identity and result. Do not query real contacts or unrelated data.
5. Compare the result with the expected access boundary. If you use ADB to inspect behavior, repeat the relevant check from the ordinary test app: the ADB shell is not equivalent to an unprivileged app.

## Troubleshooting

If the provider cannot be reached, check the authority, package version and emulator configuration. A declared exported component does not guarantee the test is reachable or exploitable on every Android version.

<details markdown="1">
<summary>Hints</summary>

1. Compare the declared and required permission names, and inspect component implementation and intent handling.
2. The source manifest lists exported providers including `com.bugbazaar.provider.addresses`; Android version and caller identity can affect behavior.

</details>

## Evidence
Submit component name, manifest configuration, invocation method, sanitized result and impact, and a remediation plus a negative access test. ADB shell permissions are not identical to those of an ordinary third-party app; verify that distinction.

## Cleanup and review

Remove only the instructor-provided synthetic data through the agreed reset process. Which caller could access the component, and what permission or export setting would enforce the intended boundary?
