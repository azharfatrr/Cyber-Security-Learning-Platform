#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$LAB_DIR/../.." && pwd)"
WORK_DIR="$LAB_DIR/.work"
SRC_DIR="$WORK_DIR/BugBazaar"
TARBALL="$WORK_DIR/BugBazaar-fef6a899.tar.gz"
REVISION="fef6a899a684245eb70b2ab4be926f62be849ed9"

mkdir -p "$WORK_DIR"
if [ ! -d "$SRC_DIR" ]; then
  curl -fL --retry 3 -o "$TARBALL" \
    "https://codeload.github.com/payatu/BugBazaar/tar.gz/$REVISION"
  mkdir -p "$SRC_DIR"
  tar xzf "$TARBALL" -C "$SRC_DIR" --strip-components=1
  python3 "$LAB_DIR/prepare.py" "$SRC_DIR"
fi

SDK_DIR="${ANDROID_HOME:-$HOME/Android/Sdk}"
printf 'sdk.dir=%s\n' "$SDK_DIR" > "$SRC_DIR/local.properties"

(cd "$SRC_DIR" && ./gradlew --no-daemon assembleDebug)
cp "$SRC_DIR/app/build/outputs/apk/debug/app-debug.apk" \
  "$ROOT_DIR/docs/assets/apk/bugbazaar-lab27-emulator.apk"
sha256sum "$ROOT_DIR/docs/assets/apk/bugbazaar-lab27-emulator.apk"
