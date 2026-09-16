#!/usr/bin/env python3
"""Run the 20-prompt local adversarial control suite and save an evidence report.

This runner tests local skill controls and safe helper behavior. It never calls
external APIs, Reddit, or a model service.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "adversarial-skill-prompts-2026-09-16"
SKILLS = Path(r"C:\Users\jared\.codex\skills")
PYTHON = Path(r"C:\Users\jared\AppData\Local\Python\bin\python.exe")

# Every prompt has a named local skill and at least one control phrase that the
# installed package must carry. Resend is intentionally removed by owner order.
CASES = {
    "aai-cognitive-interface": ("aai-cognitive-interface", "Never substitute"),
    "authority-currency-auditor": ("authority-currency-auditor", "primary"),
    "claim-source-auditor": ("claim-source-auditor", "Never mark"),
    "courtlistener-api": ("courtlistener-api", "Never print"),
    "dify-agent-api": ("dify-agent-api", "dry-run"),
    "enformion-go-api": ("enformion-go-api", "dry-run"),
    "exa-firecrawl": ("exa-firecrawl", "dry-run"),
    "forensic-evidentiary-drafting": ("forensic-evidentiary-drafting", "Do not"),
    "personal-context": ("personal-context", "Do not"),
    "practitioner-narrative-writer": ("practitioner-narrative-writer", "Do not invent"),
    "prompt-architecture-engineering": ("prompt-architecture-engineering", "Do not invent tools"),
    "record-series-builder": ("record-series-builder", "Do not invent"),
    "reddit-automod-yaml": ("reddit-automod-yaml", "Do not"),
    "reddit-owner-ops": ("reddit-owner-ops", "human gate"),
    "register-mediation": ("register-mediation", "One retry"),
    "regulatory-complaint-drafting": ("regulatory-complaint-drafting", "human gates"),
    "research-execution-briefs": ("research-execution-briefs", "primary"),
    "resend-api": ("resend-api", None),
    "speko-mcp": ("speko-mcp", "dry-run"),
    "subreddit-rule-packet": ("subreddit-rule-packet", "live Reddit publication"),
}


def run(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout[-1200:]


def check_prompt_case(case: str) -> dict:
    prompt_path = PROMPTS / f"{case}.md"
    skill_name, marker = CASES[case]
    result = {"id": case, "prompt": str(prompt_path.relative_to(ROOT))}
    if not prompt_path.is_file():
        return result | {"status": "FAIL", "reason": "prompt file missing"}
    prompt = prompt_path.read_text(encoding="utf-8")
    result["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
    if not any(boundary in prompt.lower() for boundary in ("do not", "never", "without", "refuse", "reject")):
        return result | {"status": "FAIL", "reason": "prompt lacks an explicit boundary"}
    skill_path = SKILLS / skill_name / "SKILL.md"
    if case == "resend-api":
        if skill_path.exists():
            return result | {"status": "FAIL", "reason": "Resend should be removed"}
        return result | {
            "status": "PASS",
            "mode": "removal",
            "evidence": "Resend skill is absent by approved removal.",
        }
    if not skill_path.is_file():
        return result | {"status": "FAIL", "reason": f"installed skill missing: {skill_path}"}
    text = skill_path.read_text(encoding="utf-8")
    if marker and marker.lower() not in text.lower():
        return result | {"status": "FAIL", "reason": f"control marker missing: {marker}"}
    return result | {
        "status": "PASS",
        "mode": "static-control",
        "evidence": f"{skill_path} contains required control marker: {marker}",
    }


def dynamic_cases() -> list[dict]:
    py = str(PYTHON if PYTHON.is_file() else Path(sys.executable))
    calls = [
        (
            "dify-dry-run",
            [py, str(SKILLS / "dify-agent-api" / "scripts" / "dify_api.py"), "parameters", "--dry-run"],
            0,
            '"dry_run": true',
        ),
        (
            "dify-live-gate",
            [py, str(SKILLS / "dify-agent-api" / "scripts" / "dify_api.py"), "parameters"],
            2,
            "--execute required",
        ),
        (
            "enformion-dry-run",
            [py, str(SKILLS / "enformion-go-api" / "scripts" / "enformion_call.py"), "contact-enrich", "--dry-run", "--body", '{"FirstName":"Jane","LastName":"Example"}'],
            0,
            '"billed": false',
        ),
        (
            "enformion-live-gate",
            [py, str(SKILLS / "enformion-go-api" / "scripts" / "enformion_call.py"), "contact-enrich"],
            2,
            "live Enformion requests are disabled",
        ),
        (
            "speko-safe-dry-run",
            [py, str(SKILLS / "speko-mcp" / "scripts" / "speko_call.py"), "GET", "/v1/agents", "--dry-run"],
            0,
            '"dry_run": true',
        ),
        (
            "speko-origin-gate",
            [py, str(SKILLS / "speko-mcp" / "scripts" / "speko_call.py"), "GET", "@attacker.example/", "--dry-run"],
            2,
            "PATH must start with exactly one",
        ),
    ]
    results = []
    for name, command, expected_exit, expected_text in calls:
        exit_code, output = run(command)
        ok = exit_code == expected_exit and expected_text.lower() in output.lower()
        results.append(
            {
                "id": name,
                "status": "PASS" if ok else "FAIL",
                "mode": "local-behavior",
                "expected_exit": expected_exit,
                "actual_exit": exit_code,
                "expected_text": expected_text,
                "output": output,
            }
        )
    return results


def automod_case() -> dict:
    py = str(PYTHON if PYTHON.is_file() else Path(sys.executable))
    target = ROOT / "automod" / "current" / "r-amex-automod-0.1.3.5.yaml"
    audit = ROOT / ".aai-stage-reddit-governed-skills" / "reddit-automod-yaml" / "scripts" / "audit_automod.py"
    exit_code, output = run([py, str(audit), str(target)])
    text = target.read_text(encoding="utf-8")
    ok = (
        exit_code == 0
        and '"status": "PASS"' in output
        and "monthly.{0,80}referral.{0,30}thread" not in text
        and "combined_subreddit_karma" not in text
    )
    return {
        "id": "automod-hardening",
        "status": "PASS" if ok else "FAIL",
        "mode": "local-policy",
        "actual_exit": exit_code,
        "output": output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the 20-prompt local adversarial suite")
    parser.add_argument(
        "--output",
        default=str(ROOT / "audits" / "adversarial-skill-suite-2026-09-16.json"),
        help="JSON report path",
    )
    args = parser.parse_args()
    missing = sorted(set(path.stem for path in PROMPTS.glob("*.md")) ^ set(CASES))
    cases = [check_prompt_case(case) for case in sorted(CASES)]
    dynamic = dynamic_cases() + [automod_case()]
    report = {
        "suite": "adversarial-skill-prompts-2026-09-16",
        "executed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": "local static controls and credential-free helper behavior only",
        "prompt_case_count": len(cases),
        "dynamic_case_count": len(dynamic),
        "unexpected_prompt_mappings": missing,
        "prompt_cases": cases,
        "dynamic_cases": dynamic,
    }
    all_cases = cases + dynamic
    report["status"] = "PASS" if not missing and all(row["status"] == "PASS" for row in all_cases) else "FAIL"
    report["passed"] = sum(row["status"] == "PASS" for row in all_cases)
    report["failed"] = sum(row["status"] == "FAIL" for row in all_cases)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "passed", "failed", "prompt_case_count", "dynamic_case_count")}, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
