# Civic-Legal Skill Pattern Library

This reference documents the recurring structural patterns shared across
the civic-tech/legal-advocacy skill family: authority-currency-auditor,
claim-source-auditor, forensic-evidentiary-drafting,
regulatory-complaint-drafting, record-series-builder, and
research-execution-briefs. New skills in this family inherit these
patterns by default. Deviation requires a stated reason.

## Pattern 1: Matter context

Every skill that touches case-specific or matter-specific work loads a
matter file first (matter-[name]-verified-facts.md). The canonical
template lives at
forensic-evidentiary-drafting/references/matter-file-template.md.

```
## Matter context

IF a matter file (matter-[name]-verified-facts.md) exists for [the
relevant scope]:
THEN load it before [primary action]. Treat verified facts as a
provenance-bearing baseline. Re-check underlying sources when the applicable
audit skill requires it. Treat logged user corrections as hard constraints.

IF no matter file exists:
THEN proceed using available context and sources. Create persistent matter
state only when it is within the requested objective.
```

## Pattern 2: Status taxonomy table

Audit-style skills (claim-source-auditor, authority-currency-auditor)
use a closed status taxonomy: every audited item gets exactly one status
from a fixed list, statuses do not blend, and each status has a required
basis. New audit skills define their own taxonomy table rather than
reusing another skill's verbatim, because the audited object differs
(supplied documents vs. live legal sources).

## Pattern 3: Dependency invocation

Drafting skills that produce filed or delivered documents auto-invoke
verification skills before delivery, without a user prompt:

```
## Dependency invocation

IF this skill produces [output type]:
THEN invoke these skills automatically before delivery:
  - authority-currency-auditor: on every legal citation.
  - claim-source-auditor: on every factual assertion.

IF either auditor returns a status other than "current" or "verified":
THEN flag and correct before delivery. Do not deliver unflagged.
```

An auditor retrieval failure is not itself proof that an item is
unverifiable. Do not repeat an identical blocked request. Try another
permitted authoritative retrieval or extraction route first. Never treat a
fallback model's text as verification. If the evidence remains unavailable,
label the limitation explicitly.

## Pattern 4: Pro se attestation variant

Any skill producing a document with a signature block or attestation
checks filer status. The pro se attestation language and the rules for
omitting attorney-specific terms live in
forensic-evidentiary-drafting/references/section-templates.md. Skills
reference this rather than redefining attestation language.

## Pattern 5: Jurisdiction cross-reference (Hamilton County)

Any skill whose output may be filed with a Hamilton County court or the
Hamilton County Clerk first identifies the exact court, division, case type,
document purpose, and filing channel. It loads
forensic-evidentiary-drafting/references/hamilton-county-filing.md for routing,
then applies output format, file-size, split, or service procedures only when
the current official source confirms they govern that identified channel.
No Hamilton County limit is a generic county-wide default.

## Pattern 6: Formatting deference

No skill in this family restates aai-cognitive-interface's global
formatting rules (no em/en dashes, active voice, one idea per sentence,
tables for 3+ items). Skills cross-reference aai-cognitive-interface and
add only domain-specific voice extensions (for example, forensic voice
permits colons and semicolons for clause separation).

## Pattern 7: Validation checklist

Skills producing filed or delivered documents end with a numbered
pre-delivery checklist covering structure, source grounding, citation
currency, and jurisdiction-specific requirements. The checklist is the
last thing the skill does, after all dependency invocations.

## Pattern 8: AAI interoperability

`aai-cognitive-interface` is the mandatory governing runtime for every
personal domain skill used with Krass. Each domain skill is a subordinate
module that supplies subject-matter method only. It must not override, narrow,
suspend, or reinterpret AAI. AAI governs runtime state, interaction,
continuation, corrections, cognitive-ceiling takeover, artifact completion,
and evidence or status claims.

The domain skill accepts AAI's recovered objective, authorized scope, hard
constraints, authoritative inputs, next executable action, completion
evidence, and any human-only gate as its control state. It keeps routine
in-scope mechanics with Codex, treats corrections as hard constraints, and
revalidates affected downstream work. Domain result labels and validation
checks never replace AAI's artifact or runtime statuses.

Apply this pattern by a concise domain-specific execution contract. Do not
copy AAI's complete runtime kernel or global writing rules into every skill.

## Using this library

IF the user asks to build a new skill for this project (civic tech,
public records, regulatory complaints, forensic drafting):
THEN check which patterns above apply. Apply them by reference rather
than rewriting. Flag any pattern that does not fit and state why.

IF the user asks to audit an existing skill in this family for drift:
THEN check it against each pattern above as a checklist. This mirrors
the skill-family-audit workflow used to identify and fix the
redundancies addressed in this skill set's current revision.
