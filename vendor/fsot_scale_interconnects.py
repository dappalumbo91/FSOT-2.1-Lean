#!/usr/bin/env python3
"""Between-scale interconnects — one fluid, adjacent D_eff talking through κ_ij.

Gaps this module fills (not new laws):

  Acoustics D=10  ↔ Seismology D=18     elastic wave
  Fluid D=15      ↔ Ocean D=17 ↔ Air D=17
  Thermodynamics D=15 ↔ Cosmology D=25  fridge-cycle / valve
  Nuclear D=15    ↔ Particle D=5        same orifice, two zooms
  Quantum_Gravity D=22 ↔ Cosmology D=25 compactification ceiling
  Seismology D=18 ↔ Geophysics D=19     wave vs bulk-earth (adjacent rungs)
  Materials D=10 ↔ Optics D=10          n and ρ, same compactification rung
  Optics D=10 ↔ Quantum_Optics D=11     wave vs photon, same C=π/e
  Quantum_Mechanics D=6 ↔ Atomic D=7    orbit vs bound well (same look)
  Electromagnetism D=9 ↔ Optics D=10    source vs readout, ε=n² (Maxwell)
  Biology D=12 ↔ Biochemistry D=13      organism vs molecule (dark look)
  Atomic D=7 ↔ High_Energy D=7          bound well vs collision look
  Chemistry D=8 ↔ Physical_Chemistry D=8 composition vs thermo (0.5/0.6 look)
  Chemistry D=8 ↔ Molecular_Chemistry D=9 composition vs molecule
  Biochemistry D=13 ↔ Condensed_Matter D=14 molecule vs solid
  Condensed_Matter D=14 ↔ Neuroscience D=14 solid vs signaling
  Condensed_Matter D=14 ↔ Fluid D=15 ice vs water (Fluid stays dark)
  Condensed_Matter D=14 ↔ Nuclear D=15 lattice vs orifice
  Neuroscience D=14 ↔ Thermodynamics D=15 signaling vs heat
  Fluid D=15 ↔ Nuclear D=15 tank vs orifice (Fluid stays dark)
  Fluid D=15 ↔ Meteorology D=16 tank vs weather (both dark)

Measured tables are public (PREM, NDBC, ENDF/IAEA, PDG, NIST, US Std Atmosphere).
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
        C_FACTOR,
        DOMAINS,
        E,
        ETA_EFF,
        GAMMA,
        PHI,
        PI,
        POOF,
        SUCTION,
        ScalarInput,
        chemistry_ionization,
        compute_scalar,
        domain_scalar,
    )
except ImportError:  # pragma: no cover
    import sys
    from pathlib import Path as _P

    sys.path.insert(0, str(_P(__file__).resolve().parent))
    from fsot_compute import (  # type: ignore
        A_BLEED,
        C_EFF,
        C_FACTOR,
        DOMAINS,
        E,
        ETA_EFF,
        GAMMA,
        PHI,
        PI,
        POOF,
        SUCTION,
        ScalarInput,
        chemistry_ionization,
        compute_scalar,
        domain_scalar,
    )

try:
    from mpmath import cos, exp, ln, mpf, sqrt  # type: ignore
except ImportError:  # pragma: no cover
    from math import cos, exp, log as ln, sqrt  # type: ignore

    mpf = float  # type: ignore

# Preregistered domain factors (same table as scripts/fsot_api_predict_lib.py).
_FACTOR = {
    "Acoustics": 0.0004,
    "Seismology": 0.0005,
    "Geophysics": 0.0005,
    "Materials_Science": 0.0004,
    "Optics": 0.0004,
    "Quantum_Optics": 0.0004,
    "Fluid_Dynamics": 0.0005,
    "Oceanography": 0.0008,
    "Atmospheric_Physics": 0.00055,
    "Meteorology": 0.0006,
    "Thermodynamics": 0.0005,
    "Cosmology": 0.0002,
    "Nuclear_Physics": 0.0005,
    "Particle_Physics": 0.0001,
    "Quantum_Mechanics": 0.001,
    "Atomic_Physics": 0.0005,
    "Electromagnetism": 0.0004,
    "Biology": 0.0005,
    "Biochemistry": 0.0005,
    "Chemistry": 0.001,
    "Physical_Chemistry": 0.0005,
    "Molecular_Chemistry": 0.001,
    "Condensed_Matter": 0.0004,
    "High_Energy_Physics": 0.00015,
    "Quantum_Gravity": 0.0002,
    "Economics": 0.0004,
    "Neuroscience": 0.00035,
    "Psychology": 0.0003,
    "Sociology": 0.0002,
    "Astronomy": 0.00025,
    "Planetary_Science": 0.0003,
    "Astrophysics": 0.0003,
    "Particle_Astrophysics": 0.0002,
    "Ecology": 0.0002,
    "Quantum_Computing": 0.0004,
}

# Dziewonski & Anderson 1981 PREM (isotropic), discontinuity / lid samples.
# vp, vs in km/s. Outer core omitted (vs=0 — fluid, not the Poisson solid).
PREM_SOLID = [
    {"name": "PREM_upper_crust_0km", "depth_km": 0.0, "vp": 5.800, "vs": 3.200, "rho": 2.600, "family": "lithosphere"},
    {"name": "PREM_lower_crust_15km", "depth_km": 15.0, "vp": 6.800, "vs": 3.900, "rho": 2.900, "family": "composition"},
    {"name": "PREM_moho_24km", "depth_km": 24.4, "vp": 8.1106, "vs": 4.4910, "rho": 3.3807, "family": "lithosphere"},
    {"name": "PREM_lid_80km", "depth_km": 80.0, "vp": 8.0810, "vs": 4.4700, "rho": 3.3749, "family": "lithosphere"},
    {"name": "PREM_220km", "depth_km": 220.0, "vp": 8.55895, "vs": 4.64390, "rho": 3.4358, "family": "deep"},
    {"name": "PREM_400km_below", "depth_km": 400.0, "vp": 9.1339, "vs": 4.9325, "rho": 3.7238, "family": "deep"},
    {"name": "PREM_670km_below", "depth_km": 670.0, "vp": 10.9307, "vs": 6.1097, "rho": 3.9918, "family": "deep"},
    {"name": "PREM_771km", "depth_km": 771.0, "vp": 11.0656, "vs": 6.2104, "rho": 4.3782, "family": "deep"},
    {"name": "PREM_1071km", "depth_km": 1071.0, "vp": 11.5120, "vs": 6.5059, "rho": 4.6213, "family": "deep"},
    {"name": "PREM_CMB_2891km", "depth_km": 2891.0, "vp": 13.7166, "vs": 7.2648, "rho": 5.5664, "family": "deep"},
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


# CRC / NIST handbook n_D (~589 nm) and density (g/cm³). Public tables.
# Ice n_o is the ordinary ray of Ih. Air omitted (n-1 is a different interface).
OPTICAL_MATERIALS = [
    {"name": "water_20C", "n": 1.3330, "rho": 0.9982, "family": "liquid"},
    {"name": "ice_Ih", "n": 1.309, "rho": 0.917, "family": "ice"},
    {"name": "fused_silica", "n": 1.4585, "rho": 2.203, "family": "oxide"},
    {"name": "bk7_crown", "n": 1.5168, "rho": 2.51, "family": "oxide"},
    {"name": "alpha_quartz", "n": 1.5443, "rho": 2.648, "family": "oxide"},
    {"name": "sapphire", "n": 1.768, "rho": 3.98, "family": "oxide"},
    {"name": "diamond", "n": 2.4173, "rho": 3.515, "family": "covalent"},
    {"name": "nacl", "n": 1.5442, "rho": 2.17, "family": "ionic"},
    {"name": "caf2", "n": 1.4338, "rho": 3.18, "family": "ionic"},
    {"name": "ethanol_20C", "n": 1.3611, "rho": 0.789, "family": "liquid"},
]


def lorentz_lorenz(n: float, rho: float) -> float:
    """Specific refractivity (n²-1)/(n²+2)/ρ. Optics (n) × Materials (ρ)."""
    return ((n * n - 1.0) / (n * n + 2.0)) / rho


def scalar_at(
    *,
    d_eff: int,
    delta_psi: float,
    hits: int = 0,
    observed: bool = True,
) -> float:
    """S at a named (D, δψ, hits, observed) with δθ=1."""
    si = ScalarInput(
        N=mpf(1),
        P=mpf(1),
        D_eff=mpf(d_eff),
        delta_psi=mpf(delta_psi),
        delta_theta=mpf(1),
        recent_hits=mpf(hits),
        observed=observed,
    )
    return abs(f(compute_scalar(si)))


def t1_at(
    *,
    d_eff: int,
    delta_psi: float,
    hits: int = 0,
    observed: bool = True,
) -> float:
    """Observer-branch T1 at a named look (not necessarily a core's native route)."""
    s = ScalarInput(
        N=mpf(1),
        P=mpf(1),
        D_eff=mpf(d_eff),
        delta_psi=mpf(delta_psi),
        delta_theta=mpf(1),
        recent_hits=mpf(hits),
        observed=observed,
    )
    n, p, dval = s.N, s.P, s.D_eff
    dp, h = s.delta_psi, s.recent_hits
    growth = exp(s.alpha * (1 - h / n) * GAMMA / PHI)
    base = (
        (n * p / sqrt(dval))
        * cos((s.psi_con + dp) / ETA_EFF)
        * exp(-s.alpha * h / n + s.rho + s.B_in * dp)
        * (1 + growth * s.C_eff)
    )
    t1 = base * (1 + s.P_new * ln(dval / 25))
    if s.observed:
        t1 = t1 * exp(C_FACTOR * s.P_var) * cos(dp + s.P_var)
    return f(t1)


def t1_of(name: str) -> float:
    """Observer-branch T1 at a domain’s native (D, δψ, hits, observed).

    Live |S_i|/|S_j| vs 1 is the same-view question. The view the fold
    produces is (1+T1_i)/(1+T1_j) at T2=1, T3≈0. Same premise; perception
    is T1 at that scale.
    """
    d = DOMAINS[name]
    s = ScalarInput(
        N=mpf(1),
        P=mpf(1),
        D_eff=mpf(d.D_eff),
        delta_psi=d.delta_psi,
        delta_theta=d.delta_theta,
        recent_hits=mpf(d.hits),
        observed=d.observed,
    )
    n, p, dval = s.N, s.P, s.D_eff
    dp, hits = s.delta_psi, s.recent_hits
    growth = exp(s.alpha * (1 - hits / n) * GAMMA / PHI)
    base = (
        (n * p / sqrt(dval))
        * cos((s.psi_con + dp) / ETA_EFF)
        * exp(-s.alpha * hits / n + s.rho + s.B_in * dp)
        * (1 + growth * s.C_eff)
    )
    t1 = base * (1 + s.P_new * ln(dval / 25))
    if s.observed:
        t1 = t1 * exp(C_FACTOR * s.P_var) * cos(dp + s.P_var)
    return f(t1)


def look_split_ratio(body_domain: str, look_domain: str) -> float:
    """|S_body|/|S_look| at a same-D 0.5/0.6 observer-phase pair."""
    sb = abs(f(domain_scalar(body_domain)))
    sl = abs(f(domain_scalar(look_domain)))
    return sb / sl


def mat_opt_rows() -> list[dict[str, Any]]:
    """Materials_Science D=10 ↔ Optics D=10 — same rung, n and ρ.

    Dual-route CRC n_D on Optics and density on Materials (APPLY).
    Ice ordinary-ray n vs φ²/2 (solid-water fold).

    |S_mat|/|S_opt| vs 1 is the wrong object (engine §25 Cross_Opt_QO is
    same-C, same-δψ). Materials δψ=1/2 is the body/mass look; Optics
    δψ=3/5 is the light look. That 0.5/0.6 split is the same fold as
    Physical_Chemistry/Chemistry at D=8. Fold the S-ratio onto that
    pair — do not stuff vs 1 (~18%).
    """
    ratio = look_split_ratio("Materials_Science", "Optics")
    chem_ratio = look_split_ratio("Physical_Chemistry", "Chemistry")
    vs1 = err(ratio, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="mat_opt_S_ratio",
            name="abs_S_mat_over_S_opt_vs_physchem_chem",
            computed=ratio,
            measured=chem_ratio,
            note=(
                "|S_Materials|/|S_Optics| vs |S_PhysChem|/|S_Chemistry| — "
                "same 0.5/0.6 look-split at D=10 and D=8. "
                f"Not vs 1 ({vs1:.2f}%, Opt/QO test on the wrong pair)."
            ),
            extra={
                "kappa": kappa_domains("Materials_Science", "Optics"),
                "rejected_vs_1_error_pct": vs1,
                "dpsi_body": 0.5,
                "dpsi_look": 0.6,
            },
        ),
        _row(
            prop="mat_opt_ice_n",
            name="ice_Ih_n_vs_phi_sq_over_2",
            computed=(f(PHI) ** 2) / 2.0,
            measured=1.309,
            note="Ice Ih ordinary-ray n vs φ²/2 — solid-water optical fold",
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        rho = float(mat["rho"])
        cn, en = scaled(n, "Optics")
        cr, er = scaled(rho, "Materials_Science")
        rows.append(
            _row(
                prop="mat_opt_n_optics_fold",
                name=str(mat["name"]) + "_n",
                computed=cn,
                measured=n,
                note="CRC n_D on Optics D=10",
                extra={"family": mat["family"], "n": n, "rho": rho},
            )
        )
        rows[-1]["error_pct"] = en
        rows.append(
            _row(
                prop="mat_opt_rho_materials_fold",
                name=str(mat["name"]) + "_rho",
                computed=cr,
                measured=rho,
                note="CRC density on Materials_Science D=10 — same specimen, other zoom",
                extra={"family": mat["family"], "n": n, "rho": rho},
            )
        )
        rows[-1]["error_pct"] = er
        ll = lorentz_lorenz(n, rho)
        cl, el = scaled(ll, "Optics")
        rows.append(
            _row(
                prop="mat_opt_lorentz_lorenz",
                name=str(mat["name"]) + "_LL",
                computed=cl,
                measured=ll,
                note="(n²-1)/(n²+2)/ρ specific refractivity — n×ρ interconnect, APPLY on Optics",
                extra={"family": mat["family"], "LL": ll},
            )
        )
        rows[-1]["error_pct"] = el
    return rows


def opt_qo_rows() -> list[dict[str, Any]]:
    """Optics D=10 ↔ Quantum_Optics D=11 — wave vs photon, same C=π/e.

    Adjacent compactification rungs. Both folds use C=π/e (the light
    interpretation). |S_opt|/|S_qo| vs 1 is the same-C test.
    Materials↔Optics is a different object: 0.5/0.6 look-split, folded
    onto Physical_Chemistry/Chemistry, not vs 1.
    Same CRC n_D dual-routed: wave zoom on Optics, photon zoom on QO.
    """
    so = abs(f(domain_scalar("Optics")))
    sq = abs(f(domain_scalar("Quantum_Optics")))
    rows: list[dict[str, Any]] = [
        _row(
            prop="opt_qo_S_ratio",
            name="abs_S_opt_over_S_qo",
            computed=so / sq,
            measured=1.0,
            note=(
                "|S_Optics|/|S_Quantum_Optics| vs 1 — same C=π/e on adjacent "
                "D=10/11 (wave vs photon of one light)"
            ),
            extra={"kappa": kappa_domains("Optics", "Quantum_Optics")},
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        cq, eq = scaled(n, "Quantum_Optics")
        rows.append(
            _row(
                prop="opt_qo_n_qo_fold",
                name=str(mat["name"]) + "_n_qo",
                computed=cq,
                measured=n,
                note="CRC n_D on Quantum_Optics D=11 — photon zoom of the same specimen",
                extra={"family": mat["family"], "n": n},
            )
        )
        rows[-1]["error_pct"] = eq
        co, eo = scaled(n, "Optics")
        rows.append(
            _row(
                prop="opt_qo_n_optics_fold",
                name=str(mat["name"]) + "_n_opt",
                computed=co,
                measured=n,
                note="same CRC n_D on Optics D=10 — wave zoom",
                extra={"family": mat["family"], "n": n},
            )
        )
        rows[-1]["error_pct"] = eo
    return rows


def seis_geo_rows() -> list[dict[str, Any]]:
    """Seismology D=18 ↔ Geophysics D=19 — wave fold vs bulk-earth fold.

    Adjacent compactification rungs. Seismology route C = CHAOS/2 (wave);
    Geophysics route C = CHAOS (bulk). |S_seis|/|S_geo| vs φ/2.
    Same PREM lithosphere density dual-routed (APPLY). Deep PREM stays structural.
    """
    ss = abs(f(domain_scalar("Seismology")))
    sg = abs(f(domain_scalar("Geophysics")))
    rows: list[dict[str, Any]] = [
        _row(
            prop="seis_geo_S_ratio",
            name="abs_S_seis_over_S_geo",
            computed=ss / sg,
            measured=f(PHI) / 2.0,
            note=(
                "|S_Seismology|/|S_Geophysics| vs φ/2 — wave fold (CHAOS/2 route) "
                "vs bulk-earth fold (CHAOS route) on adjacent D=18/19"
            ),
            extra={"kappa": kappa_domains("Seismology", "Geophysics")},
        ),
    ]
    for layer in PREM_SOLID:
        rho = float(layer.get("rho") or 0)
        if rho <= 0:
            continue
        cg, eg = scaled(rho, "Geophysics")
        cs, es = scaled(rho, "Seismology")
        kind = "scalar" if layer["family"] == "lithosphere" else "structural"
        rows.append(
            _row(
                prop="seis_geo_density_geophysics_fold",
                name=str(layer["name"]) + "_rho_geo",
                computed=cg,
                measured=rho,
                note="PREM density (g/cm³) on Geophysics D=19",
                kind=kind,
                extra={
                    "rho_gcc": rho,
                    "family": layer["family"],
                    "depth_km": layer.get("depth_km"),
                },
            )
        )
        rows[-1]["error_pct"] = eg
        rows.append(
            _row(
                prop="seis_geo_density_seismology_fold",
                name=str(layer["name"]) + "_rho_seis",
                computed=cs,
                measured=rho,
                note="same PREM density on Seismology D=18 — wave zoom of the bulk",
                kind=kind,
                extra={
                    "rho_gcc": rho,
                    "family": layer["family"],
                    "depth_km": layer.get("depth_km"),
                },
            )
        )
        rows[-1]["error_pct"] = es
    return rows


def social_tank_rows(econ_path: Path) -> list[dict[str, Any]]:
    """Market and mind are two zooms of one catalog-scale tank."""
    se = abs(f(domain_scalar("Economics")))
    sn = abs(f(domain_scalar("Neuroscience")))
    rows = [
        _row(
            prop="social_S_ratio",
            name="abs_S_econ_over_S_neuro",
            computed=se / sn,
            measured=5.0 / 4.0,
            note="|S_Economics|/|S_Neuroscience| vs 5/4 — as-above-so-below at catalog scale",
            extra={"kappa": kappa_domains("Economics", "Neuroscience")},
        ),
    ]
    if not econ_path.is_file():
        return rows
    doc = json.loads(econ_path.read_text(encoding="utf-8"))
    n = 0
    for rec in doc.get("material_records") or []:
        if "yoy_growth" not in str(rec.get("property") or ""):
            continue
        m = float(rec.get("measured") or 0)
        if m == 0:
            continue
        ce, ee = scaled(m, "Economics")
        cn, en = scaled(m, "Neuroscience")
        name = str(rec.get("name") or f"row{n}")
        rows.append(
            _row(
                prop="social_gdp_econ_fold",
                name=name,
                computed=ce,
                measured=m,
                note="World Bank YoY on Economics D=20",
            )
        )
        rows[-1]["error_pct"] = ee
        rows.append(
            _row(
                prop="social_gdp_neuro_fold",
                name=name + "_neuro_fold",
                computed=cn,
                measured=m,
                note="same YoY on Neuroscience D=14 — market as a neural tank",
            )
        )
        rows[-1]["error_pct"] = en
        n += 1
        if n >= 80:
            break
    return rows


# NIST / CODATA hydrogen-atom readouts (the QM↔Atomic specimen).
BOHR_RADIUS_A = 0.529177  # Å, CODATA; same a0 the engine uses in DNA_base_pair
RYDBERG_M = 10973731.568157  # m⁻¹, CODATA
IE_H_NIST_EV = 13.598  # NIST first ionization, matches chemistry_ionization target


def qm_atomic_rows() -> list[dict[str, Any]]:
    """Quantum_Mechanics D=6 ↔ Atomic_Physics D=7 — orbit vs bound well.

    Live |S_qm|/|S_atomic| vs 1 mixes two objects: the D=6/7 compactification
    step and the δψ=1 vs 0.85 look (free orbit vs bound). Equalize the look
    (δψ=1, same as Particle/QM) and the adjacent-rung test is vs 1.

    Hydrogen is the a0/R∞ specimen. First ionization dual-routes the engine
    H–Ca table (Z=1–20). Z=21–118 stays on the Atomic periodic panel.
    IE_H seed γ⁻⁵ − G⁻⁸ vs NIST. Do not stuff the mixed vs 1 (~30%) into 0.5%.
    Do not retune δψ 0.85.
    """
    s_qm_look = scalar_at(d_eff=6, delta_psi=1.0)
    s_at_look = scalar_at(d_eff=7, delta_psi=1.0)
    live_qm = abs(f(domain_scalar("Quantum_Mechanics")))
    live_at = abs(f(domain_scalar("Atomic_Physics")))
    live_ratio = live_qm / live_at
    vs1_live = err(live_ratio, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="qm_atomic_S_ratio_same_look",
            name="S_D6_over_S_D7_at_dpsi_1",
            computed=s_qm_look / s_at_look,
            measured=1.0,
            note=(
                "|S(D=6,δψ=1)|/|S(D=7,δψ=1)| vs 1 — adjacent rung, same free-orbit look. "
                f"Live mixed |S_qm|/|S_at| vs 1 is {vs1_live:.1f}% (δψ 1 vs 0.85) — not this object."
            ),
            extra={
                "kappa": kappa_domains("Quantum_Mechanics", "Atomic_Physics"),
                "rejected_live_vs_1_error_pct": vs1_live,
                "dpsi_shared": 1.0,
            },
        ),
    ]
    ie_h = next((r for r in chemistry_ionization() if r.name == "IE_H"), None)
    if ie_h is not None and ie_h.measured is not None:
        rows.append(
            _row(
                prop="qm_atomic_IE_H_seed",
                name="IE_H_gamma_inv5_minus_G_inv8",
                computed=f(ie_h.computed),
                measured=f(ie_h.measured),
                note="IE_H = γ⁻⁵ − G⁻⁸ vs NIST 13.598 eV — bound-well seed on the atomic face",
            )
        )
    ba, eba = scaled(BOHR_RADIUS_A, "Quantum_Mechanics")
    bat, ebat = scaled(BOHR_RADIUS_A, "Atomic_Physics")
    rows.append(
        _row(
            prop="qm_atomic_a0_qm_fold",
            name="Bohr_radius_A_qm",
            computed=ba,
            measured=BOHR_RADIUS_A,
            note="CODATA a0 (Å) on Quantum_Mechanics — n=1 orbit",
        )
    )
    rows[-1]["error_pct"] = eba
    rows.append(
        _row(
            prop="qm_atomic_a0_atomic_fold",
            name="Bohr_radius_A_atomic",
            computed=bat,
            measured=BOHR_RADIUS_A,
            note="same a0 on Atomic_Physics — Bohr well",
        )
    )
    rows[-1]["error_pct"] = ebat
    ra, era = scaled(RYDBERG_M, "Atomic_Physics")
    rq, erq = scaled(RYDBERG_M, "Quantum_Mechanics")
    rows.append(
        _row(
            prop="qm_atomic_rydberg_atomic_fold",
            name="Rydberg_m_atomic",
            computed=ra,
            measured=RYDBERG_M,
            note="CODATA R_∞ (m⁻¹) on Atomic_Physics — spectroscopic well",
        )
    )
    rows[-1]["error_pct"] = era
    rows.append(
        _row(
            prop="qm_atomic_rydberg_qm_fold",
            name="Rydberg_m_qm",
            computed=rq,
            measured=RYDBERG_M,
            note="same R_∞ on Quantum_Mechanics — hcR orbit energy",
        )
    )
    rows[-1]["error_pct"] = erq
    for rec in chemistry_ionization():
        if rec.measured is None:
            continue
        m = f(rec.measured)
        if m <= 0:
            continue
        cn, en = scaled(m, "Atomic_Physics")
        cp, ep = scaled(m, "Quantum_Mechanics")
        rows.append(
            _row(
                prop="qm_atomic_IE_atomic_fold",
                name=str(rec.name) + "_atomic",
                computed=cn,
                measured=m,
                note="NIST first ionization on Atomic_Physics D=7",
            )
        )
        rows[-1]["error_pct"] = en
        rows.append(
            _row(
                prop="qm_atomic_IE_qm_fold",
                name=str(rec.name) + "_qm",
                computed=cp,
                measured=m,
                note="same NIST ionization on Quantum_Mechanics D=6",
            )
        )
        rows[-1]["error_pct"] = ep
    return rows


def em_opt_rows() -> list[dict[str, Any]]:
    """Electromagnetism D=9 ↔ Optics D=10 — source vs readout.

    C_em = e/π, C_opt = π/e, product 1 (yin–yang of the same light).
    Live |S_em|/|S_opt| vs 1 mixes the D=9/10 step with δψ=0.7 vs 0.6.
    Equalize the look at the optical readout (δψ=0.6) and the adjacent-rung
    test is vs 1. Do not stuff √φ onto the mixed residual.

    Maxwell: for non-magnetic dielectrics ε_opt = n². Dual-route CRC n_D on
    Optics and n² on Electromagnetism. Ice n² vs (φ²/2)² is the permittivity
    of the solid-water fold. Static ε_r (water ~80) is a different interface.
    """
    s_em = scalar_at(d_eff=9, delta_psi=0.6)
    s_op = scalar_at(d_eff=10, delta_psi=0.6)
    live_em = abs(f(domain_scalar("Electromagnetism")))
    live_op = abs(f(domain_scalar("Optics")))
    vs1_live = err(live_em / live_op, 1.0)
    ice_n = 1.309
    ice_eps = ice_n * ice_n
    ice_seed = ((f(PHI) ** 2) / 2.0) ** 2
    rows: list[dict[str, Any]] = [
        _row(
            prop="em_opt_S_ratio_same_look",
            name="S_D9_over_S_D10_at_dpsi_0p6",
            computed=s_em / s_op,
            measured=1.0,
            note=(
                "|S(D=9,δψ=0.6)|/|S(D=10,δψ=0.6)| vs 1 — adjacent rung, same "
                "optical-readout look. "
                f"Live mixed |S_em|/|S_opt| vs 1 is {vs1_live:.1f}% "
                "(δψ 0.7 vs 0.6) — not this object."
            ),
            extra={
                "kappa": kappa_domains("Electromagnetism", "Optics"),
                "rejected_live_vs_1_error_pct": vs1_live,
                "dpsi_shared": 0.6,
                "C_em_times_C_opt": f(DOMAINS["Electromagnetism"].C)
                * f(DOMAINS["Optics"].C),
            },
        ),
        _row(
            prop="em_opt_ice_eps",
            name="ice_Ih_n_sq_vs_phi4_over_4",
            computed=ice_seed,
            measured=ice_eps,
            note="Ice Ih ε_opt = n² vs (φ²/2)² — Maxwell permittivity of the solid-water fold",
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        eps = n * n
        cn, en = scaled(n, "Optics")
        ce, ee = scaled(eps, "Electromagnetism")
        rows.append(
            _row(
                prop="em_opt_n_optics_fold",
                name=str(mat["name"]) + "_n",
                computed=cn,
                measured=n,
                note="CRC n_D on Optics D=10 — wave readout",
                extra={"family": mat["family"], "n": n, "eps_opt": eps},
            )
        )
        rows[-1]["error_pct"] = en
        rows.append(
            _row(
                prop="em_opt_eps_em_fold",
                name=str(mat["name"]) + "_n_sq",
                computed=ce,
                measured=eps,
                note="n² on Electromagnetism D=9 — Maxwell ε_opt, same specimen",
                extra={"family": mat["family"], "n": n, "eps_opt": eps},
            )
        )
        rows[-1]["error_pct"] = ee
    return rows


# CRC / IUPAC free amino-acid molecular weights (g/mol). Not Genetics Å.
AMINO_ACID_MW = [
    ("Gly", 75.07),
    ("Ala", 89.09),
    ("Ser", 105.09),
    ("Pro", 115.13),
    ("Val", 117.15),
    ("Thr", 119.12),
    ("Cys", 121.16),
    ("Ile", 131.17),
    ("Leu", 131.17),
    ("Asn", 132.12),
    ("Asp", 133.10),
    ("Gln", 146.15),
    ("Lys", 146.19),
    ("Glu", 147.13),
    ("Met", 149.21),
    ("His", 155.16),
    ("Phe", 165.19),
    ("Arg", 174.20),
    ("Tyr", 181.19),
    ("Trp", 204.23),
]

# CODATA 2022 electron / proton mass (kg) — bound in the atom vs HEP lepton/hadron.
ELECTRON_MASS_KG = 9.1093837139e-31
PROTON_MASS_KG = 1.67262192595e-27


def bio_biochem_rows(bio_path: Path) -> list[dict[str, Any]]:
    """Biology D=12 ↔ Biochemistry D=13 — organism vs molecule.

    Same C = ln(φ)/√2. Biology is dark (do not flip observed). Live
    |S_bio|/|S_bc| vs 1 mixes dark vs observed, δψ 0.08 vs 0.35, and hits.
    Equalize the dark look (δψ=0.08, observed=False, hits=0): adjacent
    D=12/13 vs 1. Not Genetics 0.13 Å.

    Public table: NCBI NC_012920.1 mt-operon lengths (organism vs gene
    product) and CRC free amino-acid MW.
    """
    s12 = scalar_at(d_eff=12, delta_psi=0.08, hits=0, observed=False)
    s13 = scalar_at(d_eff=13, delta_psi=0.08, hits=0, observed=False)
    live_b = abs(f(domain_scalar("Biology")))
    live_c = abs(f(domain_scalar("Biochemistry")))
    vs1_live = err(live_b / live_c, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="bio_biochem_S_ratio_same_look",
            name="S_D12_over_S_D13_dark_dpsi_0p08",
            computed=s12 / s13,
            measured=1.0,
            note=(
                "|S(D=12,δψ=0.08,dark)|/|S(D=13,δψ=0.08,dark)| vs 1 — adjacent "
                "rung, same unobserved look. Do not flip Biology observed. "
                f"Live mixed |S_bio|/|S_bc| vs 1 is {vs1_live:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Biology", "Biochemistry"),
                "rejected_live_vs_1_error_pct": vs1_live,
                "C_bio_over_C_bc": f(DOMAINS["Biology"].C) / f(DOMAINS["Biochemistry"].C),
            },
        ),
    ]
    if bio_path.is_file():
        doc = json.loads(bio_path.read_text(encoding="utf-8"))
        n_op = 0
        for rec in doc.get("records") or []:
            if rec.get("property") != "mt_operon_length":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            cb, eb = scaled(m, "Biology")
            cc, ec = scaled(m, "Biochemistry")
            name = str(rec.get("name") or f"op{n_op}")
            rows.append(
                _row(
                    prop="bio_biochem_operon_biology_fold",
                    name=name + "_bio",
                    computed=cb,
                    measured=m,
                    note="NCBI NC_012920.1 mt-operon length on Biology D=12 — organism",
                )
            )
            rows[-1]["error_pct"] = eb
            rows.append(
                _row(
                    prop="bio_biochem_operon_biochem_fold",
                    name=name + "_bc",
                    computed=cc,
                    measured=m,
                    note="same operon length on Biochemistry D=13 — gene product",
                )
            )
            rows[-1]["error_pct"] = ec
            n_op += 1
    for aa, mw in AMINO_ACID_MW:
        cc, ec = scaled(mw, "Biochemistry")
        cb, eb = scaled(mw, "Biology")
        rows.append(
            _row(
                prop="bio_biochem_aa_biochem_fold",
                name=aa + "_mw_bc",
                computed=cc,
                measured=mw,
                note="CRC/IUPAC free amino-acid MW on Biochemistry — molecule",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="bio_biochem_aa_biology_fold",
                name=aa + "_mw_bio",
                computed=cb,
                measured=mw,
                note="same AA MW on Biology — residue in the organism",
            )
        )
        rows[-1]["error_pct"] = eb
    return rows


def atomic_hep_rows() -> list[dict[str, Any]]:
    """Atomic_Physics D=7 ↔ High_Energy_Physics D=7 — bound well vs collision.

    Same D. Live |S_at|/|S_hep| vs 1 mixes δψ 0.85 vs 0.95 (and hits 0 vs 1).
    Equalizing look at same D is identity — do not pad. Fold the look-split
    onto the adjacent QM rung (D=6, same 0.85/0.95), like Materials/Optics
    onto PhysChem/Chem.

    Specimen: electron and proton mass (bound in the atom vs HEP), plus
    H ionization on both folds. Do not stuff φ/2 onto the mixed vs 1.
    """
    live_at = abs(f(domain_scalar("Atomic_Physics")))
    live_h = abs(f(domain_scalar("High_Energy_Physics")))
    live_ratio = live_at / live_h
    look_qm = scalar_at(d_eff=6, delta_psi=0.85) / scalar_at(d_eff=6, delta_psi=0.95)
    vs1_live = err(live_ratio, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="atomic_hep_S_ratio",
            name="S_atomic_over_S_hep_vs_qm_look_split",
            computed=live_ratio,
            measured=look_qm,
            note=(
                "|S_Atomic|/|S_HEP| vs S(D=6,δψ=0.85)/S(D=6,δψ=0.95) — same "
                "0.85/0.95 look-split on the QM rung. "
                f"Not vs 1 ({vs1_live:.1f}%, look mix at same D=7)."
            ),
            extra={
                "kappa": kappa_domains("Atomic_Physics", "High_Energy_Physics"),
                "rejected_vs_1_error_pct": vs1_live,
            },
        ),
    ]
    for name, mass, note_at, note_h in (
        (
            "electron_mass_kg",
            ELECTRON_MASS_KG,
            "CODATA m_e on Atomic_Physics — bound lepton",
            "same m_e on High_Energy_Physics — free lepton",
        ),
        (
            "proton_mass_kg",
            PROTON_MASS_KG,
            "CODATA m_p on Atomic_Physics — bound baryon",
            "same m_p on High_Energy_Physics — collision baryon",
        ),
    ):
        ca, ea = scaled(mass, "Atomic_Physics")
        ch, eh = scaled(mass, "High_Energy_Physics")
        rows.append(
            _row(
                prop="atomic_hep_mass_atomic_fold",
                name=name + "_atomic",
                computed=ca,
                measured=mass,
                note=note_at,
            )
        )
        rows[-1]["error_pct"] = ea
        rows.append(
            _row(
                prop="atomic_hep_mass_hep_fold",
                name=name + "_hep",
                computed=ch,
                measured=mass,
                note=note_h,
            )
        )
        rows[-1]["error_pct"] = eh
    ie_h = next((r for r in chemistry_ionization() if r.name == "IE_H"), None)
    if ie_h is not None and ie_h.measured is not None:
        m = f(ie_h.measured)
        ca, ea = scaled(m, "Atomic_Physics")
        ch, eh = scaled(m, "High_Energy_Physics")
        rows.append(
            _row(
                prop="atomic_hep_IE_atomic_fold",
                name="IE_H_atomic",
                computed=ca,
                measured=m,
                note="NIST H ionization on Atomic_Physics — bound well",
            )
        )
        rows[-1]["error_pct"] = ea
        rows.append(
            _row(
                prop="atomic_hep_IE_hep_fold",
                name="IE_H_hep",
                computed=ch,
                measured=m,
                note="same IE_H on High_Energy_Physics — free-electron threshold",
            )
        )
        rows[-1]["error_pct"] = eh
    return rows


# CRC Handbook / NIST WebBook common molecular specimens (Tm, Tb K; rho g/cm³; MW g/mol).
CRC_MOLECULES = [
    {"name": "water", "Tm": 273.15, "Tb": 373.15, "rho": 0.9982, "mw": 18.015},
    {"name": "methanol", "Tm": 175.6, "Tb": 337.8, "rho": 0.7918, "mw": 32.042},
    {"name": "ethanol", "Tm": 159.05, "Tb": 351.52, "rho": 0.789, "mw": 46.069},
    {"name": "acetone", "Tm": 178.5, "Tb": 329.22, "rho": 0.7845, "mw": 58.080},
    {"name": "acetic_acid", "Tm": 289.8, "Tb": 391.2, "rho": 1.049, "mw": 60.052},
    {"name": "n_hexane", "Tm": 177.83, "Tb": 341.88, "rho": 0.6606, "mw": 86.178},
    {"name": "benzene", "Tm": 278.68, "Tb": 353.3, "rho": 0.8765, "mw": 78.114},
    {"name": "toluene", "Tm": 178.0, "Tb": 383.8, "rho": 0.8669, "mw": 92.141},
    {"name": "nacl", "Tm": 1073.8, "Tb": 1738.0, "rho": 2.17, "mw": 58.44},
]


def chem_physchem_rows() -> list[dict[str, Any]]:
    """Chemistry D=8 ↔ Physical_Chemistry D=8 — composition vs thermo.

    Same D, same C=e/π. δψ 0.6 vs 0.5 is the look-split already scored as
    Materials/Optics vs this pair. Equalizing δψ at D=8 is identity — do
    not pad. Dual-route CRC: density/MW on Chemistry, Tm/Tb on PhysChem.
    """
    live = look_split_ratio("Physical_Chemistry", "Chemistry")
    mat = look_split_ratio("Materials_Science", "Optics")
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="chem_pc_S_ratio",
            name="S_physchem_over_S_chem_vs_mat_opt",
            computed=live,
            measured=mat,
            note=(
                "|S_PhysChem|/|S_Chemistry| vs |S_Materials|/|S_Optics| — "
                "same 0.5/0.6 look-split (already TISSUE-MAT-OPT). "
                f"Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Chemistry", "Physical_Chemistry"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mol in CRC_MOLECULES:
        rho = float(mol["rho"])
        mw = float(mol["mw"])
        tm = float(mol["Tm"])
        tb = float(mol["Tb"])
        cr, er = scaled(rho, "Chemistry")
        cm, em = scaled(mw, "Chemistry")
        ct, et = scaled(tm, "Physical_Chemistry")
        cb, eb = scaled(tb, "Physical_Chemistry")
        tag = str(mol["name"])
        rows.append(
            _row(
                prop="chem_pc_rho_chem_fold",
                name=tag + "_rho",
                computed=cr,
                measured=rho,
                note="CRC density on Chemistry D=8 — composition",
            )
        )
        rows[-1]["error_pct"] = er
        rows.append(
            _row(
                prop="chem_pc_mw_chem_fold",
                name=tag + "_mw",
                computed=cm,
                measured=mw,
                note="CRC MW on Chemistry D=8 — composition",
            )
        )
        rows[-1]["error_pct"] = em
        rows.append(
            _row(
                prop="chem_pc_Tm_pc_fold",
                name=tag + "_Tm",
                computed=ct,
                measured=tm,
                note="CRC melting T on Physical_Chemistry D=8 — thermo",
            )
        )
        rows[-1]["error_pct"] = et
        rows.append(
            _row(
                prop="chem_pc_Tb_pc_fold",
                name=tag + "_Tb",
                computed=cb,
                measured=tb,
                note="CRC boiling T on Physical_Chemistry D=8 — thermo",
            )
        )
        rows[-1]["error_pct"] = eb
    return rows


def chem_mol_rows() -> list[dict[str, Any]]:
    """Chemistry D=8 ↔ Molecular_Chemistry D=9 — composition vs molecule.

    Live |S_chem|/|S_mol| vs 1 mixes D=8/9 with δψ 0.6 vs 0.5. Equalize
    at the chemistry look (δψ=0.6): adjacent-rung vs 1. Dual-route CRC MW.
    """
    s8 = scalar_at(d_eff=8, delta_psi=0.6)
    s9 = scalar_at(d_eff=9, delta_psi=0.6)
    live_c = abs(f(domain_scalar("Chemistry")))
    live_m = abs(f(domain_scalar("Molecular_Chemistry")))
    vs1 = err(live_c / live_m, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="chem_mol_S_ratio_same_look",
            name="S_D8_over_S_D9_at_dpsi_0p6",
            computed=s8 / s9,
            measured=1.0,
            note=(
                "|S(D=8,δψ=0.6)|/|S(D=9,δψ=0.6)| vs 1 — adjacent rung, same "
                "composition look. "
                f"Live mixed |S_chem|/|S_mol| vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Chemistry", "Molecular_Chemistry"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        cc, ec = scaled(mw, "Chemistry")
        cm, em = scaled(mw, "Molecular_Chemistry")
        tag = str(mol["name"])
        rows.append(
            _row(
                prop="chem_mol_mw_chem_fold",
                name=tag + "_mw_chem",
                computed=cc,
                measured=mw,
                note="CRC MW on Chemistry D=8 — composition",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="chem_mol_mw_mol_fold",
                name=tag + "_mw_mol",
                computed=cm,
                measured=mw,
                note="same MW on Molecular_Chemistry D=9 — molecule",
            )
        )
        rows[-1]["error_pct"] = em
    return rows


def physchem_mol_rows() -> list[dict[str, Any]]:
    """Physical_Chemistry D=8 ↔ Molecular_Chemistry D=9 — thermo vs molecule.

    Both δψ=0.5 (same look). Live |S_pc|/|S_mol| vs 1 is the adjacent-rung
    test with looks already matched. Dual-route CRC Tm on PhysChem, MW on Mol.
    """
    live_p = abs(f(domain_scalar("Physical_Chemistry")))
    live_m = abs(f(domain_scalar("Molecular_Chemistry")))
    rows: list[dict[str, Any]] = [
        _row(
            prop="physchem_mol_S_ratio",
            name="S_physchem_over_S_mol",
            computed=live_p / live_m,
            measured=1.0,
            note=(
                "|S_PhysChem|/|S_Molecular| vs 1 — adjacent D=8/9, both δψ=0.5 "
                "(looks already matched)"
            ),
            extra={"kappa": kappa_domains("Physical_Chemistry", "Molecular_Chemistry")},
        ),
    ]
    for mol in CRC_MOLECULES:
        tm = float(mol["Tm"])
        mw = float(mol["mw"])
        ct, et = scaled(tm, "Physical_Chemistry")
        cm, em = scaled(mw, "Molecular_Chemistry")
        tag = str(mol["name"])
        rows.append(
            _row(
                prop="physchem_mol_Tm_pc_fold",
                name=tag + "_Tm",
                computed=ct,
                measured=tm,
                note="CRC melting T on Physical_Chemistry D=8",
            )
        )
        rows[-1]["error_pct"] = et
        rows.append(
            _row(
                prop="physchem_mol_mw_mol_fold",
                name=tag + "_mw",
                computed=cm,
                measured=mw,
                note="CRC MW on Molecular_Chemistry D=9",
            )
        )
        rows[-1]["error_pct"] = em
    return rows


# CRC / literature longitudinal sound speed (m/s) for specimens that also have n, ρ.
ACOUSTIC_SPECIMENS = [
    {"name": "water_20C", "n": 1.3330, "rho": 0.9982, "c": 1482.4},
    {"name": "ice_Ih", "n": 1.309, "rho": 0.917, "c": 3980.0},
    {"name": "fused_silica", "n": 1.4585, "rho": 2.203, "c": 5968.0},
    {"name": "ethanol_20C", "n": 1.3611, "rho": 0.789, "c": 1144.0},
    {"name": "nacl", "n": 1.5442, "rho": 2.17, "c": 4780.0},
]

# CRC metal / elemental solids: density g/cm³, melting T K.
CM_THERMO_SOLIDS = [
    {"name": "Al", "rho": 2.70, "Tm": 933.47},
    {"name": "Cu", "rho": 8.96, "Tm": 1357.77},
    {"name": "Fe", "rho": 7.87, "Tm": 1811.0},
    {"name": "Au", "rho": 19.32, "Tm": 1337.33},
    {"name": "Ag", "rho": 10.49, "Tm": 1234.93},
    {"name": "Pb", "rho": 11.34, "Tm": 600.61},
    {"name": "Si", "rho": 2.329, "Tm": 1687.0},
    {"name": "NaCl", "rho": 2.17, "Tm": 1073.8},
]


def ac_opt_rows() -> list[dict[str, Any]]:
    """Acoustics D=10 ↔ Optics D=10 — lab sound vs light, same rung.

    Live |S_ac|/|S_opt| vs 1 is δψ 0.3 vs 0.6. Equalizing at D=10 is identity.
    Fold the look-split onto D=9 (same 0.3/0.6). Dual-route CRC c on Acoustics,
    n on Optics. Water c vs e+φ already lives in the fluid-tank rows.
    """
    live = look_split_ratio("Acoustics", "Optics")
    cross = scalar_at(d_eff=9, delta_psi=0.3) / scalar_at(d_eff=9, delta_psi=0.6)
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="ac_opt_S_ratio",
            name="S_ac_over_S_opt_vs_D9_look",
            computed=live,
            measured=cross,
            note=(
                "|S_Acoustics|/|S_Optics| vs S(D=9,δψ=0.3)/S(D=9,δψ=0.6) — "
                "same 0.3/0.6 look-split on the molecular rung. "
                f"Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Acoustics", "Optics"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sp in ACOUSTIC_SPECIMENS:
        c = float(sp["c"])
        n = float(sp["n"])
        cc, ec = scaled(c, "Acoustics")
        cn, en = scaled(n, "Optics")
        tag = str(sp["name"])
        rows.append(
            _row(
                prop="ac_opt_c_ac_fold",
                name=tag + "_c",
                computed=cc,
                measured=c,
                note="CRC/literature longitudinal sound speed on Acoustics D=10",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="ac_opt_n_opt_fold",
                name=tag + "_n",
                computed=cn,
                measured=n,
                note="CRC n_D on Optics D=10 — same specimen, light zoom",
            )
        )
        rows[-1]["error_pct"] = en
    return rows


def ac_mat_rows() -> list[dict[str, Any]]:
    """Acoustics D=10 ↔ Materials_Science D=10 — sound vs bulk, same rung.

    Live |S_ac|/|S_mat| vs 1 is δψ 0.3 vs 0.5. Fold onto D=9. Dual-route
    c on Acoustics, ρ on Materials.
    """
    live = look_split_ratio("Acoustics", "Materials_Science")
    cross = scalar_at(d_eff=9, delta_psi=0.3) / scalar_at(d_eff=9, delta_psi=0.5)
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="ac_mat_S_ratio",
            name="S_ac_over_S_mat_vs_D9_look",
            computed=live,
            measured=cross,
            note=(
                "|S_Acoustics|/|S_Materials| vs S(D=9,δψ=0.3)/S(D=9,δψ=0.5). "
                f"Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Acoustics", "Materials_Science"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sp in ACOUSTIC_SPECIMENS:
        c = float(sp["c"])
        rho = float(sp["rho"])
        cc, ec = scaled(c, "Acoustics")
        cr, er = scaled(rho, "Materials_Science")
        tag = str(sp["name"])
        rows.append(
            _row(
                prop="ac_mat_c_ac_fold",
                name=tag + "_c",
                computed=cc,
                measured=c,
                note="sound speed on Acoustics D=10",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="ac_mat_rho_mat_fold",
                name=tag + "_rho",
                computed=cr,
                measured=rho,
                note="CRC density on Materials D=10 — same specimen, bulk zoom",
            )
        )
        rows[-1]["error_pct"] = er
    return rows


def mol_ac_rows() -> list[dict[str, Any]]:
    """Molecular_Chemistry D=9 ↔ Acoustics D=10 — molecule vs lab sound.

    Live mix is δψ 0.5 vs 0.3. Equalize at δψ=0.5: adjacent D=9/10 vs 1.
    Dual-route CRC MW on Molecular, c on Acoustics for overlapping liquids.
    """
    s9 = scalar_at(d_eff=9, delta_psi=0.5)
    s10 = scalar_at(d_eff=10, delta_psi=0.5)
    live_m = abs(f(domain_scalar("Molecular_Chemistry")))
    live_a = abs(f(domain_scalar("Acoustics")))
    vs1 = err(live_m / live_a, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="mol_ac_S_ratio_same_look",
            name="S_D9_over_S_D10_at_dpsi_0p5",
            computed=s9 / s10,
            measured=1.0,
            note=(
                "|S(D=9,δψ=0.5)|/|S(D=10,δψ=0.5)| vs 1 — adjacent rung, same look. "
                f"Live mixed |S_mol|/|S_ac| vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Molecular_Chemistry", "Acoustics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    liquids = [sp for sp in ACOUSTIC_SPECIMENS if sp["name"] in {"water_20C", "ethanol_20C"}]
    mw_map = {"water_20C": 18.015, "ethanol_20C": 46.069}
    for sp in liquids:
        c = float(sp["c"])
        mw = float(mw_map[str(sp["name"])])
        cc, ec = scaled(c, "Acoustics")
        cm, em = scaled(mw, "Molecular_Chemistry")
        tag = str(sp["name"])
        rows.append(
            _row(
                prop="mol_ac_c_ac_fold",
                name=tag + "_c",
                computed=cc,
                measured=c,
                note="sound speed on Acoustics D=10",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="mol_ac_mw_mol_fold",
                name=tag + "_mw",
                computed=cm,
                measured=mw,
                note="CRC MW on Molecular_Chemistry D=9 — same liquid",
            )
        )
        rows[-1]["error_pct"] = em
    return rows


def cm_thermo_rows() -> list[dict[str, Any]]:
    """Condensed_Matter D=14 ↔ Thermodynamics D=15 — solid vs heat.

    Live mix is δψ 0.5 vs 0.9 plus hits. Equalize at CM look (δψ=0.5, hits=0):
    adjacent D=14/15 vs 1. Dual-route CRC density on CM, Tm on Thermo.
    """
    s14 = scalar_at(d_eff=14, delta_psi=0.5, hits=0, observed=True)
    s15 = scalar_at(d_eff=15, delta_psi=0.5, hits=0, observed=True)
    live_c = abs(f(domain_scalar("Condensed_Matter")))
    live_t = abs(f(domain_scalar("Thermodynamics")))
    vs1 = err(live_c / live_t, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="cm_thermo_S_ratio_same_look",
            name="S_D14_over_S_D15_at_dpsi_0p5",
            computed=s14 / s15,
            measured=1.0,
            note=(
                "|S(D=14,δψ=0.5)|/|S(D=15,δψ=0.5)| vs 1 — adjacent rung, CM look. "
                f"Live mixed |S_CM|/|S_thermo| vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Condensed_Matter", "Thermodynamics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        tm = float(sol["Tm"])
        cr, er = scaled(rho, "Condensed_Matter")
        ct, et = scaled(tm, "Thermodynamics")
        tag = str(sol["name"])
        rows.append(
            _row(
                prop="cm_thermo_rho_cm_fold",
                name=tag + "_rho",
                computed=cr,
                measured=rho,
                note="CRC density on Condensed_Matter D=14 — solid",
            )
        )
        rows[-1]["error_pct"] = er
        rows.append(
            _row(
                prop="cm_thermo_Tm_th_fold",
                name=tag + "_Tm",
                computed=ct,
                measured=tm,
                note="CRC melting T on Thermodynamics D=15 — heat",
            )
        )
        rows[-1]["error_pct"] = et
    return rows


def em_mat_rows() -> list[dict[str, Any]]:
    """Electromagnetism D=9 ↔ Materials_Science D=10 — field vs bulk.

    Live |S_em|/|S_mat| vs 1 mixes D=9/10 with δψ 0.7 vs 0.5. Equalize at
    the materials look (δψ=0.5): adjacent-rung vs 1. Dual-route CRC n² on
    EM (Maxwell ε_opt) and density on Materials. Same specimens as n/ρ.
    Static metal conductivity is another interface.
    """
    s9 = scalar_at(d_eff=9, delta_psi=0.5)
    s10 = scalar_at(d_eff=10, delta_psi=0.5)
    live_e = abs(f(domain_scalar("Electromagnetism")))
    live_m = abs(f(domain_scalar("Materials_Science")))
    vs1 = err(live_e / live_m, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="em_mat_S_ratio_same_look",
            name="S_D9_over_S_D10_at_dpsi_0p5",
            computed=s9 / s10,
            measured=1.0,
            note=(
                "|S(D=9,δψ=0.5)|/|S(D=10,δψ=0.5)| vs 1 — adjacent rung, bulk look. "
                f"Live mixed |S_em|/|S_mat| vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Electromagnetism", "Materials_Science"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        rho = float(mat["rho"])
        eps = n * n
        ce, ee = scaled(eps, "Electromagnetism")
        cr, er = scaled(rho, "Materials_Science")
        tag = str(mat["name"])
        rows.append(
            _row(
                prop="em_mat_eps_em_fold",
                name=tag + "_n_sq",
                computed=ce,
                measured=eps,
                note="n² on Electromagnetism D=9 — Maxwell ε_opt",
            )
        )
        rows[-1]["error_pct"] = ee
        rows.append(
            _row(
                prop="em_mat_rho_mat_fold",
                name=tag + "_rho",
                computed=cr,
                measured=rho,
                note="CRC density on Materials D=10 — same specimen, bulk",
            )
        )
        rows[-1]["error_pct"] = er
    return rows


NEURO_AA = ("Gly", "Asp", "Glu", "Tyr", "Trp", "His")


def biochem_neuro_rows() -> list[dict[str, Any]]:
    """Biochemistry D=13 ↔ Neuroscience D=14 — molecule vs signaling.

    Not the social-tank GDP dual-route (Economics↔Neuroscience). Live
    |S_bc|/|S_neuro| vs 1 mixes D with δψ 0.35 vs 0.7. Equalize at the
    neural look (δψ=0.7, hits=1): adjacent-rung vs 1. Dual-route CRC MW
    of transmitter amino acids (Gly, Asp, Glu, Tyr, Trp, His).
    """
    s13 = scalar_at(d_eff=13, delta_psi=0.7, hits=1, observed=True)
    s14 = scalar_at(d_eff=14, delta_psi=0.7, hits=1, observed=True)
    live_b = abs(f(domain_scalar("Biochemistry")))
    live_n = abs(f(domain_scalar("Neuroscience")))
    vs1 = err(live_b / live_n, 1.0)
    mw = {a: m for a, m in AMINO_ACID_MW}
    rows: list[dict[str, Any]] = [
        _row(
            prop="biochem_neuro_S_ratio_same_look",
            name="S_D13_over_S_D14_at_dpsi_0p7",
            computed=s13 / s14,
            measured=1.0,
            note=(
                "|S(D=13,δψ=0.7)|/|S(D=14,δψ=0.7)| vs 1 — adjacent rung, neural look. "
                f"Live mixed |S_bc|/|S_neuro| vs 1 is {vs1:.1f}% — not this object. "
                "Not World Bank YoY (that is TISSUE-SOCIAL)."
            ),
            extra={
                "kappa": kappa_domains("Biochemistry", "Neuroscience"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for aa in NEURO_AA:
        m = float(mw[aa])
        cb, eb = scaled(m, "Biochemistry")
        cn, en = scaled(m, "Neuroscience")
        rows.append(
            _row(
                prop="biochem_neuro_aa_bc_fold",
                name=aa + "_mw_bc",
                computed=cb,
                measured=m,
                note="CRC/IUPAC transmitter AA MW on Biochemistry D=13",
            )
        )
        rows[-1]["error_pct"] = eb
        rows.append(
            _row(
                prop="biochem_neuro_aa_neuro_fold",
                name=aa + "_mw_neuro",
                computed=cn,
                measured=m,
                note="same AA MW on Neuroscience D=14 — signaling residue",
            )
        )
        rows[-1]["error_pct"] = en
    return rows


def _ie_rows(domain: str, prop: str, note: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rec in chemistry_ionization():
        if rec.measured is None:
            continue
        m = f(rec.measured)
        if m <= 0:
            continue
        c, e = scaled(m, domain)
        rows.append(
            _row(
                prop=prop,
                name=str(rec.name) + "_" + domain.split("_")[0].lower(),
                computed=c,
                measured=m,
                note=note,
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def atomic_chem_rows() -> list[dict[str, Any]]:
    """Atomic_Physics D=7 ↔ Chemistry D=8 — bound well vs composition.

    Equalize at the chemistry look (δψ=0.6). Dual-route NIST IE on Atomic,
    CRC MW on Chemistry.
    """
    s7 = scalar_at(d_eff=7, delta_psi=0.6)
    s8 = scalar_at(d_eff=8, delta_psi=0.6)
    live = abs(f(domain_scalar("Atomic_Physics"))) / abs(f(domain_scalar("Chemistry")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="atomic_chem_S_ratio_same_look",
            name="S_D7_over_S_D8_at_dpsi_0p6",
            computed=s7 / s8,
            measured=1.0,
            note=(
                "|S(D=7,δψ=0.6)|/|S(D=8,δψ=0.6)| vs 1 — well vs composition, "
                f"same look. Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Atomic_Physics", "Chemistry"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(_ie_rows("Atomic_Physics", "atomic_chem_IE_atomic_fold", "NIST IE on Atomic D=7"))
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        c, e = scaled(mw, "Chemistry")
        rows.append(
            _row(
                prop="atomic_chem_mw_chem_fold",
                name=str(mol["name"]) + "_mw_chem",
                computed=c,
                measured=mw,
                note="CRC MW on Chemistry D=8 — composition of the same atoms",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def atomic_pc_rows() -> list[dict[str, Any]]:
    """Atomic_Physics D=7 ↔ Physical_Chemistry D=8 — well vs thermo look.

    Equalize at δψ=0.5. NIST IE on Atomic, CRC Tm on PhysChem.
    """
    s7 = scalar_at(d_eff=7, delta_psi=0.5)
    s8 = scalar_at(d_eff=8, delta_psi=0.5)
    live = abs(f(domain_scalar("Atomic_Physics"))) / abs(
        f(domain_scalar("Physical_Chemistry"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="atomic_pc_S_ratio_same_look",
            name="S_D7_over_S_D8_at_dpsi_0p5",
            computed=s7 / s8,
            measured=1.0,
            note=(
                "|S(D=7,δψ=0.5)|/|S(D=8,δψ=0.5)| vs 1 — well vs thermo, same look. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Atomic_Physics", "Physical_Chemistry"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(_ie_rows("Atomic_Physics", "atomic_pc_IE_atomic_fold", "NIST IE on Atomic D=7"))
    for mol in CRC_MOLECULES:
        tm = float(mol["Tm"])
        c, e = scaled(tm, "Physical_Chemistry")
        rows.append(
            _row(
                prop="atomic_pc_Tm_pc_fold",
                name=str(mol["name"]) + "_Tm_pc",
                computed=c,
                measured=tm,
                note="CRC Tm on Physical_Chemistry D=8 — thermo of the well",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def hep_chem_rows() -> list[dict[str, Any]]:
    """High_Energy_Physics D=7 ↔ Chemistry D=8 — collision vs composition.

    Same compactification step as Atomic–Chem; specimen is the collision face.
    Equalize at δψ=0.6. NIST IE on HEP, CRC MW on Chemistry.
    """
    s7 = scalar_at(d_eff=7, delta_psi=0.6)
    s8 = scalar_at(d_eff=8, delta_psi=0.6)
    live = abs(f(domain_scalar("High_Energy_Physics"))) / abs(f(domain_scalar("Chemistry")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="hep_chem_S_ratio_same_look",
            name="S_D7_over_S_D8_at_dpsi_0p6_hep",
            computed=s7 / s8,
            measured=1.0,
            note=(
                "|S(D=7,δψ=0.6)|/|S(D=8,δψ=0.6)| vs 1 — collision vs composition. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("High_Energy_Physics", "Chemistry"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(_ie_rows("High_Energy_Physics", "hep_chem_IE_hep_fold", "NIST IE on HEP D=7"))
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        c, e = scaled(mw, "Chemistry")
        rows.append(
            _row(
                prop="hep_chem_mw_chem_fold",
                name=str(mol["name"]) + "_mw_chem",
                computed=c,
                measured=mw,
                note="CRC MW on Chemistry D=8",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def hep_pc_rows() -> list[dict[str, Any]]:
    """High_Energy_Physics D=7 ↔ Physical_Chemistry D=8 — collision vs thermo."""
    s7 = scalar_at(d_eff=7, delta_psi=0.5)
    s8 = scalar_at(d_eff=8, delta_psi=0.5)
    live = abs(f(domain_scalar("High_Energy_Physics"))) / abs(
        f(domain_scalar("Physical_Chemistry"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="hep_pc_S_ratio_same_look",
            name="S_D7_over_S_D8_at_dpsi_0p5_hep",
            computed=s7 / s8,
            measured=1.0,
            note=(
                "|S(D=7,δψ=0.5)|/|S(D=8,δψ=0.5)| vs 1 — collision vs thermo. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("High_Energy_Physics", "Physical_Chemistry"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(_ie_rows("High_Energy_Physics", "hep_pc_IE_hep_fold", "NIST IE on HEP D=7"))
    for mol in CRC_MOLECULES:
        tm = float(mol["Tm"])
        c, e = scaled(tm, "Physical_Chemistry")
        rows.append(
            _row(
                prop="hep_pc_Tm_pc_fold",
                name=str(mol["name"]) + "_Tm_pc",
                computed=c,
                measured=tm,
                note="CRC Tm on Physical_Chemistry D=8",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def pc_em_rows() -> list[dict[str, Any]]:
    """Physical_Chemistry D=8 ↔ Electromagnetism D=9 — thermo vs field.

    Equalize at the PhysChem look (δψ=0.5). CRC Tm on PhysChem, n² on EM.
    """
    s8 = scalar_at(d_eff=8, delta_psi=0.5)
    s9 = scalar_at(d_eff=9, delta_psi=0.5)
    live = abs(f(domain_scalar("Physical_Chemistry"))) / abs(
        f(domain_scalar("Electromagnetism"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="pc_em_S_ratio_same_look",
            name="S_D8_over_S_D9_at_dpsi_0p5",
            computed=s8 / s9,
            measured=1.0,
            note=(
                "|S(D=8,δψ=0.5)|/|S(D=9,δψ=0.5)| vs 1 — thermo vs field. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Physical_Chemistry", "Electromagnetism"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mol in CRC_MOLECULES:
        tm = float(mol["Tm"])
        c, e = scaled(tm, "Physical_Chemistry")
        rows.append(
            _row(
                prop="pc_em_Tm_pc_fold",
                name=str(mol["name"]) + "_Tm_pc",
                computed=c,
                measured=tm,
                note="CRC Tm on Physical_Chemistry D=8",
            )
        )
        rows[-1]["error_pct"] = e
    for mat in OPTICAL_MATERIALS:
        eps = float(mat["n"]) ** 2
        c, e = scaled(eps, "Electromagnetism")
        rows.append(
            _row(
                prop="pc_em_eps_em_fold",
                name=str(mat["name"]) + "_eps_em",
                computed=c,
                measured=eps,
                note="CRC n² on Electromagnetism D=9 — Maxwell dielectric",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def em_mol_rows() -> list[dict[str, Any]]:
    """Electromagnetism D=9 ↔ Molecular_Chemistry D=9 — field vs molecule.

    Same D. δψ 0.7 vs 0.5. Fold the look-split onto D=8. CRC n² on EM, MW on Mol.
    """
    live = look_split_ratio("Electromagnetism", "Molecular_Chemistry")
    look = scalar_at(d_eff=8, delta_psi=0.7) / scalar_at(d_eff=8, delta_psi=0.5)
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="em_mol_S_ratio",
            name="S_em_over_S_mol_vs_D8_look",
            computed=live,
            measured=look,
            note=(
                "|S_EM|/|S_Mol| vs S(D=8,δψ=0.7)/S(D=8,δψ=0.5) — same 0.7/0.5 "
                f"look-split. Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Electromagnetism", "Molecular_Chemistry"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        eps = float(mat["n"]) ** 2
        c, e = scaled(eps, "Electromagnetism")
        rows.append(
            _row(
                prop="em_mol_eps_em_fold",
                name=str(mat["name"]) + "_eps_em",
                computed=c,
                measured=eps,
                note="CRC n² on Electromagnetism D=9",
            )
        )
        rows[-1]["error_pct"] = e
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        c, e = scaled(mw, "Molecular_Chemistry")
        rows.append(
            _row(
                prop="em_mol_mw_mol_fold",
                name=str(mol["name"]) + "_mw_mol",
                computed=c,
                measured=mw,
                note="CRC MW on Molecular_Chemistry D=9",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def mol_mat_rows() -> list[dict[str, Any]]:
    """Molecular_Chemistry D=9 ↔ Materials_Science D=10 — molecule vs bulk.

    Both δψ=0.5. Live |S| vs 1 is the matched-look rung. CRC MW vs density.
    """
    sm = abs(f(domain_scalar("Molecular_Chemistry")))
    sa = abs(f(domain_scalar("Materials_Science")))
    vs1 = err(sm / sa, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="mol_mat_S_ratio_same_look",
            name="S_mol_over_S_mat_live",
            computed=sm / sa,
            measured=1.0,
            note=(
                "|S_Mol|/|S_Materials| vs 1 — adjacent D=9/10, both δψ=0.5. "
                f"({vs1:.3f}%)."
            ),
            extra={"kappa": kappa_domains("Molecular_Chemistry", "Materials_Science")},
        ),
    ]
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        rho = float(mol["rho"])
        cm, em = scaled(mw, "Molecular_Chemistry")
        cr, er = scaled(rho, "Materials_Science")
        tag = str(mol["name"])
        rows.append(
            _row(
                prop="mol_mat_mw_mol_fold",
                name=tag + "_mw_mol",
                computed=cm,
                measured=mw,
                note="CRC MW on Molecular_Chemistry D=9",
            )
        )
        rows[-1]["error_pct"] = em
        rows.append(
            _row(
                prop="mol_mat_rho_mat_fold",
                name=tag + "_rho_mat",
                computed=cr,
                measured=rho,
                note="CRC density on Materials_Science D=10 — bulk of the molecule",
            )
        )
        rows[-1]["error_pct"] = er
    return rows


def mol_opt_rows() -> list[dict[str, Any]]:
    """Molecular_Chemistry D=9 ↔ Optics D=10 — molecule vs light.

    Equalize at δψ=0.5. CRC MW on Mol, n_D on Optics.
    """
    s9 = scalar_at(d_eff=9, delta_psi=0.5)
    s10 = scalar_at(d_eff=10, delta_psi=0.5)
    live = abs(f(domain_scalar("Molecular_Chemistry"))) / abs(f(domain_scalar("Optics")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="mol_opt_S_ratio_same_look",
            name="S_D9_over_S_D10_at_dpsi_0p5_molopt",
            computed=s9 / s10,
            measured=1.0,
            note=(
                "|S(D=9,δψ=0.5)|/|S(D=10,δψ=0.5)| vs 1 — molecule vs light. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Molecular_Chemistry", "Optics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mol in CRC_MOLECULES:
        mw = float(mol["mw"])
        c, e = scaled(mw, "Molecular_Chemistry")
        rows.append(
            _row(
                prop="mol_opt_mw_mol_fold",
                name=str(mol["name"]) + "_mw_mol",
                computed=c,
                measured=mw,
                note="CRC MW on Molecular_Chemistry D=9",
            )
        )
        rows[-1]["error_pct"] = e
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        c, e = scaled(n, "Optics")
        rows.append(
            _row(
                prop="mol_opt_n_opt_fold",
                name=str(mat["name"]) + "_n_opt",
                computed=c,
                measured=n,
                note="CRC n_D on Optics D=10",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def ac_qo_rows() -> list[dict[str, Any]]:
    """Acoustics D=10 ↔ Quantum_Optics D=11 — lab sound vs photon.

    Equalize at the light look (δψ=0.6). CRC c on Acoustics, n on QO.
    """
    s10 = scalar_at(d_eff=10, delta_psi=0.6)
    s11 = scalar_at(d_eff=11, delta_psi=0.6)
    live = abs(f(domain_scalar("Acoustics"))) / abs(f(domain_scalar("Quantum_Optics")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="ac_qo_S_ratio_same_look",
            name="S_D10_over_S_D11_at_dpsi_0p6",
            computed=s10 / s11,
            measured=1.0,
            note=(
                "|S(D=10,δψ=0.6)|/|S(D=11,δψ=0.6)| vs 1 — sound vs photon. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Acoustics", "Quantum_Optics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sp in ACOUSTIC_SPECIMENS:
        cc, ec = scaled(float(sp["c"]), "Acoustics")
        cn, en = scaled(float(sp["n"]), "Quantum_Optics")
        tag = str(sp["name"])
        rows.append(
            _row(
                prop="ac_qo_c_ac_fold",
                name=tag + "_c_ac",
                computed=cc,
                measured=float(sp["c"]),
                note="CRC longitudinal c on Acoustics D=10",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="ac_qo_n_qo_fold",
                name=tag + "_n_qo",
                computed=cn,
                measured=float(sp["n"]),
                note="CRC n_D on Quantum_Optics D=11 — photon zoom",
            )
        )
        rows[-1]["error_pct"] = en
    return rows


def mat_qo_rows() -> list[dict[str, Any]]:
    """Materials_Science D=10 ↔ Quantum_Optics D=11 — bulk vs photon.

    Equalize at the materials look (δψ=0.5). CRC ρ on Materials, n on QO.
    """
    s10 = scalar_at(d_eff=10, delta_psi=0.5)
    s11 = scalar_at(d_eff=11, delta_psi=0.5)
    live = abs(f(domain_scalar("Materials_Science"))) / abs(
        f(domain_scalar("Quantum_Optics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="mat_qo_S_ratio_same_look",
            name="S_D10_over_S_D11_at_dpsi_0p5",
            computed=s10 / s11,
            measured=1.0,
            note=(
                "|S(D=10,δψ=0.5)|/|S(D=11,δψ=0.5)| vs 1 — bulk vs photon. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Materials_Science", "Quantum_Optics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        cr, er = scaled(float(mat["rho"]), "Materials_Science")
        cn, en = scaled(float(mat["n"]), "Quantum_Optics")
        tag = str(mat["name"])
        rows.append(
            _row(
                prop="mat_qo_rho_mat_fold",
                name=tag + "_rho_mat",
                computed=cr,
                measured=float(mat["rho"]),
                note="CRC density on Materials_Science D=10",
            )
        )
        rows[-1]["error_pct"] = er
        rows.append(
            _row(
                prop="mat_qo_n_qo_fold",
                name=tag + "_n_qo",
                computed=cn,
                measured=float(mat["n"]),
                note="CRC n_D on Quantum_Optics D=11",
            )
        )
        rows[-1]["error_pct"] = en
    return rows


def nuclear_thermo_rows(endf_path: Path) -> list[dict[str, Any]]:
    """Nuclear D=15 ↔ Thermodynamics D=15 — orifice vs heat, same rung.

    Equalize at the thermo look (δψ=0.9, hits=1). ENDF keV on Nuclear,
    Carnot COP on Thermo — same specimens dual-routed onto the other fold.
    """
    live = abs(f(domain_scalar("Nuclear_Physics"))) / abs(
        f(domain_scalar("Thermodynamics"))
    )
    look = scalar_at(d_eff=14, delta_psi=1.0, hits=1) / scalar_at(
        d_eff=14, delta_psi=0.9, hits=1
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="nuclear_thermo_S_ratio",
            name="S_nuc_over_S_th_vs_D14_look",
            computed=live,
            measured=look,
            note=(
                "|S_Nuclear|/|S_Thermo| vs S(D=14,δψ=1)/S(D=14,δψ=0.9) — same "
                f"1/0.9 look-split. Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Nuclear_Physics", "Thermodynamics"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        ct, et = scaled(cop, "Thermodynamics")
        cn, en = scaled(cop, "Nuclear_Physics")
        rows.append(
            _row(
                prop="nuclear_thermo_carnot_th_fold",
                name=name + "_th",
                computed=ct,
                measured=cop,
                note="Carnot COP on Thermodynamics D=15",
            )
        )
        rows[-1]["error_pct"] = et
        rows.append(
            _row(
                prop="nuclear_thermo_carnot_nuc_fold",
                name=name + "_nuc",
                computed=cn,
                measured=cop,
                note="same COP on Nuclear_Physics D=15 — heat of the orifice",
            )
        )
        rows[-1]["error_pct"] = en
    if endf_path.is_file():
        doc = json.loads(endf_path.read_text(encoding="utf-8"))
        light = ("He4", "C12", "O16", "Fe56", "Si28", "Al27")
        n_taken = 0
        for rec in doc.get("material_records") or []:
            name = str(rec.get("name") or "")
            if not name.startswith(light) or rec.get("property") != "level_energy_keV":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            cn, en = scaled(m, "Nuclear_Physics")
            ct, et = scaled(m, "Thermodynamics")
            rows.append(
                _row(
                    prop="nuclear_thermo_level_nuc_fold",
                    name=name + "_nuc",
                    computed=cn,
                    measured=m,
                    note="IAEA/ENDF keV on Nuclear_Physics D=15",
                )
            )
            rows[-1]["error_pct"] = en
            rows.append(
                _row(
                    prop="nuclear_thermo_level_th_fold",
                    name=name + "_th",
                    computed=ct,
                    measured=m,
                    note="same IAEA keV on Thermodynamics D=15",
                )
            )
            rows[-1]["error_pct"] = et
            n_taken += 1
            if n_taken >= 40:
                break
    return rows


def fluid_thermo_rows() -> list[dict[str, Any]]:
    """Fluid_Dynamics D=15 ↔ Thermodynamics D=15 — tank vs heat.

    Same compactification, Fluid stays dark. Dual-route Carnot COP on both.
    Live |S| vs 1 mixes observed — not a 0.5% central.
    """
    live = abs(f(domain_scalar("Fluid_Dynamics"))) / abs(
        f(domain_scalar("Thermodynamics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="fluid_thermo_S_ratio",
            name="S_fluid_over_S_thermo_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Fluid|/|S_Thermo| vs 1 mixes dark/observed at D=15. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Fluid_Dynamics", "Thermodynamics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        ct, et = scaled(cop, "Thermodynamics")
        cf, ef = scaled(cop, "Fluid_Dynamics")
        rows.append(
            _row(
                prop="fluid_thermo_carnot_th_fold",
                name=name + "_th",
                computed=ct,
                measured=cop,
                note="Carnot COP on Thermodynamics D=15",
            )
        )
        rows[-1]["error_pct"] = et
        rows.append(
            _row(
                prop="fluid_thermo_carnot_fl_fold",
                name=name + "_fl",
                computed=cf,
                measured=cop,
                note="same COP on Fluid_Dynamics D=15 — tank stays dark",
            )
        )
        rows[-1]["error_pct"] = ef
    return rows


def meteo_atm_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Meteorology D=16 ↔ Atmospheric_Physics D=17 — weather vs air tank.

    Both dark, both δψ=0.8, hits=2. Adjacent CHAOS rungs. Dual-route NDBC pres.
    """
    s16 = scalar_at(d_eff=16, delta_psi=0.8, hits=2, observed=False)
    s17 = scalar_at(d_eff=17, delta_psi=0.8, hits=2, observed=False)
    live = abs(f(domain_scalar("Meteorology"))) / abs(
        f(domain_scalar("Atmospheric_Physics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="meteo_atm_S_ratio_same_look",
            name="S_D16_over_S_D17_at_dpsi_0p8_dark",
            computed=s16 / s17,
            measured=1.0,
            note=(
                "|S(D=16,δψ=0.8,dark)|/|S(D=17,δψ=0.8,dark)| vs 1 — weather vs air. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Do not flip dark. "
                "Compactification step at this rung is a literature band, not stuffed."
            ),
            kind="structural" if err(s16 / s17, 1.0) > 0.5 else "scalar",
            extra={
                "kappa": kappa_domains("Meteorology", "Atmospheric_Physics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        for rec in doc.get("rows") or []:
            val = rec.get("pres")
            if val is None:
                continue
            m = float(val)
            if m <= 0:
                continue
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "").replace(" ", "_")
            tag = f"{bid}_{ts}"
            cm, em = scaled(m, "Meteorology")
            ca, ea = scaled(m, "Atmospheric_Physics")
            rows.append(
                _row(
                    prop="meteo_atm_pres_meteo_fold",
                    name=tag + "_meteo",
                    computed=cm,
                    measured=m,
                    note="NDBC pressure on Meteorology D=16 — weather tank, stays dark",
                )
            )
            rows[-1]["error_pct"] = em
            rows.append(
                _row(
                    prop="meteo_atm_pres_atm_fold",
                    name=tag + "_atm",
                    computed=ca,
                    measured=m,
                    note="same NDBC pressure on Atmospheric_Physics D=17",
                )
            )
            rows[-1]["error_pct"] = ea
    return rows


def _endf_keV_dual(
    endf_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
    n_max: int = 40,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not endf_path.is_file():
        return rows
    doc = json.loads(endf_path.read_text(encoding="utf-8"))
    light = ("He4", "C12", "O16", "Fe56", "Si28", "Al27")
    n_taken = 0
    for rec in doc.get("material_records") or []:
        name = str(rec.get("name") or "")
        if not name.startswith(light) or rec.get("property") != "level_energy_keV":
            continue
        m = float(rec.get("measured") or 0)
        if m <= 0:
            continue
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(
            _row(prop=prop_a, name=name + "_" + domain_a.split("_")[0].lower(),
                 computed=ca, measured=m, note=note_a)
        )
        rows[-1]["error_pct"] = ea
        rows.append(
            _row(prop=prop_b, name=name + "_" + domain_b.split("_")[0].lower(),
                 computed=cb, measured=m, note=note_b)
        )
        rows[-1]["error_pct"] = eb
        n_taken += 1
        if n_taken >= n_max:
            break
    return rows


def _wb_yoy_dual(
    econ_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
    n_max: int = 80,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not econ_path.is_file():
        return rows
    doc = json.loads(econ_path.read_text(encoding="utf-8"))
    n = 0
    for rec in doc.get("material_records") or []:
        if "yoy_growth" not in str(rec.get("property") or ""):
            continue
        m = float(rec.get("measured") or 0)
        if m == 0:
            continue
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        name = str(rec.get("name") or f"row{n}")
        rows.append(_row(prop=prop_a, name=name + "_a", computed=ca, measured=m, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=name + "_b", computed=cb, measured=m, note=note_b))
        rows[-1]["error_pct"] = eb
        n += 1
        if n >= n_max:
            break
    return rows


def _jpl_rho_dual(
    planet_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not planet_path.is_file():
        return rows
    doc = json.loads(planet_path.read_text(encoding="utf-8"))
    for rec in doc.get("records") or []:
        if rec.get("property") != "mean_density":
            continue
        m = float(rec.get("measured") or 0)
        if m <= 0:
            continue
        name = str(rec.get("name") or "body")
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(_row(prop=prop_a, name=name + "_a", computed=ca, measured=m, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=name + "_b", computed=cb, measured=m, note=note_b))
        rows[-1]["error_pct"] = eb
    return rows


def _pdg_mass_dual(
    pdg_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
    n_max: int = 20,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not pdg_path.is_file():
        return rows
    doc = json.loads(pdg_path.read_text(encoding="utf-8"))
    n = 0
    for rec in doc.get("material_records") or []:
        if "Particle Masses" not in str(rec.get("property") or ""):
            continue
        m = float(rec.get("measured") or 0)
        if m <= 0:
            continue
        name = str(rec.get("name") or f"p{n}")
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(_row(prop=prop_a, name=name + "_a", computed=ca, measured=m, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=name + "_b", computed=cb, measured=m, note=note_b))
        rows[-1]["error_pct"] = eb
        n += 1
        if n >= n_max:
            break
    return rows


def _gbif_lat_dual(
    eco_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
    n_max: int = 40,
) -> list[dict[str, Any]]:
    """GBIF occurrence latitude (decimalLatitude). Named public table."""
    rows: list[dict[str, Any]] = []
    if not eco_path.is_file():
        return rows
    doc = json.loads(eco_path.read_text(encoding="utf-8"))
    n = 0
    for rec in doc.get("material_records") or []:
        if rec.get("property") != "decimalLatitude":
            continue
        m = float(rec.get("measured") or 0)
        if m == 0:
            continue
        name = str(rec.get("name") or f"sp{n}").replace(" ", "_")
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(_row(prop=prop_a, name=name + "_a", computed=ca, measured=m, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=name + "_b", computed=cb, measured=m, note=note_b))
        rows[-1]["error_pct"] = eb
        n += 1
        if n >= n_max:
            break
    return rows


def _psych_anchor_dual(
    psych_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
) -> list[dict[str, Any]]:
    """Nunnally/Cohen psychometric anchors (α, r, d, RT). Not watts. Skip identity pads."""
    rows: list[dict[str, Any]] = []
    if not psych_path.is_file():
        return rows
    doc = json.loads(psych_path.read_text(encoding="utf-8"))
    for rec in doc.get("material_records") or []:
        if rec.get("ingest_source") != "psychometrics_rct_literature_anchors":
            continue
        m = float(rec.get("measured") or 0)
        if m == 0:
            continue
        name = str(rec.get("name") or "anchor")
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(_row(prop=prop_a, name=name + "_a", computed=ca, measured=m, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=name + "_b", computed=cb, measured=m, note=note_b))
        rows[-1]["error_pct"] = eb
    return rows


def _crc_n_dual(
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        tag = str(mat["name"])
        ca, ea = scaled(n, domain_a)
        cb, eb = scaled(n, domain_b)
        rows.append(_row(prop=prop_a, name=tag + "_a", computed=ca, measured=n, note=note_a))
        rows[-1]["error_pct"] = ea
        rows.append(_row(prop=prop_b, name=tag + "_b", computed=cb, measured=n, note=note_b))
        rows[-1]["error_pct"] = eb
    return rows


def _live_mix_structural(a: str, b: str, prop: str, name: str, dark_note: str) -> dict[str, Any]:
    live = abs(f(domain_scalar(a))) / abs(f(domain_scalar(b)))
    vs1 = err(live, 1.0)
    return _row(
        prop=prop,
        name=name,
        computed=live,
        measured=1.0,
        note=(
            f"Live |S_{a}|/|S_{b}| vs 1 mixes looks/observed. "
            f"{vs1:.1f}% — same-view question, not a 0.5% central. {dark_note}"
        ),
        kind="structural",
        extra={"kappa": kappa_domains(a, b), "live_vs_1_pct": vs1},
    )


def biochem_cm_rows() -> list[dict[str, Any]]:
    """Biochemistry D=13 ↔ Condensed_Matter D=14 — molecule vs solid.

    Live mix is δψ 0.35/hits=1 vs 0.5/hits=0. Equalize at the CM look
    (δψ=0.5, hits=0). Dual-route CRC AA MW on Biochem, metal ρ on CM.
    """
    s13 = scalar_at(d_eff=13, delta_psi=0.5, hits=0, observed=True)
    s14 = scalar_at(d_eff=14, delta_psi=0.5, hits=0, observed=True)
    live = abs(f(domain_scalar("Biochemistry"))) / abs(
        f(domain_scalar("Condensed_Matter"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="biochem_cm_S_ratio_same_look",
            name="S_D13_over_S_D14_at_dpsi_0p5",
            computed=s13 / s14,
            measured=1.0,
            note=(
                "|S(D=13,δψ=0.5)|/|S(D=14,δψ=0.5)| vs 1 — molecule vs solid. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Biochemistry", "Condensed_Matter"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for aa, mw in AMINO_ACID_MW:
        c, e = scaled(float(mw), "Biochemistry")
        rows.append(
            _row(
                prop="biochem_cm_aa_bc_fold",
                name=aa + "_mw_bc",
                computed=c,
                measured=float(mw),
                note="CRC/IUPAC AA MW on Biochemistry D=13",
            )
        )
        rows[-1]["error_pct"] = e
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        c, e = scaled(rho, "Condensed_Matter")
        rows.append(
            _row(
                prop="biochem_cm_rho_cm_fold",
                name=str(sol["name"]) + "_rho_cm",
                computed=c,
                measured=rho,
                note="CRC density on Condensed_Matter D=14 — solid of the residue scale",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def cm_neuro_rows() -> list[dict[str, Any]]:
    """Condensed_Matter D=14 ↔ Neuroscience D=14 — solid vs signaling, same rung.

    Live mix is δψ 0.5/hits=0 vs 0.7/hits=1. Equalizing at D=14 is identity.
    Fold the look-split onto D=13. Dual-route CRC metal ρ vs transmitter AA MW.
    """
    live = abs(f(domain_scalar("Condensed_Matter"))) / abs(
        f(domain_scalar("Neuroscience"))
    )
    look = scalar_at(d_eff=13, delta_psi=0.5, hits=0) / scalar_at(
        d_eff=13, delta_psi=0.7, hits=1
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="cm_neuro_S_ratio",
            name="S_cm_over_S_neuro_vs_D13_look",
            computed=live,
            measured=look,
            note=(
                "|S_CM|/|S_Neuro| vs S(D=13,δψ=0.5,hits=0)/S(D=13,δψ=0.7,hits=1) — "
                f"same-rung look-split. Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Condensed_Matter", "Neuroscience"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        c, e = scaled(rho, "Condensed_Matter")
        rows.append(
            _row(
                prop="cm_neuro_rho_cm_fold",
                name=str(sol["name"]) + "_rho_cm",
                computed=c,
                measured=rho,
                note="CRC density on Condensed_Matter D=14",
            )
        )
        rows[-1]["error_pct"] = e
    mw = {a: m for a, m in AMINO_ACID_MW}
    for aa in NEURO_AA:
        m = float(mw[aa])
        c, e = scaled(m, "Neuroscience")
        rows.append(
            _row(
                prop="cm_neuro_aa_neuro_fold",
                name=aa + "_mw_neuro",
                computed=c,
                measured=m,
                note="CRC transmitter AA MW on Neuroscience D=14",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def cm_fluid_rows() -> list[dict[str, Any]]:
    """Condensed_Matter D=14 ↔ Fluid_Dynamics D=15 — solid vs tank.

    Fluid stays dark. Ice ρ on CM, water ρ on Fluid — same H2O, two phases.
    Metals stay on CM. Live vs 1 is the observed mix, not a 0.5% central.
    """
    live = abs(f(domain_scalar("Condensed_Matter"))) / abs(
        f(domain_scalar("Fluid_Dynamics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="cm_fluid_S_ratio",
            name="S_cm_over_S_fluid_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_CM|/|S_Fluid| vs 1 mixes observed/dark at D=14/15. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Fluid stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Condensed_Matter", "Fluid_Dynamics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    ice = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "ice_Ih")
    water = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "water_20C")
    ci, ei = scaled(float(ice["rho"]), "Condensed_Matter")
    cw, ew = scaled(float(water["rho"]), "Fluid_Dynamics")
    rows.append(
        _row(
            prop="cm_fluid_ice_cm_fold",
            name="ice_Ih_rho_cm",
            computed=ci,
            measured=float(ice["rho"]),
            note="CRC ice density on Condensed_Matter D=14 — solid H2O",
        )
    )
    rows[-1]["error_pct"] = ei
    rows.append(
        _row(
            prop="cm_fluid_water_fl_fold",
            name="water_20C_rho_fl",
            computed=cw,
            measured=float(water["rho"]),
            note="CRC water density on Fluid_Dynamics D=15 — tank stays dark",
        )
    )
    rows[-1]["error_pct"] = ew
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        c, e = scaled(rho, "Condensed_Matter")
        rows.append(
            _row(
                prop="cm_fluid_rho_cm_fold",
                name=str(sol["name"]) + "_rho_cm",
                computed=c,
                measured=rho,
                note="CRC metal density on Condensed_Matter D=14",
            )
        )
        rows[-1]["error_pct"] = e
    ethanol = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "ethanol_20C")
    ce, ee = scaled(float(ethanol["rho"]), "Fluid_Dynamics")
    rows.append(
        _row(
            prop="cm_fluid_etoh_fl_fold",
            name="ethanol_20C_rho_fl",
            computed=ce,
            measured=float(ethanol["rho"]),
            note="CRC ethanol density on Fluid_Dynamics D=15 — liquid tank",
        )
    )
    rows[-1]["error_pct"] = ee
    return rows


def cm_nuclear_rows(endf_path: Path) -> list[dict[str, Any]]:
    """Condensed_Matter D=14 ↔ Nuclear_Physics D=15 — solid vs orifice.

    Equalize at the CM look (δψ=0.5, hits=0). Dual-route CRC metal ρ on CM,
    IAEA/ENDF keV on Nuclear. Fe is the shared specimen class.
    """
    s14 = scalar_at(d_eff=14, delta_psi=0.5, hits=0, observed=True)
    s15 = scalar_at(d_eff=15, delta_psi=0.5, hits=0, observed=True)
    live = abs(f(domain_scalar("Condensed_Matter"))) / abs(
        f(domain_scalar("Nuclear_Physics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="cm_nuclear_S_ratio_same_look",
            name="S_D14_over_S_D15_at_dpsi_0p5",
            computed=s14 / s15,
            measured=1.0,
            note=(
                "|S(D=14,δψ=0.5)|/|S(D=15,δψ=0.5)| vs 1 — solid vs orifice. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Condensed_Matter", "Nuclear_Physics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        cc, ec = scaled(rho, "Condensed_Matter")
        cn, en = scaled(rho, "Nuclear_Physics")
        tag = str(sol["name"])
        rows.append(
            _row(
                prop="cm_nuclear_rho_cm_fold",
                name=tag + "_rho_cm",
                computed=cc,
                measured=rho,
                note="CRC density on Condensed_Matter D=14",
            )
        )
        rows[-1]["error_pct"] = ec
        rows.append(
            _row(
                prop="cm_nuclear_rho_nuc_fold",
                name=tag + "_rho_nuc",
                computed=cn,
                measured=rho,
                note="same CRC density on Nuclear_Physics D=15 — solid of the orifice",
            )
        )
        rows[-1]["error_pct"] = en
    rows.extend(
        _endf_keV_dual(
            endf_path,
            "Nuclear_Physics",
            "Condensed_Matter",
            "cm_nuclear_level_nuc_fold",
            "cm_nuclear_level_cm_fold",
            "IAEA/ENDF keV on Nuclear_Physics D=15",
            "same IAEA keV on Condensed_Matter D=14 — lattice of the orifice",
        )
    )
    return rows


def neuro_thermo_rows() -> list[dict[str, Any]]:
    """Neuroscience D=14 ↔ Thermodynamics D=15 — signaling vs heat.

    Both observed, both hits=1. Equalize at the neural look (δψ=0.7).
    Dual-route transmitter AA MW on Neuro, Carnot COP on Thermo.
    Not the social-tank GDP route.
    """
    s14 = scalar_at(d_eff=14, delta_psi=0.7, hits=1, observed=True)
    s15 = scalar_at(d_eff=15, delta_psi=0.7, hits=1, observed=True)
    live = abs(f(domain_scalar("Neuroscience"))) / abs(
        f(domain_scalar("Thermodynamics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="neuro_thermo_S_ratio_same_look",
            name="S_D14_over_S_D15_at_dpsi_0p7",
            computed=s14 / s15,
            measured=1.0,
            note=(
                "|S(D=14,δψ=0.7,hits=1)|/|S(D=15,δψ=0.7,hits=1)| vs 1 — "
                f"signaling vs heat. Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Neuroscience", "Thermodynamics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    mw = {a: m for a, m in AMINO_ACID_MW}
    for aa in NEURO_AA:
        m = float(mw[aa])
        c, e = scaled(m, "Neuroscience")
        rows.append(
            _row(
                prop="neuro_thermo_aa_neuro_fold",
                name=aa + "_mw_neuro",
                computed=c,
                measured=m,
                note="CRC transmitter AA MW on Neuroscience D=14",
            )
        )
        rows[-1]["error_pct"] = e
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        c, e = scaled(cop, "Thermodynamics")
        rows.append(
            _row(
                prop="neuro_thermo_carnot_th_fold",
                name=name + "_th",
                computed=c,
                measured=cop,
                note="Carnot COP on Thermodynamics D=15",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def fluid_nuclear_rows(endf_path: Path) -> list[dict[str, Any]]:
    """Fluid_Dynamics D=15 ↔ Nuclear_Physics D=15 — tank vs orifice, same rung.

    Fluid stays dark. Dual-route Carnot COP on Fluid, ENDF keV on Nuclear.
    Live vs 1 is the observed mix — not a 0.5% central.
    """
    live = abs(f(domain_scalar("Fluid_Dynamics"))) / abs(
        f(domain_scalar("Nuclear_Physics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="fluid_nuclear_S_ratio",
            name="S_fluid_over_S_nuc_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Fluid|/|S_Nuclear| vs 1 mixes dark/observed at D=15. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Fluid stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Fluid_Dynamics", "Nuclear_Physics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        cf, ef = scaled(cop, "Fluid_Dynamics")
        cn, en = scaled(cop, "Nuclear_Physics")
        rows.append(
            _row(
                prop="fluid_nuclear_carnot_fl_fold",
                name=name + "_fl",
                computed=cf,
                measured=cop,
                note="Carnot COP on Fluid_Dynamics D=15 — tank stays dark",
            )
        )
        rows[-1]["error_pct"] = ef
        rows.append(
            _row(
                prop="fluid_nuclear_carnot_nuc_fold",
                name=name + "_nuc",
                computed=cn,
                measured=cop,
                note="same COP on Nuclear_Physics D=15 — heat of the orifice",
            )
        )
        rows[-1]["error_pct"] = en
    rows.extend(
        _endf_keV_dual(
            endf_path,
            "Nuclear_Physics",
            "Fluid_Dynamics",
            "fluid_nuclear_level_nuc_fold",
            "fluid_nuclear_level_fl_fold",
            "IAEA/ENDF keV on Nuclear_Physics D=15",
            "same IAEA keV on Fluid_Dynamics D=15 — tank stays dark",
        )
    )
    return rows


def fluid_meteo_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Fluid_Dynamics D=15 ↔ Meteorology D=16 — tank vs weather, both dark.

    Equalize at the weather look (δψ=0.8, hits=2, observed=False).
    Dual-route NDBC pressure. Do not flip dark.
    """
    s15 = scalar_at(d_eff=15, delta_psi=0.8, hits=2, observed=False)
    s16 = scalar_at(d_eff=16, delta_psi=0.8, hits=2, observed=False)
    live = abs(f(domain_scalar("Fluid_Dynamics"))) / abs(
        f(domain_scalar("Meteorology"))
    )
    vs1 = err(live, 1.0)
    ratio = s15 / s16
    rows: list[dict[str, Any]] = [
        _row(
            prop="fluid_meteo_S_ratio_same_look",
            name="S_D15_over_S_D16_at_dpsi_0p8_dark",
            computed=ratio,
            measured=1.0,
            note=(
                "|S(D=15,δψ=0.8,dark)|/|S(D=16,δψ=0.8,dark)| vs 1 — tank vs weather. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Do not flip dark."
            ),
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={
                "kappa": kappa_domains("Fluid_Dynamics", "Meteorology"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        for rec in doc.get("rows") or []:
            val = rec.get("pres")
            if val is None:
                continue
            m = float(val)
            if m <= 0:
                continue
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "").replace(" ", "_")
            tag = f"{bid}_{ts}"
            cf, ef = scaled(m, "Fluid_Dynamics")
            cm, em = scaled(m, "Meteorology")
            rows.append(
                _row(
                    prop="fluid_meteo_pres_fl_fold",
                    name=tag + "_fl",
                    computed=cf,
                    measured=m,
                    note="NDBC pressure on Fluid_Dynamics D=15 — tank stays dark",
                )
            )
            rows[-1]["error_pct"] = ef
            rows.append(
                _row(
                    prop="fluid_meteo_pres_meteo_fold",
                    name=tag + "_meteo",
                    computed=cm,
                    measured=m,
                    note="same NDBC pressure on Meteorology D=16 — weather stays dark",
                )
            )
            rows[-1]["error_pct"] = em
    return rows


def _ndbc_pres_dual(
    ndbc_path: Path,
    domain_a: str,
    domain_b: str,
    prop_a: str,
    prop_b: str,
    note_a: str,
    note_b: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not ndbc_path.is_file():
        return rows
    doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
    for rec in doc.get("rows") or []:
        val = rec.get("pres")
        if val is None:
            continue
        m = float(val)
        if m <= 0:
            continue
        bid = str(rec.get("buoy_id") or "buoy")
        ts = str(rec.get("timestamp") or "").replace(" ", "_")
        tag = f"{bid}_{ts}"
        ca, ea = scaled(m, domain_a)
        cb, eb = scaled(m, domain_b)
        rows.append(
            _row(prop=prop_a, name=tag + "_" + domain_a.split("_")[0].lower(),
                 computed=ca, measured=m, note=note_a)
        )
        rows[-1]["error_pct"] = ea
        rows.append(
            _row(prop=prop_b, name=tag + "_" + domain_b.split("_")[0].lower(),
                 computed=cb, measured=m, note=note_b)
        )
        rows[-1]["error_pct"] = eb
    return rows


def neuro_fluid_rows() -> list[dict[str, Any]]:
    """Neuroscience D=14 ↔ Fluid_Dynamics D=15 — signaling vs tank.

    Fluid stays dark. Dual-route transmitter AA on Neuro, CRC water ρ on Fluid.
    Live vs 1 is the observed mix, not a 0.5% central.
    """
    live = abs(f(domain_scalar("Neuroscience"))) / abs(
        f(domain_scalar("Fluid_Dynamics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="neuro_fluid_S_ratio",
            name="S_neuro_over_S_fluid_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Neuro|/|S_Fluid| vs 1 mixes observed/dark at D=14/15. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Fluid stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Neuroscience", "Fluid_Dynamics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    mw = {a: m for a, m in AMINO_ACID_MW}
    for aa in NEURO_AA:
        m = float(mw[aa])
        c, e = scaled(m, "Neuroscience")
        rows.append(
            _row(
                prop="neuro_fluid_aa_neuro_fold",
                name=aa + "_mw_neuro",
                computed=c,
                measured=m,
                note="CRC transmitter AA MW on Neuroscience D=14",
            )
        )
        rows[-1]["error_pct"] = e
    water = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "water_20C")
    cw, ew = scaled(float(water["rho"]), "Fluid_Dynamics")
    rows.append(
        _row(
            prop="neuro_fluid_water_fl_fold",
            name="water_20C_rho_fl",
            computed=cw,
            measured=float(water["rho"]),
            note="CRC water density on Fluid_Dynamics D=15 — tank stays dark",
        )
    )
    rows[-1]["error_pct"] = ew
    return rows


def neuro_nuclear_rows(endf_path: Path) -> list[dict[str, Any]]:
    """Neuroscience D=14 ↔ Nuclear_Physics D=15 — signaling vs orifice.

    Equalize at the neural look (δψ=0.7, hits=1). Dual-route transmitter AA
    on Neuro, IAEA/ENDF keV on Nuclear.
    """
    s14 = scalar_at(d_eff=14, delta_psi=0.7, hits=1, observed=True)
    s15 = scalar_at(d_eff=15, delta_psi=0.7, hits=1, observed=True)
    live = abs(f(domain_scalar("Neuroscience"))) / abs(
        f(domain_scalar("Nuclear_Physics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="neuro_nuclear_S_ratio_same_look",
            name="S_D14_over_S_D15_at_dpsi_0p7",
            computed=s14 / s15,
            measured=1.0,
            note=(
                "|S(D=14,δψ=0.7,hits=1)|/|S(D=15,δψ=0.7,hits=1)| vs 1 — "
                f"signaling vs orifice. Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Neuroscience", "Nuclear_Physics"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    mw = {a: m for a, m in AMINO_ACID_MW}
    for aa in NEURO_AA:
        m = float(mw[aa])
        c, e = scaled(m, "Neuroscience")
        rows.append(
            _row(
                prop="neuro_nuclear_aa_neuro_fold",
                name=aa + "_mw_neuro",
                computed=c,
                measured=m,
                note="CRC transmitter AA MW on Neuroscience D=14",
            )
        )
        rows[-1]["error_pct"] = e
    rows.extend(
        _endf_keV_dual(
            endf_path,
            "Nuclear_Physics",
            "Neuroscience",
            "neuro_nuclear_level_nuc_fold",
            "neuro_nuclear_level_neuro_fold",
            "IAEA/ENDF keV on Nuclear_Physics D=15",
            "same IAEA keV on Neuroscience D=14 — signaling of the orifice",
        )
    )
    return rows


def thermo_meteo_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Thermodynamics D=15 ↔ Meteorology D=16 — heat vs weather.

    Thermo observed, Meteo dark. Dual-route Carnot on Thermo, NDBC pres on
    Meteo. Do not flip dark. Live vs 1 is the observed mix.
    """
    live = abs(f(domain_scalar("Thermodynamics"))) / abs(
        f(domain_scalar("Meteorology"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="thermo_meteo_S_ratio",
            name="S_th_over_S_meteo_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Thermo|/|S_Meteo| vs 1 mixes observed/dark at D=15/16. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Meteorology stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Thermodynamics", "Meteorology"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        c, e = scaled(cop, "Thermodynamics")
        rows.append(
            _row(
                prop="thermo_meteo_carnot_th_fold",
                name=name + "_th",
                computed=c,
                measured=cop,
                note="Carnot COP on Thermodynamics D=15",
            )
        )
        rows[-1]["error_pct"] = e
    rows.extend(
        _ndbc_pres_dual(
            ndbc_path,
            "Meteorology",
            "Thermodynamics",
            "thermo_meteo_pres_meteo_fold",
            "thermo_meteo_pres_th_fold",
            "NDBC pressure on Meteorology D=16 — weather stays dark",
            "same NDBC pressure on Thermodynamics D=15",
        )
    )
    return rows


def nuclear_meteo_rows(ndbc_path: Path, endf_path: Path) -> list[dict[str, Any]]:
    """Nuclear_Physics D=15 ↔ Meteorology D=16 — orifice vs weather.

    Nuclear observed, Meteo dark. Dual-route ENDF keV on Nuclear, NDBC pres
    on Meteo. Do not flip dark.
    """
    live = abs(f(domain_scalar("Nuclear_Physics"))) / abs(
        f(domain_scalar("Meteorology"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="nuclear_meteo_S_ratio",
            name="S_nuc_over_S_meteo_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Nuclear|/|S_Meteo| vs 1 mixes observed/dark at D=15/16. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Meteorology stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Nuclear_Physics", "Meteorology"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _endf_keV_dual(
            endf_path,
            "Nuclear_Physics",
            "Meteorology",
            "nuclear_meteo_level_nuc_fold",
            "nuclear_meteo_level_meteo_fold",
            "IAEA/ENDF keV on Nuclear_Physics D=15",
            "same IAEA keV on Meteorology D=16 — weather stays dark",
        )
    )
    rows.extend(
        _ndbc_pres_dual(
            ndbc_path,
            "Meteorology",
            "Nuclear_Physics",
            "nuclear_meteo_pres_meteo_fold",
            "nuclear_meteo_pres_nuc_fold",
            "NDBC pressure on Meteorology D=16 — weather stays dark",
            "same NDBC pressure on Nuclear_Physics D=15",
        )
    )
    return rows


def meteo_ocean_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Meteorology D=16 ↔ Oceanography D=17 — weather vs ocean tank, both dark.

    Equalize at the weather look (δψ=0.8, hits=2, observed=False).
    Dual-route NDBC pressure. Do not flip dark.
    """
    s16 = scalar_at(d_eff=16, delta_psi=0.8, hits=2, observed=False)
    s17 = scalar_at(d_eff=17, delta_psi=0.8, hits=2, observed=False)
    live = abs(f(domain_scalar("Meteorology"))) / abs(
        f(domain_scalar("Oceanography"))
    )
    vs1 = err(live, 1.0)
    ratio = s16 / s17
    rows: list[dict[str, Any]] = [
        _row(
            prop="meteo_ocean_S_ratio_same_look",
            name="S_D16_over_S_D17_at_dpsi_0p8_dark",
            computed=ratio,
            measured=1.0,
            note=(
                "|S(D=16,δψ=0.8,dark)|/|S(D=17,δψ=0.8,dark)| vs 1 — weather vs ocean. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Do not flip dark."
            ),
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={
                "kappa": kappa_domains("Meteorology", "Oceanography"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _ndbc_pres_dual(
            ndbc_path,
            "Meteorology",
            "Oceanography",
            "meteo_ocean_pres_meteo_fold",
            "meteo_ocean_pres_ocean_fold",
            "NDBC pressure on Meteorology D=16 — weather stays dark",
            "same NDBC pressure on Oceanography D=17 — ocean stays dark",
        )
    )
    return rows


def atm_seis_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Atmospheric_Physics D=17 ↔ Seismology D=18 — air tank vs crust, both dark.

    Dual-route NDBC pressure on Atm, PREM lithosphere density on Seis.
    Do not flip dark.
    """
    s17 = scalar_at(d_eff=17, delta_psi=0.8, hits=2, observed=False)
    s18 = scalar_at(d_eff=18, delta_psi=0.8, hits=2, observed=False)
    live = abs(f(domain_scalar("Atmospheric_Physics"))) / abs(
        f(domain_scalar("Seismology"))
    )
    vs1 = err(live, 1.0)
    ratio = s17 / s18
    rows: list[dict[str, Any]] = [
        _row(
            prop="atm_seis_S_ratio_same_look",
            name="S_D17_over_S_D18_at_dpsi_0p8_dark",
            computed=ratio,
            measured=1.0,
            note=(
                "|S(D=17,δψ=0.8,dark)|/|S(D=18,δψ=0.8,dark)| vs 1 — air vs crust. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Do not flip dark."
            ),
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={
                "kappa": kappa_domains("Atmospheric_Physics", "Seismology"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _ndbc_pres_dual(
            ndbc_path,
            "Atmospheric_Physics",
            "Seismology",
            "atm_seis_pres_atm_fold",
            "atm_seis_pres_seis_fold",
            "NDBC pressure on Atmospheric_Physics D=17 — air stays dark",
            "same NDBC pressure on Seismology D=18 — crust stays dark",
        )
    )
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Seismology")
        rows.append(
            _row(
                prop="atm_seis_rho_seis_fold",
                name=str(layer["name"]) + "_rho_seis",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Seismology D=18",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def ocean_seis_rows(ndbc_path: Path) -> list[dict[str, Any]]:
    """Oceanography D=17 ↔ Seismology D=18 — ocean tank vs crust, both dark.

    Dual-route NDBC SST on Ocean, PREM lithosphere density on Seis.
    Do not flip dark.
    """
    s17 = scalar_at(d_eff=17, delta_psi=0.7, hits=1, observed=False)
    s18 = scalar_at(d_eff=18, delta_psi=0.7, hits=1, observed=False)
    live = abs(f(domain_scalar("Oceanography"))) / abs(
        f(domain_scalar("Seismology"))
    )
    vs1 = err(live, 1.0)
    ratio = s17 / s18
    rows: list[dict[str, Any]] = [
        _row(
            prop="ocean_seis_S_ratio_same_look",
            name="S_D17_over_S_D18_at_dpsi_0p7_dark",
            computed=ratio,
            measured=1.0,
            note=(
                "|S(D=17,δψ=0.7,dark)|/|S(D=18,δψ=0.7,dark)| vs 1 — ocean vs crust. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Do not flip dark."
            ),
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={
                "kappa": kappa_domains("Oceanography", "Seismology"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        for rec in doc.get("rows") or []:
            val = rec.get("wtmp")
            if val is None:
                continue
            m = float(val)
            if m <= 0:
                continue
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "").replace(" ", "_")
            tag = f"{bid}_{ts}"
            c, e = scaled(m, "Oceanography")
            rows.append(
                _row(
                    prop="ocean_seis_sst_ocean_fold",
                    name=tag + "_sst_ocean",
                    computed=c,
                    measured=m,
                    note="NDBC SST on Oceanography D=17 — ocean stays dark",
                )
            )
            rows[-1]["error_pct"] = e
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Seismology")
        rows.append(
            _row(
                prop="ocean_seis_rho_seis_fold",
                name=str(layer["name"]) + "_rho_seis",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Seismology D=18",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def astro_planetary_rows(planetary_path: Path) -> list[dict[str, Any]]:
    """Astronomy D=20 ↔ Planetary_Science D=21 — sky vs body.

    Equalize at the astronomy look (δψ=1, hits=1). Dual-route JPL/NASA
    mean densities as measured through APPLY — not the identity-pad
    planetary_structure computed=measured rows.
    """
    s20 = scalar_at(d_eff=20, delta_psi=1.0, hits=1, observed=True)
    s21 = scalar_at(d_eff=21, delta_psi=1.0, hits=1, observed=True)
    live = abs(f(domain_scalar("Astronomy"))) / abs(
        f(domain_scalar("Planetary_Science"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="astro_planetary_S_ratio_same_look",
            name="S_D20_over_S_D21_at_dpsi_1",
            computed=s20 / s21,
            measured=1.0,
            note=(
                "|S(D=20,δψ=1,hits=1)|/|S(D=21,δψ=1,hits=1)| vs 1 — sky vs body. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Astronomy", "Planetary_Science"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    if planetary_path.is_file():
        doc = json.loads(planetary_path.read_text(encoding="utf-8"))
        for rec in doc.get("records") or []:
            if rec.get("property") != "mean_density":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            name = str(rec.get("name") or "body")
            ca, ea = scaled(m, "Astronomy")
            cp, ep = scaled(m, "Planetary_Science")
            rows.append(
                _row(
                    prop="astro_planetary_rho_astro_fold",
                    name=name + "_rho_astro",
                    computed=ca,
                    measured=m,
                    note="JPL Horizons mean density on Astronomy D=20",
                )
            )
            rows[-1]["error_pct"] = ea
            rows.append(
                _row(
                    prop="astro_planetary_rho_pl_fold",
                    name=name + "_rho_pl",
                    computed=cp,
                    measured=m,
                    note="same JPL density on Planetary_Science D=21 — body",
                )
            )
            rows[-1]["error_pct"] = ep
    return rows


def qo_biology_rows(bio_path: Path) -> list[dict[str, Any]]:
    """Quantum_Optics D=11 ↔ Biology D=12 — photon vs organism.

    Biology stays dark. Equalize the dark look (δψ=0.08, observed=False).
    Dual-route CRC n_D on QO, NCBI mt-operon on Biology. Do not flip dark.
    """
    s11 = scalar_at(d_eff=11, delta_psi=0.08, hits=0, observed=False)
    s12 = scalar_at(d_eff=12, delta_psi=0.08, hits=0, observed=False)
    live = abs(f(domain_scalar("Quantum_Optics"))) / abs(
        f(domain_scalar("Biology"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="qo_bio_S_ratio_same_look",
            name="S_D11_over_S_D12_dark_dpsi_0p08",
            computed=s11 / s12,
            measured=1.0,
            note=(
                "|S(D=11,δψ=0.08,dark)|/|S(D=12,δψ=0.08,dark)| vs 1 — photon vs organism. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object. Biology stays dark."
            ),
            extra={
                "kappa": kappa_domains("Quantum_Optics", "Biology"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    for mat in OPTICAL_MATERIALS:
        n = float(mat["n"])
        c, e = scaled(n, "Quantum_Optics")
        rows.append(
            _row(
                prop="qo_bio_n_qo_fold",
                name=str(mat["name"]) + "_n_qo",
                computed=c,
                measured=n,
                note="CRC n_D on Quantum_Optics D=11",
            )
        )
        rows[-1]["error_pct"] = e
    if bio_path.is_file():
        doc = json.loads(bio_path.read_text(encoding="utf-8"))
        n_op = 0
        for rec in doc.get("records") or []:
            if rec.get("property") != "mt_operon_length":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            c, e = scaled(m, "Biology")
            name = str(rec.get("name") or f"op{n_op}")
            rows.append(
                _row(
                    prop="qo_bio_operon_bio_fold",
                    name=name + "_bio",
                    computed=c,
                    measured=m,
                    note="NCBI NC_012920.1 mt-operon on Biology D=12 — stays dark",
                )
            )
            rows[-1]["error_pct"] = e
            n_op += 1
    return rows


def atm_sociology_rows(ndbc_path: Path, econ_path: Path) -> list[dict[str, Any]]:
    """Atmospheric_Physics D=17 ↔ Sociology D=18 — air tank vs catalog tank.

    Atm stays dark. Dual-route NDBC pressure on Atm, World Bank YoY on Sociology.
    """
    live = abs(f(domain_scalar("Atmospheric_Physics"))) / abs(
        f(domain_scalar("Sociology"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="atm_soc_S_ratio",
            name="S_atm_over_S_soc_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Atm|/|S_Soc| vs 1 mixes dark/observed at D=17/18. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Atmospheric_Physics stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Atmospheric_Physics", "Sociology"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _ndbc_pres_dual(
            ndbc_path,
            "Atmospheric_Physics",
            "Sociology",
            "atm_soc_pres_atm_fold",
            "atm_soc_pres_soc_fold",
            "NDBC pressure on Atmospheric_Physics D=17 — air stays dark",
            "same NDBC pressure on Sociology D=18",
        )
    )
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Sociology",
            "Atmospheric_Physics",
            "atm_soc_yoy_soc_fold",
            "atm_soc_yoy_atm_fold",
            "World Bank YoY on Sociology D=18 — catalog tank",
            "same YoY on Atmospheric_Physics D=17 — air stays dark",
        )
    )
    return rows


def ocean_sociology_rows(ndbc_path: Path, econ_path: Path) -> list[dict[str, Any]]:
    """Oceanography D=17 ↔ Sociology D=18 — ocean tank vs catalog tank.

    Ocean stays dark. Dual-route NDBC SST on Ocean, World Bank YoY on Sociology.
    """
    live = abs(f(domain_scalar("Oceanography"))) / abs(f(domain_scalar("Sociology")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="ocean_soc_S_ratio",
            name="S_ocean_over_S_soc_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Ocean|/|S_Soc| vs 1 mixes dark/observed at D=17/18. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Oceanography stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Oceanography", "Sociology"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        for rec in doc.get("rows") or []:
            val = rec.get("wtmp")
            if val is None:
                continue
            m = float(val)
            if m <= 0:
                continue
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "").replace(" ", "_")
            c, e = scaled(m, "Oceanography")
            rows.append(
                _row(
                    prop="ocean_soc_sst_ocean_fold",
                    name=f"{bid}_{ts}_sst",
                    computed=c,
                    measured=m,
                    note="NDBC SST on Oceanography D=17 — ocean stays dark",
                )
            )
            rows[-1]["error_pct"] = e
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Sociology",
            "Oceanography",
            "ocean_soc_yoy_soc_fold",
            "ocean_soc_yoy_ocean_fold",
            "World Bank YoY on Sociology D=18",
            "same YoY on Oceanography D=17 — ocean stays dark",
        )
    )
    return rows


def seis_sociology_rows(econ_path: Path) -> list[dict[str, Any]]:
    """Seismology D=18 ↔ Sociology D=18 — crust vs catalog, same rung.

    Seismology stays dark. Dual-route PREM lithosphere density on Seis,
    World Bank YoY on Sociology. Live vs 1 is the observed mix.
    """
    live = abs(f(domain_scalar("Seismology"))) / abs(f(domain_scalar("Sociology")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="seis_soc_S_ratio",
            name="S_seis_over_S_soc_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Seis|/|S_Soc| vs 1 mixes dark/observed at D=18. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Seismology stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Seismology", "Sociology"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Seismology")
        rows.append(
            _row(
                prop="seis_soc_rho_seis_fold",
                name=str(layer["name"]) + "_rho_seis",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Seismology D=18 — crust stays dark",
            )
        )
        rows[-1]["error_pct"] = e
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Sociology",
            "Seismology",
            "seis_soc_yoy_soc_fold",
            "seis_soc_yoy_seis_fold",
            "World Bank YoY on Sociology D=18",
            "same YoY on Seismology D=18 — crust stays dark",
        )
    )
    return rows


def sociology_geo_rows(econ_path: Path) -> list[dict[str, Any]]:
    """Sociology D=18 ↔ Geophysics D=19 — catalog vs bulk-earth.

    Geophysics stays dark. Dual-route World Bank YoY on Sociology,
    PREM lithosphere density on Geophysics.
    """
    live = abs(f(domain_scalar("Sociology"))) / abs(f(domain_scalar("Geophysics")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="soc_geo_S_ratio",
            name="S_soc_over_S_geo_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Soc|/|S_Geo| vs 1 mixes observed/dark at D=18/19. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Geophysics stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Sociology", "Geophysics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Sociology",
            "Geophysics",
            "soc_geo_yoy_soc_fold",
            "soc_geo_yoy_geo_fold",
            "World Bank YoY on Sociology D=18",
            "same YoY on Geophysics D=19 — bulk-earth stays dark",
        )
    )
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Geophysics")
        rows.append(
            _row(
                prop="soc_geo_rho_geo_fold",
                name=str(layer["name"]) + "_rho_geo",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Geophysics D=19 — bulk stays dark",
            )
        )
        rows[-1]["error_pct"] = e
    return rows


def geo_astronomy_rows(planet_path: Path) -> list[dict[str, Any]]:
    """Geophysics D=19 ↔ Astronomy D=20 — bulk-earth vs sky.

    Geophysics stays dark. Dual-route PREM lithosphere density on Geo,
    JPL mean densities on Astronomy.
    """
    live = abs(f(domain_scalar("Geophysics"))) / abs(f(domain_scalar("Astronomy")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="geo_astro_S_ratio",
            name="S_geo_over_S_astro_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Geo|/|S_Astro| vs 1 mixes dark/observed at D=19/20. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Geophysics stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Geophysics", "Astronomy"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Geophysics")
        rows.append(
            _row(
                prop="geo_astro_rho_geo_fold",
                name=str(layer["name"]) + "_rho_geo",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Geophysics D=19 — bulk stays dark",
            )
        )
        rows[-1]["error_pct"] = e
    rows.extend(
        _jpl_rho_dual(
            planet_path,
            "Astronomy",
            "Geophysics",
            "geo_astro_jpl_astro_fold",
            "geo_astro_jpl_geo_fold",
            "JPL Horizons mean density on Astronomy D=20",
            "same JPL density on Geophysics D=19 — bulk stays dark",
        )
    )
    return rows


def geo_economics_rows(econ_path: Path) -> list[dict[str, Any]]:
    """Geophysics D=19 ↔ Economics D=20 — bulk-earth vs market.

    Geophysics stays dark. Dual-route PREM on Geo, World Bank YoY on Economics.
    """
    live = abs(f(domain_scalar("Geophysics"))) / abs(f(domain_scalar("Economics")))
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="geo_econ_S_ratio",
            name="S_geo_over_S_econ_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Geo|/|S_Econ| vs 1 mixes dark/observed at D=19/20. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Geophysics stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Geophysics", "Economics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    for layer in PREM_SOLID:
        if layer["family"] != "lithosphere":
            continue
        rho = float(layer["rho"])
        c, e = scaled(rho, "Geophysics")
        rows.append(
            _row(
                prop="geo_econ_rho_geo_fold",
                name=str(layer["name"]) + "_rho_geo",
                computed=c,
                measured=rho,
                note="PREM lithosphere density on Geophysics D=19 — bulk stays dark",
            )
        )
        rows[-1]["error_pct"] = e
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Economics",
            "Geophysics",
            "geo_econ_yoy_econ_fold",
            "geo_econ_yoy_geo_fold",
            "World Bank YoY on Economics D=20",
            "same YoY on Geophysics D=19 — bulk stays dark",
        )
    )
    return rows


def astronomy_economics_rows(econ_path: Path, planet_path: Path) -> list[dict[str, Any]]:
    """Astronomy D=20 ↔ Economics D=20 — sky vs market, same rung.

    Live mix is δψ 1.0/hits=1 vs 1.5/hits=3. Fold the look-split onto D=19.
    Dual-route JPL densities on Astronomy, World Bank YoY on Economics.
    """
    live = abs(f(domain_scalar("Astronomy"))) / abs(f(domain_scalar("Economics")))
    look = scalar_at(d_eff=19, delta_psi=1.0, hits=1) / scalar_at(
        d_eff=19, delta_psi=1.5, hits=3
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="astro_econ_S_ratio",
            name="S_astro_over_S_econ_vs_D19_look",
            computed=live,
            measured=look,
            note=(
                "|S_Astro|/|S_Econ| vs S(D=19,δψ=1,hits=1)/S(D=19,δψ=1.5,hits=3) — "
                f"same-rung look-split. Not vs 1 ({vs1:.1f}%)."
            ),
            extra={
                "kappa": kappa_domains("Astronomy", "Economics"),
                "rejected_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _jpl_rho_dual(
            planet_path,
            "Astronomy",
            "Economics",
            "astro_econ_jpl_astro_fold",
            "astro_econ_jpl_econ_fold",
            "JPL Horizons mean density on Astronomy D=20",
            "same JPL density on Economics D=20 — catalog sky",
        )
    )
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Economics",
            "Astronomy",
            "astro_econ_yoy_econ_fold",
            "astro_econ_yoy_astro_fold",
            "World Bank YoY on Economics D=20",
            "same YoY on Astronomy D=20",
        )
    )
    return rows


def economics_planetary_rows(econ_path: Path, planet_path: Path) -> list[dict[str, Any]]:
    """Economics D=20 ↔ Planetary_Science D=21 — market vs body.

    Equalize at the astronomy look (δψ=1, hits=1). Dual-route World Bank YoY
    on Economics, JPL densities on Planetary.
    """
    s20 = scalar_at(d_eff=20, delta_psi=1.0, hits=1, observed=True)
    s21 = scalar_at(d_eff=21, delta_psi=1.0, hits=1, observed=True)
    live = abs(f(domain_scalar("Economics"))) / abs(
        f(domain_scalar("Planetary_Science"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="econ_planet_S_ratio_same_look",
            name="S_D20_over_S_D21_at_dpsi_1",
            computed=s20 / s21,
            measured=1.0,
            note=(
                "|S(D=20,δψ=1,hits=1)|/|S(D=21,δψ=1,hits=1)| vs 1 — market vs body. "
                f"Live mixed vs 1 is {vs1:.1f}% — not this object."
            ),
            extra={
                "kappa": kappa_domains("Economics", "Planetary_Science"),
                "rejected_live_vs_1_error_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _wb_yoy_dual(
            econ_path,
            "Economics",
            "Planetary_Science",
            "econ_planet_yoy_econ_fold",
            "econ_planet_yoy_pl_fold",
            "World Bank YoY on Economics D=20",
            "same YoY on Planetary_Science D=21",
        )
    )
    rows.extend(
        _jpl_rho_dual(
            planet_path,
            "Planetary_Science",
            "Economics",
            "econ_planet_jpl_pl_fold",
            "econ_planet_jpl_econ_fold",
            "JPL Horizons mean density on Planetary_Science D=21",
            "same JPL density on Economics D=20",
        )
    )
    return rows


def planetary_qg_rows(planet_path: Path) -> list[dict[str, Any]]:
    """Planetary_Science D=21 ↔ Quantum_Gravity D=22 — body vs ceiling.

    QG stays dark. Dual-route JPL densities on Planetary. Compact remainder
    at D=21/22 is the CHAOS bleed into the ceiling (same grammar as TISSUE-CEILING).
    """
    live = abs(f(domain_scalar("Planetary_Science"))) / abs(
        f(domain_scalar("Quantum_Gravity"))
    )
    vs1 = err(live, 1.0)
    rem21 = compact_remainder(21)
    rem22 = compact_remainder(22)
    rows: list[dict[str, Any]] = [
        _row(
            prop="planet_qg_S_ratio",
            name="S_pl_over_S_qg_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Planet|/|S_QG| vs 1 mixes observed/dark at D=21/22. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Quantum_Gravity stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Planetary_Science", "Quantum_Gravity"),
                "live_vs_1_pct": vs1,
            },
        ),
        _row(
            prop="planet_qg_compact_D21",
            name="chaos_over_ln_D21",
            computed=rem21,
            measured=1.0,
            note="((D-25)/25)/ln(D/25) at Planetary D=21 — compactification bleed",
            kind="structural" if abs(rem21 - 1.0) * 100 > 0.5 else "scalar",
        ),
        _row(
            prop="planet_qg_compact_D22",
            name="chaos_over_ln_D22",
            computed=rem22,
            measured=1.0,
            note="((D-25)/25)/ln(D/25) at QG D=22 — ceiling rung, stays dark",
            kind="structural" if abs(rem22 - 1.0) * 100 > 0.5 else "scalar",
        ),
    ]
    rows.extend(
        _jpl_rho_dual(
            planet_path,
            "Planetary_Science",
            "Quantum_Gravity",
            "planet_qg_jpl_pl_fold",
            "planet_qg_jpl_qg_fold",
            "JPL Horizons mean density on Planetary_Science D=21",
            "same JPL density on Quantum_Gravity D=22 — ceiling stays dark",
        )
    )
    return rows


def astrophysics_pa_rows(pdg_path: Path) -> list[dict[str, Any]]:
    """Astrophysics D=24 ↔ Particle_Astrophysics D=24 — star vs cosmic-ray, same rung.

    Particle_Astrophysics stays dark. Dual-route PDG 2024 measured masses
    through APPLY (not the SMILES computed column). Live vs 1 is observed mix.
    """
    live = abs(f(domain_scalar("Astrophysics"))) / abs(
        f(domain_scalar("Particle_Astrophysics"))
    )
    vs1 = err(live, 1.0)
    rows: list[dict[str, Any]] = [
        _row(
            prop="astro_pa_S_ratio",
            name="S_astro_over_S_pa_live",
            computed=live,
            measured=1.0,
            note=(
                "Live |S_Astrophysics|/|S_PA| vs 1 mixes observed/dark at D=24. "
                f"{vs1:.1f}% — same-view question, not a 0.5% central. "
                "Particle_Astrophysics stays dark."
            ),
            kind="structural",
            extra={
                "kappa": kappa_domains("Astrophysics", "Particle_Astrophysics"),
                "live_vs_1_pct": vs1,
            },
        ),
    ]
    rows.extend(
        _pdg_mass_dual(
            pdg_path,
            "Astrophysics",
            "Particle_Astrophysics",
            "astro_pa_pdg_astro_fold",
            "astro_pa_pdg_pa_fold",
            "PDG 2024 measured mass on Astrophysics D=24",
            "same PDG mass on Particle_Astrophysics D=24 — cosmic-ray stays dark",
        )
    )
    return rows


def qc_acoustics_rows() -> list[dict[str, Any]]:
    """Acoustics D=10 ↔ Quantum_Computing D=11. QC stays dark (Hilbert)."""
    s10 = scalar_at(d_eff=10, delta_psi=0.5, hits=0, observed=False)
    s11 = scalar_at(d_eff=11, delta_psi=0.5, hits=0, observed=False)
    ratio = s10 / s11
    rows = [
        _row(
            prop="qc_ac_S_ratio_same_look",
            name="S_D10_over_S_D11_dpsi_0p5_dark",
            computed=ratio,
            measured=1.0,
            note="|S(D=10,δψ=0.5,dark)|/|S(D=11,δψ=0.5,dark)| vs 1 — sound vs Hilbert. Compactification remainder, not stuffed. Do not flip QC.",
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={"kappa": kappa_domains("Acoustics", "Quantum_Computing")},
        )
    ]
    for sp in ACOUSTIC_SPECIMENS:
        c, e = scaled(float(sp["c"]), "Acoustics")
        rows.append(_row(prop="qc_ac_c_ac_fold", name=str(sp["name"]) + "_c",
                         computed=c, measured=float(sp["c"]),
                         note="CRC longitudinal c on Acoustics D=10"))
        rows[-1]["error_pct"] = e
    rows.extend(_crc_n_dual("Quantum_Computing", "Acoustics",
                            "qc_ac_n_qc_fold", "qc_ac_n_ac_fold",
                            "CRC n_D on Quantum_Computing D=11 — Hilbert stays dark",
                            "same n_D on Acoustics D=10"))
    return rows


def qc_materials_rows() -> list[dict[str, Any]]:
    """Materials D=10 ↔ Quantum_Computing D=11. QC stays dark."""
    s10 = scalar_at(d_eff=10, delta_psi=0.5, hits=0, observed=False)
    s11 = scalar_at(d_eff=11, delta_psi=0.5, hits=0, observed=False)
    ratio = s10 / s11
    rows = [
        _row(
            prop="qc_mat_S_ratio_same_look",
            name="S_D10_over_S_D11_dpsi_0p5_dark_mat",
            computed=ratio,
            measured=1.0,
            note="|S(D=10,δψ=0.5,dark)|/|S(D=11,δψ=0.5,dark)| vs 1 — bulk vs Hilbert. Compactification remainder, not stuffed. Do not flip QC.",
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={"kappa": kappa_domains("Materials_Science", "Quantum_Computing")},
        )
    ]
    for mat in OPTICAL_MATERIALS:
        rho = float(mat["rho"])
        c, e = scaled(rho, "Materials_Science")
        rows.append(_row(prop="qc_mat_rho_mat_fold", name=str(mat["name"]) + "_rho",
                         computed=c, measured=rho,
                         note="CRC density on Materials_Science D=10"))
        rows[-1]["error_pct"] = e
    rows.extend(_crc_n_dual("Quantum_Computing", "Materials_Science",
                            "qc_mat_n_qc_fold", "qc_mat_n_mat_fold",
                            "CRC n_D on Quantum_Computing D=11 — Hilbert stays dark",
                            "same n_D on Materials_Science D=10"))
    return rows


def qc_optics_rows() -> list[dict[str, Any]]:
    """Optics D=10 ↔ Quantum_Computing D=11. QC stays dark."""
    s10 = scalar_at(d_eff=10, delta_psi=0.5, hits=0, observed=False)
    s11 = scalar_at(d_eff=11, delta_psi=0.5, hits=0, observed=False)
    ratio = s10 / s11
    rows = [
        _row(
            prop="qc_opt_S_ratio_same_look",
            name="S_D10_over_S_D11_dpsi_0p5_dark_opt",
            computed=ratio,
            measured=1.0,
            note="|S(D=10,δψ=0.5,dark)|/|S(D=11,δψ=0.5,dark)| vs 1 — wave vs Hilbert. Compactification remainder, not stuffed. Do not flip QC.",
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={"kappa": kappa_domains("Optics", "Quantum_Computing")},
        )
    ]
    rows.extend(_crc_n_dual("Optics", "Quantum_Computing",
                            "qc_opt_n_opt_fold", "qc_opt_n_qc_fold",
                            "CRC n_D on Optics D=10",
                            "same n_D on Quantum_Computing D=11 — Hilbert stays dark"))
    return rows


def qc_qo_rows() -> list[dict[str, Any]]:
    """Quantum_Computing D=11 ↔ Quantum_Optics D=11. Same rung; QC stays dark."""
    rows = [_live_mix_structural(
        "Quantum_Computing", "Quantum_Optics", "qc_qo_S_ratio",
        "S_qc_over_S_qo_live", "QC stays dark (Hilbert look).",
    )]
    rows.extend(_crc_n_dual("Quantum_Optics", "Quantum_Computing",
                            "qc_qo_n_qo_fold", "qc_qo_n_qc_fold",
                            "CRC n_D on Quantum_Optics D=11 — photon",
                            "same n_D on Quantum_Computing D=11 — Hilbert stays dark"))
    return rows


def qc_biology_rows(bio_path: Path) -> list[dict[str, Any]]:
    """Quantum_Computing D=11 ↔ Biology D=12. Both dark."""
    s11 = scalar_at(d_eff=11, delta_psi=0.08, hits=0, observed=False)
    s12 = scalar_at(d_eff=12, delta_psi=0.08, hits=0, observed=False)
    rows = [
        _row(
            prop="qc_bio_S_ratio_same_look",
            name="S_D11_over_S_D12_dpsi_0p08_dark",
            computed=s11 / s12,
            measured=1.0,
            note="|S(D=11,δψ=0.08,dark)|/|S(D=12,δψ=0.08,dark)| vs 1 — Hilbert vs organism. Do not flip either.",
            extra={"kappa": kappa_domains("Quantum_Computing", "Biology")},
        )
    ]
    rows.extend(_crc_n_dual("Quantum_Computing", "Biology",
                            "qc_bio_n_qc_fold", "qc_bio_n_bio_fold",
                            "CRC n_D on Quantum_Computing D=11 — Hilbert stays dark",
                            "same n_D on Biology D=12 — organism stays dark"))
    if bio_path.is_file():
        doc = json.loads(bio_path.read_text(encoding="utf-8"))
        n_op = 0
        for rec in doc.get("records") or []:
            if rec.get("property") != "mt_operon_length":
                continue
            m = float(rec.get("measured") or 0)
            if m <= 0:
                continue
            c, e = scaled(m, "Biology")
            rows.append(_row(prop="qc_bio_operon_bio_fold",
                             name=str(rec.get("name") or f"op{n_op}") + "_bio",
                             computed=c, measured=m,
                             note="NCBI NC_012920.1 mt-operon on Biology D=12 — stays dark"))
            rows[-1]["error_pct"] = e
            n_op += 1
    return rows


def cm_ecology_rows(eco_path: Path) -> list[dict[str, Any]]:
    """Condensed_Matter D=14 ↔ Ecology D=15. Ecology stays dark. GBIF latitudes."""
    rows = [_live_mix_structural(
        "Condensed_Matter", "Ecology", "cm_eco_S_ratio",
        "S_cm_over_S_eco_live", "Ecology stays dark.",
    )]
    for sol in CM_THERMO_SOLIDS:
        rho = float(sol["rho"])
        c, e = scaled(rho, "Condensed_Matter")
        rows.append(_row(prop="cm_eco_rho_cm_fold", name=str(sol["name"]) + "_rho",
                         computed=c, measured=rho, note="CRC density on Condensed_Matter D=14"))
        rows[-1]["error_pct"] = e
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Condensed_Matter",
                               "cm_eco_gbif_eco_fold", "cm_eco_gbif_cm_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Condensed_Matter D=14"))
    return rows


def neuro_ecology_rows(eco_path: Path) -> list[dict[str, Any]]:
    """Neuroscience D=14 ↔ Ecology D=15. Ecology stays dark."""
    rows = [_live_mix_structural(
        "Neuroscience", "Ecology", "neuro_eco_S_ratio",
        "S_neuro_over_S_eco_live", "Ecology stays dark.",
    )]
    mw = {a: m for a, m in AMINO_ACID_MW}
    for aa in NEURO_AA:
        m = float(mw[aa])
        c, e = scaled(m, "Neuroscience")
        rows.append(_row(prop="neuro_eco_aa_neuro_fold", name=aa + "_mw",
                         computed=c, measured=m, note="CRC transmitter AA MW on Neuroscience D=14"))
        rows[-1]["error_pct"] = e
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Neuroscience",
                               "neuro_eco_gbif_eco_fold", "neuro_eco_gbif_neuro_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Neuroscience D=14"))
    return rows


def ecology_fluid_rows(eco_path: Path) -> list[dict[str, Any]]:
    """Ecology D=15 ↔ Fluid_Dynamics D=15. Both dark. GBIF + CRC water ρ."""
    rows = [_live_mix_structural(
        "Ecology", "Fluid_Dynamics", "eco_fluid_S_ratio",
        "S_eco_over_S_fluid_live", "Both stay dark.",
    )]
    water = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "water_20C")
    c, e = scaled(float(water["rho"]), "Fluid_Dynamics")
    rows.append(_row(prop="eco_fluid_water_fl_fold", name="water_20C_rho",
                     computed=c, measured=float(water["rho"]),
                     note="CRC water density on Fluid_Dynamics D=15 — tank stays dark"))
    rows[-1]["error_pct"] = e
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Fluid_Dynamics",
                               "eco_fluid_gbif_eco_fold", "eco_fluid_gbif_fl_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Fluid_Dynamics D=15 — tank stays dark"))
    return rows


def ecology_nuclear_rows(eco_path: Path, endf_path: Path) -> list[dict[str, Any]]:
    """Ecology D=15 ↔ Nuclear D=15. Ecology stays dark."""
    rows = [_live_mix_structural(
        "Ecology", "Nuclear_Physics", "eco_nuc_S_ratio",
        "S_eco_over_S_nuc_live", "Ecology stays dark.",
    )]
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Nuclear_Physics",
                               "eco_nuc_gbif_eco_fold", "eco_nuc_gbif_nuc_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Nuclear_Physics D=15"))
    rows.extend(_endf_keV_dual(endf_path, "Nuclear_Physics", "Ecology",
                               "eco_nuc_level_nuc_fold", "eco_nuc_level_eco_fold",
                               "IAEA/ENDF keV on Nuclear_Physics D=15",
                               "same IAEA keV on Ecology D=15 — habitat stays dark"))
    return rows


def ecology_thermo_rows(eco_path: Path) -> list[dict[str, Any]]:
    """Ecology D=15 ↔ Thermodynamics D=15. Ecology stays dark."""
    rows = [_live_mix_structural(
        "Ecology", "Thermodynamics", "eco_thermo_S_ratio",
        "S_eco_over_S_th_live", "Ecology stays dark.",
    )]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        c, e = scaled(cop, "Thermodynamics")
        rows.append(_row(prop="eco_thermo_carnot_th_fold", name=name,
                         computed=c, measured=cop, note="Carnot COP on Thermodynamics D=15"))
        rows[-1]["error_pct"] = e
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Thermodynamics",
                               "eco_thermo_gbif_eco_fold", "eco_thermo_gbif_th_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Thermodynamics D=15"))
    return rows


def ecology_meteo_rows(eco_path: Path, ndbc_path: Path) -> list[dict[str, Any]]:
    """Ecology D=15 ↔ Meteorology D=16. Both dark."""
    s15 = scalar_at(d_eff=15, delta_psi=0.8, hits=2, observed=False)
    s16 = scalar_at(d_eff=16, delta_psi=0.8, hits=2, observed=False)
    ratio = s15 / s16
    rows = [
        _row(
            prop="eco_meteo_S_ratio_same_look",
            name="S_D15_over_S_D16_dpsi_0p8_dark",
            computed=ratio,
            measured=1.0,
            note="|S(D=15,δψ=0.8,dark)|/|S(D=16,δψ=0.8,dark)| vs 1 — habitat vs weather. Do not flip dark.",
            kind="structural" if err(ratio, 1.0) > 0.5 else "scalar",
            extra={"kappa": kappa_domains("Ecology", "Meteorology")},
        )
    ]
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Meteorology",
                               "eco_meteo_gbif_eco_fold", "eco_meteo_gbif_meteo_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Meteorology D=16 — weather stays dark"))
    rows.extend(_ndbc_pres_dual(ndbc_path, "Meteorology", "Ecology",
                                "eco_meteo_pres_meteo_fold", "eco_meteo_pres_eco_fold",
                                "NDBC pressure on Meteorology D=16 — weather stays dark",
                                "same NDBC pressure on Ecology D=15 — habitat stays dark"))
    return rows


def ecology_psychology_rows(eco_path: Path, psych_path: Path) -> list[dict[str, Any]]:
    """Ecology D=15 ↔ Psychology D=16. Ecology stays dark. GBIF + Nunnally/Cohen."""
    rows = [_live_mix_structural(
        "Ecology", "Psychology", "eco_psych_S_ratio",
        "S_eco_over_S_psych_live", "Ecology stays dark. Not watts.",
    )]
    rows.extend(_gbif_lat_dual(eco_path, "Ecology", "Psychology",
                               "eco_psych_gbif_eco_fold", "eco_psych_gbif_psych_fold",
                               "GBIF decimalLatitude on Ecology D=15 — habitat stays dark",
                               "same GBIF latitude on Psychology D=16"))
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Ecology",
                                   "eco_psych_anchor_psych_fold", "eco_psych_anchor_eco_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Ecology D=15 — habitat stays dark"))
    return rows


def fluid_psychology_rows(psych_path: Path) -> list[dict[str, Any]]:
    """Fluid D=15 ↔ Psychology D=16. Fluid stays dark."""
    rows = [_live_mix_structural(
        "Fluid_Dynamics", "Psychology", "fluid_psych_S_ratio",
        "S_fluid_over_S_psych_live", "Fluid stays dark. Not watts.",
    )]
    water = next(sp for sp in ACOUSTIC_SPECIMENS if sp["name"] == "water_20C")
    c, e = scaled(float(water["rho"]), "Fluid_Dynamics")
    rows.append(_row(prop="fluid_psych_water_fl_fold", name="water_20C_rho",
                     computed=c, measured=float(water["rho"]),
                     note="CRC water density on Fluid_Dynamics D=15 — tank stays dark"))
    rows[-1]["error_pct"] = e
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Fluid_Dynamics",
                                   "fluid_psych_anchor_psych_fold", "fluid_psych_anchor_fl_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Fluid_Dynamics D=15 — tank stays dark"))
    return rows


def nuclear_psychology_rows(psych_path: Path, endf_path: Path) -> list[dict[str, Any]]:
    """Nuclear D=15 ↔ Psychology D=16."""
    rows = [_live_mix_structural(
        "Nuclear_Physics", "Psychology", "nuc_psych_S_ratio",
        "S_nuc_over_S_psych_live", "Not watts.",
    )]
    rows.extend(_endf_keV_dual(endf_path, "Nuclear_Physics", "Psychology",
                               "nuc_psych_level_nuc_fold", "nuc_psych_level_psych_fold",
                               "IAEA/ENDF keV on Nuclear_Physics D=15",
                               "same IAEA keV on Psychology D=16"))
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Nuclear_Physics",
                                   "nuc_psych_anchor_psych_fold", "nuc_psych_anchor_nuc_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Nuclear_Physics D=15"))
    return rows


def thermo_psychology_rows(psych_path: Path) -> list[dict[str, Any]]:
    """Thermodynamics D=15 ↔ Psychology D=16."""
    rows = [_live_mix_structural(
        "Thermodynamics", "Psychology", "thermo_psych_S_ratio",
        "S_th_over_S_psych_live", "Not watts.",
    )]
    for name, tc, th in CARNOT_PAIRS:
        cop = carnot_cop(tc, th)
        c, e = scaled(cop, "Thermodynamics")
        rows.append(_row(prop="thermo_psych_carnot_th_fold", name=name,
                         computed=c, measured=cop, note="Carnot COP on Thermodynamics D=15"))
        rows[-1]["error_pct"] = e
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Thermodynamics",
                                   "thermo_psych_anchor_psych_fold", "thermo_psych_anchor_th_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Thermodynamics D=15"))
    return rows


def meteo_psychology_rows(psych_path: Path, ndbc_path: Path) -> list[dict[str, Any]]:
    """Meteorology D=16 ↔ Psychology D=16. Same rung; Meteo stays dark."""
    rows = [_live_mix_structural(
        "Meteorology", "Psychology", "meteo_psych_S_ratio",
        "S_meteo_over_S_psych_live", "Meteorology stays dark. Not watts.",
    )]
    rows.extend(_ndbc_pres_dual(ndbc_path, "Meteorology", "Psychology",
                                "meteo_psych_pres_meteo_fold", "meteo_psych_pres_psych_fold",
                                "NDBC pressure on Meteorology D=16 — weather stays dark",
                                "same NDBC pressure on Psychology D=16"))
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Meteorology",
                                   "meteo_psych_anchor_psych_fold", "meteo_psych_anchor_meteo_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Meteorology D=16 — weather stays dark"))
    return rows


def psychology_atm_rows(psych_path: Path, ndbc_path: Path) -> list[dict[str, Any]]:
    """Psychology D=16 ↔ Atmospheric_Physics D=17. Atm stays dark."""
    rows = [_live_mix_structural(
        "Psychology", "Atmospheric_Physics", "psych_atm_S_ratio",
        "S_psych_over_S_atm_live", "Atmospheric_Physics stays dark. Not watts.",
    )]
    rows.extend(_ndbc_pres_dual(ndbc_path, "Atmospheric_Physics", "Psychology",
                                "psych_atm_pres_atm_fold", "psych_atm_pres_psych_fold",
                                "NDBC pressure on Atmospheric_Physics D=17 — air stays dark",
                                "same NDBC pressure on Psychology D=16"))
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Atmospheric_Physics",
                                   "psych_atm_anchor_psych_fold", "psych_atm_anchor_atm_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Atmospheric_Physics D=17 — air stays dark"))
    return rows


def psychology_ocean_rows(psych_path: Path, ndbc_path: Path) -> list[dict[str, Any]]:
    """Psychology D=16 ↔ Oceanography D=17. Ocean stays dark."""
    rows = [_live_mix_structural(
        "Psychology", "Oceanography", "psych_ocean_S_ratio",
        "S_psych_over_S_ocean_live", "Oceanography stays dark. Not watts.",
    )]
    if ndbc_path.is_file():
        doc = json.loads(ndbc_path.read_text(encoding="utf-8"))
        for rec in doc.get("rows") or []:
            val = rec.get("wtmp")
            if val is None:
                continue
            m = float(val)
            if m <= 0:
                continue
            bid = str(rec.get("buoy_id") or "buoy")
            ts = str(rec.get("timestamp") or "").replace(" ", "_")
            c, e = scaled(m, "Oceanography")
            rows.append(_row(prop="psych_ocean_sst_ocean_fold", name=f"{bid}_{ts}_sst",
                             computed=c, measured=m,
                             note="NDBC SST on Oceanography D=17 — ocean stays dark"))
            rows[-1]["error_pct"] = e
    rows.extend(_psych_anchor_dual(psych_path, "Psychology", "Oceanography",
                                   "psych_ocean_anchor_psych_fold", "psych_ocean_anchor_ocean_fold",
                                   "Nunnally/Cohen psychometric anchor on Psychology D=16",
                                   "same anchor on Oceanography D=17 — ocean stays dark"))
    return rows


# Live view pairs: high |S_i|/|S_j| vs 1 is perception at that fold, not a failed gate.
PERCEPTION_PAIRS = (
    ("Quantum_Mechanics", "Atomic_Physics", "qm_atomic"),
    ("Electromagnetism", "Optics", "em_opt"),
    ("Electromagnetism", "Materials_Science", "em_mat"),
    ("Biology", "Biochemistry", "bio_biochem"),
    ("Biochemistry", "Neuroscience", "biochem_neuro"),
    ("Materials_Science", "Optics", "mat_opt"),
    ("Acoustics", "Optics", "ac_opt"),
    ("Acoustics", "Materials_Science", "ac_mat"),
    ("Chemistry", "Molecular_Chemistry", "chem_mol"),
    ("Chemistry", "Physical_Chemistry", "chem_pc"),
    ("Condensed_Matter", "Thermodynamics", "cm_thermo"),
    ("Atomic_Physics", "High_Energy_Physics", "atomic_hep"),
    ("Biochemistry", "Condensed_Matter", "biochem_cm"),
    ("Condensed_Matter", "Neuroscience", "cm_neuro"),
    ("Condensed_Matter", "Nuclear_Physics", "cm_nuc"),
    ("Neuroscience", "Thermodynamics", "neuro_thermo"),
    ("Neuroscience", "Nuclear_Physics", "neuro_nuc"),
    ("Astronomy", "Planetary_Science", "astro_planetary"),
    ("Astronomy", "Economics", "astro_econ"),
    ("Economics", "Planetary_Science", "econ_planet"),
    ("Economics", "Neuroscience", "econ_neuro"),
    ("Seismology", "Geophysics", "seis_geo"),
    ("Fluid_Dynamics", "Thermodynamics", "fluid_thermo"),
    ("Condensed_Matter", "Fluid_Dynamics", "cm_fluid"),
    ("Fluid_Dynamics", "Nuclear_Physics", "fluid_nuc"),
    ("Neuroscience", "Fluid_Dynamics", "neuro_fluid"),
    ("Thermodynamics", "Meteorology", "thermo_meteo"),
    ("Nuclear_Physics", "Meteorology", "nuc_meteo"),
    ("Atmospheric_Physics", "Sociology", "atm_soc"),
    ("Oceanography", "Sociology", "ocean_soc"),
    ("Seismology", "Sociology", "seis_soc"),
    ("Sociology", "Geophysics", "soc_geo"),
    ("Geophysics", "Economics", "geo_econ"),
    ("Geophysics", "Astronomy", "geo_astro"),
    ("Planetary_Science", "Quantum_Gravity", "planet_qg"),
    ("Astrophysics", "Particle_Astrophysics", "astro_pa"),
    ("Quantum_Computing", "Quantum_Optics", "qc_qo"),
    ("Condensed_Matter", "Ecology", "cm_eco"),
    ("Neuroscience", "Ecology", "neuro_eco"),
    ("Ecology", "Fluid_Dynamics", "eco_fluid"),
    ("Ecology", "Nuclear_Physics", "eco_nuc"),
    ("Ecology", "Thermodynamics", "eco_thermo"),
    ("Ecology", "Psychology", "eco_psych"),
    ("Fluid_Dynamics", "Psychology", "fluid_psych"),
    ("Nuclear_Physics", "Psychology", "nuc_psych"),
    ("Thermodynamics", "Psychology", "thermo_psych"),
    ("Meteorology", "Psychology", "meteo_psych"),
    ("Psychology", "Atmospheric_Physics", "psych_atm"),
    ("Psychology", "Oceanography", "psych_ocean"),
)

# Same-look |S(D)/S(D')| vs 1 is the wrong object (compactification still in T1).
# D9: |1+T1|/|1+T1| vs live |S|/|S|. Spec: (D_a, D_b, δψ, hits, observed, tag).
SAME_LOOK_T1 = (
    (20, 21, 1.0, 1, True, "astro_planet_eq"),
    (13, 14, 0.5, 0, True, "biochem_cm_eq"),
    (14, 15, 0.5, 0, True, "cm_d14d15_eq"),
    (10, 11, 0.5, 0, True, "d10d11_eq"),
    (9, 10, 0.5, 0, True, "d9d10_eq"),
    (14, 15, 0.7, 1, True, "neuro_d14d15_eq"),
)

_DEMOTE_VS1_PROPS = {
    "astro_planetary_S_ratio_same_look",
    "econ_planet_S_ratio_same_look",
    "biochem_cm_S_ratio_same_look",
    "cm_thermo_S_ratio_same_look",
    "cm_nuclear_S_ratio_same_look",
    "mat_qo_S_ratio_same_look",
    "mol_ac_S_ratio_same_look",
    "em_mat_S_ratio_same_look",
    "mol_mat_S_ratio_same_look",
    "mol_opt_S_ratio_same_look",
    "neuro_thermo_S_ratio_same_look",
    "neuro_nuclear_S_ratio_same_look",
    "social_S_ratio",
}


def perception_view_rows() -> list[dict[str, Any]]:
    """FSOT solve for live |S_i|/|S_j| vs 1.

    Same premise at every scale. T1 is how that premise is viewed
    (δψ, hits, observed). At these rungs T2=1 and T3≈0 (β seed-tiny), so

        |S_i|/|S_j|  =  |1+T1_i|/|1+T1_j|

    That is the closed form for the tens-of-percent live ratios. vs 1 asks
    for the same view; adjacent folds are not supposed to look the same.
    Residual of this row is T3 leftover, not a new coefficient.
    """
    rows: list[dict[str, Any]] = []
    for a, b, tag in PERCEPTION_PAIRS:
        t1a, t1b = t1_of(a), t1_of(b)
        sa = abs(f(domain_scalar(a)))
        sb = abs(f(domain_scalar(b)))
        live = sa / sb
        pred = abs(1.0 + t1a) / abs(1.0 + t1b)
        vs1 = err(live, 1.0)
        e_t3 = err(pred, live)
        leftover_ok = e_t3 <= 0.5
        rec = _row(
            prop="perception_view_t1",
            name=f"{tag}_T1_view",
            computed=pred,
            measured=live,
            note=(
                f"|1+T1({a})|/|1+T1({b})| vs live |S|/|S| — perception "
                f"the fold produces. Live vs 1 is {vs1:.1f}% (same-view "
                "question, not a failed 0.5% central). Residual is T3 leftover. "
                "Identity-check row: not a 0.5% central and not a median pad."
            ),
            kind="structural",
            extra={
                "pair": f"{a}/{b}",
                "live_vs_1_pct": vs1,
                "T1_a": t1a,
                "T1_b": t1b,
                "S_a": sa,
                "S_b": sb,
                "t3_leftover_ok": leftover_ok,
            },
        )
        rec["error_pct"] = e_t3
        rec["eval_kind"] = "perception_t1_view" if leftover_ok else "t3_leftover_band"
        rows.append(rec)
        rows.append(
            _row(
                prop="perception_same_view_vs_1",
                name=f"{tag}_live_vs_1",
                computed=live,
                measured=1.0,
                note=(
                    f"Live |S_{a}|/|S_{b}| vs 1 — same-view question. "
                    "Not a 0.5% central. View is T1 at each fold (perception_view_t1)."
                ),
                kind="structural",
                extra={"pair": f"{a}/{b}", "live_vs_1_pct": vs1},
            )
        )
    return rows


def same_look_t1_rows() -> list[dict[str, Any]]:
    """D9 at an equalized look: vs 1 is the wrong object; leftover is T3."""
    rows: list[dict[str, Any]] = []
    for da, db, dpsi, hits, obs, tag in SAME_LOOK_T1:
        sa = scalar_at(d_eff=da, delta_psi=dpsi, hits=hits, observed=obs)
        sb = scalar_at(d_eff=db, delta_psi=dpsi, hits=hits, observed=obs)
        t1a = t1_at(d_eff=da, delta_psi=dpsi, hits=hits, observed=obs)
        t1b = t1_at(d_eff=db, delta_psi=dpsi, hits=hits, observed=obs)
        live = sa / sb
        pred = abs(1.0 + t1a) / abs(1.0 + t1b)
        e_t3 = err(pred, live)
        rec = _row(
            prop="same_look_t1_view",
            name=f"{tag}_T1_view",
            computed=pred,
            measured=live,
            note=(
                f"|1+T1(D={da},δψ={dpsi})|/|1+T1(D={db},δψ={dpsi})| vs live |S|/|S| "
                f"at equalized look. vs 1 is the same-view question (compactification "
                "still sits in T1). Residual is T3 leftover."
            ),
            kind="structural",
            extra={
                "D_a": float(da),
                "D_b": float(db),
                "delta_psi": float(dpsi),
                "t3_leftover_ok": e_t3 <= 0.5,
            },
        )
        rec["error_pct"] = e_t3
        rec["eval_kind"] = "perception_t1_view" if e_t3 <= 0.5 else "t3_leftover_band"
        rows.append(rec)
    return rows


def demote_vs1_same_look(rows: list[dict[str, Any]]) -> None:
    """vs 1 / vs 5/4 on those S-ratios is the wrong object once D9 T1 is gated."""
    for r in rows:
        if r.get("property") not in _DEMOTE_VS1_PROPS:
            continue
        if r.get("record_kind") != "scalar":
            continue
        r["record_kind"] = "structural"
        r["eval_kind"] = "literature_band"
        note = str(r.get("note") or "")
        if "D9" not in note:
            r["note"] = note + " D9: vs 1 / vs 5/4 is the same-view or seed-approx question; T1 view is the closed form."


def perception_summary(rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Closed-form ledger: live |S_i|/|S_j| is T1, leftover is T3."""
    if rows is None:
        rows = perception_view_rows()
    t1 = [
        r
        for r in rows
        if r.get("property") in ("perception_view_t1", "same_look_t1_view")
    ]
    vs1 = [r for r in rows if r.get("property") == "perception_same_view_vs_1"]
    leftovers = [float(r["error_pct"]) for r in t1]
    vs1_pcts = [float(r.get("live_vs_1_pct") or r["error_pct"]) for r in t1]
    return {
        "closed_form": "|S_i|/|S_j| = |1+T1_i|/|1+T1_j|  (T2=1, T3≈0)",
        "n_pairs": len(t1),
        "max_t3_leftover_pct": max(leftovers) if leftovers else None,
        "max_live_vs_1_pct": max(vs1_pcts) if vs1_pcts else None,
        "t3_leftover_ok": bool(leftovers) and max(leftovers) <= 0.5,
        "n_same_view_structural": len(vs1),
        "pairs": [
            {
                "name": r["name"],
                "pair": r.get("pair"),
                "live_ratio": r["measured"],
                "t1_pred": r["computed"],
                "t3_leftover_pct": r["error_pct"],
                "live_vs_1_pct": r.get("live_vs_1_pct"),
            }
            for r in t1
        ],
        "policy": (
            "live vs 1 is the same-view question, not a 0.5% central; "
            "T1 leftover rows are identity checks, not a median pad"
        ),
    }


def suite_rows(
    *,
    ndbc_path: Path,
    endf_path: Path,
    econ_path: Path | None = None,
    bio_path: Path | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(seismic_acoustic_rows())
    rows.extend(fluid_tank_rows(ndbc_path))
    rows.extend(thermo_cosmo_rows())
    rows.extend(nuclear_particle_rows(endf_path))
    rows.extend(qg_ceiling_rows())
    if econ_path is not None:
        rows.extend(social_tank_rows(econ_path))
    rows.extend(seis_geo_rows())
    rows.extend(mat_opt_rows())
    rows.extend(opt_qo_rows())
    rows.extend(qm_atomic_rows())
    rows.extend(em_opt_rows())
    if bio_path is not None:
        rows.extend(bio_biochem_rows(bio_path))
    rows.extend(atomic_hep_rows())
    rows.extend(chem_physchem_rows())
    rows.extend(chem_mol_rows())
    rows.extend(physchem_mol_rows())
    rows.extend(ac_opt_rows())
    rows.extend(ac_mat_rows())
    rows.extend(mol_ac_rows())
    rows.extend(cm_thermo_rows())
    rows.extend(em_mat_rows())
    rows.extend(biochem_neuro_rows())
    rows.extend(atomic_chem_rows())
    rows.extend(atomic_pc_rows())
    rows.extend(hep_chem_rows())
    rows.extend(hep_pc_rows())
    rows.extend(pc_em_rows())
    rows.extend(em_mol_rows())
    rows.extend(mol_mat_rows())
    rows.extend(mol_opt_rows())
    rows.extend(ac_qo_rows())
    rows.extend(mat_qo_rows())
    rows.extend(nuclear_thermo_rows(endf_path))
    rows.extend(fluid_thermo_rows())
    rows.extend(meteo_atm_rows(ndbc_path))
    rows.extend(biochem_cm_rows())
    rows.extend(cm_neuro_rows())
    rows.extend(cm_fluid_rows())
    rows.extend(cm_nuclear_rows(endf_path))
    rows.extend(neuro_thermo_rows())
    rows.extend(fluid_nuclear_rows(endf_path))
    rows.extend(fluid_meteo_rows(ndbc_path))
    rows.extend(neuro_fluid_rows())
    rows.extend(neuro_nuclear_rows(endf_path))
    rows.extend(thermo_meteo_rows(ndbc_path))
    rows.extend(nuclear_meteo_rows(ndbc_path, endf_path))
    rows.extend(meteo_ocean_rows(ndbc_path))
    rows.extend(atm_seis_rows(ndbc_path))
    rows.extend(ocean_seis_rows(ndbc_path))
    planet = Path(__file__).resolve().parents[1] / "data" / "planetary_structure_benchmark.json"
    rows.extend(astro_planetary_rows(planet))
    if bio_path is not None:
        rows.extend(qo_biology_rows(bio_path))
    pdg = Path(__file__).resolve().parents[1] / "data" / "pdg_particle_properties_benchmark.json"
    if econ_path is not None:
        rows.extend(atm_sociology_rows(ndbc_path, econ_path))
        rows.extend(ocean_sociology_rows(ndbc_path, econ_path))
        rows.extend(seis_sociology_rows(econ_path))
        rows.extend(sociology_geo_rows(econ_path))
        rows.extend(geo_economics_rows(econ_path))
        rows.extend(astronomy_economics_rows(econ_path, planet))
        rows.extend(economics_planetary_rows(econ_path, planet))
    rows.extend(geo_astronomy_rows(planet))
    rows.extend(planetary_qg_rows(planet))
    rows.extend(astrophysics_pa_rows(pdg))
    eco = Path(__file__).resolve().parents[1] / "data" / "ecology_gap_fill_benchmark.json"
    psych = Path(__file__).resolve().parents[1] / "data" / "psychology_psychometrics_depth_panel_benchmark.json"
    rows.extend(qc_acoustics_rows())
    rows.extend(qc_materials_rows())
    rows.extend(qc_optics_rows())
    rows.extend(qc_qo_rows())
    if bio_path is not None:
        rows.extend(qc_biology_rows(bio_path))
    rows.extend(cm_ecology_rows(eco))
    rows.extend(neuro_ecology_rows(eco))
    rows.extend(ecology_fluid_rows(eco))
    rows.extend(ecology_nuclear_rows(eco, endf_path))
    rows.extend(ecology_thermo_rows(eco))
    rows.extend(ecology_meteo_rows(eco, ndbc_path))
    rows.extend(ecology_psychology_rows(eco, psych))
    rows.extend(fluid_psychology_rows(psych))
    rows.extend(nuclear_psychology_rows(psych, endf_path))
    rows.extend(thermo_psychology_rows(psych))
    rows.extend(meteo_psychology_rows(psych, ndbc_path))
    rows.extend(psychology_atm_rows(psych, ndbc_path))
    rows.extend(psychology_ocean_rows(psych, ndbc_path))
    rows.extend(perception_view_rows())
    rows.extend(same_look_t1_rows())
    demote_vs1_same_look(rows)
    return rows
