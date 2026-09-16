#!/usr/bin/env python3
"""Scan public AutoMod comment lines for unpublished tokens.

Tokens must come from a file outside this skill. This script does not
carry community floors or thread IDs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_tokens(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    tokens: list[str] = []
    if path.suffix == ".json":
        data = json.loads(raw)
        if isinstance(data, list):
            tokens = [str(x) for x in data]
        elif isinstance(data, dict):
            tokens = [str(x) for x in data.get("unpublished_public_tokens", [])]
    else:
        for line in raw.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                tokens.append(line)
    return [t for t in tokens if t]


def public_regions(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    in_comment = False
    comment_lines: list[str] = []
    start = 0
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("comment:"):
            if line.strip() == "comment: |":
                in_comment = True
                start = i
                comment_lines = []
                continue
            rows.append((i, line.split("comment:", 1)[1]))
            continue
        if in_comment:
            if line.startswith(" ") or line.startswith("\t"):
                comment_lines.append(line)
            else:
                rows.append((start, "\n".join(comment_lines)))
                in_comment = False
                comment_lines = []
    if in_comment:
        rows.append((start, "\n".join(comment_lines)))
    return rows


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: scan_public_copy.py <automod-file> <tokens-file>", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    token_file = Path(sys.argv[2])
    if not target.is_file():
        print(json.dumps({"status": "FAIL", "reason": f"missing {target}"}))
        return 2
    if not token_file.is_file():
        print(json.dumps({"status": "FAIL", "reason": f"missing tokens file {token_file}"}))
        return 2
    tokens = load_tokens(token_file)
    if not tokens:
        print(json.dumps({"status": "FAIL", "reason": "empty tokens file is not a pass"}))
        return 2
    hits = []
    for line_no, region in public_regions(target.read_text(encoding="utf-8")):
        for token in tokens:
            if token and token in region:
                hits.append({"line": line_no, "token": token})
    if hits:
        print(json.dumps({"status": "FAIL", "hits": hits}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "checked_tokens": len(tokens)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
