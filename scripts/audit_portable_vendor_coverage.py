#!/usr/bin/env python3
"""Audit portable vendor coverage for extension domains and bundled assets."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "portable_vendor_coverage_audit.json"
EXTENSION_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
EXTERNAL_MANIFEST = ROOT / "data" / "external_data_manifest.yaml"


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def audit() -> dict:
    ext = _load_yaml(EXTENSION_MANIFEST).get("extension_domains") or {}
    bundled = (_load_yaml(EXTERNAL_MANIFEST).get("bundled") or {}) if EXTERNAL_MANIFEST.exists() else {}

    domain_rows: list[dict] = []
    missing_benchmarks: list[str] = []
    for name, cfg in ext.items():
        bench_rel = cfg.get("benchmark_data")
        bench_path = ROOT / bench_rel if bench_rel else None
        bench_ok = bench_path.exists() if bench_path else False
        if bench_rel and not bench_ok:
            missing_benchmarks.append(name)
        domain_rows.append(
            {
                "domain": name,
                "tier": cfg.get("tier"),
                "benchmark_data": bench_rel,
                "benchmark_present": bench_ok,
                "build_script": cfg.get("build_script"),
                "lean_module": cfg.get("lean_module"),
            }
        )

    bundled_rows: list[dict] = []
    missing_vendor: list[str] = []
    for key, cfg in bundled.items():
        rel = cfg.get("path")
        path = ROOT / rel if rel else None
        present = path.exists() if path else False
        if rel and not present:
            missing_vendor.append(key)
        bundled_rows.append({"asset": key, "path": rel, "present": present})

    formula_corpus = ROOT / "vendor" / "formula_corpus" / "by_domain" / "strict_empirical.jsonl"
    precision_candidates: list[dict] = []
    for row in domain_rows:
        bench_path = ROOT / row["benchmark_data"] if row.get("benchmark_data") else None
        if not bench_path or not bench_path.exists():
            continue
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        med = bench.get("median_error_pct")
        if med is not None and float(med) > 1.0:
            precision_candidates.append(
                {
                    "domain": row["domain"],
                    "median_error_pct": med,
                    "record_count": bench.get("record_count"),
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "extension_domain_count": len(domain_rows),
        "bundled_asset_count": len(bundled_rows),
        "formula_corpus_portable": formula_corpus.exists(),
        "formula_corpus_records_hint": 7941 if formula_corpus.exists() else 0,
        "missing_benchmark_domains": missing_benchmarks,
        "missing_bundled_assets": missing_vendor,
        "precision_tightening_candidates": sorted(
            precision_candidates, key=lambda r: float(r["median_error_pct"]), reverse=True
        ),
        "all_extension_benchmarks_present": len(missing_benchmarks) == 0,
        "all_bundled_assets_present": len(missing_vendor) == 0,
        "domains": domain_rows,
        "bundled_assets": bundled_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = audit()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  extension domains: {doc['extension_domain_count']}")
    print(f"  formula corpus portable: {doc['formula_corpus_portable']}")
    print(f"  missing benchmarks: {len(doc['missing_benchmark_domains'])}")
    print(f"  missing bundled: {len(doc['missing_bundled_assets'])}")
    print(f"  precision candidates (>1% median): {len(doc['precision_tightening_candidates'])}")
    critical_ok = doc["all_extension_benchmarks_present"] and doc["formula_corpus_portable"]
    return 0 if critical_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())