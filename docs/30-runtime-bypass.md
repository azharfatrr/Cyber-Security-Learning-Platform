# 30 — Client-side login bypass through runtime manipulation

*Can changing BugBazaar's local PIN check make an incorrect PIN work?*

## What this lab does

Set a synthetic PIN in BugBazaar, confirm that an incorrect PIN is rejected, then inspect the local PIN check. With instructor-provided Frida on a disposable emulator, test whether changing that check lets the app proceed with the same incorrect PIN.

This tests BugBazaar's local check only. Reaching another screen does not prove that a server accepted an unauthorized request.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md). Use an instructor-provided instrumentable emulator with matching Frida client/server, and set a synthetic PIN.

The local passcode comparison is present in the source. The Frida hook below was run once in the Android 14 / API 34 pilot, but the same-PIN comparison before and after the hook was not completed. Confirm both results on your own setup before you report a bypass.

## Guided walkthrough

You will use the host terminal, the Android emulator, and JADX. ADB commands go in the host terminal, not in the emulator. Keep the emulator offline as described in [BugBazaar setup](02-bugbazaar-setup.md), and use only the synthetic PIN prepared for this lab.

!!! warning "Check the versions before you attach"
    The example below uses Frida 17.4.2 on an x86_64 Android 14 / API 34 emulator. The hook installed and ran during the pilot, but the full same-PIN comparison was not completed. Confirm the versions on your own setup before you start.

### 1. Check that ADB can see the emulator

On the host, open a Bash terminal and run:

```bash
adb devices -l
```

Find the line for your instructor-approved emulator. The first item is its serial number. The second item must say `device`.

If no emulator is listed, or its status says `offline` or `unauthorized`, stop and ask the instructor. Do not install the app on a different device.

Copy the serial number from the first item. Use it in place of `emulator-5554` in the commands below. Keep using the same terminal so the `SERIAL` value stays set.

```bash
set -euo pipefail
SERIAL=emulator-5554  # Replace with the serial shown by adb devices -l
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
adb -s "$SERIAL" shell getprop ro.product.cpu.abi
frida --version
```

Write down the Android release, API level, device ABI, and Frida client version. Ask the instructor to confirm that the installed Frida server matches the client and device ABI. If `frida --version` fails, or the instructor cannot confirm compatibility, stop here. Do not install a different server or change the emulator yourself.

### 2. Check how BugBazaar handles the PIN

On the emulator, open BugBazaar from the app launcher.

1. If BugBazaar shows **Enter Passcode**, tap four digits different from your lab PIN. Confirm that four dots appear above the keypad, then tap **VALIDATE**.
2. Record the message and screen you actually see. During the Android 14 / API 34 pilot, BugBazaar displayed `Incorrect passcode. Try again.` after a rejected attempt. The entered digits were not confirmed in that capture, so it does not establish a four-digit baseline for a bypass test.
3. Enter your synthetic lab PIN, confirm that four dots appear, and tap **VALIDATE** again. Record what happens. The source predicts that a correct PIN opens the dashboard; this result has not been verified in the pilot.

If the incorrect PIN is not rejected or the correct PIN does not reach the expected screen, stop and ask the instructor. Do not continue to the runtime test with a different baseline.

![BugBazaar passcode screen showing an incorrect-passcode message.](images/lab-30/passcode-rejected.png)

This pilot screenshot shows a rejected attempt. It does not establish which digits were entered or demonstrate a bypass.

![BugBazaar home screen on the Android 14 / API 34 emulator.](images/lab-30/bugbazaar-home-screen.png)

This is the destination shown by the pinned APK's successful passcode branch. The screenshot shows the screen only; it does not record a PIN attempt.

!!! warning "If BugBazaar opens past the passcode screen"
    Close BugBazaar from the recent-apps list and open it again. If it still opens on the dashboard, restart the emulator and open BugBazaar from the launcher; in the pilot, that showed **Enter Passcode** again without any data reset. Do not clear app data, uninstall the app, or use ADB to start the private passcode activity.

### 3. Find the PIN comparison in JADX

On the host, open JADX and use **File → Open** to select the verified `BugBazaar_v1.2.1.apk` from BugBazaar setup. After it loads, use JADX's class search to find `PasscodeActivity`, then open `com.BugBazaar.ui.PasscodeActivity`.

In the displayed code, find `btnValidate.setOnClickListener`. Inside its `onClick` method, find the call to `UserAuthSave.getpasscode()` and the `enteredPasscode.equals(passcode)` comparison. The screenshot below shows these lines in the pinned source; JADX may display the code differently.

Read both sides of the `if` statement:

- If the entered PIN matches, the source starts `NavigationDrawer_Dashboard`.
- If it does not match, the source displays `Incorrect passcode. Try again.` and clears the entered value.

These are source-code results. They describe what the APK is written to do; they do not prove that either result happens on your emulator. If JADX shows a different class or comparison, stop and ask the instructor to check the APK.

![Pinned PasscodeActivity.java source showing the PIN comparison and the success and mismatch branches.](images/lab-30/passcode-activity-source.png)

This pinned source screenshot shows the comparison. It does not show a PIN attempt or a bypass.

### 4. Observe the check with Frida

First check whether a Frida server is already running on the emulator:

```bash
adb -s "$SERIAL" shell 'ps -A | grep frida'
```

