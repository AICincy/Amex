---
name: resend-api
description: Inspect Resend mail routes and prepare or execute specifically authorized email operations without exposing credentials.
---

# Resend API

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate mail-route module and must not override, narrow, suspend, or
reinterpret AAI. Accept AAI's recovered objective, authorized scope, hard
constraints, next executable action, completion evidence, status, and any
human-only gate as control state. The active Codex agent may combine it with
applicable skills and exposed tools in the current turn. It may not create
private inter-skill messages, background workers, or unsurfaced requests.

## Credentials and action gates

Use `RESEND_API_KEY` from the environment or a local file named by
`RESEND_KEYS_FILE`. Credential files never belong in the package, artifacts,
or version control. Never print a key.

Read-only inspection still requires a user-authorized account scope. Sending,
updating, cancelling, deleting, domain and webhook changes, audience writes,
and API-key operations require the current objective to authorize that exact
operation. A send also requires named sender, recipient, subject, body, and
`RESEND_EXECUTE_SEND=1`; the helper has no stored identity, recipient, or
message.

```bash
bash scripts/list_emails.sh
bash scripts/get_email.sh EMAIL_ID
RESEND_FROM='sender@example.com' RESEND_TO='recipient@example.com' \
  RESEND_SUBJECT='Subject' RESEND_HTML='<p>Body</p>' RESEND_EXECUTE_SEND=1 \
  bash scripts/send_email.sh
```

Do not execute the send example merely to test the package. Confirm accepted
mail only from Resend's current response and delivery only from its reported
events. Do not carry historical sends, email IDs, addresses, or delivery state
inside this skill.

## Boundaries

- Keep every request to the user's named Resend account and present scope.
- Re-fetch current Resend documentation before an unsupported product surface
  or request shape. Do not treat this package as API authority.
- Surface the status and safe error body when a request fails. Never fake a
  send, delivery, or connector state.
- Read [references/sibling-routing.md](references/sibling-routing.md) and
  [references/coordination-contract.md](references/coordination-contract.md)
  for current-turn coordination.
