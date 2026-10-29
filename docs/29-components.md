# 29 — Unauthorized access to Android components

**Target:** BugBazaar release `v1.2.1`, built from source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9). **Runtime tested:** Android 14 / API 34. A separate ordinary app queried only the uniquely marked synthetic record, and the provider returned it. This demonstrates cross-app access to that lab record; the result does not establish access to other rows.

## Objective and challenge

Inspect the installed package's exported Android components and their access controls. This walkthrough tests the `AddressContentProvider`: determine whether an ordinary app can read the one synthetic address created for the exercise. An `exported` declaration is a clue, not proof; the finding below is based on an actual query from a distinct app UID.

## Before you begin

Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md), including installation and verification of both the target and prebuilt ordinary-caller APK. Do not build either app. Use an instructor-approved disposable Android emulator with ADB access; do not use a personal phone, real contacts, or personal addresses. Keep the emulator offline as configured in setup. You need `adb` for the walkthrough.

## Guided walkthrough

**Tools:** Android SDK Platform Tools (`adb`). These commands use the pilot serial; substitute the serial shown by `adb devices -l` if yours differs.

### 1. Confirm the emulator and setup readiness

```bash
adb devices -l
SERIAL=emulator-5554
adb -s "$SERIAL" shell getprop ro.build.version.release
adb -s "$SERIAL" shell getprop ro.build.version.sdk
adb -s "$SERIAL" shell pm path com.BugBazaar
adb -s "$SERIAL" shell pm path org.lab.module29caller
```

The pilot device reported Android `14` and API `34`. Both `pm path` commands should return an installed package path. The emulator must remain offline as verified in [BugBazaar setup](02-bugbazaar-setup.md); if its network state or either package is uncertain, stop and ask the instructor. Do not wipe or reset the emulator.

### 2. Create one synthetic address through the app UI

Launch BugBazaar after the first-run guard is verified in setup. Use its local demo login (`admin` / `BugBazaarSeccool`) and set a lab-only four-digit passcode; these are local app credentials, not a cloud login. Deny unrelated SMS and storage/media permission prompts. The Addresses screen may display fictional seed rows; do not include those rows in submitted screenshots. Search Addresses for the exact nickname below before saving:

- Nickname: `LAB29-PILOT-20261028-7F3A`
- Address: `SYNTHETIC lab address 29 for lab only`

If exactly one matching record exists, reuse it and do not save another. If no match exists, save exactly one entry with these values. If multiple matches appear or the result is uncertain, stop and ask the instructor; do not add another row. The app should show the exact marker in its search results. Do not enter a real address or use provider writes to seed the record.

![BugBazaar's address screen showing the uniquely marked synthetic lab record.](images/lab-29/bugbazaar-synthetic-address.png)

### 3. Query the provider from a separate ordinary app

The prebuilt caller was installed and verified in [BugBazaar setup](02-bugbazaar-setup.md). Launch its fixed read-only query only after the synthetic marker exists:

```bash
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

### 4. Interpret the result

The installed manifest declares this provider exported and does not declare a provider read permission. The distinct ordinary app UID returned the exact synthetic row, so cross-app read access is demonstrated for that record. The ordinary-app query was restricted to that marker; BugBazaar's UI can display other fictional seed rows, which are outside this query and must be excluded from submitted screenshots. Do not claim that real data was accessed or that every record is exposed based only on this run.

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
