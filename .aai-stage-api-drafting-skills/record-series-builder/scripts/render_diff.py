#!/usr/bin/env python3
"""
render_diff.py

Post-render invariance check for record-series-builder. Confirms that a
rendered docx or PDF volume carries the same content as its audited
markdown source, so post-audit mutation cannot ship silently.

The comparison normalizes both sides to semantic tokens and reports token runs
present on one side but not the other. Numeric signs, decimals, percentages,
and currency symbols remain content because stripping them can reverse
meaning. Formatting-only differences produce no findings. Content deltas are
routed to review; this script never decides which side is correct.

Extraction:
  .docx  stdlib only: reads word/document.xml from the archive.
  .pdf   tries pdftotext (poppler), then the pypdf module. If neither
         is available, exits 2 with a stated limitation, per
         record-series-builder's rule that a skipped check is labeled,
         never silent.

Usage:
    python3 render_diff.py SOURCE.md RENDERED.docx
    python3 render_diff.py SOURCE.md RENDERED.pdf

Exit codes: 0 content-equivalent, 1 content delta found, 2 extraction,
tooling, format, or input failure.
"""

import difflib
import html
import os
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

TAG = re.compile(r"<[^>]+>")
MD_SYNTAX = re.compile(r"(```.*?```|`[^`]*`|!\[[^\]]*\]\([^)]*\)|\[([^\]]*)\]\([^)]*\)|[#>*_|:]+)", re.S)
TOKEN = re.compile(
    r"[+\-\u2212]?[$\u00a3\u20ac]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?:%|[a-z]+)?"
    r"|[a-z]+(?:['\u2019][a-z]+)?|[$\u00a3\u20ac\u00a7]",
    re.IGNORECASE,
)


class ExtractionError(Exception):
    """Rendered/source content could not be extracted reliably."""


