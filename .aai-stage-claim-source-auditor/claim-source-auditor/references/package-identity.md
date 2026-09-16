# Package Identity

| Field | Value |
| --- | --- |
| Skill name | claim-source-auditor |
| Directory name | claim-source-auditor |
| Role | Subordinate domain module |
| Governor | aai-cognitive-interface |
| Implemented surface | Five-status claim map, timestamp diff helper |
| Not implemented | Open-web completeness, attachment graphs, AAI runtime labels |

A hashed export folder such as `skill-<id>/` is a transport wrapper.

Claim STATIC-PASS only after `python3 scripts/aai_runtime_gate.py package <this-directory>` returns PASS in `package-skill` mode.

A completed source map is not SAVED, INSTALLED, or runtime verification. `verified` is a claim-to-source label only.
