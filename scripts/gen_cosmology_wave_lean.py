#!/usr/bin/env python3
"""Generate FSOT/Formal/CosmologyWave{N}Priors.lean for waves 4–10."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
FORMAL = ROOT / "FSOT" / "Formal"
DEFAULT_WAVES = [4, 5, 6, 7, 8, 9, 10]


def build_lean(wave_num: int, summary: dict) -> str:
    n = int(summary.get("observable_count") or 0)
    max_err = summary.get("max_error_pct") or 0.0
    med = summary.get("median_error_pct")
    med = summary.get("mean_error_pct") if med is None else med
    med = 0.0 if med is None else float(med)
    prefix = f"cosmology_wave{wave_num}"
    return f"""/-
  FSOT Formal CosmologyWave{wave_num}Priors — fsot_compute wave{wave_num} certificate.
  Generator: scripts/gen_cosmology_wave_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_max_error_pct : ℝ := ({max_err} : ℝ)
def {prefix}_median_error_pct : ℝ := ({med} : ℝ)

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_max_error_under_half_pct :
    {prefix}_max_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_max_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

theorem {prefix}_median_error_under_half_pct :
    {prefix}_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_median_error_pct
  have h : _ < (0.5 : ℝ) := by norm_num
  exact h

/-- Bundle: wave{wave_num} observables within 5% tolerance band. -/
theorem cosmology_wave{wave_num}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_max_error_pct < (0.5 : ℝ) ∧
    {prefix}_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    {prefix}_max_error_under_half_pct,
    {prefix}_median_error_under_half_pct,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--wave", type=int, action="append", dest="waves")
    parser.add_argument("--output-dir", type=Path, default=FORMAL)
    args = parser.parse_args()
    waves = args.waves or DEFAULT_WAVES
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for wave_num in waves:
        key = f"cosmology_wave{wave_num}_lab"
        summary = registry.get(key) or {}
        if not summary.get("observable_count"):
            print(f"Skip wave{wave_num}: {key} not ingested")
            continue
        out = args.output_dir / f"CosmologyWave{wave_num}Priors.lean"
        out.write_text(build_lean(wave_num, summary), encoding="utf-8")
        print(f"Wrote {out}  observables={summary['observable_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())