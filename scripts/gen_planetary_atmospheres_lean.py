#!/usr/bin/env python3
"""Generate FSOT/Formal/PlanetaryAtmospheresPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "planetary_atmospheres_manifest.yaml"
BENCH = ROOT / "data" / "planetary_atmospheres_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "PlanetaryAtmospheresPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    bodies = int(bench.get("body_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 16)
    source = cfg.get("source_repo", "vendor/planetary_atmospheres")
    sign = (cfg.get("lean") or {}).get("sign_theorems", ["galactic_raw_S_positive"])[0]
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal PlanetaryAtmospheresPriors — FSOT-adjusted JPL/NASA atmosphere observables.
  Generator: scripts/gen_planetary_atmospheres_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def planetary_atmospheres_observable_count : ℕ := {n}
def planetary_atmospheres_body_count : ℕ := {bodies}
def planetary_atmospheres_D_eff : ℕ := {d_eff}
def planetary_atmospheres_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def planetary_atmospheres_headline_median_error_pct : ℝ := ({headline} : ℝ)
def planetary_atmospheres_beats_sota_headlines : ℕ := {beats}

theorem planetary_atmospheres_observable_count_pos : 0 < planetary_atmospheres_observable_count := by
  unfold planetary_atmospheres_observable_count; norm_num

theorem planetary_atmospheres_body_count_pos : 0 < planetary_atmospheres_body_count := by
  unfold planetary_atmospheres_body_count; norm_num

theorem planetary_atmospheres_pooled_median_under_half_pct :
    planetary_atmospheres_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold planetary_atmospheres_pooled_median_error_pct; norm_num

theorem planetary_atmospheres_headline_median_under_half_pct :
    planetary_atmospheres_headline_median_error_pct < (0.5 : ℝ) := by
  unfold planetary_atmospheres_headline_median_error_pct; norm_num

theorem planetary_atmospheres_beats_sota_headlines_pos : 0 < planetary_atmospheres_beats_sota_headlines := by
  unfold planetary_atmospheres_beats_sota_headlines; norm_num

theorem planetary_atmospheres_bundle :
    planetary_atmospheres_observable_count = {n} ∧
    planetary_atmospheres_body_count = {bodies} ∧
    planetary_atmospheres_D_eff = {d_eff} ∧
    planetary_atmospheres_pooled_median_error_pct < (0.5 : ℝ) ∧
    planetary_atmospheres_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < planetary_atmospheres_beats_sota_headlines ∧
    raw_S (get_domain_params "galactic") > 0 := by
  refine ⟨
    by unfold planetary_atmospheres_observable_count; norm_num,
    by unfold planetary_atmospheres_body_count; norm_num,
    by unfold planetary_atmospheres_D_eff; norm_num,
    planetary_atmospheres_pooled_median_under_half_pct,
    planetary_atmospheres_headline_median_under_half_pct,
    planetary_atmospheres_beats_sota_headlines_pos,
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