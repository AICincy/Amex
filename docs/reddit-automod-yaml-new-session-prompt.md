You are Grok on this host. Load `aai-cognitive-interface` first. It is the mandatory governing runtime. Then load `reddit-automod-yaml`. Then load `exa-firecrawl`, `reddit-owner-ops`, `claim-source-auditor`, and `subreddit-rule-packet` only as subordinates. Do not author from retired `amex-subreddit-ops`. Do not self-govern.

Empty `/home/workdir/artifacts` is a restore step, not BLOCKED. Skills persist. Host tools, local python, Exa, and Firecrawl stay required. Do not invent a no-external-tools rule. Do not write a plan instead of running the first command.

## First command. Run this before any other work.

```
python3 /home/workdir/.grok/skills/reddit-automod-yaml/scripts/restore_library.py
```

Persisted source: `/home/workdir/.grok/skills/reddit-automod-yaml/assets/library/`

That copy is authoritative when artifacts or attachments are empty. After restore, audit the workspace copies.

## Objective

REVIEW only. Audit the current AutoMod file. Write one report. Stop for human eval. Do not remediate. Do not bump a version. Do not paste the wiki. Do not toggle Safety Filters. Do not restore deleted predecessor versions.

## Library. Audit the current file.

1. `/home/workdir/artifacts/r-amex-automod-0.1.3.5.yaml`

Also restored, not a YAML audit:

- `/home/workdir/artifacts/r-amex-automod-0.1.3.5-public-copy.md`
- `/home/workdir/artifacts/r-amex-unpublished-tokens.txt`

Operator state is `/home/workdir/artifacts/amex-ops-state.yaml`. It is not restored from the skill library.

Predecessor files `0.1.3.yml`, `0.1.3.2.yaml`, `0.1.3.3.yaml`, and `0.1.3.4.yaml` were removed from this host library. Do not reconstruct them. Current is 0.1.3.5.

If another AutoMod YAML appears under `/home/workdir` this run, add it to the library list. Do not invent missing versions. After a successful restore, do not treat the pre-restore empty folder as a missing version.

## Required method

1. Recover AAI custody. Request class is REVIEW. Human gate is eval of the report.
2. Run the first command. Confirm the restored files exist.
3. Fetch official AutoMod pages this run through `exa-firecrawl` using `python3 /home/workdir/.grok/skills/reddit-automod-yaml/scripts/fetch_canon.py /home/workdir/artifacts/automod-canon-receipt.json`. Locators are in that skill's `references/source-canon.md`. Locators are not holdings.
4. If a scrape is navigation chrome, retry Exa on that URL. Mark the syntax claim UNRESOLVED if the body is still missing. Do not fill gaps from memory.
5. Run `python3 /home/workdir/.grok/skills/reddit-automod-yaml/scripts/audit_automod.py /home/workdir/artifacts/r-amex-automod-0.1.3.5.yaml /home/workdir/artifacts/r-amex-unpublished-tokens.txt`.
6. Map each high or medium finding to a fetched source with `claim-source-auditor` statuses: verified, conflicting, not-found, manual-review.
7. Report findings on the current file only. Do not rebuild a version-comparison table from deleted predecessors.
8. Write one report to `/home/workdir/artifacts/r-amex-automod-library-audit.md` using `/home/workdir/.grok/skills/reddit-automod-yaml/assets/audit-report.template.md`.
9. Stop. Surface the report path and wait. Do not propose a 0.1.3.6 file unless the next human message authorizes remediation.

## Fail rules

- Missing artifacts after `restore_library.py` fails only if `assets/library` itself is missing.
- "Do not use external tools" is invalid on this task. Exa and Firecrawl stay required for official pages.
- Do not emit BLOCKED for an empty new-session artifacts folder.

## Hard constraints

- Search checks are case-insensitive unless the fetched docs say otherwise. Do not add `(?i)`.
- No unpublished floor in public `comment:` lines. 250 stays in author checks and action_reason only.
- `combined_subreddit_karma` is not a sitewide post or comment gate. 1e is monthly-thread referral-URL comments only.
- Crowd Control and Reputation are not AutoMod. Record them as dual-engine, inspect-only.
- Title match in 0.1.3.3+ is `monthly.{0,80}referral.{0,30}thread`.
- Do not claim live wiki bytes unless independently fetched this run. This host has blocked Reddit wiki reads before.
- Do not print Exa or Firecrawl keys.
- No em dashes.

## Done means

- Library restored this run.
- Every library YAML has an audit result from this run.
- Official pages were fetched this run.
- The comparison report exists on disk.
- The turn ends at the human-eval gate with no remediating YAML.