def semantic_tokens(text):
    text = text.lower().replace("\u2212", "-")
    number = r"[$\u00a3\u20ac]?\s*(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?:%|[a-z]+)?"
    text = re.sub(rf"\(\s*({number})\s*\)", lambda match: "-" + re.sub(r"\s+", "", match.group(1)), text)
    numeric_start = r"(?:[$\u00a3\u20ac]\s*)?(?:\d|\.\d)"
    text = re.sub(
        rf"(?<=[a-z0-9)\]}}:=,])\s+([+\-])\s+(?={numeric_start})",
        r" \1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(rf"(?<=[(\[{{])([+\-])\s+(?={numeric_start})", r"\1", text)
    text = re.sub(r"([+\-])\s*([$\u00a3\u20ac])\s*(?=(?:\d|\.\d))", r"\1\2", text)
    text = re.sub(r"([$\u00a3\u20ac])\s*([+\-])\s*(?=(?:\d|\.\d))", r"\2\1", text)
    text = re.sub(r"([$\u00a3\u20ac])\s+(?=(?:\d|\.\d))", r"\1", text)
    trailing_amount = rf"(?:[$\u00a3\u20ac]\s*{number}|{number})"
    text = re.sub(
        rf"(?<![a-z0-9])({trailing_amount})\s*([+\-])(?=\s|[.,;:)\]}}]|$)",
        lambda match: match.group(2) + re.sub(r"\s+", "", match.group(1)),
        text,
        flags=re.IGNORECASE,
    )
    return TOKEN.findall(text)


def tokens_from_markdown(path):
    text = html.unescape(open(path, encoding="utf-8").read())
    text = MD_SYNTAX.sub(lambda m: m.group(2) or " ", text)
    return semantic_tokens(text)


def tokens_from_docx(path):
    with zipfile.ZipFile(path) as z:
        try:
            document_root = ET.fromstring(z.read("word/document.xml"))
        except (UnicodeError, ET.ParseError) as exc:
            raise ExtractionError(f"invalid XML in word/document.xml: {exc}") from exc
        relationship_attribute = (
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        )
        word_id_attribute = (
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id"
        )
        referenced_ids = {"header": [], "footer": []}
        referenced_notes = {"footnote": [], "endnote": []}
        for element in document_root.iter():
            reference_kind = element.tag.rsplit("}", 1)[-1]
            kind = {"headerReference": "header", "footerReference": "footer"}.get(reference_kind)
            if kind is not None:
                relationship_id = element.attrib.get(relationship_attribute)
                if relationship_id and relationship_id not in referenced_ids[kind]:
                    referenced_ids[kind].append(relationship_id)
                continue
            note_kind = {"footnoteReference": "footnote", "endnoteReference": "endnote"}.get(
                reference_kind
            )
            if note_kind is not None:
                note_id = element.attrib.get(word_id_attribute)
                if note_id and note_id not in referenced_notes[note_kind]:
                    referenced_notes[note_kind].append(note_id)

        relationship_targets = {}
        note_targets = {}
        if any(referenced_ids.values()) or any(referenced_notes.values()):
            try:
                relationships_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
            except (KeyError, UnicodeError, ET.ParseError) as exc:
                raise ExtractionError(f"invalid document relationships: {exc}") from exc
            for relationship in relationships_root.iter():
                if relationship.tag.rsplit("}", 1)[-1] != "Relationship":
                    continue
                if relationship.attrib.get("TargetMode", "Internal") != "Internal":
                    continue
                relationship_id = relationship.attrib.get("Id")
                target = relationship.attrib.get("Target")
                relationship_type = relationship.attrib.get("Type", "")
                if relationship_id and target:
                    if target.startswith("/"):
                        name = target.lstrip("/")
                    else:
                        name = posixpath.normpath(posixpath.join("word", target))
                    if not name.startswith("word/"):
                        raise ExtractionError(f"relationship target escapes word package: {target}")
                    relationship_targets[relationship_id] = name
                    if relationship_type.endswith("/footnotes"):
                        note_targets["footnote"] = name
                    elif relationship_type.endswith("/endnotes"):
                        note_targets["endnote"] = name

        def related_text(kind):
            parts = []
            for relationship_id in referenced_ids[kind]:
                name = relationship_targets.get(relationship_id)
                if not name:
                    raise ExtractionError(f"missing {kind} relationship: {relationship_id}")
                try:
                    root = ET.fromstring(z.read(name))
                except (KeyError, UnicodeError, ET.ParseError) as exc:
                    raise ExtractionError(f"invalid XML in {name}: {exc}") from exc
                parts.append(" ".join(root.itertext()))
            return parts

        def related_note_text(kind):
            requested = set(referenced_notes[kind])
            if not requested:
                return []
            name = note_targets.get(kind)
            if not name:
                raise ExtractionError(f"missing {kind} relationship")
            try:
                root = ET.fromstring(z.read(name))
            except (KeyError, UnicodeError, ET.ParseError) as exc:
                raise ExtractionError(f"invalid XML in {name}: {exc}") from exc
            parts = []
            found = set()
            for element in root:
                if element.tag.rsplit("}", 1)[-1] != kind:
                    continue
                note_id = element.attrib.get(word_id_attribute)
                if note_id in requested:
                    found.add(note_id)
                    parts.append(" ".join(element.itertext()))
            missing = sorted(requested - found)
            if missing:
                raise ExtractionError(f"missing referenced {kind}(s): {', '.join(missing)}")
            return parts

        visible_parts = related_text("header")
        visible_parts.append(" ".join(document_root.itertext()))
        visible_parts.extend(related_note_text("footnote"))
        visible_parts.extend(related_note_text("endnote"))
        visible_parts.extend(related_text("footer"))
    return semantic_tokens(" ".join(visible_parts))


def tokens_from_pdf(path):
    errors = []
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(
                ["pdftotext", path, "-"], capture_output=True, text=True
            )
            if out.returncode == 0:
                return semantic_tokens(out.stdout)
            errors.append(f"pdftotext exited {out.returncode}")
        except OSError as exc:
            errors.append(f"pdftotext failed: {exc}")
    try:
        from pypdf import PdfReader
    except ImportError:
        errors.append("pypdf is unavailable")
    else:
        try:
            text = " ".join((page.extract_text() or "") for page in PdfReader(path).pages)
            return semantic_tokens(text)
        except Exception as exc:
            errors.append(f"pypdf failed: {exc}")
    raise ExtractionError("; ".join(errors) or "no PDF extraction route succeeded")


def extract(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".markdown", ".txt"):
        return tokens_from_markdown(path)
    if ext == ".docx":
        return tokens_from_docx(path)
    if ext == ".pdf":
        return tokens_from_pdf(path)
    raise ExtractionError(f"unsupported format {ext or '(none)'}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src_path, rendered_path = sys.argv[1], sys.argv[2]
    if os.path.splitext(src_path)[1].lower() not in (".md", ".markdown", ".txt"):
        print("ERROR: source must be Markdown or plain text", file=sys.stderr)
        sys.exit(2)
    if os.path.splitext(rendered_path)[1].lower() not in (".docx", ".pdf"):
        print("ERROR: rendered target must be DOCX or PDF", file=sys.stderr)
        sys.exit(2)
    try:
        src = extract(src_path)
        rnd = extract(rendered_path)
    except (ExtractionError, OSError, UnicodeError, zipfile.BadZipFile, KeyError) as exc:
        print(f"ERROR: invariance extraction failed: {exc}", file=sys.stderr)
        sys.exit(2)

    sm = difflib.SequenceMatcher(a=src, b=rnd, autojunk=False)
    deltas = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == "equal":
            continue
        lost = " ".join(src[a1:a2])
        gained = " ".join(rnd[b1:b2])
        if lost:
            deltas.append(("MISSING FROM RENDER", lost[:160]))
        if gained:
            deltas.append(("ADDED IN RENDER", gained[:160]))

    for kind, run in deltas:
        print(f"DELTA ({kind}): {run}")
    ratio = sm.ratio()
    print(f"\nSummary: {len(deltas)} content delta(s), similarity {ratio:.4f}, "
          f"{'CONTENT-EQUIVALENT' if not deltas else 'RE-AUDIT CHANGED PASSAGES'}")
    sys.exit(1 if deltas else 0)


if __name__ == "__main__":
    main()
