# Human gates

These actions stay with the operator. Grok on this host cannot paste them.

| Gate | Where | Current recorded state |
| --- | --- | --- |
| AutoMod wiki paste | `r/amex` wiki `config/automoderator` | Operator recorded 0.1.3.5 on 2026-09-11 |
| Rule 1 body | Rules Hub | Operator recorded 2026-09-10 |
| Removal reason 1e | Mod tools, removal reasons | Operator recorded 2026-09-10 |
| Monthly thread header | Current monthly referral thread | Operator recorded 2026-09-10 |
| Crowd Control | Safety Filters | Posts Off, comments Off as of 2026-09-11 screenshot |
| Reputation | Safety Filters | Inspect only |

Live wiki bytes and live Rules Hub bytes are not independently fetched by this project. Recorded state is operator-reported.

## Ship sequence

1. Change YAML under `automod/` from the last authorized version only.
2. Keep auditor PASS. Do not bump a version unless authorized.
3. Push. Let Actions parse and guard the file.
4. Operator pastes AutoMod wiki.
5. Operator pastes Rule 1 / 1e / header if public wording changed.
6. Operator inspects Crowd Control.
7. Record the paste in `ops/amex-ops-state.public.yaml` without unpublished token values.
