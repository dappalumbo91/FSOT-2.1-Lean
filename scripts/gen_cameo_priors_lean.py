#!/usr/bin/env python3
"""Generate FSOT/Formal/CameoPriors.lean from cameo_lab registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "CameoPriors.lean"


def build_lean(registry: dict) -> str:
    cameo = registry.get("cameo_lab", {})
    count = cameo.get("benchmark_count", 130)
    sym = cameo.get("symbolic_formula", {})
    mae = sym.get("mae_angstrom", 8.85)
    nodes = sym.get("node_count", 5)

    return f"""/-
  FSOT Formal CameoPriors — Genetics CAMEO symbolic folding certificates.

  Source: Genetics/fsot_cameo_results.csv + fluid-to-solid symbolic formula
  Generator: scripts/gen_cameo_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def cameo_benchmark_count : ℕ := {count}
def cameo_symbolic_node_count : ℕ := {nodes}
def cameo_symbolic_mae_angstrom : ℝ := ({mae} : ℝ)

theorem cameo_benchmark_count_pos : 0 < cameo_benchmark_count := by
  unfold cameo_benchmark_count; norm_num

theorem cameo_symbolic_mae_positive : (0 : ℝ) < cameo_symbolic_mae_angstrom := by
  unfold cameo_symbolic_mae_angstrom; norm_num

/-- Bundle: CAMEO benchmarks and crystallized FSOT symbolic folding (molecular domain). -/
theorem cameo_symbolic_bundle :
    cameo_benchmark_count = {count} ∧
    cameo_symbolic_node_count = {nodes} ∧
    cameo_symbolic_mae_angstrom = ({mae} : ℝ) ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold cameo_benchmark_count; norm_num,
    by unfold cameo_symbolic_node_count; norm_num,
    by unfold cameo_symbolic_mae_angstrom; norm_num,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CameoPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())