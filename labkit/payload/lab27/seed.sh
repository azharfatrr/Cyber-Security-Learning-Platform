#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
BUCKET="lab27-local.appspot.com"
BASE="http://127.0.0.1:9199/v0/b/$BUCKET/o"

upload() {
  local source="$1"
  local name="$2"
  curl -fsS -X POST \
    --data-binary "@$source" \
    -H "Content-Type: text/plain" \
    "$BASE?name=$name" > /dev/null
  echo "Seeded $name"
}

upload "$LAB_DIR/fixtures/alice-userinfo.txt" "alice-lab27%2Fuserinfo.txt"
upload "$LAB_DIR/fixtures/bob-userinfo.txt" "bob-lab27%2Fuserinfo.txt"
