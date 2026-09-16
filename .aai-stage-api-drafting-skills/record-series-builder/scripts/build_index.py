#!/usr/bin/env python3
"""
build_index.py

Generates a master index.md across a multi-volume markdown series:
one entry per volume, linking to the volume file and its H2 sections,
plus the volume's handoff line if one is found.

Usage:
    python3 build_index.py vol1.md vol2.md vol3.md -o index.md
    python3 build_index.py --dir ./series --pattern "vol*.md" -o index.md

Volume order is the order files are given, or alphabetical within
--dir. The script reads only headings (# and ##) and a handoff line; it
does not rewrite the volume files.

A handoff line must use the anchored field `Handoff: ...`, name the actual
next volume, and describe what that volume covers or continues. Every
intermediate volume requires one. The final input volume must omit it.
"""

import argparse
import glob
import os
import re
import sys
import tempfile
from urllib.parse import quote

H1_RE = re.compile(r"^#\s+(.+)$")
H2_RE = re.compile(r"^##\s+(.+)$")
HANDOFF_RE = re.compile(r"^Handoff:\s*(.+)$", re.IGNORECASE)
VOLUME_ID_RE = re.compile(r"\bVolume\s+([A-Za-z0-9._-]+)\b", re.IGNORECASE)
COVERAGE_RE = re.compile(
    r"\b(?:cover(?:s|ed|ing)?|contain(?:s|ed|ing)?|continu(?:e|es|ed|ing)|"
    r"address(?:es|ed|ing)?|include(?:s|d|ing)?|present(?:s|ed|ing)?|"
    r"document(?:s|ed|ing)?|resume(?:s|d|ing)?|begin(?:s|ning)?|start(?:s|ed|ing)?|"
    r"focus(?:es|ed|ing)?|examine(?:s|d|ing)?|catalogue(?:s|d|ing)?)\b",
    re.IGNORECASE,
)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def markdown_label(text: str) -> str:
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]").replace("\n", " ")


def parse_volume(path: str):
    title = os.path.basename(path)
    sections = []
    handoff = None
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    content_lines = []
    in_fence = False
    fence_char = None
    fence_width = 0
    for line_number, line in enumerate(lines, 1):
        if in_fence:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_char)}{{{fence_width},}}[ \t]*$",
                line,
            )
            if closing:
                in_fence, fence_char, fence_width = False, None, 0
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening:
            marker = opening.group(1)
            info = opening.group(2)
            if marker[0] != "`" or "`" not in info:
                in_fence, fence_char, fence_width = True, marker[0], len(marker)
                continue
        if in_fence or line.startswith(("    ", "\t")):
            continue
        content_lines.append((line_number, line))
    unclosed_fence = in_fence

    for _line_number, line in content_lines:
        m1 = H1_RE.match(line)
        if m1 and title == os.path.basename(path):
            title = m1.group(1).strip()
            continue
        m2 = H2_RE.match(line)
        if m2:
            heading = m2.group(1).strip()
            sections.append((heading, slugify(heading)))

    handoff_matches = []
    for line_number, line in content_lines:
        match = HANDOFF_RE.match(line.rstrip())
        if match:
            handoff_matches.append((line_number, match.group(1).strip()))

    for _line_number, line in reversed(content_lines):
        stripped = line.strip()
        if not stripped:
            continue
        handoff_match = HANDOFF_RE.match(line.rstrip())
        if handoff_match:
            handoff = handoff_match.group(1).strip()
        break

    invalid_handoff_position = unclosed_fence or (
        bool(handoff_matches) and (handoff is None or len(handoff_matches) != 1)
    )
    return title, sections, handoff, invalid_handoff_position


