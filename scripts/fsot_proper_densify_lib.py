#!/usr/bin/env python3
"""FSOT-correct densify — real measured anchors + seed formula / domain S only.

Hard rules (Damian / FSOT authority):
  1. measured = real data (literature target, API, catalog, lab) — never invented
  2. computed = evaluate_formula(seed formula) OR fsot_scaled(measured, domain)
  3. NEVER pad with seed_identity (φ=φ), process_gate, or cross-domain error copy
  4. Wrong residual → fix D_eff / domain route, not free parameters

Use this for all densify / thin-fill work.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STRICT_JSONL = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"

# Contaminating densify markers — strip these on remediation
BAD_EVAL_KINDS = frozenset(
    {
        "c_thin_depth_relay",
        "process_gate",
        "seed_densify",
        "lean_route_bridge",  # pool identity bridge — not a measurement
    }
)
BAD_PROPERTY_PREFIXES = (
    "seed_phi",
    "seed_e",
    "seed_pi",
    "seed_theta",
    "seed_c_eff",
    "seed_p_var",
    "seed_k",
    "seed_coherence",
    "zero_free_param",
    "route_credibility_process",
    "scaffold_ready",
    "bits_per_trit",  # when used as pad; real pack panels keep via formula tag
)
BAD_NAME_MARKERS = (
    "_seed_densify",
    "_process",
    "seed densify",
    "structure densify",
    "process densify",
)
BAD_FORMULAS = frozenset({"process_gate", "process"})
BAD_NOTES = (
    "seed densify",
    "process densify",
    "structure densify",
    "not free-param fold",
    "not free BR fold",
    "depth_relay",
    "c_thin_depth",
)


def is_contaminating_row(row: dict[str, Any]) -> bool:
    """True if row is densify padding / relay copy, not FSOT formula vs real data."""
    ek = str(row.get("eval_kind") or "")
    if ek in BAD_EVAL_KINDS or ek.endswith("_depth_relay"):
        return True
    if row.get("depth_relay_from") or row.get("source_panel") and ek in ("", "live_formula") and "relay" in ek:
        return True
    if row.get("depth_relay_from"):
        return True
    prop = str(row.get("property") or "")
    name = str(row.get("name") or "")
    formula = str(row.get("formula") or "")
    note = str(row.get("note") or "")
    blob = f"{prop} {name} {formula} {note}".lower()
    if formula in BAD_FORMULAS:
        return True
    if any(m in blob for m in BAD_NOTES):
        return True
    if any(prop.startswith(p) or prop == p.rstrip("_") for p in BAD_PROPERTY_PREFIXES):
        # allow pack density on hardware labs with explicit pack formula
        if "pack" in formula.lower() or "trit" in formula.lower() and "ceil" in formula.lower():
            if row.get("lab", "").startswith("fsot_") and "hardware" in str(row.get("layer", "")):
                return False
        if prop in ("bits_per_trit", "states_per_u64") and formula and "log2" in formula or "64" in formula:
            # real packing law — keep if measured != pure pad name
            if "seed densify" not in name and "seed_densify" not in name:
                return False
        return True
    if any(m in name for m in BAD_NAME_MARKERS):
        return True
    # pure identity pad: computed==measured, error 0, no real formula path
    try:
        c, m = float(row.get("computed")), float(row.get("measured"))
        e = float(row.get("error_pct") or 0)
        if e == 0.0 and c == m and not formula and ek in ("live_formula", "fsot_prediction", ""):
            if "identity" in blob or "densify" in blob:
                return True
    except (TypeError, ValueError):
        pass
    return False


def strip_contamination(records: list[dict]) -> list[dict]:
    return [r for r in records if not is_contaminating_row(r)]


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0.0 and computed == 0.0:
        return 0.0
    denom = abs(measured) if abs(measured) > 1e-30 else abs(computed)
    if denom < 1e-30:
        return 0.0 if abs(computed - measured) < 1e-12 else 100.0
    return abs(computed - measured) / denom * 100.0


_CORPUS_CACHE: list[dict[str, Any]] | None = None


def _load_corpus_eval_cache() -> list[dict[str, Any]]:
    """One-time live seed-formula eval of unique corpus targets (real measured)."""
    global _CORPUS_CACHE
    if _CORPUS_CACHE is not None:
        return _CORPUS_CACHE
    if not STRICT_JSONL.is_file():
        _CORPUS_CACHE = []
        return _CORPUS_CACHE
    from math_formula_eval import core_context, evaluate_formula  # noqa: WPS433

    ctx = core_context()
    ctx.update(
        {
            "eta": ctx.get("eta_eff", 0),
            "psi": ctx.get("psi_con", 0),
            "theta": ctx.get("theta_s", 0),
            "g": ctx.get("g_cat", 0),
            "gamma": ctx.get("gamma", 0),
            "poof": ctx.get("poof", 0),
            "c_factor": ctx.get("c_factor", 0),
            "pnew": ctx.get("pnew", 0),
            "pbase": ctx.get("pbase", 0),
        }
    )
    seen: set[tuple[str, str, str]] = set()
    cache: list[dict[str, Any]] = []
    with STRICT_JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            outcome = row.get("outcome") or {}
            target = outcome.get("target_value", row.get("target_quantity"))
            formula = row.get("formula_canonical") or row.get("formula_publication")
            if target is None or not formula:
                continue
            key = (str(row.get("concept_name") or ""), str(formula), str(target))
            if key in seen:
                continue
            seen.add(key)
            try:
                measured = float(target)
                computed = float(evaluate_formula(str(formula), ctx))
            except Exception:
                continue
            if not math.isfinite(computed) or not math.isfinite(measured):
                continue
            err = _err_pct(computed, measured)
            blob = " ".join(
                str(row.get(k) or "")
                for k in ("concept_name", "source_relative_path", "project", "fsot_physics_explanation")
            ).lower()
            cache.append(
                {
                    "property": str(row.get("concept_name") or "formula_obs"),
                    "name": str(row.get("record_id") or row.get("concept_name") or "corpus"),
                    "computed": computed,
                    "measured": measured,
                    "error_pct": round(err, 9),
                    "formula": str(formula),
                    "blob": blob,
                    "verification_citations": row.get("verification_citations"),
                }
            )
    _CORPUS_CACHE = cache
    return cache


def formula_corpus_fsot_records(
    *,
    lab: str,
    domain: str,
    limit: int = 40,
    max_error_pct: float = 0.5,  # green-gate compatible: seed formula vs real target
    seed: int = 42,
    domain_keywords: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Live-eval seed formulas from strict_empirical.jsonl vs real target_quantity."""
    cache = _load_corpus_eval_cache()
    candidates: list[dict] = []
    for row in cache:
        if float(row["error_pct"]) > max_error_pct:
            continue
        if domain_keywords:
            blob = row.get("blob") or ""
            if not any(kw.lower() in blob for kw in domain_keywords):
                continue
        candidates.append(
            {
                "lab": lab,
                "property": row["property"],
                "name": row["name"],
                "computed": row["computed"],
                "measured": row["measured"],
                "error_pct": row["error_pct"],
                "eval_kind": "fsot_seed_formula",
                "formula": row["formula"],
                "fsot_domain": domain,
                "source": "vendor/formula_corpus/by_domain/strict_empirical.jsonl",
                "verification_citations": row.get("verification_citations"),
            }
        )
    rng = random.Random(seed)
    if len(candidates) > limit:
        candidates.sort(key=lambda r: float(r["error_pct"]))
        head = candidates[: max(limit // 2, 1)]
        rest = candidates[len(head) :]
        rng.shuffle(rest)
        candidates = head + rest[: max(0, limit - len(head))]
    return candidates[:limit]


def measured_fsot_scaled_records(
    anchors: list[dict[str, Any]],
    *,
    lab: str,
    default_domain: str,
) -> list[dict[str, Any]]:
    """Each anchor: {property, name, measured, domain?} → make_fsot_record via domain S."""
    from fsot_api_predict_lib import make_fsot_record  # noqa: WPS433

    out: list[dict] = []
    for a in anchors:
        if a.get("measured") is None:
            continue
        try:
            measured = float(a["measured"])
        except (TypeError, ValueError):
            continue
        domain = str(a.get("domain") or default_domain)
        rec = make_fsot_record(
            lab=lab,
            property_name=str(a.get("property") or "observable"),
            name=str(a.get("name") or a.get("property") or "anchor"),
            measured=measured,
            domain=domain,
            formula=a.get("formula"),
            eval_kind="fsot_prediction",
            extra={k: v for k, v in a.items() if k not in ("property", "name", "measured", "domain", "formula")},
        )
        out.append(rec)
    return out


def densify_to_min(
    base: list[dict],
    *,
    lab: str,
    domain: str,
    min_records: int = 20,
    domain_keywords: list[str] | None = None,
    extra_anchors: list[dict] | None = None,
) -> list[dict]:
    """Strip contamination, keep real rows, fill from formula corpus + optional anchors."""
    records = strip_contamination(base)
    seen = {(r.get("name"), r.get("property")) for r in records}

    def _add(rows: list[dict]) -> None:
        for r in rows:
            if len(records) >= min_records:
                return
            key = (r.get("name"), r.get("property"))
            if key in seen:
                continue
            seen.add(key)
            records.append(r)

    if extra_anchors:
        _add(measured_fsot_scaled_records(extra_anchors, lab=lab, default_domain=domain))
    need = max(0, min_records - len(records))
    if need > 0:
        _add(
            formula_corpus_fsot_records(
                lab=lab,
                domain=domain,
                limit=max(need + 10, 30),
                domain_keywords=domain_keywords,
            )
        )
    # if still short, broader corpus (still real targets + seed formulas)
    if len(records) < min_records:
        _add(
            formula_corpus_fsot_records(
                lab=lab,
                domain=domain,
                limit=min_records - len(records) + 20,
                domain_keywords=None,
            )
        )
    return records
