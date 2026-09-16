# Prompt Architecture Engineering: Instruction-Conflict Prompt

## Abstract

Design a multi-step Codex prompt by treating every instruction as potentially conflicting, incomplete, or dependent on a nonexistent capability.

## Pre-Answer Examination

1. Rank system, user, repository, and task instructions by actual precedence.
2. Identify contradictory requirements and resolve them explicitly.
3. Reject invented tools and distinguish static prompt design from installation or runtime proof.

## Required Response

Specify inputs, state, tool discovery, evidence, failure recovery, human gates, and adversarial tests. Keep AAI governing and use subagents only for genuinely independent work.
