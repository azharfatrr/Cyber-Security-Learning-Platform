#!/usr/bin/env bash

lab27_process_matches() {
  local pid="$1" lab_dir="$2" command_line working_directory expected_cli
  [[ "$pid" =~ ^[0-9]+$ ]] || return 1
  kill -0 "$pid" 2>/dev/null || return 1
  [[ -r "/proc/$pid/cmdline" ]] || return 1
  command_line="$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null)" || return 1
  working_directory="$(readlink -f -- "/proc/$pid/cwd" 2>/dev/null)" || return 1
  expected_cli="./node_modules/.bin/firebase"
  [[ "$working_directory" == "$lab_dir" \
    && "$command_line" == *"$expected_cli"* \
    && "$command_line" == *"emulators:start"* \
    && "$command_line" == *"--only storage"* \
    && "$command_line" == *"--project lab27-local"* \
    && "$command_line" == *"--config firebase.json"* ]]
}
