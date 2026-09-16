# Execution Trail Template

Default in Codex: append one JSONL line. See audit-log.md.

Use this long markdown format only when Krass asks for a full trail.

```markdown
# Execution Trail: [Task Summary]
## Date: [ISO date]
## Scope: [Single-step | Linear | Branching | Decision-gated]

## Steps Executed

### Step 1: [Action name]
- Tool(s): [tool names used]
- Input: [what was queried, read, or processed]
- Output: [summary of result, not full content]
- Decision: [continue | surface | wait]
- Reason: [why this decision was made]

### Step 2: [Action name]
- Tool(s): [tool names used]
- Input: [what was queried, read, or processed]
- Output: [summary of result]
- Decision: [continue | surface | wait]
- Reason: [why this decision was made]

[repeat for each step]

## Items Surfaced
[List of what the user saw in the final chat output]

## Items Suppressed
[Items found but not relevant enough to include in output]

## Parking Lot
[Side-findings that do not serve the primary objective
but may be useful later]

## Coverage Statement
[What was checked. What was not checked. What remains open.]
```

## Notes on trail generation

- The trail captures observable actions, results, and concise task rationale.
  It never records private chain-of-thought or hidden reasoning. Tool outputs
  can be thousands of tokens, so summarize only the task-relevant result.
- Each step's "Decision" field records whether Codex continued
  executing, surfaced output to the user, or waited for input.
- The "Reason" field records a concise operational rationale, referencing the
  continuation protocol's surface conditions when applicable. Do not expose
  private reasoning traces.
- The parking lot carries forward from the main response if one exists.
- The coverage statement is the integrity check: what was and was not
  verified.
