#!/usr/bin/env python3
"""Thin wrapper. Canonical gate lives in aai-cognitive-interface/scripts."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
CANDIDATES = []
for parent in HERE.parents:
    CANDIDATES.append(parent / "aai-cognitive-interface" / "scripts" / "aai_runtime_gate.py")
    CANDIDATES.append(parent / "artifacts" / "aai-cognitive-interface" / "scripts" / "aai_runtime_gate.py")


def main() -> int:
    seen = []
    for path in CANDIDATES:
        if path in seen:
            continue
        seen.append(path)
        if path.is_file() and path.stat().st_size > 2000:
            sys.argv[0] = str(path)
            runpy.run_path(str(path), run_name="__main__")
            return 0
    print("BLOCKED: canonical aai_runtime_gate.py not found", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
