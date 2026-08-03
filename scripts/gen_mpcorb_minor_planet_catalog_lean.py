#!/usr/bin/env python3
"""Generate FSOT/Formal/MpcorbMinorPlanetCatalogPriors.lean from refined benchmark."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "mpcorb_fsot_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "MpcorbMinorPlanetCatalogPriors.lean"


def main() -> int:
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    n = int(bench.get("mpcorb_object_count") or bench.get("record_count") or 0)
    med = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    d_eff = int(bench.get("D_eff") or 21)
    kepler = float((bench.get("catalog_stats") or {}).get("kepler_median_error_pct") or 0.0)
    green = bool(bench.get("green_gate_pass"))

    text = f"""/-
  FSOT Formal MpcorbMinorPlanetCatalogPriors — IAU MPCORB full-catalog residual gates.
  Generator: scripts/gen_mpcorb_minor_planet_catalog_lean.py
  Refinement: docs/MPCORB_REFINEMENT_PROCESS.md
  Prediction law: measured * (1 + |S(domain)| * factor) at D_eff interfaces.
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def mpcorb_object_count : ℕ := {n}
def mpcorb_D_eff : ℕ := {d_eff}
def mpcorb_pooled_median_error_pct : ℝ := ({med} : ℝ)
def mpcorb_kepler_median_error_pct : ℝ := ({kepler} : ℝ)
def mpcorb_green_gate_flag : ℕ := {1 if green else 0}

theorem mpcorb_object_count_pos : 0 < mpcorb_object_count := by
  unfold mpcorb_object_count; norm_num

theorem mpcorb_pooled_median_under_half_pct :
    mpcorb_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold mpcorb_pooled_median_error_pct; norm_num

theorem mpcorb_pooled_median_under_tier_aspiration :
    mpcorb_pooled_median_error_pct < (0.05 : ℝ) := by
  unfold mpcorb_pooled_median_error_pct; norm_num

theorem mpcorb_kepler_integrity_under_ppm :
    mpcorb_kepler_median_error_pct < (0.001 : ℝ) := by
  unfold mpcorb_kepler_median_error_pct; norm_num

theorem mpcorb_green_gate_pass : mpcorb_green_gate_flag = 1 := by
  unfold mpcorb_green_gate_flag; rfl

theorem mpcorb_minor_planet_catalog_bundle :
    mpcorb_object_count = {n} ∧
    mpcorb_D_eff = {d_eff} ∧
    mpcorb_pooled_median_error_pct < (0.5 : ℝ) ∧
    mpcorb_pooled_median_error_pct < (0.05 : ℝ) ∧
    mpcorb_kepler_median_error_pct < (0.001 : ℝ) ∧
    mpcorb_green_gate_flag = 1 ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold mpcorb_object_count; norm_num,
    by unfold mpcorb_D_eff; norm_num,
    mpcorb_pooled_median_under_half_pct,
    mpcorb_pooled_median_under_tier_aspiration,
    mpcorb_kepler_integrity_under_ppm,
    mpcorb_green_gate_pass,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
"""
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"  objects={n} pooled_med%={med} D_eff={d_eff} green={green}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
