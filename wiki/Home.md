# r/Amex staff handbook

Technical handbook for [AICincy/Amex](https://github.com/AICincy/Amex) and [r/amex](https://www.reddit.com/r/amex/).

This repository is an operator hub. It is not an application. Files here are drafts a moderator pastes into Reddit. The GitHub Wiki tab is empty. Use these files.

## Recorded live state

| Surface | Recorded state |
| --- | --- |
| AutoMod wiki | Operator recorded paste of **0.1.3.5** on 2026-09-11. Live wiki bytes not fetched this run. |
| Rule 1 TEXT | Waits for next monthly thread post. |
| Removal reason 1e | Advisory comment posted in the current monthly thread on 2026-09-13. Live Rules Hub bytes not fetched. |
| Monthly thread header | Operator recorded fixed 2026-09-13. |
| Crowd Control | 3-day trial started 2026-09-13. Re-inspect 2026-09-16. |
| Current YAML | [`automod/current/r-amex-automod-0.1.3.5.yaml`](https://github.com/AICincy/Amex/blob/main/automod/current/r-amex-automod-0.1.3.5.yaml) |

0.1.3.5 is a version stamp of 0.1.3.4. The last body change was 0.1.3.4.

## Pages

- [AutoMod](AutoMod.md)
- [YAML conventions](YAML-conventions.md)
- [Rule 1 and 1e](Rule-1-and-1e.md)
- [Safety Filters](Safety-Filters.md)
- [Human gates](Human-gates.md)
- [Repository layout](Repository-layout.md)
- [Workflows](Workflows.md)

## Hard rules

- Unpublished numeric floors stay in author checks and `action_reason` only. Never in `comment:`, stickies, Rule 1 text, or packet text.
- `combined_subreddit_karma` is not a sitewide post or comment gate. 1e is monthly-thread referral-URL comments only.
- Title match from 0.1.3.3 forward: `monthly.{0,80}referral.{0,30}thread`
- Do not add `(?i)` or `(?-i)` to search checks.
- Crowd Control and Reputation are Safety Filters, not AutoMod. Do not encode them as YAML.
- Do not commit `.env`, Exa keys, Firecrawl keys, or the unpublished-tokens list.
