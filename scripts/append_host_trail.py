#!/usr/bin/env python3
"""Append one host-trail row. Never write secrets."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", default="audits/host-trail/CURRENT.md")
    p.add_argument("--skill", default="-")
    p.add_argument("--tool", required=True)
    p.add_argument("--target", default="-")
    p.add_argument("--result", required=True)
    p.add_argument("--note", default="")
    args = p.parse_args()
    path = Path(args.file)
    path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"| {ts} | {args.skill} | {args.tool} | {args.target} | {args.result} |"
    if args.note:
        line += f" {args.note}"
    if not path.exists():
        path.write_text(
            "# Host trail\n\n| Time (UTC) | Skill | Tool / route | Target | Result |\n| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
        )
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + line + "\n", encoding="utf-8")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
