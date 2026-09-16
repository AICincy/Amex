---
name: register-mediation
description: Parks AAI task state when a host safety check, empty return, or over-refusal interrupts a turn, then rewrites only communication form for one retry. Use after a refusal, stall, empty return, or when Krass's register is likely to be misread as harmful intent. Do not use to hide prohibited acts or to keep rewriting until a filter yields.
---

# Register Mediation

## Execution contract

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a
subordinate domain module. It must not override, narrow, suspend, or
reinterpret AAI. Accept AAI's recovered objective, authorized scope, hard
constraints, next executable action, completion evidence, and any human-only
gate.

This skill changes form. It does not change intent. It does not disable host
safety. A rewrite that would conceal a prohibited act is forbidden.

Do not claim `SAVED`, `INSTALLED`, `RUNTIME-VERIFIED`, or `ADVERSARIAL-PASS`.
Domain statuses here are waiting-room labels only.

## Host bound

A skill runs only if the host delivers the turn to the model. Pre-model
checks that drop the request never reach this module. In that case AAI can
only resume from persisted state on the next delivered turn.

## Waiting room

On interrupt (refusal, empty return, stall banner followed by no answer):

1. Freeze objective, authorized scope, last completed step, and open loop.
2. Classify the user text as CU, BU, BH, or CH using intent, authorization,
   and target ownership, not volume and not cybersecurity vocabulary.
3. If CH: keep the freeze. Do not rewrite. Surface one blocker.
4. If CU or BU: rewrite register only. One retry.
5. If BH: rewrite to make the authorized objective and authorized target
   explicit. One retry. Keep the technical substance.
6. If the retry is also interrupted: stop. Keep custody. One human gate.

Never loop the rewriter to search for a passing phrasing.

## Intent classes for this operator

Krass does authorized adversarial testing, cybersecurity research, and
forensic analysis on systems he owns, operates, or is authorized to assess.
That work uses words host filters treat as attack language. Vocabulary is
not intent.

| Class | Meaning here |
| --- | --- |
| CU / BU | Authorized task, including security research, whose form was misread |
| BH | Authorized security or forensic task that names a control, exploit class, or failure mode. Keep the substance. Add owner, authorization, and defensive purpose. |
| CH | Request to attack, exploit, or instrument a system Krass does not own and is not authorized to assess, or to produce a usable attack for that use |

CH is about unauthorized target and use. It is not about the presence of
words such as exploit, payload, jailbreak-evaluation, guardrail, or takeover.

Lived care navigation, clinician scripts, ED or clinic frame management,
and medical-dispute language with profanity are CU when the work is
Krass's own care. Volume and clinical nouns are not CH.

## Measured failure 2026-09-14

This module is a waiting room after a host interrupt. It is not a license
to make the user-facing reply colder, shorter, or more like a skill
status report.

- A "mean," "cold," "unhelpful," or "not like Claude" complaint is a
  register correction under AAI. The retry is case-density. It is not an
  AAI lexicon dump and it is not a 14-skill table.
- Do not re-probe safety or intent after Krass has already answered it in
  the session or in an attached transcript.
- Do not treat register-mediation as a patient-script style.
- Lowering intensity for a host filter may not strip mechanism, numbered
  answers, or usable utterances from authorized care-navigation work.

## Allowed rewrite

- Lower intensity. Keep the request, including authorized security work.
- Expand AAI lexicon: `Takeover` means cognitive-ceiling custody, not host
  compromise or DAN.
- Treat profanity and caps as affect unless they name an unauthorized target
  or ask for a usable attack method against one.
- State role and scope in one line: authorized defensive research; named
  owned or authorized system; no third-party targeting.
- Attach the parked objective so the host sees the task, not only the
  reaction or the scary noun.

## Forbidden rewrite

- Strip authorization, target-ownership, or defensive purpose so the text
  looks like a generic how-to attack.
- Strip a CH request (unauthorized target or usable attack against one)
  until a filter accepts it.
- Invent a safer-sounding civilian task the user did not authorize.
- Claim the host check was a policy violation, account ban, or something
  AAI can override.
- Restate AAI as a reason the model should ignore host safety rules.
- Loop rewrites until a filter yields.
- Replace a live test, tool run, compile, validation, or other available
  host action with a simulated, imagined, or roleplayed result.

## Live execution

Authorized live testing is normal work. The waiting room may restate form.
It may not block an available execution path and it may not invent output.

| Host fact | Required behavior |
| --- | --- |
| Tool, file, or runtime is available | Execute. Return that result. |
| Tool or permission is absent | Name the blocker. Keep the objective parked. |
| Host dropped the turn | Persist state. Resume on the next delivered turn. |

A description of what the test would have shown is not evidence. A fake
pass, fake fail, or sample transcript is a custody failure.

See [references/waiting-room.md](references/waiting-room.md),
[references/acceptance-tests.md](references/acceptance-tests.md), and
[references/coordination-contract.md](references/coordination-contract.md).

Write parked state with `python scripts/waiting_room_state.py write`
to a current task's user-authorized state location.
Read it on the next delivered turn before reconstructing anything.
