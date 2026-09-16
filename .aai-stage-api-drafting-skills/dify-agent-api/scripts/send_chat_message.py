#!/usr/bin/env python3
"""Stream a Dify Agent chat message. Never print the API key."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import urllib.error
import urllib.request

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


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--user", required=True)
    parser.add_argument("--conversation-id", default="")
    args = parser.parse_args()

    base = os.environ.get("DIFY_API_URL", "").rstrip("/")
    key = os.environ.get("DIFY_API_KEY", "")
    if not base or not key:
        print("BLOCKED DIFY_API_URL or DIFY_API_KEY missing", file=sys.stderr)
        return 2

    body = {
        "inputs": {},
        "query": args.query,
        "response_mode": "streaming",
        "user": args.user,
        "conversation_id": args.conversation_id,
        "auto_generate_name": True,
    }
    req = urllib.request.Request(
        f"{base}/chat-messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=3600) as resp:
            conversation_id = ""
            answer_parts: list[str] = []
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    event = json.loads(payload)
                except json.JSONDecodeError:
                    print(payload)
                    continue
                ev = event.get("event")
                if event.get("conversation_id"):
                    conversation_id = event["conversation_id"]
                if ev == "agent_message":
                    delta = event.get("answer") or event.get("thought") or ""
                    if delta:
                        answer_parts.append(delta)
                        print(delta, end="", flush=True)
                elif ev == "message":
                    final = event.get("answer") or ""
                    if final and not answer_parts:
                        print(final, end="", flush=True)
                        answer_parts.append(final)
                elif ev == "error":
                    print(f"\nBLOCKED {event.get('code')} {event.get('message')}", file=sys.stderr)
                    return 2
            print()
            if conversation_id:
                print(f"conversation_id={conversation_id}")
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8", errors="replace")
        print(f"BLOCKED HTTP {exc.code} {err}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"BLOCKED {type(exc).__name__}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
