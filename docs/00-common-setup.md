# Common prerequisites

**Status:** Shared safety and tooling guidance for all labs. Use an isolated, disposable lab. These deliberately vulnerable apps and services must not be exposed to the internet or corporate networks.

## Download and prepare the LabKit once

Download the single [LabKit for all ten labs](downloads.md), extract it, then run these commands from the extracted `LabKit` directory:

```bash
./setup.sh --check
./setup.sh
```

The first command checks prerequisites without changing files or device state. The second fetches the pinned Devom source and host dependencies, installs the locked Firebase CLI, prefetches its Storage emulator, and prepares the pinned Frida and JADX tools. It does not install or launch apps, clear app data, or copy `frida-server` onto the emulator. For a selected lab, its setup page tells you which bundled APK to install with `./install-apk.sh <apk-filename>`.

The LabKit supports **Linux x86_64** and requires Bash, Python 3.12 or newer with `venv` and `ensurepip`, Git, curl, `sha256sum`, Node.js 20 or newer, npm, Java 17 or newer, and Android SDK Platform Tools (`adb`). It also requires an already installed and booted disposable Android 14 / API 34 x86_64 instrumentable emulator. Android Studio, SDK components, and emulator system images are not included. The LabKit is a one-time manual download, not an offline bundle: first-time setup contacts the pinned GitHub, PyPI, npm, and Google Storage sources and may download large analysis-tool packages.

Keep setup egress restricted to the documented package/release endpoints and their download hosts. After setup, apply the more restrictive runtime policy below; do not leave broad bootstrap egress enabled for a lab.

## Choose a target setup

Complete the one-time LabKit setup, then prepare the target used by your lab:

- [Devom setup](01-devom-setup.md) for Labs 09, 10, 14, 24, 25, 26, and 28.
- [BugBazaar setup](02-bugbazaar-setup.md) for Labs 27, 29, and 30. Lab 27 uses the included repository-built variant and local Firebase Storage emulator; complete its Lab 27 section.

The setup pages identify each target's reviewed revision and artifact identity. Provenance, hashes, and redistribution notes are on [Lab downloads](downloads.md) and in the repository `NOTICE`.

## Shared environment and tools

Use an approved disposable VM and the supported Android emulator with synthetic data. Use an API client or debugging proxy only for labs that require one, and keep it local to the isolated environment.

Use the same network-safety baseline for both targets: block public and corporate access, restrict network egress, and allow only the path required for the selected lab. Devom may need an approved local route from the emulator to its backend. BugBazaar Labs 29–30 need no external network access; Lab 27 uses only the local emulator on the host loopback path. Do not publicly forward a proxy or service.

Android Studio is not required just to install the supplied APKs; the Android SDK and emulator image must already be available. Docker is optional for the Devom backend. Lab 30 additionally needs an instrumentable emulator that permits the documented Frida workflow; the LabKit cannot make an incompatible or non-instrumentable emulator suitable for that exercise.

## Safe use and evidence

Do not use a personal phone, real contacts, production accounts, or personal data. Use only synthetic records and lab-only accounts. Keep sanitized requests, responses, and screenshots with timestamps; redact tokens and sensitive fields. Stop if an endpoint, package, or network path does not match the approved lab environment.

The installer verifies the APK against the bundled manifest and will not replace an existing package whose installed APK hash differs. Do not uninstall or clear existing app data to force setup through; use a fresh disposable emulator instead. Values such as `$TOKEN` and `$USER_ID` must come from your own lab session; do not submit placeholders unchanged.
