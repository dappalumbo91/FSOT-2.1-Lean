"""Resolve literature σ / uncertainty bands for benchmark records."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANCHORS_PATH = ROOT / "data" / "literature_uncertainty_anchors.json"
STUMPED_PATH = ROOT / "data" / "stumped_observables_reference.json"

CONTESTED_EVAL_KINDS = frozenset(
    {
        "contested_observable",
        "w0_live",
        "wa_live",
        "wa_preregistered",
        "preregistered_falsifiable",
        "h0_live",
    }
)

CONTESTED_PROPERTIES = frozenset(
    {
        "hubble_constant",
        "sector_h0_overlay",
        "frb_p34_periodicity",
        "host_h0_median",
        "host_h0_weighted_mean",
        "dark_energy_eos",
        "dark_energy_eos_evolution",
        "reionization_optical_depth",
    }
)

RECORD_NAME_ANCHOR_ALIASES: dict[str, str] = {
    "Mean_dependency_length_EN": "mean_dependency_length",
    "FRB20200929C": "frb_p34_periodicity",
}

PROPERTY_ANCHOR_ALIASES: dict[str, str] = {
    "H0_planck_km_s_Mpc": "hubble_constant",
    "h0_planck_km_s_mpc": "hubble_constant",
    "w0_bao_readout": "w0_constraint",
    "wa_bao_readout": "dark_energy_eos",
    "w0_cmb_readout": "w0_constraint",
    "wa_cmb_readout": "dark_energy_eos",
}

BIOCHEM_UNCERTAINTY_PCT = 0.2
BEHAVIORAL_UNCERTAINTY_PCT = 0.15


def _normalize_biochem_text(text: str) -> str:
    p = text.lower()
    for src, dst in (("δ", "delta"), ("Δ", "delta"), ("γ", "gamma")):
        p = p.replace(src, dst)
    p = p.replace("delta g", "deltag").replace("delta_g", "deltag")
    return p


def _biochem_property(*fields: str) -> bool:
    tokens = (
        "pka",
        "pkd",
        "pki",
        "deltag",
        "km",
        "kcat",
        "ki",
        "ic50",
        "ec50",
        "kd",
        "stacking",
        "activation_ea",
        "youngs_modulus",
    )
    for field in fields:
        if not field:
            continue
        p = _normalize_biochem_text(field)
        if any(t in p for t in tokens):
            return True
    return False


@lru_cache(maxsize=1)
def load_anchors() -> dict[str, dict[str, Any]]:
    if not ANCHORS_PATH.exists():
        return {}
    doc = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    return dict((doc.get("anchors") or {}))


@lru_cache(maxsize=1)
def load_stumped_ids() -> dict[str, dict[str, Any]]:
    if not STUMPED_PATH.exists():
        return {}
    doc = json.loads(STUMPED_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    for row in doc.get("observables") or []:
        prop = str(row.get("property") or "")
        if prop:
            out[prop] = row
        oid = str(row.get("id") or "")
        if oid:
            out[oid] = row
    return out


def is_contested_record(record: dict) -> bool:
    ek = str(record.get("eval_kind") or "").lower()
    if ek in CONTESTED_EVAL_KINDS:
        return True
    prop = str(record.get("property") or "")
    if prop in CONTESTED_PROPERTIES:
        return True
    if str(record.get("comparison_class") or "") in {
        "tension_sector_prediction",
        "preregistered_falsifiable",
        "literature_monitor",
        "bao_sector_prediction",
        "cmb_sector_prediction",
    }:
        return True
    if record.get("sector") and prop == "hubble_constant":
        return True
    return False


def _stumped_canonical_property(record: dict) -> str:
    """Map record id/name aliases to stumped observable property keys."""
    prop = str(record.get("property") or "")
    for key in (prop, str(record.get("name") or ""), str(record.get("id") or "")):
        if not key:
            continue
        stumped = load_stumped_ids().get(key)
        if stumped and stumped.get("property"):
            return str(stumped["property"])
    return prop


def resolve_reference_uncertainty_pct(record: dict) -> float | None:
    """Return literature relative uncertainty (%) when known."""
    row = record or {}
    if row.get("reference_uncertainty_pct") is not None:
        try:
            return float(row["reference_uncertainty_pct"])
        except (TypeError, ValueError):
            pass

    sci = row.get("scientific_measurement") or {}
    if sci.get("reference_uncertainty_pct") is not None:
        try:
            return float(sci["reference_uncertainty_pct"])
        except (TypeError, ValueError):
            pass

    if row.get("measured_uncertainty_rel") is not None:
        try:
            return float(row["measured_uncertainty_rel"]) * 100.0
        except (TypeError, ValueError):
            pass

    measured = row.get("measured")
    if row.get("measured_uncertainty") is not None and measured not in (None, 0):
        try:
            return abs(float(row["measured_uncertainty"]) / float(measured)) * 100.0
        except (TypeError, ValueError, ZeroDivisionError):
            pass

    if row.get("sigma") is not None and row.get("sigma_distance") is not None:
        try:
            return float(row.get("error_pct") or 0.0)
        except (TypeError, ValueError):
            pass

    prop = _stumped_canonical_property(row)
    anchors = load_anchors()
    anchor = anchors.get(prop)
    if anchor is None:
        anchor = anchors.get(PROPERTY_ANCHOR_ALIASES.get(prop, ""))
    if anchor is None and _biochem_property(
        prop,
        str(row.get("name") or ""),
        str(row.get("display_name") or ""),
        str(row.get("section_display_name") or ""),
    ):
        return BIOCHEM_UNCERTAINTY_PCT
    if anchor is None and (
        "neuroeconomics" in str(row.get("lab") or "").lower()
        or prop.endswith("_alpha")
        or "transfer_pct" in prop
    ):
        return BEHAVIORAL_UNCERTAINTY_PCT
    if anchor is None:
        name = str(row.get("name") or "")
        alias = RECORD_NAME_ANCHOR_ALIASES.get(name)
        if alias:
            anchor = anchors.get(alias)
    if anchor and anchor.get("measured_uncertainty_pct") is not None:
        return float(anchor["measured_uncertainty_pct"])

    stumped = load_stumped_ids().get(prop)
    if stumped and stumped.get("measured_uncertainty_pct") is not None:
        return float(stumped["measured_uncertainty_pct"])

    return None


def literature_metadata_for_record(record: dict) -> dict[str, Any]:
    """Attach reference citation + uncertainty for scientific_measurement envelope."""
    prop = str(record.get("property") or "")
    anchors = load_anchors()
    anchor = anchors.get(prop) or {}
    stumped = load_stumped_ids().get(prop) or {}

    ref = record.get("reference") or anchor.get("reference") or stumped.get("reference")
    unc_pct = resolve_reference_uncertainty_pct(record)
    contested = is_contested_record(record)

    out: dict[str, Any] = {}
    if ref:
        out["reference"] = ref
    if unc_pct is not None:
        out["reference_uncertainty_pct"] = unc_pct
    if contested:
        out["contested"] = True
        out["precision_tier"] = "contested"
    status = stumped.get("status") or anchor.get("status")
    if status:
        out["observable_status"] = status
    return out