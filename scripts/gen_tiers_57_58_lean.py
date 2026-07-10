#!/usr/bin/env python3
"""Generate Lean priors for Tier 57–58 domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "Interdisciplinary_Spine_Crosswalk": ("interdisciplinary_spine_crosswalk", "InterdisciplinarySpineCrosswalkPriors", 17, "interdisciplinary_spine_crosswalk_benchmark.json"),
    "Chemical_Structure_Stability_Panel": ("chemical_structure_stability_panel", "ChemicalStructureStabilityPanelPriors", 14, "chemical_structure_stability_panel_benchmark.json"),
    "Published_Fuel_Property_Panel": ("published_fuel_property_panel", "PublishedFuelPropertyPanelPriors", 16, "published_fuel_property_panel_benchmark.json"),
    "GWOSC_Live_Event_Deep": ("gwosc_live_event_deep", "GWOSCLiveEventDeepPriors", 20, "gwosc_live_event_deep_benchmark.json"),
    "Stellar_Multiplicity_Live_Deep": ("stellar_multiplicity_live_deep", "StellarMultiplicityLiveDeepPriors", 19, "stellar_multiplicity_live_deep_benchmark.json"),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    return f"""/-
  FSOT Formal {module_stem} — Tier 57/58 public interdisciplinary / live catalog.
  Generator: scripts/gen_tiers_57_58_lean.py
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
    for domain in args.only or sorted(DOMAIN_CONFIG.keys()):
        prefix, module_stem, d_eff, bench_name = DOMAIN_CONFIG[domain]
        bench_path = DATA / bench_name
        if not bench_path.exists():
            print(f"Missing benchmark: {bench_path}", file=sys.stderr)
            return 1
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(build_lean(bench, prefix, module_stem, d_eff), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())