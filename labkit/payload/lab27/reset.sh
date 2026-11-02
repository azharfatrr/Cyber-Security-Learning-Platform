#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"

"$LAB_DIR/stop.sh"
rm -rf "$LAB_DIR/.runtime"
"$LAB_DIR/start.sh"
"$LAB_DIR/seed.sh"
