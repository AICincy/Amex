#!/usr/bin/env python3
"""Fetch live r/amex monthly thread IDs from Arctic Shift and update ops YAML.

Does not edit AutoMod YAML.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
UA = "AICincy-Amex-live-pointers/1.0"


def get(url: str) -> dict:
    last = None
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            last = SystemExit(f"BLOCKED Arctic Shift {e.code}: {body}")
            if e.code in (422, 429, 500, 502, 503, 504):
                time.sleep(8 * (attempt + 1))
                continue
            raise last
        except TimeoutError as e:
            last = e
            time.sleep(8 * (attempt + 1))
    raise last or SystemExit("BLOCKED Arctic Shift")


def newest(query: str, title_exact: str | None = None) -> dict:
    qs = urllib.parse.urlencode(
        {"subreddit": "amex", "query": query, "limit": 15, "sort": "desc"}
    )
    data = get(f"{BASE}?{qs}").get("data") or []
    rows = []
    for item in data:
        row = item.get("data", item) if isinstance(item, dict) else {}
        title = (row.get("title") or "").strip()
        if title_exact and title != title_exact:
            continue
        rows.append(row)
    if not rows:
        for item in data:
            row = item.get("data", item) if isinstance(item, dict) else {}
            title = (row.get("title") or "").strip().lower()
            if query.lower() in title:
                rows.append(row)
    if not rows:
        raise SystemExit(f"BLOCKED: no Arctic Shift hit for {query!r}")
    rows.sort(key=lambda r: int(r.get("created_utc") or 0), reverse=True)
    return rows[0]


def permalink(row: dict) -> str:
    p = row.get("permalink") or f"/r/amex/comments/{row.get('id')}/"
    if p.startswith("http"):
        return p
    return "https://www.reddit.com" + p


def upsert(text: str, key: str, value: str) -> str:
    line = f"{key}: {value}"
    if re.search(rf"^{re.escape(key)}:", text, flags=re.M):
        return re.sub(rf"^{re.escape(key)}:.*$", line, text, count=1, flags=re.M)
    return text.rstrip() + "\n" + line + "\n"


def main() -> int:
    ops_path = Path(sys.argv[1] if len(sys.argv) > 1 else "ops/amex-ops-state.public.yaml")
    referral = newest("Monthly Amex Referral Thread", "Monthly Amex Referral Thread")
    questions = newest("Monthly Common Questions", "Monthly Common Questions & Advice Thread")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = ops_path.read_text(encoding="utf-8")
    text = upsert(text, "live_fetch_route", "arctic-shift.photon-reddit.com")
    text = upsert(text, "live_fetch_at", json.dumps(now))
    text = upsert(text, "current_referral_thread_title", referral.get("title") or "")
    text = upsert(text, "current_referral_thread", json.dumps(permalink(referral)))
    text = upsert(
        text,
        "current_common_questions_thread",
        json.dumps(permalink(questions)),
    )
    ops_path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    out = {
        "ok": True,
        "referral_id": referral.get("id"),
        "referral": permalink(referral),
        "questions_id": questions.get("id"),
        "questions": permalink(questions),
        "ops": str(ops_path),
    }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
