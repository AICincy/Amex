#!/usr/bin/env python3
"""CourtListener REST v4 helper. Token optional. Never prints the token."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.environ.get("COURTLISTENER_KEYS_FILE", os.path.join(ROOT, "secrets", "keys.env"))
BASE = "https://www.courtlistener.com/api/rest/v4"
SEARCH_TYPES = ("o", "r", "rd", "d", "p", "oa")


def load_env(path: str) -> dict[str, str]:
    if not os.path.isfile(path):
        return {}
    out: dict[str, str] = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def token() -> str:
    env = load_env(ENV_PATH)
    return env.get("COURTLISTENER_TOKEN") or os.environ.get("COURTLISTENER_TOKEN") or ""


def headers() -> dict[str, str]:
    out = {
        "Accept": "application/json",
        "User-Agent": "aai-courtlistener-api",
    }
    tok = token()
    if tok:
        out["Authorization"] = f"Token {tok}"
    return out


def redact(text: str) -> str:
    tok = token()
    return text.replace(tok, "[REDACTED]") if tok else text


def request(url: str) -> tuple[int, dict | list | str]:
    req = urllib.request.Request(url, headers=headers(), method="GET")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.getcode()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": redact(body)[:4000]}
        return exc.code, parsed
    except Exception as exc:
        return 0, {"error": redact(str(exc))}
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, {"raw": raw[:4000]}


def emit(payload: dict, code: int) -> int:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    if payload.get("ok"):
        return 0
    return 1 if code and code >= 400 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="GET CourtListener v4")
    sub = parser.add_subparsers(dest="cmd", required=True)

    search = sub.add_parser("search")
    search.add_argument("--q", required=True)
    search.add_argument("--type", default="r", choices=SEARCH_TYPES)
    search.add_argument("--court", default="")
    search.add_argument("--page-size", type=int, default=20)
    search.add_argument("--dry-run", action="store_true")

    getp = sub.add_parser("get")
    getp.add_argument("--path", required=True, help="API path starting with /, e.g. /dockets/1/")
    getp.add_argument("--params", default="", help="raw query string")
    getp.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.cmd == "search":
        query = {"q": args.q, "type": args.type}
        if args.court:
            query["court"] = args.court
        url = BASE + "/search/?" + urllib.parse.urlencode(query)
        if args.dry_run:
            return emit(
                {
                    "ok": True,
                    "route": "courtlistener_dry_run",
                    "method": "GET",
                    "url": url,
                    "auth": bool(token()),
                    "type": args.type,
                },
                200,
            )
        status, body = request(url)
        ok = status == 200 and isinstance(body, dict)
        return emit(
            {
                "ok": ok,
                "route": "courtlistener_search",
                "status": status,
                "url": url,
                "auth": bool(token()),
                "count": body.get("count") if isinstance(body, dict) else None,
                "result": body,
            },
            status,
        )

    path = args.path if args.path.startswith("/") else "/" + args.path
    url = BASE + path
    if args.params:
        url += ("&" if "?" in url else "?") + args.params
    if args.dry_run:
        return emit(
            {
                "ok": True,
                "route": "courtlistener_dry_run",
                "method": "GET",
                "url": url,
                "auth": bool(token()),
            },
            200,
        )
    status, body = request(url)
    ok = status == 200
    return emit(
        {
            "ok": ok,
            "route": "courtlistener_get",
            "status": status,
            "url": url,
            "auth": bool(token()),
            "result": body,
        },
        status,
    )


if __name__ == "__main__":
    raise SystemExit(main())
