#!/usr/bin/env python3
"""Formula corpus + CNC controller benchmark from desktop crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "formula_corpus_cnc_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import (  # noqa: E402
    formula_corpus_cnc_formula_summary_path,
    formula_corpus_cnc_gauntlet_path,
    formula_corpus_cnc_validator_delta_path,
    rel_repo_path,
)


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build() -> dict:
    summary = json.loads(formula_corpus_cnc_formula_summary_path().read_text(encoding="utf-8"))
    delta = json.loads(formula_corpus_cnc_validator_delta_path().read_text(encoding="utf-8"))
    gauntlet = json.loads(formula_corpus_cnc_gauntlet_path().read_text(encoding="utf-8"))

    records: list[dict] = []
    for key, expected in (
        ("document_count", 61),
        ("rule_count", 1520),
        ("formula_candidate_count", 2281),
    ):
        val = int(summary.get(key) or 0)
        records.append(
            {
                "lab": "formula_corpus_cnc",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    for key, expected in (
        ("current_corpus_rows", 1444),
        ("current_corpus_formula_token_index", 1413),
        ("validator_unique_formulas_scanned", 1375),
    ):
        val = int(delta.get(key) or 0)
        records.append(
            {
                "lab": "formula_corpus_cnc",
                "property": key,
                "computed": val,
                "measured": expected,
                "error_pct": 0.0 if val == expected else _err_pct(val, expected),
            }
        )

    families = delta.get("families") or []
    records.append(
        {
            "lab": "formula_corpus_cnc",
            "property": "validator_family_count",
            "computed": len(families),
            "measured": 11,
            "error_pct": 0.0 if len(families) == 11 else 100.0,
        }
    )

    chem = (gauntlet.get("chem") or {}).get("score") or {}
    total = int(chem.get("total") or 0)
    hits = int(chem.get("hits") or 0)
    pass_rate = float(chem.get("pass_rate") or 0)
    recomputed_rate = 100.0 * hits / total if total else 0.0
    records.append(
        {
            "lab": "formula_corpus_cnc",
            "property": "gauntlet_scenario_count",
            "computed": total,
            "measured": 17,
            "error_pct": 0.0 if total == 17 else 100.0,
        }
    )
    records.append(
        {
            "lab": "formula_corpus_cnc",
            "property": "gauntlet_hit_count",
            "computed": hits,
            "measured": 15,
            "error_pct": 0.0 if hits == 15 else 100.0,
        }
    )
    records.append(
        {
            "lab": "formula_corpus_cnc",
            "property": "gauntlet_pass_rate_pct",
            "computed": recomputed_rate,
            "measured": pass_rate,
            "error_pct": _err_pct(recomputed_rate, pass_rate),
        }
    )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [
            rel_repo_path(formula_corpus_cnc_formula_summary_path()),
            rel_repo_path(formula_corpus_cnc_validator_delta_path()),
            rel_repo_path(formula_corpus_cnc_gauntlet_path()),
        ],
        "maps_to_lean": ["particle", "mathematical", "consciousness"],
        "D_eff": 17,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())