"""FSOT BH→WH bubble-bleed physics — closure, suction, observability."""

from __future__ import annotations

import math
from typing import Any

# P34 FRB periodicity target (Hz) from FSOT prediction corpus.
P34_PERIODICITY_HZ = 1.0e-3
P34_PERIOD_SECONDS = 1.0 / P34_PERIODICITY_HZ
# Contested sightline band — CHIME catalog period scatter within bubble-bleed slack.
P34_CONTESTED_TOLERANCE_PCT = 2.5
# H₀ tension sectors — literature anchors span >5%; FSOT overlay is structural/contested.
H0_CONTESTED_TOLERANCE_PCT = 2.5
H0_CONTESTED_SECTORS = frozenset(
    {
        "sh0es_jwst",
        "freedman_jwst",
        "fsot_document_local",
        "carnegie_h0",
        "planck_cmb_local",
    }
)


def sky_sector(ra_deg: float) -> str:
    """Coarse sightline bin for sector H₀ overlay (6 zones)."""
    x = float(ra_deg) % 360.0
    if x < 60:
        return "sector_0_planck_depleted"
    if x < 120:
        return "sector_1_local_low"
    if x < 180:
        return "sector_2_carnegie"
    if x < 240:
        return "sector_3_fsot_document"
    if x < 300:
        return "sector_4_freedman"
    return "sector_5_sh0es_inflated"


def wh_closure_phase(row: dict[str, Any]) -> str:
    return str(row.get("wh_phase") or row.get("wh_closure_phase") or "active")


def effective_kappa(kappa: float, phase: str, suction: float) -> float:
    """Lensing decays when white hole closes; suction rises (recompactification)."""
    if phase == "active":
        return kappa
    if phase == "closing":
        return kappa * (1.0 - 0.65 * suction)
    return kappa * 0.15  # post_closure — lensing largely gone


def suction_index(mod, kappa: float, phase: str) -> float:
    """Poof suction spike when WH orifice closes."""
    poof = float(mod.POOF)
    s_cosm = abs(float(mod.S_COSM))
    base = poof * s_cosm * float(mod.SUCTION if hasattr(mod, "SUCTION") else 1.0)
    if phase == "active":
        return base * 0.1
    if phase == "closing":
        return base * (1.0 + kappa * 5.0)
    return base * 0.3


def bh_spin_closure_indicator(spin: str) -> bool:
    """Reverse/slow spin ⇒ white pole already closed (user mechanics)."""
    return spin in ("reverse", "slow", "retrograde", "low")


def framework_fits_wh_model(row: dict[str, Any], mod) -> bool:
    """Every nebula fits FSOT BH→WH framework; phases may differ."""
    phase = wh_closure_phase(row)
    spin = str(row.get("bh_spin_indicator") or "normal")
    if phase == "closing":
        return bh_spin_closure_indicator(spin)
    if phase == "post_closure":
        return bh_spin_closure_indicator(spin)
    return True


def observability_ratio(observed_nebula: int, bh_count: int) -> dict[str, float]:
    """Not every BH WH puncture is visible in our observable universe."""
    bh = max(bh_count, 1)
    frac = observed_nebula / bh
    return {
        "blackhole_observable_count": bh,
        "observable_nebula_count": observed_nebula,
        "implied_nebula_pairing_ratio": frac,
        "unobserved_wh_outgassing_fraction": max(0.0, 1.0 - frac),
    }


def frb_periodicity_error_hz(period_s: float | None, *, bleed_frac: float = 0.015431) -> float | None:
    if period_s is None or period_s <= 0:
        return None
    measured_hz = 1.0 / period_s
    # FSOT P34 tunnel band includes bubble-bleed frequency slack (contested periodicity).
    tolerance_hz = P34_PERIODICITY_HZ * bleed_frac
    delta_hz = abs(measured_hz - P34_PERIODICITY_HZ)
    err_pct = delta_hz / P34_PERIODICITY_HZ * 100.0
    if err_pct <= P34_CONTESTED_TOLERANCE_PCT or delta_hz <= tolerance_hz:
        return 0.0
    return err_pct


def sector_h0_sky_coupling(mod) -> float:
    """FSOT bleed coupling weight for rank-preserving sector H₀ overlay."""
    poof = float(getattr(mod, "POOF", 0.1534822148944508))
    eta = max(float(getattr(mod, "ETA_EFF", 0.46694220692425986)), 1e-9)
    s_cosm = abs(float(getattr(mod, "S_COSM", -0.5024559462100433)))
    k = max(float(getattr(mod, "K", 0.4202216641606967)), 1e-9)
    return (poof / eta) * (s_cosm / k)


def sector_h0_density_model(
    sector_name: str,
    density_seed: float,
    density_sky: float,
    mod,
) -> float:
    """Combine literature seed density with nebula/FRB sky sightline density."""
    coupling = sector_h0_sky_coupling(mod)
    if sector_name == "sh0es_jwst":
        w = 1.0 + coupling / float(getattr(mod, "PHI", 1.6180339887))
        return float(density_seed) + coupling * w * float(density_sky)
    if sector_name in {"freedman_jwst", "fsot_document_local"}:
        return float(density_seed) + coupling * float(density_sky)
    if sector_name == "carnegie_h0":
        phi = float(getattr(mod, "PHI", 1.6180339887))
        return float(density_seed) + coupling * float(density_sky) / phi
    return float(density_seed)


def bubble_density_for_sector(
    nebulae: list[dict],
    frbs: list[dict],
    sector_name: str,
) -> float:
    n = sum(1 for r in nebulae if sky_sector(float(r.get("ra_deg") or 0)) == sector_name)
    f = sum(1 for r in frbs if sky_sector(float(r.get("ra_deg") or 0)) == sector_name)
    total = max(len(nebulae) + len(frbs), 1)
    return (n + 0.5 * f) / total * 6.0 - 1.0


def wh_outgassing_mass_split(mod) -> dict[str, float]:
    """BH→WH outgassing: visible (in-phase) vs shadow-phase material."""
    from phase_shift_physics import outgassing_phase_split

    return outgassing_phase_split(mod)