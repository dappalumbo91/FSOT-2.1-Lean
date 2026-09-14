#!/usr/bin/env python3
"""Write predictions/LEDGER_A_FREEZE.yaml from live fsot_predict (no measured in formula)."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_ledger_a_lib import LEDGER_A, compare_anchor, engine_pin  # noqa: E402

OUT = ROOT / "predictions" / "LEDGER_A_FREEZE.yaml"


def _ops(expr: str) -> int:
    return sum(expr.count(ch) for ch in "+-*/")


def main() -> int:
    pin = engine_pin()
    lines = [
        f"# Ledger A freeze — pin {pin}",
        f"# generated_at: {datetime.now(timezone.utc).isoformat()}",
        "# Changing an expression requires a new PRED id. No silent rewrite.",
        "ledger: A",
        f"pin: {pin}",
        "rows:",
    ]
    n_fore = n_id = n_miss = 0
    for oid in sorted(LEDGER_A):
        spec = LEDGER_A[oid]
        rec = compare_anchor(oid)
        err = float(rec["error_pct"])
        kind = spec["kind"]
        if kind == "FORECAST":
            n_fore += 1
        else:
            n_id += 1
        if kind == "FORECAST" and err > 0.5:
            n_miss += 1
        lines += [
            f"  - id: {oid}",
            f"    kind: {kind}",
            f"    expression: {spec['expression']!r}",
            f"    expression_id: {spec['expression_id']}",
            f"    units: {spec['units']!r}",
            f"    value: {rec['value']}",
            f"    anchor: {spec['anchor']}",
            f"    error_pct: {err:.6f}",
            f"    operator_count: {_ops(spec['expression'])}",
            f"    kill_band: {spec['kill_band']!r}",
            f"    measured_in_formula: false",
        ]
    lines += [
        f"n_forecast: {n_fore}",
        f"n_constant_identity: {n_id}",
        f"n_forecast_outside_half_pct: {n_miss}",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} pin={pin} forecast={n_fore} identity={n_id} miss>0.5%={n_miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
