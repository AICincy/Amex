#!/usr/bin/env python3
"""Deterministic package and response checks for AAI."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping key is not scalar",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"duplicate key: {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


PROHIBITED = {
    "perhaps you might consider": "indirect recommendation",
    "it's worth noting that": "filler",
    "keep in mind that": "filler",
    "great question": "praise preamble",
    "that's a good point": "praise preamble",
    "i understand how you feel": "unsupported emotional mirroring",
    "you may want to": "delegated execution returned to user",
    "let me search for that": "future-tense tool narration",
    "let me check": "future-tense tool narration",
}

REQUIRED_FILES = {
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "assets/icon.svg",
    "references/operator-model.md",
    "references/runtime-contract.md",
    "references/acceptance-tests.md",
    "references/continuation-protocol.md",
    "references/crisis-protocol.md",
    "references/retrieval-scaffolding.md",
    "references/register-examples.md",
    "references/register-precedence.md",
    "references/execution-trail-template.md",
    "references/package-identity.md",
    "references/composition-map.md",
    "references/host-binding.md",
    "references/state-schema.md",
    "references/runtime-only.md",
    "references/trusted-controller.md",
    "references/host-activation.md",
    "references/connector-routing.md",
    "schemas/turn-state.schema.json",
    "schemas/evidence-ledger.schema.json",
    "scripts/aai_runtime_gate.py",
    "scripts/aai_state_check.py",
}

REQUIRED_SKILL_MARKERS = {
    "## Runtime kernel",
    "## Action-before-narration gate",
    "## State custody",
    "## Artifact completion contract",
    "## Cognitive-ceiling takeover",
    "## Execution trail",
    "## External dependencies",
    "## Runtime-only overlay",
    "## No silent failure",
    "## Final response gate",
    "## Register precedence",
}

GENERIC_REQUIRED_FILES = {"SKILL.md", "agents/openai.yaml"}

SUBORDINATE_MARKERS = {
    "mandatory governing runtime",
    "subordinate",
    "must not override, narrow, suspend, or reinterpret AAI",
    "authorized scope",
    "hard constraints",
    "completion evidence",
    "status",
}

STATUS_PATTERNS = {
    "DRAFTED": re.compile(r"\bDRAFTED\b"),
    "STATIC-PASS": re.compile(r"\bSTATIC-PASS\b", re.IGNORECASE),
    "SAVED": re.compile(r"\bSAVED\b"),
    "INSTALLED": re.compile(r"\bINSTALLED\b"),
    "RUNTIME-SMOKE-PASS": re.compile(r"\bRUNTIME-SMOKE-PASS\b", re.IGNORECASE),
    "RUNTIME-VERIFIED": re.compile(r"\bRUNTIME-VERIFIED\b", re.IGNORECASE),
    "ADVERSARIAL-PASS": re.compile(r"\bADVERSARIAL-PASS\b", re.IGNORECASE),
}

STATUS_HYPHENS = str.maketrans({
    "\u2010": "-",  # hyphen
    "\u2011": "-",  # nonbreaking hyphen
    "\u2012": "-",  # figure dash
    "\u2013": "-",  # en dash
    "\u2014": "-",  # em dash
    "\u2212": "-",  # minus sign
})

STANDALONE_UNVERIFIABLE = {
    "SAVED",
    "INSTALLED",
    "RUNTIME-SMOKE-PASS",
    "RUNTIME-VERIFIED",
    "ADVERSARIAL-PASS",
}

def result(mode: str, violations: list[dict[str, str]]) -> int:
    payload = {
        "mode": mode,
        "status": "PASS" if not violations else "FAIL",
        "violation_count": len(violations),
        "violations": violations,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not violations else 1


def skill_name(skill_path: Path) -> str | None:
    if not skill_path.is_file():
        return None
    try:
        text = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    names = [value.strip().strip("'\"") for value in
             re.findall(r"^name:\s*([^\n]+?)\s*$", match.group(1), re.MULTILINE)]
    if "aai-cognitive-interface" in names:
        return "aai-cognitive-interface"
    return names[0] if len(names) == 1 else None


def check_frontmatter(text: str, expected_name: str | None, violations) -> dict | None:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        violations.append({"rule": "frontmatter", "detail": "frontmatter block missing"})
        return None
    raw = match.group(1)
    keys = re.findall(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:", raw, re.MULTILINE)
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        violations.append({"rule": "frontmatter", "detail": f"duplicate keys: {duplicates}"})
    if set(keys) != {"name", "description"}:
        violations.append({
            "rule": "frontmatter",
            "detail": f"allowed keys are name and description; found {sorted(set(keys))}",
        })
    try:
        document = yaml.load(raw, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        violations.append({"rule": "frontmatter", "detail": f"invalid YAML: {exc}"})
        return None
    if not isinstance(document, dict):
        violations.append({"rule": "frontmatter", "detail": "frontmatter must be a mapping"})
        return None
    if set(document) != {"name", "description"}:
        violations.append({
            "rule": "frontmatter",
            "detail": f"parsed keys must be name and description; found {sorted(map(str, document))}",
        })
    if expected_name is not None and document.get("name") != expected_name:
        violations.append({"rule": "frontmatter", "detail": f"name must be {expected_name}"})
    if not nonempty_string(document.get("description")):
        violations.append({"rule": "frontmatter", "detail": "description must be a nonempty string"})
    return document


def check_agent_metadata(root: Path, name: str | None, violations) -> None:
    path = root / "agents/openai.yaml"
    if not path.is_file() or not name:
        return
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        violations.append({"rule": "agent-metadata", "detail": f"invalid YAML: {exc}"})
        return
    if not isinstance(document, dict):
        violations.append({"rule": "agent-metadata", "detail": "root must be a mapping"})
        return
    interface = document.get("interface")
    policy = document.get("policy")
    if not isinstance(interface, dict):
        violations.append({"rule": "agent-metadata", "detail": "interface mapping missing"})
    else:
        for field in ("display_name", "short_description", "default_prompt"):
            if not nonempty_string(interface.get(field)):
                violations.append({"rule": "agent-metadata", "detail": f"interface.{field} missing"})
        token = re.compile(rf"(?<![\w-])\${re.escape(name)}(?![\w-])")
        if nonempty_string(interface.get("default_prompt")) and not token.search(interface["default_prompt"]):
            violations.append({"rule": "agent-metadata", "detail": "default prompt omits skill name"})
    if not isinstance(policy, dict) or type(policy.get("allow_implicit_invocation")) is not bool:
        violations.append({"rule": "agent-metadata", "detail": "boolean invocation policy missing"})
    elif name == "aai-cognitive-interface" and policy["allow_implicit_invocation"] is not True:
        violations.append({"rule": "agent-metadata", "detail": "AAI must allow implicit invocation"})


def markdown_link_targets(text: str):
    """Yield Markdown link targets outside fenced and inline code."""
    visible_lines = []
    fence_char = None
    fence_width = 0
    for line in text.splitlines():
        if fence_char is not None:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_char)}{{{fence_width},}}[ \t]*$",
                line,
            )
            if closing:
                fence_char, fence_width = None, 0
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening:
            marker = opening.group(1)
            info = opening.group(2)
            if marker[0] != "`" or "`" not in info:
                fence_char, fence_width = marker[0], len(marker)
                continue
        visible_lines.append(re.sub(r"(`+)[^\n]*?\1", " ", line))
    visible = "\n".join(visible_lines)
    for match in re.finditer(r"(?<!\\)\[[^\]\n]+\]\(([^)\n]+)\)", visible):
        yield match.group(1)

    def normalized_label(value):
        return " ".join(value.split()).casefold()

    referenced_labels = set()
    for match in re.finditer(
        r"(?<!\\)\[([^\]\n]+)\]\[([^\]\n]*)\]",
        visible,
    ):
        referenced_labels.add(normalized_label(match.group(2) or match.group(1)))
    definitions = re.finditer(
        r"^ {0,3}(?<!\\)\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|([^\s]+))",
        visible,
        re.MULTILINE,
    )
    for match in definitions:
        if normalized_label(match.group(1)) in referenced_labels:
            yield match.group(2) or match.group(3)


def check_aai_package(root: Path) -> int:
    violations: list[dict[str, str]] = []
    if root.name != "aai-cognitive-interface":
        violations.append({
            "rule": "package-identity",
            "detail": f"directory must be aai-cognitive-interface, found {root.name}",
        })
    for relative in sorted(REQUIRED_FILES):
        required = root / relative
        if not required.is_file():
            violations.append({"rule": "required-file", "detail": relative})
            continue
        try:
            required.resolve().relative_to(root.resolve())
        except (OSError, RuntimeError, ValueError):
            violations.append({"rule": "required-file", "detail": f"escapes package: {relative}"})
            continue
        try:
            if not required.read_text(encoding="utf-8").strip():
                violations.append({"rule": "required-file", "detail": f"empty text file: {relative}"})
        except (OSError, UnicodeError) as exc:
            violations.append({"rule": "required-file", "detail": f"unreadable UTF-8 text: {relative}: {exc}"})

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        try:
            text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            violations.append({"rule": "input-read", "detail": f"SKILL.md: {exc}"})
        else:
            check_frontmatter(text, "aai-cognitive-interface", violations)
            for marker in sorted(REQUIRED_SKILL_MARKERS):
                if marker not in text:
                    violations.append({"rule": "runtime-marker", "detail": marker})
            if "—" in text or "–" in text:
                violations.append({"rule": "dash", "detail": "SKILL.md contains em or en dash"})
            if len(text.splitlines()) > 500:
                violations.append({"rule": "size", "detail": "SKILL.md exceeds 500 lines"})
            for link in markdown_link_targets(text):
                target = link.split("#", 1)[0]
                if re.match(r"^file://", target, re.IGNORECASE):
                    violations.append({"rule": "linked-path", "detail": f"file URI is forbidden: {link}"})
                    continue
                if target and not re.match(r"^[a-z]+://", target, re.IGNORECASE):
                    try:
                        resolved = (root / target).resolve()
                        resolved.relative_to(root.resolve())
                    except (OSError, RuntimeError, ValueError):
                        violations.append({"rule": "linked-path", "detail": f"escapes package: {link}"})
                        continue
                    if not resolved.is_file():
                        violations.append({"rule": "linked-path", "detail": target})

    gate_script = root / "scripts/aai_runtime_gate.py"
    if gate_script.is_file():
        try:
            compile(gate_script.read_text(encoding="utf-8"), str(gate_script), "exec")
        except (OSError, UnicodeError, SyntaxError) as exc:
            violations.append({"rule": "python-parse", "detail": str(exc)})

    check_agent_metadata(root, "aai-cognitive-interface", violations)

    return result("package-aai", violations)


def check_generic_package(root: Path) -> int:
    violations: list[dict[str, str]] = []
    for relative in sorted(GENERIC_REQUIRED_FILES):
        required = root / relative
        if not required.is_file():
            violations.append({"rule": "required-file", "detail": relative})
            continue
        try:
            required.resolve().relative_to(root.resolve())
        except (OSError, RuntimeError, ValueError):
            violations.append({"rule": "required-file", "detail": f"escapes package: {relative}"})

    skill_path = root / "SKILL.md"
    name = skill_name(skill_path)
    if name is None:
        violations.append({"rule": "frontmatter", "detail": "name missing or invalid"})
    elif not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        violations.append({"rule": "frontmatter", "detail": f"invalid skill name: {name}"})
    elif root.name != name:
        violations.append({
            "rule": "package-identity",
            "detail": f"directory must be {name}, found {root.name}",
        })

    if skill_path.is_file():
        try:
            text = skill_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            violations.append({"rule": "input-read", "detail": f"SKILL.md: {exc}"})
        else:
            check_frontmatter(text, name, violations)
            if "—" in text or "–" in text:
                violations.append({"rule": "dash", "detail": "SKILL.md contains em or en dash"})
            if len(text.splitlines()) > 500:
                violations.append({"rule": "size", "detail": "SKILL.md exceeds 500 lines"})
            if name != "aai-cognitive-interface":
                flattened = " ".join(text.splitlines())
                for marker in sorted(SUBORDINATE_MARKERS):
                    if marker not in flattened:
                        violations.append({"rule": "aai-subordination", "detail": marker})

            for link in markdown_link_targets(text):
                target = link.split("#", 1)[0]
                if re.match(r"^file://", target, re.IGNORECASE):
                    violations.append({"rule": "linked-path", "detail": f"file URI is forbidden: {link}"})
                    continue
                if not target or re.match(r"^[a-z]+://", target, re.IGNORECASE):
                    continue
                try:
                    resolved = (root / target).resolve()
                    resolved.relative_to(root.resolve())
                except (OSError, RuntimeError, ValueError):
                    violations.append({"rule": "linked-path", "detail": f"escapes package: {link}"})
                    continue
                if not resolved.is_file():
                    violations.append({"rule": "linked-path", "detail": target})

    check_agent_metadata(root, name, violations)

    scripts = root / "scripts"
    if scripts.is_dir():
        for script in sorted(scripts.rglob("*.py")):
            try:
                compile(script.read_text(encoding="utf-8"), str(script), "exec")
            except (OSError, UnicodeError, SyntaxError) as exc:
                violations.append({"rule": "python-parse", "detail": f"{script.name}: {exc}"})

    return result("package-skill", violations)


def check_package(root: Path, requested_mode: str = "auto") -> int:
    name = skill_name(root / "SKILL.md")
    if name == "aai-cognitive-interface":
        return check_aai_package(root)
    if requested_mode == "aai":
        return result("package-aai", [{
            "rule": "mode-mismatch",
            "detail": "package is not aai-cognitive-interface",
        }])
    return check_generic_package(root)


def negated_claim(text: str, start: int, end: int) -> bool:
    prefix = text[max(0, start - 100):start]
    clause = re.split(
        r"[.!?;:,\n]|\b(?:and|but|yet)\b",
        prefix,
        flags=re.IGNORECASE,
    )[-1]
    direct_negative = re.compile(
        r"(?:"
        r"\bnot\b(?!\s+(?:only|just|merely|simply)\b)"
        r"|\b(?:does|do|did|is|are|was|were|has|have|had)\s+not\b"
        r"(?!\s+(?:only|just|merely|simply)\b)"
        r"|\b(?:doesn['’]?t|isn['’]?t|aren['’]?t|wasn['’]?t|weren['’]?t|"
        r"hasn['’]?t|haven['’]?t|hadn['’]?t|cannot|can['’]?t)\b"
        r"|\b(?:never|neither)\b"
        r"|\b(?:fail|fails|failed|failing)\s+to\b"
        r"|\b(?:no|without)\s+(?:evidence|proof|receipt|basis|support)\b"
        r"|\b(?:no|without)\s*$"
        r")[^.!?;:,\n]{0,70}$",
        re.IGNORECASE,
    )
    suffix = re.split(r"[.!?;\n]", text[end:], maxsplit=1)[0]
    postfix_negative = re.compile(
        r"^\s*[, :]?\s*(?:(?:but|and|yet)\s+)?"
        r"(?:"
        r"(?:(?:was|is|were|are|has|have|had)\s+)?(?:not|never)\s+"
        r"(?:achieved|established|awarded|reached|obtained|verified|supported|earned|met|attained)\b"
        r"|(?:failed|fails)\b"
        r")",
        re.IGNORECASE,
    )
    return bool(direct_negative.search(clause) or postfix_negative.search(suffix))


def claimed_statuses(text: str) -> set[str]:
    normalized = text.translate(STATUS_HYPHENS)
    claims = set()
    for label, pattern in STATUS_PATTERNS.items():
        for match in pattern.finditer(normalized):
            if not negated_claim(normalized, match.start(), match.end()):
                claims.add(label)
    return claims


def valid_base_receipt(entry) -> bool:
    if not isinstance(entry, dict) or entry.get("current_run") is not True:
        return False
    evidence = entry.get("evidence")
    structurally_valid = (
        isinstance(evidence, dict)
        and isinstance(evidence.get("kind"), str)
        and bool(evidence["kind"].strip())
        and isinstance(evidence.get("source"), str)
        and bool(evidence["source"].strip())
        and isinstance(evidence.get("detail"), str)
        and len(evidence["detail"].strip()) >= 12
    )
    if not structurally_valid:
        return False
    return True


def nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def exact_int(value) -> bool:
    return type(value) is int


def direct_nonempty_file(target) -> bool:
    if not nonempty_string(target):
        return False
    path = Path(target)
    if not path.is_absolute() or not path.is_file():
        return False
    try:
        if path.stat().st_size <= 0:
            return False
        with path.open("rb") as stream:
            return bool(stream.read(1))
    except OSError:
        return False


def direct_package_pass(target) -> bool:
    if not nonempty_string(target):
        return False
    path = Path(target)
    if not path.is_absolute() or not path.is_dir():
        return False
    try:
        completed = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "package", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return completed.returncode == 0


def receipt_defect(label: str, entry) -> str | None:
    if not valid_base_receipt(entry):
        return "requires current_run=true and structured evidence with kind, source, and detail"
    kind = entry["evidence"]["kind"]
    if label == "DRAFTED":
        if kind != "content" or entry.get("content_exists") is not True:
            return "requires content evidence and content_exists=true"
        if not direct_nonempty_file(entry.get("target")):
            return "target must be an absolute readable nonempty regular file verified by this invocation"
    elif label == "STATIC-PASS":
        if (
            kind != "validator"
            or entry.get("validator") != "aai-package"
            or not exact_int(entry.get("exit_code"))
            or entry["exit_code"] != 0
        ):
            return "requires validator='aai-package' and integer exit_code=0"
        if not direct_package_pass(entry.get("target")):
            return "declared absolute package target did not pass this invocation's allowlisted package validator"
    return None


def check_response(path: Path, evidence_path: Path | None = None) -> int:
    violations: list[dict[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return result("response", [{"rule": "input-read", "detail": str(exc)}])
    lower = text.lower()

    if "—" in text or "–" in text:
        violations.append({"rule": "dash", "detail": "response contains em or en dash"})
    for phrase, detail in PROHIBITED.items():
        if phrase in lower:
            violations.append({"rule": "prohibited-language", "detail": f"{phrase}: {detail}"})

    evidence = {}
    if evidence_path:
        try:
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            violations.append({"rule": "evidence-ledger", "detail": str(exc)})
            evidence = {}
        if not isinstance(evidence, dict):
            violations.append({"rule": "evidence-ledger", "detail": "ledger must be a JSON object"})
            evidence = {}

    for label in sorted(claimed_statuses(text)):
        if label in STANDALONE_UNVERIFIABLE:
            violations.append({
                "rule": "unverifiable-status",
                "detail": (f"{label}: a standalone linter cannot authenticate this operation or "
                           "runtime result from user-writable receipts; trusted controller evidence is required"),
            })
            continue
        defect = receipt_defect(label, evidence.get(label))
        if defect:
            violations.append({"rule": "status-evidence", "detail": f"{label}: {defect}"})

    return result("response", violations)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in ("package", "package-aai", "package-skill"):
        package = sub.add_parser(mode)
        package.add_argument("skill_directory", type=Path)
    response = sub.add_parser("response")
    response.add_argument("draft_file", type=Path)
    response.add_argument("--evidence-file", type=Path)
    args = parser.parse_args()

    if args.mode in {"package", "package-aai", "package-skill"}:
        requested = "auto" if args.mode == "package" else args.mode.removeprefix("package-")
        return check_package(args.skill_directory.resolve(), requested)
    return check_response(
        args.draft_file.resolve(),
        args.evidence_file.resolve() if args.evidence_file else None,
    )


if __name__ == "__main__":
    sys.exit(main())
