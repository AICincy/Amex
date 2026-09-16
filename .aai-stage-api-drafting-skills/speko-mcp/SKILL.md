---
name: speko-mcp
description: Inspect Speko documentation or prepare and run specifically authorized Speko API operations without exposing credentials.
---

# Speko API

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate control-plane module and must not override, narrow, suspend, or
reinterpret AAI. Accept AAI's recovered objective, authorized scope, hard
constraints, next executable action, completion evidence, status, and any
human-only gate as control state. In the active Codex turn, the active agent
may compose it with applicable skills and exposed tools. It cannot create
hidden messages, background work, or unseen requests.

## Credentials and execution

Use `SPEKO_API_KEY` from the environment or `SPEKO_KEYS_FILE`. Credential
files never belong in this package, artifacts, or version control. Never print
or place a key in a client-side payload.

Re-fetch Speko documentation before selecting a request shape. Start with the
non-network dry run when adding a route:

```bash
python scripts/docs_search.py "QUERY" --dry-run
python scripts/speko_call.py GET /v1/agents --dry-run
```

`--dry-run` validates the method and destination without loading credentials or
making a request. Live requests also require `--execute`; the helper sends a
credential only to `https://api.speko.dev` and rejects authority-bearing paths.
`--execute` does not replace current scope authorization.
Creation, deployment, testing that consumes credits, phone dialing, deletion,
and any account or key change require explicit current authorization. Use a
fresh idempotency key for a mutating request. Do not claim a created agent,
session, deployment, or installed connector without its current response.

## Data boundary

Keep API credentials server-side. Send a browser only an appropriately scoped
session or transport token supplied by the service. Do not persist a voice
agent's personal data, phone number, test transcript, or prior account state in
this package.

Read [references/host-limit.md](references/host-limit.md),
[references/best-practices.md](references/best-practices.md), and
[references/coordination-contract.md](references/coordination-contract.md)
when those aspects apply.
