# Ground-truth adversarial audit 2026-09-13

Scope: public GitHub files in AICincy/Amex plus this-run live fetches.
Live Reddit rules JSON and hot listing returned 403/Blocked. Firecrawl rules scrape returned 500. Those surfaces are not independently verified this run.

Statuses: verified | conflicting | not found in searched sources | manual review needed.

| ID | Claim | Status | Source |
| --- | --- | --- | --- |
| G1 | Current paste file is `automod/current/r-amex-automod-0.1.3.5.yaml` and starts with `---` | verified | file SHA 7c655fcb; first two lines |
| G2 | 0.1.3.5 header comment is a version stamp of 0.1.3.4 | verified | changelog V1; file header |
| G3 | 1e AutoMod rule is monthly-thread referral-URL comments only, floor only in author check and action_reason | verified | YAML 1e rule; public copy; public comment field has no 250 |
| G4 | Title match is `monthly.{0,80}referral.{0,30}thread` | verified | YAML parent_submission and submission exemptions |
| G5 | Operator recorded AutoMod wiki paste of 0.1.3.5 on 2026-09-11 | verified as operator-reported | ops notes; live wiki bytes not fetched |
| G6 | Live AutoMod wiki bytes match 0.1.3.5 | not found in searched sources | wiki `config/automoderator` not fetched |
| G7 | Live Rule 1 TEXT matches public copy | not found in searched sources | `/r/amex/about/rules` 403 this run |
| G8 | Current monthly referral thread title and header match public addendum | not found in searched sources | no September 2026 r/amex thread found; August thread `1vcdxf9` is the newest public hit |
| G9 | wiki/Home Crowd Control still Off after 2026-09-13 trial | conflicting | Home said Off; operator recorded 3-day trial |
| G10 | wiki/Home Rule 1 / 1e paste complete on 2026-09-10 | conflicting | operator 2026-09-13: Rule 1 TEXT waits for next monthly thread; header fixed; advisory comment posted |
| G11 | AutoMod.md says the stack holds the monthly thread if the title is wrong | conflicting | YAML does not remove a submission solely for a non-matching title |
| G12 | AutoMod.md says the stack holds card-name referral titles | conflicting | YAML matches referral URLs and named phrases, not card names |
| G13 | Common Questions helper URL `1vm5hnj` is the current monthly thread | not found in searched sources | URL is hardcoded in YAML; current September thread not fetched |
| G14 | Changelog paths under `/home/workdir/artifacts/` are repo paths | conflicting | changelog names host artifact paths |
| G15 | `audits/audit-0.1.3.5.json` is a complete audit | conflicting | stub PASS with empty findings |
| G16 | GitHub Wiki tab is the staff handbook | conflicting | Wiki tab empty; handbook is `wiki/` in the repo |
| G17 | Projects board exists | not found in searched sources | Projects API 403; public projects page empty |
| G18 | Release `v0.1.3.5` exists with YAML and public copy | verified | GitHub release 388054270 |
| G19 | Validate / Guard / Lint passed on `b453a906` | verified | Actions runs 34786825926, 34786825931, 34786825941 |
| G20 | Broad `DM` / `PM` word-remove rules exist besides packet 1b | verified | YAML messaging rules vs packet 1b |

## Remediation this run

- Align Home, Human-gates, Rule-1, Safety-Filters with 2026-09-13 operator record.
- Correct AutoMod.md stack description.
- Replace changelog host paths.
- Replace stub audit JSON and point CURRENT.md at this audit.
- Leave AutoMod YAML unchanged. No authorized version bump.
