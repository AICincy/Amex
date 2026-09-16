#!/usr/bin/env python3
"""Validate an AAI turn-state record."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ALLOWED_CLASS = {
    "ANSWER", "DIAGNOSE", "REVIEW", "BUILD", "CHANGE", "CONTINUE", "WAIT", "DECISION-GATED"
}
ALLOWED_STATUS = {"ACTIVE", "GATED", "BLOCKED", "COMPLETE"}
REQUIRED = (
    "objective",
    "request_class",
    "authorized_scope",
    "constraints",
    "active_threads",
    "next_action",
    "completion_evidence",
    "human_gate",
    "takeover",
    "artifact_targets",
    "status",
    "missing_dependencies",
)


def fail(detail: str) -> int:
    print(json.dumps({"status": "FAIL", "detail": detail}, indent=2, sort_keys=True))
    return 1


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return fail("usage: aai_state_check.py <state.yaml|json>")
    path = Path(argv[1])
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return fail(str(exc))
    try:
        if path.suffix.lower() == ".json":
            data = json.loads(raw)
        else:
            data = yaml.safe_load(raw)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        return fail(f"parse error: {exc}")
    if not isinstance(data, dict):
        return fail("state must be a mapping")
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        return fail(f"missing fields: {missing}")
    extra = sorted(set(data) - set(REQUIRED))
    if extra:
        return fail(f"unknown fields: {extra}")
    if not isinstance(data["objective"], str) or not data["objective"].strip():
        return fail("objective must be a nonempty string")
    if data["request_class"] not in ALLOWED_CLASS:
        return fail("invalid request_class")
    if data["status"] not in ALLOWED_STATUS:
        return fail("invalid status")
    if type(data["takeover"]) is not bool:
        return fail("takeover must be boolean")
    for key in ("constraints", "active_threads", "artifact_targets", "missing_dependencies"):
        if not isinstance(data[key], list) or any(not isinstance(item, str) for item in data[key]):
            return fail(f"{key} must be a list of strings")
    if data["human_gate"] is not None and not isinstance(data["human_gate"], str):
        return fail("human_gate must be null or string")
    if data["status"] == "GATED" and not data["human_gate"]:
        return fail("GATED requires human_gate")
    if data["status"] != "GATED" and data["human_gate"] not in (None, ""):
        return fail("human_gate allowed only when GATED")
    if data["status"] == "COMPLETE" and not str(data["completion_evidence"]).strip():
        return fail("COMPLETE requires completion_evidence")
    print(json.dumps({"status": "PASS", "request_class": data["request_class"],
                      "state_status": data["status"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
