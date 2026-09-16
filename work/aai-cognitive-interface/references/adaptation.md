# Adaptation Contract

Codex applies AAI through current-turn instructions and authorized control artifacts. It does not learn by memory or export-learning.

## Allowed adaptation sources

1. Krass's latest explicit correction or decision this session.
2. Authorized matter file or other current source artifact.
3. Live tool results from this run.
4. Persisted Codex skill files under the local Codex skill root.
5. Waiting-room and host-activation state files.
6. Workspace attachments and files from this conversation.

## Forbidden adaptation sources

- ChatGPT / Codex memory
- "I remember from the export"
- Bundled dated tables used as current fact
- Reconstructed prior chats when no file or tool returned them
- Silent weight-level claims that a rule was learned

## Write-back rule

When Krass corrects a durable control rule, write the correction into the governing skill, a reference file, or authorized state. Then use that file on later turns.

When the correction is matter fact, write it only into an authorized matter file. Skills stay runtimes.

## Session rule

A later Codex session can rely on a change only when it is in a persisted file or current visible context. If the file is absent, the fact is unresolved. Say so.

## One-loop rule

Do not ask Krass to re-teach a correction already written to a persist-path file. Reload the file.
