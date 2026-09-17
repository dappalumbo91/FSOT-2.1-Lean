#!/usr/bin/env python3
"""Optics n_D product — CRC index on Optics fold, not Chemistry MW. Pin AEB2AD."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import fsot_correct  # noqa: E402
from fsot_compute import PHI  # noqa: E402


def main() -> int:
    print("product=optics_nd pin=AEB2AD ledger=B_correct kill=water_eps80_as_n2")
    rows = [
        ("water_nD_20C", 1.3330, "Optics"),
        ("ice_Ih_nD", 1.309, "Optics"),
        ("ice_n_phi2_over_2", float(PHI) ** 2 / 2.0, "Condensed_Matter"),
    ]
    print(f"{'object':<22} {'m':>8} {'c':>10} {'err%':>8} fold")
    worst = 0.0
    for name, m, domain in rows:
        if name == "ice_n_phi2_over_2":
            c, err = m, abs(m - 1.309) / 1.309 * 100.0
            print(f"{name:<22} {1.309:8.4f} {c:10.4f} {err:8.4f} seed vs CRC ice")
            worst = max(worst, err)
            continue
        c, err = fsot_correct(m, domain)
        worst = max(worst, err)
        print(f"{name:<22} {m:8.4f} {c:10.4f} {err:8.4f} {domain}")
    print("Maxwell n^2 is the optical dielectric. Static ε~80 is a different orifice.")
    return 0 if worst <= 0.5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
