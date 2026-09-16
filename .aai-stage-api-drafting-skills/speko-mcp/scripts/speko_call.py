#!/usr/bin/env python3
"""Call Speko Platform API. Reads SPEKO_API_KEY. Never prints the key."""
import json
import os
import sys
import uuid
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.environ.get("SPEKO_KEYS_FILE", os.path.join(ROOT, "secrets", "keys.env"))


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
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def main():
    args = [arg for arg in sys.argv[1:] if arg != "--dry-run"]
    dry_run = "--dry-run" in sys.argv[1:]
    if len(args) < 2:
        sys.stderr.write("usage: speko_call.py METHOD PATH [JSON_BODY] [--dry-run]\n")
        sys.exit(2)
    method = args[0].upper()
    path = args[1]
    body = args[2] if len(args) > 2 else None
    if dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "method": method, "path": path}))
        return
    env = load_env(ENV_PATH)
    key = env.get("SPEKO_API_KEY") or os.environ.get("SPEKO_API_KEY")
    if not key:
        sys.stderr.write("BLOCKED SPEKO_API_KEY missing\n")
        sys.exit(2)
    base = env.get("SPEKO_BASE_URL") or os.environ.get("SPEKO_BASE_URL") or "https://api.speko.dev"
    url = base.rstrip("/") + path
    headers = {
        "Authorization": "Bearer " + key,
        "Accept": "application/json",
        "Idempotency-Key": str(uuid.uuid4()),
    }
    data = None
    if body:
        headers["Content-Type"] = "application/json"
        data = body.encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            print(raw)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"HTTP {e.code} {path}\n{err}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
