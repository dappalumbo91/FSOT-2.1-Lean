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
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

from fsot_paths import fsot_compute_candidates, fsot_compute_path  # noqa: E402

_MOD: Any = None
_MOD_PATH: Path | None = None


def load_fsot_compute():
    global _MOD, _MOD_PATH
    if _MOD is not None:
        return _MOD, _MOD_PATH
    for path in fsot_compute_candidates() or [fsot_compute_path()]:
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


_EXT_FOLDS: dict[str, Any] | None = None


def _extension_folds() -> dict[str, Any]:
    """Parent-nest folds. YAML D_eff/delta_psi/hits are not authority."""
    global _EXT_FOLDS
    if _EXT_FOLDS is None:
        path = ROOT / "data" / "extension_folds_derived.json"
        if path.exists():
            _EXT_FOLDS = json.loads(path.read_text(encoding="utf-8")).get("folds") or {}
        else:
            _EXT_FOLDS = {}
    return _EXT_FOLDS


def canonical_domain_scalar(name: str) -> float:
    """S for a 35-core name, or an extension inheriting the parent nest.

    YAML integers cannot leak: extensions read data/extension_folds_derived.json.
    """
    mod, _ = load_fsot_compute()
    if name in mod.DOMAINS:
        return float(mod.domain_scalar(name))
    fold = _extension_folds().get(name)
    if not fold:
        raise KeyError(f"no core or derived extension fold for {name!r}")
    return float(
        mod.scalar_from_fold(
            D_eff=int(fold["D_eff"]),
            look=mod.mpf(fold["look"]),
            hits=int(fold["hits"]),
            observed=bool(fold["observed"]),
        )
    )


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


def compartment_scalar(
    trit_mean: float,
    c_factor: float | None = None,
    d_eff: float | None = None,
) -> float:
    """NEURON pre-training compartment S = K · t̄ · C_factor / D_neuro.

    D is the Neuroscience nest value, not an assigned 14. C_factor is live C_FACTOR.
    """
    mod, _ = load_fsot_compute()
    if c_factor is None:
        c_factor = float(mod.C_FACTOR)
    if d_eff is None:
        d_eff = float(mod.derived_D_eff("Neuroscience"))
    k = float(mod.K)
    return k * trit_mean * (c_factor / d_eff)


def golden_angle_deg(phi: float | None = None) -> float:
    if phi is None:
        phi = (1 + math.sqrt(5)) / 2
    return 360.0 / (phi**2)


def rel_err(a: float, b: float) -> float:
    if b == 0:
        return abs(a - b)
    return abs(a - b) / abs(b)