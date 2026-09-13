# Host scripts

Run from this Grok host. Not GitHub Actions.

```bash
python3 scripts/live_pointers.py ops/amex-ops-state.public.yaml
python3 scripts/check_faq_helper_drift.py ops/amex-ops-state.public.yaml automod/current/r-amex-automod-0.1.3.5.yaml
```

`live_pointers.py` writes thread IDs into `ops/`.
`check_faq_helper_drift.py` exits 2 on helper URL drift. It does not edit YAML.
