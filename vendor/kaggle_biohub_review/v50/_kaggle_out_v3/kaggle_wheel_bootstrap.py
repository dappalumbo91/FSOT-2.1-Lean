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
    """Extract cellmot_code_bundle.zip from bundle copy or Kaggle inputs."""
    candidates = [
        work / "cellmot_code_bundle.zip",
        *glob.glob("/kaggle/input/**/cellmot_code_bundle.zip", recursive=True),
    ]
    for bundle_path in candidates:
        p = Path(bundle_path)
        if not p.exists():
            continue
        with zipfile.ZipFile(p, "r") as zf:
            zf.extractall(work)
        print(f"[CELLMOT] extracted {p}")
        return True
    print("[WARN] cellmot_code_bundle.zip not found")
    return False