#!/usr/bin/env python3
"""Quantum materials — condensed-matter SMILES observables (v1.1 headline rollup)."""

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
MANIFEST = ROOT / "data" / "quantum_materials_manifest.yaml"
OUTPUT = ROOT / "data" / "quantum_materials_benchmark.json"

QUANTUM_MATERIALS_SECTIONS = {
    "\u00a729 Dielectric \u03b5r",
    "\u00a733 Debye Temps",
    "\u00a738 Resistivity \u03c1",
    "\u00a752 \u00b9\u00b3C NMR \u03b4",
    "\u00a763 Lattice Param",
    "\u00a713 \u03c7m Magnetic",
    "\u00a719 NMR \u03b4",
    "\u00a731 Band Gaps",
    "\u00a755 \u03bceff Magnetic",
    "\u00a775 Superconducting Tc",
    "\u00a776 Magnetic Ordering T",
    "\u00a74b Lattice Energies",
    "\u00a718 Crystal Field \u0394o",
}

HEADLINE_SECTIONS = [
    "\u00a731 Band Gaps",
    "\u00a718 Crystal Field \u0394o",
    "\u00a755 \u03bceff Magnetic",
    "\u00a775 Superconducting Tc",
]

SOTA_SECTION_BASELINES = {
    "\u00a731 Band Gaps": {
        "sota_model": "Materials Project DFT band-gap workflow",
        "sota_typical_error_pct": 10.0,
        "reference": "MP band-gap MAE vs experiment (~0.3–1 eV)",
    },
    "\u00a718 Crystal Field \u0394o": {
        "sota_model": "Ligand-field + cluster DFT fits",
        "sota_typical_error_pct": 15.0,
        "reference": "Transition-metal complex Δo tabulations",
    },
    "\u00a755 \u03bceff Magnetic": {
        "sota_model": "Spin-only + crystal-field correction fits",
        "sota_typical_error_pct": 8.0,
        "reference": "Inorganic complex μeff regressions",
    },
    "\u00a775 Superconducting Tc": {
        "sota_model": "McMillan/BCS empirical Tc correlations",
        "sota_typical_error_pct": 20.0,
        "reference": "Elemental/compound Tc phenomenology",
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
        .replace("\u03b5", "epsilon")
        .replace("\u03c1", "rho")
        .replace("\u03b4", "delta")
        .replace("\u03c7", "chi")
        .replace("\u03bc", "mu")
        .replace("\u0394", "Delta")
        .replace("\u00b9", "")
        .replace("\u00b3", "")
        .replace("(", "")
        .replace(")", "")
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
            "lab": "quantum_materials_lab",
            "property": "pooled_condensed_matter_median",
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
                "lab": "quantum_materials_lab",
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
    sections = set(spec.get("sections") or QUANTUM_MATERIALS_SECTIONS)

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from fsot_paths import smiles_dataset_path  # noqa: E402

    _, authority_path = load_fsot_compute()
    smiles_json = smiles_dataset_path()
    if not smiles_json.exists():
        return {"record_count": 0, "records": [], "error": "SMILES dataset missing"}

    doc = json.loads(smiles_json.read_text(encoding="utf-8"))
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
                "lab": "quantum_materials_lab",
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
        "condensed_matter_dft": {
            "sota_model": "DFT + tight-binding (Materials Project class)",
            "sota_typical_error_pct": 5.0,
            "reference": "Materials Project DFT bands/lattice medians",
        },
        "materials_calphad": {
            "sota_model": "DFT + CALPHAD thermodynamic fits",
            "sota_typical_error_pct": 5.0,
            "reference": "Materials Project formation-energy workflows",
        },
    }
    operational_baselines.update(SOTA_SECTION_BASELINES)

    beats_sota_summary = {
        "pooled_vs_condensed_matter_dft": (
            pooled_median is not None and pooled_median < 5.0
        ),
        "pooled_vs_materials_calphad": (
            pooled_median is not None and pooled_median < 5.0
        ),
    }
    for section, baseline in SOTA_SECTION_BASELINES.items():
        stats = section_decomposition.get(section) or {}
        med = stats.get("median_error_pct")
        key = f"section_{_section_slug(section)}_vs_baseline"
        beats_sota_summary[key] = (
            med is not None and float(med) < float(baseline["sota_typical_error_pct"])
        )

    sota_comparison = {
        "fsot_free_parameters": 0,
        "headline_observables": {
            "pooled_median_error_pct": pooled_median,
            "headline_median_error_pct": headline_median,
            "section_count": len(section_decomposition),
        },
        "operational_baselines": operational_baselines,
        "beats_sota_summary": beats_sota_summary,
    }

    d_eff = int(spec.get("D_eff") or 16)
    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": str(smiles_json),
        "source_repo": spec.get("source_repo", "vendor/smiles"),
        "maps_to_lean": spec.get("maps_to_lean") or ["material", "quantum"],
        "D_eff": d_eff,
        "record_count": len(material_records),
        "observable_count": len(material_records),
        "section_count": len(section_decomposition),
        "median_error_pct": pooled_median,
        "headline_median_error_pct": headline_median,
        "pooled_median_error_pct": pooled_median,
        "section_decomposition": section_decomposition,
        "sota_comparison": sota_comparison,
        "records": headline_records,
        "material_records": material_records,
        "crosswalk_modules": ["FSOT.Formal.QuantumMaterialsPriors"],
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
    beats = sum(1 for v in (doc.get("sota_comparison") or {}).get("beats_sota_summary", {}).values() if v)
    print(f"  beats_sota_headlines: {beats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())