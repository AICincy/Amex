# Composition plan

Mediation-layer object. Not an agent.

Schema: `family/schemas/composition-plan.schema.json`
Writer: `family/scripts/write_composition_plan.py <plan.json> --output <authorized-path>`
Instance: an authorized external task artifact

Write a plan at the start of a multi-skill turn. First skill is always `aai-cognitive-interface`.

Use `compose-skills` unless the current Codex turn explicitly exposes and the
user authorizes a separate agent workflow.

Contract lives here and in AAI `references/composition-map.md`.
Do not copy the schema into every domain SKILL.md.
