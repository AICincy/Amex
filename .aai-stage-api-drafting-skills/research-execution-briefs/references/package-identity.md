# Package Identity

| Field | Value |
| --- | --- |
| Skill name | research-execution-briefs |
| Directory name | research-execution-briefs |
| Role | Subordinate domain module |
| Governor | aai-cognitive-interface |
| Version file | ../VERSION |

A hashed export folder such as `skill-<id>/` is a transport wrapper. Validate and install from `research-execution-briefs/`.

This package may claim STATIC-PASS only after:

```
python3 scripts/aai_runtime_gate.py package <this-directory>
```

returns `status: PASS` in `package-skill` mode.

Research coverage labels are not AAI artifact statuses. A complete source map does not prove SAVED, INSTALLED, or any runtime label.
