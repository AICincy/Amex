---
name: subreddit-rule-packet
description: Writes reviewable subreddit rule packets with coded removal reasons. Use when drafting or revising community rules, removal reasons, sidebar text, or a monthly thread header for Reddit. Do not use for legal memos, research briefs, social posts, or live Reddit publication.
---

# Subreddit Rule Packet

## Execution contract

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate domain module that supplies one load format only. It must not
override, narrow, suspend, or reinterpret AAI. Platform and safety
instructions remain authoritative.

Accept AAI's recovered objective, authorized scope, hard constraints,
completion evidence, and corrections as control state. If AAI is not loaded,
say so and stop. Continue the packet emit and validate loop without asking
Krass to pick tools. The accepted specimen is
[assets/format-specimen.txt](assets/format-specimen.txt). That file is the
format authority. Do not invent a kit, memo, slide deck, or essay instead.

The canonical directory name is `subreddit-rule-packet`.

Domain completeness is not an AAI status claim. Do not label the packet
`INSTALLED` or `RUNTIME-VERIFIED`.

## AAI coordination and autonomous execution

This package is a format method inside the active Codex turn. It is not a
background process and cannot privately message sibling skills, invoke unseen
tools, or load rules into Reddit. The active agent silently composes relevant
methods under AAI, selects exposed tools autonomously, and preserves the
current source boundary.

Use `reddit-owner-ops` for human moderator gates and
`reddit-automod-yaml` to assess YAML mechanics. A sibling result is a bounded
input, not evidence of a live community state or a completed publication. If a
source, sibling, or tool is unavailable, name that limit and keep the packet
as a draft. See [references/coordination-contract.md](references/coordination-contract.md).

## Output contract

Write only the packet artifacts the user names. When both are requested, use:

- `<slug>-rules.txt` using the specimen section labels
- `<slug>-rules.load.json` using the specimen JSON keys

Do not add extra deliverables. Do not wrap the packet in a plan or a
publication record.

Required txt sections, in this order:

1. `ENFORCEMENT`
2. `COMMUNITY DESCRIPTION`
3. For each rule `N` starting at 1
   - `RULE N TITLE`
   - `RULE N TEXT`
   - `RULE N REMOVAL REASONS`
   - one or more lines `Na. sentence` `Nb. sentence`
4. `MONTHLY THREAD HEADER` when the community uses a sticky exception thread

Blank line between sections. No markdown headings. No commentary.

JSON keys:

- `subreddit`
- `enforcement`
- `community_description`
- `rules[]` with `kind`, `short_name`, `description`, `violation_reasons[{code,text}]`
- `monthly_thread_header` when applicable

Reason codes use the rule number plus a letter. Rule 1 reasons are `1a`, `1b`,
`1c`. Do not emit a single generic reason per rule.

## Register

Adult readers, 21 and older. Formal grammar. Short sentences. No slang in the
packet. No jokes. No process narration.

Sitewide Reddit terms are the floor. Subreddit rules name the local additions.
Members report. Moderators enforce. Say that in `COMMUNITY DESCRIPTION` when
it is true for the community.

Title at most 100 characters. Rule text at most 220 characters unless the user
sets another cap. Each removal reason is one sentence.

## Content rules

Keep every controlling policy the user or source already set. Do not invent
unpublished enforcement numbers, including karma thresholds.

Do not restore obsolete penalty lines the user struck, including first-strike
permanent-ban slogans and remove-first warning ladders, unless the current
source still uses them.

If a rule needs more than one removal path, add letters. Do not lengthen the
rule text to cover every path.

## Emit

When filesystem execution is available, write the packet with
[scripts/emit_packet.py](scripts/emit_packet.py) and check it with
[scripts/validate_packet.py](scripts/validate_packet.py).

See [references/format.md](references/format.md) for the label grammar.
Use [references/sibling-routing.md](references/sibling-routing.md) for
cross-skill boundaries and [references/acceptance-tests.md](references/acceptance-tests.md)
after a material revision.
