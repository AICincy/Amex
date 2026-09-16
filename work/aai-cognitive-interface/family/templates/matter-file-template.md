# Matter File Template

This template formalizes the verified-facts-ledger pattern (the
bwc_verified_facts.md convention) for any active matter: a criminal
defense matter, a public-records dispute, a regulatory complaint, or a
civic-tech project with a legal track.

A matter file is a single markdown file used as persistent working state.
Skills load it first and treat verified facts as a previously verified
baseline carrying the recorded provenance. They do not casually re-derive
settled facts. They re-check the underlying source when provenance is absent,
the source identity/version changed, or a new draft materially conflicts with
the baseline. Logged user corrections remain hard constraints.

## File naming

`matter-[short-name]-verified-facts.md`

Example: `matter-example-verified-facts.md`.

## Required sections

### 1. Matter identification

| Field | Value |
|---|---|
| Matter name | |
| Case or docket number | |
| Court or agency | |
| Jurisdiction | |
| Filing status | Pro se / represented |
| Next deadline | Date and description |

### 2. Verified facts (immutable)

Numbered, dated facts. Each fact carries a source pointer. Once a fact
is added here, no skill rewrites it without an explicit correction
logged in section 5.

| Fact ID | Fact | Source | Verified date |
|---|---|---|---|

### 3. Exhibit ledger

Tracks exhibit identifiers across every document produced for this
matter, so Exhibit A in one volume is the same Exhibit A everywhere.

| Exhibit ID | Description | Source file | First used in |
|---|---|---|---|

### 4. Citation status cache

Caches the most recent authority-currency-auditor result for each authority
cited in this matter. The cache accelerates background work. Filing,
publication, external send, expressly current work, and other time-sensitive
uses require fresh current-session verification regardless of cache age.
Background research may reuse a non-time-sensitive entry within 30 days.

| Authority | Status | Verified date | Note |
|---|---|---|---|

### 5. Correction log

Every user correction to a Codex-generated fact, timestamp, or
attribution in this matter. Per aai-cognitive-interface, a logged
correction is a hard constraint for the remainder of work on this
matter. No skill produces output contradicting a logged correction.

| Date | What was wrong | Correction | Applies to |
|---|---|---|---|

### 6. Open items

| Item ID | Description | Owner | Status |
|---|---|---|---|

## How skills use this file

IF a matter file exists for the active task:
THEN load it before drafting, auditing, or organizing. Use section 1
for headers and jurisdiction rules. Use section 2 as a provenance-bearing
baseline under the re-check conditions above. Use section 3
to assign new exhibit IDs without collision. Use section 4 to skip
redundant authority-currency-auditor calls within the cache window.
Use section 5 as binding constraints. Use section 6 to surface
outstanding work without the user repeating it.

IF the current task produces a new verified fact, exhibit, citation
check, or correction:
THEN update the existing matter file when that persistence is already within
the authorized matter workflow, and include the update in the execution
trail. If persistence would widen the task, propose it without writing.

IF no matter file exists and the task clearly involves an ongoing
matter:
THEN state that no matter file was found, proceed using conversation
context and available sources. Create one from this template only when
persistent matter state is within the requested objective.
