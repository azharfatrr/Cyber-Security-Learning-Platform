# BugBazaar setup

Complete [Common prerequisites](00-common-setup.md) and run the LabKit bootstrap once. Then follow this page to prepare the bundled BugBazaar APKs for Labs 27, 29, and 30. You do not build the apps from source. Lab 27 uses a separately built variant and a local Firebase emulator. For Lab 30, your Android emulator must support runtime instrumentation with Frida.

**Status:** The official APK hash and the Module 29 and 30 workflows were verified on 2 November 2026 on Android 14 / API 34. The Lab 27 variant and its local emulator workflow were also tested on 2 November 2026 on Android 14 / API 34. Other emulator images may behave differently.

The official APK includes configuration for an upstream Firebase project, a Firebase Storage flow, and a first-run path that downloads another APK. Labs 29 and 30 use local app functionality and need no external network access. Keep the emulator on the approved egress-restricted lab network; do not allow public or corporate access or contact the upstream Firebase project or downloader. Lab 27 uses the separate `bugbazaar-lab27-emulator.apk`, which points only at the local emulator on the host loopback path.

## Pinned release and artifacts

All four verified APKs are included in the LabKit; see [Lab downloads](downloads.md) for the single archive, hashes, and attribution.

- Official target APK: `BugBazaar_v1.2.1.apk`.
- Pinned source revision: [`fef6a899a684245eb70b2ab4be926f62be849ed9`](https://github.com/payatu/BugBazaar/tree/fef6a899a684245eb70b2ab4be926f62be849ed9).
- Target APK SHA-256: `c307c7856b270da40357006eaa763c06bcdc2913d0d0b0bab7e0b2ed564f5f4c`.
- The release APK embeds app version `1.0` (version code `1`), not `1.2.1`.
- Lab 27 variant: `bugbazaar-lab27-emulator.apk`, package `com.BugBazaar.lab27`, SHA-256 `b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604`.
- Lab 29 also requires the prebuilt ordinary-caller APK, `module-29-caller.apk`. Its SHA-256 is `5f8d04886763a4d543cd66222d1f1de7d9f14e2fe73d96a6013754bcc55728cc`. Do not build or substitute another caller.

Use the supported disposable emulator with ADB access on the restricted lab network described in [Common prerequisites](00-common-setup.md). Do not use a personal phone, real contacts, or personal addresses. Install an APK from the LabKit directory with `./install-apk.sh <apk-filename>`; do not copy APKs from a repository checkout. If the network egress policy, package identity, or an existing installation cannot be verified, stop rather than replacing or clearing emulator state.

## Network policy for local labs

Before launching BugBazaar for Labs 29 or 30, confirm that the disposable emulator's network policy blocks egress to public and corporate networks, including the upstream Firebase project and the first-run APK download host. These local exercises need no external connection. Configure this at the approved VM, firewall, or virtual-network boundary; do not rely on ADB connectivity or the emulator's Wi-Fi indicator as proof that egress is blocked. If you cannot confirm the policy, stop. Lab 27 is separate: its variant app uses only the local Firebase Storage emulator through the host loopback path, and the emulator ports must not be exposed beyond the disposable lab.

## 1. Verify and install the target APK

Run on the host, from the extracted LabKit directory:

```bash title="01 · Verify and install BugBazaar"
./install-apk.sh BugBazaar_v1.2.1.apk
```

!!! success "Expected"
    The LabKit hash and installed APK hash match; package metadata reports version name `1.0` / version code `1`. A checksum, ADB, or installation error stops this procedure. If a pre-existing installation does not match, do not replace, uninstall, or clear it; use a fresh disposable emulator. Package metadata alone cannot distinguish this release from older versions.

## 2. Disable the first-run downloader before launch

This debug APK's first-run path can download another APK from GitHub. Preserve existing preferences: if `MyAppPreferences.xml` already exists, accept it only if it already contains `isFirstRun=false`; otherwise stop without changing it. Create the small guard only when the file is absent:

```bash title="02 · Set the first-run download guard"
set -euo pipefail
SERIAL=emulator-5554
adb -s "$SERIAL" shell "run-as com.BugBazaar sh -c 'if [ -e shared_prefs/MyAppPreferences.xml ]; then grep -Fq \"name=\\\"isFirstRun\\\" value=\\\"false\\\"\" shared_prefs/MyAppPreferences.xml || { echo \"Existing preferences do not have isFirstRun=false; stopping without changes.\" >&2; exit 1; }; else mkdir -p shared_prefs && printf \"%s\\\\n\" \"<map>\" \"<boolean name=\\\"isFirstRun\\\" value=\\\"false\\\" />\" \"</map>\" > shared_prefs/MyAppPreferences.xml; fi'"
adb -s "$SERIAL" shell 'run-as com.BugBazaar grep -Fq "name=\"isFirstRun\" value=\"false\"" shared_prefs/MyAppPreferences.xml'
adb -s "$SERIAL" shell 'run-as com.BugBazaar cat shared_prefs/MyAppPreferences.xml'
```

!!! success "Expected"
    The output contains `<boolean name="isFirstRun" value="false" />`. If `run-as` fails or the value is not `false`, stop; do not launch the app. Existing preferences are never overwritten. In the absent-file case this creates only the first-run guard; it does not modify the database.

## 3. Install the prebuilt Module 29 caller APK

The caller is a separate ordinary app with its own package and UID. Install the bundled `module-29-caller.apk`, but do not launch it until Lab 29 has created or confirmed its synthetic marker record.

Run from the extracted LabKit directory:

```bash title="03 · Verify and install the caller APK"
./install-apk.sh module-29-caller.apk
```

!!! success "Expected"
    The installer succeeds only if the installed caller's APK hash matches the published hash.

If a different caller is already installed, do not replace or uninstall it; use a fresh disposable emulator. The caller is read-only and has no declared permissions. Lab 29 uses its distinct UID to demonstrate ordinary-app access; an `adb shell content query` is not an equivalent check.

## 4. Install the Lab 27 variant

The Lab 27 app is a separate package (`com.BugBazaar.lab27`) built from the same pinned source. It can be installed alongside the official app without uninstalling or clearing either one. Install it only when you are doing Lab 27.

```bash title="04 · Verify and install the Lab 27 variant"
./install-apk.sh bugbazaar-lab27-emulator.apk
```

!!! success "Expected"
    The installer succeeds only if the installed Lab 27 APK hash matches the published hash. Package metadata reports version name `1.0` / version code `1` for `com.BugBazaar.lab27`. If a different package with this ID is already installed, stop and use a fresh disposable emulator.

## Ready for a lab

BugBazaar is ready for Labs 29–30 only when the target APK and, for Lab 29, the caller APK match their expected hashes, the first-run guard reads back correctly, and the restricted egress policy is confirmed. For Lab 27, the variant must match its expected hash and the local emulator must be running as described on the [Lab 27 page](27-cloud-database.md). Return to the selected lab for scenario-specific accounts, data, and exercise steps.
