---
name: exa-firecrawl
description: Retrieve current web sources with Exa discovery or Firecrawl page extraction when the user authorizes live retrieval.
---

# Exa Firecrawl

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate retrieval module and must not override, narrow, suspend, or
reinterpret AAI. Accept AAI's recovered objective, authorized scope, hard
constraints, next executable action, completion evidence, status, and any
human-only gate as control state. In an active Codex turn, the active agent may
compose it with other applicable skills and select available tools. It cannot
create hidden inter-skill messages, background workers, or unseen network
activity.

Use Exa for discovery and Firecrawl for a named page body. Treat results as
source material, not as the authority. Preserve the route, URL, retrieval
time, and any failure in the task evidence.

## Credentials and execution

Read `EXA_API_KEY` or `FIRECRAWL_API_KEY` from the environment. A local file
may be supplied through `EXA_FIRECRAWL_KEYS_FILE`; credential files never
belong in this package, artifacts, or version control. Missing credentials
block a live call. Do not invent, print, or request a secret in chat.

Run a dry run before a new route or request shape:

```bash
python scripts/exa_search.py "QUERY" --num 8 --dry-run
python scripts/firecrawl_scrape.py "https://example.com" --dry-run
```

Remove `--dry-run` only when the current objective authorizes live retrieval.
Do not represent a dry run as source retrieval or a connected plugin.

## Boundaries

- Keep to the user's current source scope and stop if a page is inaccessible,
  paywalled, or disallowed.
- Do not scrape authenticated, private, or personal data without explicit
  authorization and a lawful purpose.
- Surface nonzero scripts and vendor errors exactly. Do not fabricate results.
- For host limits and the active-turn coordination boundary, read
  [references/host-limit.md](references/host-limit.md) and
  [references/coordination-contract.md](references/coordination-contract.md).
