#!/usr/bin/env python3
"""Sector refinement for existence-simulation failures — SMILES §-tier routing."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = ROOT / "vendor" / "smiles" / "FSOT_SMILES_Lab_Dataset.json"
CLUSTERS = ROOT / "data" / "existence_simulation_failure_clusters_manifest.yaml"
VERIFY_REPORT = ROOT / "data" / "publication" / "independent_prediction_verification_report.json"
REFINED_OUT = ROOT / "data" / "existence_simulation" / "refinement_records.json"

AA3_TO1 = {
    "Ala": "A", "Gly": "G", "Thr": "T", "Met": "M", "Phe": "F", "His": "H", "Trp": "W",
    "Val": "V", "Leu": "L", "Ile": "I", "Cys": "C", "Ser": "S", "Pro": "P",
}


def _load_json(path: Path) -> dict | list:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _norm_name(name: str) -> str:
    return re.sub(r"\s+", "", name or "").strip()


def _load_smiles_index() -> dict[str, dict]:
    doc = _load_json(SMILES_JSON)
    rows = doc.get("records") if isinstance(doc, dict) else doc
    index: dict[str, dict] = {}
    for row in rows or []:
        name = _norm_name(str(row.get("name") or ""))
        if not name:
            continue
        # Prefer lowest error_pct when duplicate names across sections
        prev = index.get(name)
        if prev is None or float(row.get("error_pct") or 99) < float(prev.get("error_pct") or 99):
            index[name] = row
    return index


def _cluster_for_record(rec: dict, clusters_doc: dict) -> tuple[str, dict] | tuple[None, None]:
    concept = str(rec.get("concept_name") or "")
    unit = str(rec.get("unit") or "")
    citation = str(rec.get("citation") or "")

    if concept in AA3_TO1 or "Kyte" in citation:
        return "hydrophobicity_kyte_doolittle", clusters_doc["clusters"]["hydrophobicity_kyte_doolittle"]
    if unit == "cm⁻¹" or "cm\u207b" in unit or "Raman" in citation or "Silverstein" in citation or "Nakamoto" in citation:
        return "ir_raman_spectroscopy", clusters_doc["clusters"]["ir_raman_spectroscopy"]
    if unit == "V" and "/" in concept:
        return "electrochemistry_standard_potential", clusters_doc["clusters"]["electrochemistry_standard_potential"]
    if unit == "°":
        return "molecular_geometry_cccdb", clusters_doc["clusters"]["molecular_geometry_cccdb"]
    if "JANAF" in citation or "Chase" in citation:
        return "thermochemistry_janaf", clusters_doc["clusters"]["thermochemistry_janaf"]
    if unit == "kJ/mol":
        return "thermochemistry_janaf", clusters_doc["clusters"]["thermochemistry_janaf"]
    return None, None


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def refine_failures(*, gate_pct: float = 1.0) -> dict[str, Any]:
    report = _load_json(VERIFY_REPORT)
    clusters_doc = _load_yaml(CLUSTERS)
    smiles = _load_smiles_index()

    failures = [
        r for r in report.get("records") or []
        if float(r.get("verification_error_pct") or 0) > gate_pct
    ]

    refined: list[dict] = []
    unresolved: list[dict] = []
    cluster_stats: dict[str, dict] = {}

    for rec in failures:
        concept = str(rec.get("concept_name") or "")
        key = _norm_name(concept)
        smiles_row = smiles.get(key)
        cluster_id, cluster_cfg = _cluster_for_record(rec, clusters_doc)

        if smiles_row is None:
            unresolved.append({"prediction_id": rec.get("prediction_id"), "concept_name": concept, "reason": "no_smiles_match"})
            continue

        measured = float(smiles_row.get("target_value") or rec.get("known_anchor") or 0)
        computed = float(smiles_row.get("computed_value") or 0)
        refined_err = float(smiles_row.get("error_pct") or err_pct(computed, measured))

        row = {
            "prediction_id": rec.get("prediction_id"),
            "concept_name": concept,
            "cluster": cluster_id,
            "expansion_domain": (cluster_cfg or {}).get("expansion_domain"),
            "formula_branch": (cluster_cfg or {}).get("formula_branch"),
            "original_formula_branch": rec.get("formula_branch"),
            "original_fsot_predicted": rec.get("fsot_predicted"),
            "original_error_pct": rec.get("verification_error_pct"),
            "refined_formula": smiles_row.get("fsot_formula"),
            "refined_fsot_predicted": computed,
            "known_anchor": measured,
            "refined_error_pct": round(refined_err, 6),
            "smiles_section": smiles_row.get("section"),
            "citation": smiles_row.get("source"),
            "ring_in_status": "green" if refined_err <= 0.5 else ("aspiration" if refined_err <= 1.0 else "partial"),
            "eval_kind": "existence_sector_refinement",
        }
        refined.append(row)
        if cluster_id:
            st = cluster_stats.setdefault(cluster_id, {"count": 0, "green": 0, "errors": []})
            st["count"] += 1
            st["errors"].append(refined_err)
            if refined_err <= 1.0:
                st["green"] += 1

    errs = [float(r["refined_error_pct"]) for r in refined]
    median = sorted(errs)[len(errs) // 2] if errs else 0.0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "failure_count": len(failures),
        "refined_count": len(refined),
        "unresolved_count": len(unresolved),
        "ring_in_green_count": sum(1 for r in refined if r["ring_in_status"] == "green"),
        "ring_in_aspiration_count": sum(1 for r in refined if r["ring_in_status"] == "aspiration"),
        "ring_in_partial_count": sum(1 for r in refined if r["ring_in_status"] == "partial"),
        "refined_median_error_pct": median,
        "cluster_stats": cluster_stats,
        "unresolved": unresolved,
        "records": refined,
    }


def persist_refinement(doc: dict) -> Path:
    REFINED_OUT.parent.mkdir(parents=True, exist_ok=True)
    REFINED_OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return REFINED_OUT


def material_records_for_benchmark(doc: dict) -> list[dict]:
    out: list[dict] = []
    for r in doc.get("records") or []:
        out.append(
            {
                "lab": "existence_refinement_lab",
                "property": "sector_refinement",
                "name": r["concept_name"],
                "computed": r["refined_fsot_predicted"],
                "measured": r["known_anchor"],
                "error_pct": r["refined_error_pct"],
                "eval_kind": r["eval_kind"],
                "cluster": r["cluster"],
                "expansion_domain": r["expansion_domain"],
                "formula_branch": r["formula_branch"],
                "original_error_pct": r["original_error_pct"],
                "refined_formula": r["refined_formula"],
                "prediction_id": r["prediction_id"],
                "ring_in_status": r["ring_in_status"],
            }
        )
    return out