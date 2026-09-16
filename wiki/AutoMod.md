# AutoMod

Current paste file: [`automod/current/r-amex-automod-0.1.3.5.yaml`](https://github.com/AICincy/Amex/blob/main/automod/current/r-amex-automod-0.1.3.5.yaml)

Changelog: [`audits/r-amex-automod-0.1.3.5-changelog.md`](https://github.com/AICincy/Amex/blob/main/audits/r-amex-automod-0.1.3.5-changelog.md)

## What the stack does

Verified against the tracked security-hardening draft. It is not proof of the
current Reddit wiki bytes.

1. Filter Amex referral URLs, named referral phrases, social links, and shortened links for moderator review. A user-controlled title does not create an exception.
2. Keep the former automatic 1e check disabled until the official monthly thread has a trusted, enforceable identity.
3. Remove email addresses, likely card numbers in every context, manufactured-spending mentions, and DM/PM solicitation.
4. Leave helper comments on a few FAQ titles. Those rules do not remove.

The bare `DM` / `PM` word rules are broader than packet 1b. That is in the authorized YAML. Do not change it without a version bump.

## Monthly referral thread

The old title regex is not a trusted identity. The hardening draft does not
grant a referral, social-link, or payment-card exception from a title match.
Monthly content needs moderator review until a trusted thread identity is
implemented and released.

## Version line

| Version | Role |
| --- | --- |
| 0.1.3 | Base library copy |
| 0.1.3.2 | Intermediate history |
| 0.1.3.3 | Tight title match |
| 0.1.3.4 | Last body revision |
| 0.1.3.5 | Operator recorded as live wiki paste on 2026-09-11. The tracked same-named file is now a non-deployed security-hardening draft pending a new versioned release. |

Do not paste the hardening draft until a moderator approves a new versioned release.

## Where to paste

Subreddit wiki page: `r/amex` wiki `config/automoderator`.

Paste is a human gate. This GitHub repo is not the live AutoMod engine.
