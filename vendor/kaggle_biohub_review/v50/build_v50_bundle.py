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
PATCHED_PREDICT = ROOT / "kaggle-cell-tracking-competition" / "scripts" / "predict_unet_transformer.py"

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
    if not cellmot_zip.exists():
        raise SystemExit(f"Missing {cellmot_zip}")
    if not PATCHED_PREDICT.exists():
        raise SystemExit(f"Missing patched predict script: {PATCHED_PREDICT}")

    staging = ROOT / "_cellmot_bundle_staging"
    if staging.exists():
        shutil.rmtree(staging)
    with zipfile.ZipFile(cellmot_zip, "r") as zf:
        zf.extractall(staging)
    bundle_predict = staging / "cellmot_bundle" / "scripts" / "predict_unet_transformer.py"
    if not bundle_predict.parent.exists():
        raise SystemExit(f"Unexpected cellmot zip layout (no {bundle_predict.parent})")
    shutil.copy2(PATCHED_PREDICT, bundle_predict)
    out_cellmot_zip = OUT_DIR / "cellmot_code_bundle.zip"
    with zipfile.ZipFile(out_cellmot_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(staging).as_posix())
    shutil.rmtree(staging)
    print("  cellmot_code_bundle.zip (patched predict_unet_transformer)")

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