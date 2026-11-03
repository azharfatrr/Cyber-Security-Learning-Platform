#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIR="${SCRIPT_PATH%/*}"
if [[ "$SCRIPT_DIR" == "$SCRIPT_PATH" ]]; then
  SCRIPT_DIR="."
fi
KIT_ROOT="$(cd "$SCRIPT_DIR" && pwd -P)"
WORK_DIR="$KIT_ROOT/.labkit"

fail() {
  printf 'LabKit setup: %s\n' "$*" >&2
  exit 1
}

preflight() {
  local missing=()
  local name
  for name in bash python3 git curl sha256sum node npm java adb uname tr; do
    command -v "$name" >/dev/null 2>&1 || missing+=("$name")
  done
  if ((${#missing[@]})); then
    printf 'Missing required host tools: %s\n' "${missing[*]}" >&2
    return 1
  fi

  [[ "$(uname -s)" == "Linux" ]] || fail "Linux is required."
  [[ "$(uname -m)" == "x86_64" ]] || fail "A Linux x86_64 host is required."
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' \
    || fail "Python 3.12 or newer is required."
  python3 -c 'import ensurepip, venv' >/dev/null 2>&1 \
    || fail "Python venv support is required (install the host package that provides venv and ensurepip)."
  local node_version
  node_version="$(node --version)"
  python3 -c 'import re,sys; m=re.match(r"v?(\d+)", sys.argv[1]); sys.exit(0 if m and int(m.group(1)) >= 20 else 1)' "$node_version" \
    || fail "Node.js 20 or newer is required."
  local java_version
  java_version="$(java -version 2>&1 || true)"
  python3 -c 'import re,sys; m=re.search(r"version \"(?:1\.)?(\d+)", sys.argv[1]); sys.exit(0 if m and int(m.group(1)) >= 17 else 1)' "$java_version" \
    || fail "Java 17 or newer is required."

  local connected=() serial state rest
  while read -r serial state rest; do
    [[ -z "${serial:-}" || "$serial" == "List" ]] && continue
    [[ "${state:-}" == "device" ]] && connected+=("$serial")
  done < <(adb devices)

  if [[ -n "${LABKIT_SERIAL:-}" ]]; then
    local found=false
    for serial in "${connected[@]}"; do
      [[ "$serial" == "$LABKIT_SERIAL" ]] && found=true
    done
    [[ "$found" == true ]] || fail "LABKIT_SERIAL '$LABKIT_SERIAL' is not an authorized connected device."
    DEVICE_SERIAL="$LABKIT_SERIAL"
  else
    ((${#connected[@]} == 1)) || fail "Connect exactly one authorized emulator, or set LABKIT_SERIAL when multiple devices are attached."
    DEVICE_SERIAL="${connected[0]}"
  fi

  local qemu api abi
  qemu="$(adb -s "$DEVICE_SERIAL" shell getprop ro.kernel.qemu | tr -d '\r')"
  [[ "$qemu" == "1" ]] || fail "An Android emulator is required; '$DEVICE_SERIAL' is not identified as an emulator."
  api="$(adb -s "$DEVICE_SERIAL" shell getprop ro.build.version.sdk | tr -d '\r')"
  abi="$(adb -s "$DEVICE_SERIAL" shell getprop ro.product.cpu.abi | tr -d '\r')"
  [[ "$api" == "34" ]] || fail "Emulator API 34 is required; '$DEVICE_SERIAL' reports API ${api:-unknown}."
  [[ "$abi" == "x86_64" ]] || fail "An x86_64 emulator is required; '$DEVICE_SERIAL' reports ABI ${abi:-unknown}."
  printf 'Compatible emulator: %s (Android API %s, ABI %s).\n' "$DEVICE_SERIAL" "$api" "$abi"
}

if [[ "${1:-}" == "--check" ]]; then
  [[ $# -eq 1 ]] || fail "Usage: ./setup.sh [--check]"
  preflight
  printf 'Read-only preflight passed; no files or device state were changed.\n'
  exit 0
fi
[[ $# -eq 0 ]] || fail "Usage: ./setup.sh [--check]"
preflight

(
  cd "$KIT_ROOT"
  sha256sum --check manifest.sha256
)

# versions.env is part of the hash-verified archive.
# shellcheck disable=SC1091
source "$KIT_ROOT/tools/versions.env"
mkdir -p "$WORK_DIR/downloads" "$WORK_DIR/tools"

download_pinned() {
  local url="$1" destination="$2" expected="$3" temporary
  if [[ -e "$destination" ]]; then
    printf '%s  %s\n' "$expected" "$destination" | sha256sum --check --status \
      || fail "Cached download has the wrong SHA-256: $destination (left untouched)."
    return
  fi
  temporary="${destination}.part.$$"
  curl --fail --location --retry 3 --output "$temporary" "$url"
  if ! printf '%s  %s\n' "$expected" "$temporary" | sha256sum --check --status; then
    rm -f -- "$temporary"
    fail "Downloaded file failed its pinned SHA-256 check: $url"
  fi
  mv -- "$temporary" "$destination"
}

DEVOM_DIR="$WORK_DIR/Devom"
if [[ -d "$DEVOM_DIR/.git" ]]; then
  actual_revision="$(git -C "$DEVOM_DIR" rev-parse HEAD)"
  [[ "$actual_revision" == "$DEVOM_REVISION" ]] \
    || fail "Existing Devom checkout is at $actual_revision, not $DEVOM_REVISION; it was left untouched."
elif [[ -e "$DEVOM_DIR" ]]; then
  fail "Existing $DEVOM_DIR is not a Git checkout; it was left untouched."
else
  partial="$WORK_DIR/Devom.partial.$$"
  mkdir "$partial"
  git -C "$partial" init --quiet
  git -C "$partial" remote add origin https://github.com/memohk/Devom.git
  git -C "$partial" fetch --depth 1 origin "$DEVOM_REVISION"
  git -C "$partial" checkout --quiet --detach FETCH_HEAD
  [[ "$(git -C "$partial" rev-parse HEAD)" == "$DEVOM_REVISION" ]] \
    || fail "Fetched Devom checkout did not match the pinned revision."
  mv -- "$partial" "$DEVOM_DIR"
fi

if [[ ! -x "$DEVOM_DIR/.venv/bin/python" ]]; then
  [[ ! -e "$DEVOM_DIR/.venv" ]] || fail "Existing Devom .venv is incomplete; it was left untouched."
  python3 -m venv "$DEVOM_DIR/.venv"
fi
"$DEVOM_DIR/.venv/bin/python" -m pip install --disable-pip-version-check \
  --require-hashes --requirement "$KIT_ROOT/backend/requirements.lock"
"$DEVOM_DIR/.venv/bin/python" -m pip check

FIREBASE="$KIT_ROOT/lab27/firebase-tools-linux"
if [[ ! -x "$FIREBASE" ]]; then
  FIREBASE="$KIT_ROOT/lab27/node_modules/.bin/firebase"
fi
if [[ -x "$FIREBASE" ]]; then
  firebase_version="$(HOME="$WORK_DIR/home" "$FIREBASE" --version)"
  [[ "$firebase_version" == "15.34.2" ]] \
    || fail "Existing Firebase CLI is $firebase_version, not locked 15.34.2; it was left untouched."
elif [[ -e "$KIT_ROOT/lab27/node_modules" ]]; then
  fail "Existing lab27/node_modules is incomplete; it was left untouched."
else
  (cd "$KIT_ROOT/lab27" && npm ci --no-audit --no-fund)
fi
mkdir -p "$WORK_DIR/home"
STORAGE_RUNTIME="$WORK_DIR/home/.cache/firebase/emulators/cloud-storage-rules-runtime-v$FIREBASE_STORAGE_RUNTIME_VERSION.jar"
if [[ "$FIREBASE" == "$KIT_ROOT/lab27/firebase-tools-linux" ]]; then
  STORAGE_RUNTIME="$KIT_ROOT/lab27/emulators/cloud-storage-rules-runtime-v$FIREBASE_STORAGE_RUNTIME_VERSION.jar"
fi
if [[ -e "$STORAGE_RUNTIME" ]]; then
  printf '%s  %s\n' "$FIREBASE_STORAGE_RUNTIME_SHA256" "$STORAGE_RUNTIME" | sha256sum --check --status \
    || fail "Cached Firebase Storage emulator has the wrong SHA-256; it was left untouched."
else
  (cd "$KIT_ROOT/lab27" && HOME="$WORK_DIR/home" "$FIREBASE" setup:emulators:storage)
  printf '%s  %s\n' "$FIREBASE_STORAGE_RUNTIME_SHA256" "$STORAGE_RUNTIME" | sha256sum --check \
    || fail "Prefetched Firebase Storage emulator failed its pinned SHA-256 check."
fi

FRIDA_VENV="$WORK_DIR/frida-venv"
if [[ ! -x "$FRIDA_VENV/bin/frida" ]]; then
  [[ ! -e "$FRIDA_VENV" ]] || fail "Existing Frida environment is incomplete; it was left untouched."
  python3 -m venv "$FRIDA_VENV"
  "$FRIDA_VENV/bin/python" -m pip install --disable-pip-version-check \
    --require-hashes --requirement "$KIT_ROOT/tools/frida-requirements.lock"
fi
frida_version="$("$FRIDA_VENV/bin/frida" --version)"
[[ "$frida_version" == "$FRIDA_VERSION" ]] || fail "Frida client version mismatch: $frida_version"

JADX_ARCHIVE="$WORK_DIR/downloads/jadx-$JADX_VERSION.zip"
JADX_DIR="$WORK_DIR/jadx"
JADX_MARKER="$WORK_DIR/jadx-archive.sha256"
download_pinned "https://github.com/skylot/jadx/releases/download/v$JADX_VERSION/jadx-$JADX_VERSION.zip" \
  "$JADX_ARCHIVE" "$JADX_SHA256"
if [[ -d "$JADX_DIR" ]]; then
  [[ -f "$JADX_MARKER" && "$(cat "$JADX_MARKER")" == "$JADX_SHA256" \
    && -x "$JADX_DIR/bin/jadx-gui" ]] \
    || fail "Existing JADX directory is not the verified $JADX_VERSION install; it was left untouched."
else
  jadx_stage="$WORK_DIR/jadx.stage.$$"
  mkdir "$jadx_stage"
  python3 - "$JADX_ARCHIVE" "$jadx_stage" <<'PY'
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from zipfile import ZipFile

archive_path, destination = Path(sys.argv[1]), Path(sys.argv[2])
with ZipFile(archive_path) as archive:
    bad = archive.testzip()
    if bad:
        raise SystemExit(f"Corrupt JADX archive member: {bad}")
    root = destination.resolve()
    for info in archive.infolist():
        name = info.filename.rstrip("/")
        member = PurePosixPath(name)
        mode = info.external_attr >> 16
        if not name or member.is_absolute() or any(part in ("", ".", "..") for part in member.parts):
            raise SystemExit(f"Unsafe JADX archive path: {info.filename!r}")
        if stat.S_ISLNK(mode):
            raise SystemExit(f"JADX archive contains a symbolic link: {info.filename!r}")
        target = root.joinpath(*member.parts)
        if not target.resolve().is_relative_to(root):
            raise SystemExit(f"JADX archive path escaped destination: {info.filename!r}")
        if info.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(info) as source, target.open("wb") as output:
            output.write(source.read())
        os.chmod(target, 0o755 if mode & 0o111 else 0o644)

if not (destination / "bin" / "jadx-gui").is_file():
    raise SystemExit("Pinned JADX archive did not contain bin/jadx-gui")
PY
  mv -- "$jadx_stage" "$JADX_DIR"
  printf '%s\n' "$JADX_SHA256" > "$JADX_MARKER"
fi

FRIDA_ARCHIVE="$WORK_DIR/downloads/frida-server-$FRIDA_VERSION-android-x86_64.xz"
FRIDA_SERVER="$WORK_DIR/tools/frida-server-$FRIDA_VERSION-android-x86_64"
download_pinned "https://github.com/frida/frida/releases/download/$FRIDA_VERSION/frida-server-$FRIDA_VERSION-android-x86_64.xz" \
  "$FRIDA_ARCHIVE" "$FRIDA_SERVER_SHA256"
if [[ -e "$FRIDA_SERVER" ]]; then
  printf '%s  %s\n' "$FRIDA_SERVER_BINARY_SHA256" "$FRIDA_SERVER" | sha256sum --check --status \
    || fail "Existing Frida server binary failed its pinned SHA-256 check; it was left untouched."
else
  temporary="$FRIDA_SERVER.part.$$"
  python3 - "$FRIDA_ARCHIVE" "$temporary" <<'PY'
import lzma
import shutil
import sys
with lzma.open(sys.argv[1], "rb") as source, open(sys.argv[2], "wb") as output:
    shutil.copyfileobj(source, output)
PY
  if ! printf '%s  %s\n' "$FRIDA_SERVER_BINARY_SHA256" "$temporary" | sha256sum --check --status; then
    rm -f -- "$temporary"
    fail "Decompressed Frida server failed its pinned SHA-256 check."
  fi
  chmod 755 "$temporary"
  mv -- "$temporary" "$FRIDA_SERVER"
fi

printf '\nLabKit setup is ready. APKs were not installed and no app was launched.\n'
printf 'Install one target when needed, for example: ./install-apk.sh Dvom.apk\n'
printf 'Frida: %s/bin/frida; JADX: %s/bin/jadx-gui\n' "$FRIDA_VENV" "$JADX_DIR"
printf 'Frida server: %s (copy to the emulator only when Lab 30 requires it).\n' "$FRIDA_SERVER"
