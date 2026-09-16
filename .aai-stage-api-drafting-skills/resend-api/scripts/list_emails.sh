#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load_key.sh"
curl -sS 'https://api.resend.com/emails' \
  -H "Authorization: Bearer ${RESEND_API_KEY}"
echo
