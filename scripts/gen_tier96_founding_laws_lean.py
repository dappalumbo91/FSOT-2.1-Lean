#!/usr/bin/env python3
"""Generate Lean priors for Tier 96 founding-law extension panels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "law_11": (
        "founding_quantum_vacuum_panel",
        "FoundingQuantumVacuumPanelPriors",
        8,
        "founding_quantum_vacuum_panel_benchmark.json",
    ),
    "law_12": (
        "founding_cosmic_ray_panel",
        "FoundingCosmicRayPanelPriors",
        10,
        "founding_cosmic_ray_panel_benchmark.json",
    ),
    "law_13": (
        "founding_galactic_halo_rotation_panel",
        "FoundingGalacticHaloRotationPanelPriors",
        14,
        "founding_galactic_halo_rotation_panel_benchmark.json",
    ),
    "law_20": (
        "founding_cosmic_dust_panel",
        "FoundingCosmicDustPanelPriors",
        13,
        "founding_cosmic_dust_panel_benchmark.json",
    ),
    "law_23": (
        "founding_white_dwarf_cooling_panel",
        "FoundingWhiteDwarfCoolingPanelPriors",
        15,
        "founding_white_dwarf_cooling_panel_benchmark.json",
    ),
    "law_26": (
        "founding_atmospheric_ozone_panel",
        "FoundingAtmosphericOzonePanelPriors",
        12,
        "founding_atmospheric_ozone_panel_benchmark.json",
    ),
    "law_34": (
        "founding_pulsar_glitch_panel",
        "FoundingPulsarGlitchPanelPriors",
        16,
        "founding_pulsar_glitch_panel_benchmark.json",
    ),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int, law_id: str) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    law_name = str(bench.get("founding_law_name") or law_id)
    return f"""/-
  FSOT Formal {module_stem} — Tier 96 founding law panel ({law_id}: {law_name}).
  Generator: scripts/gen_tier96_founding_laws_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_founding_law_id : String := "{law_id}"
def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) ∧
    {prefix}_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · exact {prefix}_pooled_median_under_half_pct
  · exact {prefix}_beats_sota_headlines_pos

end
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(DOMAIN_CONFIG.keys()), action="append")
    args = parser.parse_args()
    targets = args.only or sorted(DOMAIN_CONFIG.keys())
    for law_id in targets:
        prefix, module_stem, d_eff, bench_name = DOMAIN_CONFIG[law_id]
        bench_path = DATA / bench_name
        if not bench_path.exists():
            print(f"Missing benchmark: {bench_path}", file=sys.stderr)
            return 1
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, prefix, module_stem, d_eff, law_id)
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())