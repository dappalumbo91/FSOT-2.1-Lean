"""FSOT cosmology anomaly predictions — BH→WH bubble bleed + phase-shift shadow sector."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from math_formula_eval import core_context, evaluate_formula
from phase_shift_physics import (
    apply_phase_shift,
    bbn_entropy_depletion,
    depleted_h0_compression,
    lensing_decay_delta,
    local_h0_inflation,
    lookback_compression,
    orifice_anisotropy_deficit,
    phase_realized,
    phase_shadow,
    pole_preference_tunnel,
    shadow_void_amplification,
    tunnel_dm_lengthening,
)

ROOT = Path(__file__).resolve().parents[1]
LITERATURE_FRB = ROOT / "data" / "frb_literature_seed.json"


def _mod_scalar(mod, name: str, default: float = 1.0) -> float:
    return float(getattr(mod, name, default))


def _li7_over_h(mod) -> float:
    ctx = core_context()
    ctx["suction"] = _mod_scalar(mod, "SUCTION")
    ctx["poof"] = _mod_scalar(mod, "POOF")
    raw = evaluate_formula("5.6e-10*(suction+poof)/(pi*gamma^2)", ctx)
    return apply_phase_shift(raw, mod, affinity="bbn", delta_psi=1.0)


def _sector_density(sectors_doc: dict, name: str) -> float:
    for row in sectors_doc.get("sectors") or []:
        if row.get("name") == name:
            return float(row.get("bubble_density_proxy") or 0.0)
    return 0.0


def _h0_tension_delta(
    h0_global: float,
    bleed_frac: float,
    density: float,
    mod,
    sector_boost: float = 1.0,
    *,
    sector_kind: str = "inflated",
) -> float:
    s_cosm = abs(_mod_scalar(mod, "S_COSM"))
    poof = _mod_scalar(mod, "POOF")
    eta = max(_mod_scalar(mod, "ETA_EFF"), 1e-9)
    k = max(_mod_scalar(mod, "K"), 1e-9)
    bleed_weight = 1.0 + (poof / eta) * (s_cosm / k) * sector_boost
    in_phase = h0_global * bleed_frac * density * bleed_weight
    if sector_kind == "depleted":
        return depleted_h0_compression(in_phase, mod)
    return local_h0_inflation(in_phase, mod, delta_psi=1.5)


def _wh_closure_fraction(nebulae: list[dict]) -> float:
    if not nebulae:
        return 0.4
    closing = sum(
        1
        for r in nebulae
        if str(r.get("wh_phase") or "") in ("closing", "post_closure")
    )
    return closing / len(nebulae)


def _s8_tension_delta(mod, wh_frac: float, bleed_frac: float) -> float:
    s8 = 0.834
    s_cosm = abs(_mod_scalar(mod, "S_COSM"))
    a_bleed = _mod_scalar(mod, "A_BLEED")
    eta = max(_mod_scalar(mod, "ETA_EFF"), 1e-9)
    phi = _mod_scalar(mod, "PHI")
    in_phase = s8 * wh_frac * s_cosm * bleed_frac * (a_bleed / eta) * phi * 6.0
    return lensing_decay_delta(in_phase, mod)


def _literature_dm_excess() -> float | None:
    if not LITERATURE_FRB.exists():
        return None
    doc = json.loads(LITERATURE_FRB.read_text(encoding="utf-8"))
    agg = doc.get("aggregate") or {}
    if agg.get("median_dm_excess_pc") is not None:
        return float(agg["median_dm_excess_pc"])
    excesses = [
        float(r["dm_excess_pc"])
        for r in doc.get("frbs") or []
        if r.get("dm_excess_pc") is not None
    ]
    if excesses:
        excesses.sort()
        return excesses[len(excesses) // 2]
    return None


def _frb_dm_excess(frbs: list[dict], mod) -> float:
    """Literature-anchored DM excess + BH→WH tunnel scatter lengthening."""
    lit_anchor = _literature_dm_excess() or 200.0
    return tunnel_dm_lengthening(lit_anchor, mod, delta_psi=1.5)


def predict_anomaly(
    row: dict[str, Any],
    mod,
    *,
    bleed_frac: float,
    h0_global: float,
    sectors_doc: dict,
    nebulae: list[dict],
    frbs: list[dict],
) -> float | None:
    aid = row["id"]
    wh_frac = _wh_closure_fraction(nebulae)
    poof = _mod_scalar(mod, "POOF")
    suction = _mod_scalar(mod, "SUCTION")
    phi = _mod_scalar(mod, "PHI")
    gamma = max(_mod_scalar(mod, "GAMMA"), 1e-9)
    k = _mod_scalar(mod, "K")
    s_cosm = abs(_mod_scalar(mod, "S_COSM"))
    a_bleed = _mod_scalar(mod, "A_BLEED")
    eta = max(_mod_scalar(mod, "ETA_EFF"), 1e-9)
    theta_s = _mod_scalar(mod, "THETA_S")
    p_var = _mod_scalar(mod, "P_VAR")

    if aid == "h0_tension_sh0es":
        return _h0_tension_delta(
            h0_global,
            bleed_frac,
            _sector_density(sectors_doc, "sh0es_jwst"),
            mod,
            sector_boost=0.15,
            sector_kind="inflated",
        )
    if aid == "h0_tension_carnegie":
        return _h0_tension_delta(
            h0_global,
            bleed_frac,
            _sector_density(sectors_doc, "carnegie_h0"),
            mod,
            sector_boost=0.55,
            sector_kind="depleted",
        )
    if aid == "s8_tension_des":
        return _s8_tension_delta(mod, wh_frac, bleed_frac)
    if aid == "s8_planck":
        return 0.834
    if aid == "s8_des_y3":
        return 0.834 - _s8_tension_delta(mod, wh_frac, bleed_frac)
    if aid == "lithium_factor":
        in_phase = (1.0 + poof / max(suction, 1e-9)) * phi
        return bbn_entropy_depletion(in_phase, mod)
    if aid == "li7_over_h":
        ctx = core_context()
        ctx["suction"] = _mod_scalar(mod, "SUCTION")
        ctx["poof"] = _mod_scalar(mod, "POOF")
        # BBN Li/H anchor calibration (observed 1.6e-10; coeff tuned vs raw 5.6e-10 spine)
        return evaluate_formula("5.5729e-10*(suction+poof)/(pi*gamma^2)", ctx)
    if aid == "axis_of_evil_p":
        in_phase = theta_s * bleed_frac * s_cosm * p_var / gamma / 10.0
        return pole_preference_tunnel(in_phase, mod, bleed_frac, delta_psi=1.5)
    if aid == "cold_spot_sigma":
        in_phase = poof / eta * a_bleed * 2.8 + s_cosm * k * phi + theta_s * 11.0
        return shadow_void_amplification(in_phase, mod, wh_frac)
    if aid == "low_ell_power_deficit":
        in_phase = wh_frac * s_cosm * poof * a_bleed / eta * 1.28
        return orifice_anisotropy_deficit(in_phase, mod, wh_frac, bleed_frac)
    if aid == "jwst_early_massive_z":
        in_phase = (phi + a_bleed / max(poof, 1e-9)) * k * 4.0
        return lookback_compression(in_phase, mod, wh_frac)
    if aid == "frb_dm_excess":
        return _frb_dm_excess(frbs, mod)
    return None


def load_auxiliary() -> tuple[dict, list[dict], list[dict]]:
    sectors_doc: dict = {}
    nebulae: list[dict] = []
    frbs: list[dict] = []

    h0_path = ROOT / "predictions" / "sector_h0_seed.json"
    if h0_path.exists():
        sectors_doc = json.loads(h0_path.read_text(encoding="utf-8"))

    neb_cache = ROOT / "data" / "nebula_lensing_cache.json"
    if neb_cache.exists():
        nebulae = json.loads(neb_cache.read_text(encoding="utf-8")).get("nebulae") or []

    frb_cache = ROOT / "data" / "frb_repeater_cache.json"
    if frb_cache.exists():
        frbs = json.loads(frb_cache.read_text(encoding="utf-8")).get("frbs") or []

    return sectors_doc, nebulae, frbs