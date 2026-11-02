# Common prerequisites

**Status:** Shared safety and tooling guidance for all labs. Use an isolated, disposable lab. These deliberately vulnerable apps and services must not be exposed to the internet or corporate networks.

## Choose a target setup

Complete these shared prerequisites, then prepare the target used by your lab:

- [Devom setup](01-devom-setup.md) for Labs 09, 10, 14, 24, 25, 26, and 28.
- [BugBazaar setup](02-bugbazaar-setup.md) for Labs 27, 29, and 30. Lab 27 uses the separate repository-built variant and the committed local Firebase Storage emulator; complete the Lab 27 section of that setup page.

The target setup pages pin the reviewed revisions and APK artifacts. Review each project's license before internal distribution; the verified status of each mirrored binary is recorded on [Lab downloads](downloads.md) and in the repository `NOTICE`.

## Shared environment and tools

Use an approved disposable VM and Android emulator with synthetic data. Have Android SDK Platform Tools (`adb`), Bash, `curl`, and `sha256sum` available. Use an API client or debugging proxy only for labs that require one, and keep it local to the isolated environment.

Use the same network-safety baseline for both targets: block public and corporate access, restrict network egress, and allow only the path required for the selected lab. Devom may need an approved local route from the emulator to its backend. BugBazaar Labs 29–30 need no external network access; Lab 27 uses only the local emulator on the host loopback path. Do not publicly forward a proxy or service.

Android Studio is not required just to install the supplied APKs; you can use it to manage an emulator. Docker is optional for the Devom backend and is not required for APK installation. Labs 29–30 may need a compatible instrumentable emulator and Frida tooling; use only the disposable lab device and follow the individual lab's prerequisites.

## Safe use and evidence

Do not use a personal phone, real contacts, production accounts, or personal data. Use only synthetic records and lab-only accounts. Keep sanitized requests, responses, and screenshots with timestamps; redact tokens and sensitive fields. Stop if an endpoint, package, or network path does not match the approved lab environment.

Examples use Bash on Linux. Confirm an authorized emulator is connected before installing any APK:

```bash
adb devices
```

The device should appear with status `device`. Install supplied APKs only on the disposable lab emulator. Values such as `$TOKEN` and `$USER_ID` must come from your own lab session; do not submit placeholder values unchanged.
