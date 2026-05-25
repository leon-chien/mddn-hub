#!/usr/bin/env python3
"""Build the MDDataNet Hub dataset registry index."""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

from validate_entry import (
    REPO_ROOT,
    ValidationError,
    load_json,
    load_yaml,
    validate_entry,
)


DATASETS_DIR = REPO_ROOT / "datasets"
REGISTRY_DIR = REPO_ROOT / "registry"
INDEX_PATH = REGISTRY_DIR / "index.json"
INDEX_SCHEMA_VERSION = "0.1.0"


def dataset_entries() -> list[Path]:
    if not DATASETS_DIR.is_dir():
        raise ValidationError("datasets/ directory does not exist")
    entries = sorted(path for path in DATASETS_DIR.iterdir() if path.is_dir())
    if not entries:
        raise ValidationError("no dataset entries found under datasets/")
    return entries


def package_url(downloads: object, entry_dir: Path) -> str:
    if not isinstance(downloads, dict):
        raise ValidationError(f"{entry_dir}: download.yaml root must be a mapping")
    package = downloads.get("package")
    if not isinstance(package, dict):
        raise ValidationError(f"{entry_dir}: download.yaml must include package asset")
    url = package.get("url")
    if not isinstance(url, str) or not url:
        raise ValidationError(f"{entry_dir}: download.yaml package.url is required")
    return url


def index_record(entry_dir: Path) -> dict[str, object]:
    validate_entry(entry_dir)
    metadata = load_json(entry_dir / "metadata.json")
    downloads = load_yaml(entry_dir / "download.yaml")
    if not isinstance(metadata, dict):
        raise ValidationError(f"{entry_dir}: metadata.json root must be an object")

    task = metadata.get("task")
    system = metadata.get("system")
    if not isinstance(task, dict):
        raise ValidationError(f"{entry_dir}: metadata.task must be an object")
    if not isinstance(system, dict):
        raise ValidationError(f"{entry_dir}: metadata.system must be an object")

    return {
        "dataset_id": metadata["dataset_name"],
        "version": metadata["version"],
        "task_type": task["task_type"],
        "target_event": task["target_event"],
        "horizon_frames": task.get("horizon_frames"),
        "system_type": system["system_type"],
        "storage_profile": metadata["storage_profile"],
        "license": metadata["license"],
        "package_url": package_url(downloads, entry_dir),
    }


def build_index() -> dict[str, object]:
    records = [index_record(entry) for entry in dataset_entries()]
    records.sort(key=lambda record: str(record["dataset_id"]))
    return {
        "schema_version": INDEX_SCHEMA_VERSION,
        "datasets": records,
    }


def render_index(index: dict[str, object]) -> str:
    return json.dumps(index, indent=2, sort_keys=False) + "\n"


def write_index() -> None:
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(render_index(build_index()), encoding="utf-8")
    print(f"Wrote {INDEX_PATH.relative_to(REPO_ROOT)}")


def check_index() -> int:
    expected = render_index(build_index())
    if not INDEX_PATH.exists():
        print("ERROR: registry/index.json is missing", file=sys.stderr)
        return 1
    actual = INDEX_PATH.read_text(encoding="utf-8")
    if actual != expected:
        print("ERROR: registry/index.json is stale", file=sys.stderr)
        diff = difflib.unified_diff(
            actual.splitlines(),
            expected.splitlines(),
            fromfile="registry/index.json",
            tofile="expected registry/index.json",
            lineterm="",
        )
        for line in diff:
            print(line, file=sys.stderr)
        return 1
    print("OK: registry/index.json")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if registry/index.json is missing or stale",
    )
    args = parser.parse_args(argv)

    try:
        if args.check:
            return check_index()
        write_index()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
