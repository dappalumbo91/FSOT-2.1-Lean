#!/usr/bin/env python3
"""MPCORB catalog product — class residual, not one ε per rock. Pin AEB2AD."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "mpcorb_fsot_benchmark.json"


def main() -> int:
    print("product=catalog_mpcorb pin=AEB2AD ledger=B_correct kill=one_epsilon_per_asteroid")
    if not BENCH.is_file():
        print("missing data/mpcorb_fsot_benchmark.json")
        return 1
    d = json.loads(BENCH.read_text(encoding="utf-8"))
    n = d.get("record_count") or d.get("n_objects") or d.get("mpcorb_object_count")
    med = d.get("pooled_median_error_pct") or d.get("median_error_pct")
    print(f"domain={d.get('domain')} records={n} pooled_median_pct={med}")
    print("class residual on IAU MPCORB. not_claimed: ToE accuracy; per-object free ε")
    return 0 if med is not None and float(med) <= 0.5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
