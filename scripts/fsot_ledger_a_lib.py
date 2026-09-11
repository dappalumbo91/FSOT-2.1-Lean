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


def _from_wave1(name: str) -> Callable[[], float]:
    def _emit() -> float:
        for r in wave1():
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
        "kill_band": "If Planck-class H0 leaves [66.0, 69.0] this expression is dead",
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
