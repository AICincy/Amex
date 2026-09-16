# Acceptance tests

Static only unless Krass authorizes a billed live search.

1. SKILL.md names `aai-cognitive-interface` as governor and refuses to self-govern.
2. Description triggers on Enformion, EnformionGO, Endato, Galaxy, Contact Enrich, Caller ID, Person Search.
3. Secrets live only in `secrets/keys.env`. SKILL.md has no profile values.
4. `enformion_call.py --list` prints aliases and no credentials.
5. `enformion_call.py contact-enrich --dry-run --body '{...}'` prints method, path, search type, and redacted header names.
6. Missing `secrets/keys.env` on a live call exits 2 with `BLOCKED secrets/keys.env missing`.
7. A live call without a named subject and authorization must not run.
8. Package gate `package` on this directory returns PASS. That is STATIC-PASS only.
