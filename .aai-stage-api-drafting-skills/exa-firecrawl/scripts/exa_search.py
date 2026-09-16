#!/usr/bin/env python3
"""Exa search. Reads key from secrets/keys.env. Never prints the key."""
import argparse
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.environ.get("EXA_FIRECRAWL_KEYS_FILE", os.path.join(ROOT, "secrets", "keys.env"))


def load_env(path):
    if not os.path.isfile(path):
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--num", type=int, default=8)
    p.add_argument("--livecrawl", default="preferred")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.dry_run:
        json.dump({"ok": True, "dry_run": True, "route": "exa_rest_search", "query": args.query, "numResults": args.num}, sys.stdout)
        sys.stdout.write("\n")
        return
    env = load_env(ENV_PATH)
    key = env.get("EXA_API_KEY") or os.environ.get("EXA_API_KEY")
    if not key:
        sys.stderr.write("BLOCKED: EXA_API_KEY missing\n")
        sys.exit(2)
    body = json.dumps({
        "query": args.query,
        "numResults": args.num,
        "type": "auto",
        "contents": {"text": {"maxCharacters": 1200}},
        "livecrawl": args.livecrawl,
    }).encode()
    req = urllib.request.Request(
        "https://api.exa.ai/search",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = json.loads(resp.read().decode())
    except Exception as e:
        sys.stderr.write(f"BLOCKED: Exa request failed: {e}\n")
        sys.exit(1)
    rows = []
    for r in raw.get("results", []):
        rows.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "published": r.get("publishedDate"),
            "text": (r.get("text") or "")[:800],
        })
    json.dump({"ok": True, "route": "exa_rest_search", "results": rows}, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
