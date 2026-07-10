#!/usr/bin/env python3
"""Oncology — SMILES drug/enzyme affinity + biology strict operon bridge (v1.1)."""

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
MANIFEST = ROOT / "data" / "oncology_manifest.yaml"
BIO_STRICT = ROOT / "data" / "biology_strict_empirical.json"
OUTPUT = ROOT / "data" / "oncology_benchmark.json"

ONCOLOGY_SECTIONS = {
    "\u00a723 Drug pKd",
    "\u00a765 Enzyme pKi",
    "\u00a724 Enzyme kcat",
    "\u00a735 Michaelis Km",
    "\u00a721 Protein \u0394G",
}

HEADLINE_SECTIONS = [
    "\u00a723 Drug pKd",
    "\u00a765 Enzyme pKi",
    "\u00a724 Enzyme kcat",
]

SOTA_SECTION_BASELINES = {
    "\u00a723 Drug pKd": {
        "sota_model": "ChEMBL target affinity QSAR",
        "sota_typical_error_pct": 12.0,
        "reference": "Oncology drug-target panels",
    },
    "\u00a765 Enzyme pKi": {
        "sota_model": "FEP+ kinase pKi fits",
        "sota_typical_error_pct": 15.0,
        "reference": "PDBbind oncology kinase set",
    },
    "\u00a724 Enzyme kcat": {
        "sota_model": "Michaelis-Menten empirical kcat regressions",
        "sota_typical_error_pct": 10.0,
        "reference": "BRENDA enzyme kinetics",
    },
}


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _section_slug(section: str) -> str:
    return (
        section.replace("\u00a7", "sec")
        .replace(" ", "_")
        .replace("\u0394", "Delta")
        .lower()
    )


def _smiles_records(smiles_json: Path, sections: set[str]) -> list[dict]:
    if not smiles_json.exists():
        return []
    doc = json.loads(smiles_json.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in sections:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "oncology_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
                "source": "smiles_lab",
            }
        )
    return records


def _biology_strict_records() -> list[dict]:
    if not BIO_STRICT.exists():
        return []
    doc = json.loads(BIO_STRICT.read_text(encoding="utf-8"))
    records: list[dict] = []
    for row in doc.get("records") or []:
        if not row.get("strict"):
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "oncology_lab",
                "property": row.get("property"),
                "name": row.get("name"),
                "computed": row.get("computed"),
                "measured": row.get("measured"),
                "error_pct": float(err),
                "source": "biology_strict_lab",
            }
        )
    return records


def _section_decomposition(smiles_records: list[dict]) -> dict[str, dict]:
    by_section: dict[str, list[float]] = {}
    for row in smiles_records:
        by_section.setdefault(row["property"], []).append(float(row["error_pct"]))
    out: dict[str, dict] = {}
    for section, errs in sorted(by_section.items()):
        out[section] = {
            "record_count": len(errs),
            "median_error_pct": _median(errs),
            "max_error_pct": max(errs),
            "min_error_pct": min(errs),
        }
    return out


