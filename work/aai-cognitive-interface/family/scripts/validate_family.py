#!/usr/bin/env python3
"""Validate only the supplied AAI governor package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "aai_runtime_gate.py"


def main() -> int:
    completed = subprocess.run(
        [sys.executable, str(GATE), "package", str(ROOT)],
        text=True,
        capture_output=True,
        check=False,
    )
    payload = {
        "scope": "aai-cognitive-interface only",
        "status": "STATIC-PASS" if completed.returncode == 0 else "FAIL",
        "exit": completed.returncode,
        "root": str(ROOT),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if completed.returncode != 0:
        print(completed.stdout or completed.stderr, file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
