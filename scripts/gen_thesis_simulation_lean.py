#!/usr/bin/env python3
"""Generate FSOT/Formal/ThesisSimulationPriors.lean from thesis simulation benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "thesis_simulation_manifest.yaml"
DEFAULT_BENCH = ROOT / "data" / "thesis_simulation_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "ThesisSimulationPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    waves = int(bench.get("wave_target_count") or 0)
    intrinsic = int(bench.get("intrinsic_screen_count") or 0)
    total = int(bench.get("observable_count") or waves + intrinsic)
    wave_files = int(bench.get("wave_file_count") or 0)
    best_rmse = bench.get("intrinsic_best_rmse")
    best_rmse = 0.0 if best_rmse is None else float(best_rmse)
    sign = cfg.get("lean", {}).get("sign_theorem", "particle_raw_S_positive")
    return f"""/-
  FSOT Formal ThesisSimulationPriors — Tier 15 thesis simulation lab observables.
  Source: data/thesis_simulation_benchmark.json (wave7–10 + intrinsic screens)
  Generator: scripts/gen_thesis_simulation_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def thesis_wave_target_count : ℕ := {waves}
def thesis_intrinsic_screen_count : ℕ := {intrinsic}
def thesis_simulation_observable_count : ℕ := {total}
def thesis_wave_file_count : ℕ := {wave_files}
def thesis_intrinsic_best_rmse : ℝ := ({best_rmse} : ℝ)

theorem thesis_wave_target_count_pos : 0 < thesis_wave_target_count := by
  unfold thesis_wave_target_count; norm_num

theorem thesis_intrinsic_screen_count_pos : 0 < thesis_intrinsic_screen_count := by
  unfold thesis_intrinsic_screen_count; norm_num

theorem thesis_simulation_observable_count_pos : 0 < thesis_simulation_observable_count := by
  unfold thesis_simulation_observable_count; norm_num

theorem thesis_intrinsic_best_rmse_positive : (0 : ℝ) < thesis_intrinsic_best_rmse := by
  unfold thesis_intrinsic_best_rmse; norm_num

theorem thesis_simulation_components_le_total :
    thesis_wave_target_count + thesis_intrinsic_screen_count = thesis_simulation_observable_count := by
  unfold thesis_wave_target_count thesis_intrinsic_screen_count thesis_simulation_observable_count; norm_num

/-- Bundle: wave observations + intrinsic formula screens with particle-domain sign proxy. -/
theorem thesis_simulation_bundle :
    thesis_wave_target_count = {waves} ∧
    thesis_intrinsic_screen_count = {intrinsic} ∧
    thesis_simulation_observable_count = {total} ∧
    thesis_wave_file_count = {wave_files} ∧
    thesis_wave_target_count + thesis_intrinsic_screen_count = thesis_simulation_observable_count ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold thesis_wave_target_count; norm_num,
    by unfold thesis_intrinsic_screen_count; norm_num,
    by unfold thesis_simulation_observable_count; norm_num,
    by unfold thesis_wave_file_count; norm_num,
    thesis_simulation_components_le_total,
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