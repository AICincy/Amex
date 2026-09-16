#!/usr/bin/env python3
"""
inventory.py

Scans a directory and produces the inventory table record-series-builder
requires before proposing any volume architecture: sources, outputs,
scripts, and stale residue.

Usage:
    python3 inventory.py DIRECTORY
    python3 inventory.py DIRECTORY --recursive
    python3 inventory.py DIRECTORY --recursive --flag-pattern "(?i)(draft|backup)"

Output is a markdown table (Path, Type, Size, Modified, Flags) plus a
summary count by file type. The Flags column marks likely stale or
duplicate residue using the default pattern below, or a pattern you
supply. Flagged files are not removed. Per record-series-builder's
rules, flagged items go to the user for approval before removal.
"""

import argparse
import hashlib
import os
import re
import stat
import sys
from datetime import datetime, timezone

DEFAULT_FLAG_PATTERN = r"(?i)(draft|old|copy|tmp|temp|backup|_v\d+|\(\d+\)|~$|\.bak$)"


def hash_record(path: str):
    digest = hashlib.sha256()
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise OSError(f"not a regular file: {path}")
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
        after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns
    ):
        raise OSError(f"file changed while inventorying: {path}")
    path_after = os.stat(path, follow_symlinks=False)
    if (after.st_dev, after.st_ino) != (path_after.st_dev, path_after.st_ino):
        raise OSError(f"file path was replaced while inventorying: {path}")
    return digest.hexdigest(), after


def md_escape(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024:
            return f"{num:.0f}{unit}" if unit == "B" else f"{num:.1f}{unit}"
        num /= 1024
    return f"{num:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--flag-pattern", default=DEFAULT_FLAG_PATTERN,
                         help="Regex for flagging likely stale/duplicate files")
    args = parser.parse_args()

    try:
        flag_re = re.compile(args.flag_pattern)
    except re.error as exc:
        print(f"ERROR: invalid flag pattern: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    root = args.directory
    if not os.path.isdir(root):
        print(f"ERROR: inventory root is not a readable directory: {root}", file=sys.stderr)
        raise SystemExit(2)

    rows = []
    try:
        if args.recursive:
            for dirpath, _dirs, names in os.walk(root):
                for name in names:
                    rows.append(os.path.join(dirpath, name))
        else:
            for name in sorted(os.listdir(root)):
                full = os.path.join(root, name)
                if os.path.isfile(full):
                    rows.append(full)
    except OSError as exc:
        print(f"ERROR: cannot inventory {root}: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    rows.sort()
    ext_counts = {}
    hash_groups = {}
    records = {}
    read_errors = {}
    for path in rows:
        try:
            digest, file_stat = hash_record(path)
        except OSError as exc:
            read_errors[path] = str(exc)
            continue
        records[path] = file_stat
        hash_groups.setdefault(digest, []).append(path)

    duplicates = {}
    for paths in hash_groups.values():
        if len(paths) < 2:
            continue
        canonical = min(paths, key=lambda p: os.path.relpath(p, root))
        canonical_rel = os.path.relpath(canonical, root)
        for path in paths:
            duplicates[path] = canonical_rel

    print("| Path | Type | Size | Modified (UTC) | Flags |")
    print("|---|---|---|---|---|")
    for path in rows:
        rel = os.path.relpath(path, root)
        ext = os.path.splitext(path)[1].lstrip(".").lower() or "(none)"
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
        file_stat = records.get(path)
        if file_stat is None:
            print(f"| {md_escape(rel)} | {md_escape(ext)} | error | error | read-error |")
            continue
        try:
            current = os.stat(path, follow_symlinks=False)
        except OSError as exc:
            read_errors[path] = str(exc)
            print(f"| {md_escape(rel)} | {md_escape(ext)} | error | error | read-error |")
            continue
        if (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns, current.st_ctime_ns) != (
            file_stat.st_dev, file_stat.st_ino, file_stat.st_size, file_stat.st_mtime_ns, file_stat.st_ctime_ns
        ):
            read_errors[path] = "file changed after hashing"
            print(f"| {md_escape(rel)} | {md_escape(ext)} | error | error | changed-after-hash |")
            continue
        size = human_size(file_stat.st_size)
        mtime = datetime.fromtimestamp(file_stat.st_mtime, tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M"
        )
        flags = []
        if flag_re.search(rel):
            flags.append("stale-candidate")
        if path in duplicates:
            flags.append(f"duplicate-content:{duplicates[path]}")
        if path in read_errors:
            flags.append("read-error")
        print(f"| {md_escape(rel)} | {md_escape(ext)} | {size} | {mtime} | {md_escape(', '.join(flags))} |")

    print()
    print("## Summary by type")
    print()
    print("| Type | Count |")
    print("|---|---|")
    for ext, count in sorted(ext_counts.items()):
        print(f"| {md_escape(ext)} | {count} |")
    print()
    print(f"Total files: {len(rows)}")
    if read_errors:
        print(f"ERROR: {len(read_errors)} file(s) could not be read completely.", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
