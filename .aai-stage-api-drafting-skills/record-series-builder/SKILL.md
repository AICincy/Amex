---
name: record-series-builder
description: Turns large document sets into matched multi-volume series with consistent structure, formatting, handoff pages, abbreviations, and output artifacts. Use when organizing records into volumes, normalizing Markdown/DOCX/PDF packets, or aligning multiple packets. Also use when the user says organize this packet, build a series, or package these records.
---

# Record Series Builder

## Execution contract

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate domain module that supplies record-series methods only. It must
not override, narrow, suspend, or reinterpret AAI. The user owns the package
objective and material choices. Codex owns routine inventory, architecture,
normalization, audit routing, rendering, invariance checks, visual QA, safe
retries, and index generation inside that objective.

Accept AAI's recovered objective, authorized scope, hard constraints,
authoritative source and target identities, next executable action,
completion evidence, and any human-only gate as the control state. AAI also
governs corrections, cognitive-ceiling takeover, artifact completion, and
evidence or status claims. Platform and safety instructions remain
authoritative. Treat corrections as hard constraints across every affected
volume and derivative render, then rebuild and revalidate them. During
takeover, surface only one actual gate or exact blocker.

Inventory, render-diff, content, and visual checks prove domain validation
only. They do not prove `SAVED`, `INSTALLED`, `RUNTIME-VERIFIED`, or
`ADVERSARIAL-PASS` without the evidence AAI requires. Complete the AAI
artifact transaction for every reusable series artifact.

The canonical directory name is `record-series-builder`. Treat hashed export
folders as transport wrappers. See
[references/package-identity.md](references/package-identity.md),
[references/scope-boundary.md](references/scope-boundary.md), and
[references/sibling-routing.md](references/sibling-routing.md).

This skill packages files into matched volumes. It does not turn a file
inventory into a record, occurrence, or attachment graph. Hash-identical
copies stay flagged, not merged, until Krass authorizes removal.

If `aai-cognitive-interface`, documents, pdf, claim-source-auditor,
authority-currency-auditor, or forensic-evidentiary-drafting is absent,
degrade per sibling-routing.md. Do not invent those outputs or call a legal
packet filing-ready.

Use subagents for genuinely independent volume audits or visual QA when that
reduces latency or context pressure. Give each branch explicit files and a
concrete deliverable. The primary agent owns cross-volume reconciliation,
canonical source selection, and final package verification.

## Codex/ChatGPT Work bindings

Use the installed `documents` skill for DOCX rendering and `pdf` for PDF
rendering/verification. Resolve sibling personal skills by `SKILL.md`
frontmatter name before reading their bundled references or scripts; do not
assume their installation directory matches the human-facing skill name.

## Matter context

IF a matter file (matter-[name]-verified-facts.md) exists for the series
being built:
THEN load it before proposing volume architecture. Use its exhibit
ledger to keep exhibit IDs consistent across volumes. Treat its verified
facts as a provenance-bearing baseline under the claim-source rules. Treat
logged user corrections as hard constraints.

IF no matter file exists and the series is matter-related:
THEN proceed using available context and sources. Create persistent matter
state only when that is within the requested objective.

IF that template cannot be located:
THEN continue the series task without inventing template content. Try another
installed-skill resolution path first. Surface the missing template only if
it actually blocks an authorized persistence task.

## Rules

IF the user provides a large document set:
THEN inventory the current packet set before proposing any structure.
Run [scripts/inventory.py](scripts/inventory.py) over the working
directory to list sources, outputs, scripts, and flagged stale residue
as a table, rather than listing files by hand.

IF organizing into volumes:
THEN define the series architecture first: volume names, section order,
handoff logic, and file-type subfolders. If a reasonable architecture follows
from the requested objective, state it briefly and build. Ask for a decision
only when competing architectures materially change scope, audience,
filing strategy, or another user-owned value judgment.

IF multiple volumes share the same controlling document type and recipient
class:
THEN enforce matched section order, consistent headings, stable abbreviations,
and matching rendering rules across those volumes.

IF a series combines heterogeneous court, agency, evidentiary, or recipient
documents:
THEN preserve each subordinate domain skill's controlling structure. Match
only package-wide elements that do not conflict, including title treatment,
abbreviations, exhibit identifiers, cross-volume references, and rendering
tokens.

IF the series is a legal filing package (forensic analysis, suppression
memo appendix, evidence inventory, regulatory complaint, demand letter
set):
THEN first run claim-source-auditor on record-backed factual assertions and
authority-currency-auditor on legal authorities in the Markdown source. Fix
or explicitly resolve audit defects before treating that Markdown as the
canonical render source. Then apply the Template Spec table from
forensic-evidentiary-drafting only as the visual and rendering style source
for docx and PDF output across applicable volumes. Do not import its output
format, file-size, filing-procedure, court-routing, or recipient-specific rows;
those remain controlled per volume by the identified court, agency, recipient,
and subordinate domain skill.

