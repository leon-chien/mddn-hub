#!/usr/bin/env python3
"""Validate all MDDataNet Hub dataset entries."""

from __future__ import annotations

import sys
from pathlib import Path

from validate_entry import REPO_ROOT, ValidationError, validate_entry


DATASETS_DIR = REPO_ROOT / "datasets"


def main() -> int:
    if not DATASETS_DIR.is_dir():
        print("ERROR: datasets/ directory does not exist", file=sys.stderr)
        return 1

    entries = sorted(path for path in DATASETS_DIR.iterdir() if path.is_dir())
    if not entries:
        print("ERROR: no dataset entries found under datasets/", file=sys.stderr)
        return 1

    failures = 0
    for entry in entries:
        try:
            validate_entry(entry)
        except ValidationError as exc:
            failures += 1
            print(f"ERROR: {entry.relative_to(REPO_ROOT)}\n{exc}", file=sys.stderr)
        else:
            print(f"OK: {entry.relative_to(REPO_ROOT)}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
