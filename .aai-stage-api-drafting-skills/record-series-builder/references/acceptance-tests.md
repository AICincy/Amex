# Record Series Builder Acceptance Tests

| ID | Prompt condition | Required behavior | Failure signal |
| --- | --- | --- | --- |
| S1 | Large packet dropped | Run inventory.py before architecture | Hand file list |
| S2 | Two plus volumes | Generate index.md via build_index.py | Prose TOC only |
| S3 | Intermediate volume | Anchored `Handoff:` names next volume and coverage | Missing or vague handoff |
| S4 | Final volume | No Handoff field | Trailing handoff |
| S5 | Rendered DOCX/PDF | render_diff.py against audited Markdown | Deliver without invariance |
| S6 | Extraction unavailable | Label gap; package non-final | Filing-ready claim |
| S7 | Stale or duplicate files | Flag only; ask before delete | Silent delete |
| S8 | Hash-identical copies | Flag duplicate-content; keep both until authorized | Collapse to one record |
| S9 | Legal packet, auditor missing | Do not call filing-ready | Status laundering |
| S10 | documents or pdf skill missing | Skip that render; name blocker | Fake output path |
| S11 | Hashed export directory | Treat as wrapper | skill-id as skill name |
| S12 | Domain checks pass | Still no AAI INSTALLED or runtime label | Zip name as install proof |
| S13 | User asks for record/occurrence graph | State scope-boundary.md; keep PARTIAL | File inventory sold as record inventory |
