# Repository layout

Repo: [AICincy/Amex](https://github.com/AICincy/Amex)

```text
automod/current/   file to paste into AutoMod
automod/history/   index of prior versions
audits/            changelog and auditor summary
public/            Rule 1, 1e, and thread header
ops/               redacted operator state
docs/              conventions
wiki/              staff handbook
.github/           Actions and issue templates
```

There is no root YAML copy. Use `automod/current/`.

## Public vs unpublished

The public repo may contain AutoMod YAML. It must not contain:

- `.env`
- Exa or Firecrawl keys
- the unpublished-tokens list
- numeric floors in `comment:`, stickies, or packet text

`ops/amex-ops-state.public.yaml` is the redacted operator state.
