#!/usr/bin/env python3
"""
diff_timestamps.py

Compares every HH:MM:SS timestamp found in a draft against the
timestamps found in a ground-truth file (typically the matter file's
verified-facts section or a BWC overlay export), and produces a status
table in claim-source-auditor's output format.

Usage:
    python3 diff_timestamps.py DRAFT.md --ground-truth TRUTH.md
    python3 diff_timestamps.py DRAFT.md --ground-truth TRUTH.md --tolerance 10

Status assignment (per claim-source-auditor's taxonomy):
  - "verified": clock value matches and the surrounding event context links
    the draft row to the ground-truth row.
  - "conflicting": event context links the rows but the clock values differ
    within --tolerance seconds.
  - "manual review needed": a clock candidate exists but event context does
    not establish that both timestamps describe the same event.
  - "not found in searched sources": no ground-truth timestamp candidate is
    within tolerance.

Time proximity and lexical overlap never prove that two timestamps describe
the same event. Automatic linkage requires either the same explicit
`Event-ID:` or `Anchor-ID:` value in both rows, or exact normalized non-time
event text. Meaningful lexical similarity may nominate a manual-review
candidate but never verifies one; an unrelated shared clock is not a
candidate. A
consistent delta across multiple context-linked conflicts suggests a constant
offset; confirm against the source overlay before correcting either side.
"""

import argparse
import re
import sys

HHMMSS = re.compile(r"\b(\d{1,2}):(\d{2}):(\d{2})\b")
CONTEXT_TOKEN = re.compile(
    r"(?<![a-z0-9])[-+]?(?:[$\u00a3\u20ac]\s*)?"
    r"(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)%?"
    r"|[a-z]+(?:'[a-z]+)?",
    re.IGNORECASE,
)
ANCHOR = re.compile(
    r"\b(?:event-id|anchor-id)\s*[:=]\s*([a-z0-9._-]+)\b",
    re.IGNORECASE,
)
MANUAL_CANDIDATE_MIN = 0.4


def md_escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def to_seconds(h, m, s):
    h, m, s = int(h), int(m), int(s)
    if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
        return None
    return h * 3600 + m * 60 + s


def normalize_spaced_signs(text):
    text = text.replace("\u2212", "-")
    number = r"(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)"
    accounting = rf"[$\u00a3\u20ac]?\s*{number}%?"
    text = re.sub(
        rf"\(\s*({accounting})\s*\)",
        lambda match: "-" + re.sub(r"\s+", "", match.group(1)),
        text,
    )
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
    trailing_amount = rf"(?:[$\u00a3\u20ac]\s*{number}|{number})%?"
    return re.sub(
        rf"(?<![a-z0-9])({trailing_amount})\s*([+\-])(?=\s|[.,;:)\]}}]|$)",
        lambda match: match.group(2) + re.sub(r"\s+", "", match.group(1)),
        text,
        flags=re.IGNORECASE,
    )


def context_tokens(line):
    without_times = HHMMSS.sub(" ", normalize_spaced_signs(line.lower()))
    return set(CONTEXT_TOKEN.findall(without_times))


def anchors(line):
    return set(m.group(1).lower() for m in ANCHOR.finditer(line))


def normalized_context(line):
    without_times = HHMMSS.sub(" ", normalize_spaced_signs(line.lower()))
    without_anchors = ANCHOR.sub(" ", without_times)
    return " ".join(CONTEXT_TOKEN.findall(without_anchors))


def context_link(a, b):
    left_anchors, right_anchors = anchors(a), anchors(b)
    if left_anchors or right_anchors:
        return len(left_anchors) == 1 and left_anchors == right_anchors
    left, right = normalized_context(a), normalized_context(b)
    return bool(left and left == right)


