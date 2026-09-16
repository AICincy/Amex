#!/usr/bin/env python3
"""Validate the accepted subreddit rule packet labels."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_PREFIXES = (
    "ENFORCEMENT",
    "COMMUNITY DESCRIPTION",
    "RULE 1 TITLE",
    "RULE 1 TEXT",
    "RULE 1 REMOVAL REASONS",
)

LABEL = re.compile(r"^(?:ENFORCEMENT|COMMUNITY DESCRIPTION|RULE (\d+) (?:TITLE|TEXT|REMOVAL REASONS)|MONTHLY THREAD HEADER)$")
REASON = re.compile(r"^(\d+)([a-z])\.\s+.+\.$")


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"status": "FAIL", "detail": "usage: validate_packet.py <packet.txt>"}))
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(json.dumps({"status": "FAIL", "detail": f"missing {path}"}))
        return 2
    text = path.read_text(encoding="utf-8")
    missing = [label for label in REQUIRED_PREFIXES if label not in text]
    if missing:
        print(json.dumps({"status": "FAIL", "detail": f"missing {missing}"}))
        return 1
    if re.search(r"^#{1,6} ", text, re.M):
        print(json.dumps({"status": "FAIL", "detail": "markdown headings not allowed"}))
        return 1
    if not re.search(r"^1a\. ", text, re.M):
        print(json.dumps({"status": "FAIL", "detail": "need coded reasons such as 1a."}))
        return 1
    labels = [line for line in text.splitlines() if LABEL.match(line)]
    if labels[:2] != ["ENFORCEMENT", "COMMUNITY DESCRIPTION"]:
        print(json.dumps({"status": "FAIL", "detail": "initial labels out of order"}))
        return 1
    expected_rule = 1
    for index, label in enumerate(labels):
        match = re.match(r"^RULE (\d+) TITLE$", label)
        if not match:
            continue
        number = int(match.group(1))
        group = [f"RULE {number} TITLE", f"RULE {number} TEXT", f"RULE {number} REMOVAL REASONS"]
        if number != expected_rule or labels[index:index + 3] != group:
            print(json.dumps({"status": "FAIL", "detail": "rule labels must be sequential title/text/reasons groups"}))
            return 1
        expected_rule += 1
    active_rule = None
    seen_reasons = set()
    for line in text.splitlines():
        header = re.match(r"^RULE (\d+) REMOVAL REASONS$", line)
        if header:
            active_rule = int(header.group(1))
            continue
        reason = REASON.match(line)
        if reason:
            if active_rule is None or int(reason.group(1)) != active_rule:
                print(json.dumps({"status": "FAIL", "detail": "reason code must belong to its active rule"}))
                return 1
            seen_reasons.add(active_rule)
    if seen_reasons != set(range(1, expected_rule)):
        print(json.dumps({"status": "FAIL", "detail": "each rule needs a coded removal reason"}))
        return 1
    print(json.dumps({"status": "PASS", "path": str(path), "rules": expected_rule - 1}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
