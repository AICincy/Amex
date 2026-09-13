# r/Amex staff repo

Working copies for [r/amex](https://www.reddit.com/r/amex/) moderation.

This is not an app. Nothing deploys. Files here are drafts a moderator pastes into Reddit.

Audience: r/Amex staff. If you can paste wiki, Rules Hub, or Safety Filters, this page is for you.

## Current state

| Surface | Recorded state | Paste source |
| --- | --- | --- |
| AutoMod wiki `config/automoderator` | Operator recorded **0.1.3.5** on 2026-09-11 | [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml) |
| Rule 1 body | Operator recorded 2026-09-10 | [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md) |
| Removal reason `1e` | Operator recorded 2026-09-10 | same file |
| Monthly referral thread header | Operator recorded 2026-09-10 | same file |
| Crowd Control | Posts Off, comments Off | Safety Filters. Not YAML. |
| Reputation | Inspect only | Safety Filters. Not YAML. |

0.1.3.5 is a version stamp of 0.1.3.4. The last rule-body change was 0.1.3.4.

Live Reddit bytes are not fetched by this repo. The table is operator-reported.

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

A person must do these. A push to GitHub does not change live r/amex.

1. Paste [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml) into wiki `config/automoderator`.
2. Paste Rule 1, reason `1e`, and the thread header from [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md) if public wording changed.
3. Inspect Crowd Control. Leave posts and comments Off unless a separate abuse problem requires a filter.
4. Record the paste in [`ops/amex-ops-state.public.yaml`](ops/amex-ops-state.public.yaml).

Do not put unpublished numeric floors in `comment:`, stickies, Rule 1, reason `1e` public text, or the thread header.

## Ship a YAML change

1. Edit only the file in `automod/current/`.
2. First line must be `---` with no text above it.
3. Do not add `(?i)` or `(?-i)` to search checks.
4. Prefer single-quoted regex. Do not wrap a regex field in a YAML `\|` block.
5. Keep `combined_subreddit_karma` on the monthly-thread referral-URL comment rule only.
6. Push to `main` or open a PR. Actions parse YAML and guard public copy.
7. Complete the human gates above.
8. Do not invent a version newer than the one staff authorized.

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

## Do not commit

- `.env`, Exa keys, Firecrawl keys
- unpublished-tokens lists
- live wiki dumps unless fetched that day

## Checks

- [Validate AutoMod YAML](.github/workflows/validate-automod.yml)
- [Guard public copy](.github/workflows/guard-public-copy.yml)

Ruleset `protect-main`: no delete of `main`, no force-push. Direct commits are allowed.
