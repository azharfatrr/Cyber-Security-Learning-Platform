# 29 — Unauthorized access to Android components

**Target:** BugBazaar release `v1.2.1`, built from source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9). **Runtime tested:** Android 14 / API 34, using a separate ordinary app UID and one synthetic address. The provider returned that row. This confirms cross-app access to the selected lab record; no unrelated or real records were queried.

## Objective and challenge

Inspect the installed package's exported Android components and their access controls. This walkthrough tests the `AddressContentProvider`: determine whether an ordinary app can read the one synthetic address created for the exercise. An `exported` declaration is a clue, not proof; the finding below is based on an actual query from a distinct app UID.

## Before you begin

Use an instructor-approved disposable Android emulator with ADB access. Do not use a personal phone, real contacts, or personal addresses. Keep the device offline during the local exercise. You need `adb`, `curl`, `sha256sum`, and a prebuilt ordinary-caller APK supplied separately by the instructor. The caller APK is not published with this documentation; do not build BugBazaar or install Android Studio for this lab.

The official release asset is [BugBazaar v1.2.1](https://github.com/payatu/BugBazaar/releases/download/v1.2.1/BugBazaar_v1.2.1.apk). Its release tag points to the pinned source revision above. The APK's embedded app version is `1.0` (version code `1`), not `1.2.1`.

## Guided walkthrough

**Tools:** Android SDK Platform Tools (`adb`), `curl`, `sha256sum`, and the instructor-supplied ordinary-caller APK. These commands use the pilot serial; substitute the serial shown by `adb devices -l` if yours differs.

### 1. Check the emulator and isolate network access

```bash
adb devices -l
SERIAL=emulator-5554
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
```

The pilot device reported Android `14` and API `34`. Enable Airplane mode in the emulator's Quick Settings before launching BugBazaar, then confirm:

```bash
adb -s "$SERIAL" shell cmd connectivity airplane-mode
```

Expected: `enabled`. If ADB disconnects while changing network state, reconnect to the same existing emulator; do not wipe or reset it.

### 2. Download and verify the prebuilt target APK

```bash
APK=BugBazaar_v1.2.1.apk
curl -fL -o "$APK" \
  https://github.com/payatu/BugBazaar/releases/download/v1.2.1/BugBazaar_v1.2.1.apk
printf '%s  %s\n' \
  c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c "$APK" \
  | sha256sum --check -
```

Expected: `BugBazaar_v1.2.1.apk: OK`. The SHA-256 is `c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c`. The release is tied to the pinned source revision; the installed package reports `com.BugBazaar`, version name `1.0`, version code `1`.

Check package state before installing:

```bash
adb -s "$SERIAL" shell pm path com.BugBazaar
```

If the package is absent, install the downloaded APK:

```bash
adb -s "$SERIAL" install "$APK"
```

Expected: `Success`. If BugBazaar is already installed, inspect `adb -s "$SERIAL" shell dumpsys package com.BugBazaar`; do not replace or clear an unknown installation. Confirm the installed build before continuing.

Verify the package path and embedded version:

```bash
adb -s "$SERIAL" shell pm path com.BugBazaar
adb -s "$SERIAL" shell dumpsys package com.BugBazaar | grep -E 'versionCode=|versionName='
```

Expected: an installed path for `com.BugBazaar`, `versionCode=1`, and `versionName=1.0`.

### 3. Disable the first-run downloader before launch

This debug APK's first-run path can download another APK from GitHub. Set its local guard before launching BugBazaar:

```bash
adb -s "$SERIAL" shell "run-as com.BugBazaar sh -c 'mkdir -p shared_prefs && printf \"%s\\n\" \"<map>\" \"<boolean name=\\\"isFirstRun\\\" value=\\\"false\\\" />\" \"</map>\" > shared_prefs/MyAppPreferences.xml'"
adb -s "$SERIAL" shell 'run-as com.BugBazaar cat shared_prefs/MyAppPreferences.xml'
```

Expected output contains `<boolean name="isFirstRun" value="false" />`. If `run-as` fails or the value is not `false`, stop; do not launch the app. This step writes only the target's first-run preference, not its database.

### 4. Create one synthetic address through the app UI

Launch BugBazaar after the guard is verified. Use its local demo login (`admin` / `BugBazaarSeccool`) and set a lab-only four-digit passcode; these are local app credentials, not a cloud login. Deny unrelated SMS and storage/media permission prompts. Navigate to **Addresses** and save exactly one synthetic entry:

- Nickname: `LAB29-PILOT-20261028-7F3A`
- Address: `SYNTHETIC lab address 29 for lab only`

The app should show a successful save and the exact marker in its saved-address list. Do not enter a real address or use provider writes to seed the record.

![BugBazaar's address screen showing the uniquely marked synthetic lab record.](images/lab-29/bugbazaar-synthetic-address.png)

### 5. Query the provider from a separate ordinary app

Obtain the instructor-supplied prebuilt caller APK separately; it is intentionally not deployed with this site. The pilot artifact's SHA-256 is `eedfec951335a8ed876241d86bc9e6c53a7dff4833b98fa522f8cbfc1168900e`. Verify it, then install and launch its fixed read-only query:

```bash
printf '%s  %s\n' \
  eedfec951335a8ed876241d86bc9e6c53a7dff4833b98fa522f8cbfc1168900e \
  module-29-caller.apk | sha256sum --check -
adb -s "$SERIAL" install module-29-caller.apk
adb -s "$SERIAL" shell am start -n org.lab.module29caller/.MainActivity
```

The helper has no declared permissions, uses a separate package/UID, accepts no arbitrary URI or input, and filters only the exact synthetic nickname. On Android 11 and later, its manifest must declare visibility of the provider authority with `<queries><provider android:authorities="com.bugbazaar.provider.addresses"/></queries>`; this is package visibility, not a permission grant. Do not substitute `adb shell content query` as proof of ordinary-app access.

The pilot observed target UID `10197` and caller `org.lab.module29caller` UID `10198` on this emulator. UIDs vary by device. The caller queried `content://com.bugbazaar.provider.addresses/addresses` using a read-only `nickname = ?` selection and received:

```text
Caller package: org.lab.module29caller
Caller UID: 10198
URI: content://com.bugbazaar.provider.addresses/addresses
Operation: read-only query
Filter: nickname = LAB29-PILOT-20261028-7F3A

Result:
LAB29-PILOT-20261028-7F3A
SYNTHETIC lab address 29 for lab only
```

![Ordinary caller app displaying its UID, the provider URI, and the returned synthetic row.](images/lab-29/ordinary-app-provider-result.png)

### 6. Interpret the result

The installed manifest declares this provider exported and does not declare a provider read permission. The distinct ordinary app UID returned the exact synthetic row, so cross-app read access is demonstrated for that record. The helper deliberately did not query other rows; do not claim that real data was accessed or that every record is exposed based only on this run.

## Troubleshooting

- **The first-run APK download prompt appears:** stop the app without continuing, verify the `isFirstRun=false` guard, and relaunch only after the read-back is correct.
- **The helper returns no matching row:** confirm BugBazaar displays the exact nickname, that both apps are installed under different UIDs, and that the helper manifest includes the provider authority under `<queries>` on Android 11+. Do not broaden the query to inspect other rows.
- **The provider reports an access error:** record the exact Android version, package versions, caller UID, URI, and error. An exported declaration does not guarantee the same runtime behavior on every Android release.
- **ADB shell returns a row but the helper does not:** that is not proof of cross-app access. Resolve the helper's package visibility and repeat the query from the ordinary app.

<details markdown="1">
<summary>Hints</summary>

1. Compare the provider's `exported` and permission attributes with the caller's package and UID.
2. Android package visibility and Android component permissions are separate controls. The helper's `<queries>` entry makes the named authority discoverable; it does not grant access.
3. Use a parameterized exact-marker selection. Never query real contacts or unrelated rows for this exercise.

</details>

## Evidence

Record the target release URL, source revision, APK SHA-256, embedded app version, Android version/API, target and caller package/UID, exact URI, operation, selection marker, and returned result. Attach the sanitized screenshots above. State explicitly that the query was made by an ordinary app, not only by the ADB shell. The tested helper source is kept outside the published site at `engineering/fixtures/module-29-caller/`; the instructor must distribute its prebuilt APK separately.

## Cleanup and review

The tested app UI has no address-delete control, and this provider's `delete()` method returns `0`; there is no verified safe way to remove the row. Leave the uniquely marked synthetic record in the disposable lab and do not clear BugBazaar data, uninstall apps, or call provider delete. The marker to identify is `LAB29-PILOT-20261028-7F3A`; use the instructor's disposable-emulator disposal procedure when finished.

Which access control would prevent an unrelated app from reading these addresses? What negative test would confirm that the same caller is denied after the provider is protected?
