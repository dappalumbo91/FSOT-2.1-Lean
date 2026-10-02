#!/usr/bin/env python3
"""Resolve multi-drive external data root for large open-science downloads.

Preference order:
  1. FSOT_EXTERNAL_DATA_ROOT env
  2. $FSOT_EXTERNAL_DATA_ROOT (existing public-data volume)
  3. $FSOT_EXTERNAL_DATA_ROOT (physical archive drive — created if I: present)
  4. $FSOT_EXTERNAL_DATA_ROOT
  5. vendor/public_data/cache (repo-local fallback)
"""

from __future__ import annotations

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[1]


def _fsot_local_path(env, default):
    """Local path outside the repo: $env if set, else a path relative to the repo root."""
    _v = _os.environ.get(env, "").strip()
    return _Path(_v) if _v else _REPO_ROOT / default


import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_CANDIDATES = (
    _fsot_local_path('FSOT_EXTERNAL_DATA_ROOT', 'data_external/public_data'),
    _fsot_local_path('FSOT_EXTERNAL_DATA_ROOT', 'data_external/public_data'),
    _fsot_local_path('FSOT_EXTERNAL_DATA_ROOT', 'data_external/public_data'),
    _fsot_local_path('FSOT_EXTERNAL_DATA_ROOT', 'data_external/public_data'),
)


def external_data_root(*, ensure: bool = True) -> Path:
    env = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    if env:
        p = Path(env).expanduser()
        if ensure:
            p.mkdir(parents=True, exist_ok=True)
        return p
    for cand in _CANDIDATES:
        # Prefer an existing parent drive
        drive = cand.anchor
        if drive and Path(drive).exists():
            if ensure:
                cand.mkdir(parents=True, exist_ok=True)
            return cand
    fallback = ROOT / "vendor" / "public_data" / "cache"
    if ensure:
        fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def open_science_large_dir(sub: str = "") -> Path:
    base = external_data_root(ensure=True) / "open_science_large"
    base.mkdir(parents=True, exist_ok=True)
    if sub:
        p = base / sub
        p.mkdir(parents=True, exist_ok=True)
        return p
    return base


if __name__ == "__main__":
    r = external_data_root()
    print(f"FSOT external data root: {r}")
    print(f"open_science_large: {open_science_large_dir()}")
