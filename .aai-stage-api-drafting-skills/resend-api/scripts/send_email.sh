#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load_key.sh"

: "${RESEND_FROM:?BLOCKED RESEND_FROM must be supplied for this exact send}"
: "${RESEND_TO:?BLOCKED RESEND_TO must be supplied for this exact send}"
: "${RESEND_SUBJECT:?BLOCKED RESEND_SUBJECT must be supplied for this exact send}"
: "${RESEND_HTML:?BLOCKED RESEND_HTML must be supplied for this exact send}"
if [[ "${RESEND_EXECUTE_SEND:-}" != "1" ]]; then
  echo "BLOCKED RESEND_EXECUTE_SEND=1 required for a human-authorized send" >&2
  exit 2
fi

BODY="$(python3 - <<'PY'
import json, os
print(json.dumps({
    "from": os.environ["RESEND_FROM"],
    "to": os.environ["RESEND_TO"],
    "subject": os.environ["RESEND_SUBJECT"],
    "html": os.environ["RESEND_HTML"],
}))
PY
)"

curl -sS -X POST 'https://api.resend.com/emails' \
  -H "Authorization: Bearer ${RESEND_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d "$BODY"
echo
