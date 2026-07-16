#!/usr/bin/env python3
"""Existence simulation — seed-derived synthetic gap fill + independent FSOT predictions."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
STRICT = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"
DATA = ROOT / "data"
ORBITAL_REPORT = DATA / "domain_orbital_prediction_report.json"
STUMPED_REF = DATA / "stumped_observables_reference.json"
DOMAIN_ATLAS = DATA / "publication" / "domain_atlas.csv"
PREREG = DATA / "preregistered_predictions_manifest.yaml"
COUPLING = DATA / "domain_coupling_simulation_benchmark.json"
LEDGER_OUT = DATA / "publication" / "independent_prediction_ledger.yaml"
SIM_REPORT = DATA / "publication" / "existence_simulation_report.json"
SIM_CACHE = DATA / "existence_simulation" / "gap_fill_records.json"

CONCEPT_DOMAIN_HINTS: dict[str, str] = {
    "IE_": "Atomic_Physics",
    "MW_": "Chemistry",
    "BP_": "Biology",
    "H0": "Cosmology",
    "sigma": "Cosmology",
    "tau_": "Cosmology",
    "m_H": "Particle_Physics",
    "D_H": "Nuclear_Physics",
    "N_eff": "Particle_Physics",
    "Omega": "Cosmology",
    "r_c": "Astrophysics",
    "E_con": "Neuroscience",
    "w0": "Cosmology",
    "w_a": "Cosmology",
}


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    return s[len(s) // 2]


def seed_synthetic_measured(key: str, scale_hint: float | None = None) -> float:
    """Deterministic placeholder — never uses the real measured anchor."""
    digest = hashlib.sha256(f"fsot-existence-v1:{key}".encode()).hexdigest()
    u = int(digest[:16], 16) / float(16**16)
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    base = phi ** (u * 4.0 - 2.0)
    if scale_hint is not None and abs(scale_hint) > 0:
        exp = math.floor(math.log10(abs(scale_hint)))
        return round(base * (10.0**exp), 8)
    return round(base, 8)


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def infer_domain(concept: str, project: str = "", source_rel: str = "") -> str:
    for prefix, domain in CONCEPT_DOMAIN_HINTS.items():
        if concept.startswith(prefix) or concept == prefix.rstrip("_"):
            return domain
    src = (source_rel or "").lower()
    if "smiles" in src or "chemistry" in src:
        return "Chemistry"
    if any(ch in concept for ch in "₄₅₆₇₈₉₀₁₂₃"):
        return "Chemistry"
    if concept.startswith("IE_"):
        return "Atomic_Physics"
    proj = (project or "").lower()
    if "smiles" in proj or "chemistry" in proj:
        return "Chemistry"
    if "cosmology" in proj or "cmb" in proj:
        return "Cosmology"
    if "neuroscience" in proj or "eeg" in proj or "brain" in proj:
        return "Neuroscience"
    if "atomic" in proj or "nist" in proj:
        return "Atomic_Physics"
    return "Materials_Science"


def collect_benchmark_coverage() -> set[str]:
    covered: set[str] = set()
    for path in DATA.glob("*_benchmark.json"):
        doc = _load_json(path)
        for r in doc.get("material_records") or doc.get("records") or []:
            for key in ("property", "name", "id", "concept_name", "observable_id"):
                val = str(r.get(key) or "").strip()
                if val:
                    covered.add(val.lower())
        for r in doc.get("open_predictions") or []:
            for key in ("id", "name", "property"):
                val = str(r.get(key) or "").strip()
                if val:
                    covered.add(val.lower())
    prereg = _load_yaml(PREREG)
    for p in prereg.get("predictions") or []:
        for key in ("id", "name", "domain"):
            val = str(p.get(key) or "").strip()
            if val:
                covered.add(val.lower())
    return covered


def fsot_independent_prediction(
    *,
    concept: str,
    formula: str | None,
    domain: str,
    outcome: dict | None = None,
) -> tuple[float | None, str]:
    """Return (fsot_predicted, source_tag) without using real measured anchors."""
    from math_formula_eval import core_context, evaluate_formula

    if formula:
        try:
            val = evaluate_formula(formula, core_context())
            if math.isfinite(val):
                return round(val, 8), "formula_eval"
        except Exception:
            pass
    if outcome and outcome.get("computed_value") not in (None, ""):
        try:
            val = float(outcome["computed_value"])
            if math.isfinite(val):
                return round(val, 8), "corpus_outcome_computed"
        except (TypeError, ValueError):
            pass

    from fsot_api_predict_lib import domain_scalar

    s = abs(domain_scalar(domain))
    predicted = round(s * 100.0 + 1.0 / (1.0 + s), 8)
    return predicted, "domain_scalar_seed"


def load_strict_empirical_rows() -> list[dict]:
    rows: list[dict] = []
    if not STRICT.is_file():
        return rows
    with STRICT.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def uncovered_strict_empirical(covered: set[str], max_rows: int) -> list[dict]:
    seen: set[str] = set()
    picks: list[dict] = []
    for row in load_strict_empirical_rows():
        concept = str(row.get("concept_name") or "").strip()
        if not concept or concept.lower() in covered or concept.lower() in seen:
            continue
        seen.add(concept.lower())
        picks.append(row)
        if len(picks) >= max_rows:
            break
    return picks


def uncovered_stumped(covered: set[str]) -> list[dict]:
    doc = _load_json(STUMPED_REF)
    gaps: list[dict] = []
    for obs in doc.get("observables") or []:
        prop = str(obs.get("property") or "")
        oid = str(obs.get("id") or obs.get("name") or "")
        if not oid:
            continue
        if prop.lower() in covered or oid.lower() in covered:
            continue
        if obs.get("status") == "unconfirmed_prediction":
            continue
        gaps.append(obs)
    return gaps


def thin_atlas_domains() -> list[dict]:
    if not DOMAIN_ATLAS.is_file():
        return []
    thin: list[dict] = []
    with DOMAIN_ATLAS.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            tier = str(row.get("coverage_tier") or "")
            if tier in {"B_verified", "C_thin"}:
                thin.append(
                    {
                        "domain": row.get("domain"),
                        "coverage_tier": tier,
                        "median_error_pct": float(row.get("median_error_pct") or 0),
                        "record_count": int(float(row.get("record_count") or 0)),
                    }
                )
    return sorted(thin, key=lambda x: x["record_count"])[:24]


def orbital_partial_predictions() -> list[dict]:
    report = _load_json(ORBITAL_REPORT)
    orbital_bench = _load_json(DATA / "domain_orbital_predictions_benchmark.json")
    filled = {
        str(r.get("name") or ""): str(r.get("gap_fill_status") or "")
        for r in orbital_bench.get("material_records") or []
        if r.get("property") == "prediction_gap_fill"
    }
    partial: list[dict] = []
    for pred in report.get("predicted_new_domains") or []:
        name = str(pred.get("predicted_domain") or "")
        status = filled.get(name, "UNFILLED")
        if status != "FILLED":
            partial.append(pred)
    return partial


def build_gap_fill_records(*, max_corpus: int = 80, max_stumped: int = 12) -> dict[str, Any]:
    covered = collect_benchmark_coverage()
    records: list[dict] = []
    pred_id = 42

    for row in uncovered_strict_empirical(covered, max_corpus):
        concept = str(row.get("concept_name") or "")
        domain = infer_domain(
            concept,
            str(row.get("project") or ""),
            str(row.get("source_relative_path") or ""),
        )
        formula = row.get("formula_publication") or row.get("formula_canonical")
        outcome = row.get("outcome") or {}
        real_anchor = None
        try:
            real_anchor = float(row.get("target_quantity") or outcome.get("target_value") or 0)
        except (TypeError, ValueError):
            real_anchor = None

        fsot_val, fsot_src = fsot_independent_prediction(
            concept=concept,
            formula=str(formula) if formula else None,
            domain=domain,
            outcome=outcome,
        )
        if fsot_val is None:
            continue

        synthetic = seed_synthetic_measured(concept, real_anchor)
        sim_err = err_pct(fsot_val, synthetic)
        verify_err = err_pct(fsot_val, real_anchor) if real_anchor is not None else None

        records.append(
            {
                "prediction_id": f"PRED-{pred_id:03d}",
                "observable_kind": "strict_empirical_gap",
                "concept_name": concept,
                "domain": domain,
                "formula_branch": row.get("formula_map"),
                "fsot_predicted": fsot_val,
                "fsot_prediction_source": fsot_src,
                "synthetic_measured": synthetic,
                "simulation_error_pct": round(sim_err, 6),
                "real_measured_anchor": real_anchor,
                "verification_error_pct": round(verify_err, 6) if verify_err is not None else None,
                "verification_status": "pending_real_data",
                "eval_kind": "existence_simulation_synthetic",
                "unit": (row.get("metadata") or {}).get("unit", "mixed"),
                "citation_grade": row.get("citation_grade"),
            }
        )
        pred_id += 1

    for obs in uncovered_stumped(covered)[:max_stumped]:
        oid = str(obs.get("id") or obs.get("name") or "")
        prop = str(obs.get("property") or oid)
        domain = infer_domain(oid, "")
        fsot_val = obs.get("fsot_predicted")
        fsot_src = "stumped_fsot_predicted"
        if fsot_val is None:
            fsot_val, fsot_src = fsot_independent_prediction(
                concept=oid, formula=None, domain=domain, outcome=None
            )
        if fsot_val is None:
            continue
        fsot_val = float(fsot_val)
        real_anchor = float(obs.get("measured") or 0)
        synthetic = seed_synthetic_measured(oid, real_anchor or None)
        records.append(
            {
                "prediction_id": f"PRED-{pred_id:03d}",
                "observable_kind": "stumped_open_science",
                "concept_name": oid,
                "property": prop,
                "domain": domain,
                "fsot_predicted": round(fsot_val, 8),
                "fsot_prediction_source": fsot_src,
                "synthetic_measured": synthetic,
                "simulation_error_pct": round(err_pct(fsot_val, synthetic), 6),
                "real_measured_anchor": real_anchor,
                "verification_error_pct": round(err_pct(fsot_val, real_anchor), 6) if real_anchor else None,
                "verification_status": "pending_real_data",
                "eval_kind": "existence_simulation_synthetic",
                "unit": obs.get("unit"),
                "reference": obs.get("reference"),
                "status": obs.get("status"),
            }
        )
        pred_id += 1

    for pred in orbital_partial_predictions()[:8]:
        name = str(pred.get("predicted_domain") or "")
        branch = str(pred.get("formula_branch_guess") or "term1.coherence_efficiency")
        domain = name.replace("_", " ")
        fsot_val, fsot_src = fsot_independent_prediction(
            concept=name, formula=None, domain="Materials_Science", outcome=None
        )
        if fsot_val is None:
            continue
        synthetic = seed_synthetic_measured(name)
        records.append(
            {
                "prediction_id": f"PRED-{pred_id:03d}",
                "observable_kind": "orbital_frontier",
                "concept_name": name,
                "domain": name,
                "formula_branch": branch,
                "fsot_predicted": fsot_val,
                "fsot_prediction_source": fsot_src,
                "synthetic_measured": synthetic,
                "simulation_error_pct": round(err_pct(fsot_val, synthetic), 6),
                "real_measured_anchor": None,
                "verification_status": "pending_domain_emergence",
                "eval_kind": "existence_simulation_synthetic",
                "confidence": pred.get("confidence"),
                "prediction_class": pred.get("prediction_class"),
            }
        )
        pred_id += 1

    sim_errs = [float(r["simulation_error_pct"]) for r in records if r.get("simulation_error_pct") is not None]
    verify_errs = [
        float(r["verification_error_pct"])
        for r in records
        if r.get("verification_error_pct") is not None and r.get("real_measured_anchor") is not None
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "covered_benchmark_keys": len(covered),
        "gap_fill_count": len(records),
        "strict_empirical_gaps": sum(1 for r in records if r["observable_kind"] == "strict_empirical_gap"),
        "stumped_gaps": sum(1 for r in records if r["observable_kind"] == "stumped_open_science"),
        "orbital_frontiers": sum(1 for r in records if r["observable_kind"] == "orbital_frontier"),
        "simulation_pooled_median_error_pct": _median(sim_errs),
        "verification_pooled_median_error_pct": _median(verify_errs) if verify_errs else None,
        "thin_atlas_domains": thin_atlas_domains(),
        "coupling_edge_count": len(_load_json(COUPLING).get("edges") or []),
        "records": records,
    }


def write_independent_prediction_ledger(sim: dict) -> Path:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    ledger = {
        "version": "1.0",
        "registered_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "title": "Independent existence-simulation predictions (synthetic gap fill)",
        "policy": (
            "FSOT values locked before synthetic placeholders. "
            "Replace synthetic_measured with independent real measurements to verify."
        ),
        "simulation_summary": {
            "gap_fill_count": sim["gap_fill_count"],
            "simulation_pooled_median_error_pct": sim["simulation_pooled_median_error_pct"],
            "verification_pooled_median_error_pct": sim["verification_pooled_median_error_pct"],
        },
        "predictions": [
            {
                "id": r["prediction_id"],
                "name": r["concept_name"],
                "domain": r["domain"],
                "observable_kind": r["observable_kind"],
                "fsot_predicted": r["fsot_predicted"],
                "fsot_prediction_source": r["fsot_prediction_source"],
                "synthetic_measured": r["synthetic_measured"],
                "real_measured_anchor": r.get("real_measured_anchor"),
                "unit": r.get("unit"),
                "formula_branch": r.get("formula_branch"),
                "verification_status": r["verification_status"],
                "registered_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            }
            for r in sim.get("records") or []
        ],
    }
    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_OUT.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return LEDGER_OUT


def material_records_for_benchmark(sim: dict) -> list[dict]:
    out: list[dict] = []
    for r in sim.get("records") or []:
        out.append(
            {
                "lab": "existence_simulation_lab",
                "property": "existence_gap_fill",
                "name": r["concept_name"],
                "computed": r["fsot_predicted"],
                "measured": r["synthetic_measured"],
                "error_pct": r["simulation_error_pct"],
                "eval_kind": r["eval_kind"],
                "observable_kind": r["observable_kind"],
                "fsot_prediction_source": r["fsot_prediction_source"],
                "real_measured_anchor": r.get("real_measured_anchor"),
                "verification_error_pct": r.get("verification_error_pct"),
                "verification_status": r["verification_status"],
                "prediction_id": r["prediction_id"],
            }
        )
    return out


def persist_simulation(sim: dict) -> tuple[Path, Path]:
    SIM_CACHE.parent.mkdir(parents=True, exist_ok=True)
    SIM_CACHE.write_text(json.dumps(sim, indent=2), encoding="utf-8")
    SIM_REPORT.parent.mkdir(parents=True, exist_ok=True)
    summary = {k: v for k, v in sim.items() if k != "records"}
    summary["record_sample"] = (sim.get("records") or [])[:5]
    SIM_REPORT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    ledger = write_independent_prediction_ledger(sim)
    return SIM_CACHE, ledger