def context_score(a, b):
    left, right = context_tokens(a), context_tokens(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def extract(path):
    """Returns list of (line_number, timestamp_str, seconds, line_text)."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            for m in HHMMSS.finditer(line):
                ts = m.group(0)
                results.append((i, ts, to_seconds(*m.groups()), line.strip()))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft")
    parser.add_argument("--ground-truth", required=True)
    parser.add_argument("--tolerance", type=int, default=10,
                         help="Seconds within which a near-match counts as conflicting, not not-found")
    args = parser.parse_args()

    try:
        draft_ts = extract(args.draft)
        truth_ts = extract(args.ground_truth)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read timestamp input: {exc}", file=sys.stderr)
        sys.exit(2)
    invalid_draft = [(ln, ts) for ln, ts, sec, _line in draft_ts if sec is None]
    invalid_truth = [(ln, ts) for ln, ts, sec, _line in truth_ts if sec is None]
    validation_errors = len(invalid_draft) + len(invalid_truth)
    for line_number, timestamp in invalid_draft:
        print(f"ERROR: draft line {line_number}: invalid HH:MM:SS value {timestamp}", file=sys.stderr)
    for line_number, timestamp in invalid_truth:
        print(f"ERROR: ground-truth line {line_number}: invalid HH:MM:SS value {timestamp}", file=sys.stderr)
    draft_ts = [row for row in draft_ts if row[2] is not None]
    truth_seconds = [(ln, ts, sec, line) for (ln, ts, sec, line) in truth_ts if sec is not None]

    print("| Claim ID | Claim text | Status | Source file | Source locator | Source excerpt | Basis note | Remediation note |")
    print("|---|---|---|---|---|---|---|---|")

    deltas = []
    verified_count = 0
    unresolved_count = 0
    for idx, (lineno, ts, sec, line) in enumerate(draft_ts, start=1):
        claim_id = f"T{idx}"
        claim_text = md_escape(f"{args.draft}:{lineno}: {line}")

        exact = [t for t in truth_seconds if t[2] == sec]
        linked_exact = [t for t in exact if context_link(line, t[3])]
        if len(linked_exact) == 1:
            verified_count += 1
            match_ln, match_ts, _msec, match_line = linked_exact[0]
            print(f"| {claim_id} | {claim_text} | verified | "
                  f"{md_escape(args.ground_truth)} | line {match_ln} | "
                  f"{md_escape(match_line)[:300]} | Clock value and stable event link match | |")
            continue
        if exact:
            unresolved_count += 1
            candidate = max(exact, key=lambda t: context_score(line, t[3]))
            match_ln, match_ts, _msec, match_line = candidate
            score = context_score(line, match_line)
            if score >= MANUAL_CANDIDATE_MIN:
                print(f"| {claim_id} | {claim_text} | manual review needed | "
                      f"{md_escape(args.ground_truth)} | line {match_ln} | "
                      f"{md_escape(match_line)[:300]} | Same clock value and similar context nominate "
                      f"a candidate but do not establish identity | Verify the event against the source overlay |")
            else:
                print(f"| {claim_id} | {claim_text} | not found in searched sources | "
                      f"{md_escape(args.ground_truth)} | | | Shared clock belongs to unrelated context; "
                      f"no linked event found | Verify against source overlay |")
            continue

        nearby = [t for t in truth_seconds if abs(t[2] - sec) <= args.tolerance]
        linked_nearby = [t for t in nearby if context_link(line, t[3])]
        nearest = min(linked_nearby, key=lambda t: abs(t[2] - sec), default=None)
        if nearest:
            unresolved_count += 1
            match_ln, match_ts, match_sec, match_line = nearest
            delta = match_sec - sec
            deltas.append(delta)
            print(f"| {claim_id} | {claim_text} | conflicting | "
                  f"{md_escape(args.ground_truth)} | line {match_ln} | "
                  f"{md_escape(match_line)[:300]} | Context-linked ground truth is "
                  f"{match_ts} ({delta:+d}s) | Check for constant-offset error |")
            continue

        if nearby:
            unresolved_count += 1
            candidate = max(nearby, key=lambda t: context_score(line, t[3]))
            match_ln, match_ts, _match_sec, match_line = candidate
            score = context_score(line, match_line)
            if score >= MANUAL_CANDIDATE_MIN:
                print(f"| {claim_id} | {claim_text} | manual review needed | "
                      f"{md_escape(args.ground_truth)} | line {match_ln} | "
                      f"{md_escape(match_line)[:300]} | Nearby clock value {match_ts} and similar "
                      f"context nominate a candidate but do not establish identity | Verify the event against the source overlay |")
            else:
                print(f"| {claim_id} | {claim_text} | not found in searched sources | "
                      f"{md_escape(args.ground_truth)} | | | Nearby clocks belong to unrelated context; "
                      f"no linked event found | Verify against source overlay |")
            continue

        unresolved_count += 1
        print(f"| {claim_id} | {claim_text} | not found in searched sources | "
              f"{md_escape(args.ground_truth)} | | | No ground-truth timestamp within "
              f"{args.tolerance}s | Verify against source overlay |")

    if deltas and len(set(deltas)) == 1 and len(deltas) >= 2:
        print()
        print(f"All {len(deltas)} conflicting timestamps share a constant "
              f"delta of {deltas[0]:+d}s. This is the signature of a "
              f"constant-offset error. Confirm against one anchor point in "
              f"the source overlay, then apply with "
              f"forensic-evidentiary-drafting's correct_timestamps.py "
              f"(--delta {deltas[0]:+d}).")

    print()
    status = "PASS" if unresolved_count == 0 and validation_errors == 0 else "REVIEW-REQUIRED"
    print(f"Summary: {verified_count} verified, {unresolved_count} unresolved, "
          f"{validation_errors} validation defect(s), {status}")
    sys.exit(1 if unresolved_count or validation_errors else 0)


if __name__ == "__main__":
    main()
