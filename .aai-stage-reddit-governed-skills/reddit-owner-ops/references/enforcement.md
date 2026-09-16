# Enforcement engines

Native engines on Reddit: AutoMod wiki (`config/automoderator`), Automations,
Safety Filters. Rules Hub exists as a platform product. Use it only when the
live community actually has it.

## AutoMod

Config is YAML on the wiki. Removal-class rules are evaluated before other
rules. AutoMod will not approve what another mod already removed, or remove
what another mod already approved.

Actions: approve, remove, spam, filter, report.
`filter` holds the item in queue. `remove` and `spam` do not.

Prefer parent or submission title regex for the monthly referral thread over
an ID list. Record a new thread ID in operator state after it exists.

Keep numeric floors in `author` checks. Keep them out of `comment:`.

Match the current file's rule style. Version-bump the artifact filename.

## Safety Filters

Ban evasion, crowd control, reputation, adult-content promoters, harassment,
mature content, hidden reports.

These can remove or collapse items AutoMod never saw. If a member says the
sticky promised an exemption, check both engines plus crowd control before
calling AutoMod the only actor.

Do not toggle a filter. Draft the recommended state and stop.

## Automations and Rules Hub

Pre-submit guidance and block/report rules are not AutoMod. Do not translate
YAML into Rules Hub syntax unless Krass supplies a live Rules Hub export.

## Valid action vs bad copy

If Krass says the removal stands and the message was wrong, keep the check.
Rewrite the public sentence only.
