#!/usr/bin/env python3
"""Verify existence-simulation predictions against known data not in benchmark panels."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from existence_simulation_lib import (  # noqa: E402
    collect_benchmark_coverage,
    err_pct,
    fsot_independent_prediction,
)
from math_formula_eval import core_context, evaluate_formula  # noqa: E402

STRICT = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"
SIM_CACHE = ROOT / "data" / "existence_simulation" / "gap_fill_records.json"
OUT = ROOT / "data" / "publication" / "independent_prediction_verification_report.json"

GREEN_GATE = 0.5
ASPIRATION_GATE = 1.0

# NIST ASD first-ionization energies (eV) — independent of corpus CSV anchors.
NIST_ASD_IE_EV: dict[str, float] = {
    "H": 13.59843449,
    "He": 24.587387011,
    "Li": 5.391719266,
    "Be": 9.322699,
    "B": 8.298019,
    "C": 11.260288,
    "N": 14.53413,
    "O": 13.618055,
    "F": 17.42282,
    "Ne": 21.564548,
    "Na": 5.13907696,
    "Mg": 7.646236,
    "Al": 5.985769,
    "Si": 8.15168,
    "P": 10.48669,
    "S": 10.36001,
    "Cl": 12.967633,
    "Ar": 15.7596119,
    "K": 4.3406637,
    "Ca": 6.1131555,
    "Sc": 6.56149,
    "Ti": 6.82812,
    "V": 6.74619,
    "Cr": 6.76651,
    "Mn": 7.434038,
    "Fe": 7.9024681,
    "Co": 7.88101,
    "Ni": 7.639878,
    "Cu": 7.72638,
    "Zn": 9.394197,
    "Ga": 5.999302,
    "Ge": 7.8994,
    "As": 9.7886,
    "Se": 9.75238,
    "Br": 11.81381,
    "Kr": 13.999605,
    "Rb": 4.177128,
    "Sr": 5.694867,
    "Y": 6.21726,
    "Zr": 6.63312,
    "Nb": 6.75885,
    "Mo": 7.09243,
    "Tc": 7.28,
    "Ru": 7.3605,
    "Rh": 7.45885,
    "Pd": 8.3369,
    "Ag": 7.57592,
    "Cd": 8.99382,
    "In": 5.78636,
    "Sn": 7.34312,
    "Sb": 8.60839,
    "Te": 9.009808,
    "I": 10.45126,
    "Xe": 12.12987,
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    return s[len(s) // 2]


def _load_corpus_by_concept() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not STRICT.is_file():
        return out
    with STRICT.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            concept = str(row.get("concept_name") or "").strip()
            if concept:
                out[concept] = row
    return out


def _tier(error: float | None) -> str:
    if error is None:
        return "no_anchor"
    if error <= GREEN_GATE:
        return "green"
    if error <= ASPIRATION_GATE:
        return "aspiration"
    return "fail"


def _external_known_value(concept: str, unit: str, corpus_row: dict) -> tuple[float | None, str | None]:
    """Return independent external anchor when available."""
    if unit == "eV" and concept in NIST_ASD_IE_EV:
        return NIST_ASD_IE_EV[concept], "NIST_ASD_first_ionization"
    citation = str(corpus_row.get("verification_citations") or "")
    if "NIST" in citation and unit == "eV" and re.fullmatch(r"[A-Z][a-z]?", concept):
        return NIST_ASD_IE_EV.get(concept), "NIST_ASD_first_ionization"
    return None, None


def _recompute_fsot(corpus_row: dict) -> tuple[float | None, str]:
    concept = str(corpus_row.get("concept_name") or "")
    formula = corpus_row.get("formula_publication") or corpus_row.get("formula_canonical")
    return fsot_independent_prediction(
        concept=concept,
        formula=str(formula) if formula else None,
        domain="Chemistry",
        outcome=corpus_row.get("outcome"),
    )


def verify() -> dict:
    sim = _load_json(SIM_CACHE)
    corpus = _load_corpus_by_concept()
    covered = collect_benchmark_coverage()
    records_in: list[dict] = list(sim.get("records") or [])

    results: list[dict] = []
    for rec in records_in:
        concept = str(rec.get("concept_name") or "")
        corpus_row = corpus.get(concept, {})
        in_panel = concept.lower() in covered

        known_anchor = rec.get("real_measured_anchor")
        if known_anchor is None and corpus_row:
            try:
                known_anchor = float(
                    corpus_row.get("target_quantity")
                    or (corpus_row.get("outcome") or {}).get("target_value")
                    or 0
                )
            except (TypeError, ValueError):
                known_anchor = None

        recomputed, re_src = _recompute_fsot(corpus_row) if corpus_row else (None, "missing_corpus")
        fsot_pred = float(rec.get("fsot_predicted") or recomputed or 0)
        recompute_delta = (
            abs(fsot_pred - float(recomputed)) if recomputed is not None else None
        )

        verify_err = (
            err_pct(fsot_pred, float(known_anchor))
            if known_anchor is not None
            else None
        )

        ext_val, ext_src = _external_known_value(
            concept, str(rec.get("unit") or ""), corpus_row
        )
        external_err = err_pct(fsot_pred, ext_val) if ext_val is not None else None

        results.append(
            {
                "prediction_id": rec.get("prediction_id"),
                "concept_name": concept,
                "domain": rec.get("domain"),
                "unit": rec.get("unit"),
                "formula_branch": rec.get("formula_branch"),
                "fsot_predicted": fsot_pred,
                "fsot_prediction_source": rec.get("fsot_prediction_source"),
                "recomputed_fsot": recomputed,
                "recompute_source": re_src,
                "recompute_match": recompute_delta is not None and recompute_delta < 1e-4,
                "known_anchor": known_anchor,
                "verification_error_pct": round(verify_err, 6) if verify_err is not None else None,
                "accuracy_tier": _tier(verify_err),
                "external_anchor": ext_val,
                "external_source": ext_src,
                "external_error_pct": round(external_err, 6) if external_err is not None else None,
                "external_tier": _tier(external_err),
                "in_benchmark_panel": in_panel,
                "citation": corpus_row.get("verification_citations"),
                "citation_grade": corpus_row.get("citation_grade"),
                "not_previously_benchmarked": not in_panel,
            }
        )

    verify_errs = [r["verification_error_pct"] for r in results if r["verification_error_pct"] is not None]
    ext_errs = [r["external_error_pct"] for r in results if r["external_error_pct"] is not None]
    tier_counts = Counter(r["accuracy_tier"] for r in results)
    ext_tier_counts = Counter(r["external_tier"] for r in results if r["external_error_pct"] is not None)
    citation_groups: dict[str, list[float]] = defaultdict(list)
    for r in results:
        cite = str(r.get("citation") or "unknown")[:60]
        if r["verification_error_pct"] is not None:
            citation_groups[cite].append(r["verification_error_pct"])

    by_citation = [
        {
            "citation": k,
            "count": len(v),
            "median_error_pct": _median(v),
            "green_count": sum(1 for e in v if e <= GREEN_GATE),
        }
        for k, v in sorted(citation_groups.items(), key=lambda x: -len(x[1]))
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prediction_count": len(results),
        "not_in_benchmark_panel": sum(1 for r in results if r["not_previously_benchmarked"]),
        "with_known_anchor": len(verify_errs),
        "accuracy_summary": {
            "median_error_pct": _median(verify_errs),
            "mean_error_pct": sum(verify_errs) / len(verify_errs) if verify_errs else None,
            "green_gate_0_5pct": sum(1 for e in verify_errs if e <= GREEN_GATE),
            "aspiration_gate_1pct": sum(1 for e in verify_errs if e <= ASPIRATION_GATE),
            "fail_above_1pct": sum(1 for e in verify_errs if e > ASPIRATION_GATE),
            "tier_counts": dict(tier_counts),
        },
        "external_nist_summary": {
            "nist_crosscheck_count": len(ext_errs),
            "median_error_pct": _median(ext_errs) if ext_errs else None,
            "tier_counts": dict(ext_tier_counts),
        },
        "by_citation_source": by_citation,
        "best_predictions": sorted(
            [r for r in results if r["verification_error_pct"] is not None],
            key=lambda x: x["verification_error_pct"],
        )[:10],
        "worst_predictions": sorted(
            [r for r in results if r["verification_error_pct"] is not None],
            key=lambda x: -x["verification_error_pct"],
        )[:10],
        "records": results,
    }


def _update_ledger_status(report: dict) -> None:
    try:
        import yaml
    except ImportError:
        return
    ledger_path = ROOT / "data" / "publication" / "independent_prediction_ledger.yaml"
    if not ledger_path.is_file():
        return
    ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
    by_id = {r["prediction_id"]: r for r in report.get("records") or []}
    for pred in ledger.get("predictions") or []:
        row = by_id.get(pred.get("id"))
        if not row:
            continue
        tier = row.get("accuracy_tier")
        if tier == "green":
            pred["verification_status"] = "verified_green"
        elif tier == "aspiration":
            pred["verification_status"] = "verified_aspiration"
        elif tier == "fail":
            pred["verification_status"] = "verified_fail"
        pred["verification_error_pct"] = row.get("verification_error_pct")
        pred["known_anchor"] = row.get("known_anchor")
        pred["citation"] = row.get("citation")
    ledger["verification_audit"] = {
        "audited_at": report["generated_at"],
        "median_error_pct": report["accuracy_summary"]["median_error_pct"],
        "green_count": report["accuracy_summary"]["green_gate_0_5pct"],
        "report": str(OUT).replace("\\", "/"),
    }
    ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _combined_post_refinement(report: dict) -> dict:
    refined_path = ROOT / "data" / "existence_simulation" / "refinement_records.json"
    if not refined_path.is_file():
        return {}
    refined = _load_json(refined_path)
    by_id = {r["prediction_id"]: r for r in refined.get("records") or []}
    combined_errs: list[float] = []
    for rec in report.get("records") or []:
        pid = rec.get("prediction_id")
        if pid in by_id:
            combined_errs.append(float(by_id[pid]["refined_error_pct"]))
        elif rec.get("verification_error_pct") is not None:
            combined_errs.append(float(rec["verification_error_pct"]))
    if not combined_errs:
        return {}
    s = sorted(combined_errs)
    return {
        "combined_median_error_pct": s[len(s) // 2],
        "combined_green_0_5pct": sum(1 for e in combined_errs if e <= GREEN_GATE),
        "combined_aspiration_1pct": sum(1 for e in combined_errs if e <= ASPIRATION_GATE),
        "combined_fail_above_1pct": sum(1 for e in combined_errs if e > ASPIRATION_GATE),
        "refined_override_count": len(by_id),
    }


def main() -> int:
    report = verify()
    report["post_refinement"] = _combined_post_refinement(report)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    _update_ledger_status(report)

    acc = report["accuracy_summary"]
    ext = report["external_nist_summary"]
    print(f"Verified {report['prediction_count']} independent predictions")
    print(f"  Not in any benchmark panel: {report['not_in_benchmark_panel']}/{report['prediction_count']}")
    print(f"  Known-data median error: {acc['median_error_pct']:.4f}%")
    print(f"  Green (<=0.5%): {acc['green_gate_0_5pct']}/{report['with_known_anchor']}")
    print(f"  Aspiration (<=1%): {acc['aspiration_gate_1pct']}/{report['with_known_anchor']}")
    print(f"  Fail (>1%): {acc['fail_above_1pct']}/{report['with_known_anchor']}")
    if ext["nist_crosscheck_count"]:
        print(f"  NIST ASD independent cross-checks: {ext['nist_crosscheck_count']}")
        print(f"  NIST median error: {ext['median_error_pct']:.4f}%")
    print("\nTop hits:")
    for r in report["best_predictions"][:5]:
        print(
            f"  {r['prediction_id']} {r['concept_name']}: "
            f"{r['verification_error_pct']}% ({r.get('citation', '')[:40]})"
        )
    print("\nMisses (>1%):")
    for r in report["worst_predictions"]:
        if (r["verification_error_pct"] or 0) <= ASPIRATION_GATE:
            continue
        print(
            f"  {r['prediction_id']} {r['concept_name']}: "
            f"{r['verification_error_pct']}% pred={r['fsot_predicted']} known={r['known_anchor']}"
        )
    post = report.get("post_refinement") or {}
    if post:
        print("\nPost ring-in (80 predictions, failures sector-refined):")
        print(f"  Combined median error: {post['combined_median_error_pct']:.4f}%")
        print(f"  Green (<=0.5%): {post['combined_green_0_5pct']}/80")
        print(f"  Aspiration (<=1%): {post['combined_aspiration_1pct']}/80")
        print(f"  Fail (>1%): {post['combined_fail_above_1pct']}/80")
    print(f"\nWrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())