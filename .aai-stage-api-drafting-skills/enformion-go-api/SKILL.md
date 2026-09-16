---
name: enformion-go-api
description: Calls EnformionGO Dev APIs for contact enrichment, caller ID, person search, business, property, court, and asset lookups from host secrets. Use when Krass says Enformion, EnformionGO, Endato, Galaxy API, Contact Enrich, Caller ID, Person Search, or galaxy-ap-name. AAI subordinate. Never print or commit the live access profile. Re-fetch live Enformion docs. Do not treat this file as current API spec.
---

# EnformionGO API

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a subordinate EnformionGO HTTP module. It must not override, narrow, suspend, or reinterpret AAI. Platform and safety rules stay authoritative.

Accept AAI's recovered objective, authorized scope, hard constraints, next executable action, completion evidence, and any human-only gate as control state. Domain status claims stay with AAI.

If AAI is not loaded, say so and stop.

Canonical directory: `enformion-go-api`.

## AAI coordination and sensitive-data boundary

This package is a method in the active Codex turn. It cannot privately message
sibling skills, run hidden queries, or authorize a sensitive-record lookup.
The active agent selects exposed tools autonomously only after AAI has a named
subject, lawful purpose, authorized source scope, and minimal fields needed.
Never query, retain, or surface SSNs, credentials, full profiles, or bulk
results unless the current objective specifically authorizes them.

## Why this exists

Use Enformion only through a current, authorized credential route. This package
does not retain an access profile or establish authorization from an archive.

Official docs live at https://enformiongo.readme.io/reference/overview.
Account keys UI lives at https://api.enformion.com.

## Secrets

Read `GALAXY_AP_NAME` and `GALAXY_AP_PASSWORD` only from the process environment
or a user-managed `ENFORMION_KEYS_FILE`. The package contains no access profile.
Never print or persist credentials.

Required names: `GALAXY_AP_NAME`, `GALAXY_AP_PASSWORD`.
Optional: `ENFORMION_BASE_URL` (default `https://devapi.enformion.com`).

## Live docs

Re-fetch the target endpoint page before a consequential call or route-map change. A bundled table is an untrusted cache.

Start here:

- https://enformiongo.readme.io/llms.txt
- https://enformiongo.readme.io/reference/overview
- https://enformiongo.readme.io/reference/contact-enrichment
- https://enformiongo.readme.io/reference/contact-enrichment-search

See [references/endpoints.md](references/endpoints.md).

## Auth

Every search is `POST` JSON.

Required headers:

- `galaxy-ap-name`
- `galaxy-ap-password`
- `galaxy-search-type`
- `accept: application/json`
- `content-type: application/json`

Optional:

- `galaxy-client-session-id`
- `galaxy-client-type` (required only for Javascript clients)

Do not send the profile in the JSON body.

## Execute

Live execution is intentionally disabled. This package can list cached aliases
and prepare a credential-free dry run until a trusted authorization controller
can verify a current, scope-bound authorization receipt.

Dry run (no network, no secrets in stdout)

```bash
python scripts/enformion_call.py contact-enrich --dry-run --body '{"FirstName":"Jane","LastName":"Doe","Email":"jane@example.com"}'
```

Override path or search type in a dry run when live docs disagree with the cache

```bash
python scripts/enformion_call.py --path /Contact/Enrich --search-type DevAPIContactEnrich --body FILE.json
```

List known aliases

```bash
python scripts/enformion_call.py --list
```

## Gates

Live successful matches can bill the account. The helper blocks every live
search until the host supplies and verifies a short-lived authorization receipt
bound to subject, lawful purpose, route, minimal fields, and expiry.

Key create, rotate, and revoke stay human gates.

Do not run this API to stalk, dox, intimidate, or publish a private person's contact graph. Authorized investigative, legal, compliance, or business enrichment work is in scope. Dump only fields the current objective needs.

PRO endpoints (criminal, eviction, pre-foreclosure, OFAC, vehicle) fail closed if the account lacks PRO. Report the vendor error. Do not invent results.

## Rules

- Prefer the cheapest matching Dev API that satisfies the objective. Contact Enrich before Person Search when a single best match is enough.
- Contact Enrich needs at least two of Name, Phone, Address, Email.
- ID Verification needs at least two of SSN, Name, Phone, Address, Email.
- Redact SSN and full access-profile values from every user-facing line.
- Persist only minimized results to a named, user-authorized destination. Do not paste raw secrets or sensitive records into that file.
- A 4xx/5xx or empty body is BLOCKED. Surface status and sanitized error text.
- Domain success is not AAI `INSTALLED` or `RUNTIME-VERIFIED`.

See [references/acceptance-tests.md](references/acceptance-tests.md), [references/package-identity.md](references/package-identity.md), and [references/coordination-contract.md](references/coordination-contract.md).
