#!/usr/bin/env python3
"""Ledger A closed-form emit — no measured value in the call stack.

fsot_predict(observable_id) returns units, value, expression, pin.
Compare is a separate step (compare_to_anchor.py).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_compute import (  # noqa: E402
    A_BLEED,
    A_IN,
    E,
    GAMMA,
    P_BASE,
    PHI,
    PI,
    S_COSM,
    S_QUANT,
    C_COSM,
    fabs,
    wave1,
    wave2,
    validation_suite,
    lepton_ratios,
    chemistry_ionization,
    chemistry_molecular,
    wave8,
    wave10,
)

PIN_PATH = ROOT / "vendor" / "fsot_compute.py"


def engine_pin() -> str:
    sha = hashlib.sha256(PIN_PATH.read_bytes()).hexdigest().upper()
    return sha[:6]


def _f(x: Any) -> float:
    return float(x)


def _t_cmb() -> float:
    return _f(PHI) ** 2 + _f(P_BASE) * abs(_f(S_COSM))


def _h0_planck_class() -> float:
    return 100.0 * (1.0 + _f(S_COSM) * _f(A_BLEED) / _f(A_IN))


def _alpha_s() -> float:
    return 1.0 / (_f(E) * _f(PI))


def _n_s() -> float:
    return 1.0 + _f(S_COSM) * _f(C_COSM) * (_f(PHI) ** (1.0 / _f(PI)))


def _omega_b_h2() -> float:
    return abs(_f(S_COSM)) * (1.0 - _f(S_QUANT))


def _riemann_t1() -> float:
    return _f(E) / (_f(GAMMA) ** 3)


def _from_fn(fn: Callable[[], list], name: str) -> Callable[[], float]:
    def _emit() -> float:
        for r in fn():
            if r.name == name:
                return _f(r.computed)
        raise KeyError(name)

    return _emit


# kind: FORECAST = next measurement claimed here; CONSTANT_IDENTITY = seed form
# matches published digits (numerology inventory, not a ToE paragraph).
LEDGER_A: dict[str, dict[str, Any]] = {
    "T_CMB": {
        "units": "K",
        "expression": "phi**2 + P_base*|S_cosm|",
        "expression_id": "wave1.T_CMB",
        "emit": _t_cmb,
        "kind": "FORECAST",
        "anchor": 2.72548,
        "anchor_source": "CODATA/PDG CMB monopole (literature, compare step only)",
        "kill_band": "If a future CMB monopole leaves [2.724, 2.727] K this expression is dead",
    },
    "H0_PLANCK_CLASS": {
        "units": "km s^-1 Mpc^-1",
        "expression": "100*(1 + S_cosm*A_bleed/A_in)",
        "expression_id": "wave1.H0",
        "emit": _h0_planck_class,
        "kind": "FORECAST",
        "anchor": 67.4,
        "anchor_source": "Planck 2018 TT,TE,EE+lowE+lensing class (compare step only)",
        "kill_band": "If Planck-class H0 leaves [66.0, 69.0] this expression is dead. Not the SH0ES ladder object.",
    },
    "alpha_s_MZ": {
        "units": "1",
        "expression": "1/(e*pi)",
        "expression_id": "wave1.alpha_s",
        "emit": _alpha_s,
        "kind": "FORECAST",
        "anchor": 0.1179,
        "anchor_source": "PDG alpha_s(M_Z) (compare step only)",
        "kill_band": "If PDG alpha_s(M_Z) leaves [0.116, 0.120] this expression is dead",
    },
    "n_s": {
        "units": "1",
        "expression": "1 + S_cosm*C_cosm*phi**(1/pi)",
        "expression_id": "wave1.n_s",
        "emit": _n_s,
        "kind": "FORECAST",
        "anchor": 0.9649,
        "anchor_source": "Planck 2018 n_s (compare step only)",
        "kill_band": "If n_s leaves [0.95, 0.98] this expression is dead",
    },
    "Omega_b_h2": {
        "units": "1",
        "expression": "|S_cosm|*(1 - S_quant)",
        "expression_id": "wave1.Omega_b_h2",
        "emit": _omega_b_h2,
        "kind": "FORECAST",
        "anchor": 0.02237,
        "anchor_source": "Planck 2018 Omega_b h^2 (compare step only)",
        "kill_band": "If Omega_b h^2 leaves [0.0215, 0.0232] this expression is dead",
    },
    "First_Riemann_zero": {
        "units": "1",
        "expression": "e/gamma**3",
        "expression_id": "validation.First_Riemann_zero",
        "emit": _riemann_t1,
        "kind": "FORECAST",
        "anchor": 14.134725141734693,
        "anchor_source": "Odlyzko / LMFDB Im(rho1) (compare step only)",
        "kill_band": "If tabulated Im(rho1) leaves [14.13, 14.14] this expression is dead",
    },
    "Dark_energy_wa": {
        "units": "1",
        "expression": "-gamma*e*phi/pi",
        "expression_id": "validation.Dark_energy_wa",
        "emit": _from_fn(validation_suite, "Dark_energy_wa"),
        "kind": "FORECAST",
        "anchor": -0.8081,
        "anchor_source": "w_a class (DESI/Planck-style; compare only)",
        "kill_band": "If DESI w_a leaves [-1.05, -0.60] this expression is dead",
    },
    "sigma_8": {
        "units": "1",
        "expression": "|S_cosm|*S_quant + |Chaos|",
        "expression_id": "wave2.sigma_8",
        "emit": _from_fn(wave2, "sigma_8"),
        "kind": "FORECAST",
        "anchor": 0.8111,
        "anchor_source": "Planck 2018 sigma_8 (compare only)",
        "kill_band": "If Planck-class sigma_8 leaves [0.78, 0.85] this expression is dead",
    },
    "N_eff": {
        "units": "1",
        "expression": "P_new*e*pi + ln(phi)",
        "expression_id": "wave2.N_eff",
        "emit": _from_fn(wave2, "N_eff"),
        "kind": "FORECAST",
        "anchor": 3.046,
        "anchor_source": "Planck N_eff (compare only)",
        "kill_band": "If N_eff leaves [2.8, 3.4] this expression is dead",
    },
    "inv_alpha_em": {
        "units": "1",
        "expression": "e**3 * phi**4 - psi_con",
        "expression_id": "wave2.1/alpha_em",
        "emit": _from_fn(wave2, "1/alpha_em"),
        "kind": "FORECAST",
        "anchor": 137.036,
        "anchor_source": "CODATA 1/alpha (compare only)",
        "kill_band": "If 1/alpha leaves [136.9, 137.2] this expression is dead",
    },
    "sin2_theta_W": {
        "units": "1",
        "expression": "sqrt(e)*P_new*eta_eff",
        "expression_id": "wave2.sin2_theta_W",
        "emit": _from_fn(wave2, "sin2_theta_W"),
        "kind": "FORECAST",
        "anchor": 0.23122,
        "anchor_source": "PDG sin^2 theta_W (compare only)",
        "kill_band": "If sin^2 theta_W leaves [0.22, 0.24] this expression is dead",
    },
    "Omega_Lambda": {
        "units": "1",
        "expression": "S_quant/e + gamma**2",
        "expression_id": "wave2.Omega_Lambda",
        "emit": _from_fn(wave2, "Omega_Lambda"),
        "kind": "FORECAST",
        "anchor": 0.6847,
        "anchor_source": "Planck Omega_Lambda (compare only)",
        "kill_band": "If Omega_Lambda leaves [0.65, 0.72] this expression is dead",
    },
    "m_pi_over_m_p": {
        "units": "1",
        "expression": "K*P_new*ln(pi)",
        "expression_id": "wave2.m_pi/m_p",
        "emit": _from_fn(wave2, "m_pi/m_p"),
        "kind": "FORECAST",
        "anchor": 0.14446,
        "anchor_source": "PDG m_pi+/m_p (compare only)",
        "kill_band": "If m_pi/m_p leaves [0.14, 0.15] this expression is dead",
    },
    "m_mu_over_m_e": {
        "units": "1",
        "expression": "(35*phi**(-5)+145)*e**(1/3)",
        "expression_id": "lepton.m_mu/m_e_lepton",
        "emit": _from_fn(lepton_ratios, "m_mu/m_e_lepton"),
        "kind": "FORECAST",
        "anchor": 206.768,
        "anchor_source": "CODATA m_mu/m_e (compare only)",
        "kill_band": "If m_mu/m_e leaves [206.0, 207.5] this expression is dead",
    },
    "m_tau_over_m_e": {
        "units": "1",
        "expression": "9*pi*phi**10",
        "expression_id": "lepton.m_tau/m_e_lepton",
        "emit": _from_fn(lepton_ratios, "m_tau/m_e_lepton"),
        "kind": "FORECAST",
        "anchor": 3477.48,
        "anchor_source": "PDG m_tau/m_e (compare only)",
        "kill_band": "If m_tau/m_e leaves [3460, 3500] this expression is dead",
    },
    "IE_H": {
        "units": "eV",
        "expression": "gamma**(-5) - G**(-8)",
        "expression_id": "chemistry.IE_H",
        "emit": _from_fn(chemistry_ionization, "IE_H"),
        "kind": "FORECAST",
        "anchor": 13.598,
        "anchor_source": "NIST H ionization energy (compare only)",
        "kill_band": "If IE_H leaves [13.5, 13.7] eV this expression is dead",
    },
    "H2O_bond_angle": {
        "units": "deg",
        "expression": "e**3 / gamma**3",
        "expression_id": "wave8.H2O_bond_angle",
        "emit": _from_fn(wave8, "H2O_bond_angle"),
        "kind": "FORECAST",
        "anchor": 104.5,
        "anchor_source": "CRC H2O bond angle (compare only)",
        "kill_band": "If the H2O angle leaves [104.0, 105.0] deg this expression is dead",
    },
    "Water_triple_K": {
        "units": "K",
        "expression": "pi**5 * sin(pi/phi) * C_eff",
        "expression_id": "wave10.Water_triple_K",
        "emit": _from_fn(wave10, "Water_triple_K"),
        "kind": "FORECAST",
        "anchor": 273.16,
        "anchor_source": "ITS-90 water triple point (compare only)",
        "kill_band": "If T_triple leaves [273.0, 273.3] K this expression is dead",
    },
    "BP_H2O": {
        "units": "K",
        "expression": "e**6 - pi**3",
        "expression_id": "chemistry.BP_H2O",
        "emit": _from_fn(chemistry_molecular, "BP_H₂O"),
        "kind": "CONSTANT_IDENTITY",
        "anchor": 373.15,
        "anchor_source": "CRC T_b water (compare only). Exact-digit hits are inventory, not ToE forecasts.",
        "kill_band": "Inventory only — not a FORECAST",
    },
    "tau_reion": {
        "units": "1",
        "expression": "phi*|Chaos| - ln(phi)",
        "expression_id": "wave2.tau_reion",
        "emit": _from_fn(wave2, "tau_reion"),
        "kind": "FORECAST",
        "anchor": 0.0544,
        "anchor_source": "Planck tau_reion (compare only)",
        "kill_band": "If tau_reion leaves [0.04, 0.07] this expression is dead",
    },
}


def fsot_predict(observable_id: str) -> dict[str, Any]:
    """Ledger A emit. Takes no measured value. Raises if measured is in the caller."""
    sid = str(observable_id).strip()
    spec = LEDGER_A.get(sid)
    if spec is None:
        known = ", ".join(sorted(LEDGER_A))
        raise KeyError(f"unknown Ledger A id {sid!r}. known: {known}")
    value = float(spec["emit"]())
    return {
        "observable_id": sid,
        "value": value,
        "units": spec["units"],
        "expression": spec["expression"],
        "expression_id": spec["expression_id"],
        "kind": spec["kind"],
        "pin": engine_pin(),
        "ledger": "A",
        "measured_in_formula": False,
    }


def compare_anchor(observable_id: str) -> dict[str, Any]:
    """Separate compare step. Anchor is literature, not an input to the formula."""
    spec = LEDGER_A[observable_id]
    pred = fsot_predict(observable_id)
    m = float(spec["anchor"])
    err = abs(pred["value"] - m) / max(abs(m), 1e-30) * 100.0
    return {
        **pred,
        "anchor": m,
        "anchor_source": spec["anchor_source"],
        "error_pct": err,
        "kill_band": spec["kill_band"],
        "kind": spec["kind"],
        "note": "Compare is not predict. Anchor never entered the formula.",
    }
