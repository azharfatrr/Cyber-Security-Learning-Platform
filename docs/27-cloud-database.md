# 27 — Cloud storage misconfiguration

*Can a client read a stored user record without any credentials?*

!!! danger "Use only the local emulator in a disposable lab"
    This lab runs entirely against the repository's Firebase Storage emulator on the host loopback interface. Do not point the app at a cloud project, reuse any key from the APK, or expose the emulator ports beyond the disposable lab. The committed rules are deliberately open for the exercise and must never be deployed to a real project.

## What this lab does

BugBazaar's README describes a cloud-database module, but the shipped source uses Firebase **Storage**, not Firestore. Saving a profile in `MyProfile` builds a small text record and uploads it to `<device-name>/userinfo.txt` in the configured bucket.

In this lab you will:

1. Start the committed local Storage emulator and confirm its synthetic baseline.
2. Read a seeded synthetic record with no credentials.
3. Confirm that the installed app and its configuration point at that local emulator.
4. Save a synthetic profile in the app and confirm the upload.
5. Read the app-written object with no credentials.
6. Compare the result with the committed Storage rule.

**Completion criteria:** you have a baseline read, an app-written object, an unauthenticated read of that object, and the matching rule text.

**Verification status:** verified end to end on 2 November 2026 on Android 14 / API 34 with the published APK. The outputs below are from that run.

**Target:** the repository-built `bugbazaar-lab27-emulator.apk` (package `com.BugBazaar.lab27`), built from BugBazaar source revision [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9). Complete [Common prerequisites](00-common-setup.md) and [BugBazaar setup](02-bugbazaar-setup.md), including its Lab 27 install section.

## Before you begin

### Tools needed

- The repository checkout, because the emulator configuration and lifecycle scripts live in `engineering/lab27/`.
- Node.js and `npm`, to install the pinned Firebase CLI once.
- `curl` and `python3` on the host, for the object reads and JSON formatting.
- An Android emulator with ADB access and a route to the host alias `10.0.2.2`.
- The published Lab 27 APK from [Lab downloads](downloads.md).

Install the pinned CLI from the repository root:

```bash title="Install the pinned Firebase CLI"
cd engineering/lab27
npm install --no-audit --no-fund
cd ../..
```

`package.json` pins `firebase-tools@15.34.2`. The build also used Gradle 8.4, Android Gradle plugin 8.3.1, NDK 26.1.10909125, and OpenJDK 21.0.12.1.

Keep host egress restricted to the loopback path used here. The emulator must be able to reach the host; confirm that the approved firewall allows `127.0.0.1:9199` and `127.0.0.1:4000` from the lab boundary and blocks unrelated egress. Do not expose either port to a LAN or the internet.

## Understand the scenario

Firebase Storage protects objects with rules evaluated by the storage service, not by the Android UI. The app uploads with its own configuration and does not sign the user in to Firebase. The committed rule for this lab allows every read and write:

```text
match /{allPaths=**} {
  allow read, write: if true;
}
```

That rule makes the object effectively public to anyone who can reach the emulator. The UI still asks for an app login and a device passcode, but those are local app controls and do not protect the Storage object. This lab separates the two: the app login gets you to the profile screen; the unauthenticated `curl` request shows what the storage boundary actually enforces.

## Guided walkthrough

### 1. Start the emulator and confirm the baseline

**Where:** host shell, repository root.

`reset.sh` stops any running instance, clears the emulator's runtime state, starts it, and uploads the fixtures:

```bash title="01 · Reset, start, and seed the local emulator"
./engineering/lab27/reset.sh
```

Expected output from the verified run:

```text
Lab 27 emulator stopped.
Lab 27 Storage emulator is ready at http://127.0.0.1:9199
Emulator UI: http://127.0.0.1:4000
Seeded alice-lab27%2Fuserinfo.txt
Seeded bob-lab27%2Fuserinfo.txt
```

List the objects:

```bash title="02 · List the baseline objects"
curl -fsS 'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o' \
  | python3 -m json.tool
```

Expected: two items, both in bucket `lab27-local.appspot.com`:

```json
{
    "prefixes": [],
    "items": [
        {
            "name": "alice-lab27/userinfo.txt",
            "bucket": "lab27-local.appspot.com"
        },
        {
            "name": "bob-lab27/userinfo.txt",
            "bucket": "lab27-local.appspot.com"
        }
    ]
}
```

**Check:** the bucket identifier is `lab27-local.appspot.com`, not an upstream project. If the command fails, stop and use the troubleshooting section; do not continue with an unknown backend.

### 2. Read a seeded record without credentials

**Where:** host shell, repository root.

