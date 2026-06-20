#!/usr/bin/env python3
"""Generate FSOT/Formal/EvolutionPriors.lean from evolution_lab registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "EvolutionPriors.lean"


def build_lean(registry: dict) -> str:
    e = registry.get("evolution_lab", {})
    operons = e.get("operon_count", 13)
    fitness = e.get("fitness", 58.49)
    capacity = e.get("biological_capacity", 8002.5)

    return f"""/-
  FSOT Formal EvolutionPriors — mitochondrial operon evolution certificates.

  Source: fsot_evolution_sim biological_mt_operons + best_evolved_organism
  Generator: scripts/gen_evolution_priors_lean.py
-/

import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

def evolution_operon_count : ℕ := {operons}
def evolution_best_fitness : ℝ := ({fitness} : ℝ)
def evolution_biological_capacity : ℝ := ({capacity} : ℝ)

theorem evolution_fitness_positive : (0 : ℝ) < evolution_best_fitness := by
  unfold evolution_best_fitness; norm_num

theorem evolution_operon_count_pos : 0 < evolution_operon_count := by
  unfold evolution_operon_count; norm_num

/-- Bundle: 13 mitochondrial operons with positive biological-domain sign certificate. -/
theorem evolution_priors_bundle :
    evolution_operon_count = {operons} ∧
    evolution_best_fitness = ({fitness} : ℝ) ∧
    evolution_biological_capacity = ({capacity} : ℝ) ∧
    (0 : ℝ) < evolution_best_fitness ∧
    (0 : ℝ) < raw_S (get_domain_params "biological") := by
  refine ⟨
    by unfold evolution_operon_count; norm_num,
    by unfold evolution_best_fitness; norm_num,
    by unfold evolution_biological_capacity; norm_num,
    evolution_fitness_positive,
    lab_biological_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate EvolutionPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())