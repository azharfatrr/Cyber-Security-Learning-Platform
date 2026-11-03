# Common prerequisites

Use an isolated, disposable lab. Never expose these deliberately vulnerable apps and services to the internet or corporate networks. LabKit is an optional setup convenience; you can prepare the same tools and verified artifacts independently.

## Host requirements

- Use an approved disposable Linux x86_64 VM for the documented commands and pinned tools.
- Install Bash, Git, curl and `sha256sum`.
- For the Devom backend, install Python 3.12 or newer with `venv` and `ensurepip`. The loopback walkthroughs were tested with Python 3.14 and Flask 3.1.3.
- For Lab 27, install Java 17 or newer and Node.js 20 or newer for the emulator UI. Only repository-based preparation needs npm; the download includes the standalone CLI and emulator dependencies. These are separate from your host tools.
- For Lab 30, install Python with `venv` and `ensurepip` for Frida, and Java for JADX 1.5.1.
- Docker is optional for Devom. Android Studio is optional if you already have the Android SDK and emulator image.

## Android emulator

- For BugBazaar Labs 27, 29 and 30, prepare a disposable Android 14 / API 34 x86_64 emulator and boot it before setup.
- Install Android SDK Platform Tools (`adb`) on the host. Check `adb devices -l`; use only your authorized emulator with state `device`.
- For Lab 30, the emulator must permit the documented `su` and Frida server workflow. LabKit does not root an emulator or make an incompatible image instrumentable.
- Devom's seven API walkthroughs run against the host backend and do not require the Android app. If you use that optional app, prepare the same disposable emulator and the approved local backend route.
- Do not use a personal phone. Do not reset, uninstall or clear an existing app to force setup through; use a fresh disposable emulator if its identity or state is uncertain.

## Common tools

- Use a host terminal for Bash, `curl`, Python and ADB commands; use the emulator for app interactions.
- Use an editor to inspect the pinned source. Lab 09 also needs a browser for Devom's local admin console.
- An API client or debugging proxy is optional where the lab offers it. Keep it local; never publicly forward a proxy or service.
- Verify APK hashes against [Lab downloads](downloads.md), whether you use the optional installer or prepare files yourself. Do not substitute another build with the same package name.

## Lab-specific tools

- Labs 09, 10, 14, 24, 25, 26 and 28: the pinned Devom backend and its hash-locked Python dependencies. Lab 09 uses PyJWT; Lab 14 uses `requests`, both included in that lock. Follow [Devom setup](01-devom-setup.md).
- Lab 27: Firebase CLI `15.34.2`, Storage rules runtime `1.1.3`, emulator UI `1.15.0`, local configuration, lifecycle scripts, synthetic fixtures and verified `bugbazaar-lab27-emulator.apk`. All are in the download; you do not need to fetch them separately. See the preparation paths below.
- Lab 29: the verified official BugBazaar APK and prebuilt `module-29-caller.apk`. No Android build toolchain is needed.
- Lab 30: Frida client/server `17.4.2` (Android x86_64 server), `frida-tools` `14.4.6`, JADX `1.5.1`, the reviewed hook and the verified official BugBazaar APK. Only this lab needs runtime instrumentation.

## Optional LabKit setup

Download and verify the single [LabKit archive](downloads.md), extract it, then run these commands from the extracted `LabKit` directory:

```bash
./setup.sh --check
./setup.sh
```

The first command checks prerequisites without changing files or device state. The second prepares all ten labs, so it requires the full host tool list and a booted compatible emulator even if you plan to run only a Devom API lab.

Setup prepares the pinned Devom source and dependencies, Frida and JADX, and verifies the included Firebase tools. Lab 27 can skip this bootstrap entirely: the archive already includes its dependencies. Setup does not install or launch apps, clear app data, or copy `frida-server` onto the emulator. Follow the target setup page before launching an app.

## Independent preparation

You can skip `setup.sh` and prepare only the tools your selected lab needs. The walkthroughs use a common directory layout so their commands work with either preparation path. Run preparation commands in Bash with `set -euo pipefail`; if a command fails, stop rather than continuing to the next block.

### Prepare a workspace and verified artifacts

Choose one source:

- Extract and verify the archive on [Lab downloads](downloads.md). From its `LabKit` directory, run `sha256sum --check manifest.sha256`. You can use its files without running the bootstrap.
- Or clone this platform's [repository](https://github.com/azharfatrr/Cyber-Security-Learning-Platform) and assemble a fresh workspace from its versioned files. From the repository root:

