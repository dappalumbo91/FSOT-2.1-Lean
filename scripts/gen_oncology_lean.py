#!/usr/bin/env python3
"""Generate FSOT/Formal/OncologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "oncology_manifest.yaml"
BENCH = ROOT / "data" / "oncology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "OncologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    sections = int(bench.get("section_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 14)
    source = cfg.get("source_repo", "vendor/oncology")
    sign = (cfg.get("lean") or {}).get("sign_theorems", ["medical_raw_S_positive"])[0]
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal OncologyPriors — SMILES drug/enzyme + biology strict bridge.
  Generator: scripts/gen_oncology_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def oncology_observable_count : ℕ := {n}
def oncology_section_count : ℕ := {sections}
def oncology_D_eff : ℕ := {d_eff}
def oncology_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def oncology_headline_median_error_pct : ℝ := ({headline} : ℝ)
def oncology_beats_sota_headlines : ℕ := {beats}

theorem oncology_observable_count_pos : 0 < oncology_observable_count := by
  unfold oncology_observable_count; norm_num

theorem oncology_section_count_pos : 0 < oncology_section_count := by
  unfold oncology_section_count; norm_num

theorem oncology_pooled_median_under_five_pct :
    oncology_pooled_median_error_pct < (5 : ℝ) := by
  unfold oncology_pooled_median_error_pct; norm_num

theorem oncology_headline_median_under_five_pct :
    oncology_headline_median_error_pct < (5 : ℝ) := by
  unfold oncology_headline_median_error_pct; norm_num

theorem oncology_beats_sota_headlines_pos : 0 < oncology_beats_sota_headlines := by
  unfold oncology_beats_sota_headlines; norm_num

theorem oncology_bundle :
    oncology_observable_count = {n} ∧
    oncology_section_count = {sections} ∧
    oncology_D_eff = {d_eff} ∧
    oncology_pooled_median_error_pct < (5 : ℝ) ∧
    oncology_headline_median_error_pct < (5 : ℝ) ∧
    0 < oncology_beats_sota_headlines ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold oncology_observable_count; norm_num,
    by unfold oncology_section_count; norm_num,
    by unfold oncology_D_eff; norm_num,
    oncology_pooled_median_under_five_pct,
    oncology_headline_median_under_five_pct,
    oncology_beats_sota_headlines_pos,
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