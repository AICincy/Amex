#!/usr/bin/env bash
# Source this file. Do not execute as a standalone printer.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEYS="${RESEND_KEYS_FILE:-${SCRIPT_DIR}/../secrets/keys.env}"
if [[ -f "$KEYS" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$KEYS"
  set +a
fi
if [[ -z "${RESEND_API_KEY:-}" || "$RESEND_API_KEY" == "re_xxxxxxxxx" ]]; then
  echo "BLOCKED RESEND_API_KEY missing from the environment or RESEND_KEYS_FILE" >&2
  exit 2
fi
