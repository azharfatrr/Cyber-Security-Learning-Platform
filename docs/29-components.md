# 29 — Unauthorized access to Android components

**Target:** BugBazaar release `v1.2.1`, built from source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9). **Runtime tested:** Android 14 / API 34. A separate ordinary app queried only the uniquely marked synthetic record, and the provider returned it. This demonstrates cross-app access to that lab record; the result does not establish access to other rows.

## Objective and challenge

Inspect the installed package's exported Android components and their access controls. This walkthrough tests the `AddressContentProvider`: determine whether an ordinary app can read the one synthetic address created for the exercise. An `exported` declaration is a clue, not proof; the finding below is based on an actual query from a distinct app UID.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md). Both BugBazaar and the prebuilt caller app must already be installed and verified, and the emulator must be offline. Do not build either app. Use an instructor-approved disposable emulator; do not use a personal phone, real contacts, or personal addresses.

## Tools needed

- An Android emulator with ADB access.
- Android SDK Platform Tools (`adb`) and a terminal on the host computer.
- The BugBazaar target app and the instructor-supplied Module 29 caller app, installed as described in [BugBazaar setup](02-bugbazaar-setup.md).

Run ADB commands in the host terminal. Do the login, address search, and caller-screen check in the emulator. This walkthrough does not install or build apps.

## Guided walkthrough

### 1. Check the emulator and installed apps

In the host terminal, list connected devices. Set `SERIAL` to the emulator's serial from that list. The example below uses the pilot serial.

```bash title="Check the emulator and installed apps"
set -euo pipefail
adb devices -l
SERIAL=emulator-5554  # Replace if your emulator has a different serial
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
adb -s "$SERIAL" shell pm path com.BugBazaar
adb -s "$SERIAL" shell pm path org.lab.module29caller
adb -s "$SERIAL" shell pm list packages -U com.BugBazaar
```

**Expected:** `adb devices -l` lists your emulator with state `device`. The version commands print the Android release and API level; the pilot used Android `14` / API `34`. Each `pm path` command prints a `package:` path. The final command prints `package:com.BugBazaar uid:<number>`. Record that UID; it varies by emulator.

If the emulator is missing, unauthorized, or either package has no `package:` path, stop and ask the instructor. Do not wipe or reset it. Confirm it remains offline as described in BugBazaar setup.

### 2. Find or create the synthetic address

On the emulator, open BugBazaar. Sign in with its local demo account, `admin` / `BugBazaarSeccool`, then set a four-digit passcode for this disposable lab if prompted. These are local app credentials, not a cloud login. Deny unrelated SMS and storage or media permission prompts.

Open **Addresses**. Enter this nickname in **Search Addresses**, then tap **Search**:

- Nickname: `LAB29-PILOT-20261028-7F3A`
- Address: `SYNTHETIC lab address 29 for lab only`

If one matching record appears, leave it as is and continue. If none appears, tap BugBazaar's add-address control and save one record with the exact nickname and address above. Search again after saving. Stop and ask the instructor if more than one match appears or if you cannot confirm the saved values. Do not add another copy or use provider writes to create the record. The address list may contain fictional seed records; do not include them in screenshots.

!!! success "Expected"
    The Addresses screen shows exactly one card with nickname `LAB29-PILOT-20261028-7F3A` and address `SYNTHETIC lab address 29 for lab only`.

![BugBazaar's address screen showing the uniquely marked synthetic lab record.](images/lab-29/bugbazaar-synthetic-address.png)

### 3. Run the query from the ordinary caller app

Return to the host terminal. This command opens **Module 29 Provider Caller** on the emulator. The caller runs its fixed, read-only query as soon as it opens; you do not need to type anything into the app.

```bash title="Open the Module 29 caller"
adb -s "$SERIAL" shell am start -n org.lab.module29caller/.MainActivity
```

Look at the caller app screen. It displays the caller's package and UID, the provider URI, the operation, the fixed nickname filter, and the query result. The supplied caller has no permissions, accepts no URI or filter input, and queries only the synthetic nickname. Its Android 11+ `<queries>` entry makes the provider discoverable to the caller; it does not grant read access. Do not use `adb shell content query` instead; a query from the ADB shell does not prove that an ordinary app can read the provider.

The screen should show the following. The caller UID shown on your emulator will differ from the pilot's `10198`.

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

!!! success "Expected"
    The caller screen shows package `org.lab.module29caller`, a caller UID different from BugBazaar's `uid` from Step 1, URI `content://com.bugbazaar.provider.addresses/addresses`, and exactly the one synthetic record. If the screen says `No matching row returned` or `Query failed`, stop and use Troubleshooting. Do not broaden the query.

![Ordinary caller app displaying its UID, the provider URI, and the returned synthetic row.](images/lab-29/ordinary-app-provider-result.png)

### 4. Decide what the result proves

Compare the two identities: Step 1 printed BugBazaar's UID, and the caller screen printed the caller's package and UID. The UIDs must differ for this to show access from a separate app. In the pilot, BugBazaar's UID was `10197` and the caller's was `10198`; your numbers will vary.

The pinned release's manifest declares the provider exported and does not declare a read permission. When the separate caller returns the exact marker, the result demonstrates that an ordinary app could read this one synthetic record. It does not show access to other rows, real addresses, or every component in BugBazaar. Keep the query limited to the marker.

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
