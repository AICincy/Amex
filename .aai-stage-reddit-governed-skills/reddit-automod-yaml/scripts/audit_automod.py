#!/usr/bin/env python3
"""Deterministic AutoMod YAML audit. Does not fetch docs. Does not print secrets."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ILLEGAL_GROUPS = ("(?i)", "(?-i)", "(?i:", "(?-i:")
WRAP = {
    "includes": "%s",
    "includes-word": r"(?:^|\W|\b)%s(?:$|\W|\b)",
    "full-exact": r"^%s$",
    "full-text": r"^\W*%s\W*$",
    "starts-with": r"^%s",
    "ends-with": r"%s$",
}
FLAGS = re.DOTALL | re.UNICODE | re.IGNORECASE
CHECK_RE = re.compile(
    r"^(?P<neg>~)?(?P<field>title|body|url|domain|body\+title|title\+body)"
    r"(?:#\d+)?\s*\((?P<mods>[^)]*regex[^)]*)\)\s*:\s*(?P<val>.*)$"
)


def public_comment_regions(text: str) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    in_comment = False
    start = 0
    buf: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("comment:"):
            if line.strip() == "comment: |":
                in_comment = True
                start = i
                buf = []
                continue
            rows.append((i, line.split("comment:", 1)[1]))
            continue
        if in_comment:
            if line.startswith(" ") or line.startswith("\t"):
                buf.append(line)
            else:
                rows.append((start, "\n".join(buf)))
                in_comment = False
                buf = []
    if in_comment:
        rows.append((start, "\n".join(buf)))
    return rows


def load_tokens(path: Path | None) -> list[str]:
    if path is None or not path.is_file():
        return []
    tokens = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            tokens.append(line)
    return tokens


def split_docs(text: str) -> list[tuple[int, str]]:
    parts = re.split(r"(?m)^---\s*$", text)
    return [(i, p) for i, p in enumerate(parts)]


def audit(text: str, tokens: list[str]) -> dict:
    findings: list[dict] = []

    prefix = text.split("---", 1)[0]
    if prefix.strip():
        findings.append(
            {
                "id": "Y1",
                "class": "yaml",
                "severity": "high",
                "detail": "Text exists before the first --- separator.",
            }
        )

    if "\t" in text:
        findings.append(
            {
                "id": "Y2",
                "class": "yaml",
                "severity": "medium",
                "detail": "Tab characters present. AutoMod indent is spaces.",
            }
        )

    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith(" ") and line.strip() == "---":
            findings.append(
                {
                    "id": f"Y3-L{i}",
                    "class": "yaml",
                    "severity": "high",
                    "detail": "Document separator has leading spaces.",
                }
            )
        for g in ILLEGAL_GROUPS:
            if g in line and not line.lstrip().startswith("#"):
                findings.append(
                    {
                        "id": f"C1-L{i}",
                        "class": "compile",
                        "severity": "high",
                        "detail": f"Inline group {g} found. Case-insensitivity is default. Unicode /u compilers reject (?i).",
                    }
                )

    if yaml is None:
        findings.append(
            {
                "id": "Y0",
                "class": "unresolved-source",
                "severity": "high",
                "detail": "PyYAML missing. Document parse skipped.",
            }
        )
    else:
        for idx, body in split_docs(text):
            raw = body.strip()
            if not raw:
                continue
            content = [
                ln
                for ln in raw.splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
            if not content:
                continue
            try:
                yaml.safe_load(raw)
            except Exception as e:
                findings.append(
                    {
                        "id": f"Y4-D{idx}",
                        "class": "yaml",
                        "severity": "high",
                        "detail": f"YAML parse failed in document {idx}: {e}",
                    }
                )

    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = CHECK_RE.search(line.strip())
        if not m:
            continue
        mods = [x.strip() for x in m.group("mods").split(",")]
        val = m.group("val").strip()
        values: list[str]
        if val == "|":
            block = []
            for nxt in lines[i + 1 :]:
                if nxt.startswith(" ") or nxt.startswith("\t"):
                    block.append(nxt)
                else:
                    break
            findings.append(
                {
                    "id": f"C2-L{i+1}",
                    "class": "compile",
                    "severity": "high",
                    "detail": "Regex uses a YAML literal block. Indent and newline become part of the pattern.",
                    "repr": repr("\n".join(block)),
                }
            )
            values = ["\n".join(block)]
        elif yaml is not None:
            try:
                loaded = yaml.safe_load(val)
            except Exception as e:
                findings.append(
                    {
                        "id": f"C3-L{i+1}",
                        "class": "compile",
                        "severity": "high",
                        "detail": f"Regex value failed YAML load: {e}",
                    }
                )
                continue
            values = loaded if isinstance(loaded, list) else [loaded]
        else:
            values = [val]
        wrap_mod = "includes"
        for cand in (
            "includes-word",
            "full-exact",
            "full-text",
            "starts-with",
            "ends-with",
            "includes",
        ):
            if cand in mods:
                wrap_mod = cand
                break
        joined = "(%s)" % "|".join(str(v) for v in values)
        wrapped = WRAP[wrap_mod] % joined
        try:
            re.compile(wrapped, FLAGS)
        except Exception as e:
            findings.append(
                {
                    "id": f"C4-L{i+1}",
                    "class": "compile",
                    "severity": "high",
                    "detail": f"Python re compile failed: {e}",
                    "pattern": wrapped[:300],
                }
            )
        try:
            js = subprocess.run(
                [
                    "node",
                    "-e",
                    "const fs=require('fs'); const p=fs.readFileSync(0,'utf8'); try { new RegExp(p,'u'); } catch(e) { console.log(e.message); process.exit(3); }",
                ],
                input=wrapped,
                capture_output=True,
                text=True,
            )
            if js.returncode == 3:
                findings.append(
                    {
                        "id": f"C5-L{i+1}",
                        "class": "compile",
                        "severity": "high",
                        "detail": f"JS /u compile failed: {js.stdout.strip() or js.stderr.strip()}",
                    }
                )
        except FileNotFoundError:
            pass

    if tokens:
        for line_no, region in public_comment_regions(text):
            for token in tokens:
                if token and token in region:
                    findings.append(
                        {
                            "id": f"P1-L{line_no}",
                            "class": "public-copy",
                            "severity": "high",
                            "detail": f"Unpublished token leaked into public comment: {token}",
                        }
                    )

    karma_author = len(re.findall(r"combined_subreddit_karma:", text))
    if karma_author > 1:
        findings.append(
            {
                "id": "S1",
                "class": "scope",
                "severity": "medium",
                "detail": f"combined_subreddit_karma appears {karma_author} times. Confirm each is scoped to the intended parent_submission.",
            }
        )

    return {
        "status": "FAIL" if any(f.get("severity") == "high" for f in findings) else "PASS",
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: audit_automod.py <yaml> [tokens-file]", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    if not target.is_file():
        print(json.dumps({"status": "FAIL", "reason": f"missing {target}"}))
        return 2
    tokens = load_tokens(Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    result = audit(target.read_text(encoding="utf-8"), tokens)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
