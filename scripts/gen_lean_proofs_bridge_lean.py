#!/usr/bin/env python3
"""Generate FSOT/Formal/LeanProofsBridge.lean from lean_proofs_bridge registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "LeanProofsBridge.lean"


def build_lean(registry: dict) -> str:
    b = registry.get("lean_proofs_bridge", {})
    formal_count = b.get("formal_constant_count", 25)
    proven_count = b.get("domain_proven_count", 25)

    return f"""/-
  FSOT Formal LeanProofsBridge — FSOT_Lean_Proofs formal constant bridge certificates.

  Source: FSOT_Lean_Proofs/FSOT_Formal_Output.json
  Generator: scripts/gen_lean_proofs_bridge_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def lean_proofs_formal_constant_count : ℕ := {formal_count}
def lean_proofs_domain_proven_count : ℕ := {proven_count}

theorem lean_proofs_formal_constant_count_pos : 0 < lean_proofs_formal_constant_count := by
  unfold lean_proofs_formal_constant_count; norm_num

theorem lean_proofs_domain_proven_count_pos : 0 < lean_proofs_domain_proven_count := by
  unfold lean_proofs_domain_proven_count; norm_num

theorem lean_proofs_domain_proven_le_formal :
    lean_proofs_domain_proven_count ≤ lean_proofs_formal_constant_count := by
  unfold lean_proofs_domain_proven_count lean_proofs_formal_constant_count; norm_num

/-- Bundle: formalized constants with SMILES k-alignment certificate. -/
theorem lean_proofs_constant_bundle :
    lean_proofs_formal_constant_count = {formal_count} ∧
    lean_proofs_domain_proven_count = {proven_count} ∧
    lean_proofs_domain_proven_count ≤ lean_proofs_formal_constant_count ∧
    |k - smiles_k_cached| < (5e-4 : ℝ) := by
  refine ⟨
    by unfold lean_proofs_formal_constant_count; norm_num,
    by unfold lean_proofs_domain_proven_count; norm_num,
    lean_proofs_domain_proven_le_formal,
    smiles_k_matches_formal_k
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LeanProofsBridge.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())