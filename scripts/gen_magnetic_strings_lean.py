#!/usr/bin/env python3
"""Generate FSOT/Formal/MagneticStringPriors.lean from magnetic_strings registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "MagneticStringPriors.lean"


def build_lean(registry: dict) -> str:
    m = registry.get("magnetic_strings", {})
    n = m.get("string_count", 250)
    s_em = m.get("S_em", 0.519)
    aligned = m.get("top_aligned_count", 75)

    return f"""/-
  FSOT Formal MagneticStringPriors — magnetic string lattice certificates.

  Source: fsot_magnetic_string_sim/fsot_magnetic_strings_final.json
  Generator: scripts/gen_magnetic_strings_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def magnetic_string_count : ℕ := {n}
def magnetic_top_aligned_count : ℕ := {aligned}
def magnetic_S_em : ℝ := ({s_em} : ℝ)

theorem magnetic_S_em_positive : (0 : ℝ) < magnetic_S_em := by
  unfold magnetic_S_em; norm_num

theorem magnetic_string_count_pos : 0 < magnetic_string_count := by
  unfold magnetic_string_count; norm_num

/-- Bundle: 250-string lattice with positive electromagnetic scalar (electron domain). -/
theorem magnetic_string_bundle :
    magnetic_string_count = {n} ∧
    magnetic_top_aligned_count = {aligned} ∧
    magnetic_S_em = ({s_em} : ℝ) ∧
    (0 : ℝ) < magnetic_S_em ∧
    (0 : ℝ) < raw_S (get_domain_params "electron") := by
  refine ⟨
    by unfold magnetic_string_count; norm_num,
    by unfold magnetic_top_aligned_count; norm_num,
    by unfold magnetic_S_em; norm_num,
    magnetic_S_em_positive,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MagneticStringPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())