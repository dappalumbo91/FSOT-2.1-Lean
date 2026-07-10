#!/usr/bin/env python3
"""Generate Lean priors for Tier 53–56 expansion domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "Stellar_Multiplicity_Catalog": ("stellar_multiplicity_catalog", "StellarMultiplicityCatalogPriors", 19, "stellar_multiplicity_catalog_benchmark.json"),
    "Compact_Object_Binary_Events": ("compact_object_binary_events", "CompactObjectBinaryEventsPriors", 20, "compact_object_binary_events_benchmark.json"),
    "Galactic_Structure_Sample": ("galactic_structure_sample", "GalacticStructureSamplePriors", 20, "galactic_structure_sample_benchmark.json"),
    "Solar_System_Structure_Deep": ("solar_system_structure_deep", "SolarSystemStructureDeepPriors", 18, "solar_system_structure_deep_benchmark.json"),
    "Exoplanet_System_Architecture": ("exoplanet_system_architecture", "ExoplanetSystemArchitecturePriors", 21, "exoplanet_system_architecture_benchmark.json"),
    "PubChem_Stability_Panel": ("pubchem_stability_panel", "PubChemStabilityPanelPriors", 14, "pubchem_stability_panel_benchmark.json"),
    "Materials_Genome_Crosswalk": ("materials_genome_crosswalk", "MaterialsGenomeCrosswalkPriors", 15, "materials_genome_crosswalk_benchmark.json"),
    "UniProt_Structure_Annotations_Deep": ("uniprot_structure_annotations_deep", "UniProtStructureAnnotationsDeepPriors", 13, "uniprot_structure_annotations_deep_benchmark.json"),
    "IGEM_Parts_Expanded": ("igem_parts_expanded", "IGEMPartsExpandedPriors", 14, "igem_parts_expanded_benchmark.json"),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    return f"""/-
  FSOT Formal {module_stem} — generated from public catalog benchmarks.
  Generator: scripts/gen_tiers_53_56_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) ∧
    {prefix}_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · exact {prefix}_pooled_median_under_half_pct
  · exact {prefix}_beats_sota_headlines_pos

end
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(DOMAIN_CONFIG.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(DOMAIN_CONFIG.keys())
    for domain in domains:
        prefix, module_stem, d_eff, bench_name = DOMAIN_CONFIG[domain]
        bench_path = DATA / bench_name
        if not bench_path.exists():
            print(f"Missing benchmark: {bench_path}", file=sys.stderr)
            return 1
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, prefix, module_stem, d_eff)
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())