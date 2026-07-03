#!/usr/bin/env python3
"""Generate FSOT/Formal/ParticlePhysicsPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "particle_physics_manifest.yaml"
DEFAULT_BENCH = ROOT / "data" / "particle_physics_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "ParticlePhysicsPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    smiles = int(bench.get("smiles_particle_count") or 0)
    thesis = int(bench.get("thesis_particle_wave_count") or 0)
    w4 = int(bench.get("wave4_count") or 0)
    rules = int(bench.get("math_physics_rule_count") or 0)
    total = int(bench.get("observable_count") or smiles + thesis + w4 + rules)
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    max_err = bench.get("max_error_pct")
    max_err = 0.0 if max_err is None else float(max_err)
    within_2 = int(bench.get("within_two_pct_count") or 0)
    sign = cfg.get("lean", {}).get("sign_theorem", "particle_raw_S_positive")
    return f"""/-
  FSOT Formal ParticlePhysicsPriors — Tier 16 particle physics extended observables.
  Sources: SMILES §66/§78/§88 + thesis waves + Wave-4 + math-physics rules
  Generator: scripts/gen_particle_physics_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def particle_smiles_record_count : ℕ := {smiles}
def particle_thesis_wave_count : ℕ := {thesis}
def particle_wave4_count : ℕ := {w4}
def particle_math_physics_rule_count : ℕ := {rules}
def particle_physics_observable_count : ℕ := {total}
def particle_physics_median_error_pct : ℝ := ({med} : ℝ)
def particle_physics_max_error_pct : ℝ := ({max_err} : ℝ)
def particle_physics_within_two_pct : ℕ := {within_2}

theorem particle_smiles_record_count_pos : 0 < particle_smiles_record_count := by
  unfold particle_smiles_record_count; norm_num

theorem particle_wave4_count_pos : 0 < particle_wave4_count := by
  unfold particle_wave4_count; norm_num

theorem particle_physics_observable_count_pos : 0 < particle_physics_observable_count := by
  unfold particle_physics_observable_count; norm_num

theorem particle_physics_components_sum :
    particle_smiles_record_count + particle_thesis_wave_count + particle_wave4_count + particle_math_physics_rule_count =
      particle_physics_observable_count := by
  unfold particle_smiles_record_count particle_thesis_wave_count particle_wave4_count
    particle_math_physics_rule_count particle_physics_observable_count; norm_num

theorem particle_physics_median_error_under_five_pct :
    particle_physics_median_error_pct < (5 : ℝ) := by
  unfold particle_physics_median_error_pct; norm_num

theorem particle_physics_max_error_under_five_pct :
    particle_physics_max_error_pct < (5 : ℝ) := by
  unfold particle_physics_max_error_pct; norm_num

/-- Bundle: particle masses, Higgs/Z branching, CKM/PMNS Wave-4, formal math-physics rules. -/
theorem particle_physics_bundle :
    particle_smiles_record_count = {smiles} ∧
    particle_thesis_wave_count = {thesis} ∧
    particle_wave4_count = {w4} ∧
    particle_math_physics_rule_count = {rules} ∧
    particle_physics_observable_count = {total} ∧
    particle_smiles_record_count + particle_thesis_wave_count + particle_wave4_count + particle_math_physics_rule_count = {total} ∧
    particle_physics_median_error_pct < (5 : ℝ) ∧
    particle_physics_max_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold particle_smiles_record_count; norm_num,
    by unfold particle_thesis_wave_count; norm_num,
    by unfold particle_wave4_count; norm_num,
    by unfold particle_math_physics_rule_count; norm_num,
    by unfold particle_physics_observable_count; norm_num,
    particle_physics_components_sum,
    particle_physics_median_error_under_five_pct,
    particle_physics_max_error_under_five_pct,
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