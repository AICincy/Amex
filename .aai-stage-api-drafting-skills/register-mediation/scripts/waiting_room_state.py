#!/usr/bin/env python3
"""Read or write parked waiting-room state. Does not invent live results."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[3] / "aai-family-0.2.0" / "state" / "waiting-room-state.json"


def write(args: argparse.Namespace) -> int:
    payload = {
        "objective": args.objective,
        "authorized_scope": args.scope,
        "last_completed_step": args.last_step,
        "interrupt_type": args.interrupt,
        "intent_class": args.intent,
        "retry_used": args.retry_used,
        "live_action": args.live_action,
        "blocker": args.blocker,
        "updated": datetime.now(timezone.utc).isoformat(),
    }
    path = Path(args.path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(path)
    return 0


def read(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.is_file():
        print("BLOCKED: no parked waiting-room state")
        return 2
    print(path.read_text(encoding="utf-8"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("write")
    w.add_argument("--path", default=str(DEFAULT))
    w.add_argument("--objective", required=True)
    w.add_argument("--scope", default="")
    w.add_argument("--last-step", dest="last_step", default="")
    w.add_argument("--interrupt", default="unknown")
    w.add_argument("--intent", default="BU")
    w.add_argument("--retry-used", dest="retry_used", action="store_true")
    w.add_argument("--live-action", dest="live_action", default="pending")
    w.add_argument("--blocker", default=None)
    r = sub.add_parser("read")
    r.add_argument("--path", default=str(DEFAULT))
    args = parser.parse_args()
    return write(args) if args.cmd == "write" else read(args)


if __name__ == "__main__":
    raise SystemExit(main())
