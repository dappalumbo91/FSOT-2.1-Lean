#!/usr/bin/env python3
"""Write each handbook vaporization leaf as K times a power of the chemistry fold.

On the chemistry fold the valve is silent and T2 = 1, so S_chem = K * gamma
with gamma = S_chem / K. Every §47 ΔHvap leaf L then satisfies

    L = K * (S_chem / K)^p
    p = ln(L / K) / ln(S_chem / K)

p is the logarithm of the existing leaf. It is not fitted to the handbook
target, and the leaf's computed value does not move. vendor/fsot_compute.py
is not rewritten.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mpmath import log, mpf, power

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402

CRC = ROOT / "data" / "crc_handbook_properties_benchmark.json"
OUT = ROOT / "data" / "enthalpy_fold_powers.json"


def hvap_rows(node) -> list[dict]:
    found: list[dict] = []
    if isinstance(node, dict):
        prop = str(node.get("property") or "")
        if "Hvap" in prop and node.get("computed") is not None and node.get("name"):
            found.append(node)
        for value in node.values():
            found.extend(hvap_rows(value))
    elif isinstance(node, list):
        for value in node:
            found.extend(hvap_rows(value))
    return found


def main() -> int:
    gamma = F.S_CHEM / F.K
    rows = hvap_rows(json.loads(CRC.read_text(encoding="utf-8")))
    if len(rows) < 18:
        raise SystemExit(f"expected the 18 handbook vaporization rows, found {len(rows)}")
    payload = []
    for row in rows:
        leaf = mpf(str(row["computed"]))
        exponent = log(leaf / F.K) / log(gamma)
        rebuilt = F.K * power(gamma, exponent)
        if abs(rebuilt - leaf) > mpf("1e-18"):
            raise SystemExit(f"{row['name']} did not rebuild: {rebuilt} vs {leaf}")
        payload.append(
            {
                "name": row["name"],
                "property": row.get("property"),
                "leaf": str(row["computed"]),
                "measured": row.get("measured"),
                "leaf_formula": row.get("fsot_formula") or row.get("formula"),
                "fold_power": str(exponent),
                "form": "K*(S_chem/K)^p",
            }
        )
    OUT.write_text(
        json.dumps(
            {
                "K": str(F.K),
                "S_chem": str(F.S_CHEM),
                "gamma_chem": str(gamma),
                "identity": "L = K*(S_chem/K)^p with p = ln(L/K)/ln(S_chem/K)",
                "rows": payload,
            },
            indent=2,
         allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"rows={len(payload)} gamma={gamma}")
    print(f"wrote {OUT}")
    print("enthalpy_reduction_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
