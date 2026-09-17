#!/usr/bin/env python3
"""Chemistry lab product — CRC water, three zooms. Ledger B correction. Pin AEB2AD."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import fsot_correct  # noqa: E402
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402


def main() -> int:
    mod, path = load_fsot_compute()
    pin = __import__("hashlib").sha256(Path(path).read_bytes()).hexdigest()[:6].upper()
    rows = [
        ("MW H2O", 18.015, "Chemistry", "g/mol"),
        ("Tm ice", 273.15, "Physical_Chemistry", "K"),
        ("Tb water", 373.15, "Physical_Chemistry", "K"),
    ]
    print(f"product=chemistry_lab pin={pin} ledger=B_correct kill=fitted_Trouton")
    print(f"{'object':<12} {'m':>10} {'c':>10} {'err%':>8} fold")
    worst = 0.0
    for name, m, domain, unit in rows:
        c, err = fsot_correct(m, domain)
        worst = max(worst, err)
        print(f"{name:<12} {m:10.3f} {c:10.4f} {err:8.3f} {domain} ({unit})")
    print("green_if_median<=0.5  (this trio is a specimen, not the 477-file gate)")
    print("not_claimed: ToE accuracy; n_D as MW")
    return 0 if worst <= 0.5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
