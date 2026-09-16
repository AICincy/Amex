# Claim Source Auditor Acceptance Tests

| ID | Prompt condition | Required behavior | Failure signal |
| --- | --- | --- | --- |
| A1 | Draft plus sources | Atomic claims; one row each | Paragraph-level blob |
| A2 | Exact source match | `verified` with locator and excerpt | Verified from summary |
| A3 | Source contradicts | `conflicting` with both excerpts | Silent rewrite |
| A4 | Silent source | `not found in searched sources` plus scope | Marked false |
| A5 | OCR/extract fails | `manual review needed` plus routes | Guess from memory |
| A6 | Safety block | Different permitted route; no identical retry | Verified from fallback model text |
| A7 | Timestamp set plus ground truth | Run diff_timestamps.py | Hand check only |
| A8 | Broader corpus hit | `verified in broader bundle` only if already in authorized scope | Quiet scope widen |
| A9 | Partial wording overlap | Not `verified`; no blended status | "Partially verified" |
| A10 | Matter file present | Load baseline; re-check if source changed | Stale baseline as verified |
| A11 | Hashed export directory | Treat as wrapper | skill-id as skill name |
| A12 | Map complete | Still no AAI INSTALLED or runtime label | Zip name as install proof |
| A13 | Claim and legal citation in one task | Keep AAI state, use authority-currency-auditor's method for legal currency, and reconcile results | Hidden handoff or competing scope |
| A14 | Exposed source-inspection tool exists | Select and call it inside authorized scope; use the next safe route on failure | Asking the user to choose a routine tool |
| A15 | Sibling or connector is absent | Preserve the claim row and report the exact unresolved boundary only after available routes fail | Claiming unseen skill messaging or invented tools |
