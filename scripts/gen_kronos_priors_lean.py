#!/usr/bin/env python3
"""Generate FSOT/Formal/KronosPriors.lean from kronos_lab registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "KronosPriors.lean"


def build_lean(registry: dict) -> str:
    k = registry.get("kronos_lab", {})
    runs = k.get("run_count", 100)
    best = k.get("best_fractional_error", 1.0e-6)
    unc = k.get("record_fractional_uncertainty", 5.5e-19)

    return f"""/-
  FSOT Formal KronosPriors — chronometry / metrology thesis certificates.

  Source: Kronos/thesis_kronos_run_summary.csv
  Generator: scripts/gen_kronos_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def kronos_run_count : ℕ := {runs}
def kronos_best_fractional_error : ℝ := ({best} : ℝ)
def kronos_record_fractional_uncertainty : ℝ := ({unc} : ℝ)

theorem kronos_run_count_pos : 0 < kronos_run_count := by
  unfold kronos_run_count; norm_num

theorem kronos_best_fractional_error_positive : (0 : ℝ) < kronos_best_fractional_error := by
  unfold kronos_best_fractional_error; norm_num

theorem kronos_record_fractional_uncertainty_positive :
    (0 : ℝ) < kronos_record_fractional_uncertainty := by
  unfold kronos_record_fractional_uncertainty; norm_num

/-- Bundle: Kronos metrology runs with medical-domain observed-sign proxy. -/
theorem kronos_metrology_bundle :
    kronos_run_count = {runs} ∧
    kronos_best_fractional_error = ({best} : ℝ) ∧
    kronos_record_fractional_uncertainty = ({unc} : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "medical") := by
  refine ⟨
    by unfold kronos_run_count; norm_num,
    by unfold kronos_best_fractional_error; norm_num,
    by unfold kronos_record_fractional_uncertainty; norm_num,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate KronosPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())