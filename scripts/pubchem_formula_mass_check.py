#!/usr/bin/env python3
"""Score stored PubChem weights by the atomic-mass sum. This script only prints."""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fsot_api_predict_lib import formula_mass  # noqa: E402


def main() -> int:
    path = ROOT / "data" / "pubchem_compound_properties_benchmark.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    rows = doc.get("records") or []
    errs: list[float] = []
    unparsed = 0
    for row in rows:
        mass = formula_mass(str(row.get("formula") or ""))
        measured = row.get("measured")
        if mass is None or not isinstance(measured, (int, float)) or float(measured) == 0:
            unparsed += 1
            print(f"unparsed name={row.get('name')} formula={row.get('formula')}")
            continue
        errs.append(abs(mass - float(measured)) / abs(float(measured)) * 100.0)
    print(f"n={len(errs)} unparsed={unparsed}")
    if errs:
        print(f"median={statistics.median(errs)} max={max(errs)}")
    kinds = sorted({str(row.get("eval_kind")) for row in rows})
    print(f"eval_kinds={kinds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
