# Audit State

AAI owns objective, authorized scope, constraints, takeover, and AAI status
labels. This record is domain state only.

```yaml
source_universe: named files or locators
temporal_bounds: string or null
claims: atomic propositions
row_count: integer
coverage: COMPLETE | PARTIAL
failed_routes: list
```

Each row uses exactly one taxonomy status from status-taxonomy.md:

`verified` | `verified in broader bundle` | `conflicting` | `not found in searched sources` | `manual review needed`

Rules:

- Citation presence is not entailment.
- Prestige, repetition, and coherence cannot upgrade support.
- The AAI profile's "partial" support is not a status here. Partial match is `not found in searched sources` or `manual review needed` with a basis note.
- Do not blend statuses.
- `verified` requires a locator and excerpt from the inspected source.
- OCR failure, missing attachment, or blocked extraction stays on the row.
- This map cannot award AAI INSTALLED or runtime labels.
