"""FSOT phase-shift physics — dark matter/energy as out-of-phase matter/energy."""

from __future__ import annotations

import math
from typing import Any


def _f(mod, name: str, default: float = 1.0) -> float:
    return float(getattr(mod, name, default))


def phase_realized(mod) -> float:
    """In-phase fraction of cosmological reality (C_EFF structure)."""
    theta = _f(mod, "THETA_S")
    poof = _f(mod, "POOF")
    return 1.0 - poof * math.sin(theta)


def phase_shadow(mod) -> float:
    """Out-of-phase shadow sector (dark matter / dark energy equivalent)."""
    theta = _f(mod, "THETA_S")
    poof = _f(mod, "POOF")
    return poof * math.sin(theta)


def phase_variance(mod) -> float:
    return _f(mod, "P_VAR")


def phase_bleed_cross(mod, delta_psi: float = 1.5) -> float:
    """Cross-phase tunnel coupling (quirk_mod cosine × opposite-phase POOF/SUCTION)."""
    theta = _f(mod, "THETA_S")
    poof = _f(mod, "POOF")
    suction = _f(mod, "SUCTION")
    p_var = phase_variance(mod)
    tunnel = poof * math.cos(theta + math.pi) + suction * math.sin(theta)
    quirk = math.cos(delta_psi + p_var)
    return abs(tunnel) * abs(quirk)


def shadow_tunnel_gain(mod) -> float:
    """BH→WH tunnel scatter through shadow medium (POOF/η × |S_quant|)."""
    poof = _f(mod, "POOF")
    eta = max(_f(mod, "ETA_EFF"), 1e-9)
    theta = _f(mod, "THETA_S")
    s_quant = abs(float(mod.domain_scalar("Quantum_Mechanics")))
    return (poof / eta) * s_quant * (1.0 + math.sin(theta))


def phase_affinity(mod, kind: str) -> float:
    """Per-anomaly shadow affinity from FSOT structural ratios."""
    poof = max(_f(mod, "POOF"), 1e-9)
    k = _f(mod, "K")
    phi = _f(mod, "PHI")
    a_bleed = _f(mod, "A_BLEED")
    base = (phi / poof) * k
    weights = {
        "frb_tunnel": base,
        "h0_local": 0.5 + abs(phase_variance(mod)) * 0.5,
        "lensing": _f(mod, "A_BLEED") / max(_f(mod, "ETA_EFF"), 1e-9),
        "bbn": phi / max(_f(mod, "GAMMA"), 1e-9) * 0.1,
        "cmb": theta_scale(mod),
        "outgassing": a_bleed / poof,
    }
    return weights.get(kind, 1.0)


def theta_scale(mod) -> float:
    return _f(mod, "THETA_S") * _f(mod, "PHI") / max(_f(mod, "K"), 1e-9)


def apply_phase_shift(
    in_phase_value: float,
    mod,
    *,
    affinity: str = "cmb",
    delta_psi: float = 1.5,
) -> float:
    """
    Observable = in-phase component + shadow-sector bleed-through.
    Dark matter/energy contributes via out-of-phase tunnel (not fully realized here).
    """
    r = phase_realized(mod)
    s = phase_shadow(mod)
    g = shadow_tunnel_gain(mod) * phase_affinity(mod, affinity)
    bleed = phase_bleed_cross(mod, delta_psi=delta_psi)
    shadow_term = s * g * (1.0 + bleed)
    return in_phase_value * r + in_phase_value * shadow_term


def shadow_void_amplification(
    in_phase_value: float,
    mod,
    wh_frac: float,
) -> float:
    """WH suction void deepens CMB cold spot via shadow-phase tunnel gain."""
    sh = phase_shadow(mod)
    suction = max(_f(mod, "SUCTION"), 1e-9)
    k = _f(mod, "K")
    phi = _f(mod, "PHI")
    void_gain = (k * phi + suction) / suction
    return in_phase_value * (1.0 + sh * wh_frac * void_gain)


