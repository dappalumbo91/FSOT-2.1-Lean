#!/usr/bin/env python3
"""Generate Lean priors for Tier 52 astrophysical structure crosswalk."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
BENCH = ROOT / "data" / "astrophysical_structure_crosswalk_benchmark.json"


def build_lean(bench: dict) -> str:
    prefix = "astrophysical_structure_crosswalk"
    module_stem = "AstrophysicalStructureCrosswalkPriors"
    n = int(bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    meta = bench.get("crosswalk_meta") or {}
    cat_n = int(meta.get("catalog_systems") or 0)
    class_n = len(meta.get("structure_classes") or [])

    return f"""/-
  FSOT Formal {module_stem} — Tier 52 public catalog crosswalk.
  Generator: scripts/gen_tier52_astrophysical_lean.py
  Note: published observables only; no undisclosed predictions.
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := 18
def {prefix}_catalog_system_count : ℕ := {cat_n}
def {prefix}_structure_class_count : ℕ := {class_n}

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

theorem {prefix}_catalog_systems_pos : 0 < {prefix}_catalog_system_count := by
  unfold {prefix}_catalog_system_count; norm_num

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
    if not BENCH.exists():
        print(f"Missing benchmark: {BENCH}", file=sys.stderr)
        return 1
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    lean = build_lean(bench)
    out = FORMAL / "AstrophysicalStructureCrosswalkPriors.lean"
    out.write_text(lean, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())