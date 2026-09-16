#!/usr/bin/env python3
"""Append one compact audit event. No tool dumps. No reasoning traces."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "state" / "audit.jsonl"
ALLOWED_ACT = {"load", "tool", "gate", "status", "adapt", "park", "block", "draft"}
ALLOWED_RESULT = {"PASS", "FAIL", "OK", "BLOCKED", "REFUSED", "WAIT"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skill", required=True)
    p.add_argument("--act", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--note", default="")
    args = p.parse_args()
    if args.act not in ALLOWED_ACT:
        raise SystemExit(f"bad act: {args.act}")
    if args.result not in ALLOWED_RESULT:
        raise SystemExit(f"bad result: {args.result}")
    note = args.note.strip().replace("\n", " ")[:120]
    event = {
        "t": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skill": args.skill,
        "act": args.act,
        "target": args.target[:160],
        "result": args.result,
        "note": note,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, separators=(",", ":")) + "\n")
    print(json.dumps(event, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
