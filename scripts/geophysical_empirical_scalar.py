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
    depth_pressure_scale: float = 8.0,
    env_pressure_scale: float = 4.0,
) -> tuple[float, dict[str, float]]:
    """Depth classifier cutoff with fluid-structure environmental pressure coupling."""
    s_emp = empirical_energy_scalar()
    env = environmental_pressure_magnitude(mod)
    cutoff = shallow_threshold_km + abs(s_emp) * depth_pressure_scale + env * env_pressure_scale
    meta = {
        "S_seismology_empirical": round(s_emp, 6),
        "environmental_pressure": round(env, 6),
        "depth_cutoff_km": round(cutoff, 4),
    }
    return cutoff, meta