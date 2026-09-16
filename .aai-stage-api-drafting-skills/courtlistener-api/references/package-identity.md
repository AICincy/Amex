# Package Identity

| Field | Value |
| --- | --- |
| Skill name | courtlistener-api |
| Directory name | courtlistener-api |
| Role | Subordinate domain module |
| Governor | aai-cognitive-interface |
| Implemented surface | CourtListener REST v4 search and GET helper |
| Not implemented | NCIC, statewide rap sheets, county clerk APIs, Enformion PRO court |

Claim STATIC-PASS only after
`python scripts/aai_runtime_gate.py package <this-directory>`
returns PASS in package-skill mode.

A live 200 is not RUNTIME-VERIFIED.
