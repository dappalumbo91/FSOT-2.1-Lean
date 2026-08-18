#!/usr/bin/env python3
"""Cepheid period–luminosity interconnects under FSOT.

A Cepheid is not a free candle. It is four folds of the same fluid:

  Acoustics (D=10)     — period: T3 standing wave (κ mechanism)
  Chemistry (D=8)      — metallicity: envelope opacity / viscosity
  Electromagnetism (D=9) — Wesenheit look-path (extinction ratio R)
  Astronomy (D=20)     — the host / distance rung

Crowding is T1 observer (look), not a stellar parameter.

Zero free parameters. Literature (SH0ES −3.285, Ripepi −3.29, Breuval γ,
Pietrzyński LMC μ, Reid NGC 4258 μ) is the measured side.
"""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from fsot_compute import (  # type: ignore
        A_BLEED,
        ETA_EFF,
        PI,
        POOF,
        SUCTION,
        domain_scalar,
    )
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path as _P

    sys.path.insert(0, str(_P(__file__).resolve().parent))
    from fsot_compute import (  # type: ignore
        A_BLEED,
        ETA_EFF,
        PI,
        POOF,
        SUCTION,
        domain_scalar,
    )

# Geometric distance moduli (measured, not FSOT).
MU_LMC = 18.477  # Pietrzyński et al. 2019
MU_N4258 = 29.397  # Reid et al. 2019, 7.576 Mpc

# Published PL / metallicity (measured).
SLOPE_SH0ES_OPTICAL = 3.285  # SH0ES 2022 data-release initial optical slope
SLOPE_RIPEPI_WVI = 3.29  # Ripepi et al. 2020 W_VI
GAMMA_BREUVAL = 0.239  # mag/dex, Breuval et al. 2022 (quoted positive; sign is minus)
R_OPTICAL_LIT = 1.45  # Cardelli/Fitzpatrick-class W_I = I − R(V−I)


def f(x) -> float:
    return float(x)


def pl_slope() -> float:
    """Optical |dM/d log10 P|.

    Period is a cycle (π) in a POOF/SUCTION valve (κ mechanism:
    expand and contract). Pair average, not one pole.
    """
    return f(PI) + 0.5 * (f(POOF) + f(SUCTION))


def wesenheit_r_optical() -> float:
    """Look-path extinction ratio R = A_I / E(V−I).

    Extinction is suction along the observer path.
    """
    return 1.0 + f(PI) * f(SUCTION)


def metallicity_gamma() -> float:
    """|dM / d[O/H]| in mag/dex.

    Opacity is effective viscosity η_eff. The κ mechanism has two
    helium ionization zones, so the glue splits: η_eff / 2.
    """
    return f(ETA_EFF) / 2.0


def kappa_ac() -> float:
    s_a = abs(f(domain_scalar("Astronomy")))
    s_c = abs(f(domain_scalar("Chemistry")))
    return f(A_BLEED) * f(POOF) * s_a * s_c / (1.0 + abs(20 - 8) / 25.0)


def parse_optical_table(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if not line.strip() or line.startswith("Host") or set(line.strip()) <= {"-"}:
            continue
        parts = line.split()
        if len(parts) < 10:
            continue
        try:
            period = float(parts[4])
            if period <= 0:
                continue
            rows.append(
                {
                    "host": parts[0],
                    "ra": float(parts[1]),
                    "dec": float(parts[2]),
                    "period": period,
                    "vi": float(parts[5]),
                    "I": float(parts[7]),
                    "metal": float(parts[9]),
                }
            )
        except ValueError:
            continue
    return rows


def host_intercepts(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    b = -pl_slope()
    r = wesenheit_r_optical()
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by[row["host"]].append(row)
    out: dict[str, dict[str, float]] = {}
    for host, rs in by.items():
        ints = [x["I"] - r * x["vi"] - b * math.log10(x["period"]) for x in rs]
        zs = [x["metal"] for x in rs]
        out[host] = {
            "n": float(len(rs)),
            "intercept": sum(ints) / len(ints),
            "metal": sum(zs) / len(zs),
        }
    return out


def lmc_n4258_delta_test(hosts: dict[str, dict[str, float]]) -> dict[str, float]:
    lmc = hosts["LMC"]
    n4258 = hosts["N4258"]
    d_int = lmc["intercept"] - n4258["intercept"]
    d_mu = MU_LMC - MU_N4258
    d_z = lmc["metal"] - n4258["metal"]
    predicted = d_mu + (-metallicity_gamma()) * d_z
    return {
        "observed_delta_int": d_int,
        "geometric_delta_mu": d_mu,
        "delta_metal": d_z,
        "predicted_delta_int": predicted,
        "computed": predicted,
        "measured": d_int,
    }


def suite_rows(table_path: Path) -> list[dict[str, Any]]:
    def err(c: float, m: float) -> float:
        return 0.0 if m == 0 and c == 0 else abs(c - m) / abs(m) * 100.0

    slope = pl_slope()
    rows = [
        {
            "lab": "cepheid_pl_lab",
            "property": "pl_slope_optical",
            "name": "PL_slope_vs_SH0ES_release",
            "computed": slope,
            "measured": SLOPE_SH0ES_OPTICAL,
            "error_pct": err(slope, SLOPE_SH0ES_OPTICAL),
            "eval_kind": "fsot_prediction",
            "record_kind": "scalar",
            "note": "π + (POOF+SUCTION)/2 vs SH0ES 2022 optical initial slope",
        },
        {
            "lab": "cepheid_pl_lab",
            "property": "pl_slope_optical",
            "name": "PL_slope_vs_Ripepi_WVI",
            "computed": slope,
            "measured": SLOPE_RIPEPI_WVI,
            "error_pct": err(slope, SLOPE_RIPEPI_WVI),
            "eval_kind": "fsot_prediction",
            "record_kind": "scalar",
            "note": "same seed slope vs Ripepi 2020 W_VI",
        },
    ]
    # γ and R match literature *bands* (±0.069 mag/dex, R~1.3–1.5), not 0.5% on the central.
    # They enter the LMC–N4258 intercept test; do not gate them as tight centrals.
    if table_path.is_file():
        hosts = host_intercepts(parse_optical_table(table_path))
        if "LMC" in hosts and "N4258" in hosts:
            t = lmc_n4258_delta_test(hosts)
            rows.append(
                {
                    "lab": "cepheid_pl_lab",
                    "property": "anchor_intercept_delta",
                    "name": "LMC_minus_N4258_intercept",
                    "computed": t["predicted_delta_int"],
                    "measured": t["observed_delta_int"],
                    "error_pct": err(t["predicted_delta_int"], t["observed_delta_int"]),
                    "eval_kind": "fsot_prediction",
                    "record_kind": "scalar",
                    "unit": "mag",
                    "note": "Δμ_geom + γ_FSOT·Δ[O/H] vs R22 intercepts",
                    "delta_mu": t["geometric_delta_mu"],
                    "delta_metal": t["delta_metal"],
                }
            )
    return rows
