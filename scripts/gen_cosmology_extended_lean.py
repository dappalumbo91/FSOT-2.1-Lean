#!/usr/bin/env python3
"""Generate FSOT/Formal/CosmologyExtendedPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_extended_manifest.yaml"
DEFAULT_BENCH = ROOT / "data" / "cosmology_extended_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "CosmologyExtendedPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    sk = int(bench.get("skeleton_derivation_count") or 0)
    lc = int(bench.get("lambda_cdm_count") or 0)
    th = int(bench.get("thesis_cosmology_wave_count") or 0)
    total = int(bench.get("observable_count") or sk + lc + th)
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    within = int(bench.get("within_five_pct_count") or 0)
    sign = cfg.get("lean", {}).get("sign_theorem", "omega_b_h2_fsot_cached_pos")
    return f"""/-
  FSOT Formal CosmologyExtendedPriors — Tier 16 cosmology extended observables.
  Sources: Skeleton Key DB + ΛCDM + thesis cosmology waves
  Generator: scripts/gen_cosmology_extended_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_skeleton_derivation_count : ℕ := {sk}
def cosmology_lambda_cdm_extended_count : ℕ := {lc}
def cosmology_thesis_wave_count : ℕ := {th}
def cosmology_extended_observable_count : ℕ := {total}
def cosmology_extended_median_error_pct : ℝ := ({med} : ℝ)
def cosmology_extended_within_five_pct : ℕ := {within}

theorem cosmology_skeleton_derivation_count_pos : 0 < cosmology_skeleton_derivation_count := by
  unfold cosmology_skeleton_derivation_count; norm_num

theorem cosmology_lambda_cdm_extended_count_pos : 0 < cosmology_lambda_cdm_extended_count := by
  unfold cosmology_lambda_cdm_extended_count; norm_num

theorem cosmology_extended_observable_count_pos : 0 < cosmology_extended_observable_count := by
  unfold cosmology_extended_observable_count; norm_num

theorem cosmology_extended_components_sum :
    cosmology_skeleton_derivation_count + cosmology_lambda_cdm_extended_count + cosmology_thesis_wave_count =
      cosmology_extended_observable_count := by
  unfold cosmology_skeleton_derivation_count cosmology_lambda_cdm_extended_count
    cosmology_thesis_wave_count cosmology_extended_observable_count; norm_num

theorem cosmology_extended_median_error_under_five_pct :
    cosmology_extended_median_error_pct < (5 : ℝ) := by
  unfold cosmology_extended_median_error_pct; norm_num

theorem cosmology_extended_within_le_total :
    cosmology_extended_within_five_pct ≤ cosmology_extended_observable_count := by
  unfold cosmology_extended_within_five_pct cosmology_extended_observable_count; norm_num

/-- Bundle: CMB/BBN/rotation-curve skeleton + ΛCDM + thesis cosmology waves. -/
theorem cosmology_extended_bundle :
    cosmology_skeleton_derivation_count = {sk} ∧
    cosmology_lambda_cdm_extended_count = {lc} ∧
    cosmology_thesis_wave_count = {th} ∧
    cosmology_extended_observable_count = {total} ∧
    cosmology_skeleton_derivation_count + cosmology_lambda_cdm_extended_count + cosmology_thesis_wave_count = {total} ∧
    cosmology_extended_median_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold cosmology_skeleton_derivation_count; norm_num,
    by unfold cosmology_lambda_cdm_extended_count; norm_num,
    by unfold cosmology_thesis_wave_count; norm_num,
    by unfold cosmology_extended_observable_count; norm_num,
    cosmology_extended_components_sum,
    cosmology_extended_median_error_under_five_pct,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bench = json.loads(args.benchmark.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())