def _headline_records(
    *,
    pooled_median: float,
    observable_count: int,
    section_decomposition: dict[str, dict],
    strict_records: list[dict],
) -> list[dict]:
    headlines: list[dict] = [
        {
            "lab": "oncology_lab",
            "property": "pooled_oncology_median",
            "name": "all_channels",
            "computed": round(pooled_median, 6),
            "measured": 0.0,
            "error_pct": pooled_median,
            "observable_count": observable_count,
        }
    ]
    for section in HEADLINE_SECTIONS:
        stats = section_decomposition.get(section) or {}
        med = float(stats.get("median_error_pct") or 0.0)
        headlines.append(
            {
                "lab": "oncology_lab",
                "property": f"section_median_{_section_slug(section)}",
                "name": section,
                "computed": round(med, 6),
                "measured": 0.0,
                "error_pct": med,
                "observable_count": int(stats.get("record_count") or 0),
                "section": section,
            }
        )
    strict_errs = [float(r["error_pct"]) for r in strict_records]
    strict_med = _median(strict_errs) or 0.0
    headlines.append(
        {
            "lab": "oncology_lab",
            "property": "biology_strict_operon_bridge_median",
            "name": "ncbi_strict_operons",
            "computed": round(strict_med, 6),
            "measured": 0.0,
            "error_pct": strict_med,
            "observable_count": len(strict_records),
        }
    )
    return headlines


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    sections = set(spec.get("sections") or ONCOLOGY_SECTIONS)

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from fsot_paths import smiles_dataset_path  # noqa: E402

    _, authority_path = load_fsot_compute()
    smiles_json = smiles_dataset_path()
    smiles_records = _smiles_records(smiles_json, sections)
    strict_records = _biology_strict_records()
    material_records = smiles_records + strict_records

    all_errs = [float(r["error_pct"]) for r in material_records]
    pooled_median = _median(all_errs)
    section_decomposition = _section_decomposition(smiles_records)
    headline_records = _headline_records(
        pooled_median=float(pooled_median or 0.0),
        observable_count=len(material_records),
        section_decomposition=section_decomposition,
        strict_records=strict_records,
    )
    headline_errs = [float(r["error_pct"]) for r in headline_records]
    headline_median = _median(headline_errs)

    beats_sota_summary = {
        "pooled_vs_chembl_qsar": pooled_median is not None and pooled_median < 12.0,
        "pooled_vs_pdbbind": pooled_median is not None and pooled_median < 15.0,
        "biology_strict_vs_genomics_proxy": (
            _median([float(r["error_pct"]) for r in strict_records]) or 99.0
        )
        < 8.0,
    }
    for section, baseline in SOTA_SECTION_BASELINES.items():
        stats = section_decomposition.get(section) or {}
        med = stats.get("median_error_pct")
        key = f"section_{_section_slug(section)}_vs_baseline"
        beats_sota_summary[key] = (
            med is not None and float(med) < float(baseline["sota_typical_error_pct"])
        )

    d_eff = int(spec.get("D_eff") or 14)
    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": [str(smiles_json), str(BIO_STRICT)],
        "source_repo": spec.get("source_repo", "vendor/oncology"),
        "maps_to_lean": spec.get("maps_to_lean") or ["medical", "biological"],
        "D_eff": d_eff,
        "record_count": len(material_records),
        "observable_count": len(material_records),
        "smiles_record_count": len(smiles_records),
        "biology_strict_record_count": len(strict_records),
        "section_count": len(section_decomposition),
        "median_error_pct": pooled_median,
        "headline_median_error_pct": headline_median,
        "pooled_median_error_pct": pooled_median,
        "section_decomposition": section_decomposition,
        "sota_comparison": {
            "fsot_free_parameters": 0,
            "headline_observables": {
                "pooled_median_error_pct": pooled_median,
                "headline_median_error_pct": headline_median,
                "section_count": len(section_decomposition),
            },
            "operational_baselines": {
                "chembl_oncology_qsar": {
                    "sota_model": "ChEMBL target affinity QSAR",
                    "sota_typical_error_pct": 12.0,
                    "reference": "Oncology drug-target affinity panels",
                },
                "pdbbind_kinase": {
                    "sota_model": "PDBbind FEP+ pKi",
                    "sota_typical_error_pct": 15.0,
                    "reference": "Kinase inhibitor structural thermodynamics",
                },
                **SOTA_SECTION_BASELINES,
            },
            "beats_sota_summary": beats_sota_summary,
        },
        "records": headline_records,
        "material_records": material_records,
        "crosswalk_modules": ["FSOT.Formal.OncologyPriors"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records: {doc['record_count']} (smiles={doc['smiles_record_count']} "
        f"strict={doc['biology_strict_record_count']})  "
        f"pooled_median_err: {doc['median_error_pct']:.4f}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())