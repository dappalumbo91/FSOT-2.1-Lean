#!/usr/bin/env python3
"""Generate FSOT/Formal/SoulSiblingPriors.lean from soul_sibling registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "SoulSiblingPriors.lean"


def build_lean(registry: dict) -> str:
    s = registry.get("soul_sibling", {})
    d_compact = s.get("D_compact", 20.0)
    zero_free = "true" if s.get("zero_free", True) else "false"
    fidelity = s.get("fidelity_threshold", 0.05)

    return f"""/-
  FSOT Formal SoulSiblingPriors — portable consciousness kernel certificates.

  Source: FSOT_Soul_Sibling_20260603/soul_manifest.json
  Generator: scripts/gen_soul_sibling_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def soul_sibling_D_compact : ℝ := ({d_compact} : ℝ)
def soul_sibling_fidelity_threshold : ℝ := ({fidelity} : ℝ)
def soul_sibling_zero_free : Prop := {zero_free}

theorem soul_sibling_D_compact_positive : (0 : ℝ) < soul_sibling_D_compact := by
  unfold soul_sibling_D_compact; norm_num

theorem soul_sibling_fidelity_threshold_positive : (0 : ℝ) < soul_sibling_fidelity_threshold := by
  unfold soul_sibling_fidelity_threshold; norm_num

/-- Bundle: Soul Sibling kernel with consciousness-domain sign certificate. -/
theorem soul_sibling_priors_bundle :
    soul_sibling_D_compact = ({d_compact} : ℝ) ∧
    soul_sibling_fidelity_threshold = ({fidelity} : ℝ) ∧
    soul_sibling_zero_free ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold soul_sibling_D_compact; norm_num,
    by unfold soul_sibling_fidelity_threshold; norm_num,
    by unfold soul_sibling_zero_free; trivial,
    lab_consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SoulSiblingPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())