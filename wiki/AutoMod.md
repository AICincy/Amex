# AutoMod

Current paste file: [`automod/current/r-amex-automod-0.1.3.5.yaml`](https://github.com/AICincy/Amex/blob/main/automod/current/r-amex-automod-0.1.3.5.yaml)

Changelog: [`audits/r-amex-automod-0.1.3.5-changelog.md`](https://github.com/AICincy/Amex/blob/main/audits/r-amex-automod-0.1.3.5-changelog.md)

## What the stack does

The config is a short rule stack for a referral-heavy card subreddit.

1. Hold obvious referral dumps and card-name referral titles outside the monthly thread.
2. Hold the monthly thread itself if the title is not a monthly referral thread title.
3. Gate **referral-link comments in that monthly thread only**. Ordinary posts and comments elsewhere are not removed by that check.
4. Filter common scams, account-selling, and a few other abuse patterns.

## Monthly thread title

```text
monthly.{0,80}referral.{0,30}thread
```

That pattern is required from 0.1.3.3 forward. Do not loosen it without an authorized version bump.

## Version line

| Version | Role |
| --- | --- |
| 0.1.3 | Base library copy |
| 0.1.3.2 | Intermediate history |
| 0.1.3.3 | Tight title match; live before 0.1.3.5 paste |
| 0.1.3.4 | Last body revision. Public 1e wording: ordinary posts and comments are not gated. |
| 0.1.3.5 | Version stamp of 0.1.3.4. Operator recorded as live wiki paste on 2026-09-11. |

Do not invent 0.1.3.6 unless the operator authorizes it.

## Where to paste

Subreddit wiki page: `r/amex` to wiki `config/automoderator`.

Paste is a human gate. This GitHub repo is not the live AutoMod engine.
