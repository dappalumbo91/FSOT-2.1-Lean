#!/usr/bin/env python3
"""Lean-aligned domain scalar oracle (mirrors FSOT.Formal.Scalar)."""

from __future__ import annotations

import math
from dataclasses import dataclass

PHI = (1 + math.sqrt(5)) / 2
E = math.e
PI = math.pi
SQRT2 = math.sqrt(2)
GAMMA_EULER = 0.57721566490153286060651209008240243
CATALAN_G = 0.91596559417721901505460351493238411

ALPHA = math.log(PI) / (E * PHI**13)
PSI_CON = 1 - math.exp(-1)
ETA_EFF = 1 / (PI - 1)
BETA = 1 / math.exp(PI**PI + (E - 1))
GAMMA = -math.log(2) / PHI
OMEGA = math.sin(PI / E) * SQRT2
THETA_S = math.sin(PSI_CON * ETA_EFF)
POOF_FACTOR = math.exp(-(math.log(PI) / E) / (ETA_EFF * math.log(PHI)))
ACOUSTIC_BLEED = math.sin(PI / E) * PHI / SQRT2
PHASE_VARIANCE = -math.cos(THETA_S + PI)
COHERENCE_EFFICIENCY = (1 - POOF_FACTOR * math.sin(THETA_S)) * (
    1 + 0.01 * CATALAN_G / (PI * PHI)
)
BLEED_IN_FACTOR = COHERENCE_EFFICIENCY * (1 - math.sin(THETA_S) / PHI)
ACOUSTIC_INFLOW = ACOUSTIC_BLEED * (1 + math.cos(THETA_S) / PHI)
SUCTION_FACTOR = POOF_FACTOR * (-math.cos(THETA_S - PI))
CHAOS_FACTOR = GAMMA / OMEGA
NEW_PERCEIVED_PARAM = (GAMMA_EULER / E) * SQRT2
CONSCIOUSNESS_FACTOR = COHERENCE_EFFICIENCY * NEW_PERCEIVED_PARAM
K = PHI * (GAMMA_EULER / E) * SQRT2 / math.log(PI) * 0.99


@dataclass
class FSOTParams:
    N: float = 1.0
    P: float = 1.0
    D_eff: float = 25.0
    recent_hits: float = 0.0
    delta_psi: float = 1.0
    delta_theta: float = 1.0
    rho: float = 1.0
    scale: float = 1.0
    amplitude: float = 1.0
    trend_bias: float = 0.0
    observed: bool = False


DOMAINS: dict[str, FSOTParams] = {
    "ai": FSOTParams(D_eff=11, recent_hits=0, delta_psi=0.50, delta_theta=1.0, observed=False),
    "neural": FSOTParams(D_eff=14, recent_hits=1, delta_psi=0.70, observed=True),
    "quantum": FSOTParams(D_eff=6, recent_hits=0, delta_psi=1.0, observed=True),
    "particle": FSOTParams(D_eff=7, recent_hits=0, delta_psi=0.85, observed=True),
    "cmb": FSOTParams(D_eff=24, recent_hits=0, delta_psi=0.8, observed=False),
    "chemical": FSOTParams(D_eff=9, recent_hits=0, delta_psi=0.5, observed=True),
    "molecular": FSOTParams(D_eff=9, recent_hits=0, delta_psi=0.4, observed=True),
    "material": FSOTParams(D_eff=10, recent_hits=0, delta_psi=0.5, observed=True),
    "biological": FSOTParams(D_eff=12, recent_hits=0, delta_psi=0.08, observed=False),
    "electron": FSOTParams(D_eff=8, recent_hits=0, delta_psi=0.6, observed=True),
    "astronomical": FSOTParams(D_eff=20, recent_hits=1, delta_psi=1.0, observed=True),
    "higgs": FSOTParams(D_eff=7, recent_hits=1, delta_psi=0.95, observed=True),
    "galactic": FSOTParams(D_eff=21, recent_hits=1, delta_psi=0.9, observed=True),
    "fusion": FSOTParams(D_eff=16, recent_hits=1, delta_psi=0.95, observed=True),
    "proton": FSOTParams(D_eff=8, recent_hits=0, delta_psi=0.7, observed=True),
    "medical": FSOTParams(D_eff=13, recent_hits=1, delta_psi=0.35, observed=True),
    "nuclear": FSOTParams(D_eff=15, recent_hits=1, delta_psi=1.0, observed=True),
    "energy": FSOTParams(D_eff=15, recent_hits=1, delta_psi=0.9, observed=True),
    "blackhole": FSOTParams(D_eff=23, recent_hits=2, delta_psi=1.25, observed=True),
    "consciousness": FSOTParams(D_eff=16, recent_hits=1, delta_psi=1.15, observed=True),
}


