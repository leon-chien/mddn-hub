#!/usr/bin/env python3
"""Validate one MDDataNet Hub dataset entry."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by users
    missing = exc.name or "a required package"
    print(
        f"Missing validation dependency: {missing}. "
        "Install project dependencies from pyproject.toml.",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schemas"
REQUIRED_FILES = {
    "dataset_card.md",
    "metadata.json",
    "manifest.json",
    "download.yaml",
    "checksums.json",
}
LARGE_FILE_SUFFIXES = {
    ".mddatanet.zip",
    ".zarr.zip",
    ".xtc",
    ".dcd",
    ".trr",
    ".nc",
    ".h5",
    ".hdf5",
    ".pdb.gz",
}
LARGE_DIR_SUFFIXES = {
    ".zarr",
}


class ValidationError(Exception):
    """Raised when a dataset entry is invalid."""


def load_json(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def load_yaml(path: Path) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc


def load_schema(name: str) -> dict:
    schema = load_json(SCHEMA_DIR / name)
    if not isinstance(schema, dict):
        raise ValidationError(f"schemas/{name}: schema must be a JSON object")
    return schema


def schema_registry() -> Registry:
    schemas = {
        schema_path.name: load_schema(schema_path.name)
        for schema_path in SCHEMA_DIR.glob("*.schema.json")
    }
    resources = []
    for schema_id, schema in schemas.items():
        resource = Resource.from_contents(schema)
        resources.append((schema_id, resource))
        resources.append((schema.get("$id", schema_id), resource))
    return Registry().with_resources(resources)


def validate_schema(instance: object, schema_name: str, label: str) -> None:
    schema = load_schema(schema_name)
    validator = Draft202012Validator(
        schema,
        registry=schema_registry(),
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(instance), key=lambda err: err.path)
    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            messages.append(f"{label}: {location}: {error.message}")
        raise ValidationError("\n".join(messages))


def require_files(entry_dir: Path) -> None:
    missing = sorted(name for name in REQUIRED_FILES if not (entry_dir / name).is_file())
    if missing:
        raise ValidationError(
            f"{entry_dir}: missing required file(s): {', '.join(missing)}"
        )


def reject_large_artifacts(entry_dir: Path) -> None:
    offenders: list[str] = []
    for path in entry_dir.rglob("*"):
        rel = path.relative_to(entry_dir)
        name = path.name.lower()
        if path.is_dir() and any(name.endswith(suffix) for suffix in LARGE_DIR_SUFFIXES):
            offenders.append(str(rel))
        if path.is_file() and any(name.endswith(suffix) for suffix in LARGE_FILE_SUFFIXES):
            offenders.append(str(rel))
    if offenders:
        raise ValidationError(
            f"{entry_dir}: large data artifacts are not allowed: "
            + ", ".join(sorted(offenders))
        )


def validate_dataset_name(entry_dir: Path, metadata: object) -> None:
    if not isinstance(metadata, dict):
        raise ValidationError("metadata.json: root must be an object")
    dataset_name = metadata.get("dataset_name")
    if dataset_name != entry_dir.name:
        raise ValidationError(
            "metadata.json: dataset_name must match directory name "
            f"({dataset_name!r} != {entry_dir.name!r})"
        )


def validate_download_urls(downloads: object) -> None:
    if not isinstance(downloads, dict):
        raise ValidationError("download.yaml: root must be a mapping")
    for asset_name, asset in downloads.items():
        if not isinstance(asset, dict):
            raise ValidationError(f"download.yaml: {asset_name}: asset must be a mapping")
        url = asset.get("url")
        parsed = urlparse(url) if isinstance(url, str) else None
        if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValidationError(
                f"download.yaml: {asset_name}: url must be an absolute HTTP(S) URL"
            )


def validate_checksum_alignment(downloads: object, checksums: object) -> None:
    if not isinstance(downloads, dict) or not isinstance(checksums, dict):
        return
    missing = sorted(name for name in downloads if name not in checksums)
    if missing:
        raise ValidationError(
            "checksums.json: missing checksum entry for download asset(s): "
            + ", ".join(missing)
        )
    mismatched = []
    for name, asset in downloads.items():
        if not isinstance(asset, dict):
            continue
        checksum = checksums.get(name)
        if isinstance(checksum, dict) and checksum.get("sha256") != asset.get("sha256"):
            mismatched.append(name)
    if mismatched:
        raise ValidationError(
            "checksums.json: sha256 does not match download.yaml for asset(s): "
            + ", ".join(sorted(mismatched))
        )


def validate_entry(entry_dir: Path) -> None:
    if not entry_dir.is_dir():
        raise ValidationError(f"{entry_dir}: dataset entry directory does not exist")

    require_files(entry_dir)
    reject_large_artifacts(entry_dir)

    metadata = load_json(entry_dir / "metadata.json")
    manifest = load_json(entry_dir / "manifest.json")
    downloads = load_yaml(entry_dir / "download.yaml")
    checksums = load_json(entry_dir / "checksums.json")

    validate_schema(metadata, "metadata.schema.json", "metadata.json")
    validate_schema(manifest, "manifest.schema.json", "manifest.json")
    validate_schema(downloads, "download.schema.json", "download.yaml")
    validate_schema(checksums, "checksums.schema.json", "checksums.json")

    validate_dataset_name(entry_dir, metadata)
    validate_download_urls(downloads)
    validate_checksum_alignment(downloads, checksums)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_entry.py datasets/<dataset_name>", file=sys.stderr)
        return 2

    entry_dir = Path(argv[1]).resolve()
    try:
        validate_entry(entry_dir)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OK: {entry_dir.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
