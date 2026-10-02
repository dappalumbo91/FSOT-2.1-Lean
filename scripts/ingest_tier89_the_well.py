#!/usr/bin/env python3
"""Tier 89 — The Well outcomes verification ingests."""

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

from tier89_the_well_lib import INGESTORS, cache_root  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deep", action="store_true")
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    parser.add_argument(
        "--external-root",
        default="",
        help="Override FSOT_EXTERNAL_DATA_ROOT (e.g. $FSOT_EXTERNAL_DATA_ROOT)",
    )
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER89_DEEP"] = "1"
    if args.external_root:
        os.environ["FSOT_EXTERNAL_DATA_ROOT"] = args.external_root
    elif not os.environ.get("FSOT_EXTERNAL_DATA_ROOT"):
        for candidate in (_os.fspath(_fsot_local_path('FSOT_EXTERNAL_DATA_ROOT', 'data_external/public_data')), _os.fspath(_fsot_local_path('FSOT_LEAN_PUBLIC_DATA', 'data_external/lean_public_data'))):
            if Path(candidate).exists():
                os.environ["FSOT_EXTERNAL_DATA_ROOT"] = candidate
                break
    print(f"External cache: {cache_root()}")
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        count = doc.get("dataset_count") or doc.get("spot_count") or 0
        print(f"{key}: {count} ({doc.get('source')})")
    print("\nAll Tier 89 The Well ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())