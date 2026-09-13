# Host trail

Continuous log of what this Grok host ran against AICincy/Amex.

- Append-only tables. Newest day file plus [`CURRENT.md`](CURRENT.md).
- Record skill, tool/route, target, result.
- Do not write keys, tokens, unpublished floors, or live wiki dumps.
- This is not GitHub Actions. Rows are written when Grok runs.

Append:

```bash
python3 scripts/append_host_trail.py \
  --skill reddit-owner-ops \
  --tool arctic-shift \
  --target r/amex \
  --result PASS
```
