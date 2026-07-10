#!/usr/bin/env python3
"""Generate FSOT/Formal/SyntheticBiologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "synthetic_biology_manifest.yaml"
BENCH = ROOT / "data" / "synthetic_biology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "SyntheticBiologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    d_eff = int(cfg.get("D_eff", 14))
    sign = cfg.get("lean", {}).get("sign_theorem", "biological_raw_S_positive")
    return f"""/-
  FSOT Formal SyntheticBiologyPriors — evolution operons + biology strict bridge.
  Generator: scripts/gen_synthetic_biology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def synthetic_biology_observable_count : ℕ := {n}
def synthetic_biology_median_error_pct : ℝ := ({med} : ℝ)
def synthetic_biology_D_eff : ℕ := {d_eff}

theorem synthetic_biology_observable_count_pos : 0 < synthetic_biology_observable_count := by
  unfold synthetic_biology_observable_count; norm_num

theorem synthetic_biology_median_error_under_half_pct :
    synthetic_biology_median_error_pct < (0.5 : ℝ) := by
  unfold synthetic_biology_median_error_pct; norm_num

theorem synthetic_biology_bundle :
    synthetic_biology_observable_count = {n} ∧
    synthetic_biology_D_eff = {d_eff} ∧
    synthetic_biology_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold synthetic_biology_observable_count; norm_num,
    by unfold synthetic_biology_D_eff; norm_num,
    synthetic_biology_median_error_under_half_pct,
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