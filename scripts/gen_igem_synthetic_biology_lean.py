#!/usr/bin/env python3
"""Generate FSOT/Formal/IGEMSyntheticBiologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "igem_synthetic_biology_manifest.yaml"
BENCH = ROOT / "data" / "igem_synthetic_biology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "IGEMSyntheticBiologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    parts = int(bench.get("part_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 14)
    source = cfg.get("source_repo", "vendor/igem")
    sign = (cfg.get("lean") or {}).get("sign_theorem", "biological_raw_S_positive")
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal IGEMSyntheticBiologyPriors — iGEM parts-registry strict-empirical bridge.
  Generator: scripts/gen_igem_synthetic_biology_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def igem_synthetic_biology_observable_count : ℕ := {n}
def igem_synthetic_biology_part_count : ℕ := {parts}
def igem_synthetic_biology_D_eff : ℕ := {d_eff}
def igem_synthetic_biology_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def igem_synthetic_biology_headline_median_error_pct : ℝ := ({headline} : ℝ)
def igem_synthetic_biology_beats_sota_headlines : ℕ := {beats}

theorem igem_synthetic_biology_observable_count_pos : 0 < igem_synthetic_biology_observable_count := by
  unfold igem_synthetic_biology_observable_count; norm_num

theorem igem_synthetic_biology_part_count_pos : 0 < igem_synthetic_biology_part_count := by
  unfold igem_synthetic_biology_part_count; norm_num

theorem igem_synthetic_biology_pooled_median_under_half_pct :
    igem_synthetic_biology_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold igem_synthetic_biology_pooled_median_error_pct; norm_num

theorem igem_synthetic_biology_headline_median_under_half_pct :
    igem_synthetic_biology_headline_median_error_pct < (0.5 : ℝ) := by
  unfold igem_synthetic_biology_headline_median_error_pct; norm_num

theorem igem_synthetic_biology_beats_sota_headlines_pos : 0 < igem_synthetic_biology_beats_sota_headlines := by
  unfold igem_synthetic_biology_beats_sota_headlines; norm_num

theorem igem_synthetic_biology_bundle :
    igem_synthetic_biology_observable_count = {n} ∧
    igem_synthetic_biology_part_count = {parts} ∧
    igem_synthetic_biology_D_eff = {d_eff} ∧
    igem_synthetic_biology_pooled_median_error_pct < (0.5 : ℝ) ∧
    igem_synthetic_biology_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < igem_synthetic_biology_beats_sota_headlines ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold igem_synthetic_biology_observable_count; norm_num,
    by unfold igem_synthetic_biology_part_count; norm_num,
    by unfold igem_synthetic_biology_D_eff; norm_num,
    igem_synthetic_biology_pooled_median_under_half_pct,
    igem_synthetic_biology_headline_median_under_half_pct,
    igem_synthetic_biology_beats_sota_headlines_pos,
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