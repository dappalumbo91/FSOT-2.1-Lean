#!/usr/bin/env python3
"""Generate FSOT/Formal/GeochemistryPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "geochemistry_manifest.yaml"
BENCH = ROOT / "data" / "geochemistry_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "GeochemistryPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    d_eff = int(cfg.get("D_eff", 15))
    sign = cfg.get("lean", {}).get("sign_theorem", "galactic_raw_S_positive")
    return f"""/-
  FSOT Formal GeochemistryPriors — SMILES mineral/geo + planetary bulk density.
  Generator: scripts/gen_geochemistry_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def geochemistry_observable_count : ℕ := {n}
def geochemistry_median_error_pct : ℝ := ({med} : ℝ)
def geochemistry_D_eff : ℕ := {d_eff}

theorem geochemistry_observable_count_pos : 0 < geochemistry_observable_count := by
  unfold geochemistry_observable_count; norm_num

theorem geochemistry_median_error_under_five_pct :
    geochemistry_median_error_pct < (5 : ℝ) := by
  unfold geochemistry_median_error_pct; norm_num

theorem geochemistry_bundle :
    geochemistry_observable_count = {n} ∧
    geochemistry_D_eff = {d_eff} ∧
    geochemistry_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold geochemistry_observable_count; norm_num,
    by unfold geochemistry_D_eff; norm_num,
    geochemistry_median_error_under_five_pct,
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