def quirk_mod(p: FSOTParams) -> float:
    if p.observed:
        return math.exp(CONSCIOUSNESS_FACTOR * PHASE_VARIANCE) * math.cos(
            p.delta_psi + PHASE_VARIANCE
        )
    return 1.0


def growth_term(p: FSOTParams) -> float:
    return math.exp(ALPHA * (1 - p.recent_hits / p.N) * GAMMA_EULER / PHI)


def term1_base(p: FSOTParams) -> float:
    scale = p.N * p.P / math.sqrt(p.D_eff)
    cos_arg = math.cos((PSI_CON + p.delta_psi) / ETA_EFF)
    exp_arg = math.exp(
        -ALPHA * p.recent_hits / p.N + p.rho + BLEED_IN_FACTOR * p.delta_psi
    )
    growth = 1 + growth_term(p) * COHERENCE_EFFICIENCY
    return scale * cos_arg * exp_arg * growth


def term1(p: FSOTParams) -> float:
    adj = 1 + NEW_PERCEIVED_PARAM * math.log(p.D_eff / 25)
    return term1_base(p) * adj * quirk_mod(p)


def term2(p: FSOTParams) -> float:
    return p.scale * p.amplitude + p.trend_bias


def term3(p: FSOTParams) -> float:
    scale = p.N * p.P / math.sqrt(p.D_eff)
    chaos = 1 + CHAOS_FACTOR * (p.D_eff - 25) / 25
    b1 = 1 + POOF_FACTOR * math.cos(THETA_S + PI) + SUCTION_FACTOR * math.sin(THETA_S)
    b2 = (
        1
        + ACOUSTIC_BLEED * math.sin(p.delta_theta) ** 2 / PHI
        + ACOUSTIC_INFLOW * math.cos(p.delta_theta) ** 2 / PHI
    )
    b3 = 1 + BLEED_IN_FACTOR * PHASE_VARIANCE
    return BETA * math.cos(p.delta_psi) * scale * chaos * b1 * b2 * b3


def raw_S(p: FSOTParams) -> float:
    return term1(p) + term2(p) + term3(p)


def main() -> None:
    print("domain,D_eff,delta_psi,recent_hits,observed,term1_base,term1,term2,term3,raw_S,sign")
    for name, p in DOMAINS.items():
        t1b = term1_base(p)
        t1 = term1(p)
        t2 = term2(p)
        t3 = term3(p)
        rs = raw_S(p)
        sign = "+" if rs > 0 else ("-" if rs < 0 else "0")
        print(
            f"{name},{p.D_eff},{p.delta_psi},{p.recent_hits},{p.observed},"
            f"{t1b:.6f},{t1:.6f},{t2:.6f},{t3:.6f},{rs:.6f},{sign}"
        )
        if name in ("cmb", "ai"):
            adj = 1 + NEW_PERCEIVED_PARAM * math.log(p.D_eff / 25)
            print(f"  perceived_adj={adj:.6f} quirk={quirk_mod(p):.6f}")


if __name__ == "__main__":
    main()