#!/usr/bin/env python3
"""Generate FSOT/Formal/MathGeneratorPriors.lean from registry + rules benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
RULES_BENCH_PATH = ROOT / "data" / "math_generator_rules_benchmark.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "MathGeneratorPriors.lean"


def build_lean(registry: dict, rules_bench: dict | None) -> str:
    m = registry.get("math_generator_lab", {})
    count = m.get("comparison_count", 5)
    max_err = m.get("max_error_pct", 1.0)
    c_eff = m.get("c_eff", 0.183733)
    p_base = m.get("p_base", 0.618034)

    rb = rules_bench or registry.get("math_generator_rules") or {}
    corpus_count = int(rb.get("rule_corpus_count") or 0)
    rule_count = int(rb.get("total_rule_count") or rb.get("observable_count") or 0)

    return f"""/-
  FSOT Formal MathGeneratorPriors — cross-domain formula generator + rule corpora.

  Sources:
    - Math generator Ada/Spark comparison report (math_generator_lab)
    - data/math_generator_rules_benchmark.json ({corpus_count} corpora, {rule_count} rules)
  Generator: scripts/gen_math_generator_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def math_generator_comparison_count : ℕ := {count}
def math_generator_max_error_pct : ℝ := ({max_err} : ℝ)
def math_generator_c_eff : ℝ := ({c_eff} : ℝ)
def math_generator_p_base : ℝ := ({p_base} : ℝ)
def math_generator_rule_corpus_count : ℕ := {corpus_count}
def math_generator_rule_observable_count : ℕ := {rule_count}

theorem math_generator_comparison_count_pos : 0 < math_generator_comparison_count := by
  unfold math_generator_comparison_count; norm_num

theorem math_generator_rule_corpus_count_pos : 0 < math_generator_rule_corpus_count := by
  unfold math_generator_rule_corpus_count; norm_num

theorem math_generator_rule_observable_count_pos : 0 < math_generator_rule_observable_count := by
  unfold math_generator_rule_observable_count; norm_num

theorem math_generator_max_error_pct_positive : (0 : ℝ) < math_generator_max_error_pct := by
  unfold math_generator_max_error_pct; norm_num

theorem math_generator_rule_observables_ge_corpora :
    math_generator_rule_corpus_count ≤ math_generator_rule_observable_count := by
  unfold math_generator_rule_corpus_count math_generator_rule_observable_count; norm_num

/-- Bundle: Ada/Spark comparisons + formal rule corpora with particle-domain sign proxy. -/
theorem math_generator_priors_bundle :
    math_generator_comparison_count = {count} ∧
    math_generator_max_error_pct = ({max_err} : ℝ) ∧
    math_generator_c_eff = ({c_eff} : ℝ) ∧
    math_generator_p_base = ({p_base} : ℝ) ∧
    math_generator_rule_corpus_count = {corpus_count} ∧
    math_generator_rule_observable_count = {rule_count} ∧
    math_generator_rule_corpus_count ≤ math_generator_rule_observable_count ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold math_generator_comparison_count; norm_num,
    by unfold math_generator_max_error_pct; norm_num,
    by unfold math_generator_c_eff; norm_num,
    by unfold math_generator_p_base; norm_num,
    by unfold math_generator_rule_corpus_count; norm_num,
    by unfold math_generator_rule_observable_count; norm_num,
    math_generator_rule_observables_ge_corpora,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MathGeneratorPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--rules-benchmark", type=Path, default=RULES_BENCH_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    rules_bench = None
    if args.rules_benchmark.exists():
        rules_bench = json.loads(args.rules_benchmark.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry, rules_bench), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())