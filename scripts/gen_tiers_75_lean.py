#!/usr/bin/env python3
"""Generate Lean priors for Tier 75 periodic extension closure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "Distant_Island_Z128_Z132_Deep_Panel": ("distant_island_z128_z132_deep_panel", "DistantIslandZ128Z132DeepPanelPriors", 23, "distant_island_z128_z132_deep_panel_benchmark.json"),
    "Z164_Distant_Island_Prereg_Scaffold": ("z164_distant_island_prereg_scaffold", "Z164DistantIslandPreregScaffoldPriors", 24, "z164_distant_island_prereg_scaffold_benchmark.json"),
    "Periodic_Extension_Decay_Topology_Scaffold": ("periodic_extension_decay_topology_scaffold", "PeriodicExtensionDecayTopologyScaffoldPriors", 22, "periodic_extension_decay_topology_scaffold_benchmark.json"),
    "Distant_Island_Emergence_Simulation": ("distant_island_emergence_simulation", "DistantIslandEmergenceSimulationPriors", 25, "distant_island_emergence_simulation_benchmark.json"),
    "Periodic_Table_Extension_Closure_Spine": ("periodic_table_extension_closure_spine", "PeriodicTableExtensionClosureSpinePriors", 26, "periodic_table_extension_closure_spine_benchmark.json"),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    return f"""/-
  FSOT Formal {module_stem} — Tier 75 periodic extension closure.
  Generator: scripts/gen_tiers_75_lean.py
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