# Human gates

These actions stay with the operator. Grok on this host cannot paste them.

| Gate | Where | Current recorded state |
| --- | --- | --- |
| AutoMod wiki paste | `r/amex` wiki `config/automoderator` | Operator recorded 0.1.3.5 on 2026-09-11. Live bytes not fetched. |
| Rule 1 body | Rules Hub | Waits for next monthly thread post. |
| Removal reason 1e | Mod tools, removal reasons | Advisory comment posted 2026-09-13. Live reason bytes not fetched. |
| Monthly thread header | Current monthly referral thread | Operator recorded fixed 2026-09-13. |
| Crowd Control | Safety Filters | 3-day trial started 2026-09-13. Re-inspect 2026-09-16. |
| Reputation | Safety Filters | Inspect only |

Live wiki bytes and live Rules Hub bytes are not independently fetched by this project. Recorded state is operator-reported.

## Ship sequence

1. Change YAML under `automod/current/` from the last authorized version only.
2. Keep auditor PASS. Do not bump a version unless authorized.
3. Push. Let Actions parse and guard the file.
4. Operator pastes AutoMod wiki.
5. Operator pastes Rule 1 TEXT on the next monthly thread cycle.
6. Operator re-inspects Crowd Control when the trial ends.
7. Record the result in `ops/amex-ops-state.public.yaml` without unpublished token values.
