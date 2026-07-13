#!/usr/bin/env python3
"""Download fine-tuned Biohub U-Net weights from Kaggle datasets."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DATASETS = (
    ("aashishnegi23/cellmot-ft-detector-biohub", "cellmot-ft-detector-biohub"),
    ("thibautgoldsborough/cellmot-baseline-artifacts", "cellmot-baseline-artifacts"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(r"D:\Kaggle_Biohub_Data\cellmot"),
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    for slug, name in DATASETS:
        dest = args.out / name
        if (dest / "edge_predictor_best.pth").exists() or list(dest.glob("**/edge_predictor_best.pth")):
            print(f"[skip] {name} — weights present")
            continue
        print(f"[download] {slug} -> {dest}")
        subprocess.run(
            ["kaggle", "datasets", "download", "-d", slug, "-p", str(dest), "--unzip"],
            check=False,
        )
    hits = list(args.out.glob("**/edge_predictor_best.pth"))
    print(f"found {len(hits)} edge_predictor_best.pth file(s)")
    for h in hits:
        print(f"  {h}")
    return 0 if hits else 1


if __name__ == "__main__":
    raise SystemExit(main())