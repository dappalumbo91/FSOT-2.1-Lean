#!/usr/bin/env python3
"""Generate Lean priors for Tier K ToE gap-closure domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_k_toe_gap_closure_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Fractal_Constant_Recursion": ("const_rec", "FractalConstantRecursionPriors"),
    "Preregistered_Predictions": ("prereg", "PreregisteredPredictionsPriors"),
    "Portable_Clone_Verify": ("clone_vf", "PortableCloneVerifyPriors"),
    "Observer_Channel_Derivation": ("obs_ch", "ObserverChannelDerivationPriors"),
    "Adversarial_Fractal_Break_Tests": ("adv_brk", "AdversarialFractalBreakPriors"),
    "ToE_Gap_Closure_Spine": ("gap_spine", "ToEGapClosureSpinePriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Fractal_Constant_Recursion":
        fc = int(bench.get("constant_family_count") or 0)
        sb = int(bench.get("sub_branch_count") or 0)
        extra_defs = f"def {prefix}_family_count : ℕ := {fc}\ndef {prefix}_sub_branch_count : ℕ := {sb}\n"
        extra_thms = f"theorem {prefix}_families_pos : 0 < {prefix}_family_count := by unfold {prefix}_family_count; norm_num\n"
    elif domain == "Preregistered_Predictions":
        pc = int(bench.get("prediction_count") or 0)
        dp = int(bench.get("discriminant_pass_count") or 0)
        extra_defs = f"def {prefix}_prediction_count : ℕ := {pc}\ndef {prefix}_discriminant_pass_count : ℕ := {dp}\n"
        extra_thms = f"theorem {prefix}_predictions_pos : 0 < {prefix}_prediction_count := by unfold {prefix}_prediction_count; norm_num\n"
    elif domain == "Portable_Clone_Verify":
        ok = 1 if bench.get("clone_verify_pass") else 0
        extra_defs = f"def {prefix}_clone_verify_pass : ℕ := {ok}\n"
    elif domain == "Observer_Channel_Derivation":
        qc = int(bench.get("quirkmod_derived_count") or 0)
        extra_defs = f"def {prefix}_quirkmod_derived_count : ℕ := {qc}\n"
        extra_thms = f"theorem {prefix}_quirkmod_derived_pos : 0 < {prefix}_quirkmod_derived_count := by unfold {prefix}_quirkmod_derived_count; norm_num\n"
    elif domain == "Adversarial_Fractal_Break_Tests":
        rate = int(float(bench.get("adversarial_detection_rate") or 0) * 100)
        extra_defs = f"def {prefix}_detection_rate_centipercent : ℕ := {rate}\n"
    elif domain == "ToE_Gap_Closure_Spine":
        pillars = int(bench.get("pillar_count") or 0)
        extra_defs = f"def {prefix}_pillar_count : ℕ := {pillars}\n"
        extra_thms = f"theorem {prefix}_pillars_pos : 0 < {prefix}_pillar_count := by unfold {prefix}_pillar_count; norm_num\n"
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier K gap closure.
  Generator: scripts/gen_tier_k_toe_gap_closure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 17))}
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