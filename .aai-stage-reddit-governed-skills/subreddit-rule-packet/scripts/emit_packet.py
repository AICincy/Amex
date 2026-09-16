#!/usr/bin/env python3
"""Emit the accepted subreddit rule packet format."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def emit_txt(data: dict) -> str:
    lines = [
        "ENFORCEMENT",
        str(data["enforcement"]).strip(),
        "",
        "COMMUNITY DESCRIPTION",
        str(data["community_description"]).strip(),
        "",
    ]
    for i, rule in enumerate(data["rules"], start=1):
        lines += [
            f"RULE {i} TITLE",
            str(rule["short_name"]).strip(),
            "",
            f"RULE {i} TEXT",
            str(rule["description"]).strip(),
            "",
            f"RULE {i} REMOVAL REASONS",
        ]
        reasons = rule.get("violation_reasons") or []
        if not reasons and rule.get("violation_reason"):
            reasons = [{"code": f"{i}a", "text": rule["violation_reason"]}]
        for reason in reasons:
            code = str(reason["code"]).strip()
            text = str(reason["text"]).strip().rstrip(".")
            lines.append(f"{code}. {text}.")
        lines.append("")
    header = data.get("monthly_thread_header")
    if header:
        lines += ["MONTHLY THREAD HEADER", str(header).strip(), ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("json_path")
    p.add_argument("txt_path")
    args = p.parse_args()
    data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    Path(args.txt_path).write_text(emit_txt(data), encoding="utf-8")
    print(args.txt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
