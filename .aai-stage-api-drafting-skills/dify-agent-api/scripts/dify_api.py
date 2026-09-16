#!/usr/bin/env python3
"""Small Dify Agent Service API helper. Never print the API key."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SECRETS = Path(os.environ.get("DIFY_KEYS_FILE", Path(__file__).resolve().parents[1] / "secrets" / "keys.env"))


def load_env() -> None:
    if not SECRETS.is_file():
        return
    for raw in SECRETS.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def request(method: str, path: str, query: dict | None = None, body: dict | None = None) -> int:
    load_env()
    base = os.environ.get("DIFY_API_URL", "").rstrip("/")
    key = os.environ.get("DIFY_API_KEY", "")
    if not base or not key:
        print("BLOCKED DIFY_API_URL or DIFY_API_KEY missing", file=sys.stderr)
        return 2
    url = f"{base}{path}"
    if query:
        url = f"{url}?{urlencode(query)}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=60) as resp:
            print(resp.read().decode("utf-8", errors="replace"))
    except HTTPError as exc:
        print(f"BLOCKED HTTP {exc.code} {exc.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    sub.add_parser("parameters")
    sub.add_parser("meta")
    p_conv = sub.add_parser("conversations")
    p_conv.add_argument("--user", required=True)
    p_msg = sub.add_parser("messages")
    p_msg.add_argument("--conversation-id", required=True)
    p_msg.add_argument("--user", required=True)
    p_stop = sub.add_parser("stop")
    p_stop.add_argument("--task-id", required=True)
    p_stop.add_argument("--user", required=True)
    args = parser.parse_args()
    if args.cmd == "info":
        return request("GET", "/info")
    if args.cmd == "parameters":
        return request("GET", "/parameters")
    if args.cmd == "meta":
        return request("GET", "/meta")
    if args.cmd == "conversations":
        return request("GET", "/conversations", query={"user": args.user})
    if args.cmd == "messages":
        return request(
            "GET",
            "/messages",
            query={"user": args.user, "conversation_id": args.conversation_id},
        )
    if args.cmd == "stop":
        return request("POST", f"/chat-messages/{args.task_id}/stop", body={"user": args.user})
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
