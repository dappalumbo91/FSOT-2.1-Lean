#!/usr/bin/env python3
"""Generate Lean priors for Tier 62–64 domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "WDS_Live_Multiplicity_Deep": ("wds_live_multiplicity_deep", "WDSLiveMultiplicityDeepPriors", 19, "wds_live_multiplicity_deep_benchmark.json"),
    "Gaia_DR3_TAP_Deep": ("gaia_dr3_tap_deep", "GaiaDR3TAPDeepPriors", 20, "gaia_dr3_tap_deep_benchmark.json"),
    "Preregistered_Predictions_Verification_Scaffold": (
        "preregistered_predictions_verification_scaffold",
        "PreregisteredPredictionsVerificationScaffoldPriors",
        17,
        "preregistered_predictions_verification_scaffold_benchmark.json",
    ),
    "Information_Theory_Public_Panel": ("information_theory_public_panel", "InformationTheoryPublicPanelPriors", 8, "information_theory_public_panel_benchmark.json"),
    "Network_Science_Public_Panel": ("network_science_public_panel", "NetworkSciencePublicPanelPriors", 17, "network_science_public_panel_benchmark.json"),
    "Semiconductor_Physics_Public_Panel": ("semiconductor_physics_public_panel", "SemiconductorPhysicsPublicPanelPriors", 11, "semiconductor_physics_public_panel_benchmark.json"),
    "Statistical_Mechanics_Public_Panel": ("statistical_mechanics_public_panel", "StatisticalMechanicsPublicPanelPriors", 12, "statistical_mechanics_public_panel_benchmark.json"),
    "Biophysics_Public_Panel": ("biophysics_public_panel", "BiophysicsPublicPanelPriors", 12, "biophysics_public_panel_benchmark.json"),
    "Neurolab_Gaps_Math_Spine": ("neurolab_gaps_math_spine", "NeurolabGapsMathSpinePriors", 17, "neurolab_gaps_math_spine_benchmark.json"),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    return f"""/-
  FSOT Formal {module_stem} — Tier 62–64 live astrometry, prereg scaffold, NeuroLab gaps.
  Generator: scripts/gen_tiers_62_64_lean.py
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