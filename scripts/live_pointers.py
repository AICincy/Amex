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
import argparse
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
UA = "AICincy-Amex-live-pointers/1.0"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OPS_PATH = REPO_ROOT / "ops" / "amex-ops-state.public.yaml"
ID_RE = re.compile(r"^[a-z0-9]{6,12}$")


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
    if not title_exact:
        raise SystemExit("BLOCKED: an exact expected title is required")
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
        raise SystemExit(f"BLOCKED: no exact Arctic Shift hit for {title_exact!r}")
    rows.sort(key=lambda r: int(r.get("created_utc") or 0), reverse=True)
    return rows[0]


def permalink(row: dict) -> str:
    post_id = str(row.get("id") or "").lower()
    if not ID_RE.fullmatch(post_id):
        raise SystemExit("BLOCKED: Arctic Shift result has an invalid Reddit post id")
    supplied = str(row.get("permalink") or "")
    if supplied:
        parsed = urllib.parse.urlsplit(supplied)
        if parsed.scheme and (
            parsed.scheme != "https"
            or parsed.hostname != "www.reddit.com"
            or parsed.username
            or parsed.password
            or parsed.port is not None
        ):
            raise SystemExit("BLOCKED: Arctic Shift result has an unsafe permalink origin")
        if not re.fullmatch(rf"/r/amex/comments/{post_id}/[^?#]*", parsed.path):
            raise SystemExit("BLOCKED: Arctic Shift permalink does not match its post id")
    return f"https://www.reddit.com/r/amex/comments/{post_id}/"


def upsert(text: str, key: str, value: str) -> str:
    line = f"{key}: {json.dumps(value)}"
    if re.search(rf"^{re.escape(key)}:", text, flags=re.M):
        return re.sub(rf"^{re.escape(key)}:.*$", line, text, count=1, flags=re.M)
    return text.rstrip() + "\n" + line + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare validated r/amex pointer updates")
    parser.add_argument("ops_path", nargs="?", default=str(DEFAULT_OPS_PATH))
    parser.add_argument("--apply", action="store_true", help="write the designated ops file")
    args = parser.parse_args()
    ops_path = Path(args.ops_path).resolve()
    if ops_path != DEFAULT_OPS_PATH.resolve():
        raise SystemExit(f"BLOCKED: ops path must be {DEFAULT_OPS_PATH}")
    referral = newest("Monthly Amex Referral Thread", "Monthly Amex Referral Thread")
    questions = newest("Monthly Common Questions", "Monthly Common Questions & Advice Thread")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = ops_path.read_text(encoding="utf-8")
    text = upsert(text, "live_fetch_route", "arctic-shift.photon-reddit.com")
    text = upsert(text, "live_fetch_at", now)
    text = upsert(text, "current_referral_thread_title", str(referral.get("title") or ""))
    text = upsert(text, "current_referral_thread", permalink(referral))
    text = upsert(
        text,
        "current_common_questions_thread",
        permalink(questions),
    )
    output = text if text.endswith("\n") else text + "\n"
    if args.apply:
        temporary = ops_path.with_suffix(".tmp")
        temporary.write_text(output, encoding="utf-8")
        temporary.replace(ops_path)
    out = {
        "ok": True,
        "referral_id": referral.get("id"),
        "referral": permalink(referral),
        "questions_id": questions.get("id"),
        "questions": permalink(questions),
        "ops": str(ops_path),
        "dry_run": not args.apply,
        "applied": args.apply,
    }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
