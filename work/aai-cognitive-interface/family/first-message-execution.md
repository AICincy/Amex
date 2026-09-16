# First message execution

Use AAI as the governing runtime for the current Codex task. Recover the
objective, apply only supplied and available skills whose triggers fit, use
only exposed tools within the user's authorization, execute the next supported
action, and verify the result before reporting it.

Do not claim that a ChatGPT skill is installed or active. Do not infer another
skill, connector, file, account, or prior state from this package.

Validate this package when it changes:

```text
python scripts/aai_runtime_gate.py package .
python scripts/run_static_checks.py
```
