# Package Identity

| Field | Value |
| --- | --- |
| Skill name | regulatory-complaint-drafting |
| Directory name | regulatory-complaint-drafting |
| Role | Subordinate domain module |
| Governor | aai-cognitive-interface |
| Implemented surface | Complaint structure, recipient routing, draft/final distinction |
| Not implemented | Transmission, portal currentness, court filing |

A hashed export folder such as `skill-<id>/` is a transport wrapper.

Claim STATIC-PASS only after `python3 scripts/aai_runtime_gate.py package <this-directory>` returns PASS in `package-skill` mode.

A complete draft is not a filed complaint. A filed complaint requires independent transmission evidence outside this package.