IF a volume's final section needs to hand off to the next volume:
THEN include explicit handoff language. The last page of volume N
references volume N+1 by name and states what it covers.

IF the series has two or more volumes:
THEN generate a master index with
[scripts/build_index.py](scripts/build_index.py), linking each volume
and its sections and surfacing each handoff line. Regenerate the index
whenever volume headings change.

IF the user asks to normalize across formats (Markdown, DOCX, PDF):
THEN apply the same structural rules to all formats. Heading levels,
table styles, abbreviation usage, and section order must match
regardless of output format.

IF a volume has been rendered from markdown to docx or PDF:
THEN extract the text content from each rendered file and compare it
against the audited markdown source with
[scripts/render_diff.py](scripts/render_diff.py). Any content delta
beyond formatting triggers re-audit of the changed passages
(claim-source-auditor for factual passages, authority-currency-auditor
for citations) before delivery. Route deltas to review; do not
auto-deliver and do not auto-fail on formatting-only differences.

IF text extraction from a rendered format fails or is unavailable:
THEN try another safe available extraction route for that format. Record the
failed route. If no route can establish source/render invariance, do not call
a legal package filing-ready. Deliver a clearly labeled non-final artifact
only when useful, with the unresolved invariance gap named.

IF stale, duplicate, or intermediate artifacts exist in the workspace:
THEN flag them for removal. Do not delete without the user's approval. Build
and present the verified package from a clean authoritative output directory
that excludes them. If clean isolation is impossible, keep the package
non-final and use `BLOCKED`; flagging alone does not establish an authoritative
package.

IF rendering or cleanup cannot finish:
THEN diagnose the failure and retry safe local steps or an available alternate
render/extraction route. Continue independent volumes. If a material blocker
remains, return completed artifacts plus the exact unresolved item and do not
overstate package readiness.

## Output structure

Per volume:
- Markdown source file.
- DOCX rendered file only when the current controlling court or recipient
  rules require or permit editable Word output.
- PDF rendered file when required for filing or requested for distribution.
- Do not create an extra rendered format that conflicts with the controlling
  recipient or filing requirements.
- Scripts subfolder (if build or render scripts exist).

For the series as a whole:
- index.md, the master index generated by build_index.py, when two or
  more volumes exist.

## Validation

IF the series is a legal filing package and the environment provides
code execution:
THEN run the forensic-evidentiary-drafting skill's
scripts/validate_document.py on each volume before delivery. Any script
content failure on any volume blocks the package until fixed. A tool/input
failure triggers recovery through another safe route before the package can
be called filing-ready.

Before delivery:
- Each volume has the intended outputs and only the approved outputs.
- Matched volumes share the same structure, tone, and formatting rules.
- Filenames, folder names, and handoff language are consistent.
- The authoritative output directory contains no stale, duplicate, or
  intermediate artifacts. Unapproved residue remains outside that directory.
- index.md exists and is current with the volumes' headings, when two
  or more volumes exist.

For a legal package, every rendered artifact must also pass source/render
invariance and visual inspection at representative pages after the final
source audit before it is called filing-ready.

## References

- [scripts/inventory.py](scripts/inventory.py): Scans a directory and
  produces the pre-build inventory table (path, type, size, modified,
  stale-candidate flags).

- [scripts/build_index.py](scripts/build_index.py): Generates index.md
  from a set of volume markdown files, linking sections and surfacing
  handoff lines.

- [scripts/render_diff.py](scripts/render_diff.py): Post-render
  invariance check. Extracts text from a rendered docx or PDF, normalizes
  whitespace, and diffs content tokens against the markdown source.
  Report-only; exits 1 on content deltas and 2 on extraction/tool/input
  failure so recovery or the limitation is explicit.

- [references/scope-boundary.md](references/scope-boundary.md): File
  packet vs typed-record profile.

- [references/series-state.md](references/series-state.md): Domain state
  fields.

- [references/sibling-routing.md](references/sibling-routing.md): Governor
  and sibling degrade rules.

- [references/coordination-contract.md](references/coordination-contract.md):
  Current-turn autonomy and evidence boundary.

- [references/package-identity.md](references/package-identity.md): Name,
  wrapper folders, and claimable status.

- [references/acceptance-tests.md](references/acceptance-tests.md):
  Behavior cases after a material revision.

When filesystem execution is available, run
`python3 scripts/aai_runtime_gate.py package <skill-directory>` after
modifying this skill. That is STATIC-PASS only.
