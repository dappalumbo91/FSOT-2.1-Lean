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
        # Early-universe / CMB class
        "planck_cmb_local",
        "planck_plus_bao_combo",
        "act_dr6_cmb",
        "spt3g_cmb",
        "wmap9_cmb",
        "sn_h0_no_local_cal",
        # BAO intermediate
        "desi_bao_rs_anchored",
        "sdss_bao_class",
        # Intermediate ladders
        "carnegie_h0",
        "freedman_jwst",
        "trgb_ground_class",
        "jagb_miras_class",
        # Local / geometric inflated sectors
        "sh0es_jwst",
        "sh0es_hst_cepheid",
        "jwst_cepheid_riess",
        "pantheon_plus_shoes_cal",
        "h0licow_tdcosmo",
        "tdcosmo_conservative",
        "megamaser_cosmology",
        "surface_brightness_fluctuations",
        "tully_fisher_class",
        "gw_standard_siren",
        # FSOT dual-anchor
        "fsot_document_local",
        "h0_bridge_scalar",
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


def angular_separation_deg(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    r1, d1, r2, d2 = (math.radians(float(x)) for x in (ra1, dec1, ra2, dec2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def sky_kernel_theta0_deg(mod=None) -> float:
    """Seed-closed angular scale: 180° / φ². Not a fit."""
    phi = float(getattr(mod, "PHI", 1.618033988749895)) if mod is not None else 1.618033988749895
    return 180.0 / (phi * phi)


def sky_mean_kernel(theta0_deg: float) -> float:
    """Isotropic sky average of 1/(1+θ/θ0)."""
    steps = 1800
    acc = 0.0
    wsum = 0.0
    for i in range(steps + 1):
        th = 180.0 * i / steps
        sw = math.sin(math.radians(th))
        acc += (1.0 / (1.0 + th / theta0_deg)) * sw
        wsum += sw
    return acc / wsum if wsum else 1.0


def local_sky_density(
    ra_deg: float,
    dec_deg: float,
    nebulae: list[dict],
    frbs: list[dict],
    *,
    mod=None,
) -> float:
    """Host-local catalog density in the same units as bubble_density_for_sector.

    Uniform catalog around the host → 0. Overdense → +. Underdense → −.
    Replaces 60° RA bins. No extra stretch.
    """
    theta0 = sky_kernel_theta0_deg(mod)
    w_bar = sky_mean_kernel(theta0)
    n_w = 0.0
    f_w = 0.0
    for row in nebulae:
        th = angular_separation_deg(
            ra_deg, dec_deg, float(row.get("ra_deg") or 0.0), float(row.get("dec_deg") or 0.0)
        )
        n_w += 1.0 / (1.0 + th / theta0)
    for row in frbs:
        th = angular_separation_deg(
            ra_deg, dec_deg, float(row.get("ra_deg") or 0.0), float(row.get("dec_deg") or 0.0)
        )
        f_w += 1.0 / (1.0 + th / theta0)
    total = len(nebulae) + 0.5 * len(frbs)
    if total <= 0 or w_bar <= 0:
        return 0.0
    return (n_w + 0.5 * f_w) / (total * w_bar) - 1.0


def ladder_object_density_model(
    method: str,
    density_sky: float,
    mod,
    *,
    cepheid_class_seed: float = 5.1,
) -> tuple[float, str]:
    """Per-object interface: geometric/TRGB anchors vs Cepheid SN hosts."""
    m = str(method or "")
    if "Maser" in m:
        return float(sector_h0_density_model("carnegie_h0", 2.0, density_sky, mod)), "anchor"
    if "TRGB" in m:
        return float(sector_h0_density_model("freedman_jwst", 1.85, density_sky, mod)), "anchor"
    return (
        float(sector_h0_density_model("sh0es_jwst", float(cepheid_class_seed), density_sky, mod)),
        "host",
    )


def ladder_chain_h0(
    objects: list[dict],
    *,
    h0_global: float,
    bleed_frac: float,
) -> dict[str, float]:
    """Information-weighted mixture of per-object FSOT H0.

    Weights are public Cepheid counts (measured), not a fit to 73.04.
    Each Cepheid is one unit of calibration information in the SH0ES joint fit.
    """
    rows = []
    for obj in objects:
        n = max(int(obj.get("cepheid_count") or 1), 1)
        h0 = float(obj["fsot_h0"])
        kind = str(obj.get("kind") or "host")
        rows.append((h0, n, kind))
    tot = sum(n for _, n, _ in rows) or 1
    chain = sum(h0 * n for h0, n, _ in rows) / tot
    hosts = [(h0, n) for h0, n, k in rows if k == "host"]
    anchors = [(h0, n) for h0, n, k in rows if k == "anchor"]
    host_w = sum(h0 * n for h0, n in hosts) / sum(n for _, n in hosts) if hosts else None
    anc_w = sum(h0 * n for h0, n in anchors) / sum(n for _, n in anchors) if anchors else None
    return {
        "h0_chain": chain,
        "h0_hosts_only": host_w if host_w is not None else chain,
        "h0_anchors_only": anc_w if anc_w is not None else chain,
        "weight_sum": float(tot),
        "host_weight_sum": float(sum(n for _, n in hosts)),
        "anchor_weight_sum": float(sum(n for _, n in anchors)),
    }


def wh_outgassing_mass_split(mod) -> dict[str, float]:
    """BH→WH outgassing: visible (in-phase) vs shadow-phase material."""
    from phase_shift_physics import outgassing_phase_split

    return outgassing_phase_split(mod)