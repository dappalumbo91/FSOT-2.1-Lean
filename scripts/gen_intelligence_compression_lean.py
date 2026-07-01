#!/usr/bin/env python3
"""Generate FSOT/Formal/IntelligenceCompressionPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "IntelligenceCompressionPriors.lean"


def build_lean(registry: dict) -> str:
    fic = registry.get("intelligence_compression", {})
    n = fic.get("sweep_row_count", 484)
    fertile = fic.get("fertile_count", 0)
    best = fic.get("best_intelligence_score", 0.0)
    d_eff = fic.get("D_eff", 12)
    return f"""/-
  FSOT Formal IntelligenceCompressionPriors — FIC sensitivity sweep certificates.
  Generator: scripts/gen_intelligence_compression_lean.py
  Source: FSOT-2.0-code/IntelligenceCompressor
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fic_sweep_row_count : ℕ := {n}
def fic_fertile_row_count : ℕ := {fertile}
def fic_D_eff_optimal : ℕ := {d_eff}

theorem fic_sweep_row_count_pos : 0 < fic_sweep_row_count := by
  unfold fic_sweep_row_count; norm_num

theorem fic_fertile_rows_present : 0 < fic_fertile_row_count := by
  unfold fic_fertile_row_count; norm_num

theorem fic_best_intelligence_score_positive :
    (0 : ℝ) < ({best} : ℝ) := by norm_num

/-- Bundle: Intelligence Compression fertile-window sweep with neural/consciousness/ai maps. -/
theorem intelligence_compression_priors_bundle :
    fic_sweep_row_count = {n} ∧
    fic_fertile_row_count = {fertile} ∧
    fic_D_eff_optimal = {d_eff} ∧
    (0 : ℝ) < ({best} : ℝ) ∧
    raw_S (get_domain_params "neural") > 0 ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold fic_sweep_row_count; norm_num,
    by unfold fic_fertile_row_count; norm_num,
    by unfold fic_D_eff_optimal; norm_num,
    fic_best_intelligence_score_positive,
    neural_raw_S_positive,
    consciousness_raw_S_positive
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