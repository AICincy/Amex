#!/usr/bin/env python3
"""Fail if automod/current FAQ helper URL != ops current_common_questions_thread.

Does not edit YAML.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def thread_id(url: str) -> str | None:
    m = re.search(r"/comments/([a-z0-9]+)/", url)
    return m.group(1) if m else None


def load_ops_url(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("current_common_questions_thread:"):
            raw = line.split(":", 1)[1].strip()
            return json.loads(raw) if raw.startswith('"') else raw
    raise SystemExit("BLOCKED: current_common_questions_thread missing from ops")


def load_yaml_helper(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    found = re.findall(
        r"https://www\.reddit\.com/r/amex/comments/[a-z0-9]+/monthly_common_questions_advice_thread/",
        text,
    )
    if not found:
        raise SystemExit("BLOCKED: no Common Questions helper URL in YAML")
    return found[-1]


def main() -> int:
    ops = Path(sys.argv[1] if len(sys.argv) > 1 else "ops/amex-ops-state.public.yaml")
    yaml_path = Path(
        sys.argv[2]
        if len(sys.argv) > 2
        else "automod/current/r-amex-automod-0.1.3.5.yaml"
    )
    live = load_ops_url(ops)
    draft = load_yaml_helper(yaml_path)
    live_id = thread_id(live)
    draft_id = thread_id(draft)
    drift = live_id != draft_id
    result = {
        "ok": not drift,
        "live": live,
        "live_id": live_id,
        "draft": draft,
        "draft_id": draft_id,
        "drift": drift,
    }
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    if drift:
        print(
            f"FAIL: FAQ helper drift draft={draft_id} live={live_id}",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
