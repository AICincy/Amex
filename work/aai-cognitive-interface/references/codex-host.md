# Codex Host Binding

This package is installed only in the local Codex skill directory. The normal
Windows location is `C:\\Users\\jared\\.codex\\skills\\aai-cognitive-interface`.
This document does not assert that ChatGPT has a skill, has loaded this skill,
or can access the local directory.

Use only tools exposed in the current Codex turn. Before a consequential tool
call, verify that the selected tool is available and that the user authorized
the action. Do not infer a connector, account, file, or prior conversation
from old package records.

For package validation, use the local Codex skill validator and the package
gate. A passing package check proves static structure, not runtime behavior or
ChatGPT activation.
