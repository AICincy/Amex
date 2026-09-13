# r/Amex operator repo

Drafts for [r/amex](https://www.reddit.com/r/amex/) staff.

This is not an app. Nothing deploys. A green GitHub check does not change live Reddit.

Staff handbook is [`wiki/Home.md`](wiki/Home.md). The GitHub Wiki tab is a placeholder. Do not use it.
GitHub Projects is not enabled for this token. Use [`docs/staff-board.md`](docs/staff-board.md).

## Current recorded state

| Surface | Recorded state | Source |
| --- | --- | --- |
| AutoMod wiki | Operator recorded **0.1.3.5** on 2026-09-11. Live 1e comments match that text. | [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml) |
| Monthly referral thread | Live `1w4244u`, title `Monthly Amex Referral Thread`, stickied | https://www.reddit.com/r/amex/comments/1w4244u/monthly_amex_referral_thread/ |
| Common Questions thread | Live `1we44e6`, stickied | https://www.reddit.com/r/amex/comments/1we44e6/monthly_common_questions_advice_thread/ |
| Rule 1 TEXT | Next monthly thread cycle | [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md) |
| 1e public notice | Cannabun advisory comment in `1w4244u` | same thread |
| Crowd Control | 3-day trial started 2026-09-13. Re-inspect 2026-09-16. | Safety Filters |

Release: [v0.1.3.5](https://github.com/AICincy/Amex/releases/tag/v0.1.3.5)

## Staff daily use

1. Paste YAML: [`automod/current/`](automod/current/).
2. Paste Rule 1 / `1e` / header: [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md).
3. File live misses with the issue templates.

Do not put unpublished numeric floors in `comment:`, stickies, Rule 1, reason `1e`, or the thread header.

## What AutoMod does

- Remove referral and affiliate links outside the monthly referral thread.
- Gate referral-URL comments inside that thread only when the author fails the 1e author check.
- Remove email addresses, likely card numbers, manufactured-spending mentions, DM/PM solicitation, social links outside the monthly thread.
- Leave helper comments on a few FAQ titles. Those rules do not remove.

Title match:

```text
monthly.{0,80}referral.{0,30}thread
```

## Human gates

1. Wiki paste of current YAML if the draft changes.
2. Rule 1 TEXT on the next monthly thread cycle.
3. Crowd Control re-inspect on or after 2026-09-16.
4. Point the FAQ helper at `1we44e6` on the next authorized YAML paste. Draft still has August `1vm5hnj`.

## Checks

Validate AutoMod YAML. Guard public copy. Lint YAML. Publish release on dispatch.

## Do not commit

`.env`, Exa keys, Firecrawl keys, unpublished-tokens lists, live wiki dumps unless fetched that day.
