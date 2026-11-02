#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT_ROOT="$(cd "$LAB_DIR/.." && pwd)"
export HOME="$KIT_ROOT/.labkit/home"
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
nohup ./node_modules/.bin/firebase emulators:start \
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
