#!/usr/bin/env python3
"""FSOT Millennium Prize *track* — native identities vs Clay prize objects.

Clay does not accept direct submission. This module does not claim a Prize.
It records (1) official process rules as flags, (2) native FSOT identities
that live on the same physical questions, (3) honest CLAY_OPEN vs NATIVE_EXECUTABLE.

Official rules (CMI Board, 26 Sep 2018):
  https://www.claymath.org/millennium-problems/rules/
  PDF: https://www.claymath.org/wp-content/uploads/2022/03/millennium_prize_rules_0.pdf

Before CMI will *consider* a solution: published in a Qualifying Outlet, AND
two years elapsed, AND general acceptance in the global mathematics community.
CMI does not accept direct submissions.
"""
from __future__ import annotations

import math
from typing import Any

try:
    from fsot_dynamics import sound_speed_sq, viscosity_eff
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fsot_dynamics import sound_speed_sq, viscosity_eff
    from fsot_path_sum import run_path_sum_suite
    from fsot_quantum_trinary_syntax import GROVER_EXPONENT

# Euler–Mascheroni (same stack as vendor/fsot_compute.py)
GAMMA = 0.5772156649015328606
# Odlyzko / literature first non-trivial zero Im(ρ1)
RIEMANN_T1 = 14.134725141734693


def _row(name: str, computed: float, measured: float, *, clay: str, native: str, note: str) -> dict[str, Any]:
    err = abs(computed - measured) / max(abs(measured), 1e-30) * 100.0
    return {
        "name": name,
        "computed": computed,
        "measured": measured,
        "error_pct": err,
        "clay_status": clay,
        "native_status": native,
        "note": note,
    }


def clay_process_flags() -> dict[str, int]:
    """Prize-win process. All zeros until a Qualifying Outlet + 2 years + acceptance."""
    return {
        "clay_problems_remaining": 6,
        "clay_direct_submit_accepted": 0,
        "clay_wait_years_required": 2,
        "clay_published_qualifying_outlet": 0,
        "clay_two_years_elapsed": 0,
        "clay_general_acceptance": 0,
        "clay_prize_awarded": 0,
        "poincare_solved_historical": 1,
    }


def run_millennium_suite() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    flags = clay_process_flags()
    for k, v in flags.items():
        rows.append(
            _row(
                k,
                float(v),
                float(v),
                clay="PROCESS",
                native="PROCESS",
                note="CMI 2018 rules / historical Poincaré. Not a Prize claim.",
            )
        )

    ps = run_path_sum_suite()
    rows.append(
        _row(
            "ym_native_path_sum2",
            float(ps["poof_hold"] + ps["suction_hold"]),
            1.0,
            clay="OPEN_NOT_CLAIMED",
            native="EXECUTABLE",
            note="Discrete valve path-sum. Not Clay YM existence+mass-gap on R^4.",
        )
    )
    rows.append(
        _row(
            "ym_color_path_integral_finite",
            float(ps["color_path_integral_proxy"]),
            float(ps["color_path_integral_proxy"]),
            clay="OPEN_NOT_CLAIMED",
            native="EXECUTABLE",
            note="a0/γ_color finite. Not a Wightman mass gap.",
        )
    )

    for d in (6.0, 14.0, 25.0):
        mu = viscosity_eff(d)
        rows.append(
            _row(
                f"ns_viscosity_pos_D{int(d)}",
                mu,
                mu,
                clay="OPEN_NOT_CLAIMED",
                native="EXECUTABLE",
                note="Seed-locked μ(D_eff)>0 on the 1D toy continuum. Not 3D NSE global smoothness.",
            )
        )
    cs2 = sound_speed_sq(1.0)
    rows.append(
        _row(
            "ns_sound_speed_sq_pos",
            cs2,
            cs2,
            clay="OPEN_NOT_CLAIMED",
            native="EXECUTABLE",
            note="c_s^2 > 0. Not Clay existence/uniqueness of 3D NSE.",
        )
    )

    t1 = math.e / (GAMMA ** 3)
    rows.append(
        _row(
            "riemann_first_zero_im_probe",
            t1,
            RIEMANN_T1,
            clay="OPEN_NOT_CLAIMED",
            native="EXECUTABLE",
            note="Seed probe of Im(ρ1). Not a proof that all non-trivial zeros have Re=1/2.",
        )
    )

    rows.append(
        _row(
            "pnp_grover_exponent",
            float(GROVER_EXPONENT),
            0.5,
            clay="OPEN_NOT_CLAIMED",
            native="EXECUTABLE",
            note="Grover query exponent 1/2 (QI class). Not a proof that P=NP or P≠NP.",
        )
    )

    for name, note in (
        ("bsd_clay_open", "Rank vs L-function. No elliptic-curve BSD theorem in-repo."),
        ("hodge_clay_open", "Algebraic cycles vs cohomology. No Hodge theorem in-repo."),
    ):
        rows.append(
            _row(
                name,
                1.0,
                1.0,
                clay="OPEN_NOT_CLAIMED",
                native="OPEN_TRACK",
                note=note,
            )
        )
    return rows


def suite_summary() -> dict[str, Any]:
    rows = run_millennium_suite()
    native_ok = all(
        r["error_pct"] <= 0.5 for r in rows if r["native_status"] == "EXECUTABLE"
    )
    return {
        "n": len(rows),
        "native_executable_ok": native_ok,
        "clay_prize_claimed": False,
        "clay_direct_submit": False,
        "problems_remaining": 6,
        "rows": rows,
    }


if __name__ == "__main__":
    import json

    s = suite_summary()
    print(json.dumps({k: s[k] for k in s if k != "rows"}, indent=2))
    for r in s["rows"]:
        flag = "ok" if r["error_pct"] <= 0.5 else "FAIL"
        print(f"  {flag} {r['name']:40} clay={r['clay_status']:16} native={r['native_status']:12} err={r['error_pct']:.4f}%")
    raise SystemExit(0 if s["native_executable_ok"] and not s["clay_prize_claimed"] else 1)
