#!/usr/bin/env python3
"""Download competition train GT + one test zarr dataset via Kaggle API."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

COMP = "biohub-cell-tracking-during-development"
PREFIXES = (
    "train/44b6_0113de3b.geff/",
    "train/44b6_0113de3b.zarr/",
    "test/44b6_0113de3b.zarr/",
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
        zip_path = dest.parent / Path(fname).name
        if zip_path.suffix == "" and (dest.parent / (Path(fname).name + ".zip")).exists():
            pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(r"D:\Kaggle_Biohub_Data"))
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args()
    files = _list_files()
    print(f"matched {len(files)} competition files")
    if args.list_only:
        for f in files[:20]:
            print(f"  {f}")
        if len(files) > 20:
            print(f"  ... +{len(files) - 20} more")
        return 0
    _download(files, args.out)
    print(f"done -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())