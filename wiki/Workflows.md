# Workflows

All workflows live under [`.github/workflows`](https://github.com/AICincy/Amex/tree/main/.github/workflows).

| Workflow | What it does |
| --- | --- |
| `validate-automod.yml` | Rejects text before `---` and `(?i)` in `automod/current/` |
| `guard-public-copy.yml` | Rejects unpublished floors in `comment:` and `sticky_comment:` |
| `lint-yaml.yml` | Parses GitHub and ops YAML |

Dependabot watches GitHub Actions weekly. See `.github/dependabot.yml`.

Scorecard, stale, lock-threads, labeler, dependency-review, and actionlint were removed. They are not needed for a paste repo.
