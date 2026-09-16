# Complaint State

AAI owns objective, authorized scope, constraints, takeover, and AAI status
labels. This record is domain state only.

```yaml
forum: named institution or UNRESOLVED
jurisdiction: supporting authority or UNRESOLVED
complainant_relationship: string
factual_chronology: shared across recipients
evidence_state: supported | partial | missing
disputed_propositions: list
current_authority: verified-this-session | stale-table | missing
prior_resolution_attempts: list
procedural_requirements: list
requested_action: string
available_remedies: list
attachments: list
submission_state: DRAFT | PROVISIONAL | FINAL-DRAFT | SUBMITTED
filing_blocker: null | string
```

Rules:

- Persuasion cannot create jurisdiction, currentness, remedy power, or proof of send.
- `SUBMITTED` requires independent transmission evidence from the host or user. This skill cannot award it.
- Unresolved forum, procedure, or authority yields `PROVISIONAL` plus `filing_blocker`.
- Recipient tables in this package are operator defaults. They are not filing-day verification.
- Fields marked `[VERIFY]` stay empty or blocked until checked in the current session.
- Sending, portal submit, certified mail, or clerk upload is an AAI human-only gate.
