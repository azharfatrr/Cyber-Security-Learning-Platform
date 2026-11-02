#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$LAB_DIR/.runtime"
# shellcheck source=lab27/process.sh
source "$LAB_DIR/process.sh"

if [ ! -f "$RUNTIME/emulator.pid" ]; then
  echo "No Lab 27 emulator PID file; nothing to stop."
  exit 0
fi

PID="$(cat "$RUNTIME/emulator.pid")"
if lab27_process_matches "$PID" "$LAB_DIR"; then
  kill "$PID"
  for _ in $(seq 1 30); do
    lab27_process_matches "$PID" "$LAB_DIR" || break
    sleep 1
  done
  if lab27_process_matches "$PID" "$LAB_DIR"; then
    echo "Lab 27 emulator did not stop; keeping its PID file at $RUNTIME/emulator.pid." >&2
    exit 1
  fi
else
  echo "PID file did not match a running Lab 27 emulator; leaving that process untouched."
fi
rm -f "$RUNTIME/emulator.pid"
echo "Lab 27 emulator stopped."
