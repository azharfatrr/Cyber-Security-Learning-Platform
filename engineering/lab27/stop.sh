#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$LAB_DIR/.runtime"

if [ ! -f "$RUNTIME/emulator.pid" ]; then
  echo "No Lab 27 emulator PID file; nothing to stop."
  exit 0
fi

PID="$(cat "$RUNTIME/emulator.pid")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  for _ in $(seq 1 30); do
    kill -0 "$PID" 2>/dev/null || break
    sleep 1
  done
fi
rm -f "$RUNTIME/emulator.pid"
echo "Lab 27 emulator stopped."
