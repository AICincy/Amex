#!/usr/bin/env python3
"""Run the canonical AAI package gate from this local package."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

CANONICAL = Path(__file__).resolve().parents[2] / "scripts" / "aai_runtime_gate.py"


def main() -> int:
    if not CANONICAL.is_file():
        print("BLOCKED: canonical aai_runtime_gate.py missing", file=sys.stderr)
        return 2
    sys.argv[0] = str(CANONICAL)
    runpy.run_path(str(CANONICAL), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
