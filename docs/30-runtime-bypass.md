# 30 — Client-side login bypass through runtime manipulation

*Can changing BugBazaar's local PIN check make an incorrect PIN work?*

## What this lab does

Set a synthetic PIN in BugBazaar, confirm that an incorrect PIN is rejected, then inspect the local PIN check. With instructor-provided Frida on a disposable emulator, test whether changing that check lets the app proceed with the same incorrect PIN.

This tests BugBazaar's local check only. Reaching another screen does not prove that a server accepted an unauthorized request.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md). Use an instructor-provided instrumentable emulator with matching Frida client/server, and set a synthetic PIN.

The local passcode comparison is present in the source, but runtime behavior and tool compatibility have not been verified. The instructor must confirm the emulator, architecture, and Frida versions before you attach. Do not guess at hooks or treat this as a verified working bypass.

## Guided walkthrough

**Tools:** ADB, a static analysis tool such as JADX, and instructor-provided compatible Frida client/server tooling. Check the device and local client before attaching:

```bash
adb devices
frida --version
```

The instructor must verify that the server version and architecture match the emulator. Exact hooks depend on the installed build and have not been validated; do not treat the examples as a working bypass script.

1. **Record the baseline.** In a logged-in lab session, enter an incorrect PIN and confirm BugBazaar rejects it. Enter the correct PIN and confirm it reaches the intended screen. Return to the PIN screen.
2. **Find the local check.** In the pinned source, follow `PasscodeActivity`'s validation button through `UserAuthSave.getpasscode()` to the PIN comparison and navigation decision.
3. **Observe the check.** Attach the instructor-approved Frida setup to the BugBazaar process without changing its behavior. Retry the incorrect PIN and confirm the baseline rejection.
4. **Test the local change.** Change only the local validation decision in the BugBazaar process, then retry the same incorrect PIN. Record which method or branch you observed and whether the app proceeds. Do not instrument other apps or devices.
5. **Confirm the result.** Check that the transition came through the PIN-validation branch. Another navigation path may reach the same dashboard, so seeing the dashboard alone is not proof. State whether you tested a protected server action.

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
