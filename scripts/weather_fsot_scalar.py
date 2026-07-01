"""FSOT weather scalar mapping — matches Desktop/weather/fsot_weather_simulation_v1.py."""

from __future__ import annotations

import mpmath as mp

mp.mp.dps = 50

phi = (1 + mp.sqrt(5)) / 2
e = mp.e
pi = mp.pi
sqrt2 = mp.sqrt(2)
gamma_euler = mp.euler
catalan_G = mp.mpf("0.91596559417721901505460351493238411")

alpha = mp.log(pi) / (e * phi**13)
psi_con = 1 - mp.exp(-1)
eta_eff = 1 / (pi - 1)
beta = 1 / mp.exp(mp.power(pi, pi) + (e - 1))
gamma = -mp.log(2) / phi
omega = mp.sin(pi / e) * sqrt2
theta_s = mp.sin(psi_con * eta_eff)
poof_factor = mp.exp(-(mp.log(pi) / e) / (eta_eff * mp.log(phi)))
acoustic_bleed = mp.sin(pi / e) * phi / sqrt2
phase_variance = -mp.cos(theta_s + pi)
coherence_efficiency = (1 - poof_factor * mp.sin(theta_s)) * (
    1 + mp.mpf("0.01") * catalan_G / (pi * phi)
)
bleed_in_factor = coherence_efficiency * (1 - mp.sin(theta_s) / phi)
acoustic_inflow = acoustic_bleed * (1 + mp.cos(theta_s) / phi)
suction_factor = poof_factor * -mp.cos(theta_s - pi)
chaos_factor = gamma / omega
new_perceived_param = (gamma_euler / e) * sqrt2
consciousness_factor = coherence_efficiency * new_perceived_param
k = phi * ((gamma_euler / e) * sqrt2) / mp.log(pi) * (mp.mpf("99") / 100)


def compute_S_D_chaotic(p: dict) -> float:
    growth_term = mp.exp(alpha * (1 - p["recent_hits"] / p["N"]) * gamma_euler / phi)
    term1_base = (
        (p["N"] * p["P"] / mp.sqrt(p["D_eff"]))
        * mp.cos((psi_con + p["delta_psi"]) / eta_eff)
        * mp.exp(-alpha * p["recent_hits"] / p["N"] + p["rho"] + bleed_in_factor * p["delta_psi"])
        * (1 + growth_term * coherence_efficiency)
    )
    perceived_adjust = 1 + new_perceived_param * mp.log(p["D_eff"] / 25)
    quirk_mod = (
        mp.exp(consciousness_factor * phase_variance) * mp.cos(p["delta_psi"] + phase_variance)
        if p["observed"]
        else mp.mpf(1)
    )
    term1 = term1_base * perceived_adjust * quirk_mod
    term2 = p["scale"] * p["amplitude"] + p["trend_bias"]
    term3 = (
        beta
        * mp.cos(p["delta_psi"])
        * (p["N"] * p["P"] / mp.sqrt(p["D_eff"]))
        * (1 + chaos_factor * (p["D_eff"] - 25) / 25)
        * (1 + poof_factor * mp.cos(theta_s + pi) + suction_factor * mp.sin(theta_s))
        * (
            1
            + acoustic_bleed * (mp.sin(p["delta_theta"]) ** 2) / phi
            + acoustic_inflow * (mp.cos(p["delta_theta"]) ** 2) / phi
        )
        * (1 + bleed_in_factor * phase_variance)
    )
    raw_S = term1 + term2 + term3
    return float(raw_S * k)


def map_to_fsot_params(pressure_hpa: float, wind_speed: float, precip_mm: float, observed: bool = True) -> dict:
    std_pressure = 1013.25
    delta_psi = (pressure_hpa - std_pressure) / 50.0
    recent_hits = min(3.0, max(0.0, (wind_speed / 10.0) + (precip_mm * 0.5)))
    turbulence_activity = min(1.0, max(0.0, (wind_speed / 20.0) + (precip_mm * 0.3)))
    raw_moisture = min(1.0, max(0.0, precip_mm * 0.8))
    moisture_activity = raw_moisture * (1.0 - 0.4 * turbulence_activity)
    moisture_raw = min(1.0, max(0.0, precip_mm / 5.0))
    rad_cloud = min(1.0, max(0.0, precip_mm / 4.0))
    bl_raw = min(1.0, max(0.0, (wind_speed / 15.0) + (precip_mm * 0.15)))
    effective_moisture_weight = 1.0 - 0.6 * rad_cloud
    moisture_threshold_effect = 1.0 + 0.4 * max(0.0, moisture_raw - 0.3)
    clear_factor = max(0.2, 1.0 - 0.85 * min(1.0, (precip_mm / 3.0) + (wind_speed / 20.0)))
    return {
        "N": 1.0,
        "P": 1.0,
        "D_eff": 15.0,
        "recent_hits": recent_hits,
        "delta_psi": float(delta_psi),
        "delta_theta": 1.0,
        "rho": 1.0,
        "scale": 1.0,
        "amplitude": 1.0,
        "trend_bias": 0.0,
        "observed": observed,
        "turbulence_activity": float(turbulence_activity),
        "moisture_activity": float(moisture_activity),
        "radiation_coupling": 0.30 * clear_factor + 0.10 * max(0.0, clear_factor - 0.5),
        "boundary_layer_turbulence": float(bl_raw * effective_moisture_weight),
        "moisture_phase_threshold": float(
            moisture_raw * effective_moisture_weight * moisture_threshold_effect
        ),
        "orography_wave_drag": float(min(1.0, max(0.0, wind_speed / 25.0))),
        "radiation_cloud_interaction": float(rad_cloud),
        "orography_observer_interaction": float(min(1.0, max(0.0, wind_speed / 30.0))),
        "da_observer_strength": 1.0 if observed else 0.5,
    }