#!/usr/bin/env python3
"""Materials engineering — mechanical/thermal SMILES observables (v1.1 headline rollup)."""

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
MANIFEST = ROOT / "data" / "materials_engineering_manifest.yaml"
OUTPUT = ROOT / "data" / "materials_engineering_benchmark.json"

ENGINEERING_SECTIONS = {
    "\u00a734 Young's Modulus",
    "\u00a737 Thermal \u03ba",
    "\u00a762 Bulk Modulus",
    "\u00a770 Shear Modulus",
    "\u00a773 Thermal Expansion",
    "\u00a784 Poisson Ratio \u03bd",
    "\u00a785 Thermal Diffusivity",
}

HEADLINE_SECTIONS = [
    "\u00a734 Young's Modulus",
    "\u00a737 Thermal \u03ba",
    "\u00a762 Bulk Modulus",
    "\u00a784 Poisson Ratio \u03bd",
]

SOTA_SECTION_BASELINES = {
    "\u00a734 Young's Modulus": {
        "sota_model": "FEA + empirical elastic moduli regressions",
        "sota_typical_error_pct": 8.0,
        "reference": "NIST/materials elastic-property databases",
    },
    "\u00a737 Thermal \u03ba": {
        "sota_model": "DFT phonon + Wiedemann-Franz fits",
        "sota_typical_error_pct": 10.0,
        "reference": "NIST thermal conductivity compilations",
    },
    "\u00a762 Bulk Modulus": {
        "sota_model": "DFT equation-of-state fits",
        "sota_typical_error_pct": 10.0,
        "reference": "Materials Project bulk-modulus workflows",
    },
    "\u00a784 Poisson Ratio \u03bd": {
        "sota_model": "Elastic-tensor DFT + empirical correlations",
        "sota_typical_error_pct": 6.0,
        "reference": "Crystallographic elastic-tensor fits",
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
        .replace("\u03ba", "kappa")
        .replace("\u03bd", "nu")
        .replace("'", "")
        .lower()
    )


def _section_decomposition(material_records: list[dict]) -> dict[str, dict]:
    by_section: dict[str, list[float]] = {}
    for row in material_records:
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
) -> list[dict]:
    headlines: list[dict] = [
        {
            "lab": "materials_engineering_lab",
            "property": "pooled_engineering_median",
            "name": "all_sections",
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
                "lab": "materials_engineering_lab",
                "property": f"section_median_{_section_slug(section)}",
                "name": section,
                "computed": round(med, 6),
                "measured": 0.0,
                "error_pct": med,
                "observable_count": int(stats.get("record_count") or 0),
                "section": section,
            }
        )
    return headlines


def build(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    sections = set(spec.get("sections") or ENGINEERING_SECTIONS)

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from fsot_paths import smiles_dataset_path  # noqa: E402

    _, authority_path = load_fsot_compute()
    smiles = smiles_dataset_path()
    doc = json.loads(smiles.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    material_records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in sections:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        material_records.append(
            {
                "lab": "materials_engineering_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
            }
        )

    all_errs = [float(r["error_pct"]) for r in material_records]
    pooled_median = _median(all_errs)
    section_decomposition = _section_decomposition(material_records)
    headline_records = _headline_records(
        pooled_median=float(pooled_median or 0.0),
        observable_count=len(material_records),
        section_decomposition=section_decomposition,
    )
    headline_errs = [float(r["error_pct"]) for r in headline_records]
    headline_median = _median(headline_errs)

    operational_baselines: dict[str, dict] = {
        "materials_science_dft": {
            "sota_model": "DFT + CALPHAD engineering-property fits",
            "sota_typical_error_pct": 5.0,
            "reference": "Materials Project mechanical/thermal medians",
        },
        "fea_empirical_qspr": {
            "sota_model": "FEA + empirical QSPR (ANSYS-class)",
            "sota_typical_error_pct": 8.0,
            "reference": "NIST material acoustic/mechanical databases",
        },
    }
    operational_baselines.update(SOTA_SECTION_BASELINES)

    beats_sota_summary = {
        "pooled_vs_materials_science_dft": (
            pooled_median is not None and pooled_median < 5.0
        ),
        "pooled_vs_fea_empirical": (
            pooled_median is not None and pooled_median < 8.0
        ),
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
        "source": str(smiles),
        "source_repo": spec.get("source_repo", "vendor/smiles"),
        "maps_to_lean": spec.get("maps_to_lean") or ["material", "energy"],
        "D_eff": d_eff,
        "record_count": len(material_records),
        "observable_count": len(material_records),
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
            "operational_baselines": operational_baselines,
            "beats_sota_summary": beats_sota_summary,
        },
        "records": headline_records,
        "material_records": material_records,
        "crosswalk_modules": ["FSOT.Formal.MaterialsEngineeringPriors"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  material_records: {doc['record_count']}  sections: {doc['section_count']}  "
        f"pooled_median_err: {doc['median_error_pct']:.4f}%  "
        f"headline_median_err: {doc['headline_median_error_pct']:.4f}%"
    )
    beats = sum(
        1 for v in doc["sota_comparison"]["beats_sota_summary"].values() if v
    )
    print(f"  beats_sota_headlines: {beats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())