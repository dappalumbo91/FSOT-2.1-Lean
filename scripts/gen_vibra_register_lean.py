#!/usr/bin/env python3
"""Generate FSOT/Formal/VibRegisterPriors.lean from vibra_register registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "VibRegisterPriors.lean"


def build_lean(registry: dict) -> str:
    v = registry.get("vibra_register", {})
    d_eff = v.get("d_eff", 11)
    freq = v.get("base_freq_hz", 144.0)
    pat = v.get("pattern_stability", 0.766)
    s_mean = v.get("vib_S_mean", 0.474)
    mc_prob = v.get("mc_prob_non_decrease", 1.0)

    return f"""/-
  FSOT Formal VibRegisterPriors — VibraFSOT register + FSOTLean MC certificates.

  Source: VibraFSOT/artifacts/vibrafsot_final_progress.json + FSOTLean/fsot_mc_report.json
  Generator: scripts/gen_vibra_register_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def vibra_d_eff : ℕ := {d_eff}
def vibra_base_freq_hz : ℝ := ({freq} : ℝ)
def vibra_pattern_stability : ℝ := ({pat} : ℝ)
def vibra_avg_S_mean : ℝ := ({s_mean} : ℝ)
def vibra_mc_prob_non_decrease_cp5 : ℝ := ({mc_prob} : ℝ)

theorem vibra_pattern_stability_positive : (0 : ℝ) < vibra_pattern_stability := by
  unfold vibra_pattern_stability; norm_num

theorem vibra_avg_S_mean_positive : (0 : ℝ) < vibra_avg_S_mean := by
  unfold vibra_avg_S_mean; norm_num

theorem vibra_mc_prob_non_decrease_cp5_le_one :
    vibra_mc_prob_non_decrease_cp5 ≤ (1 : ℝ) := by
  unfold vibra_mc_prob_non_decrease_cp5; norm_num

/-- Bundle: VibraFSOT register at D_eff=11 with positive S and MC observer-stability alignment. -/
theorem vibra_register_bundle :
    vibra_d_eff = {d_eff} ∧
    vibra_base_freq_hz = ({freq} : ℝ) ∧
    vibra_pattern_stability = ({pat} : ℝ) ∧
    vibra_avg_S_mean = ({s_mean} : ℝ) ∧
    vibra_mc_prob_non_decrease_cp5 = ({mc_prob} : ℝ) ∧
    (0 : ℝ) < vibra_pattern_stability ∧
    (0 : ℝ) < vibra_avg_S_mean ∧
    raw_S (get_domain_params "ai") ≤ 0 := by
  refine ⟨
    by unfold vibra_d_eff; norm_num,
    by unfold vibra_base_freq_hz; norm_num,
    by unfold vibra_pattern_stability; norm_num,
    by unfold vibra_avg_S_mean; norm_num,
    by unfold vibra_mc_prob_non_decrease_cp5; norm_num,
    vibra_pattern_stability_positive,
    vibra_avg_S_mean_positive,
    ai_raw_S_non_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate VibRegisterPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())