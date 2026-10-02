#!/usr/bin/env python3
"""Ask whether the alpha leaf can meet the CODATA uncertainty.

The leaf is e^3 * phi^4 - psi_con. The bar is the CODATA 2022 uncertainty
on alpha, 2.1e-8 absolute on alpha^-1. A correction is one power of e, phi,
or psi_con, the constants already in the leaf. The check records how many
uncertainties the leaf still misses and does not replace the leaf.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mpmath import mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

PATH = ROOT / "data" / "codata_full_table_open_benchmark.json"
TARGET = mpf("137.035999177")
# CODATA 2022: alpha^-1 = 137.035999177(21)
ABSOLUTE_UNCERTAINTY = mpf("2.1e-8")


def main() -> int:
    leaf = F.E ** 3 * F.PHI ** 4 - F.PSI_CON
    gap = leaf - TARGET
    bar_ppm = float(ABSOLUTE_UNCERTAINTY / TARGET * mpf("1e6"))
    leaf_ppm = float(abs(gap) / TARGET * mpf("1e6"))
    sigmas = leaf_ppm / bar_ppm
    closest = None
    for name, base in (("e", F.E), ("phi", F.PHI), ("psi_con", F.PSI_CON)):
        for exponent in range(-16, 9):
            if exponent == 0:
                continue
            term = power(base, exponent)
            for sign in (1, -1):
                remain = abs(gap - sign * term)
                if closest is None or remain < closest[0]:
                    closest = (remain, name, exponent, sign, term)
    remain, name, exponent, sign, term = closest
    remain_ppm = float(remain / TARGET * mpf("1e6"))
    print(f"leaf={leaf}")
    print(f"gap={gap}")
    print(f"leaf_ppm={leaf_ppm}")
    print(f"bar_ppm={bar_ppm}")
    print(f"sigmas_above_bar={sigmas}")
    print(
        f"closest {('+' if sign > 0 else '-')}{name}^{exponent} "
        f"remain_ppm={remain_ppm} meets={remain <= ABSOLUTE_UNCERTAINTY}"
    )
    if remain <= ABSOLUTE_UNCERTAINTY:
        raise SystemExit("an in-leaf power meets the bar; the leaf was not updated")
    doc = json.loads(PATH.read_text(encoding="utf-8"))
    for row in doc["material_records"]:
        bar = row.get("field_bar") or {}
        if not isinstance(row.get("error_pct"), (int, float)):
            continue
        if bar.get("unit") != "ppm" or not bar.get("value"):
            continue
        ppm = abs(float(row["error_pct"])) * 10_000.0
        row["sigmas_above_bar"] = ppm / float(bar["value"])
    attest = doc.setdefault("accuracy_attestation", {})
    attest["alpha_leaf_ppm"] = leaf_ppm
    attest["alpha_bar_ppm"] = bar_ppm
    attest["alpha_sigmas_above_bar"] = sigmas
    attest["alpha_in_leaf_power_meets_bar"] = False
    attest["alpha_closest_power"] = {
        "term": f"{'+' if sign > 0 else '-'}{name}^{exponent}",
        "remain_ppm": remain_ppm,
    }
    PATH.write_text(json.dumps(doc, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("codata_bar_check_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
