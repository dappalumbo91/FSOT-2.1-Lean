#!/usr/bin/env python3
"""Generate FSOT/Formal/MathGeneratorRulesEvalPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "math_generator_rules_eval_manifest.yaml"
BENCH = ROOT / "data" / "math_generator_rules_eval_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "MathGeneratorRulesEvalPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    corpora = int(bench.get("rule_corpus_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    numeric_n = int(bench.get("numeric_eval_count") or 0)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 17)
    source = cfg.get("source_repo", "vendor/math_generator/rules")
    sign = (cfg.get("lean") or {}).get("sign_theorem", "particle_raw_S_positive")
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal MathGeneratorRulesEvalPriors — per-rule eval across 1520 formal rules.
  Generator: scripts/gen_math_generator_rules_eval_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def math_generator_rules_eval_observable_count : ℕ := {n}
def math_generator_rules_eval_corpus_count : ℕ := {corpora}
def math_generator_rules_eval_numeric_eval_count : ℕ := {numeric_n}
def math_generator_rules_eval_D_eff : ℕ := {d_eff}
def math_generator_rules_eval_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def math_generator_rules_eval_headline_median_error_pct : ℝ := ({headline} : ℝ)
def math_generator_rules_eval_beats_sota_headlines : ℕ := {beats}

theorem math_generator_rules_eval_observable_count_pos : 0 < math_generator_rules_eval_observable_count := by
  unfold math_generator_rules_eval_observable_count; norm_num

theorem math_generator_rules_eval_corpus_count_pos : 0 < math_generator_rules_eval_corpus_count := by
  unfold math_generator_rules_eval_corpus_count; norm_num

theorem math_generator_rules_eval_pooled_median_under_five_pct :
    math_generator_rules_eval_pooled_median_error_pct < (5 : ℝ) := by
  unfold math_generator_rules_eval_pooled_median_error_pct; norm_num

theorem math_generator_rules_eval_headline_median_under_five_pct :
    math_generator_rules_eval_headline_median_error_pct < (5 : ℝ) := by
  unfold math_generator_rules_eval_headline_median_error_pct; norm_num

theorem math_generator_rules_eval_beats_sota_headlines_pos : 0 < math_generator_rules_eval_beats_sota_headlines := by
  unfold math_generator_rules_eval_beats_sota_headlines; norm_num

theorem math_generator_rules_eval_bundle :
    math_generator_rules_eval_observable_count = {n} ∧
    math_generator_rules_eval_corpus_count = {corpora} ∧
    math_generator_rules_eval_numeric_eval_count = {numeric_n} ∧
    math_generator_rules_eval_D_eff = {d_eff} ∧
    math_generator_rules_eval_pooled_median_error_pct < (5 : ℝ) ∧
    math_generator_rules_eval_headline_median_error_pct < (5 : ℝ) ∧
    0 < math_generator_rules_eval_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold math_generator_rules_eval_observable_count; norm_num,
    by unfold math_generator_rules_eval_corpus_count; norm_num,
    by unfold math_generator_rules_eval_numeric_eval_count; norm_num,
    by unfold math_generator_rules_eval_D_eff; norm_num,
    math_generator_rules_eval_pooled_median_under_five_pct,
    math_generator_rules_eval_headline_median_under_five_pct,
    math_generator_rules_eval_beats_sota_headlines_pos,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())