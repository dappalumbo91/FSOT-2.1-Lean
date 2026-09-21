#!/usr/bin/env python3
"""Sickness coupling product — host + pathogen lengths. Not a diagnosis. Pin AEB2AD."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE = ROOT / "data" / "sickness_two_system_smoke.json"


def main() -> int:
    print("product=sickness_coupling pin=AEB2AD ledger=B_correct kill=person_onset_as_0.5pct")
    if not SMOKE.is_file():
        print("missing data/sickness_two_system_smoke.json — run scripts/smoke_sickness_two_system.py")
        return 1
    d = json.loads(SMOKE.read_text(encoding="utf-8"))
    print(
        f"host_med={d.get('host_median_error_pct'):.4f}% "
        f"path_med={d.get('pathogen_median_error_pct'):.4f}% "
        f"kappa={d.get('kappa_host_pathogen'):.4f} pin={d.get('pin')}"
    )
    print(
        f"process_d12={d.get('process_time_days_host_d12'):.3f}d "
        f"process_d13={d.get('process_time_days_path_d13'):.3f}d"
    )
    print("not_claimed: this person gets sick on Tuesday; Biology observed flipped")
    ok = float(d["host_median_error_pct"]) <= 0.5 and float(d["pathogen_median_error_pct"]) <= 0.5
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
