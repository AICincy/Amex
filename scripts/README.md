# Host scripts

Run from this Grok host. Not GitHub Actions.

```bash
python3 scripts/live_pointers.py ops/amex-ops-state.public.yaml
python3 scripts/check_faq_helper_drift.py ops/amex-ops-state.public.yaml automod/current/r-amex-automod-0.1.3.5.yaml
python3 scripts/append_host_trail.py --skill reddit-owner-ops --tool arctic-shift --target r/amex --result PASS
```

Trail lives in `audits/host-trail/`.
