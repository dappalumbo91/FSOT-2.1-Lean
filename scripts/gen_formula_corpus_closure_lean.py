#!/usr/bin/env python3
"""Generate Lean priors for formula corpus closure benchmark."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
BENCH = ROOT / "data" / "formula_corpus_closure_benchmark.json"


def main() -> int:
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    n = int(bench.get("observable_count") or 0)
    strict_n = int(bench.get("strict_empirical_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    beats = sum(1 for v in (bench.get("sota_comparison") or {}).get("beats_sota_summary", {}).values() if v)
    out = FORMAL / "FormulaCorpusClosurePriors.lean"
    out.write_text(
        f"""/-
  FSOT Formal FormulaCorpusClosurePriors — strict-empirical + extension bridge closure.
  Generator: scripts/gen_formula_corpus_closure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def formula_corpus_closure_observable_count : ℕ := {n}
def formula_corpus_closure_strict_empirical_count : ℕ := {strict_n}
def formula_corpus_closure_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def formula_corpus_closure_beats_sota_headlines : ℕ := {beats}
def formula_corpus_closure_D_eff : ℕ := 17

theorem formula_corpus_closure_observable_count_pos : 0 < formula_corpus_closure_observable_count := by
  unfold formula_corpus_closure_observable_count; norm_num

theorem formula_corpus_closure_strict_empirical_pos : 0 < formula_corpus_closure_strict_empirical_count := by
  unfold formula_corpus_closure_strict_empirical_count; norm_num

theorem formula_corpus_closure_pooled_median_under_five_pct :
    formula_corpus_closure_pooled_median_error_pct < (5 : ℝ) := by
  unfold formula_corpus_closure_pooled_median_error_pct; norm_num

theorem formula_corpus_closure_beats_sota_headlines_pos : 0 < formula_corpus_closure_beats_sota_headlines := by
  unfold formula_corpus_closure_beats_sota_headlines; norm_num

theorem formula_corpus_closure_bundle :
    formula_corpus_closure_observable_count = {n} ∧
    formula_corpus_closure_strict_empirical_count = {strict_n} ∧
    formula_corpus_closure_pooled_median_error_pct < (5 : ℝ) ∧
    0 < formula_corpus_closure_beats_sota_headlines ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold formula_corpus_closure_observable_count; norm_num,
    by unfold formula_corpus_closure_strict_empirical_count; norm_num,
    formula_corpus_closure_pooled_median_under_five_pct,
    formula_corpus_closure_beats_sota_headlines_pos,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
""",
        encoding="utf-8",
    )
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())