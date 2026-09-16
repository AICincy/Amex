# Turn State Schema

Maintain one record while an objective is open. Validate with:

```
python scripts/aai_state_check.py <state.yaml>
```

Do not expose the record unless it helps resumption or review.

## Required fields

```yaml
objective: string
request_class: ANSWER | DIAGNOSE | REVIEW | BUILD | CHANGE | CONTINUE | WAIT | DECISION-GATED
authorized_scope: string
constraints: list of strings
active_threads: list of strings
next_action: string
completion_evidence: string
human_gate: null | string
takeover: boolean
artifact_targets: list of strings
status: ACTIVE | GATED | BLOCKED | COMPLETE
missing_dependencies: list of strings
```

## Rules

- `human_gate` is null unless `status` is GATED.
- `status: COMPLETE` requires nonempty `completion_evidence`.
- `takeover: true` forbids offering option menus.
- `missing_dependencies` names host modules or sibling skills that narrowed execution.
- IDs such as T1, F1, E1, C1 belong in `active_threads` when three or more items are open.

Machine schema: [../schemas/turn-state.schema.json](../schemas/turn-state.schema.json)

Evidence ledger schema: [../schemas/evidence-ledger.schema.json](../schemas/evidence-ledger.schema.json)
