#!/usr/bin/env python3
"""Math generator per-rule eval across 1520 formal rules (v1.1)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "math_generator_rules_eval_manifest.yaml"
OUTPUT = ROOT / "data" / "math_generator_rules_eval_benchmark.json"

HEADLINE_CORPORA = [
    "FSOT_OVERLAY",
    "MATHEMATICAL_PHYSICS",
    "THERMODYNAMICS_ENGINEERING",
    "MATERIALS_SCIENCE",
    "SCIENCE_SIDE",
]

SOTA_BASELINES = {
    "schema_pass_rate": {
        "sota_model": "Hand-maintained rule corpus QA",
        "sota_typical_error_pct": 5.0,
        "reference": "Schema completeness for formal rule objects",
    },
    "numeric_eval_median": {
        "sota_model": "Overlay prediction vs Planck/PDG references",
        "sota_typical_error_pct": 2.0,
        "reference": "FO-100..FO-213 numeric overlay literals",
    },
    "live_benchmark_median": {
        "sota_model": "Held-out benchmark_formula recomputation",
        "sota_typical_error_pct": 1.0,
        "reference": "FO-200/210/213 live formula eval benches",
    },
}


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _corpus_slug(corpus: str) -> str:
    return corpus.lower()


def _corpus_decomposition(records: list[dict]) -> dict[str, dict]:
    by_corpus: dict[str, list[dict]] = {}
    for row in records:
        by_corpus.setdefault(row["corpus"], []).append(row)
    out: dict[str, dict] = {}
    for corpus, rows in sorted(by_corpus.items()):
        errs = [float(r["error_pct"]) for r in rows]
        kinds: dict[str, int] = {}
        for row in rows:
            kinds[row["eval_kind"]] = kinds.get(row["eval_kind"], 0) + 1
        out[corpus] = {
            "rule_count": len(rows),
            "median_error_pct": _median(errs),
            "schema_pass_count": sum(1 for r in rows if r.get("schema_valid")),
            "eval_kind_counts": kinds,
        }
    return out


def _eval_kind_decomposition(records: list[dict]) -> dict[str, dict]:
    by_kind: dict[str, list[float]] = {}
    for row in records:
        by_kind.setdefault(row["eval_kind"], []).append(float(row["error_pct"]))
    return {
        kind: {
            "record_count": len(errs),
            "median_error_pct": _median(errs),
            "max_error_pct": max(errs),
            "min_error_pct": min(errs),
        }
        for kind, errs in sorted(by_kind.items())
    }


def _headline_records(
    *,
    pooled_median: float,
    observable_count: int,
    schema_pass_rate: float,
    numeric_eval_median: float | None,
    corpus_decomposition: dict[str, dict],
    eval_kind_decomposition: dict[str, dict],
) -> list[dict]:
    headlines: list[dict] = [
        {
            "lab": "math_generator_rules_eval_lab",
            "property": "pooled_rules_median",
            "name": "all_rules",
            "computed": round(pooled_median, 6),
            "measured": 0.0,
            "error_pct": pooled_median,
            "observable_count": observable_count,
        },
        {
            "lab": "math_generator_rules_eval_lab",
            "property": "schema_pass_rate_pct",
            "name": "schema_completeness",
            "computed": round(schema_pass_rate, 6),
            "measured": 100.0,
            "error_pct": max(0.0, 100.0 - schema_pass_rate),
            "observable_count": observable_count,
        },
    ]
    if numeric_eval_median is not None:
        headlines.append(
            {
                "lab": "math_generator_rules_eval_lab",
                "property": "numeric_eval_median",
                "name": "overlay_numeric_subset",
                "computed": round(numeric_eval_median, 6),
                "measured": 0.0,
                "error_pct": numeric_eval_median,
                "observable_count": int(
                    (eval_kind_decomposition.get("numeric_literal") or {}).get("record_count", 0)
                    + (eval_kind_decomposition.get("live_benchmark") or {}).get("record_count", 0)
                    + (eval_kind_decomposition.get("benchmark_report") or {}).get("record_count", 0)
                    + (eval_kind_decomposition.get("numeric_formula") or {}).get("record_count", 0)
                ),
            }
        )
    live_stats = eval_kind_decomposition.get("live_benchmark") or {}
    if live_stats:
        headlines.append(
            {
                "lab": "math_generator_rules_eval_lab",
                "property": "live_benchmark_median",
                "name": "formula_live_eval",
                "computed": round(float(live_stats.get("median_error_pct") or 0.0), 6),
                "measured": 0.0,
                "error_pct": float(live_stats.get("median_error_pct") or 0.0),
                "observable_count": int(live_stats.get("record_count") or 0),
            }
        )
    for corpus in HEADLINE_CORPORA:
        stats = corpus_decomposition.get(corpus) or {}
        med = float(stats.get("median_error_pct") or 0.0)
        headlines.append(
            {
                "lab": "math_generator_rules_eval_lab",
                "property": f"corpus_median_{_corpus_slug(corpus)}",
                "name": corpus,
                "computed": round(med, 6),
                "measured": 0.0,
                "error_pct": med,
                "observable_count": int(stats.get("rule_count") or 0),
                "corpus": corpus,
            }
        )
    return headlines


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from fsot_paths import math_generator_rules_root, rel_repo_path  # noqa: E402
    from math_generator_rules_eval import evaluate_all_rules  # noqa: E402

    _, authority_path = load_fsot_compute()
    rules_root = math_generator_rules_root()
    material_records, summary = evaluate_all_rules(rules_root)

    all_errs = [float(r["error_pct"]) for r in material_records]
    pooled_median = _median(all_errs)
    corpus_decomposition = _corpus_decomposition(material_records)
    eval_kind_decomposition = _eval_kind_decomposition(material_records)
    schema_pass_rate = float(summary.get("schema_pass_rate_pct") or 0.0)
    numeric_eval_median = summary.get("numeric_eval_median_error_pct")

    headline_records = _headline_records(
        pooled_median=float(pooled_median or 0.0),
        observable_count=len(material_records),
        schema_pass_rate=schema_pass_rate,
        numeric_eval_median=float(numeric_eval_median) if numeric_eval_median is not None else None,
        corpus_decomposition=corpus_decomposition,
        eval_kind_decomposition=eval_kind_decomposition,
    )
    headline_errs = [float(r["error_pct"]) for r in headline_records]
    headline_median = _median(headline_errs)

    beats_sota_summary = {
        "schema_pass_vs_qa_baseline": schema_pass_rate >= 95.0,
        "pooled_rules_vs_corpus_qa": pooled_median is not None and pooled_median < 5.0,
    }
    if numeric_eval_median is not None:
        beats_sota_summary["numeric_eval_vs_overlay_refs"] = float(numeric_eval_median) < 2.0
    live_med = (eval_kind_decomposition.get("live_benchmark") or {}).get("median_error_pct")
    if live_med is not None:
        beats_sota_summary["live_benchmark_vs_formula_eval"] = float(live_med) < 1.0

    schema_fail = sum(1 for r in material_records if not r.get("schema_valid"))
    d_eff = int(spec.get("D_eff") or 17)
    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": rel_repo_path(rules_root),
        "source_repo": spec.get("source_repo", "vendor/math_generator/rules"),
        "maps_to_lean": spec.get("maps_to_lean") or ["particle", "mathematical", "consciousness"],
        "D_eff": d_eff,
        "record_count": len(material_records),
        "observable_count": len(material_records),
        "median_error_pct": pooled_median,
        "headline_median_error_pct": headline_median,
        "pooled_median_error_pct": pooled_median,
        "schema_fail_count": schema_fail,
        "corpus_decomposition": corpus_decomposition,
        "eval_kind_decomposition": eval_kind_decomposition,
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "headline_observables": {
                "pooled_median_error_pct": pooled_median,
                "headline_median_error_pct": headline_median,
                "schema_pass_rate_pct": schema_pass_rate,
                "numeric_eval_median_error_pct": numeric_eval_median,
            },
            "operational_baselines": SOTA_BASELINES,
            "beats_sota_summary": beats_sota_summary,
        },
        **summary,
        "records": headline_records,
        "material_records": material_records,
        "crosswalk_modules": ["FSOT.Formal.MathGeneratorRulesEvalPriors"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  rules: {doc['record_count']}  pooled_median_err: {doc['median_error_pct']}  "
        f"numeric_eval: {doc.get('numeric_eval_count')}  "
        f"schema_fail: {doc['schema_fail_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())