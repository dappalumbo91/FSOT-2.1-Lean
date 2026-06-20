#!/usr/bin/env python3
"""Generate FSOT/Formal/TrinaryFluidPriors.lean from trinary_fluid_computer registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "TrinaryFluidPriors.lean"


def build_lean(registry: dict) -> str:
    t = registry.get("trinary_fluid_computer", {})
    ignition = t.get("ignition_coherence", 0.3921734915875944)
    resonance = t.get("resonance_persist", 0.8652559794322651)
    pathways = t.get("metatron_pathways", 27)
    accuracy = t.get("engine_accuracy_pct", 99.3)

    return f"""/-
  FSOT Formal TrinaryFluidPriors — Trinary Fluid Computer v2 engine audit certificates.

  Source: FSOT_Trinary_Fluid_Computer_v2 audit constants
  Generator: scripts/gen_trinary_fluid_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def trinary_ignition_coherence : ℝ := ({ignition} : ℝ)
def trinary_resonance_persist : ℝ := ({resonance} : ℝ)
def trinary_metatron_pathways : ℕ := {pathways}
def trinary_engine_accuracy_pct : ℝ := ({accuracy} : ℝ)

theorem trinary_ignition_coherence_positive : (0 : ℝ) < trinary_ignition_coherence := by
  unfold trinary_ignition_coherence; norm_num

theorem trinary_resonance_persist_positive : (0 : ℝ) < trinary_resonance_persist := by
  unfold trinary_resonance_persist; norm_num

theorem trinary_metatron_pathways_pos : 0 < trinary_metatron_pathways := by
  unfold trinary_metatron_pathways; norm_num

/-- Bundle: Trinary Fluid v2 engine constants with consciousness-domain sign proxy. -/
theorem trinary_fluid_priors_bundle :
    trinary_ignition_coherence = ({ignition} : ℝ) ∧
    trinary_resonance_persist = ({resonance} : ℝ) ∧
    trinary_metatron_pathways = {pathways} ∧
    trinary_engine_accuracy_pct = ({accuracy} : ℝ) ∧
    raw_S (get_domain_params "consciousness") > 0 := by
  refine ⟨
    by unfold trinary_ignition_coherence; norm_num,
    by unfold trinary_resonance_persist; norm_num,
    by unfold trinary_metatron_pathways; norm_num,
    by unfold trinary_engine_accuracy_pct; norm_num,
    lab_consciousness_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TrinaryFluidPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())