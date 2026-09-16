#!/usr/bin/env python3
"""Run static AAI checks that this package can actually attest."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    results = []
    package = run([PY, str(ROOT / "scripts/aai_runtime_gate.py"), "package", str(ROOT)])
    results.append(("package-gate", package.returncode, package.stdout.strip()))
    state = run([PY, str(ROOT / "scripts/aai_state_check.py"),
                 str(ROOT / "tests/fixtures/valid-state.yaml")])
    results.append(("state-valid", state.returncode, state.stdout.strip()))
    bad = run([PY, str(ROOT / "scripts/aai_runtime_gate.py"), "response",
               str(ROOT / "tests/fixtures/invalid-installed-claim.md")])
    rejected = bad.returncode != 0
    results.append(("reject-installed-claim", 0 if rejected else 1, bad.stdout.strip()))
    draft = run([PY, str(ROOT / "scripts/aai_runtime_gate.py"), "response",
                 str(ROOT / "tests/fixtures/valid-draft.md")])
    results.append(("language-draft", draft.returncode, draft.stdout.strip()))
    failed = [name for name, code, _ in results if code != 0]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "failed": failed,
        "results": [{"name": name, "exit": code} for name, code, _ in results],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if package.stdout:
        print(package.stdout)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
