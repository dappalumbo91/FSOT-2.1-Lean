#!/usr/bin/env python3
"""Tier 95 — Zebrahub zebrafish developmental genetics ingest."""

from __future__ import annotations

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[1]


def _fsot_local_path(env, default):
    """Local path outside the repo: $env if set, else a path relative to the repo root."""
    _v = _os.environ.get(env, "").strip()
    return _Path(_v) if _v else _REPO_ROOT / default


import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier95_zebrahub_development_lib import INGESTORS, cache_root  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--gpu", action="store_true", help="Run OME-Zarr GPU imaging sample ingest")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER95_DEEP"] = "1"
    if not os.environ.get("FSOT_ZEBRAHUB_CACHE_ROOT"):
        candidate = _fsot_local_path('FSOT_ARCHIVE_ROOT', 'data_external/physical_archive') / '05_Zebrahub-Development'
        if candidate.parent.exists():
            os.environ["FSOT_ZEBRAHUB_CACHE_ROOT"] = str(candidate)
    print(f"Zebrahub cache: {cache_root()}")
    keys = args.only or ["zebrahub_tracks"]
    if args.gpu and "zebrahub_gpu_imaging" not in keys:
        keys.append("zebrahub_gpu_imaging")
    for key in keys:
        doc = INGESTORS[key]()
        print(
            f"{key}: "
            f"datasets={doc.get('dataset_count', doc.get('sample_count', 'ok'))}"
        )
    print("\nTier 95 Zebrahub developmental ingest complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())