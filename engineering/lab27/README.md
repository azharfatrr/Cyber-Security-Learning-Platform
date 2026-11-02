# Lab 27 local emulator fixture

This directory builds and runs the Lab 27 variant of BugBazaar against a local Firebase Storage emulator. It is maintainer tooling; learners use the published APK and the commands on [Lab 27](../docs/27-cloud-database.md).

## Pinned inputs

- BugBazaar source: `fef6a899a684245eb70b2ab4be926f62be849ed9`
- Firebase CLI: `firebase-tools@15.34.2` (locked in `package.json` / `package-lock.json`)
- Gradle wrapper: 8.4
- Android Gradle plugin: 8.3.1
- Android NDK: 26.1.10909125
- JDK used for verification: OpenJDK 21.0.12.1
- Package: `com.BugBazaar.lab27`
- Firebase project ID: `lab27-local`
- Storage bucket: `lab27-local.appspot.com`
- Storage emulator: `127.0.0.1:9199`
- Emulator UI: `127.0.0.1:4000`

## Layout

- `prepare.py` applies the Lab 27 changes to a fresh checkout of the pinned source.
- `build.sh` downloads the pinned source into `.work/`, applies `prepare.py`, builds, and copies the APK to `docs/assets/apk/bugbazaar-lab27-emulator.apk`.
- `google-services.json` is the local-only Firebase configuration. Its project number and API key are placeholders, not credentials for a cloud project.
- `firebase.json`, `storage.rules`, and `package.json` configure the emulator.
- `start.sh`, `stop.sh`, `reset.sh`, and `seed.sh` manage the emulator lifecycle.
- `fixtures/` contains the deterministic synthetic seed objects.

## Source changes

`prepare.py` makes only these changes:

1. Pin `ndkVersion '26.1.10909125'`.
2. Replace the retired `jcenter()` repository with `google()` and `mavenCentral()`.
3. Set `applicationId` to `com.BugBazaar.lab27` so the variant installs beside the official app.
4. Rename the content-provider authorities and the contacts permission to the `.lab27` namespace.
5. Rename the launcher label to `BugBazaar Lab 27`.
6. Remove the unused Firebase Cloud Messaging service declaration.
7. Add `firebaseStorage.useEmulator("10.0.2.2", 9199)` after Storage initialization.
8. Replace `app/google-services.json` with the local-only project configuration.

The Storage upload scenario itself is unchanged: saving a profile writes `userinfo.txt` under a prefix derived from the device name.

## Build

Requirements: Android SDK with build-tools and NDK 26.1.10909125, JDK 17 or newer, `curl`, `tar`, and Python 3.

```bash
./build.sh
sha256sum ../../docs/assets/apk/bugbazaar-lab27-emulator.apk
```

The verified artifact for this revision is:

```text
b3f0249634f7bc401fb79c43eb7f6093a030501b4d36a7e0c05864cbb8041604
```

Delete `.work/BugBazaar` before rebuilding if you change `prepare.py`.

## Emulator lifecycle

Install the pinned CLI once:

```bash
npm install --no-audit --no-fund
```

From the repository root:

```bash
./engineering/lab27/reset.sh   # stop, clear runtime state, start, seed
./engineering/lab27/start.sh   # start only
./engineering/lab27/seed.sh     # re-upload fixtures
./engineering/lab27/stop.sh     # stop and remove the PID file
```

`reset.sh` is the deterministic baseline. It clears `.runtime/`, starts the emulator, and uploads:

- `alice-lab27/userinfo.txt`
- `bob-lab27/userinfo.txt`

Inspect the baseline from the host:

```bash
curl -fsS 'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o'
curl -fsS 'http://127.0.0.1:9199/v0/b/lab27-local.appspot.com/o/alice-lab27%2Fuserinfo.txt?alt=media'
```

The Storage emulator binds to `127.0.0.1` only. The Android emulator reaches it through the host alias `10.0.2.2`. On the AVD used for verification, the app-derived prefix was `Google sdk_gphone64_x86_64`; it depends on the emulator's manufacturer and model.

## Security notes

- `storage.rules` is deliberately permissive (`allow read, write: if true`) because the exercise is to observe an unauthenticated read. Never deploy these rules to a cloud project.
- Use synthetic data only. The fixtures contain reserved example domains and 555 numbers.
- Keep the emulator ports on host loopback. Do not expose them to a LAN or the internet.
- The app's `10.0.2.2` endpoint is the Android emulator's host alias, not a public address.

## Verification performed

On 2 November 2026, on Android 14 / API 34:

1. `reset.sh` started the emulator and seeded the two fixture objects.
2. The APK installed as `com.BugBazaar.lab27` alongside the official `com.BugBazaar`.
3. The app logged in, created a passcode, and saved a synthetic profile.
4. `Google sdk_gphone64_x86_64/userinfo.txt` appeared in the emulator.
5. An unauthenticated read returned the saved values.

The learner page records the exact commands and observed output.
