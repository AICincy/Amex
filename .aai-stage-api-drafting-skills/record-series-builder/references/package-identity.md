# Package Identity

| Field | Value |
| --- | --- |
| Skill name | record-series-builder |
| Directory name | record-series-builder |
| Role | Subordinate domain module |
| Governor | aai-cognitive-interface |
| Implemented surface | Inventory, volume architecture, index, render-diff |
| Not implemented | Typed record/occurrence/attachment identity from the AAI profile |

A hashed export folder such as `skill-<id>/` is a transport wrapper.

Claim STATIC-PASS only after:

```
python3 scripts/aai_runtime_gate.py package <this-directory>
```

returns `status: PASS` in `package-skill` mode.

Inventory counts, render-diff exit 0, and index generation are domain checks. They do not prove SAVED, INSTALLED, or runtime labels.