```bash
git rev-parse HEAD  # Record the platform revision used for your evidence
WORKSPACE="$PWD/lab-workspace"
mkdir "$WORKSPACE"  # Choose a new directory; stop if it already exists
cp -R labkit/payload/. "$WORKSPACE/"
mkdir "$WORKSPACE/apk"
cp labkit/input/apk/*.apk "$WORKSPACE/apk/"
cp labkit/install-apk.sh "$WORKSPACE/"
sed 's|  |  apk/|' labkit/manifest.sha256 > "$WORKSPACE/manifest.sha256"
cp labkit/manifest.sha256 "$WORKSPACE/apk/manifest.sha256"
cd "$WORKSPACE/apk"
sha256sum --check manifest.sha256
cd "$WORKSPACE"
mkdir .labkit
```

Compare the four APK hashes with [Lab downloads](downloads.md) as well. Stop on any mismatch. This repository path includes the Lab 27 support files and Lab 30 hook; do not fetch replacements from unrelated sites. The public site offers no standalone APK downloads.

From here, "workspace" means either this directory or the extracted `LabKit` directory. Prepare the relevant tool below, then follow [Devom setup](01-devom-setup.md) or [BugBazaar setup](02-bugbazaar-setup.md).

### APK installation without the helper

The target pages show `./install-apk.sh` as a convenience. You can instead install with ADB after verifying the same hashes. From the workspace, choose the exact APK and package pair from [Lab downloads](downloads.md). This example is for the official BugBazaar APK; change both values together for another target:

```bash
set -euo pipefail
SERIAL=emulator-5554  # Replace with your authorized emulator's serial
APK=BugBazaar_v1.2.1.apk
PACKAGE=com.BugBazaar
sha256sum --check manifest.sha256
test "$(adb -s "$SERIAL" shell getprop ro.kernel.qemu | tr -d '\r')" = 1
test "$(adb -s "$SERIAL" shell getprop ro.build.version.sdk | tr -d '\r')" = 34
test "$(adb -s "$SERIAL" shell getprop ro.product.cpu.abi | tr -d '\r')" = x86_64
PACKAGES=$(adb -s "$SERIAL" shell pm list packages "$PACKAGE" | tr -d '\r')
if printf '%s\n' "$PACKAGES" | grep -Fxq "package:$PACKAGE"; then
  echo 'Package already installed; stopping without changes.' >&2
  exit 1
fi
adb -s "$SERIAL" install "apk/$APK"
INSTALLED=$(adb -s "$SERIAL" shell pm path "$PACKAGE" | tr -d '\r')
test "$(printf '%s\n' "$INSTALLED" | grep -c '^package:')" = 1
EXPECTED=$(sha256sum "apk/$APK"); EXPECTED=${EXPECTED%% *}
ACTUAL=$(adb -s "$SERIAL" shell sha256sum "${INSTALLED#package:}")
test "${ACTUAL%% *}" = "$EXPECTED"
```

Stop on any failure. If a package is already installed, use the helper to check it without changes or use a fresh disposable emulator. Installation does not launch an app; BugBazaar still needs the first-run guard and egress checks on its setup page.

### Devom backend

