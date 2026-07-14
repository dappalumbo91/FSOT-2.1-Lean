#!/usr/bin/env python3
"""Verify FSOT GPU readiness (RTX 5070 / sm_120)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from zebrahub_gpu_video import _torch_info, _sample_zarr_tile  # noqa: E402


def main() -> int:
    info = _torch_info()
    ok = bool(info.get("cuda_usable"))
    print(json.dumps(info, indent=2))
    if not ok:
        print("\nCUDA not usable. Fix with:")
        print("  pip install --upgrade torch torchvision --index-url https://download.pytorch.org/whl/cu128")
        return 1
    url = (
        "https://public.czbiohub.org/royerlab/zebrahub/imaging/single-objective/"
        "ZSNS003.ome.zarr/"
    )
    sample = _sample_zarr_tile(url)
    print("\nZarr GPU sample:")
    print(json.dumps(sample, indent=2))
    if sample.get("backend") != "torch_cuda" or not sample.get("mean_intensity"):
        return 2
    print("\nFSOT CUDA verification: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())