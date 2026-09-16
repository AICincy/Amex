# YAML conventions

These rules come from official Automoderator documentation fetched during audit runs and from auditor failures on earlier library versions.

## Document shape

- No text before the first `---`.
- `---` sits on its own line with no leading spaces.
- Indent with spaces, not tabs.
- Do not use a YAML `|` block on a regex field.
- Prefer single-quoted regex. Double-quoted regex must double-escape.

## Search checks

Official search checks are case-insensitive unless the fetched docs say otherwise.

- Do not add `(?i)`.
- Do not add `(?-i)`.
- `(?i)` is a compile failure under `/u` and under Python `re`.

## Checks that stay in the file

- Do not treat a user-controlled title match as the identity of an official thread.
- Keep the automatic `combined_subreddit_karma` 1e gate disabled until a trusted official-thread identity is enforced.
- Numeric floors stay in author checks and `action_reason` only.

## CI guards

`.github/workflows/validate-automod.yml` rejects text before `---` and rejects `(?i)`.

`.github/workflows/guard-public-copy.yml` rejects unpublished floors and `combined_subreddit_karma` inside `comment:` or `sticky_comment:` fields.
