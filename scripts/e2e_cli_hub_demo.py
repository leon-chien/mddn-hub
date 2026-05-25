#!/usr/bin/env python3
"""Run a local CLI-to-Hub-to-loader proof in a temporary workspace."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from validate_entry import REPO_ROOT, validate_entry

import build_index as index_builder


DATASET_ID = "ligand_unbinding_demo_e2e"
TARGET = "ligand_unbinding_future_2"


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def cli_env(cli_repo: Path) -> dict[str, str]:
    env = os.environ.copy()
    src_path = str(cli_repo / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing else f"{src_path}{os.pathsep}{existing}"
    return env


def build_temp_index(overlay_root: Path) -> None:
    registry_dir = overlay_root / "registry"
    index_path = registry_dir / "index.json"
    registry_dir.mkdir(parents=True, exist_ok=True)

    original_datasets_dir = index_builder.DATASETS_DIR
    original_registry_dir = index_builder.REGISTRY_DIR
    original_index_path = index_builder.INDEX_PATH
    try:
        index_builder.DATASETS_DIR = overlay_root / "datasets"
        index_builder.REGISTRY_DIR = registry_dir
        index_builder.INDEX_PATH = index_path
        index = index_builder.build_index()
        expected = index_builder.render_index(index)
        index_path.write_text(expected, encoding="utf-8")
        if index_path.read_text(encoding="utf-8") != expected:
            raise RuntimeError("temporary registry index check failed")
        print(f"OK: temporary {index_path.relative_to(overlay_root)}")
    finally:
        index_builder.DATASETS_DIR = original_datasets_dir
        index_builder.REGISTRY_DIR = original_registry_dir
        index_builder.INDEX_PATH = original_index_path


def load_first_item(cli_repo: Path, package_path: Path) -> tuple[tuple[int, ...], bool, bool]:
    sys.path.insert(0, str(cli_repo / "src"))
    from mddatanet import MDDataNetDataset

    with MDDataNetDataset(package_path, window_length=2, target=TARGET) as dataset:
        item = dataset[0]
        return tuple(item["coordinates"].shape), bool(item["label"]), bool(item["valid"])


def run_demo(*, cli_repo: Path, work_dir: Path, python: Path) -> None:
    if not cli_repo.exists():
        raise FileNotFoundError(f"CLI repo not found: {cli_repo}")

    env = cli_env(cli_repo)
    cli_outputs = work_dir / "cli_outputs"
    hub_entry = work_dir / "hub_entry"
    overlay_root = work_dir / "hub_overlay"
    overlay_datasets = overlay_root / "datasets"
    overlay_entry = overlay_datasets / DATASET_ID

    run(
        [str(python), "-m", "mddatanet.cli", "demo", "--out-dir", str(cli_outputs)],
        cwd=cli_repo,
        env=env,
    )
    package_path = cli_outputs / "ligand_unbinding_demo.mddatanet.zip"

    run(
        [
            str(python),
            "-m",
            "mddatanet.cli",
            "export-manifest",
            str(package_path),
            "--out",
            str(hub_entry),
            "--dataset-id",
            DATASET_ID,
            "--overwrite",
        ],
        cwd=cli_repo,
        env=env,
    )

    shutil.copytree(REPO_ROOT / "datasets", overlay_datasets)
    shutil.copytree(hub_entry, overlay_entry)
    validate_entry(overlay_entry)
    print(f"OK: validated temporary Hub entry {overlay_entry}")

    build_temp_index(overlay_root)

    shape, label, valid = load_first_item(cli_repo, package_path)
    exported_files = ", ".join(sorted(path.name for path in hub_entry.iterdir()))

    print("\nMDDataNet ecosystem proof complete")
    print(f"package: {package_path}")
    print(f"exported files: {exported_files}")
    print("hub validation: OK")
    print("temporary index: OK")
    print(f"loader item: coordinates_shape={shape} label={label} valid={valid}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cli-repo",
        type=Path,
        default=REPO_ROOT.parent / "mddn-cli",
        help="Path to the sibling mddatanet CLI repository.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=None,
        help="Optional workspace. A temporary directory is used by default.",
    )
    parser.add_argument(
        "--python",
        type=Path,
        default=Path(sys.executable),
        help="Python executable to use for CLI commands.",
    )
    parser.add_argument(
        "--keep-work-dir",
        action="store_true",
        help="Keep the temporary workspace for inspection.",
    )
    args = parser.parse_args(argv)

    if args.work_dir is not None:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        run_demo(
            cli_repo=args.cli_repo.resolve(),
            work_dir=args.work_dir.resolve(),
            python=args.python,
        )
        return 0

    with tempfile.TemporaryDirectory(prefix="mddatanet-e2e-") as tmp:
        work_dir = Path(tmp)
        run_demo(cli_repo=args.cli_repo.resolve(), work_dir=work_dir, python=args.python)
        if args.keep_work_dir:
            kept = Path(tempfile.mkdtemp(prefix="mddatanet-e2e-kept-"))
            shutil.copytree(work_dir, kept, dirs_exist_ok=True)
            print(f"kept work dir: {kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
