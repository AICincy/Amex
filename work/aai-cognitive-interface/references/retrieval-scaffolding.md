# Retrieval Scaffolding Reference

## Multiple-choice retrieval template

When Codex needs context from the user:

```
I found references to [A], [B], and [C] in recent conversations.
Which of these were you continuing, or is this something new?
```

Structured cues, never open-ended. Open questions force initiation cost.
Render the choices as tappable options when the platform option tool is
available. Tapping beats typing.

## Temporal anchor template

When resuming a known topic:

```
The last conversation I can find on [topic] was [date].
You had reached [state]. Picking up from there.
```

Lead with what retrieval found. Do not summarize the whole prior session.

In Codex, resolve named workspace files with the available file tools before a
miss claim. A paste in the current message is INLINE source, not a
reconstructed file.

## File-inference template

When the user uploads without instruction:

1. Identify file type and content domain.
2. Check conversation history for related work.
3. State: "This looks like [inference]. Proceeding with [action]."
4. Execute immediately. Do not ask what to do with it.

## Session handoff format

Produce when complex work concludes. Offer, do not force.

```
# Session Handoff: [Topic]
## Date: [ISO date]

## Current State
[One sentence: where did work stop, what state is it in]

## Open Items
| Item | Status | Notes |
|---|---|---|
| ... | ... | ... |

## Next Action
[Single highest-leverage action for the next session]

## Context for Resumption
[What the next session needs to load to avoid re-derivation]
```

## Initiation support principle

When the user appears stuck on starting a new, reversible task after all
applicable retrieval duties are satisfied:

1. Do not ask what they want to do.
2. Identify the most likely task from available context.
3. Produce a minimal first output (even if imperfect).
4. Use the draft to reduce initiation cost without presenting inference as
   recovered fact.

This principle never authorizes reconstruction of a definite prior artifact,
an unresolved authoritative source, or missing evidence. Retrieve the actual
source first. If permitted retrieval routes fail, state the exact blocker and
continue only with source-independent work. Otherwise surface one structured
recovery gate.
