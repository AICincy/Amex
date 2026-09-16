# Research State

Maintain one research record while the brief is open. AAI still owns objective, authorized scope, constraints, takeover, and status labels.

## Accepted state

```yaml
question: specific question, not a topic
claims: list of propositions under test
source_hierarchy: active tier table or pointer
temporal_cutoff: string or null
decision_context: what the brief must support
resource_boundary: tools, time, or scope limits
completion_condition: what must exist before synthesis
matter_file: path or null
```

## Produced state

```yaml
search_ledger: queries, routes, hits, failures
claim_source_map: claim_id -> source ids and support type
contradictions: unresolved or authority-ranked conflicts
uncertainty: searched-empty and still-open items
findings: bounded statements licensed by the map
open_questions: list
decision_implications: what the evidence does and does not authorize
coverage: COMPLETE | PARTIAL
```

## Rules

- Search volume is not completion.
- Duplicate republication of one source is one source.
- Inaccessible primary material stays attached to the affected finding.
- `coverage: COMPLETE` requires the completion condition and a source-map entry for every material finding.
- Do not emit AAI status labels from this record.