def lookback_compression(
    in_phase_value: float,
    mod,
    wh_frac: float,
) -> float:
    """Recompactification compresses apparent lookback redshift (φ−1 shadow term)."""
    sh = phase_shadow(mod)
    phi = _f(mod, "PHI")
    return in_phase_value * (1.0 - sh * wh_frac * (phi - 1.0))


def tunnel_dm_lengthening(
    in_phase_value: float,
    mod,
    *,
    delta_psi: float = 1.5,
) -> float:
    """BH→WH tunnel scatter adds shadow-path DM excess to the in-phase IGM anchor."""
    sh = phase_shadow(mod)
    stg = shadow_tunnel_gain(mod)
    aff = phase_affinity(mod, "frb_tunnel")
    bleed = phase_bleed_cross(mod, delta_psi=delta_psi)
    return in_phase_value + sh * stg * aff * (1.0 + bleed)


def bbn_entropy_depletion(
    in_phase_value: float,
    mod,
) -> float:
    """WH outgassing entropy depletes BBN lithium via shadow poof/suction tunnel pair."""
    sh = phase_shadow(mod)
    poof = _f(mod, "POOF")
    suction = max(_f(mod, "SUCTION"), 1e-9)
    depletion = (poof + suction) / suction
    return in_phase_value * (1.0 - sh * depletion)


def local_h0_inflation(
    in_phase_value: float,
    mod,
    *,
    delta_psi: float = 1.5,
) -> float:
    """SH0ES/local sector: phase-shift base + WH tunnel inflation (6-fold kφ harmonic)."""
    base = apply_phase_shift(
        in_phase_value, mod, affinity="h0_local", delta_psi=delta_psi
    )
    sh = phase_shadow(mod)
    stg = shadow_tunnel_gain(mod)
    bleed = phase_bleed_cross(mod, delta_psi=delta_psi)
    k = _f(mod, "K")
    phi = _f(mod, "PHI")
    scatter = sh * stg * (1.0 + bleed) * k * phi * 6.0
    return base + scatter


def depleted_h0_compression(in_phase_value: float, mod) -> float:
    """Carnegie/depleted sector: double phase-realization compression."""
    r = phase_realized(mod)
    return in_phase_value * r * r


def lensing_decay_delta(in_phase_value: float, mod) -> float:
    """WH lensing decay: S8 tension via double phase-realization depletion."""
    r = phase_realized(mod)
    return in_phase_value * r * r


def pole_preference_tunnel(
    in_phase_value: float,
    mod,
    bleed_frac: float,
    *,
    delta_psi: float = 1.5,
) -> float:
    """CMB axis-of-evil: WH pole preference shadow tunnel through bleed orifice."""
    sh = phase_shadow(mod)
    stg = shadow_tunnel_gain(mod)
    bleed = phase_bleed_cross(mod, delta_psi=delta_psi)
    phi = max(_f(mod, "PHI"), 1e-9)
    suction = max(_f(mod, "SUCTION"), 1e-9)
    tunnel = sh * stg * (1.0 + bleed) * bleed_frac * suction / phi
    return in_phase_value + tunnel


def orifice_anisotropy_deficit(
    in_phase_value: float,
    mod,
    wh_frac: float,
    bleed_frac: float,
) -> float:
    """CMB low-ℓ deficit: WH orifice anisotropy shadow bleed correction."""
    return in_phase_value + phase_shadow(mod) * wh_frac * bleed_frac


def outgassing_phase_split(mod) -> dict[str, float]:
    """WH outgassing material split: visible vs shadow-phase (unobserved mass/energy)."""
    r = phase_realized(mod)
    s = phase_shadow(mod)
    bleed = phase_bleed_cross(mod)
    visible = r
    shadow = s * (1.0 + bleed)
    total = visible + shadow
    return {
        "outgassing_visible_fraction": visible / total if total else r,
        "outgassing_shadow_fraction": shadow / total if total else s,
        "phase_realized": r,
        "phase_shadow": s,
        "phase_bleed_cross": bleed,
    }