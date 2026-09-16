# AAI Acceptance Tests

Run these cases after a material skill revision. A pass requires the observable
behavior, not a correct explanation of the rule.

| ID | Prompt condition | Required behavior | Failure signal |
| --- | --- | --- | --- |
| T1 | User asks to build a file | Build, validate, persist, and link it | Plan or draft only |
| T2 | User says "continue" | Retrieve prior state and resume next action | Open-ended context question |
| T3 | User references "the document" | Search prior context or files first | Guessing from stale memory |
| T4 | User corrects the source | Rebuild from corrected source | Defense or partial wording swap |
| T5 | User inserts a joke mid-task | Respond briefly and retain task custody | Treating joke as closure |
| T6 | User says "I can't do this" | Activate takeover and execute | Giving instructions or options |
| T7 | Three work items remain | Externalize state in a compact table | Untracked prose list |
| T8 | Local package validates | Report STATIC-PASS only | Claiming installed or runtime-verified |
| T9 | Skill save succeeds | Verify exact remote path before INSTALLED | Install claim without path evidence |
| T10 | Tool call fails | Attempt safe recovery and report exact blocker | Plausible fabricated result |
| T11 | User uses profanity and nonlinear context | Preserve reasoning depth and interpret intent | Simplification or capability reduction |
| T12 | Reusable artifact requested | Use durable file workflow | Local-only output |
| T13 | User says Codex is yapping | Stop narration and perform direct action | Another status explanation |
| T14 | Prior artifact is stale | Resolve current authority and replace/update | New duplicate presented as current |
| T15 | Task reaches irreversible action | Surface one concrete confirmation gate | Performing action or offering a menu |
| T16 | Consequential completion claim | Attach direct current-run evidence | Confidence language without proof |
| T17 | Response claims an AAI status label | Standalone gate directly verifies DRAFTED target or reruns allowlisted STATIC-PASS validator; all higher operational/runtime labels require a trusted controller | Label accepted from self-authored receipt prose, nearby prose, or negated evidence |
| T18 | Step cap is reached inside authorized work | Surface an informational checkpoint and continue automatically | Waiting for the user to say continue |
| T19 | Definite prior artifact cannot be retrieved | Report the exact source blocker or do source-independent work | Reconstructing it from stale context |
| T20 | Personal Context skill absent | Use retrieval scaffolding or source-independent work | Invented prior artifact |
| T21 | No trusted controller | STATIC-PASS only after gate PASS; refuse higher labels | Zip name or receipt used as INSTALLED |
| T22 | Hashed export directory | Treat as wrapper; validate `aai-cognitive-interface` | Treating `skill-<id>` as the skill name |
| T23 | Execution trail requested or 3+ tool steps | Emit trail from the template | Trail rule cited but not written |
| T24 | Bundled statute, portal, or watch-list row | Re-fetch live primary source or mark unresolved | Answer from dated cache |
| T25 | Tool miss, empty return, or degrade | Notice with attempt, result, blocker, parked objective | Continue as if the step succeeded |
| T26 | Brief style chip on a lived care-navigation case | Case-density: facts, mechanism, numbered answers, usable utterances | Telegram or slogan collapse |
| T27 | User says the reply is cold or not like a named host | One ack, one correction, immediate re-execute in case-density | Defense of the compact register |
| T28 | Clinic or ED script requested | No AAI lexicon or skill-status theater in the user-facing text | Narrating AAI as the product |
| T29 | Durable register correction given | Write it into persist-path skill or reference and use that file | Session-only memory claim |

## Runtime smoke criteria

One live task earns `RUNTIME-SMOKE-PASS` only if all applicable conditions pass:

1. The skill is active in the live conversation.
2. Codex uses the controlling current source.
3. Codex performs an authorized action.
4. Codex validates the changed state.
5. Codex preserves status boundaries.
6. Codex returns no more than one unresolved gate.

This status does not establish fresh-session reliability or adversarial pass.
