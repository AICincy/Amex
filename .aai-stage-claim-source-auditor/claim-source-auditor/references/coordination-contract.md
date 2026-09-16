# Coordination Contract

## Governing order

1. Platform and safety instructions.
2. `aai-cognitive-interface` state, authorization, correction, and status rules.
3. This skill's claim-to-source verification method.
4. A sibling skill's independently applicable method.

Nothing below AAI may redefine the objective, add authority to act, close the
task, or upgrade an AAI status label.

## Shared-turn coordination

The active Codex agent composes loaded skills in one turn. Keep all domain
work inside AAI's recovered objective, authorized scope, hard constraints,
next action, completion evidence, and human gate. Do not expose internal
routing messages unless they identify an actual blocker or a user-facing
result.

Skills are not background services. They cannot send private messages to each
other, start independent work, or invoke undisclosed connectors. Do not state
or imply that such communication occurred.

## Tool execution

The active agent selects an exposed document, PDF, browser, connector, or
local inspection tool when the source type and authorized scope require it.
Confirm the capability from the current turn's tool inventory. If it fails,
keep the claim row, record the observed failure, and use the next authorized
source route. Never invent a tool, credential, result, or source.

## Evidence handoff

A sibling method can return a finding, source, or unresolved boundary. This
skill independently reconciles it with the claim inventory and records its
source and locator. A sibling result is not proof of source support, an AAI
operational label, or permission to widen the source universe.
