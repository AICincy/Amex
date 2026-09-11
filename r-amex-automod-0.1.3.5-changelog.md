# AutoMod audit

- File: `/home/workdir/artifacts/r-amex-automod-0.1.3.5.yaml`
- Base: `/home/workdir/artifacts/r-amex-automod-0.1.3.4.yaml`
- Fetched at: 2026-09-11T16:40:01.322659+00:00
- Routes: restore_library.py; firecrawl_rest_scrape (chrome); exa_rest_search retry; audit_automod.py this run
- Status: PASS (0 findings). Version-stamped copy of 0.1.3.4. No rule-body change.

Request class: CHANGE.
Human gate: wiki paste, Rules Hub paste, Safety Filter inspection.

## Findings

| ID | Class | Severity | Source URL | Detail |
| --- | --- | --- | --- | --- |
| none | — | — | this-run audit_automod.py on 0.1.3.4 and 0.1.3.5 | Both PASS, finding_count 0. |

## Remediations

| ID | Behavior change | Before | After |
| --- | --- | --- | --- |
| V1 | No | `# r/Amex AutoMod 0.1.3.4` | `# r/Amex AutoMod 0.1.3.5` |

V1 claim status: verified against file bytes. Not a syntax claim. Official pages do not govern the version comment string.

No other line changed. Diff is the version comment only.

No fetched-source-backed body change existed this run:

- 0.1.3.4 auditor PASS, so no compile/yaml defect to fix.
- Firecrawl official pages were navigation chrome.
- Exa retry retrieved Automoderator, Crowd Control, and Reputation bodies. Full documentation and writing-basic-rules bodies still missing.
- Retrieved Automoderator body restates spaces-not-tabs and `|` for multiline comments or modmail. 0.1.3.4 already complies.
- Crowd Control and Reputation remain Safety Filters, not YAML. Not encoded.
- Official "cannot react to karma" line remains conflicting with the existing 1e author check. 1e left in place per authorization.

## Claim map

| Claim | Status | Source |
| --- | --- | --- |
| 0.1.3.5 matches 0.1.3.4 except the version comment | verified | `diff -u` this run |
| 0.1.3.5 auditor PASS | verified | `/home/workdir/artifacts/audit-0.1.3.5.json` |
| Search checks need `(?i)` | not-found | official bodies this run do not state that; constraint forbids adding it |
| `|` belongs on regex fields | not-found | official Indents bullet documents `|` for comments/modmail |
| Crowd Control / Reputation are AutoMod YAML | not-found | official pages place them under Safety Filters |
| AutoMod cannot react to karma, so drop `combined_subreddit_karma` | conflicting | Automoderator "What can't" list vs authorized 1e author check. No removal. |
| Live wiki is 0.1.3.5 | not-found | wiki not fetched this run |

## Unresolved

- Full AutoMod documentation page body (52866343172500).
- Writing-basic-rules page body (52865423682452).
- Modifiers and Regex section body on the Automoderator page.
- Live r/Amex `config/automoderator` bytes.
- Whether the live compiler accepts author karma checks given the official "cannot react to karma" sentence.

## Public copy

Not rewritten. Rule 1 wording did not change.

## Ops state

`current_automod_artifact` and `current_automod_version` point at 0.1.3.5 draft. `live_automod_version_reported` stays 0.1.3.3. `human_tasks_complete` stays false.

## Human gate

Wiki paste, Rules Hub paste, and Safety Filter inspection stay with the operator.

Stop. No 0.1.3.6.
