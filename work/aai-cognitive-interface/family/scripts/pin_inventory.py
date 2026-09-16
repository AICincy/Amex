#!/usr/bin/env python3
"""SHA256 pin inventory for AAI family skills."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FAMILY = Path(__file__).resolve().parents[1]
ROOT = FAMILY.parents[0]
OUT = FAMILY / "state" / "skill-pin-inventory.json"
SKIP_PARTS = {"__pycache__", "untrusted-cache", "state"}
SKILLS = ["aai-cognitive-interface"]


def hashed_files(skill_root: Path) -> dict[str, str]:
    pins: dict[str, str] = {}
    for path in sorted(skill_root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        rel = path.relative_to(skill_root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        pins[rel] = digest
    return pins


def build() -> dict:
    packages = []
    for name in SKILLS:
        path = ROOT / name
        if not path.is_dir():
            packages.append({"skill": name, "status": "ABSENT", "files": {}})
            continue
        files = hashed_files(path)
        packages.append(
            {
                "skill": name,
                "status": "PINNED",
                "path": str(path.resolve()),
                "file_count": len(files),
                "files": files,
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT.resolve()),
        "algorithm": "sha256",
        "note": "Pins are drift evidence. They are not INSTALLED or RUNTIME labels.",
        "packages": packages,
    }


def check(current: dict) -> list[str]:
    if not OUT.is_file():
        return ["missing inventory"]
    prior = json.loads(OUT.read_text(encoding="utf-8"))
    failures = []
    prior_map = {item["skill"]: item for item in prior.get("packages", [])}
    for item in current["packages"]:
        name = item["skill"]
        old = prior_map.get(name)
        if old is None:
            failures.append(f"{name}: not in prior inventory")
            continue
        if item.get("status") != old.get("status"):
            failures.append(f"{name}: status {old.get('status')} -> {item.get('status')}")
        old_files = old.get("files", {})
        new_files = item.get("files", {})
        for rel, digest in sorted(new_files.items()):
            if rel not in old_files:
                failures.append(f"{name}: added {rel}")
            elif old_files[rel] != digest:
                failures.append(f"{name}: changed {rel}")
        for rel in sorted(set(old_files) - set(new_files)):
            failures.append(f"{name}: removed {rel}")
    return failures


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "write"
    current = build()
    if mode == "check":
        failures = check(current)
        payload = {
            "mode": "check",
            "status": "PASS" if not failures else "DRIFT",
            "failures": failures,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if not failures else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload = {
        "mode": "write",
        "status": "REFRESHED",
        "path": str(OUT),
        "package_count": len(current["packages"]),
        "absent": [p["skill"] for p in current["packages"] if p["status"] == "ABSENT"],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
