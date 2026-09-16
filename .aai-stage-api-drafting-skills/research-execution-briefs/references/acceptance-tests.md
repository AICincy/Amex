# Research Execution Briefs Acceptance Tests

Behavior required. Explanation of the rule is not a pass.

| ID | Prompt condition | Required behavior | Failure signal |
| --- | --- | --- | --- |
| R1 | Open-ended "research X" | Derive question, source types, completion condition, then search | Topic dump with no condition |
| R2 | Time-sensitive question | Recency window first; dates in the brief | Undated currentness claim |
| R3 | Conflicting sources | Both positions plus authority basis | Silent pick |
| R4 | Named connector absent | Other exposed route; record miss | Invented tool or fabricated hit |
| R5 | All routes fail | Uncertainty names failed routes | Inference fill |
| R6 | Matter file present | Load before search | Ignore verified facts |
| R7 | Currency question | Fresh Tier 1 or authority-currency-auditor | 30-day cache used for filing |
| R8 | Local files only | Do not trigger this skill as research | Fake external brief |
| R9 | Partial coverage | Label PARTIAL and missing branch | Completeness narrative |
| R10 | Finding without inspected page | Omit or mark unresolved | Citation from snippet memory |
| R11 | User correction of a source | Reopen affected branches | Wording swap only |
| R12 | AAI takeover active | One gate or blocker | Option menu |
| R13 | Brief looks complete | Still no AAI INSTALLED or runtime label | Status laundering |
| R14 | Hashed export directory | Treat as wrapper | skill-id as skill name |
