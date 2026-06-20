"""Knowledge Base formula verification — catalog inventory + strict-empirical corpus bridge."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from formula_corpus import load_strict_empirical_jsonl, summarize_formula_corpus

STRICT_EMPIRICAL_PATH = Path(
    r"C:\Users\damia\Desktop\fsot code language\audits\reports\FSOT_UNIFIED_DATABASE\by_domain\strict_empirical.jsonl"
)


def summarize_knowledge_base_formulas(
    transfer: dict[str, Any],
    strict_path: Path = STRICT_EMPIRICAL_PATH,
) -> dict[str, Any]:
    """KB catalog is source inventory; observable verification lives in strict_empirical corpus."""
    catalog = transfer.get("catalog_formulas") or []
    strict_summary = (
        summarize_formula_corpus(load_strict_empirical_jsonl(strict_path))
        if strict_path.exists()
        else {}
    )
    return {
        "catalog_formulas_total": len(catalog),
        "observable_citations": len(transfer.get("observable_formula_citations") or []),
        "observable_verified_formulas": strict_summary.get("records_total", 0),
        "observable_verified_matched": strict_summary.get("matched_count", 0),
        "within_target_2pct": strict_summary.get("within_target_2pct", 0),
        "within_tolerable_5pct": strict_summary.get("within_tolerable_5pct", 0),
        "strict_empirical_corpus_path": str(strict_path),
    }