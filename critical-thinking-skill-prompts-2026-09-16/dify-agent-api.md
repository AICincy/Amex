# Dify Agent API: Execution-Boundary Prompt

## Abstract

Construct a Dify interaction only after testing whether the request could accidentally send, upload, delete, or expose a credential.

## Pre-Answer Examination

1. Enumerate all state-changing routes implicated by the proposed interaction.
2. Verify caller-supplied user identity, app identity, and endpoint availability.
3. Compare dry-run output with the proposed live request shape and identify omitted authorization.

## Required Response

Return a sanitized request model, stream-event interpretation, and exact blocker or execution gate. Use dry run unless the exact live request is currently authorized.