Follow the independent backend preparation in [Devom setup](01-devom-setup.md#independent-backend-preparation). It checks out the exact reviewed commit into `.labkit/Devom` and installs the workspace's hash-locked dependencies.

### Lab 27 Firebase tooling

If you extracted and verified the download, skip these installation commands. It already contains `lab27/firebase-tools-linux` and the Storage runtime/UI under `lab27/emulators/`. With your host tools and Android emulator ready, install the verified variant using BugBazaar setup, then follow Lab 27's `./lab27/reset.sh` step. First start unpacks the bundled UI locally; it needs no dependency download or Firebase login.

Only the repository-only path needs the commands below. From that workspace, install the CLI using the included package lock and prepare the Storage runtime and UI. Do not run `firebase login`, create a cloud project or deploy the rules:

```bash
(cd lab27 && npm ci --no-audit --no-fund)
test "$(lab27/node_modules/.bin/firebase --version)" = '15.34.2'
mkdir -p .labkit/home
(cd lab27 && HOME="$PWD/../.labkit/home" \
  ./node_modules/.bin/firebase setup:emulators:storage)
(cd lab27 && HOME="$PWD/../.labkit/home" \
  ./node_modules/.bin/firebase setup:emulators:ui)
printf '%s  %s\n' \
  0cd52db6f6271d62078f805220706377c849220b73bd68aa27078d977df9c900 \
  .labkit/home/.cache/firebase/emulators/cloud-storage-rules-runtime-v1.1.3.jar \
  | sha256sum --check -
printf '%s  %s\n' \
  97d8c4c574e3f20c4d690a2ce8373eef76ab024da73279a062dba8517f88cf9a \
  .labkit/home/.cache/firebase/emulators/ui-v1.15.0.zip \
  | sha256sum --check -
```

Stop if installation, the CLI version check or the runtime hash check fails. The runtime cache must stay under `.labkit/home`: the bundled lifecycle scripts select that home directory. Return to [Lab 27](27-cloud-database.md) to reset, start and seed the local emulator.

### Lab 30 analysis and instrumentation tools

From the workspace, create the Frida environment using the included hash lock:

```bash
python3 -m venv .labkit/frida-venv
.labkit/frida-venv/bin/python -m pip install --require-hashes \
  -r tools/frida-requirements.lock
.labkit/frida-venv/bin/python -m pip check
.labkit/frida-venv/bin/frida --version
```

The version must be `17.4.2`. Download the pinned analysis tools from their official releases and verify the compressed files before extracting them:

```bash
mkdir -p .labkit/downloads .labkit/tools
curl --fail --location \
  https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip \
  -o .labkit/downloads/jadx-1.5.1.zip
curl --fail --location \
  https://github.com/frida/frida/releases/download/17.4.2/frida-server-17.4.2-android-x86_64.xz \
  -o .labkit/downloads/frida-server-17.4.2-android-x86_64.xz
sha256sum --check <<'EOF'
12fd966431903b8e15c36e5007f19343475be7d8f2a55f082e7a929eeabc937e  .labkit/downloads/jadx-1.5.1.zip
e06a36e1eb00d1b08842f32b018783f2bd0f2bbcb2aca2ec26eda98cb0f3680c  .labkit/downloads/frida-server-17.4.2-android-x86_64.xz
EOF
```

Stop on a mismatch. Extract only after both checks succeed, into fresh destinations:

```bash
test ! -e .labkit/jadx
test ! -e .labkit/tools/frida-server-17.4.2-android-x86_64
python3 - <<'PY'
import lzma
from pathlib import Path
from zipfile import ZipFile
with ZipFile('.labkit/downloads/jadx-1.5.1.zip') as archive:
    archive.extractall('.labkit/jadx')
server = Path('.labkit/tools/frida-server-17.4.2-android-x86_64')
with lzma.open('.labkit/downloads/frida-server-17.4.2-android-x86_64.xz', 'rb') as source:
    with server.open('xb') as output:
        output.write(source.read())
server.chmod(0o755)
for executable in Path('.labkit/jadx/bin').iterdir():
    executable.chmod(0o755)
PY
printf '%s  %s\n' \
  23ad2e64028e3aa778731ec3019d8bde4314d0d5894892e18bae2256c18293c9 \
  .labkit/tools/frida-server-17.4.2-android-x86_64 | sha256sum --check -
.labkit/jadx/bin/jadx --version
```

Confirm JADX reports `1.5.1` and the server hash is `OK`. Lab 30 explains how to verify and copy the server to your selected emulator; preparation alone does not start instrumentation.

## Network safety

During dependency preparation, restrict host egress to the required GitHub release/source hosts, PyPI (`pypi.org`, `files.pythonhosted.org`), npm (`registry.npmjs.org`) and Google Storage (`storage.googleapis.com`), including their release download redirects. After preparation, remove bootstrap egress allowances.

- Devom: allow only the approved local backend route. Restrict its all-interface debug server with the host firewall.
- BugBazaar Labs 29 and 30: block all external egress, including the upstream Firebase project and first-run downloader.
- Lab 27: permit only the local host/emulator path (`10.0.2.2:9199` from Android). Keep host services on loopback and never expose ports `9199` or `4000` to a LAN or the internet.

## Safe use and evidence

Use only synthetic records and lab-only accounts. Never use real contacts, production accounts or personal data. Keep sanitized requests, responses and screenshots with timestamps; redact tokens and sensitive fields. Stop if an endpoint, package or network path does not match the approved lab.

The optional installer verifies APK hashes and refuses to replace an installed package with a different hash. Independent installation must preserve the same checks; see the target setup pages. Values such as `$TOKEN` and `$USER_ID` must come from your own lab session; do not submit placeholders unchanged.
