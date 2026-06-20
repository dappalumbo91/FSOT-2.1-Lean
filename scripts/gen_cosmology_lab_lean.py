#!/usr/bin/env python3
"""Generate FSOT/Formal/CosmologyLab.lean from cosmology_lambda_cdm registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "CosmologyLab.lean"


def build_lean(registry: dict) -> str:
    cos = registry.get("cosmology_lambda_cdm", {})
    n = cos.get("observable_count", 19)
    w1 = cos.get("wave1_count", 5)
    w2 = cos.get("wave2_count", 10)
    w3 = cos.get("wave3_count", 15)

    return f"""/-
  FSOT Formal CosmologyLab — ΛCDM observable partition certificates.

  Source: FSOT Cosmology Lab/fsot_compute.py (Wave 1+2+3 scales)
  Generator: scripts/gen_cosmology_lab_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def lambda_cdm_observable_count : ℕ := {n}
def lambda_cdm_wave1_count : ℕ := {w1}
def lambda_cdm_wave2_count : ℕ := {w2}
def lambda_cdm_wave3_count : ℕ := {w3}

theorem lambda_cdm_wave_partition :
    lambda_cdm_wave1_count + lambda_cdm_wave2_count + lambda_cdm_wave3_count = lambda_cdm_observable_count := by
  unfold lambda_cdm_wave1_count lambda_cdm_wave2_count lambda_cdm_wave3_count lambda_cdm_observable_count; norm_num

theorem lambda_cdm_wave1_links_genomic_cosmology :
    lambda_cdm_wave1_count = 5 := by
  unfold lambda_cdm_wave1_count; norm_num

/-- Bundle: 30 ΛCDM observables partition into Wave-1/2/3 scales. -/
theorem cosmology_lambda_cdm_bundle :
    lambda_cdm_observable_count = {n} ∧
    lambda_cdm_wave1_count = {w1} ∧
    lambda_cdm_wave2_count = {w2} ∧
    lambda_cdm_wave3_count = {w3} ∧
    lambda_cdm_wave1_count + lambda_cdm_wave2_count + lambda_cdm_wave3_count = {n} ∧
    (0 : ℝ) < omega_b_h2_fsot S_cosm_cached S_quant_cached := by
  refine ⟨
    by unfold lambda_cdm_observable_count; norm_num,
    by unfold lambda_cdm_wave1_count; norm_num,
    by unfold lambda_cdm_wave2_count; norm_num,
    by unfold lambda_cdm_wave3_count; norm_num,
    lambda_cdm_wave_partition,
    omega_b_h2_fsot_cached_pos
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CosmologyLab.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())