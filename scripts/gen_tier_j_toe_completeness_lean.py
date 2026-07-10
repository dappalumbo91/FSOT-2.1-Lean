#!/usr/bin/env python3
"""Generate Lean priors for Tier J ToE completeness domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_j_toe_completeness_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Formula_Branching_Fractal": ("fractal", "mathematical", "FormulaBranchingFractalPriors"),
    "Mechanistic_Coupling": ("mech_cpl", "energy", "MechanisticCouplingPriors"),
    "CVE_Codon_Hole_Falsification": ("cve_hole", "medical", "CVECodonHoleFalsificationPriors"),
    "Theory_Completeness_Spine": ("toe_spine", "particle", "TheoryCompletenessSpinePriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, _tag, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Formula_Branching_Fractal":
        attach = int(bench.get("domain_attachment_count") or 0)
        extra_defs = f"def {prefix}_domain_attachment_count : ℕ := {attach}\n"
        extra_thms = f"""theorem {prefix}_attachments_pos : 0 < {prefix}_domain_attachment_count := by
  unfold {prefix}_domain_attachment_count; norm_num
"""
    elif domain == "Mechanistic_Coupling":
        mc = int(bench.get("mechanism_count") or 0)
        vp = int(bench.get("validated_mechanism_pairs") or 0)
        extra_defs = f"""def {prefix}_mechanism_count : ℕ := {mc}
def {prefix}_validated_pairs : ℕ := {vp}
"""
        extra_thms = f"""theorem {prefix}_mechanisms_pos : 0 < {prefix}_mechanism_count := by
  unfold {prefix}_mechanism_count; norm_num
"""
    elif domain == "CVE_Codon_Hole_Falsification":
        kev = int(bench.get("kev_record_count") or 0)
        overlap = int(float(bench.get("cwe_codon_overlap_rate") or 0) * 100)
        extra_defs = f"""def {prefix}_kev_record_count : ℕ := {kev}
def {prefix}_overlap_rate_centipercent : ℕ := {overlap}
"""
        extra_thms = f"""theorem {prefix}_kev_records_pos : 0 < {prefix}_kev_record_count := by
  unfold {prefix}_kev_record_count; norm_num
"""
    elif domain == "Theory_Completeness_Spine":
        attach = int(bench.get("domain_attachment_count") or 0)
        mech = int(bench.get("mechanism_count") or 0)
        extra_defs = f"""def {prefix}_domain_attachment_count : ℕ := {attach}
def {prefix}_mechanism_count : ℕ := {mech}
"""
        extra_thms = f"""theorem {prefix}_spine_complete_attachments : 0 < {prefix}_domain_attachment_count := by
  unfold {prefix}_domain_attachment_count; norm_num
"""
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier J ToE completeness.
  Generator: scripts/gen_tier_j_toe_completeness_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 18))}
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
        out = FORMAL / f"{LEAN_MAP[domain][2]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())