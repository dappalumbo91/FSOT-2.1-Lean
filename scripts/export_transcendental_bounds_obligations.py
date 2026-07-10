#!/usr/bin/env python3
"""Export Tier 83 transcendental bounds obligations from Bounds.lean."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transcendental_bounds_lib import write_obligations_json  # noqa: E402


def main() -> int:
    doc = write_obligations_json()
    print(f"Wrote {ROOT / 'verification' / 'obligations' / 'transcendental_bounds.json'}")
    print(f"  obligations: {doc['obligation_count']}")
    print(f"  python_decimal verified: {doc['python_decimal_verified_count']}")
    print(f"  by_proof_template: {doc['by_proof_template']}")
    print(f"  by_strategy: {doc['by_strategy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())