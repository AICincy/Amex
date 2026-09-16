#!/usr/bin/env python3
"""Call Speko Platform API. Reads SPEKO_API_KEY. Never prints the key."""
import json
import os
import sys
import uuid
import urllib.error
import urllib.request
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.environ.get("SPEKO_KEYS_FILE", os.path.join(ROOT, "secrets", "keys.env"))
SPEKO_ORIGIN = "https://api.speko.dev"
ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


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


def validated_path(value):
    """Return a relative Speko API path or stop before any credential is read."""
    if not value.startswith("/") or value.startswith("//"):
        raise ValueError("PATH must start with exactly one '/'")
    if "\\" in value or any(ord(char) < 32 for char in value):
        raise ValueError("PATH contains an unsafe character")
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or parsed.username or parsed.password:
        raise ValueError("PATH must be relative to api.speko.dev")
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Reject redirects so an authorization header never crosses an origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def open_without_redirects(req, timeout):
    return urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout)


def main():
    args = [arg for arg in sys.argv[1:] if arg not in {"--dry-run", "--execute"}]
    dry_run = "--dry-run" in sys.argv[1:]
    execute = "--execute" in sys.argv[1:]
    if len(args) < 2:
        sys.stderr.write("usage: speko_call.py METHOD PATH [JSON_BODY] [--dry-run]\n")
        sys.exit(2)
    method = args[0].upper()
    if method not in ALLOWED_METHODS:
        sys.stderr.write("BLOCKED method must be one of GET, POST, PUT, PATCH, DELETE\n")
        return 2
    try:
        path = validated_path(args[1])
    except ValueError as exc:
        sys.stderr.write(f"BLOCKED {exc}\n")
        return 2
    body = args[2] if len(args) > 2 else None
    if dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "method": method, "path": path}))
        return
    if not execute:
        sys.stderr.write("BLOCKED --execute required for a live Speko request\n")
        return 2
    env = load_env(ENV_PATH)
    key = env.get("SPEKO_API_KEY") or os.environ.get("SPEKO_API_KEY")
    if not key:
        sys.stderr.write("BLOCKED SPEKO_API_KEY missing\n")
        sys.exit(2)
    url = SPEKO_ORIGIN + path
    parsed_url = urlsplit(url)
    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname != "api.speko.dev"
        or parsed_url.port is not None
        or parsed_url.username
        or parsed_url.password
    ):
        sys.stderr.write("BLOCKED unsafe Speko destination\n")
        return 2
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
        with open_without_redirects(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            print(raw)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        sys.stderr.write(f"HTTP {e.code} {path}\n{err}\n")
        sys.exit(1)


if __name__ == "__main__":
    raise SystemExit(main())
