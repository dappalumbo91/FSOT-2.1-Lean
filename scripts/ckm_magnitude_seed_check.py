#!/usr/bin/env python3
"""Check the CKM magnitudes from the seed Wolfenstein parameters.

lambda = POOF*(1+eta_eff)
A = e/(pi*A_bleed)
rho_bar = gamma*e/pi^2
eta_bar = G_Catalan^2*K
The nine magnitudes are the Wolfenstein expansion already in the seeds.
|V_cs| uses the second-row identity sqrt(1-lambda^2-A^2*lambda^4).
The bars are the PDG 2024 global fit. Direct |V_ud| and |V_us| are printed
beside that fit. This script only prints.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from fsot_seed_flavor import (  # noqa: E402
    seed_A_wolfenstein,
    seed_ckm_magnitudes,
    seed_lambda_ckm,
)

# central, uncertainty on the low side, uncertainty on the high side
FIT = {
    "V_ud": (0.97435, 0.00016, 0.00016),
    "V_us": (0.22501, 0.00068, 0.00068),
    "V_ub": (0.003732, 0.000085, 0.000090),
    "V_cd": (0.22487, 0.00068, 0.00068),
    "V_cs": (0.97349, 0.00016, 0.00016),
    "V_cb": (0.04183, 0.00069, 0.00079),
    "V_td": (0.00858, 0.00017, 0.00019),
    "V_ts": (0.04111, 0.00068, 0.00077),
    "V_tb": (0.999118, 0.000034, 0.000029),
}
DIRECT = {
    "V_ud": (0.97367, 0.00032),
    "V_us": (0.22431, 0.00085),
}


def main() -> int:
    lam = seed_lambda_ckm()
    aval = seed_A_wolfenstein()
    mags = seed_ckm_magnitudes()
    mags["V_cs"] = (1.0 - lam * lam - (aval * aval) * (lam ** 4)) ** 0.5
    print(f"lambda={lam}")
    print(f"A={aval}")
    for name in (
        "V_ud",
        "V_us",
        "V_ub",
        "V_cd",
        "V_cs",
        "V_cb",
        "V_td",
        "V_ts",
        "V_tb",
    ):
        value = mags[name]
        central, down, up = FIT[name]
        gap = value - central
        bar = up if gap >= 0 else down
        side = "high" if gap >= 0 else "low"
        print(f"{name}={value} gap={gap} sigmas={abs(gap) / bar} side={side}")
        if name in DIRECT:
            dcentral, dbar = DIRECT[name]
            dgap = value - dcentral
            dside = "high" if dgap >= 0 else "low"
            print(f"  direct gap={dgap} sigmas={abs(dgap) / dbar} side={dside}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
