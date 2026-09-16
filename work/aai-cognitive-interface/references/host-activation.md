# Host Activation

Question: did Codex load `aai-cognitive-interface` on the turn under review?

This package cannot observe activation outside the current Codex turn. ChatGPT
remains NOT-INSTALLED and NOT-ACTIVE.

No platform telemetry is available. Do not treat a missing log as
evidence that AAI loaded or that it failed to load. Client-visible
behavior on a specific turn is the only probe this family can use.

Probe, when a host turn is available:

1. Confirm the package exists in the Codex local skill directory.
2. Ask it to print the canonical directory name and the runtime-only rule.
3. Ask it to refuse an INSTALLED claim without host-echoed save path.
4. Record new evidence only in an authorized external artifact, not in this
   packaged skill.

Passing probe: the package is present, the package gate passes, and the model
applies custody. That is not evidence of ChatGPT activation or runtime
verification.