The URL path encodes `/` as `%2F`. `alt=media` asks the Storage API for the object bytes instead of metadata.

```bash title="03 · Unauthenticated read of the seeded record"
curl -fsS \
  'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o/alice-lab27%2Fuserinfo.txt?alt=media'
```

Expected output from the verified run:

```text
Name: Alice Example
Email: alice@example.invalid
Mobile: 555-0101
Address: 1 Synthetic Way
Marker: LAB27-ALICE-SYNTHETIC
```

**Check:** the command sends no `Authorization` header and still returns the record. This is the lower-privilege baseline.

### 3. Confirm the app and configuration are local

**Where:** host shell, repository root.

Verify the published APK you installed:

```bash title="04 · Verify the Lab 27 APK identity"
printf '%s  %s\n' \
  b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604 \
  docs/assets/apk/bugbazaar-lab27-emulator.apk | sha256sum --check -
adb shell pm path com.BugBazaar.lab27
```

Expected: `OK`, followed by a package path such as `package:/data/app/.../base.apk`.

Read the committed identifiers:

```bash title="05 · Show the local project identifiers"
grep -E '"project_id"|"storage_bucket"|"package_name"' \
  engineering/lab27/google-services.json
```

Expected output:

```text
    "project_id": "lab27-local",
    "storage_bucket": "lab27-local.appspot.com",
          "package_name": "com.BugBazaar.lab27",
```

**Check:** the package is `com.BugBazaar.lab27` and both Firebase identifiers are local. The APK hash ties the installed file to this configuration and to the `10.0.2.2:9199` endpoint added by `engineering/lab27/prepare.py`.

### 4. Sign in and open My Profile

**Where:** the Android emulator.

