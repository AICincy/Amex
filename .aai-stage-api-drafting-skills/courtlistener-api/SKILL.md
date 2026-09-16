---
name: courtlistener-api
description: Calls the free CourtListener REST v4 API for opinions, PACER/RECAP dockets, filings, judges, and courts. Use when Krass says CourtListener, Free Law Project, RECAP, PACER docket, case law API, criminal docket search, or wants court records without Enformion. AAI subordinate. Token optional. Re-fetch live CourtListener docs. This is not NCIC and not a statewide rap sheet.
---

# CourtListener API

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a subordinate CourtListener HTTP module. It must not override, narrow, suspend, or reinterpret AAI. Platform and safety rules stay authoritative.

Accept AAI's recovered objective, authorized scope, hard constraints, next executable action, completion evidence, and any human-only gate as control state. Domain status claims stay with AAI.

If AAI is not loaded, say so and stop.

Canonical directory: `courtlistener-api`.

## AAI coordination and autonomous execution

This package is a method in the active Codex turn, not a background worker or
private messaging endpoint. The active agent composes applicable source-audit
methods, selects exposed tools autonomously within AAI scope, and preserves
coverage limits. A public-record retrieval is never a clean-record conclusion.
No tool call may be represented as a sibling handoff or hidden execution.

## Why this exists

Enformion criminal and court endpoints need a billed PRO profile. CourtListener is a live public API at `https://www.courtlistener.com/api/rest/v4/`. Many routes work without a token. A free token raises reliability and rate limits.

This is case law, federal PACER via RECAP, judges, and oral argument. It is not a national criminal-history database. County and municipal Ohio criminal cases are usually absent. Say that when the result set is empty.

## Secrets

Token is optional.

Read `COURTLISTENER_TOKEN` only from the process environment or a
user-managed `COURTLISTENER_KEYS_FILE`. The package contains no credentials.
Never print or persist the token.

Optional name: `COURTLISTENER_TOKEN`.
Mint at https://www.courtlistener.com/profile/api-token/ after a free account.

If the file is missing, call unauthenticated. Do not invent a token.

## Live docs

Re-fetch before changing request shapes.

- https://www.courtlistener.com/help/api/rest/
- https://www.courtlistener.com/help/api/rest/search/
- https://www.courtlistener.com/api/rest/v4/

A bundled table is an untrusted cache. See [references/endpoints.md](references/endpoints.md).

## Execute

Search

```bash
python scripts/cl_call.py search --q 'QUERY' --type r
```

Types: `o` opinions, `r` RECAP dockets with filings, `rd` RECAP documents, `d` PACER dockets, `p` judges, `oa` oral arguments.

Get a path

```bash
python scripts/cl_call.py get --path /dockets/123/
```

List courts

```bash
python scripts/cl_call.py get --path /courts/ --params 'jurisdiction=FD'
```

Dry run

```bash
python scripts/cl_call.py search --q 'QUERY' --type r --dry-run
```

County or municipal gaps: use `exa-firecrawl` against the official clerk site. Do not invent a county API.

## Gates

Do not run this to stalk, dox, or publish a private person's record set. Authorized legal, compliance, or investigative work is in scope.

Token create and reset stay human gates.

Empty result is not a clean record. It is coverage miss until an official clerk source is checked.

## Rules

- Authenticate with `Authorization: Token $COURTLISTENER_TOKEN` when the env var exists.
- Default search type for a named person in a court-records task is `r` then `o`.
- Persist results only to a named, user-authorized destination.
- A 4xx/5xx is BLOCKED. Surface status and sanitized error text.
- Domain success is not AAI `INSTALLED` or `RUNTIME-VERIFIED`.
- Default authenticated rate cap is 5/min, 50/hour, 125/day. Back off on 429.

See [references/acceptance-tests.md](references/acceptance-tests.md), [references/package-identity.md](references/package-identity.md), and [references/coordination-contract.md](references/coordination-contract.md).
