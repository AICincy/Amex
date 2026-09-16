---
name: reddit-automod-yaml
description: Audits and remediates supplied Reddit AutoModerator YAML against current official sources. Use when writing AutoMod regex, compiling a rule file, fixing illegal groups, auditing a config, or preparing a wiki YAML draft. Does not publish or paste the wiki.
---

# Reddit AutoMod YAML

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate YAML audit and remediation module. It must not override, narrow,
suspend, or reinterpret AAI. Platform and safety rules stay authoritative.

Accept AAI's recovered objective, authorized scope, hard constraints,
authoritative sources, next executable action, completion evidence, and any
human-only gate as control state. Domain status claims stay with AAI.

If `aai-cognitive-interface` is not loaded, say so and stop. Do not
self-govern.

## AAI coordination and autonomous execution

This package participates only through the active Codex turn. It is not a
background worker and cannot privately message a sibling, select an unseen
connector, or make a Reddit write. The active agent silently composes the
applicable methods under AAI, selects from tools exposed in the current turn,
and makes authorized inspection or retrieval calls autonomously.

Use a current official source when a syntax or behavior claim needs support.
If an exposed source route fails, retain the finding as unresolved, record the
observed limit, and try the next authorized route. A sibling result is a
constraint or source candidate, not proof or permission to widen scope. Draft
YAML only. Wiki paste, filter toggles, and every live moderator action remain
human gates. See [references/coordination-contract.md](references/coordination-contract.md).

This package drafts, audits, and remediates AutoModerator YAML. It does not
paste `config/automoderator`. It does not toggle Safety Filters.

## Outcome

Return one of

- an audit of a supplied YAML file against live official AutoMod sources fetched this run
- a remediating YAML file plus the audit that justified each change
- a fact-grounded suggestion that cites the fetched page, or UNRESOLVED

Do not ship syntax from model memory.

## Load order

1. `aai-cognitive-interface`
2. This skill
3. An official-source retrieval tool exposed in the current turn
4. `reddit-owner-ops` for human gates, engine vs filter split
5. `subreddit-rule-packet` when public rule text or a sticky header is in scope
6. `claim-source-auditor` when mapping a finding to a source
7. `research-execution-briefs` when comparing official pages

If no authorized source route is exposed, mark the syntax claim UNRESOLVED.
Do not invent AutoMod syntax to fill the gap.

## Required fetch before any audit or edit

Use an exposed retrieval tool to inspect the current official pages. Start with
the URLs in [references/source-canon.md](references/source-canon.md). Those
URLs are locators, not holdings.

A syntax claim is allowed only when this run's retrieval contains it. If the
result is navigation chrome or otherwise lacks the article body, retry one
authorized route and mark the claim UNRESOLVED if the body remains missing.

Record route, URL, and fetch time in the audit. Do not print keys.

## Workflow

1. Resolve the current authoritative YAML. Prefer the file the operator named this turn.
2. Retrieve the necessary current official documentation through an exposed tool.
3. Run `python3 scripts/audit_automod.py <yaml> [tokens-file]`.
4. Classify each finding as compile, yaml, scope, public-copy, dual-engine, or unresolved-source.
5. Remediate only the authorized findings. Keep unpublished numeric floors in `author` checks and `action_reason`. Keep them out of `comment:`, stickies, and packet text.
6. Re-run the audit on the remediating file.
7. Hand wiki paste, Rules Hub paste, and Safety Filter inspection to the operator.

## Hard constraints

- Search checks are case-insensitive unless the fetched docs say otherwise. Do not add `(?i)` or `(?-i)` unless the fetched compiler notes allow that group.
- Prefer single-quoted regex. Double-quoted regex must double-escape.
- Do not put any text before the first `---` document separator.
- A YAML `|` block on a regex field injects indent and newlines into the pattern. Convert those to a quoted one-liner.
- `---` must sit on its own line with no leading spaces.
- Title-regex exemptions beat hardcoded thread IDs. Tight title patterns beat loose `word.{0,n}word` pairs that match ordinary posts.
- Crowd Control and Reputation are not AutoMod. Do not encode them as YAML. Do not toggle them.
- Do not store community floors, thread IDs, or ban reasons in this skill.
- Do not claim the live wiki matches the artifact unless the operator recorded the paste.

## Output contract

Write only named, user-authorized artifacts. Use the current workspace or a
user-authorized destination. A version bump is a draft decision, not evidence
that a live wiki changed.

Every remediating change lists finding id, fetched source URL, before snippet,
after snippet, and whether behavior changes.

If a requested fix has no fetched source, write UNRESOLVED and leave the line
unchanged.

## Scripts

- [scripts/audit_automod.py](scripts/audit_automod.py)

## References

- [references/source-canon.md](references/source-canon.md)
- [references/failure-modes.md](references/failure-modes.md)
- [references/sibling-routing.md](references/sibling-routing.md)
- [references/coordination-contract.md](references/coordination-contract.md)
- [references/acceptance-tests.md](references/acceptance-tests.md)
- [assets/audit-report.template.md](assets/audit-report.template.md)
