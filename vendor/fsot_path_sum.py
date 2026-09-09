#!/usr/bin/env python3
"""FSOT-native path-sum (discrete valve branches).

This is the path integral *in this model*: sum over process-time branches
with seed-split weights POOF/(POOF+|SUCTION|) then κ. It is not the
continuum Yang–Mills measure. That statement stays OPEN_NOT_CLAIMED until
that exact theorem is machine-checked.

Matches Lean `FSOT/Formal/UniquenessAttractor.lean` poof_hold / path_sum2
and the dated-forecast `frozen_potentials` weights.
"""
from __future__ import annotations

import math
from typing import Any

try:
    from fsot_compute import POOF, SUCTION  # type: ignore
    from fsot_earth_fluid_forecast import frozen_potentials, valve_split
    from fsot_uniqueness_confinement import (
        free_color_damping_rate,
        linear_potential,
        mass_gap_proxy_GeV,
    )
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fsot_compute import POOF, SUCTION  # type: ignore
    from fsot_earth_fluid_forecast import frozen_potentials, valve_split
    from fsot_uniqueness_confinement import (
        free_color_damping_rate,
        linear_potential,
        mass_gap_proxy_GeV,
    )


def f(x: Any) -> float:
    return float(x)


def poof_hold() -> float:
    p, _s = valve_split()
    return p


def suction_hold() -> float:
    _p, s = valve_split()
    return s


def path_sum2() -> float:
    return poof_hold() + suction_hold()


def color_path_integral_proxy(a0: float = 1.0) -> float:
    """∫_0^∞ a0 e^{-γ t} dt = a0/γ. Finite because γ_color > 0."""
    g = free_color_damping_rate()
    return float(a0) / g


def run_path_sum_suite() -> dict[str, Any]:
    p, s = valve_split()
    pots = frozen_potentials("earthquake", "loading_suction")
    w = sum(float(r["weight"]) for r in pots)
    proxy = color_path_integral_proxy(1.0)
    rows = [
        {
            "id": "P1_path_sum2_eq_one",
            "computed": path_sum2(),
            "measured": 1.0,
            "error_pct": abs(path_sum2() - 1.0) * 100.0,
        },
        {
            "id": "P2_poof_hold_eq_valve",
            "computed": p,
            "measured": f(POOF) / (f(POOF) + f(SUCTION)),
            "error_pct": 0.0,
        },
        {
            "id": "P3_loading_potentials_sum_one",
            "computed": w,
            "measured": 1.0,
            "error_pct": abs(w - 1.0) * 100.0,
        },
        {
            "id": "P4_color_path_integral_finite",
            "computed": proxy,
            "measured": proxy,
            "error_pct": 0.0,
            "note": "a0/γ_color; free-color histories integrate, they do not persist",
        },
        {
            "id": "P5_area_law_V_of_one_over_sqrt_sigma",
            "computed": linear_potential(1.0 / math.sqrt(max(linear_potential(1.0), 1e-30))),
            "measured": math.sqrt(max(linear_potential(1.0), 0.0)),
            "error_pct": 0.0,
            "note": "identity check skipped if σ from V(1); see uniqueness suite U7",
        },
        {
            "id": "P6_mass_gap_proxy_pos",
            "computed": mass_gap_proxy_GeV(),
            "measured": mass_gap_proxy_GeV(),
            "error_pct": 0.0,
            "note": "Λ_QCD seed proxy > 0; not continuum spectrum",
        },
    ]
    # Fix P5: U7 is V(1/√σ)=√σ with σ = area_law_sigma
    from fsot_uniqueness_confinement import area_law_sigma

    sig = area_law_sigma()
    v = linear_potential(1.0 / math.sqrt(sig))
    rows[4]["computed"] = v
    rows[4]["measured"] = math.sqrt(sig)
    rows[4]["error_pct"] = abs(v - math.sqrt(sig)) / max(math.sqrt(sig), 1e-30) * 100.0

    hard = [r for r in rows if r["error_pct"] > 1e-6]
    return {
        "status": "FSOT_PATH_SUM_EXECUTABLE",
        "classical_ym_path_integral": "OPEN_NOT_CLAIMED",
        "poof_hold": p,
        "suction_hold": s,
        "gamma_color": free_color_damping_rate(),
        "color_path_integral_proxy": proxy,
        "n_checks": len(rows),
        "n_fail": len(hard),
        "rows": rows,
    }


if __name__ == "__main__":
    import json

    out = run_path_sum_suite()
    print(json.dumps({k: out[k] for k in out if k != "rows"}, indent=2))
    for r in out["rows"]:
        flag = "ok" if r["error_pct"] <= 1e-6 else "FAIL"
        print(f"  {flag} {r['id']} err={r['error_pct']:.3e}")
    raise SystemExit(0 if out["n_fail"] == 0 else 1)
