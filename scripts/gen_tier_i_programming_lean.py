#!/usr/bin/env python3
"""Generate Lean priors for Tier I programming domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_i_programming_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "External_OSS_Code_Genome": (
        "external_oss",
        "ai",
        "ai_raw_S_positive",
        "ExternalOSSCodeGenomePriors",
    ),
    "Programming_Language_Laws": (
        "pl_laws",
        "consciousness",
        "consciousness_raw_S_positive",
        "ProgrammingLanguageLawsPriors",
    ),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, _lean_domain, _sign, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "External_OSS_Code_Genome":
        samples = int(bench.get("oss_sample_count") or 0)
        aff = int(bench.get("high_affinity_pair_count") or 0)
        extra_defs = f"""
def {prefix}_oss_sample_count : ℕ := {samples}
def {prefix}_high_affinity_pair_count : ℕ := {aff}
"""
        extra_thms = f"""
theorem {prefix}_oss_samples_pos : 0 < {prefix}_oss_sample_count := by
  unfold {prefix}_oss_sample_count; norm_num
"""
    if domain == "Programming_Language_Laws":
        laws = int(bench.get("law_count") or 0)
        ling = int(bench.get("linguistics_bridge_count") or 0)
        cg = int(bench.get("code_genome_bridge_count") or 0)
        extra_defs = f"""
def {prefix}_law_count : ℕ := {laws}
def {prefix}_linguistics_bridge_count : ℕ := {ling}
def {prefix}_code_genome_bridge_count : ℕ := {cg}
"""
        extra_thms = f"""
theorem {prefix}_law_count_pos : 0 < {prefix}_law_count := by
  unfold {prefix}_law_count; norm_num

theorem {prefix}_cross_domain_bridges_pos :
    0 < {prefix}_linguistics_bridge_count + {prefix}_code_genome_bridge_count := by
  unfold {prefix}_linguistics_bridge_count {prefix}_code_genome_bridge_count; norm_num
"""
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier I programming verification.
  Generator: scripts/gen_tier_i_programming_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 15))}
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
        out = FORMAL / f"{LEAN_MAP[domain][3]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())