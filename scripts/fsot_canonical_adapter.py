#!/usr/bin/env python3
"""
Unified FSOT canonical adapter — single oracle for all experiment corrections.

Loads authoritative fsot_compute.py and exposes:
  - Layer-1/2 constants (ψ_con, η_eff, K, …)
  - domain_scalar() for per-approach canon
  - micro_scalar_v16() legacy projection (documented, not canon)
  - compartment_scalar() for NEURON pre-training bridge
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_PATHS = [
    Path(r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py"),
    ROOT / "_research" / "FSOT-2.0-code" / "fsot-2.0" / "fsot_2_0.py",
    Path(r"C:\Users\damia\Desktop\FSOT Cosmology Lab\fsot_compute.py"),
]

_MOD: Any = None
_MOD_PATH: Path | None = None


def load_fsot_compute():
    global _MOD, _MOD_PATH
    if _MOD is not None:
        return _MOD, _MOD_PATH
    for path in CANONICAL_PATHS:
        if not path.exists():
            continue
        spec = importlib.util.spec_from_file_location("fsot_compute", path)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        _MOD = mod
        _MOD_PATH = path
        return mod, path
    raise FileNotFoundError("fsot_compute.py not found in expected locations")


def canonical_constants() -> dict[str, float]:
    mod, _ = load_fsot_compute()
    return {
        "psi_con": float(mod.PSI_CON),
        "eta_eff": float(mod.ETA_EFF),
        "k": float(mod.K),
        "alpha_layer1": float(mod.ALPHA),
        "acoustic_bleed": float(mod.A_BLEED),
        "acoustic_inflow": float(mod.A_IN),
        "c_factor": float(mod.C_FACTOR),
    }


def canonical_domain_scalar(name: str) -> float:
    mod, _ = load_fsot_compute()
    return float(mod.domain_scalar(name))


def micro_scalar_v16(
    N: float,
    P: float,
    D: float,
    rh: float = 0.0,
    dp: float = 0.5,
    dt: float = 1.0,
    observed: bool = True,
    phi: float = 1.618033988749895,
) -> float:
    """Legacy MicroNeuron v16 projection (deprecated for canon; audit only)."""
    e = math.e
    g = 0.5772156649015329
    alpha_legacy = 0.0008082937414140402
    t1 = (N / D) * (1 + rh * 0.15)
    t2 = (P / max(1.0, D - 2)) * dt
    t3 = dp * (1 + 0.2 * rh)
    gr = math.exp(alpha_legacy * (1 - rh / 3) * g / phi)
    ch = 1.0 / (1.0 + abs(t1 + t2 + t3) * 0.08)
    om = math.exp(((g / e) * math.sqrt(2) * ch) * dp) * math.cos(dp + dp * 0.3) if observed else 1.0
    return (t1 + t2 + t3) * gr * om * ch


def compartment_scalar(trit_mean: float, c_factor: float = 0.2876, d_eff: float = 14.0) -> float:
    """NEURON pre-training compartment S = K · t̄ · C / D_eff."""
    k = canonical_constants()["k"]
    return k * trit_mean * (c_factor / d_eff)


def golden_angle_deg(phi: float | None = None) -> float:
    if phi is None:
        phi = (1 + math.sqrt(5)) / 2
    return 360.0 / (phi**2)


def rel_err(a: float, b: float) -> float:
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)