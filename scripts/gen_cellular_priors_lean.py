#!/usr/bin/env python3
"""Generate FSOT/Formal/CellularPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "CellularPriors.lean"


def build_lean(registry: dict) -> str:
    c = registry.get("cellular_lab", {})
    soul = c.get("soul_records_processed", 234447)
    operons = c.get("evolution_operon_count", 13)
    bp = c.get("evolution_total_bp", 11395)
    return f"""/-
  FSOT Formal CellularPriors — Soul Simulator + mitochondrial evolution certificates.
  Generator: scripts/gen_cellular_priors_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

def cellular_soul_records_processed : ℕ := {soul}
def cellular_evolution_operon_count : ℕ := {operons}
def cellular_evolution_total_bp : ℕ := {bp}

theorem cellular_soul_records_pos : 0 < cellular_soul_records_processed := by
  unfold cellular_soul_records_processed; norm_num

theorem cellular_operon_count_pos : 0 < cellular_evolution_operon_count := by
  unfold cellular_evolution_operon_count; norm_num

/-- Bundle: cellular training corpus + mt operons with cellular-domain sign certificate. -/
theorem cellular_priors_bundle :
    cellular_soul_records_processed = {soul} ∧
    cellular_evolution_operon_count = {operons} ∧
    cellular_evolution_total_bp = {bp} ∧
    raw_S (get_domain_params "cellular") > 0 := by
  refine ⟨
    by unfold cellular_soul_records_processed; norm_num,
    by unfold cellular_evolution_operon_count; norm_num,
    by unfold cellular_evolution_total_bp; norm_num,
    lab_cellular_raw_S_positive
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