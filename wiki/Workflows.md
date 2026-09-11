# Workflows

All workflows live under [`.github/workflows`](https://github.com/AICincy/Amex/tree/main/.github/workflows).

| Workflow | What it does |
| --- | --- |
| `validate-automod.yml` | Rejects text before `---` and `(?i)` in current AutoMod files |
| `guard-public-copy.yml` | Rejects unpublished tokens in `comment:` and `sticky_comment:` |
| `lint-yaml.yml` | `yaml.safe_load_all` on every YAML file |
| `actionlint.yml` | Lints workflow files |
| `dependency-review.yml` | Reviews dependency diffs on pull requests |
| `labeler.yml` | Labels PRs from path changes |
| `stale.yml` | Marks and closes inactive issues and PRs |
| `lock-threads.yml` | Locks closed issues and PRs after 30 days |
| `scorecard.yml` | Weekly OpenSSF Scorecard, SARIF upload |

Dependabot watches GitHub Actions only. See `.github/dependabot.yml`.

## Not used

CodeQL, Pages deploy, and welcome bots are not part of this repo. There is no application runtime.
