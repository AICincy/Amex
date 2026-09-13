# r/Amex operator repo

Drafts for [r/amex](https://www.reddit.com/r/amex/) staff.

This is not an app. Nothing deploys. A green GitHub check does not change live Reddit. A person pastes the files.

- Staff: paste sources, file issues, inspect live behavior.
- Owner (`AICincy`): authorize versions, merge YAML, record pastes in `ops/`.

## Current recorded state

| Surface | Recorded state | Source |
| --- | --- | --- |
| AutoMod wiki `config/automoderator` | Operator recorded **0.1.3.5** on 2026-09-11 | [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml) |
| Rule 1 TEXT | Waits for next monthly thread post | [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md) |
| Removal reason `1e` | Advisory comment posted in current monthly thread 2026-09-13 | same file |
| Monthly referral thread header | Operator recorded fixed 2026-09-13 | same file |
| Crowd Control | 3-day trial started 2026-09-13. Re-inspect 2026-09-16. | Safety Filters. Not YAML. |
| Reputation | Inspect only | Safety Filters. Not YAML. |

0.1.3.5 is a version stamp of 0.1.3.4. Last rule-body change: 0.1.3.4.

This repo does not fetch live Reddit bytes. The table is operator-reported. Remaining gate: Rule 1 TEXT on the next monthly thread post. Crowd Control trial ends 2026-09-16.

## Staff daily use

1. Need the live AutoMod draft? Open [`automod/current/`](automod/current/).
2. Need Rule 1 / `1e` / thread header text? Open [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md).
3. See a live miss? Open an issue with the AutoMod or live-behavior template.
4. Finished a paste? Open a paste-record issue or ask the owner to update `ops/`.

Do not put unpublished numeric floors in `comment:`, stickies, Rule 1, reason `1e` public text, or the thread header.

## What AutoMod does

- Remove referral and affiliate links outside the monthly referral thread.
- Gate referral-URL comments **inside that thread only** when the author lacks sufficient r/Amex participation.
- Remove common abuse: email addresses, likely card numbers, manufactured-spending mentions, DM/PM solicitation, social links outside the monthly thread.
- Leave helper comments on a few FAQ titles. Those rules do not remove.

Monthly-thread title match:

```text
monthly.{0,80}referral.{0,30}thread
```

Ordinary posts and comments outside that thread are not removed by the 1e participation check.

## Human gates

GitHub cannot do these. A moderator with wiki / Rules Hub / Safety Filters access must.

1. Paste the current YAML into wiki `config/automoderator`.
2. Paste Rule 1 TEXT on the next monthly thread cycle.
3. Re-inspect Crowd Control when the 3-day trial ends.
4. Record the result in [`ops/amex-ops-state.public.yaml`](ops/amex-ops-state.public.yaml).

## Owner change path

1. Edit only `automod/current/`.
2. First line must be `---` with no text above it.
3. Do not add `(?i)` or `(?-i)` to search checks.
4. Prefer single-quoted regex. Do not wrap a regex field in a YAML `|` block.
5. Keep `combined_subreddit_karma` on the monthly-thread referral-URL comment rule only.
6. Push to `main` or open a PR. Actions must pass.
7. Complete the human gates.
8. Do not invent a version newer than the one the owner authorized.

Ruleset `protect-main`: no delete of `main`, no force-push. Direct commits by the owner are allowed.

## Layout

```text
automod/current/   file to paste into AutoMod
automod/history/   index of prior versions
public/            Rule 1, 1e, and thread header
ops/               redacted operator state
audits/            changelog and auditor summary
docs/              repo conventions
wiki/              staff handbook pages
.github/           Actions and issue templates
```

Handbook pages: [`wiki/Home.md`](wiki/Home.md).

## Checks that run

| Workflow | What it rejects |
| --- | --- |
| [Validate AutoMod YAML](.github/workflows/validate-automod.yml) | text before `---`, `(?i)` in current YAML |
| [Guard public copy](.github/workflows/guard-public-copy.yml) | unpublished floors in `comment:` / `sticky_comment:` |
| [Lint YAML](.github/workflows/lint-yaml.yml) | broken GitHub or ops YAML |

## Do not commit

- `.env`, Exa keys, Firecrawl keys
- unpublished-tokens lists
- live wiki dumps unless fetched that day
