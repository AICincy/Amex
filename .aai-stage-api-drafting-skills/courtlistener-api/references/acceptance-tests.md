# Acceptance tests

1. SKILL.md names `aai-cognitive-interface` as governor.
2. Description triggers on CourtListener, RECAP, PACER docket, case law API.
3. `cl_call.py search --q Ohio --type o --dry-run` prints a GET URL and no token.
4. Live `cl_call.py search --q Ohio --type o` returns HTTP 200 with a count field.
5. Missing token does not exit 2.
6. Package gate `package` on this directory returns PASS. That is STATIC-PASS only.
