#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
SCRIPT_DIR="${SCRIPT_PATH%/*}"
if [[ "$SCRIPT_DIR" == "$SCRIPT_PATH" ]]; then
  SCRIPT_DIR="."
fi
KIT_ROOT="$(cd "$SCRIPT_DIR" && pwd -P)"

fail() {
  printf 'LabKit install: %s\n' "$*" >&2
  exit 1
}

[[ $# -eq 1 ]] || fail "Usage: ./install-apk.sh <apk-filename>"
case "$1" in
  Dvom.apk) package="com.example.vulnappowasp" ;;
  BugBazaar_v1.2.1.apk) package="com.BugBazaar" ;;
  module-29-caller.apk) package="org.lab.module29caller" ;;
  bugbazaar-lab27-emulator.apk) package="com.BugBazaar.lab27" ;;
  *) fail "Unknown APK '$1'; choose a filename listed in manifest.sha256." ;;
esac

for name in adb sha256sum tr sed; do
  command -v "$name" >/dev/null 2>&1 || fail "Required host tool '$name' is missing."
done
apk="$KIT_ROOT/apk/$1"
[[ -f "$apk" ]] || fail "APK not found: $apk"
expected=""
while read -r digest filename; do
  [[ "$filename" == "apk/$1" ]] && expected="$digest"
done < "$KIT_ROOT/manifest.sha256"
[[ -n "$expected" ]] || fail "APK is not pinned in manifest.sha256."
printf '%s  %s\n' "$expected" "$apk" | sha256sum --check --status \
  || fail "APK failed its manifest SHA-256 check: $1"

connected=()
serial=""
state=""
rest=""
while read -r serial state rest; do
  [[ -z "${serial:-}" || "$serial" == "List" ]] && continue
  [[ "${state:-}" == "device" ]] && connected+=("$serial")
done < <(adb devices)
if [[ -n "${LABKIT_SERIAL:-}" ]]; then
  found=false
  for serial in "${connected[@]}"; do
    [[ "$serial" == "$LABKIT_SERIAL" ]] && found=true
  done
  [[ "$found" == true ]] || fail "LABKIT_SERIAL '$LABKIT_SERIAL' is not an authorized connected device."
  serial="$LABKIT_SERIAL"
else
  ((${#connected[@]} == 1)) || fail "Connect exactly one authorized emulator, or set LABKIT_SERIAL when multiple devices are attached."
  serial="${connected[0]}"
fi

qemu="$(adb -s "$serial" shell getprop ro.kernel.qemu | tr -d '\r')"
[[ "$qemu" == "1" ]] || fail "An Android emulator is required; '$serial' is not identified as an emulator."
api="$(adb -s "$serial" shell getprop ro.build.version.sdk | tr -d '\r')"
abi="$(adb -s "$serial" shell getprop ro.product.cpu.abi | tr -d '\r')"
[[ "$api" == "34" && "$abi" == "x86_64" ]] \
  || fail "Expected Android API 34 / x86_64; '$serial' reports API ${api:-unknown} / ABI ${abi:-unknown}."

mapfile -t installed_paths < <(adb -s "$serial" shell pm path "$package" | tr -d '\r' | sed -n 's/^package://p')
if ((${#installed_paths[@]})); then
  ((${#installed_paths[@]} == 1)) || fail "Multiple installed APK splits found for $package; use a fresh disposable emulator."
  installed_hash_line="$(adb -s "$serial" shell sha256sum "${installed_paths[0]}")"
  installed_hash="${installed_hash_line%% *}"
  [[ "$installed_hash" == "$expected" ]] \
    || fail "Installed $package has a different APK hash; it was not replaced or cleared. Use a fresh disposable emulator."
  printf '%s is already installed with the verified hash; no change made.\n' "$package"
  exit 0
fi

adb -s "$serial" install "$apk"
mapfile -t installed_paths < <(adb -s "$serial" shell pm path "$package" | tr -d '\r' | sed -n 's/^package://p')
((${#installed_paths[@]} == 1)) || fail "Could not verify the installed package path for $package."
installed_hash_line="$(adb -s "$serial" shell sha256sum "${installed_paths[0]}")"
installed_hash="${installed_hash_line%% *}"
[[ "$installed_hash" == "$expected" ]] || fail "Installed APK hash did not match the pinned artifact."
printf 'Installed and verified %s on %s. The app was not launched.\n' "$package" "$serial"
