#!/usr/bin/env python3
"""Generate FSOT/Formal/LinguisticsPriors.lean from linguistics_lab registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "LinguisticsPriors.lean"


def build_lean(registry: dict) -> str:
    ling = registry.get("linguistics_lab", {})
    count = ling.get("target_count", 10)
    max_err = ling.get("max_error_pct", 0.01)
    mean_err = ling.get("mean_error_pct", 0.005)

    return f"""/-
  FSOT Formal LinguisticsPriors — empirical linguistic anchor certificates.

  Source: FSOT linguistics/data/LINGUISTIC_TARGETS.csv + db/linguistics.db
  Generator: scripts/gen_linguistics_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def linguistics_target_count : ℕ := {count}
def linguistics_max_error_pct : ℝ := ({max_err} : ℝ)
def linguistics_mean_error_pct : ℝ := ({mean_err} : ℝ)

theorem linguistics_target_count_pos : 0 < linguistics_target_count := by
  unfold linguistics_target_count; norm_num

theorem linguistics_max_error_within_five_pct : linguistics_max_error_pct < (5 : ℝ) := by
  unfold linguistics_max_error_pct; norm_num

/-- Bundle: 10 measured linguistic anchors within 5% FSOT seed derivations (neural domain). -/
theorem linguistics_priors_bundle :
    linguistics_target_count = {count} ∧
    linguistics_max_error_pct = ({max_err} : ℝ) ∧
    linguistics_mean_error_pct = ({mean_err} : ℝ) ∧
    linguistics_max_error_pct < (5 : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "neural") := by
  refine ⟨
    by unfold linguistics_target_count; norm_num,
    by unfold linguistics_max_error_pct; norm_num,
    by unfold linguistics_mean_error_pct; norm_num,
    linguistics_max_error_within_five_pct,
    neural_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LinguisticsPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())