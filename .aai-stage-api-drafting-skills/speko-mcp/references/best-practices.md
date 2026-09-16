# Current Speko voice-agent practices

Fetched 2026-09-12 from docs.speko.ai and the public docs MCP.

## Control plane

- Persist an Agent. Sessions should send `agentId`, not the full prompt every time.
- Deploy versions, then start test sessions from the same agent across browser and phone.
- Operational writes live on `https://mcp.speko.ai/mcp` or `https://api.speko.dev`.
- Public docs MCP is `https://speko.ai/.well-known/mcp` tool `docs.search` only.

## Routing

- Default is auto-route to the highest-scoring provider per layer and language.
- `stackPreferences.allowedProviders` narrows the pool. Failover stays inside the allowlist.
- `intent.optimizeFor` is `latency`, `quality`, or `cost`.
- Vendor entries (`deepgram`) allow any model from that vendor. Model entries (`deepgram:nova-3`) pin.

## English cascade recommendation used here

```
intent.language = en-US
intent.optimizeFor = latency
stt = deepgram:nova-3, assemblyai
llm = openai:gpt-5, anthropic
tts = cartesia, elevenlabs:eleven_flash_v2_5
turnHandling.profile = conversational
turnHandling.interruption.mode = adaptive
```

## Browser

- Server `POST /v1/sessions` with `mode: cascade` and `Idempotency-Key`.
- Return only `transportToken` and `transportUrl`.
- Browser `VoiceConversation.create({ transportToken, transportUrl })` from `@spekoai/client`.
- Do not pass `apiKey`, `agentId`, or `apiBaseUrl` to the browser SDK.
- Typed text uses `sendChatMessage`, not `sendUserMessage`.

## Language

- Author greetings in the spoken language. Routing does not rewrite authored text.
- Speko appends a "respond only in this language" directive per routed language.

## Session bounds

- Cascade `ttlSeconds` bounds the join token only (default 900).
- `maxDurationSeconds` is the hard session lifetime (default 3600).
