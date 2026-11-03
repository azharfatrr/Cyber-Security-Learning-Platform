#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT_ROOT="$(cd "$LAB_DIR/.." && pwd)"
export HOME="$KIT_ROOT/.labkit/home"
export FIREBASE_EMULATORS_PATH="$HOME/.cache/firebase/emulators"
RUNTIME="$LAB_DIR/.runtime"
BUCKET="lab27-local.appspot.com"
# shellcheck source=lab27/process.sh
source "$LAB_DIR/process.sh"

mkdir -p "$RUNTIME" "$HOME"
if [ -f "$RUNTIME/emulator.pid" ]; then
  PID="$(cat "$RUNTIME/emulator.pid")"
  if lab27_process_matches "$PID" "$LAB_DIR"; then
    echo "Lab 27 emulator is already running (PID $PID)."
    exit 0
  fi
  echo "Lab 27 PID file is stale or points to another process; leaving that process alone."
  rm -f "$RUNTIME/emulator.pid"
fi

cd "$LAB_DIR"
FIREBASE=(./node_modules/.bin/firebase)
if [[ -x ./firebase-tools-linux ]]; then
  # The standalone CLI replaces its own HOME cache on first launch. Keep the
  # bundled emulator bytes outside that cache so they survive initialization.
  export FIREBASE_EMULATORS_PATH="$LAB_DIR/emulators"
  sha256sum --check <<'EOF'
87d3b99dd2650cd8a0d5aca73fcc91ba7a14501381279f10c843a067851a9187  firebase-tools-linux
0cd52db6f6271d62078f805220706377c849220b73bd68aa27078d977df9c900  emulators/cloud-storage-rules-runtime-v1.1.3.jar
97d8c4c574e3f20c4d690a2ce8373eef76ab024da73279a062dba8517f88cf9a  emulators/ui-v1.15.0.zip
EOF
  UI_DIR="$LAB_DIR/emulators/ui-v1.15.0"
  if [[ ! -f "$UI_DIR/server/server.mjs" ]]; then
    if [[ -e "$UI_DIR" ]]; then
      echo 'Incomplete emulator UI directory; stopping without overwriting it.' >&2
      exit 1
    fi
    python3 -m zipfile -e "$LAB_DIR/emulators/ui-v1.15.0.zip" "$UI_DIR"
  fi
  # Initialize the embedded CLI locally, then invoke its embedded Node runtime
  # directly. The normal launcher forks without forwarding stop signals.
  [[ "$(./firebase-tools-linux --version)" == "15.34.2" ]]
  CLI_ENTRY="$HOME/.cache/firebase/tools/lib/node_modules/firebase-tools/lib/bin/firebase.js"
  [[ -f "$CLI_ENTRY" ]]
  FIREBASE=(env PKG_EXECPATH=PKG_INVOKE_NODEJS ./firebase-tools-linux "$CLI_ENTRY")
fi
nohup "${FIREBASE[@]}" emulators:start \
  --only storage --project lab27-local --config firebase.json \
  > "$RUNTIME/emulator.log" 2>&1 &
echo $! > "$RUNTIME/emulator.pid"

for _ in $(seq 1 60); do
  if curl -fsS -o /dev/null "http://127.0.0.1:9199/v0/b/$BUCKET/o" 2>/dev/null; then
    echo "Lab 27 Storage emulator is ready at http://127.0.0.1:9199"
    echo "Emulator UI: http://127.0.0.1:4000"
    exit 0
  fi
  if ! kill -0 "$(cat "$RUNTIME/emulator.pid")" 2>/dev/null; then
    echo "Lab 27 emulator exited during startup. Log follows:" >&2
    cat "$RUNTIME/emulator.log" >&2
    exit 1
  fi
  sleep 1
done

echo "Lab 27 emulator did not become ready. Log follows:" >&2
cat "$RUNTIME/emulator.log" >&2
exit 1
