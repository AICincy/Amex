# AutoMod

Current paste file: [`automod/current/r-amex-automod-0.1.3.5.yaml`](https://github.com/AICincy/Amex/blob/main/automod/current/r-amex-automod-0.1.3.5.yaml)

Changelog: [`audits/r-amex-automod-0.1.3.5-changelog.md`](https://github.com/AICincy/Amex/blob/main/audits/r-amex-automod-0.1.3.5-changelog.md)

## What the stack does

Verified against the current YAML file. It does not remove a post only because the title fails the monthly-thread regex.

1. Remove Amex referral URLs and named referral phrases outside a submission whose title matches the monthly-thread regex.
2. Inside a matching monthly thread, remove referral-URL comments when the author fails the unpublished 1e author check.
3. Remove email addresses, likely card numbers (outside the monthly thread), manufactured-spending mentions, DM/PM solicitation, and social URLs outside the monthly thread.
4. Leave helper comments on a few FAQ titles. Those rules do not remove.

The bare `DM` / `PM` word rules are broader than packet 1b. That is in the authorized YAML. Do not change it without a version bump.

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
| 0.1.3.3 | Tight title match |
| 0.1.3.4 | Last body revision |
| 0.1.3.5 | Version stamp of 0.1.3.4. Operator recorded as live wiki paste on 2026-09-11. |

Do not invent 0.1.3.6 unless the operator authorizes it.

## Where to paste

Subreddit wiki page: `r/amex` wiki `config/automoderator`.

Paste is a human gate. This GitHub repo is not the live AutoMod engine.
