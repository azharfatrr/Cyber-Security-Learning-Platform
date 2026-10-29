# 30 — Client-side login bypass through runtime manipulation

**Target:** BugBazaar. The local passcode comparison is present in source; runtime behavior and tool compatibility are unverified. Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md), and use an instructor-provided instrumentable emulator with matching Frida client/server.

## Objective and challenge
Set a disposable app PIN and confirm that an incorrect PIN is rejected. Inspect the client-side validation and find a point where you can observe it at runtime. Test whether changing the local decision lets the app proceed without the correct PIN. Verify the PIN-validation branch itself, since other navigation paths may also reach the dashboard. A local UI bypass alone does not prove server-side authorization bypass.

## Before you begin

The instructor must provide an instrumentable disposable emulator and compatible Frida tooling. Set a synthetic PIN. Runtime behavior has not been tested.

## Guided walkthrough

**Tools:** ADB, a static analysis tool such as JADX, and instructor-provided compatible Frida client/server tooling. Check the device and local client before attaching:

```bash
adb devices
frida --version
```

The instructor must verify that the server version and architecture match the emulator. Exact hooks depend on the installed build and have not been validated; do not treat the examples as a working bypass script.

1. Navigate to the passcode screen in a logged-in lab session. Enter an incorrect PIN and record the rejection. Confirm the correct PIN reaches the intended screen, then return to the passcode screen.
2. Read `PasscodeActivity` in the pinned source. Follow the validation button's click listener from the entered PIN through `UserAuthSave.getpasscode()` to the comparison and navigation decision.
3. Attach the approved runtime tool to the lab app process. First observe the relevant execution path without changing it, and confirm that the incorrect-PIN baseline still rejects.
4. Instrument the local validation decision in the lab process and retry the same incorrect PIN. Record which method or branch was observed and whether the result changes. Do not instrument other apps or devices.
5. Confirm that the observed transition came through the PIN-validation branch. Other app navigation paths may reach the same dashboard, so dashboard visibility by itself is not proof. Describe whether any protected server action was actually tested.

## Troubleshooting

If attachment fails, check that the Frida client and server versions match and that the emulator and process are instrumentable. Ask the instructor before changing app protection settings.

<details markdown="1">
<summary>Hints</summary>

1. Trace the PIN validation method using static analysis before attaching a runtime tool.
2. Instrument only the lab process; observe the return value before attempting to alter it. Check app protections and version compatibility if attachment fails.

</details>

## Evidence
Submit the baseline, observed method or decision point, sanitized instrumentation and result, limits of impact, and a recommendation to enforce security-sensitive authorization server-side.

## Cleanup and review

Stop the instrumentation and reset the synthetic PIN using the instructor's procedure. What is protected by the local PIN, and what evidence would be needed to claim a server-side authorization bypass?
