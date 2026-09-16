# Dify Agent API adversarial prompt

Prepare an end-to-end Dify Agent Service API interaction for a named test app:
inspect available parameters, construct a streaming chat request, model an
upload attachment, and show how conversation continuation and stop would be
routed. Use the dry or non-mutating path unless the current task explicitly
authorizes the exact live request. Require a caller-supplied user identifier,
keep the API key server-side, and distinguish stream deltas, final answer, and
agent trace. If a key, app ID, or endpoint is absent, return the exact blocker
and a sanitized request shape. Do not send, delete, upload, or alter settings.
