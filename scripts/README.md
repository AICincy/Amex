# Host scripts

Run from this Grok host. Not GitHub Actions.

## Adversarial skill suite

Run all 20 prompt cases and the local Dify, Enformion, Speko, and AutoMod
behavior checks. The runner performs no external API call, Reddit write, or
model-service call. It saves a JSON evidence report.

```bash
python3 scripts/run_adversarial_skill_suite.py
```

Report: `audits/adversarial-skill-suite-2026-09-16.json`.

```bash
python3 scripts/live_pointers.py
# Review the validated proposal, then explicitly write the designated ops file.
python3 scripts/live_pointers.py --apply
python3 scripts/check_faq_helper_drift.py ops/amex-ops-state.public.yaml automod/current/r-amex-automod-0.1.3.5.yaml
python3 scripts/append_host_trail.py --skill reddit-owner-ops --tool arctic-shift --target r/amex --result PASS
```

Trail lives in `audits/host-trail/`.
