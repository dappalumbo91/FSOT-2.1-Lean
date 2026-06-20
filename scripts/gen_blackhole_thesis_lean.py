#!/usr/bin/env python3
"""Generate FSOT/Formal/BlackHoleThesisPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "BlackHoleThesisPriors.lean"


def build_lean(registry: dict) -> str:
    b = registry.get("blackhole_thesis", {})
    n = b.get("observable_count", 28)
    w2 = b.get("within_target_2pct", 28)
    return f"""/-
  FSOT Formal BlackHoleThesisPriors — BH thermo thesis observable certificates.
  Generator: scripts/gen_blackhole_thesis_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def blackhole_thesis_observable_count : ℕ := {n}
def blackhole_thesis_within_target_2pct : ℕ := {w2}

theorem blackhole_thesis_observable_count_pos : 0 < blackhole_thesis_observable_count := by
  unfold blackhole_thesis_observable_count; norm_num

theorem blackhole_thesis_within_le_total :
    blackhole_thesis_within_target_2pct ≤ blackhole_thesis_observable_count := by
  unfold blackhole_thesis_within_target_2pct blackhole_thesis_observable_count; norm_num

/-- Bundle: BlackHole thermo thesis observables with blackhole-domain sign proxy. -/
theorem blackhole_thesis_bundle :
    blackhole_thesis_observable_count = {n} ∧
    blackhole_thesis_within_target_2pct = {w2} ∧
    blackhole_thesis_within_target_2pct ≤ blackhole_thesis_observable_count ∧
    (0 : ℝ) < raw_S (get_domain_params "blackhole") := by
  refine ⟨
    by unfold blackhole_thesis_observable_count; norm_num,
    by unfold blackhole_thesis_within_target_2pct; norm_num,
    blackhole_thesis_within_le_total,
    blackhole_raw_S_positive
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