#!/usr/bin/env python3
"""Map scientific domain coverage, accuracy tiers, and expansion opportunities."""

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
OUTPUT_JSON = ROOT / "data" / "scientific_domain_expansion_map.json"
OUTPUT_YAML = ROOT / "data" / "scientific_domain_expansion_map.yaml"

# Candidate domains beyond current 35 + 4 extensions (FSOT 2.0 expansion arc)
EXPANSION_CANDIDATES = [
    {"id": "Geochemistry", "rationale": "SMILES + planetary lab overlap; no dedicated observables", "priority": "high"},
    {"id": "Pharmacology", "rationale": "Medical/immunology bridge; drug-target strict empirical thin", "priority": "high"},
    {"id": "Oncology", "rationale": "Biology strict + immunology extension; tumor marker benchmarks", "priority": "medium"},
    {"id": "Space_Weather", "rationale": "Plasma + climate coupling; NOAA SWPC data ingest", "priority": "high"},
    {"id": "Hydrology", "rationale": "Climate NCEI scale-up; streamflow/USGS chunked ingest", "priority": "medium"},
    {"id": "Cryosphere", "rationale": "Climate + geophysics; ice-core / GRACE proxies", "priority": "medium"},
    {"id": "Neuroimmunology", "rationale": "Immunology + neuron cohort cross-domain", "priority": "medium"},
    {"id": "Synthetic_Biology", "rationale": "Biology strict + evolution operons; iGEM benchmarks", "priority": "medium"},
    {"id": "Quantum_Materials", "rationale": "Condensed matter SMILES depth; dedicated lab thin", "priority": "low"},
    {"id": "Econometrics", "rationale": "Economics uses linguistics proxy only", "priority": "low"},
]


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _tier(median: float | None, records: int) -> str:
    if median is None or records == 0:
        return "unverified"
    if median <= 2.0 and records >= 100:
        return "A_strong"
    if median <= 5.0 and records >= 20:
        return "B_verified"
    if median <= 5.0:
        return "C_thin"
    return "D_needs_work"


