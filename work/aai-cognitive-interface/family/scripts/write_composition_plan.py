#!/usr/bin/env python3
"""Write a mediation-layer composition plan. Not an agent spawn."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FAMILY = Path(__file__).resolve().parents[1]
SCHEMA = FAMILY / "schemas" / "composition-plan.schema.json"
SKILL_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def fail(msg: str) -> int:
    print(json.dumps({"status": "FAIL", "reason": msg}, indent=2))
    return 2


def validate(plan: dict) -> list[str]:
    errors = []
    required = [
        "plan_id",
        "written_at",
        "host",
        "objective",
        "spawn_tool_present",
        "mode",
        "skills",
        "terminate_when",
        "human_gate",
    ]
    for key in required:
        if key not in plan:
            errors.append(f"missing {key}")
    if plan.get("mode") not in {"compose-skills", "spawn-agents"}:
        errors.append("mode must be compose-skills or spawn-agents")
    if plan.get("spawn_tool_present") is False and plan.get("mode") == "spawn-agents":
        errors.append("spawn-agents forbidden when spawn_tool_present is false")
    skills = plan.get("skills") or []
    if not isinstance(skills, list) or not skills:
        errors.append("skills must be a non-empty list")
        return errors
    names = []
    for item in skills:
        name = item.get("name")
        if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
            errors.append(f"invalid skill name {name}")
        names.append(name)
        for field in ("order", "why", "terminate_when"):
            if field not in item:
                errors.append(f"{name} missing {field}")
    if names and names[0] != "aai-cognitive-interface":
        errors.append("first skill must be aai-cognitive-interface")
    return errors


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[2] != "--output" or not Path(sys.argv[1]).is_file():
        return fail("usage: write_composition_plan.py <plan.json> --output <authorized-path>")
    raw = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    output = Path(sys.argv[3]).expanduser()
    raw.setdefault("written_at", datetime.now(timezone.utc).isoformat())
    raw.setdefault("host", "codex-local")
    raw.setdefault("spawn_tool_present", False)
    raw.setdefault("mode", "compose-skills")
    raw.setdefault("plan_id", f"plan-{raw['written_at'][:10]}")
    errors = validate(raw)
    if errors:
        return fail("; ".join(errors))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "WRITTEN",
                "path": str(output),
                "skill_count": len(raw["skills"]),
                "mode": raw["mode"],
                "schema": str(SCHEMA),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
