# Package Identity

## Canonical identity

| Field | Value |
| --- | --- |
| Skill name | aai-cognitive-interface |
| Directory name | aai-cognitive-interface |
| Role | Governing control layer |
| Operator | Krass |
| Version file | ../VERSION |

A hashed export folder such as `skill-<id>/` is a transport wrapper. It is not the skill name. Before install or validation, copy or extract into a directory named `aai-cognitive-interface`.

## Status honesty

This package may claim STATIC-PASS only after:

```
python scripts/aai_runtime_gate.py package <this-directory>
```

returns `status: PASS`.

Do not claim SAVED, INSTALLED, RUNTIME-SMOKE-PASS, RUNTIME-VERIFIED, or ADVERSARIAL-PASS from this package, a zip filename, a local receipt, or model narrative.

## In-package vs external

In this package:

- instruction contract
- operator model
- runtime and continuation rules
- static gate
- turn-state and evidence schemas
- acceptance cases

External host modules, not shipped here:

- durable file or skill-save service
- trusted status controller
- any other skill, connector, or scheduler not exposed in the current Codex turn
