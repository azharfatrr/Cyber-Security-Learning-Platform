# 30 — Client-side login bypass through runtime manipulation

*Can changing BugBazaar's local PIN check make an incorrect PIN work?*

## What this lab does

Set a synthetic PIN in BugBazaar, confirm that an incorrect PIN is rejected, then inspect the local PIN check. With instructor-provided Frida on a disposable emulator, test whether changing that check lets the app proceed with the same incorrect PIN.

This tests BugBazaar's local check only. Reaching another screen does not prove that a server accepted an unauthorized request.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md). Use an instructor-provided instrumentable emulator with matching Frida client/server, and set a synthetic PIN.

The local passcode comparison is present in the source, but runtime behavior and tool compatibility have not been verified. The instructor must confirm the emulator, architecture, and Frida versions before you attach. Do not guess at hooks or treat this as a verified working bypass.

## Guided walkthrough

Use ADB, JADX, and the instructor-provided Frida setup. Do not attach until the instructor confirms that the emulator architecture and Frida client/server versions are compatible. The runtime procedure and hook have not been verified for this target.

### 1. Check the emulator and record the baseline

Run these checks in the host terminal. Replace `emulator-5554` with the serial shown by `adb devices -l`.

```bash
set -euo pipefail
SERIAL=emulator-5554
adb devices -l
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
frida --version
```

Check that ADB lists the emulator with state `device`. Record the Android release, API level, and Frida client version. Ask the instructor for the server version and confirmation that it matches the emulator architecture. Stop if the target or versions cannot be confirmed.

In BugBazaar, use the synthetic PIN set for the lab. Enter an incorrect PIN and confirm it is rejected. Then enter the correct PIN and confirm it reaches the intended screen.

!!! warning "Expected baseline, verify on your device"
    The incorrect PIN should be rejected and the correct PIN should be accepted before instrumentation. Confirm both results during your run. Treat them as unverified until then.

![BugBazaar home screen on the Android 14 / API 34 emulator.](images/lab-30/bugbazaar-home-screen.png)

This is the destination shown by the pinned APK's successful passcode branch. The screenshot shows the screen only; it does not record a PIN attempt.

Return to the PIN screen before continuing.

### 2. Find the local PIN check

Open the pinned BugBazaar APK or source in JADX. In `PasscodeActivity`, follow the validation button through `UserAuthSave.getpasscode()` to the comparison and the navigation decision.

Check that you can identify the exact method or branch that handles a matching PIN and a mismatch. If the installed APK does not match the pinned release, stop and ask the instructor.

![Pinned PasscodeActivity.java source showing the PIN comparison and the success and mismatch branches.](images/lab-30/passcode-activity-source.png)

This screenshot is from the pinned GitHub source. It illustrates the local decision point; it does not demonstrate runtime behavior or a bypass.

### 3. Observe the check without changing it

Attach only with an instructor-approved, compatible Frida setup and an observation procedure verified for this target. Do not guess at method names, hooks, or scripts. If no verified procedure is available, stop here and report that the runtime step is blocked.

Retry the same incorrect PIN while observing the app process. Confirm that the normal rejection still occurs and record the method or branch observed.

### 4. Test the local decision

Continue only if the instructor has supplied a verified procedure for changing the local PIN decision on this build. Change only that decision in the BugBazaar process, then retry the same incorrect PIN. Record what the app does and which method or branch you observed.

Do not instrument other apps or devices. If the procedure or result differs from the instructor's expected behavior, stop and report the actual result; do not describe an unverified bypass as successful.

### 5. Confirm the result and its limits

Check that any screen transition came through the PIN-validation branch. Another navigation path may reach the same dashboard, so seeing the dashboard alone is not proof.

State whether you tested a protected server action. Without that separate test, report only what happened at BugBazaar's local PIN screen.

## Troubleshooting

If attachment fails, check that the Frida client and server versions match and that the emulator and process are instrumentable. Ask the instructor before changing app protection settings.

<details markdown="1">
<summary>Hints</summary>

1. Trace the PIN validation method using static analysis before attaching a runtime tool.
2. Instrument only the lab process; observe the return value before attempting to alter it. Check app protections and version compatibility if attachment fails.

</details>

## Evidence

Submit these three items:

- **Baseline:** a short note that the incorrect PIN was rejected and the correct PIN was accepted before instrumentation.
- **Runtime result:** a sanitized capture showing the method or branch observed, the repeated incorrect-PIN attempt, and what the app did after the local change.
- **Context and limits:** Android version/API, Frida client/server versions, and whether you tested a protected server action. If you did not test one, say that the result covers only the app's local PIN check.

## Vulnerability and Impact

**Potential vulnerability:** BugBazaar checks the PIN in the app. If runtime instrumentation can change that check, the app may proceed with an incorrect PIN. This bypass has not been verified at runtime.

**Potential impact:** Someone who can instrument the running app may get past the local PIN screen and reach content available after it on that device. This does not show that a server accepts unauthorized requests or exposes server-side data. Test a protected server action separately before claiming that impact.

## Cleanup and review

Stop the instrumentation and reset the synthetic PIN using the instructor's procedure. What is protected by the local PIN, and what evidence would be needed to claim a server-side authorization bypass?
