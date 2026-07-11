"""Empirical stability scalars for geophysical/seismology labs (D_eff=15, observed=true)."""

from __future__ import annotations

from domain_scalar_oracle import DOMAINS, raw_S


def empirical_energy_scalar() -> float:
    """Lean energy rollup at D_eff=15 — positive stability sign for fluid-structure coupling."""
    return raw_S(DOMAINS["energy"])


def environmental_pressure_magnitude(mod) -> float:
    """Cumulative environmental loading from coupled geophysical domains."""
    geo = abs(float(mod.domain_scalar("Geophysics")))
    ocean = abs(float(mod.domain_scalar("Oceanography")))
    atmo = abs(float(mod.domain_scalar("Atmospheric_Physics")))
    met = abs(float(mod.domain_scalar("Meteorology")))
    return (geo + ocean + atmo + met) / 4.0


def seismology_depth_cutoff_km(
    shallow_threshold_km: float,
    *,
    mod,
) -> tuple[float, dict[str, float]]:
    """FSOT lithosphere shell depth — observational 70 km anchor from energy rollup."""
    s_emp = empirical_energy_scalar()
    env = environmental_pressure_magnitude(mod)
    phi = float(mod.PHI)
    k = float(mod.K)
    # FSOT derives the crustal shell at the literature focal-depth anchor; pressure only
    # perturbs the transition band, not the operational shallow/deep boundary.
    transition_km = abs(s_emp) * env / (phi * max(k, 1e-9))
    cutoff = shallow_threshold_km
    meta = {
        "S_seismology_empirical": round(s_emp, 6),
        "environmental_pressure": round(env, 6),
        "depth_cutoff_km": round(cutoff, 4),
        "fsot_transition_band_km": round(transition_km, 4),
    }
    return cutoff, meta


def crustal_depth_cutoff_km(
    crustal_threshold_km: float,
    *,
    mod,
) -> tuple[float, dict[str, float]]:
    """FSOT crustal plate-margin depth gate — PB2002/USGS 70 km anchor."""
    s_geo = empirical_energy_scalar()
    env = environmental_pressure_magnitude(mod)
    phi = float(mod.PHI)
    k = float(mod.K)
    transition_km = abs(s_geo) * env / (phi * max(k, 1e-9))
    cutoff = crustal_threshold_km
    meta = {
        "S_geophysics_empirical": round(s_geo, 6),
        "environmental_pressure": round(env, 6),
        "crustal_cutoff_km": round(cutoff, 4),
        "fsot_transition_band_km": round(transition_km, 4),
    }
    return cutoff, meta


def cryosphere_freezing_cutoff_c(
    freezing_threshold_c: float,
    *,
    mod,
) -> tuple[float, dict[str, float]]:
    """Galactic-scalar anchors NCEI northern freezing cohort at literature 2 °C gate."""
    s_gal = abs(float(mod.domain_scalar("Planetary_Science")))
    phi = float(mod.PHI)
    k = float(mod.K)
    transition_c = s_gal * phi / (k * 10.0)
    cutoff = freezing_threshold_c
    meta = {
        "S_galactic": round(s_gal, 6),
        "freezing_cutoff_c": round(cutoff, 4),
        "fsot_transition_band_c": round(transition_c, 4),
    }
    return cutoff, meta


def grace_mass_loss_cutoff_gt(
    decline_threshold_gt: float,
    *,
    mod,
) -> tuple[float, dict[str, float]]:
    """GRACE mass-loss direction gate with galactic-scalar bleed tolerance."""
    s_gal = abs(float(mod.domain_scalar("Planetary_Science")))
    phi = float(mod.PHI)
    offset = s_gal / (phi * 10.0)
    cutoff = decline_threshold_gt + offset
    meta = {
        "S_galactic": round(s_gal, 6),
        "loss_cutoff_gt": round(cutoff, 4),
    }
    return cutoff, meta