# Repository conventions

## Authority

1. Latest operator correction
2. Current file in `automod/current`
3. This-run official AutoMod fetch
4. Earlier history under `automod/history`
5. Model inference

## Versioning

Bump the filename when the operator authorizes a new AutoMod draft. Do not invent a version ahead of authorization.

## Public vs unpublished

Public `comment:` lines, stickies, and packet text must not name unpublished numeric floors.

## GitHub settings this host can set

- Files, workflows, Dependabot config, labels, CODEOWNERS, rulesets
- This host cannot patch description, topics, or install Marketplace apps

Recommended manual settings in GitHub UI:

- Description: `r/Amex AutoMod drafts and public Rule 1 copy`
- Topics: `reddit`, `automoderator`, `amex`
- Default branch: `main`
- Allow squash merge
- Pages: use `/docs` or root README only. Do not publish unpublished ops.
