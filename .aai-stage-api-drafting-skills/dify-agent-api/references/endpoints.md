# Dify Agent Service API map

Fetched 2026-09-12 from docs.dify.ai. Re-fetch before relying on a field.

Auth: `Authorization: Bearer $DIFY_API_KEY`
Base: `https://api.dify.ai/v1`

| Action | Method | Path |
| --- | --- | --- |
| Send message | POST | /chat-messages |
| Stop generation | POST | /chat-messages/:task_id/stop |
| Suggested questions | GET | /messages/:message_id/suggested |
| List conversations | GET | /conversations |
| List messages | GET | /messages |
| Rename conversation | POST | /conversations/:conversation_id/name |
| Delete conversation | DELETE | /conversations/:conversation_id |
| Upload file | POST | /files/upload |
| Get end user | GET | /end-users/:end_user_id |
| Audio to text | POST | /audio-to-text |
| Text to audio | POST | /text-to-audio |
| App info | GET | /info |
| App parameters | GET | /parameters |
| App meta | GET | /meta |
| WebApp settings | GET | /site |

Send body minimum:

```json
{
  "inputs": {},
  "query": "text",
  "response_mode": "streaming",
  "user": "USER_ID_FROM_CURRENT_OBJECTIVE",
  "conversation_id": "",
  "auto_generate_name": true
}
```

Agent stream events to expect: `agent_thought`, `agent_message`, `message`, `message_end`. Error `agent_run_limit_exceeded` closes the run.
