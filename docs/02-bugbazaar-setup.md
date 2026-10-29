# BugBazaar setup

Complete [Common prerequisites](00-common-setup.md) first. This page prepares the prebuilt BugBazaar app for Labs 27, 29, and 30; learners do not build the app from source. Lab 27 requires a separately authorized cloud environment, and Lab 30 also requires an instrumentable emulator with Frida.

**Status:** The APK hash and the Module 29 workflow were tested on 29 October 2026 on Android 14 / API 34. Other emulator images may behave differently.

The offline procedure below prepares the local exercises (Labs 29 and 30). Lab 27 needs a separately provisioned, authorized cloud environment; do not use the upstream Firebase project. If Lab 27 is approved later, the environment owner defines its restricted network path instead of using this offline-only state.

## Pinned release and artifacts

- Official target APK: [BugBazaar v1.2.1](https://github.com/payatu/BugBazaar/releases/download/v1.2.1/BugBazaar_v1.2.1.apk).
- Pinned source revision: [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9).
- Target APK SHA-256: `c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c`.
- The release APK embeds app version `1.0` (version code `1`), not `1.2.1`.
- Lab 29 also requires the prebuilt ordinary-caller APK, published here as [module-29-caller.apk](assets/apk/module-29-caller.apk). Its SHA-256 is `5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc`. Do not build or substitute another caller.

Use an approved disposable emulator with ADB access. Do not use a personal phone, real contacts, or personal addresses. Keep the device offline during the local exercise; download the APKs on the host before installing them. If network isolation, package identity, or an existing installation cannot be verified, stop rather than replacing or clearing emulator state.

## 1. Isolate the emulator

Before launching BugBazaar, enable Airplane mode, turn Wi-Fi and mobile data off, and disconnect or disable Ethernet, VPN, and USB/Bluetooth tethering. Airplane mode alone is insufficient because Wi-Fi can be re-enabled. Check the emulator state with ADB:

```bash title="01 · Confirm the emulator is offline"
set -euo pipefail
SERIAL=emulator-5554
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
AIRPLANE_STATUS=$(adb -s "$SERIAL" shell cmd connectivity airplane-mode)
WIFI_STATUS=$(adb -s "$SERIAL" shell cmd wifi status)
CONNECTIVITY_STATUS=$(adb -s "$SERIAL" shell dumpsys connectivity)
if [ "$AIRPLANE_STATUS" != "enabled" ]; then
  echo 'Airplane mode is not enabled; stopping.' >&2
  exit 1
fi
case "$WIFI_STATUS" in
  *"Wifi is disabled"*) ;;
  *) echo 'Wi-Fi is not disabled; stopping.' >&2; exit 1 ;;
esac
case "$CONNECTIVITY_STATUS" in
  *"Active default network: none"*) ;;
  *) echo 'An active default network exists; stopping.' >&2; exit 1 ;;
esac
printf '%s\n' "$AIRPLANE_STATUS" "$WIFI_STATUS" 'Active default network: none'
```

!!! success "Expected"
    Android reports airplane mode `enabled`, `Wifi is disabled`, and `Active default network: none`. Also verify in Quick Settings that mobile data is off and no other transport, VPN, or tethering is connected. Stop if any check fails or isolation cannot be confirmed. If ADB disconnects while changing network state, reconnect to the same existing emulator; do not wipe or reset it. Substitute the serial shown by `adb devices -l` if it differs from `emulator-5554`.

## 2. Download and verify the target APK

Run on the host, not on the offline emulator:

```bash title="02 · Download, verify, and install BugBazaar"
set -euo pipefail
SERIAL=emulator-5554
APK=BugBazaar_v1.2.1.apk
EXPECTED_SHA=c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c
curl -fL -o "$APK" \
  https://github.com/payatu/BugBazaar/releases/download/v1.2.1/BugBazaar_v1.2.1.apk
printf '%s  %s\n' "$EXPECTED_SHA" "$APK" | sha256sum --check -

INSTALLED_APK=$(adb -s "$SERIAL" shell pm path com.BugBazaar \
  | sed -n 's/^package://p' | sed -n '1p')
if [ -z "$INSTALLED_APK" ]; then
  adb -s "$SERIAL" install "$APK"
  INSTALLED_APK=$(adb -s "$SERIAL" shell pm path com.BugBazaar \
    | sed -n 's/^package://p' | sed -n '1p')
fi
if [ -z "$INSTALLED_APK" ]; then
  echo 'Could not identify the installed BugBazaar APK; stopping.' >&2
  exit 1
fi
INSTALLED_SHA=$(adb -s "$SERIAL" shell sha256sum "$INSTALLED_APK" | awk '{print $1}')
if [ "$INSTALLED_SHA" != "$EXPECTED_SHA" ]; then
  echo 'Installed BugBazaar APK does not match the verified v1.2.1 release; stopping without replacing it.' >&2
  exit 1
fi
adb -s "$SERIAL" shell dumpsys package com.BugBazaar | grep -E 'versionCode=|versionName='
```

!!! success "Expected"
    The downloaded APK hash matches, the installed APK hash is identical, and package metadata reports version name `1.0` / version code `1`. A checksum, ADB, or installation error stops this procedure. If a pre-existing installation does not match, do not replace, uninstall, or clear it; use a fresh disposable emulator. Package metadata alone cannot distinguish this release from older versions.

## 3. Disable the first-run downloader before launch

This debug APK's first-run path can download another APK from GitHub. Preserve existing preferences: if `MyAppPreferences.xml` already exists, accept it only if it already contains `isFirstRun=false`; otherwise stop without changing it. Create the small guard only when the file is absent:

```bash title="03 · Set the first-run download guard"
set -euo pipefail
SERIAL=emulator-5554
adb -s "$SERIAL" shell "run-as com.BugBazaar sh -c 'if [ -e shared_prefs/MyAppPreferences.xml ]; then grep -Fq \"name=\\\"isFirstRun\\\" value=\\\"false\\\"\" shared_prefs/MyAppPreferences.xml || { echo \"Existing preferences do not have isFirstRun=false; stopping without changes.\" >&2; exit 1; }; else mkdir -p shared_prefs && printf \"%s\\\\n\" \"<map>\" \"<boolean name=\\\"isFirstRun\\\" value=\\\"false\\\" />\" \"</map>\" > shared_prefs/MyAppPreferences.xml; fi'"
adb -s "$SERIAL" shell 'run-as com.BugBazaar grep -Fq "name=\"isFirstRun\" value=\"false\"" shared_prefs/MyAppPreferences.xml'
adb -s "$SERIAL" shell 'run-as com.BugBazaar cat shared_prefs/MyAppPreferences.xml'
```

!!! success "Expected"
    The output contains `<boolean name="isFirstRun" value="false" />`. If `run-as` fails or the value is not `false`, stop; do not launch the app. Existing preferences are never overwritten. In the absent-file case this creates only the first-run guard; it does not modify the database.

## 4. Install the prebuilt Module 29 caller APK

The caller is a separate ordinary app with its own package and UID. Download the published [module-29-caller.apk](assets/apk/module-29-caller.apk) on the host during setup. Install and verify it now, but do not launch it until Lab 29 has created or confirmed its synthetic marker record.

Save the downloaded `module-29-caller.apk` in the current host working directory before running the command block. Keep the emulator offline; download or copy the artifact on the host.

```bash title="04 · Verify and install the caller APK"
set -euo pipefail
SERIAL=emulator-5554
CALLER_APK=module-29-caller.apk
CALLER_EXPECTED_SHA=5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc
printf '%s  %s\n' "$CALLER_EXPECTED_SHA" "$CALLER_APK" | sha256sum --check -

CALLER_INSTALLED_APK=$(adb -s "$SERIAL" shell pm path org.lab.module29caller \
  | sed -n 's/^package://p' | sed -n '1p')
if [ -z "$CALLER_INSTALLED_APK" ]; then
  adb -s "$SERIAL" install "$CALLER_APK"
  CALLER_INSTALLED_APK=$(adb -s "$SERIAL" shell pm path org.lab.module29caller \
    | sed -n 's/^package://p' | sed -n '1p')
fi
if [ -z "$CALLER_INSTALLED_APK" ]; then
  echo 'Could not identify the installed caller APK; stopping.' >&2
  exit 1
fi
CALLER_INSTALLED_SHA=$(adb -s "$SERIAL" shell sha256sum "$CALLER_INSTALLED_APK" | awk '{print $1}')
if [ "$CALLER_INSTALLED_SHA" != "$CALLER_EXPECTED_SHA" ]; then
  echo 'Installed caller does not match the verified fixture; stopping without replacing it.' >&2
  exit 1
fi
```

!!! success "Expected"
    The block exits successfully only after the installed caller's APK hash matches the published fixture.

If a different caller is already installed, do not replace or uninstall it; use a fresh disposable emulator. The caller is read-only and has no declared permissions. Lab 29 uses its distinct UID to demonstrate ordinary-app access; an `adb shell content query` is not an equivalent check.

## Ready for a lab

BugBazaar is ready only when the target APK and, for Lab 29, the caller APK match their expected hashes, the first-run guard reads back correctly, and the emulator's offline state is confirmed. Return to the selected lab for scenario-specific accounts, data, and exercise steps. BugBazaar setup alone does not satisfy Lab 27's cloud authorization requirements or replace Lab 30's Frida prerequisites.
