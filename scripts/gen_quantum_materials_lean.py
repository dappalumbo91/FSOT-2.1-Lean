#!/usr/bin/env python3
"""Generate FSOT/Formal/QuantumMaterialsPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "quantum_materials_manifest.yaml"
BENCH = ROOT / "data" / "quantum_materials_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "QuantumMaterialsPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    d_eff = int(cfg.get("D_eff", 16))
    sign = cfg.get("lean", {}).get("sign_theorem", "material_raw_S_positive")
    return f"""/-
  FSOT Formal QuantumMaterialsPriors — condensed-matter SMILES observables.
  Generator: scripts/gen_quantum_materials_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_materials_observable_count : ℕ := {n}
def quantum_materials_median_error_pct : ℝ := ({med} : ℝ)
def quantum_materials_D_eff : ℕ := {d_eff}

theorem quantum_materials_observable_count_pos : 0 < quantum_materials_observable_count := by
  unfold quantum_materials_observable_count; norm_num

theorem quantum_materials_median_error_under_five_pct :
    quantum_materials_median_error_pct < (5 : ℝ) := by
  unfold quantum_materials_median_error_pct; norm_num

theorem quantum_materials_bundle :
    quantum_materials_observable_count = {n} ∧
    quantum_materials_D_eff = {d_eff} ∧
    quantum_materials_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold quantum_materials_observable_count; norm_num,
    by unfold quantum_materials_D_eff; norm_num,
    quantum_materials_median_error_under_five_pct,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())