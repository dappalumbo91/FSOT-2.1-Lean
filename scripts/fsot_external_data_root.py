#!/usr/bin/env python3
"""Resolve multi-drive external data root for large open-science downloads.

Preference order:
  1. FSOT_EXTERNAL_DATA_ROOT env
  2. G:/FSOT-PublicData (existing public-data volume)
  3. I:/FSOT-PublicData (physical archive drive — created if I: present)
  4. D:/FSOT-PublicData
  5. vendor/public_data/cache (repo-local fallback)
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_CANDIDATES = (
    Path(r"G:\FSOT-PublicData"),
    Path(r"I:\FSOT-PublicData"),
    Path(r"D:\FSOT-PublicData"),
    Path(r"I:\FSOT-Physical-Archive\FSOT-PublicData"),
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
