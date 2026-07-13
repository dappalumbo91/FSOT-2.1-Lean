#!/usr/bin/env python3
"""Download competition train GT + all four test zarr datasets via Kaggle API."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

COMP = "biohub-cell-tracking-during-development"

# All public test zarr + one train set for local proxy scoring
TEST_DATASETS = (
    "44b6_0113de3b",
    "44b6_0b24845f",
    "6bba_05b6850b",
    "6bba_05db0fb1",
)

PREFIXES = tuple(
    [f"train/{ds}.geff/" for ds in (TEST_DATASETS[0],)]
    + [f"train/{ds}.zarr/" for ds in (TEST_DATASETS[0],)]
    + [f"test/{ds}.zarr/" for ds in TEST_DATASETS]
)


def _list_files() -> list[str]:
    names: list[str] = []
    token = ""
    while True:
        cmd = ["kaggle", "competitions", "files", "-c", COMP, "--page-size", "300"]
        if token:
            cmd.extend(["--page-token", token])
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        token = ""
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Next Page Token = "):
                token = line.split("=", 1)[1].strip()
                continue
            if not line or line.startswith("name") or line.startswith("---"):
                continue
            name = line.split()[0]
            if any(name.startswith(p) for p in PREFIXES):
                names.append(name)
        if not token:
            break
    return sorted(set(names))


def _download(files: list[str], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, fname in enumerate(files, 1):
        dest = out_dir / fname
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[{i}/{len(files)}] {fname}")
        subprocess.run(
            ["kaggle", "competitions", "download", "-c", COMP, "-f", fname, "-p", str(dest.parent)],
            check=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(r"D:\Kaggle_Biohub_Data"))
    parser.add_argument("--list-only", action="store_true")
    parser.add_argument(
        "--test-datasets",
        nargs="*",
        default=list(TEST_DATASETS),
        help="Override test dataset ids (default: all four)",
    )
    args = parser.parse_args()

    global PREFIXES
    if args.test_datasets != list(TEST_DATASETS):
        PREFIXES = tuple(
            [f"train/{args.test_datasets[0]}.geff/"]
            + [f"train/{args.test_datasets[0]}.zarr/"]
            + [f"test/{ds}.zarr/" for ds in args.test_datasets]
        )

    files = _list_files()
    print(f"matched {len(files)} competition files")
    if args.list_only:
        for f in files[:30]:
            print(f"  {f}")
        if len(files) > 30:
            print(f"  ... +{len(files) - 30} more")
        return 0
    _download(files, args.out)
    print(f"done -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())