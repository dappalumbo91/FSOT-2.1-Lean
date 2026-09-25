#!/usr/bin/env python3
"""Read-only note of the Pantheon+SH0ES directional null.

Does not rewrite fsot_compute, Lean, or any frozen prediction.
The dipole numbers are the external 238-supernova run, stored beside this file.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "vendor"))

import fsot_compute as law  # noqa: E402

NULL = Path(__file__).with_name("pantheon_shoes_directional_null.json")


def main() -> int:
    pin = hashlib.sha256((ROOT / "vendor" / "fsot_compute.py").read_bytes()).hexdigest()[:6].upper()
    doc = json.loads(NULL.read_text(encoding="utf-8"))
    print(f"pin={pin} S_COSM={float(law.S_COSM):.6f}")
    print(
        f"null n={doc['n']} dipole={doc['dipole_pct']}% ± {doc['dipole_sigma_pct']}% "
        f"({doc['consistent_with']})"
    )
    print(doc["rule"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
