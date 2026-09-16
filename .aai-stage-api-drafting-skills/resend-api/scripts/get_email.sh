#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load_key.sh"
EMAIL_ID="${1:?usage: get_email.sh <email_id>}"
curl -sS "https://api.resend.com/emails/${EMAIL_ID}" \
  -H "Authorization: Bearer ${RESEND_API_KEY}"
echo
