# Repository layout

Repo: [AICincy/Amex](https://github.com/AICincy/Amex)

```text
automod/current/     file to paste
automod/history/     prior versions (index unless YAML is copied in)
audits/              changelogs and auditor summaries
public/              Rule 1 and 1e text safe for Reddit UI
ops/                 redacted operator state
docs/                conventions
wiki/                source copy of this handbook
.github/             Actions, Dependabot, issue templates
.grok/               local Grok workspace pointer
```

Root copies of the current YAML exist for convenience. Prefer `automod/current/`.

## Public vs unpublished

The public repo may contain AutoMod YAML. It must not contain:

- `.env`
- Exa or Firecrawl keys
- the unpublished-tokens list
- numeric floors in `comment:`, stickies, or packet text

`ops/amex-ops-state.public.yaml` is the redacted operator state. Local host state may list unpublished token names. Do not copy those values into this wiki.

## Branch protection

Ruleset `protect-main` is active:

- no delete of `main`
- no force-push

Direct commits to `main` are still allowed. This is a solo operator repo.
