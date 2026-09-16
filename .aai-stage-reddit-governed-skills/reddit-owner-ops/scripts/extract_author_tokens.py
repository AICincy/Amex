#!/usr/bin/env python3
"""Extract numeric author-check tokens from a current AutoMod file.

Writes tokens outside the skill. Does not embed community policy in this package.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

AUTHOR_NUM = re.compile(
    r"(?:karma|age)\s*:\s*[\"']?[<>]=?\s*(\d+)",
    re.IGNORECASE,
)
BARE_NUM = re.compile(r"\b(\d+)\b")


def extract(text: str) -> list[str]:
    tokens: list[str] = []
    in_author = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("author:"):
            in_author = True
            continue
        if in_author:
            if stripped and not line.startswith(" ") and not line.startswith("\t"):
                in_author = False
            else:
                for match in AUTHOR_NUM.finditer(stripped):
                    tokens.append(match.group(1))
                if "days" in stripped or "year" in stripped or "karma" in stripped:
                    for match in BARE_NUM.finditer(stripped):
                        tokens.append(match.group(1))
    # unique, stable order
    seen: set[str] = set()
    out: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.add(token)
            out.append(token)
    return out


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: extract_author_tokens.py <automod-file> <tokens-out>", file=sys.stderr)
        return 2
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    if not src.is_file():
        print(json.dumps({"status": "FAIL", "reason": f"missing {src}"}))
        return 2
    tokens = extract(src.read_text(encoding="utf-8"))
    dest.write_text("\n".join(tokens) + ("\n" if tokens else ""), encoding="utf-8")
    print(json.dumps({"status": "WRITTEN", "path": str(dest), "count": len(tokens)}))
    return 0 if tokens else 1


if __name__ == "__main__":
    raise SystemExit(main())
