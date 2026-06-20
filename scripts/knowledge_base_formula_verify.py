"""Knowledge Base formula verification — per-formula KB pass + strict-empirical bridge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from formula_corpus import load_strict_empirical_jsonl, summarize_formula_corpus

ROOT = Path(__file__).resolve().parents[1]
STRICT_EMPIRICAL_PATH = Path(
    r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\by_domain\strict_empirical.jsonl"
)
KB_SUMMARY_PATH = ROOT / "data" / "knowledge_base_formula_verification_summary.json"
KB_VALIDATION_PATH = Path(
    r"C:\Users\damia\Desktop\Knowledge base\export\full_corpus_math_validation.json"
)


def summarize_kb_per_formula(validation_path: Path = KB_VALIDATION_PATH) -> dict[str, Any]:
    if not validation_path.exists():
        return {}
    data = json.loads(validation_path.read_text(encoding="utf-8"))
    summary = data.get("summary") or {}
    rows = data.get("rows") or []
    within_2 = sum(
        1 for r in rows if r.get("error_pct") is not None and float(r["error_pct"]) <= 2.0
    )
    within_5 = sum(
        1 for r in rows if r.get("error_pct") is not None and float(r["error_pct"]) <= 5.0
    )
    return {
        "per_formula_total": summary.get("total_formulas", len(rows)),
        "per_formula_with_target": summary.get("with_target", 0),
        "per_formula_evaluated": summary.get("evaluated", 0),
        "per_formula_verified": summary.get("verified", 0),
        "per_formula_tolerable": summary.get("tolerable", 0),
        "per_formula_unacceptable": summary.get("unacceptable", 0),
        "per_formula_within_target_2pct": within_2,
        "per_formula_within_tolerable_5pct": within_5,
        "per_formula_unparseable": summary.get("unparseable", 0),
        "per_formula_validation_path": str(validation_path),
    }


def summarize_knowledge_base_formulas(
    transfer: dict[str, Any],
    strict_path: Path = STRICT_EMPIRICAL_PATH,
    kb_summary_path: Path = KB_SUMMARY_PATH,
) -> dict[str, Any]:
    catalog = transfer.get("catalog_formulas") or []
    strict_summary = (
        summarize_formula_corpus(load_strict_empirical_jsonl(strict_path))
        if strict_path.exists()
        else {}
    )
    per_formula = summarize_kb_per_formula()
    if kb_summary_path.exists():
        cached = json.loads(kb_summary_path.read_text(encoding="utf-8"))
        kb_cat = cached.get("kb_catalog") or {}
        per_formula = {
            **per_formula,
            "per_formula_total": kb_cat.get("catalog_formulas_total", per_formula.get("per_formula_total")),
            "per_formula_evaluated": kb_cat.get("evaluated", per_formula.get("per_formula_evaluated")),
            "per_formula_verified": kb_cat.get("verified_status_count", per_formula.get("per_formula_verified")),
            "per_formula_within_target_2pct": kb_cat.get("within_target_2pct", per_formula.get("per_formula_within_target_2pct")),
            "per_formula_within_tolerable_5pct": kb_cat.get("within_tolerable_5pct", per_formula.get("per_formula_within_tolerable_5pct")),
        }

    return {
        "catalog_formulas_total": len(catalog),
        "observable_citations": len(transfer.get("observable_formula_citations") or []),
        "observable_verified_formulas": strict_summary.get("records_total", 0),
        "observable_verified_matched": strict_summary.get("matched_count", 0),
        "within_target_2pct": strict_summary.get("within_target_2pct", 0),
        "within_tolerable_5pct": strict_summary.get("within_tolerable_5pct", 0),
        "strict_empirical_corpus_path": str(strict_path),
        **per_formula,
    }