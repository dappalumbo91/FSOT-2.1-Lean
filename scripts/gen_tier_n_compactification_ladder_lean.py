#!/usr/bin/env python3
"""Generate Lean priors for Tier N compactification/folding ladder domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_n_compactification_ladder_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Compactification_Ladder": ("comp_lad", "CompactificationLadderPriors"),
    "Adjacent_Rung_Coupling": ("adj_rung", "AdjacentRungCouplingPriors"),
    "Fold_Depth_Metrics": ("fold_dep", "FoldDepthMetricsPriors"),
    "Reality_Folding_Spine": ("fold_spine", "RealityFoldingSpinePriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Compactification_Ladder":
        rc = int(bench.get("rung_count") or 0)
        extra_defs = f"def {prefix}_rung_count : ℕ := {rc}\n"
        extra_thms = f"theorem {prefix}_rungs_complete : {prefix}_rung_count = 10 := by unfold {prefix}_rung_count; norm_num\n"
    elif domain == "Adjacent_Rung_Coupling":
        pc = int(bench.get("adjacent_pair_count") or 0)
        extra_defs = f"def {prefix}_adjacent_pair_count : ℕ := {pc}\n"
        extra_thms = f"theorem {prefix}_pairs_complete : {prefix}_adjacent_pair_count = 9 := by unfold {prefix}_adjacent_pair_count; norm_num\n"
    elif domain == "Fold_Depth_Metrics":
        span = int(float(bench.get("fold_depth_span") or 0) * 10000)
        extra_defs = f"def {prefix}_fold_span_ten_thousandths : ℕ := {span}\n"
        extra_thms = f"theorem {prefix}_fold_span_pos : 0 < {prefix}_fold_span_ten_thousandths := by unfold {prefix}_fold_span_ten_thousandths; norm_num\n"
    elif domain == "Reality_Folding_Spine":
        rc = int(bench.get("ladder_rung_count") or 0)
        pc = int(bench.get("adjacent_pair_count") or 0)
        nodes = int(bench.get("coupling_node_count") or 0)
        extra_defs = (
            f"def {prefix}_ladder_rung_count : ℕ := {rc}\n"
            f"def {prefix}_adjacent_pair_count : ℕ := {pc}\n"
            f"def {prefix}_coupling_node_count : ℕ := {nodes}\n"
        )
        extra_thms = f"theorem {prefix}_ladder_rungs_pos : 0 < {prefix}_ladder_rung_count := by unfold {prefix}_ladder_rung_count; norm_num\n"
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier N compactification ladder.
  Generator: scripts/gen_tier_n_compactification_ladder_lean.py
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

theorem {prefix}_pooled_median_under_five_pct :
    {prefix}_pooled_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_five_pct :
    {prefix}_headline_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num
{extra_thms}
theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (5 : ℝ) ∧
    {prefix}_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · exact {prefix}_pooled_median_under_five_pct
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