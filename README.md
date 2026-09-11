# r/Amex operator hub

Public working copy for r/Amex AutoMod drafts, audits, and public Rule 1 text.

Live subreddit: [r/amex](https://www.reddit.com/r/amex)

This repository does not paste the live wiki. Wiki paste stays a human gate.

## Current draft

- AutoMod: [`automod/current/r-amex-automod-0.1.3.5.yaml`](automod/current/r-amex-automod-0.1.3.5.yaml)
- Changelog: [`audits/r-amex-automod-0.1.3.5-changelog.md`](audits/r-amex-automod-0.1.3.5-changelog.md)
- Public Rule 1 copy: [`public/r-amex-rule-1-public-copy.md`](public/r-amex-rule-1-public-copy.md)
- Operator state (redacted): [`ops/amex-ops-state.public.yaml`](ops/amex-ops-state.public.yaml)

Recorded live wiki version: 0.1.3.3 (not fetched from the wiki in this repo).

## Folders

| Folder | What lives here |
| --- | --- |
| `automod/current` | Draft to paste when the operator authorizes it |
| `automod/history` | Prior versions 0.1.3 through 0.1.3.4 |
| `automod/prompts` | Grok invoke prompts for review and 0.1.3.5 |
| `audits` | Library comparison and per-version auditor JSON |
| `public` | Rule 1 / 1e text safe for Rules Hub and stickies |
| `ops` | Redacted operator state and human-gate notes |
| `docs` | Repo and host conventions |
| `.grok` | Local Grok workspace pointer for this repo |
| `.github` | Dependabot, Actions, issue templates, CODEOWNERS |

## Hard rules

- Do not put unpublished numeric floors in `comment:`, stickies, or packet text.
- `combined_subreddit_karma` is not a sitewide post or comment gate. 1e is monthly-thread referral-URL comments only.
- Title match from 0.1.3.3 forward: `monthly.{0,80}referral.{0,30}thread`
- Do not add `(?i)` to search checks.
- Crowd Control and Reputation are Safety Filters, not AutoMod. Inspect only. Do not encode them as YAML.
- Do not commit Exa or Firecrawl keys, `.env`, or the unpublished-tokens list.

## Human gates

Wiki paste, Rules Hub paste, and Safety Filter inspection stay with the operator.

## GitHub Apps in use

- GitHub Actions: workflow under `.github/workflows`
- Dependabot: `.github/dependabot.yml` watches GitHub Actions
- Pages and Discussions are enabled on the repository

Marketplace apps cannot be installed from this host. Enable GitHub Copilot or extra apps in the repo Settings UI if needed.

## Grok host

Workspace pointer: `.grok/workspace.yaml`

On the Grok host the matching local file is `/home/workdir/.grok/repos/aicincy-amex.yaml`.
