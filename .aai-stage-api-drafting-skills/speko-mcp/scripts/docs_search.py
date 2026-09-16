#!/usr/bin/env python3
"""Call Speko public docs MCP docs.search. No key required."""
import json
import sys
import urllib.request

URL = "https://speko.ai/.well-known/mcp"


def rpc(payload):
    req = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    args = [arg for arg in sys.argv[1:] if arg != "--dry-run"]
    dry_run = "--dry-run" in sys.argv[1:]
    query = " ".join(args).strip()
    if not query:
        sys.stderr.write("usage: docs_search.py QUERY [--dry-run]\n")
        sys.exit(2)
    if dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "route": "speko_docs_search", "query": query}))
        return
    result = rpc(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "docs.search",
                "arguments": {"query": query, "limit": 8},
            },
        }
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
