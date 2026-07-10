#!/usr/bin/env python3
"""Generate FSOT/Formal/CosmologyHigherWavesPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "CosmologyHigherWavesPriors.lean"


def build_lean(registry: dict) -> str:
    w = registry.get("cosmology_higher_waves_lab", {})
    total = int(w.get("observable_count") or 0)
    w5 = int(w.get("wave5_count") or 0)
    w6 = int(w.get("wave6_count") or 0)
    w7 = int(w.get("wave7_count") or 0)
    w8 = int(w.get("wave8_count") or 0)
    w9 = int(w.get("wave9_count") or 0)
    w10 = int(w.get("wave10_count") or 0)
    max_err = w.get("max_error_pct") or 0.0
    return f"""/-
  FSOT Formal CosmologyHigherWavesPriors — fsot_compute waves 5–10 certificates.
  Generator: scripts/gen_cosmology_higher_waves_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_higher_waves_total : ℕ := {total}
def cosmology_wave5_count : ℕ := {w5}
def cosmology_wave6_count : ℕ := {w6}
def cosmology_wave7_count : ℕ := {w7}
def cosmology_wave8_count : ℕ := {w8}
def cosmology_wave9_count : ℕ := {w9}
def cosmology_wave10_count : ℕ := {w10}
def cosmology_higher_waves_max_error_pct : ℝ := ({max_err} : ℝ)

theorem cosmology_higher_waves_total_pos : 0 < cosmology_higher_waves_total := by
  unfold cosmology_higher_waves_total; norm_num

theorem cosmology_higher_waves_partition :
    cosmology_wave5_count + cosmology_wave6_count + cosmology_wave7_count +
      cosmology_wave8_count + cosmology_wave9_count + cosmology_wave10_count =
      cosmology_higher_waves_total := by
  unfold cosmology_wave5_count cosmology_wave6_count cosmology_wave7_count
    cosmology_wave8_count cosmology_wave9_count cosmology_wave10_count
    cosmology_higher_waves_total; norm_num

theorem cosmology_higher_waves_max_error_under_half_pct :
    cosmology_higher_waves_max_error_pct < (0.5 : ℝ) := by
  unfold cosmology_higher_waves_max_error_pct; norm_num

/-- Bundle: 142 higher-wave observables (electroweak, Higgs, lattice, mega-wave). -/
theorem cosmology_higher_waves_bundle :
    cosmology_higher_waves_total = {total} ∧
    cosmology_wave5_count = {w5} ∧
    cosmology_wave6_count = {w6} ∧
    cosmology_wave7_count = {w7} ∧
    cosmology_wave8_count = {w8} ∧
    cosmology_wave9_count = {w9} ∧
    cosmology_wave10_count = {w10} ∧
    cosmology_wave5_count + cosmology_wave6_count + cosmology_wave7_count +
      cosmology_wave8_count + cosmology_wave9_count + cosmology_wave10_count = {total} ∧
    cosmology_higher_waves_max_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_higher_waves_total; norm_num,
    by unfold cosmology_wave5_count; norm_num,
    by unfold cosmology_wave6_count; norm_num,
    by unfold cosmology_wave7_count; norm_num,
    by unfold cosmology_wave8_count; norm_num,
    by unfold cosmology_wave9_count; norm_num,
    by unfold cosmology_wave10_count; norm_num,
    cosmology_higher_waves_partition,
    cosmology_higher_waves_max_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())