#!/usr/bin/env python3
"""Firecrawl scrape. Reads key from secrets/keys.env. Never prints the key."""
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
    p.add_argument("url")
    p.add_argument("--formats", default="markdown")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.dry_run:
        json.dump({"ok": True, "dry_run": True, "route": "firecrawl_rest_scrape", "url": args.url}, sys.stdout)
        sys.stdout.write("\n")
        return
    env = load_env(ENV_PATH)
    key = env.get("FIRECRAWL_API_KEY") or os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        sys.stderr.write("BLOCKED: FIRECRAWL_API_KEY missing\n")
        sys.exit(2)
    body = json.dumps({
        "url": args.url,
        "formats": [x.strip() for x in args.formats.split(",") if x.strip()],
        "onlyMainContent": True,
    }).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = json.loads(resp.read().decode())
    except Exception as e:
        sys.stderr.write(f"BLOCKED: Firecrawl request failed: {e}\n")
        sys.exit(1)
    data = raw.get("data") or {}
    out = {
        "ok": bool(raw.get("success", True)),
        "route": "firecrawl_rest_scrape",
        "url": args.url,
        "title": data.get("metadata", {}).get("title") if isinstance(data.get("metadata"), dict) else None,
        "markdown": (data.get("markdown") or "")[:8000],
    }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