def normalized_name(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def references_next_volume(handoff: str, next_path: str, next_title: str) -> bool:
    handoff_ids = {m.group(1).lower() for m in VOLUME_ID_RE.finditer(handoff)}
    next_ids = {m.group(1).lower() for m in VOLUME_ID_RE.finditer(next_title)}
    if next_ids:
        return bool(handoff_ids and handoff_ids == next_ids)
    handoff_tokens = normalized_name(handoff).split()
    candidates = [
        normalized_name(next_title).split(),
        normalized_name(os.path.splitext(os.path.basename(next_path))[0]).split(),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        width = len(candidate)
        if any(handoff_tokens[index:index + width] == candidate
               for index in range(len(handoff_tokens) - width + 1)):
            return True
    return False


def describes_coverage(handoff: str) -> bool:
    negative_to_coverage = re.compile(
        r"\b(?:fail(?:s|ed|ing)?|refuse(?:s|d|ing)?|decline(?:s|d|ing)?|unable)\b"
        r"[^.!?;:,\n]*\bto\s+"
        r"(?:cover(?:s|ed|ing)?|contain(?:s|ed|ing)?|continu(?:e|es|ed|ing)|"
        r"address(?:es|ed|ing)?|include(?:s|d|ing)?|present(?:s|ed|ing)?|"
        r"document(?:s|ed|ing)?|resume(?:s|d|ing)?|begin(?:s|ning)?|start(?:s|ed|ing)?|"
        r"focus(?:es|ed|ing)?|examine(?:s|d|ing)?|catalogue(?:s|d|ing)?)\b",
        re.IGNORECASE,
    )
    if negative_to_coverage.search(handoff):
        return False
    match = COVERAGE_RE.search(handoff)
    if not match:
        return False
    prefix = handoff[:match.start()]
    if re.search(
        r"\b(?:not(?!\s+(?:only|just|merely|simply)\b)|never|neither|cannot|can['’]?t|hardly|barely)\b"
        r"|\bdoesn['’]?t\b(?!\s+(?:only|just|merely|simply)\b)"
        r"|\bdoes\s+not\b(?!\s+(?:only|just|merely|simply)\b)"
        r"|\b(?:fail(?:s|ed|ing)?|refuse(?:s|d|ing)?|decline(?:s|d|ing)?|unable)\b"
        r"[^.!?;:,\n]*\bto\s*$",
        prefix,
        re.IGNORECASE,
    ):
        return False
    remainder = handoff[match.end():].strip(" .,:;-")
    if not remainder or re.match(r"^(?:no|none|nothing)\b", remainder, re.IGNORECASE):
        return False
    meaningful = [token for token in re.findall(r"[a-z0-9]+", remainder.lower())
                  if token not in {"the", "a", "an", "of", "in", "on", "with", "and", "to"}]
    return bool(meaningful)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", help="Volume markdown files, in order")
    parser.add_argument("--dir", help="Directory to glob for volume files")
    parser.add_argument("--pattern", default="*.md",
                         help="Glob pattern when using --dir (default *.md)")
    parser.add_argument("-o", "--output", help="Write to this path instead of stdout")
    parser.add_argument("--title", default="Series Index",
                         help="Title for the generated index")
    args = parser.parse_args()

    files = list(args.files)
    if args.dir:
        files.extend(sorted(glob.glob(os.path.join(args.dir, args.pattern))))

    if not files:
        print("No volume files given.", file=sys.stderr)
        sys.exit(1)

    resolved_inputs = [os.path.realpath(path) for path in files]
    if len(resolved_inputs) != len(set(resolved_inputs)):
        print("ERROR: the same volume input was specified more than once", file=sys.stderr)
        sys.exit(2)

    if args.output:
        output_path = os.path.abspath(args.output)
        if os.path.islink(output_path):
            print("ERROR: output path must not be a symbolic link", file=sys.stderr)
            sys.exit(2)
        overlapping = []
        for path in files:
            if os.path.abspath(path) == output_path:
                overlapping.append(path)
                continue
            if os.path.exists(output_path):
                try:
                    if os.path.samefile(path, output_path):
                        overlapping.append(path)
                except OSError:
                    pass
        if overlapping:
            print(f"ERROR: output path overlaps input volume: {overlapping[0]}", file=sys.stderr)
            sys.exit(2)

    try:
        parsed = [(path, *parse_volume(path)) for path in files]
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read volume input: {exc}", file=sys.stderr)
        sys.exit(2)
    errors = []
    for index, (path, _title, _sections, handoff, invalid_handoff) in enumerate(parsed[:-1]):
        next_path, next_title, _next_sections, _next_handoff, _next_invalid = parsed[index + 1]
        if invalid_handoff:
            errors.append(f"{path}: Handoff must appear exactly once as the final substantive line")
        elif not handoff:
            errors.append(f"{path}: missing anchored Handoff field")
        elif not references_next_volume(handoff, next_path, next_title):
            errors.append(f"{path}: handoff does not name next volume '{next_title}'")
        elif not describes_coverage(handoff):
            errors.append(f"{path}: handoff names the next volume but does not describe its coverage")
    final_path, _final_title, _final_sections, final_handoff, final_invalid_handoff = parsed[-1]
    if final_handoff or final_invalid_handoff:
        errors.append(f"{final_path}: final input volume must not contain a Handoff field")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    link_base = os.path.dirname(os.path.abspath(args.output)) if args.output else os.getcwd()
    out = [f"# {args.title.replace(chr(10), ' ')}", ""]
    for path, title, sections, handoff, _invalid_handoff in parsed:
        rel = os.path.relpath(os.path.abspath(path), link_base).replace(os.sep, "/")
        encoded_rel = quote(rel, safe="/._-~")
        out.append(f"## [{markdown_label(title)}]({encoded_rel})")
        for heading, slug in sections:
            out.append(f"- [{markdown_label(heading)}]({encoded_rel}#{slug})")
        if handoff:
            out.append("")
            out.append(f"Handoff: {handoff}")
        out.append("")

    text = "\n".join(out)
    if args.output:
        output_path = os.path.abspath(args.output)
        output_dir = os.path.dirname(output_path)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=output_dir, prefix=".build-index-", delete=False
            ) as stream:
                temporary_path = stream.name
                stream.write(text + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_path, output_path)
        except OSError as exc:
            if temporary_path:
                try:
                    os.unlink(temporary_path)
                except OSError:
                    pass
            print(f"ERROR: cannot write index: {exc}", file=sys.stderr)
            sys.exit(2)
        print(f"Wrote {args.output} ({len(files)} volume(s)).")
    else:
        print(text)


if __name__ == "__main__":
    main()