def build_map() -> dict:
    coverage = _load(ROOT / "data" / "domain_coverage_report.json")
    precision = _load(ROOT / "data" / "domain_precision_report.json")
    extension = {}
    ext_path = ROOT / "data" / "extension_domains_manifest.yaml"
    if yaml and ext_path.exists():
        extension = yaml.safe_load(ext_path.read_text(encoding="utf-8"))

    prec_by_name = {d["neurolab_domain"]: d for d in (precision.get("domains") or [])}

    neurolab_domains = []
    tier_counts = {"A_strong": 0, "B_verified": 0, "C_thin": 0, "D_needs_work": 0, "unverified": 0}
    weak_accuracy = []
    thin_empirical = []
    sign_dispersal = []

    for dom in coverage.get("domains") or []:
        name = dom["neurolab_domain"]
        prec = prec_by_name.get(name, {})
        med = prec.get("median_error_pct")
        rec = int(prec.get("record_count") or dom.get("empirical_records") or 0)
        tier = _tier(med, rec)
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        entry = {
            "domain": name,
            "lean_domain": dom.get("lean_domain"),
            "empirical_records": rec,
            "median_error_pct": med,
            "precision_status": prec.get("precision_status"),
            "sign_mismatch": prec.get("sign_mismatch", False),
            "authority_scalar_negative": dom.get("domain_scalar_S", 0) < 0 if dom.get("domain_scalar_S") is not None else None,
            "coverage_tier": tier,
            "labs": [s.get("lab") for s in (dom.get("empirical_sources") or [])],
        }
        neurolab_domains.append(entry)
        if tier in ("C_thin", "D_needs_work"):
            weak_accuracy.append(name)
        if rec < 50:
            thin_empirical.append(name)
        if entry.get("sign_mismatch") or (
            entry.get("authority_scalar_negative") and dom.get("observed")
        ):
            sign_dispersal.append(name)

    extensions = []
    for name, cfg in (extension.get("extension_domains") or {}).items():
        bench_path = ROOT / cfg["benchmark_data"]
        bench = _load(bench_path)
        n = int(bench.get("record_count") or bench.get("month_count") or 0)
        med = bench.get("median_error_pct")
        extensions.append(
            {
                "domain": name,
                "tier": cfg.get("tier"),
                "record_count": n,
                "median_error_pct": med,
                "coverage_tier": _tier(med, n),
                "lean_module": cfg.get("lean_module"),
            }
        )

    climate_bench = _load(ROOT / "data" / "climate_observed_benchmark.json")
    bio_strict = _load(ROOT / "data" / "biology_strict_empirical.json")
    neuron_th = _load(ROOT / "data" / "neuron_cohort_train_holdout.json")
    fic = _load(ROOT / "data" / "fic_sensitivity_report.json")

    intelligence_compression = None
    if fic:
        intelligence_compression = {
            "domain": "Intelligence_Compression",
            "record_count": int(fic.get("sweep_row_count") or fic.get("row_count") or 0),
            "median_error_pct": fic.get("optimal_median_error_pct"),
            "coverage_tier": _tier(fic.get("optimal_median_error_pct"), int(fic.get("sweep_row_count") or 0)),
            "lean_module": "FSOT.Formal.IntelligenceCompressionPriors",
        }

    total_covered = len(neurolab_domains) + len(extensions) + (1 if intelligence_compression else 0)
    total_records = int(coverage.get("total_empirical_records") or 0)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "neurolab_domains": len(neurolab_domains),
            "extension_domains": len(extensions),
            "total_scientific_domains_covered": total_covered,
            "total_empirical_records": total_records,
            "domains_target_band_2pct": precision.get("domains_target_band_2pct"),
            "domains_sign_mismatch": precision.get("domains_sign_mismatch"),
            "tier_distribution": tier_counts,
            "lean_formal_modules": len(list((ROOT / "FSOT" / "Formal").glob("*.lean"))),
        },
        "neurolab_domains": sorted(neurolab_domains, key=lambda x: x["domain"]),
        "extension_domains": extensions,
        "intelligence_compression": intelligence_compression,
        "specialized_bridges": {
            "biology_strict_ncbi": {
                "strict_records": bio_strict.get("strict_record_count"),
                "median_error_pct": bio_strict.get("strict_median_error_pct"),
            },
            "climate_ncei_cohort": climate_bench.get("cohort"),
            "neuron_train_holdout": {
                "train_cells": (neuron_th.get("train") or {}).get("cell_count"),
                "holdout_cells": (neuron_th.get("holdout") or {}).get("cell_count"),
                "gates_pass": (neuron_th.get("gates") or {}).get("all_pass"),
            },
        },
        "accuracy_weak_spots": sorted(set(weak_accuracy)),
        "thin_empirical_coverage": sorted(set(thin_empirical)),
        "authority_dispersal_domains": sorted(set(sign_dispersal)),
        "expansion_candidates": EXPANSION_CANDIDATES,
        "recommended_next_waves": [
            "Scale climate to 20 stations × 40 years with holdout station gates (in progress)",
            "Expand Plasma_Physics beyond 6 records (fusion lab + NIST plasma tables)",
            "Wire Space_Weather as domain #40 (NOAA SWPC Kp/Ap chunked ingest)",
            "Multi-hero neuron certification (3–5 specimens per Allen class)",
            "Pharmacology strict-empirical (ChEMBL / DrugBank property bridge)",
            "Hydrology USGS streamflow chunked ingest (climate cohort pattern)",
        ],
    }


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-yaml", type=Path, default=OUTPUT_YAML)
    args = parser.parse_args()
    doc = build_map()
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    args.output_yaml.write_text(yaml.dump(doc, sort_keys=False, default_flow_style=False), encoding="utf-8")
    s = doc["summary"]
    print(f"Wrote {args.output_json}")
    print(f"Wrote {args.output_yaml}")
    print(f"  covered: {s['total_scientific_domains_covered']} domains  records: {s['total_empirical_records']}")
    print(f"  tiers: {s['tier_distribution']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())