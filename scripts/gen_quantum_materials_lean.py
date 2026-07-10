#!/usr/bin/env python3
"""Generate FSOT/Formal/QuantumMaterialsPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "quantum_materials_manifest.yaml"
BENCH = ROOT / "data" / "quantum_materials_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "QuantumMaterialsPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    sections = int(bench.get("section_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    d_eff = int(bench.get("D_eff") or cfg.get("D_eff") or 16)
    source = cfg.get("source_repo", "vendor/smiles")
    sign = (cfg.get("lean") or {}).get("sign_theorems", ["material_raw_S_positive"])[0]
    beats = sum(
        1
        for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values()
        if v
    )
    return f"""/-
  FSOT Formal QuantumMaterialsPriors — condensed-matter SMILES observables.
  Generator: scripts/gen_quantum_materials_lean.py
  Source: {source}
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def quantum_materials_observable_count : ℕ := {n}
def quantum_materials_section_count : ℕ := {sections}
def quantum_materials_D_eff : ℕ := {d_eff}
def quantum_materials_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def quantum_materials_headline_median_error_pct : ℝ := ({headline} : ℝ)
def quantum_materials_beats_sota_headlines : ℕ := {beats}

theorem quantum_materials_observable_count_pos : 0 < quantum_materials_observable_count := by
  unfold quantum_materials_observable_count; norm_num

theorem quantum_materials_section_count_pos : 0 < quantum_materials_section_count := by
  unfold quantum_materials_section_count; norm_num

theorem quantum_materials_pooled_median_under_half_pct :
    quantum_materials_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_materials_pooled_median_error_pct; norm_num

theorem quantum_materials_headline_median_under_half_pct :
    quantum_materials_headline_median_error_pct < (0.5 : ℝ) := by
  unfold quantum_materials_headline_median_error_pct; norm_num

theorem quantum_materials_beats_sota_headlines_pos : 0 < quantum_materials_beats_sota_headlines := by
  unfold quantum_materials_beats_sota_headlines; norm_num

/-- Bundle: Quantum Materials condensed-matter SMILES depth with material/quantum maps. -/
theorem quantum_materials_bundle :
    quantum_materials_observable_count = {n} ∧
    quantum_materials_section_count = {sections} ∧
    quantum_materials_D_eff = {d_eff} ∧
    quantum_materials_pooled_median_error_pct < (0.5 : ℝ) ∧
    quantum_materials_headline_median_error_pct < (0.5 : ℝ) ∧
    0 < quantum_materials_beats_sota_headlines ∧
    raw_S (get_domain_params "material") > 0 := by
  refine ⟨
    by unfold quantum_materials_observable_count; norm_num,
    by unfold quantum_materials_section_count; norm_num,
    by unfold quantum_materials_D_eff; norm_num,
    quantum_materials_pooled_median_under_half_pct,
    quantum_materials_headline_median_under_half_pct,
    quantum_materials_beats_sota_headlines_pos,
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
    if not args.bench.exists():
        raise FileNotFoundError(f"Run build_quantum_materials_benchmark.py first: {args.bench}")
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())