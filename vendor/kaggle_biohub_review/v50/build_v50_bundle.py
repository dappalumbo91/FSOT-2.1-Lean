#!/usr/bin/env python3
"""Package v50 Python sources for Kaggle dataset fsot-v50-competitive-bundle."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTRACTED = ROOT.parent / "extracted"
OUT_DIR = ROOT / "fsot-v50-competitive-bundle"
ZIP_PATH = ROOT / "fsot-v50-competitive-bundle.zip"

BUNDLE_FILES = [
    "kaggle_main_runner.py",
    "biohub_unet_engine.py",
    "biohub_competitive.py",
    "fsot_division_ml_refine.py",
    "fsot_cellular_bridge.py",
    "fsot_core.py",
    "fsot_living_emergence.py",
    "fsot_vision_calibrate.py",
    "fsot_original_competition.py",
    "submission_io.py",
    "validate_kaggle_submission.py",
    "csv_to_geffs.py",
    "download_ft_weights.py",
    "kaggle_wheel_bootstrap.py",
]


def main() -> int:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    missing: list[str] = []
    for name in BUNDLE_FILES:
        src = ROOT / name
        if not src.exists():
            missing.append(name)
            continue
        shutil.copy2(src, OUT_DIR / name)
        print(f"  {name}")

    if missing:
        raise SystemExit(f"Missing bundle files: {missing}")

    cellmot_zip = EXTRACTED / "cellmot_code_bundle.zip"
    if cellmot_zip.exists():
        shutil.copy2(cellmot_zip, OUT_DIR / "cellmot_code_bundle.zip")
        print("  cellmot_code_bundle.zip")
    else:
        raise SystemExit(f"Missing {cellmot_zip}")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT_DIR.iterdir()):
            zf.write(path, arcname=path.name)

    print(f"\nBundle: {OUT_DIR} ({len(BUNDLE_FILES)} files)")
    print(f"Zip:    {ZIP_PATH} ({ZIP_PATH.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())