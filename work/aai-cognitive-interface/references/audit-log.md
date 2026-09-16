# Compact Audit Log

Default trail in Codex is JSONL, one event per line. Do not write the long markdown trail unless Krass asks for it.

Path: `family/state/audit.jsonl`

Append with:

```
python family/scripts/audit_append.py \
  --skill aai-cognitive-interface \
  --act gate \
  --target validate_family.py \
  --result PASS \
  --note "10/10 STATIC-PASS"
```

## Event fields

| Field | Rule |
| --- | --- |
| t | ISO timestamp |
| skill | Canonical skill name |
| act | load, tool, gate, status, adapt, park, block, draft |
| target | File, tool, or label. Short. |
| result | PASS, FAIL, OK, BLOCKED, REFUSED, WAIT |
| note | One sentence, max 120 chars. No chain of thought. No tool dump. |

## Token rules

- Record observable action and result only.
- Summarize tool output in the note. Never paste raw output.
- Do not duplicate the user-facing reply into the log.
- Write a long markdown trail only on explicit request.
- Functions inventory lives in `functions-catalog.json`. That file is static. Do not grow it per turn.
