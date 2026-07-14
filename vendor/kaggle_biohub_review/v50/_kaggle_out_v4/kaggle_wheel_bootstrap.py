"""Offline wheel bootstrap for Kaggle CPU notebooks (avoids numpy/scipy breakage)."""

from __future__ import annotations

import glob
import os
import subprocess
import zipfile
from pathlib import Path


def install_cellmot_wheels() -> str | None:
    """Install cellmot offline wheels except numpy/scipy (Kaggle base image keeps those)."""
    hits = glob.glob("/kaggle/input/**/cellmot-baseline-artifacts/**/wheels", recursive=True)
    if not hits:
        hits = glob.glob("/kaggle/input/**/wheels", recursive=True)
    if not hits:
        print("CRITICAL: cellmot wheels dir not found")
        return None

    wheel_dir = hits[0]
    skip = ("numpy-", "scipy-")
    for whl in sorted(glob.glob(f"{wheel_dir}/*.whl")):
        base = os.path.basename(whl).lower()
        if base.startswith(skip):
            continue
        subprocess.run(
            f"pip install --no-index --no-deps --force-reinstall {whl}",
            shell=True,
            capture_output=True,
            text=True,
        )

    import numpy as np
    import polars as pl
    import tracksdata as td  # noqa: F401

    if not hasattr(pl, "Float16"):
        raise RuntimeError(f"polars {pl.__version__} too old for tracksdata")
    print(f"numpy={np.__version__} polars={pl.__version__} tracksdata OK")
    return wheel_dir


def extract_cellmot_bundle(work: Path = Path("/kaggle/working")) -> bool:
    """Materialize cellmot_bundle under ``work`` for predict_unet_transformer imports."""
    import shutil

    dst = work / "cellmot_bundle"
    if (dst / "scripts" / "predict_unet_transformer.py").exists():
        print(f"[CELLMOT] bundle ready at {dst}")
        return True

    zip_candidates = [
        work / "cellmot_code_bundle.zip",
        *glob.glob("/kaggle/input/**/cellmot_code_bundle.zip", recursive=True),
    ]
    for bundle_path in zip_candidates:
        p = Path(bundle_path)
        if not p.exists():
            continue
        with zipfile.ZipFile(p, "r") as zf:
            zf.extractall(work)
        if (work / "cellmot_bundle").exists():
            print(f"[CELLMOT] extracted zip {p}")
            return True

    script_hits = glob.glob(
        "/kaggle/input/**/cellmot_bundle/scripts/predict_unet_transformer.py",
        recursive=True,
    )
    if script_hits:
        src_root = Path(script_hits[0]).parent.parent
        shutil.copytree(src_root, dst, dirs_exist_ok=True)
        print(f"[CELLMOT] copied tree from {src_root}")
        return True

    print("[WARN] cellmot_bundle not found (zip or pre-extracted tree)")
    return False