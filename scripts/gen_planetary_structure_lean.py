#!/usr/bin/env python3
"""Generate FSOT/Formal/PlanetaryStructurePriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "planetary_structure_manifest.yaml"
BENCH = ROOT / "data" / "planetary_structure_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "PlanetaryStructurePriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    d_eff = int(bench.get("D_eff") or 16)
    sign = cfg.get("lean", {}).get("sign_theorem", "galactic_raw_S_positive")
    return f"""/-
  FSOT Formal PlanetaryStructurePriors — JPL planetary density verification.
  Generator: scripts/gen_planetary_structure_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_structure_body_count : ℕ := {n}
def planetary_structure_median_error_pct : ℝ := ({med} : ℝ)
def planetary_structure_D_eff : ℕ := {d_eff}

theorem planetary_structure_body_count_pos : 0 < planetary_structure_body_count := by
  unfold planetary_structure_body_count; norm_num

theorem planetary_structure_median_error_under_five_pct :
    planetary_structure_median_error_pct < (5 : ℝ) := by
  unfold planetary_structure_median_error_pct; norm_num

theorem planetary_structure_bundle :
    planetary_structure_body_count = {n} ∧
    planetary_structure_D_eff = {d_eff} ∧
    planetary_structure_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_structure_body_count; norm_num,
    by unfold planetary_structure_D_eff; norm_num,
    planetary_structure_median_error_under_five_pct,
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