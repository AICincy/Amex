# Authority State

AAI owns objective, authorized scope, constraints, takeover, and AAI status
labels. This record is domain state only.

```yaml
source: citation string
jurisdiction: string
authority_level: primary | secondary | unknown
effective_period: string or unknown
procedural_scope: string
proposition_supported: string
currentness_state: current | amended | superseded | repealed | unverifiable
conflict_state: none | distinguishing | negative | unknown
verification_state: this-session-primary | cached | unverifiable
verified_as_of: ISO date or null
retrieval_source: string
```

Rules:

- Recognizability is not operative validity.
- A real citation does not gain force from version, prestige, or cache age.
- Cached rows must keep their original verification date.
- Filing, send, or explicit currency questions require this-session primary verification.
- Inaccessible primary material is `unverifiable`, not confirmation.
- Watch-list rows are implicit-reliance prompts. They are not current law.
- Entries marked pending manual lookup stay unresolved until checked.
- This table cannot award AAI INSTALLED or runtime labels.
