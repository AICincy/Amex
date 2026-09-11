# Amex

Working copy for [r/amex](https://www.reddit.com/r/amex/) AutoMod, public Rule 1 text, and operator notes.

This is not an app. There is nothing to deploy. The files here are the drafts a moderator pastes into Reddit.

## Status

| Surface | Recorded state |
| --- | --- |
| AutoMod wiki | Operator recorded paste of **0.1.3.5** on 2026-09-11. This repo does not fetch live wiki bytes. |
| Rule 1 / 1e public copy | Operator recorded paste on 2026-09-10. |
| Crowd Control | Inspected On, then operator set posts Off and comments Off. |
| Current YAML | [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml) |

0.1.3.5 is a version stamp of 0.1.3.4. The last body change was 0.1.3.4.

## What AutoMod does here

The live config is a short stack of rules for a referral-heavy card subreddit:

- Hold obvious referral dumps and card-name referral titles outside the monthly thread.
- Hold the monthly thread itself if the title is not a monthly referral thread title.
- Gate **referral-link comments in that monthly thread only**. Ordinary posts and comments elsewhere are not removed by that check.
- Filter common scams, account-selling, and a few other abuse patterns.

The monthly-thread title match is:

```text
monthly.{0,80}referral.{0,30}thread
```

Crowd Control and Reputation are Reddit Safety Filters. They are not AutoMod and they are not stored in the YAML.

## Public vs unpublished

Public comment text, Rule 1, removal reason 1e, and the monthly-thread header must not include unpublished numeric floors.

`combined_subreddit_karma` is not a sitewide post or comment gate. It belongs on monthly-thread referral-URL comments only.

Paste these three public blocks from [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md):

1. Rule 1 body in Rules Hub
2. Removal reason `1e`
3. Addendum on the current monthly referral thread

## How to ship a new AutoMod version

1. Edit or add a file under `automod/`.
2. Keep the first line `---` with no text above it.
3. Do not add `(?i)` to search checks. Official search checks are already case-insensitive.
4. Prefer single-quoted regex. Do not wrap a regex field in a YAML `|` block.
5. Push. GitHub Actions parses the YAML on `main` and on pull requests.
6. A person pastes the file into `r/amex` wiki `config/automoderator`.
7. A person pastes Rule 1 / 1e if the public wording changed.
8. A person inspects Crowd Control. Do not encode that toggle in YAML.

Wiki paste is always a human gate.

## Repository map

```text
automod/current/     file to paste
automod/history/     prior versions (index only unless the YAML is copied in)
audits/              changelogs and auditor summaries
public/              Rule 1 and 1e text safe for Reddit UI
ops/                 redacted operator state
docs/                conventions
.github/             Actions, Dependabot, issue templates
```

Root copies of the current YAML exist for convenience. Prefer `automod/current/`.

## Checks that stay in force

- No `(?i)` and no `(?-i)` on search fields.
- Title match stays `monthly.{0,80}referral.{0,30}thread` unless a later version is authorized.
- Do not commit `.env`, Exa keys, Firecrawl keys, or the unpublished-tokens list.
- Do not invent a version past the one the operator authorized.

## GitHub setup already applied

- Workflow: [Validate AutoMod YAML](.github/workflows/validate-automod.yml)
- Dependabot watches GitHub Actions only
- Ruleset `protect-main`: no delete of `main`, no force-push. Direct commits are still allowed.

Topics, Pages, and secret scanning are Settings UI. This host cannot write those fields.

## Owner

[AICincy](https://github.com/AICincy) operates this copy for r/amex.
