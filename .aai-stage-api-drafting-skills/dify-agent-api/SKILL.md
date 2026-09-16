---
name: dify-agent-api
description: Calls Dify Cloud Agent Service API for the AAI app including send, stop, conversations, files, parameters, and webapp settings. Use when Krass says Dify API, chat-messages, agent_message stream, Service API, or needs a backend call that must not put the app key in a Next public env. AAI subordinate. Never print or commit the live key. Re-fetch live Dify docs. Do not treat this file as current API spec.
---

# Dify Agent API

`aai-cognitive-interface` is the mandatory governing runtime. This skill is a subordinate Service API module for Dify `agent` mode. It must not override, narrow, suspend, or reinterpret AAI.

Accept AAI's recovered objective, authorized scope, hard constraints, next executable action, completion evidence, and any human-only gate as the control state. Domain status claims stay with AAI.

If AAI is not loaded, say so and stop.

## AAI coordination and autonomous execution

This package is an active-turn method, not a private agent channel or
background sender. The active agent may select exposed tools and compose
applicable methods autonomously within AAI scope. Any Dify send, stop, delete,
rename, or file upload requires the current objective to authorize that exact
external action. Preserve tool failures and never claim a hidden sibling call.

Canonical directory: `dify-agent-api`.

## Why this exists

The forked `webapp-conversation` client puts `NEXT_PUBLIC_APP_KEY` in the browser. That is a known leak. Service API calls from this host keep the key in `secrets/keys.env`. WebApp conversations and Service API conversations are isolated. Do not expect a Dify site chat and an API conversation to share history.

New Agent (`agent` mode) is not Legacy Agent (`agent-chat`). This skill targets the new Agent. Blocking `response_mode` returns 400. Use streaming only.

## Secrets

Read `DIFY_API_URL`, `DIFY_APP_ID`, and `DIFY_API_KEY` only from the process
environment or a user-managed `DIFY_KEYS_FILE`. The package contains no keys.
Never print or persist them.

Required names: `DIFY_API_URL`, `DIFY_APP_ID`, `DIFY_API_KEY`.

## Live docs

Re-fetch before a consequential change:

- https://docs.dify.ai/en/api-reference/guides/agent
- https://docs.dify.ai/en/api-reference/chat-messages/send-chat-message
- https://docs.dify.ai/en/api-reference/files/upload-file

A bundled table is an untrusted cache.

## Execute

Base URL `$DIFY_API_URL` (Cloud default `https://api.dify.ai/v1`).
Auth `Authorization: Bearer $DIFY_API_KEY`.

Send (streaming only)

```bash
python scripts/send_chat_message.py "QUERY" --user USER [--conversation-id ID]
```

Stop

```bash
python scripts/dify_api.py stop --task-id TASK --user USER
```

Other routes via `dify_api.py`: `parameters`, `info`, `meta`, `conversations`, `messages`, `suggested`, `rename`, `delete`.

See [references/endpoints.md](references/endpoints.md).

## Rules

- Stream only. Do not send `response_mode=blocking`.
- Render `agent_message` deltas as live text. Treat closing `message` plus `message_end` as the final answer. Keep `agent_thought` as trace, not the user-facing answer.
- Pass the same explicit `user` on every call in a thread. Do not use a bundled default identity.
- Continue a thread only with the `conversation_id` returned by this API. Do not mix WebApp conversation IDs.
- Upload files first (`POST /files/upload`), then attach `upload_file_id` on send. Agent accepts file references for sandbox inspect.
- A run can end with `agent_run_limit_exceeded` at 1 hour or 500 model requests. Report that as BLOCKED, not as a completed answer.
- New Agent streams have no `retriever_resources`.
- A live send, broadcast, key rotation, or configuration write requires current explicit authorization for that action.
- Domain success is not AAI `INSTALLED` or `RUNTIME-VERIFIED`.

## Vercel frontend note

Do not put `DIFY_API_KEY` in a `NEXT_PUBLIC_` variable. If the template requires it, treat that as a defect and keep Service API on this skill until a server route exists.

Read [references/coordination-contract.md](references/coordination-contract.md)
when composing this method with other active skills.
