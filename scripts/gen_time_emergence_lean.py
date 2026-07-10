#!/usr/bin/env python3
"""Generate Lean priors for Tier 50 time emergence / FPC domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_o_time_emergence_lib import BUILDERS, TIER_O, output_path  # noqa: E402

LEAN_MAP = {
    "Time_Emergence_Simulation": ("time_em", "TimeEmergenceSimulationPriors"),
    "Time_Domain_Crosswalk": ("time_xw", "TimeDomainCrosswalkPriors"),
    "FPC_Temporal_Coupling": ("fpc_link", "FPCTemporalCouplingPriors"),
    "Fluid_Phase_Current_Spine": ("fpc_spine", "FluidPhaseCurrentSpinePriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Time_Emergence_Simulation":
        scales = int(bench.get("scale_count") or 6)
        extra_defs = f"def {prefix}_scale_count : ℕ := {scales}\n"
        extra_thms = f"theorem {prefix}_scales_complete : {prefix}_scale_count = 6 := by unfold {prefix}_scale_count; norm_num\n"
    elif domain == "Time_Domain_Crosswalk":
        dc = int(bench.get("crosswalk_domain_count") or 0)
        extra_defs = f"def {prefix}_crosswalk_domain_count : ℕ := {dc}\n"
        extra_thms = f"theorem {prefix}_crosswalk_domains_pos : 0 < {prefix}_crosswalk_domain_count := by unfold {prefix}_crosswalk_domain_count; norm_num\n"
    elif domain == "FPC_Temporal_Coupling":
        ec = int(bench.get("fluidlink_edge_count") or 0)
        extra_defs = f"def {prefix}_fluidlink_edge_count : ℕ := {ec}\n"
        extra_thms = f"theorem {prefix}_fluidlink_edges_pos : 0 < {prefix}_fluidlink_edge_count := by unfold {prefix}_fluidlink_edge_count; norm_num\n"
    elif domain == "Fluid_Phase_Current_Spine":
        ec = int(bench.get("fluidlink_edge_count") or 0)
        cc = int(bench.get("crosswalk_domain_count") or 0)
        extra_defs = (
            f"def {prefix}_fluidlink_edge_count : ℕ := {ec}\n"
            f"def {prefix}_crosswalk_domain_count : ℕ := {cc}\n"
        )
        extra_thms = f"theorem {prefix}_spine_edges_pos : 0 < {prefix}_fluidlink_edge_count := by unfold {prefix}_fluidlink_edge_count; norm_num\n"
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier 50 time emergence / FPC.
  Generator: scripts/gen_time_emergence_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 19))}
{extra_defs}
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
{extra_thms}
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
    parser.add_argument("--only", choices=sorted(LEAN_MAP.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(LEAN_MAP.keys())
    for domain in domains:
        bench_path = output_path(domain)
        if not bench_path.exists():
            bench = BUILDERS[domain]()
            bench_path.write_text(json.dumps(bench, indent=2), encoding="utf-8")
        else:
            bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, domain)
        out = FORMAL / f"{LEAN_MAP[domain][1]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())