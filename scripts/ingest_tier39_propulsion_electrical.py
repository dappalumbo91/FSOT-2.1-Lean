#!/usr/bin/env python3
"""Ingest Tier 39 propulsion/electrical/HVAC/breakthroughs to Game drive."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier39_propulsion_electrical_lib import ingest_all  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    _ = parser.parse_args()
    doc = ingest_all()
    print(f"External cache: {doc['external_cache']}")
    for name, info in doc["bundles"].items():
        print(f"  {name}: {info['record_count']} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())