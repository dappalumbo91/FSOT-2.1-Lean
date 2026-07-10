#!/usr/bin/env python3
"""Generate FSOT/Formal/NeuroimmunologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "neuroimmunology_manifest.yaml"
BENCH = ROOT / "data" / "neuroimmunology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "NeuroimmunologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    sections = int(bench.get("section_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 14)
    source = cfg.get("source_repo", "vendor/neuroimmunology")
    sign = (cfg.get("lean") or {}).get("sign_theorems", ["medical_raw_S_positive"])[0]
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal NeuroimmunologyPriors — immunology SMILES + neuron cohort strata.
  Generator: scripts/gen_neuroimmunology_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def neuroimmunology_observable_count : ℕ := {n}
def neuroimmunology_section_count : ℕ := {sections}
def neuroimmunology_D_eff : ℕ := {d_eff}
def neuroimmunology_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def neuroimmunology_headline_median_error_pct : ℝ := ({headline} : ℝ)
def neuroimmunology_beats_sota_headlines : ℕ := {beats}

theorem neuroimmunology_observable_count_pos : 0 < neuroimmunology_observable_count := by
  unfold neuroimmunology_observable_count; norm_num

theorem neuroimmunology_section_count_pos : 0 < neuroimmunology_section_count := by
  unfold neuroimmunology_section_count; norm_num

theorem neuroimmunology_pooled_median_under_five_pct :
    neuroimmunology_pooled_median_error_pct < (5 : ℝ) := by
  unfold neuroimmunology_pooled_median_error_pct; norm_num

theorem neuroimmunology_headline_median_under_five_pct :
    neuroimmunology_headline_median_error_pct < (5 : ℝ) := by
  unfold neuroimmunology_headline_median_error_pct; norm_num

theorem neuroimmunology_beats_sota_headlines_pos : 0 < neuroimmunology_beats_sota_headlines := by
  unfold neuroimmunology_beats_sota_headlines; norm_num

theorem neuroimmunology_bundle :
    neuroimmunology_observable_count = {n} ∧
    neuroimmunology_section_count = {sections} ∧
    neuroimmunology_D_eff = {d_eff} ∧
    neuroimmunology_pooled_median_error_pct < (5 : ℝ) ∧
    neuroimmunology_headline_median_error_pct < (5 : ℝ) ∧
    0 < neuroimmunology_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold neuroimmunology_observable_count; norm_num,
    by unfold neuroimmunology_section_count; norm_num,
    by unfold neuroimmunology_D_eff; norm_num,
    neuroimmunology_pooled_median_under_five_pct,
    neuroimmunology_headline_median_under_five_pct,
    neuroimmunology_beats_sota_headlines_pos,
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