Complete [BugBazaar setup](02-bugbazaar-setup.md#4-install-the-lab-27-variant) first if the app is not installed. Then:

1. Launch **BugBazaar Lab 27**.
2. Sign in with the lab-only credentials `admin` / `BugBazaarSeccool`.
3. Create a four-digit passcode of your choice. Use `1234` for this walkthrough.
4. Deny the media, SMS, and notification permission prompts. They are not needed.
5. If a promotional dialog or a **No Internet Access** dialog appears, choose **OK**.
6. Tap the menu icon, then **My Profile**.

**Check:** the profile screen shows `Name:`, `Email-ID:`, `Mobile:`, and `Address:` with the app's demo values.

### 5. Save a synthetic profile

**Where:** the Android emulator, **My Profile** screen.

1. Tap **EDIT PROFILE**.
2. Replace the fields with these synthetic values:
   - Name: `Alice Example`
   - Email-ID: `alice@example.invalid`
   - Mobile: `5550101`
   - Address: `1 Synthetic Way`
3. Tap **SAVE PROFILE**.

**Check:** the screen returns to the read-only view and shows the values you entered. The app also writes `userinfo.txt` to its configured bucket; the next step confirms that write.

Use only these synthetic values. Do not enter a real address, phone number, or email.

### 6. Confirm the app-written object

**Where:** host shell, repository root.

```bash title="06 · List objects after the app save"
curl -fsS 'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o' \
  | python3 -m json.tool
```

Expected: the two seeded objects plus a new object whose prefix is the emulator's device name. The verified run produced:

```json
{
    "prefixes": [],
    "items": [
        {
            "name": "Google sdk_gphone64_x86_64/userinfo.txt",
            "bucket": "lab27-local.appspot.com"
        },
        {
            "name": "alice-lab27/userinfo.txt",
            "bucket": "lab27-local.appspot.com"
        },
        {
            "name": "bob-lab27/userinfo.txt",
            "bucket": "lab27-local.appspot.com"
        }
    ]
}
```

**Check:** a new `<device-name>/userinfo.txt` object exists. The prefix is built from the emulator's manufacturer and model, so yours may differ. Use the exact name from your list in the next step.

If the object is missing, see the troubleshooting section before changing anything.

### 7. Read the app-written object without credentials

**Where:** host shell, repository root.

Substitute your object prefix. In the verified run it was `Google sdk_gphone64_x86_64`, and the space is encoded as `%20`:

```bash title="07 · Unauthenticated read of the app-written record"
curl -fsS \
  'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o/Google%20sdk_gphone64_x86_64%2Fuserinfo.txt?alt=media'
```

Expected output from the verified run:

```text
Name: Alice Example
Email: alice@example.invalid
Mobile: 5550101
Address: 1 Synthetic Way
```

**Check:** the values you entered in the app come back with no credentials. This is the demonstrated exposure.

### 8. Compare the result with the deployed rule

**Where:** host shell, repository root.

```bash title="08 · Show the committed Storage rule"
sed -n '1,20p' engineering/lab27/storage.rules
```

Expected: the `match /{allPaths=**}` block contains `allow read, write: if true;`.

**Check:** the rule that permits your unauthenticated read is the same rule committed in the repository. Without that rule text, the read alone would be an unexpected response, not a complete configuration finding.

!!! important "Key observation"
    The app's login and passcode are local UI controls. The Storage rule is the actual boundary, and here it allows any client that can reach the emulator to read and write every object. The finding needs both parts: the unauthenticated read and the permissive rule that explains it. This lab demonstrates the configuration on a synthetic local emulator; it does not test an upstream project.

## Troubleshooting

- **`reset.sh` cannot start the emulator:** check that ports `9199` and `4000` are free, run `./engineering/lab27/stop.sh`, then retry. If it still fails, read `engineering/lab27/.runtime/emulator.log`.
- **The app shows network errors or the object never appears:** confirm the emulator has a route to the host alias `10.0.2.2` and that the approved firewall allows loopback port `9199`. Then restart the app and save again. Inspect app logs with `adb logcat --pid=$(adb shell pidof com.BugBazaar.lab27)`.
- **The object prefix differs from the example:** use the exact prefix from your object list. The prefix is the emulator's manufacturer and model, not a fixed value.
- **The app is already installed with a different signature:** the Lab 27 variant has its own package. If `com.BugBazaar.lab27` is present but not yours, use a fresh disposable emulator; do not uninstall the official `com.BugBazaar`.
- **The passcode is unknown:** app state is disposable. Use a fresh emulator, or clear only `com.BugBazaar.lab27` with `adb shell pm clear com.BugBazaar.lab27`. Never clear the official app.
- **Permission prompts keep appearing:** deny them again. They do not affect the Storage exercise.

## Evidence

Submit a sanitized record with these items. Each maps to the step that produces it.

- [ ] **Emulator baseline:** the `reset.sh` output showing `127.0.0.1:9199` and both seeded object names (Step 1).
- [ ] **Baseline object list:** the JSON list showing bucket `lab27-local.appspot.com` and the two seeded objects (Step 1).
- [ ] **Unauthenticated seeded read:** the exact `curl` command and its output for `alice-lab27/userinfo.txt` (Step 2).
- [ ] **Artifact identity:** the APK SHA-256 check result and the installed package path (Step 3).
- [ ] **Local configuration:** the three identifiers from `google-services.json` (Step 3).
- [ ] **App-written object:** the object list entry showing your `<device-name>/userinfo.txt` (Step 6).
- [ ] **Unauthenticated app-written read:** the exact `curl` command and its output for your object (Step 7).
- [ ] **Rule text:** the `allPaths` block with `allow read, write: if true;` (Step 8).
- [ ] **Limits:** one sentence stating that this is a local synthetic emulator, not an upstream project, and that the app login is not the storage boundary (Steps 2 and 8).

Redact any token, key, or unrelated device content. The synthetic fixture values themselves may be submitted; they are not real personal data.

<details markdown="1">
<summary>Hints</summary>

1. The app uses Firebase Storage, not Firestore. Look for `FirebaseStorage` and `userinfo.txt`, not a document collection.
2. The read does not need a Firebase account or token. The rule decides the result.
3. The device-name prefix comes from `Build.MANUFACTURER` and `Build.MODEL`; read it from the object list instead of guessing it.
4. A read without the matching rule is an observation. The rule makes it a configuration finding.

</details>

## Vulnerability and Impact

The Storage rule allows unauthenticated reads and writes for every object under the bucket. Anyone who can reach the emulator can enumerate and read stored profile records, and can overwrite them. In a deployed app with the same rule, that would expose every user's stored profile data and allow tampering, independent of the app's login screen.

The evidence here is limited to the local synthetic emulator and the published APK. It does not prove that an upstream project uses the same rule, and it does not test a production service. The impact in a real deployment is potential until the same rule and client path are confirmed in an authorized environment.

## Cleanup and review

Stop the emulator when the lab ends:

```bash title="Cleanup · Stop the local emulator"
./engineering/lab27/stop.sh
```

If you no longer need the app in this disposable emulator, remove only the Lab 27 package:

```bash title="Cleanup · Remove the Lab 27 variant"
adb uninstall com.BugBazaar.lab27
```

Do not uninstall or clear the official `com.BugBazaar` package. The next `reset.sh` restores the documented synthetic baseline.

Review:

1. Which control did you bypass: the app login, the device passcode, or the Storage rule?
2. What would a correct rule look like if each user should read only their own object?
3. Why is a permissive rule still a server-side issue even when the mobile UI looks protected?
