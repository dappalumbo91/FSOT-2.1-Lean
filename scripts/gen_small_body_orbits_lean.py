#!/usr/bin/env python3
"""Generate FSOT/Formal/SmallBodyOrbitsPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "small_body_orbits_manifest.yaml"
BENCH = ROOT / "data" / "small_body_orbits_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "SmallBodyOrbitsPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    d_eff = int(bench.get("D_eff") or 18)
    sign = cfg.get("lean", {}).get("sign_theorem", "astronomical_raw_S_positive")
    return f"""/-
  FSOT Formal SmallBodyOrbitsPriors — Moon/asteroid/comet JPL orbit checks.
  Generator: scripts/gen_small_body_orbits_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def small_body_orbit_count : ℕ := {n}
def small_body_median_error_pct : ℝ := ({med} : ℝ)
def small_body_D_eff : ℕ := {d_eff}

theorem small_body_orbit_count_pos : 0 < small_body_orbit_count := by
  unfold small_body_orbit_count; norm_num

theorem small_body_median_error_under_eight_pct :
    small_body_median_error_pct < (8 : ℝ) := by
  unfold small_body_median_error_pct; norm_num

theorem small_body_orbits_bundle :
    small_body_orbit_count = {n} ∧
    small_body_D_eff = {d_eff} ∧
    small_body_median_error_pct < (8 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold small_body_orbit_count; norm_num,
    by unfold small_body_D_eff; norm_num,
    small_body_median_error_under_eight_pct,
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