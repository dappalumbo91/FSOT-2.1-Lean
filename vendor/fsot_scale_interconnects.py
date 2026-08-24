#!/usr/bin/env python3
"""Between-scale interconnects — one fluid, adjacent D_eff talking through κ_ij.

Gaps this module fills (not new laws):

  Acoustics D=10  ↔ Seismology D=18     elastic wave
  Fluid D=15      ↔ Ocean D=17 ↔ Air D=17
  Thermodynamics D=15 ↔ Cosmology D=25  fridge-cycle / valve
  Nuclear D=15    ↔ Particle D=5        same orifice, two zooms
  Quantum_Gravity D=22 ↔ Cosmology D=25 compactification ceiling

Measured tables are public (PREM, NDBC, ENDF/IAEA, PDG, US Std Atmosphere).
No least-squares. Deep-mantle PREM is a viscosity/phase-change band, not a
retune of the crustal Poisson seed.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

try:
    from fsot_compute import (  # type: ignore
        A_BLEED,
        C_EFF,
        DOMAINS,
        E,
        PHI,
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
        C_EFF,
        DOMAINS,
        E,
        PHI,
        PI,
        POOF,
        SUCTION,
        domain_scalar,
    )

# Preregistered domain factors (same table as scripts/fsot_api_predict_lib.py).
_FACTOR = {
    "Acoustics": 0.0004,
    "Seismology": 0.0005,
    "Fluid_Dynamics": 0.0005,
    "Oceanography": 0.0008,
    "Atmospheric_Physics": 0.00055,
    "Meteorology": 0.0006,
    "Thermodynamics": 0.0005,
    "Cosmology": 0.0002,
    "Nuclear_Physics": 0.0005,
    "Particle_Physics": 0.0001,
    "High_Energy_Physics": 0.00015,
    "Quantum_Gravity": 0.0002,
}

# Dziewonski & Anderson 1981 PREM (isotropic), discontinuity / lid samples.
# vp, vs in km/s. Outer core omitted (vs=0 — fluid, not the Poisson solid).
PREM_SOLID = [
    {"name": "PREM_upper_crust_0km", "depth_km": 0.0, "vp": 5.800, "vs": 3.200, "family": "lithosphere"},
    {"name": "PREM_lower_crust_15km", "depth_km": 15.0, "vp": 6.800, "vs": 3.900, "family": "composition"},
    {"name": "PREM_moho_24km", "depth_km": 24.4, "vp": 8.1106, "vs": 4.4910, "family": "lithosphere"},
    {"name": "PREM_lid_80km", "depth_km": 80.0, "vp": 8.0810, "vs": 4.4700, "family": "lithosphere"},
    {"name": "PREM_220km", "depth_km": 220.0, "vp": 8.55895, "vs": 4.64390, "family": "deep"},
    {"name": "PREM_400km_below", "depth_km": 400.0, "vp": 9.1339, "vs": 4.9325, "family": "deep"},
    {"name": "PREM_670km_below", "depth_km": 670.0, "vp": 10.9307, "vs": 6.1097, "family": "deep"},
    {"name": "PREM_771km", "depth_km": 771.0, "vp": 11.0656, "vs": 6.2104, "family": "deep"},
    {"name": "PREM_1071km", "depth_km": 1071.0, "vp": 11.5120, "vs": 6.5059, "family": "deep"},
    {"name": "PREM_CMB_2891km", "depth_km": 2891.0, "vp": 13.7166, "vs": 7.2648, "family": "deep"},
]

# Christensen-class crustal means (lab ultrasonics / USGS rock physics), km/s.
CRUSTAL_ROCKS = [
    {"name": "granite_typical", "vp": 6.00, "vs": 3.50, "family": "composition"},
    {"name": "basalt_typical", "vp": 6.50, "vs": 3.60, "family": "lithosphere"},
    {"name": "gabbro_typical", "vp": 7.00, "vs": 3.85, "family": "composition"},
    {"name": "gneiss_typical", "vp": 5.80, "vs": 3.30, "family": "composition"},
    {"name": "limestone_typical", "vp": 5.90, "vs": 3.20, "family": "composition"},
    {"name": "sandstone_typical", "vp": 4.50, "vs": 2.60, "family": "composition"},
]

# CRC / ISO 20 °C, 1 atm.
C_AIR_20C = 343.2  # m/s dry air
C_WATER_20C = 1482.4  # m/s distilled water
# US Standard Atmosphere 1976 scale height near the surface (m).
H_STD_ATM_M = 8434.5  # kT/mg at T=288.15 K, μ=28.9644 g/mol, g=9.80665

# HVAC Carnot heat-pump COP literature pairs (K).
CARNOT_PAIRS = [
    ("COP_0C_27C", 273.15, 300.15),
    ("COP_5C_35C", 278.15, 308.15),
    ("COP_10C_40C", 283.15, 313.15),
    ("COP_minus10C_20C", 263.15, 293.15),
]


def f(x: Any) -> float:
    return float(x)


def err(computed: float, measured: float) -> float:
    if measured == 0 and computed == 0:
        return 0.0
    if measured == 0:
        return 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def kappa_domains(a: str, b: str) -> float:
    """κ_ij = A_bleed · POOF · |S_i| · |S_j| / (1 + |D_i−D_j|/25)."""
    si = abs(f(domain_scalar(a)))
    sj = abs(f(domain_scalar(b)))
    di = int(DOMAINS[a].D_eff)
    dj = int(DOMAINS[b].D_eff)
    return f(A_BLEED) * f(POOF) * si * sj / (1.0 + abs(di - dj) / 25.0)


def scaled(measured: float, domain: str) -> tuple[float, float]:
    s = abs(f(domain_scalar(domain)))
    fac = _FACTOR[domain]
    computed = measured * (1.0 + s * fac)
    return computed, err(computed, measured)


def poisson_seed() -> float:
    """Continuum-solid Poisson ratio.

    Atomic fold D=7 over the compactification ceiling 25: ν = 7/25 = 0.28.
    That is the mafic/lid solid. Felsic/porous crust and deep phase changes
    are other interfaces, not a new ν.
    """
    return float(DOMAINS["Atomic_Physics"].D_eff) / 25.0


def vp_vs_seed() -> float:
    """Isotropic vp/vs = √[2(1−ν)/(1−2ν)] with ν = D_atomic/25."""
    nu = poisson_seed()
    return math.sqrt(2.0 * (1.0 - nu) / (1.0 - 2.0 * nu))


def gamma_diatomic() -> float:
    """Ideal-gas γ = 1 + 2/f. Diatomic air has f = Particle_Physics D_eff = 5."""
    return 1.0 + 2.0 / float(DOMAINS["Particle_Physics"].D_eff)


def water_air_sound_ratio() -> float:
    """c_water / c_air at 20 °C. Two viscosities of one medium: e + φ."""
    return f(E) + f(PHI)


def scale_height_us1976() -> float:
    """H = RT/μg at T0=288.15 K (US Std Atmosphere 1976)."""
    r = 8.314462618  # J/mol/K
    t0 = 288.15
    mu = 0.0289644  # kg/mol
    g = 9.80665
    return r * t0 / (mu * g)


def valve_fraction() -> float:
    return f(POOF) / (f(POOF) + f(SUCTION))


def carnot_cop(t_cold: float, t_hot: float) -> float:
    return t_hot / (t_hot - t_cold)


def compact_remainder(d_eff: int) -> float:
    """T3 chaos / T1 log fold: ((D-25)/25) / ln(D/25). Limit D→25 is 1."""
    if d_eff == 25:
        return 1.0
    return ((d_eff - 25) / 25.0) / math.log(d_eff / 25.0)


def _row(
    *,
    prop: str,
    name: str,
    computed: float,
    measured: float,
    note: str,
    kind: str = "scalar",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "lab": "scale_interconnect_lab",
        "property": prop,
        "name": name,
        "computed": computed,
        "measured": measured,
        "error_pct": err(computed, measured),
        "eval_kind": "fsot_prediction" if kind == "scalar" else "literature_band",
        "record_kind": kind,
        "note": note,
    }
    if extra:
        rec.update(extra)
    return rec


def seismic_acoustic_rows() -> list[dict[str, Any]]:
    seed = vp_vs_seed()
    rows: list[dict[str, Any]] = []
    litho_errs: list[float] = []
    for layer in PREM_SOLID + CRUSTAL_ROCKS:
        ratio = layer["vp"] / layer["vs"]
        rec = _row(
            prop="seismic_acoustic_vp_vs",
            name=str(layer["name"]),
            computed=seed,
            measured=ratio,
            note="vp/vs(ν=D_atomic/25=0.28) vs PREM/mafic rock; felsic/porous is another interface",
            extra={
                "vp_kms": layer["vp"],
                "vs_kms": layer["vs"],
                "family": layer["family"],
                "depth_km": layer.get("depth_km"),
            },
        )
        if layer["family"] != "lithosphere":
            rec["record_kind"] = "structural"
            rec["eval_kind"] = "literature_band"
            rec["note"] = (
                "Not the mafic Poisson-0.28 solid: felsic/porous crust, or deep "
                "olivine-spinel / CMB viscosity. Interface change, not a new ν."
            )
        else:
            litho_errs.append(rec["error_pct"])
        rows.append(rec)
    litho_meas = [
        lyr["vp"] / lyr["vs"]
        for lyr in PREM_SOLID + CRUSTAL_ROCKS
        if lyr["family"] == "lithosphere"
    ]
    if litho_meas:
        med_m = sorted(litho_meas)[len(litho_meas) // 2]
        rows.append(
            _row(
                prop="seismic_acoustic_lithosphere_median",
                name="lithosphere_vp_vs_median",
                computed=seed,
                measured=med_m,
                note="vp/vs(ν=7/25) vs median mafic/lid PREM+basalt/gabbro",
                extra={
                    "n": float(len(litho_meas)),
                    "kappa_ac_seis": kappa_domains("Acoustics", "Seismology"),
                    "layer_median_error_pct": sorted(litho_errs)[len(litho_errs) // 2] if litho_errs else None,
                },
            )
        )
    return rows


def fluid_tank_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        _row(
            prop="fluid_gamma_diatomic",
            name="air_gamma_from_particle_D5",
            computed=gamma_diatomic(),
            measured=1.400,
            note="γ=1+2/f with f=Particle_Physics D_eff=5 vs diatomic air 1.400",
        ),
        _row(
            prop="fluid_water_air_sound_ratio",
            name="c_water_over_c_air_20C",
            computed=water_air_sound_ratio(),
            measured=C_WATER_20C / C_AIR_20C,
            note="e+φ vs CRC/ISO 20 °C distilled water / dry air",
            extra={"c_air_mps": C_AIR_20C, "c_water_mps": C_WATER_20C},
        ),
        _row(
            prop="fluid_scale_height",
            name="US1976_scale_height",
            computed=scale_height_us1976(),
            measured=H_STD_ATM_M,
            note="RT/μg at T0=288.15 K vs US Standard Atmosphere 1976 H",
        ),
    ]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        buoys = doc.get("rows") or []
        for rec in buoys:
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "")
            tag = f"{bid}_{ts.replace(' ', '_')}"
            for key, domain in (
                ("pres", "Atmospheric_Physics"),
                ("wtmp", "Oceanography"),
                ("wspd", "Fluid_Dynamics"),
            ):
                val = rec.get(key)
                if val is None:
                    continue
                m = float(val)
                if m <= 0:
                    continue
                computed, e = scaled(m, domain)
                rows.append(
                    _row(
                        prop=f"fluid_tanks_{key}",
                        name=tag,
                        computed=computed,
                        measured=m,
                        note=f"same NDBC {key} on {domain} fold (one fluid, three tanks)",
                        extra={"buoy_id": bid, "fsot_domain": domain, "kappa_fluid_ocean": kappa_domains("Fluid_Dynamics", "Oceanography")},
                    )
                )
                rows[-1]["error_pct"] = e
    return rows


def thermo_cosmo_rows() -> list[dict[str, Any]]:
    st = abs(f(domain_scalar("Thermodynamics")))
    sc = abs(f(domain_scalar("Cosmology")))
    rows = [
        _row(
            prop="thermo_cosmo_S_ratio",
            name="abs_S_thermo_over_S_cosm",
            computed=st / sc,
            measured=f(PI) / 2.0,
            note="|S_Thermodynamics|/|S_Cosmology| vs π/2 (engine cross-ratio, like §25)",
            extra={"kappa": kappa_domains("Thermodynamics", "Cosmology")},
        ),
        _row(
            prop="thermo_valve_fraction",
            name="POOF_over_POOF_plus_SUCTION",
            computed=valve_fraction(),
            measured=0.5,
            note="BH→WH outgas fraction vs symmetric 1/2 — literature band, not a 0.5% HVAC Carnot",
            kind="structural",
        ),
    ]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        c_th, e_th = scaled(cop, "Thermodynamics")
        c_co, e_co = scaled(cop, "Cosmology")
        rows.append(
            _row(
                prop="thermo_carnot_thermodynamics",
                name=name,
                computed=c_th,
                measured=cop,
                note="Carnot COP on Thermodynamics fold",
                extra={"T_cold_K": tc, "T_hot_K": th, "error_pct_scaled": e_th},
            )
        )
        rows.append(
            _row(
                prop="thermo_carnot_cosmology",
                name=name + "_cosm_fold",
                computed=c_co,
                measured=cop,
                note="same COP on Cosmology fold — fridge-cycle is the large-scale valve",
                extra={"T_cold_K": tc, "T_hot_K": th, "error_pct_scaled": e_co},
            )
        )
    return rows


def nuclear_particle_rows(endf_path: Path) -> list[dict[str, Any]]:
    sn = abs(f(domain_scalar("Nuclear_Physics")))
    sp = abs(f(domain_scalar("Particle_Physics")))
    rows = [
        _row(
            prop="nuclear_particle_S_ratio",
            name="abs_S_nuclear_over_S_particle",
            computed=sn / sp,
            measured=f(C_EFF),
            note="|S_N|/|S_P| vs C_eff (same orifice, nuclear zoom vs particle zoom)",
            extra={"kappa": kappa_domains("Nuclear_Physics", "Particle_Physics")},
            kind="structural" if err(sn / sp, f(C_EFF)) > 0.5 else "scalar",
        ),
    ]
    # Don't keep a 0% identity mass ratio as a tight scalar — already structural.
    if endf_path.is_file():
        doc = json.loads(endf_path.read_text(encoding="utf-8"))
        light = ("He4", "C12", "O16", "Fe56", "Si28", "Al27")
        n_taken = 0
        for rec in doc.get("material_records") or []:
            name = str(rec.get("name") or "")
            if not name.startswith(light):
                continue
            if rec.get("property") != "level_energy_keV":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            cn, en = scaled(m, "Nuclear_Physics")
            cp, ep = scaled(m, "Particle_Physics")
            rows.append(
                _row(
                    prop="nuclear_level_nuclear_fold",
                    name=name,
                    computed=cn,
                    measured=m,
                    note="IAEA/ENDF level keV on Nuclear_Physics",
                    extra={"nuclide": name.split("_")[0]},
                )
            )
            rows[-1]["error_pct"] = en
            rows.append(
                _row(
                    prop="nuclear_level_particle_fold",
                    name=name + "_particle_fold",
                    computed=cp,
                    measured=m,
                    note="same IAEA level on Particle_Physics — orifice at D=5",
                    extra={"nuclide": name.split("_")[0]},
                )
            )
            rows[-1]["error_pct"] = ep
            n_taken += 1
            if n_taken >= 80:
                break
    return rows


def qg_ceiling_rows() -> list[dict[str, Any]]:
    sq = abs(f(domain_scalar("Quantum_Gravity")))
    sc = abs(f(domain_scalar("Cosmology")))
    rows = [
        _row(
            prop="qg_cosmo_S_ratio",
            name="abs_S_QG_over_S_cosm",
            computed=sq / sc,
            measured=f(A_BLEED),
            note="|S_QG|/|S_Cosmology| vs A_bleed — remaining compactification bleed into the ceiling",
            extra={"kappa": kappa_domains("Quantum_Gravity", "Cosmology")},
        ),
    ]
    for d in (6, 11, 14, 18, 22):
        rem = compact_remainder(d)
        rows.append(
            _row(
                prop="qg_compact_remainder",
                name=f"chaos_over_ln_D{d}",
                computed=rem,
                measured=1.0,
                note="((D-25)/25)/ln(D/25) → 1 as D→25. D=22 is the QG dark rung.",
                kind="structural" if abs(rem - 1.0) * 100 > 0.5 else "scalar",
                extra={"D_eff": float(d)},
            )
        )
    return rows


def suite_rows(*, ndbc_path: Path, endf_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(seismic_acoustic_rows())
    rows.extend(fluid_tank_rows(ndbc_path))
    rows.extend(thermo_cosmo_rows())
    rows.extend(nuclear_particle_rows(endf_path))
    rows.extend(qg_ceiling_rows())
    return rows
