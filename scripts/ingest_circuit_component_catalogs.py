#!/usr/bin/env python3
"""Tier 96 — ingest industry component parametric catalog (offline-first)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from circuit_component_emergence_lib import INGESTORS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(INGESTORS.keys()), action="append")
    args = parser.parse_args()
    targets = args.only or sorted(INGESTORS.keys())
    for key in targets:
        doc = INGESTORS[key]()
        print(
            f"{key}: {doc.get('component_count', 0)} components, "
            f"{doc.get('reference_circuit_count', 0)} reference circuits"
        )
    print("\nAll Tier 96 circuit component ingests complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())