If a `frida-server` line appears, write down its version and skip to the next command. If nothing appears, start the server file already installed on the emulator. The file name must match your server version:

```bash
adb -s "$SERIAL" shell 'su -c "nohup /data/local/tmp/frida-server-17.4.2 >/data/local/tmp/frida.log 2>&1 &"'
adb -s "$SERIAL" shell 'ps -A | grep frida'
```

The second command must now show the server process. If `su` is denied, or the file is missing, stop and ask the instructor. Do not download a server.

On the host, confirm that the client can see BugBazaar:

```bash
frida-ps -Uai | grep BugBazaar
```

The output should list `BugBazaar` with the identifier `com.BugBazaar`. If the list is empty, or the command reports that it cannot connect, stop and fix the client/server match before continuing.

### 5. Attach the hook and retry the same PIN

Create the hook script on the host in the directory where you will run Frida:

```bash
cat > lab30-hook.js <<'EOF'
Java.perform(function () {
  var Auth = Java.use('com.BugBazaar.controller.UserAuthSave');
  Auth.getpasscode.implementation = function () {
    console.log('[lab30] getpasscode() called; returning the lab value');
    return '0000';
  };
  console.log('[lab30] hook installed');
});
EOF
```

The script replaces the value returned by `UserAuthSave.getpasscode()` with `0000`. `PasscodeActivity` reads the stored PIN through that method, so a `0000` entry now matches instead of failing.

Attach to the running BugBazaar process and load the script:

```bash
frida -U -n BugBazaar -l lab30-hook.js
```

Wait for both lines:

```text
[lab30] hook installed
[Android Emulator 5554::BugBazaar ]->
```

The `->` prompt means Frida is attached and the session is interactive. Leave this terminal running.

On the emulator, enter `0000` on the passcode screen so that four dots appear, then tap **VALIDATE**. `0000` is wrong for the lab, so without the hook it is rejected.

Watch the Frida terminal. It should print:

```text
[lab30] getpasscode() called; returning the lab value
```

That line confirms the app reached the modified method. Then check the emulator screen and record which screen is shown.

If the app still reports `Incorrect passcode. Try again.`, the hook did not take effect. Stop the Frida session with `exit`, recheck the class and method names in JADX, and ask the instructor. Do not keep retrying with other scripts.

To undo the hook, type `exit` at the Frida prompt and restart BugBazaar from the app launcher.

!!! note "What the pilot showed"
    In the Android 14 / API 34 pilot, the hook installed, `getpasscode()` was called, and the app opened `NavigationDrawer_Dashboard`. The earlier rejected attempt was captured but its four digits were not confirmed, so the exact same-PIN comparison is still unverified. Confirm both results in your own run before you report a bypass.

Seeing the dashboard by itself does not prove that the PIN check was bypassed. Confirm that the transition came from the PIN-validation branch and that the Frida output shows the hooked call.

This test covers BugBazaar's local PIN screen. Only claim a server-side impact if you separately tested an instructor-approved protected server action.

## Troubleshooting

- **`Failed to attach: unable to connect to remote frida-server: closed`:** no Frida server is running, or it crashed. Repeat the `ps -A | grep frida` check in Step 4 and start the server again.
- **`frida-ps` lists no BugBazaar:** launch BugBazaar on the emulator first, then repeat the command.
- **`hook installed` never appears:** the class or method name differs in your build. Recheck `com.BugBazaar.controller.UserAuthSave` and `getpasscode` in JADX before changing the script.
- **The app still rejects `0000`:** the hook is not active in that process. Stop Frida with `exit`, attach again, and confirm the `getpasscode() called` line when you tap **VALIDATE**.
- **Frida reports a version mismatch:** the client and server versions must match. Ask the instructor; do not install a different server yourself.

<details markdown="1">
<summary>Hints</summary>

1. Trace the PIN validation method using static analysis before attaching a runtime tool.
2. Instrument only the lab process; observe the return value before attempting to alter it. Check app protections and version compatibility if attachment fails.

</details>

## Evidence

Submit these three items:

- **Baseline:** record the four digits you entered and the message shown before instrumentation. Confirm that the incorrect PIN was rejected and the correct PIN was accepted. If you could not reach the passcode screen, say so instead.
- **Frida result:** include the sanitized Frida output showing `hook installed` and `getpasscode() called`, the PIN you entered after attaching, and a capture of the screen the app showed. Say whether the same PIN was rejected before the hook.
- **Context and limits:** Android version/API, Frida client/server versions, and whether you tested a protected server action. If you did not test one, say that the result covers only the app's local PIN check.

## Vulnerability and Impact

**Potential vulnerability:** BugBazaar compares the PIN inside the app and reads the stored value from shared preferences through `UserAuthSave.getpasscode()`. If a process can change that return value, a wrong PIN can match. In the pilot, a Frida hook replaced the value and the app opened the dashboard; the same-PIN baseline was not confirmed, so treat the bypass as observed but not fully controlled.

**Potential impact:** Someone who can instrument the running app may get past the local PIN screen and reach content available after it on that device. This does not show that a server accepts unauthorized requests or exposes server-side data. Test a protected server action separately before claiming that impact.

## Cleanup and review

Stop the instrumentation and reset the synthetic PIN using the instructor's procedure. What is protected by the local PIN, and what evidence would be needed to claim a server-side authorization bypass?
