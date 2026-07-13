#!/usr/bin/env python3
"""Create a minimal OME-Zarr smoke fixture for local CPU runner tests."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import zarr


def write_fixture(out_dir: Path, name: str = "44b6_0113de3b", frames: int = 12) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    zpath = out_dir / f"{name}.zarr"
    if zpath.exists():
        return zpath
    root = zarr.open_group(str(zpath), mode="w")
    root.attrs["image_statistics"] = {"quantiles": {"0.5": 120.0, "0.99": 400.0}}
    shape = (frames, 1, 64, 64, 64)
    chunks = (1, 1, 64, 64, 64)
    rng = np.random.default_rng(42)
    data = rng.integers(0, 80, size=shape, dtype=np.uint16)
    for t in range(frames):
        y, x = 20 + (t % 5) * 6, 24 + (t % 4) * 7
        data[t, 0, 32, y : y + 4, x : x + 4] = 450
    root.create_dataset("0", data=data, chunks=chunks, overwrite=True)
    return zpath


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(r"D:\Kaggle_Biohub_Data\test"))
    parser.add_argument("--frames", type=int, default=12)
    args = parser.parse_args()
    zpath = write_fixture(args.out, frames=args.frames)
    print(f"wrote {zpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())