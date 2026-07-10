#!/usr/bin/env python3
"""Generate FSOT/Formal/BubbleBleedPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_bubble_bleed_manifest.yaml"
BENCH = ROOT / "data" / "cosmology_bubble_bleed_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "BubbleBleedPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    neb = int(bench.get("nebula_count") or 0)
    frb = int(bench.get("frb_count") or 0)
    h0 = int(bench.get("h0_sector_count") or 0)
    fw = int(bench.get("nebula_framework_count") or neb)
    wh = int(bench.get("nebula_wh_closure_count") or neb)
    bh_spin = int(bench.get("bh_spin_closure_count") or 0)
    p34 = int(bench.get("frb_p34_count") or 0)
    total = int(bench.get("observable_count") or neb + frb + h0)
    neb_match = int(bench.get("nebula_within_5pct_count") or 0)
    fw_match = int(bench.get("nebula_framework_fit_count") or 0)
    wh_match = int(bench.get("nebula_wh_closure_match_count") or 0)
    bh_match = int(bench.get("bh_spin_closure_match_count") or 0)
    frb_match = int(bench.get("frb_classifier_match_count") or 0)
    neb_rate = float(bench.get("nebula_match_rate") or 0.0)
    fw_rate = float(bench.get("nebula_framework_fit_rate") or 0.0)
    wh_rate = float(bench.get("nebula_wh_closure_match_rate") or 0.0)
    bh_rate = float(bench.get("bh_spin_closure_match_rate") or 0.0)
    frb_rate = float(bench.get("frb_classifier_match_rate") or 0.0)
    frb_fp_rate = float(bench.get("frb_classifier_fp_rate") or 0.0)
    bleed = float(bench.get("bubble_bleed_fraction") or 0.015431)
    obs_ratio = float((bench.get("observability") or {}).get("implied_nebula_pairing_ratio") or 0.0)
    sign = cfg.get("lean", {}).get("sign_theorem", "h0_fsot_cached_approx_value")
    return f"""/-
  FSOT Formal BubbleBleedPriors — BH→WH outgassing bubble bleed lab.
  Nebula framework fit, WH closure/suction, BH spin, FRB classifier, sector H₀.
  Generator: scripts/gen_bubble_bleed_priors_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def bubble_bleed_nebula_count : ℕ := {neb}
def bubble_bleed_frb_count : ℕ := {frb}
def bubble_bleed_h0_sector_count : ℕ := {h0}
def bubble_bleed_framework_count : ℕ := {fw}
def bubble_bleed_wh_closure_count : ℕ := {wh}
def bubble_bleed_bh_spin_count : ℕ := {bh_spin}
def bubble_bleed_frb_p34_count : ℕ := {p34}
def bubble_bleed_observable_count : ℕ := {total}
def bubble_bleed_nebula_match_count : ℕ := {neb_match}
def bubble_bleed_framework_fit_count : ℕ := {fw_match}
def bubble_bleed_wh_closure_match_count : ℕ := {wh_match}
def bubble_bleed_bh_spin_match_count : ℕ := {bh_match}
def bubble_bleed_frb_match_count : ℕ := {frb_match}
def bubble_bleed_fraction : ℝ := ({bleed} : ℝ)
def bubble_bleed_observability_ratio : ℝ := ({obs_ratio} : ℝ)
def bubble_bleed_nebula_match_rate : ℝ := ({neb_rate} : ℝ)
def bubble_bleed_framework_fit_rate : ℝ := ({fw_rate} : ℝ)
def bubble_bleed_wh_closure_match_rate : ℝ := ({wh_rate} : ℝ)
def bubble_bleed_bh_spin_match_rate : ℝ := ({bh_rate} : ℝ)
def bubble_bleed_frb_match_rate : ℝ := ({frb_rate} : ℝ)
def bubble_bleed_frb_fp_rate : ℝ := ({frb_fp_rate} : ℝ)

theorem bubble_bleed_nebula_count_pos : 0 < bubble_bleed_nebula_count := by
  unfold bubble_bleed_nebula_count; norm_num

theorem bubble_bleed_frb_count_pos : 0 < bubble_bleed_frb_count := by
  unfold bubble_bleed_frb_count; norm_num

theorem bubble_bleed_observable_count_pos : 0 < bubble_bleed_observable_count := by
  unfold bubble_bleed_observable_count; norm_num

theorem bubble_bleed_framework_fit_le_total :
    bubble_bleed_framework_fit_count ≤ bubble_bleed_framework_count := by
  unfold bubble_bleed_framework_fit_count bubble_bleed_framework_count; norm_num

theorem bubble_bleed_wh_closure_match_le_total :
    bubble_bleed_wh_closure_match_count ≤ bubble_bleed_wh_closure_count := by
  unfold bubble_bleed_wh_closure_match_count bubble_bleed_wh_closure_count; norm_num

theorem bubble_bleed_bh_spin_match_le_total :
    bubble_bleed_bh_spin_match_count ≤ bubble_bleed_bh_spin_count := by
  unfold bubble_bleed_bh_spin_match_count bubble_bleed_bh_spin_count; norm_num

theorem bubble_bleed_nebula_match_le_total :
    bubble_bleed_nebula_match_count ≤ bubble_bleed_nebula_count := by
  unfold bubble_bleed_nebula_match_count bubble_bleed_nebula_count; norm_num

theorem bubble_bleed_frb_match_le_total :
    bubble_bleed_frb_match_count ≤ bubble_bleed_frb_count := by
  unfold bubble_bleed_frb_match_count bubble_bleed_frb_count; norm_num

theorem bubble_bleed_observability_ratio_nonneg :
    0 ≤ bubble_bleed_observability_ratio := by
  unfold bubble_bleed_observability_ratio; norm_num

/-- Bundle: BH→WH mechanics — framework fit, WH closure, spin, FRB, sector H₀ bleed. -/
theorem bubble_bleed_bundle :
    bubble_bleed_nebula_count = {neb} ∧
    bubble_bleed_frb_count = {frb} ∧
    bubble_bleed_h0_sector_count = {h0} ∧
    bubble_bleed_framework_count = {fw} ∧
    bubble_bleed_wh_closure_count = {wh} ∧
    bubble_bleed_bh_spin_count = {bh_spin} ∧
    bubble_bleed_observable_count = {total} ∧
    bubble_bleed_framework_fit_count ≤ bubble_bleed_framework_count ∧
    bubble_bleed_wh_closure_match_count ≤ bubble_bleed_wh_closure_count ∧
    bubble_bleed_bh_spin_match_count ≤ bubble_bleed_bh_spin_count ∧
    bubble_bleed_nebula_match_count ≤ bubble_bleed_nebula_count ∧
    bubble_bleed_frb_match_count ≤ bubble_bleed_frb_count ∧
    0 ≤ bubble_bleed_observability_ratio ∧
    |h0_fsot S_cosm_cached - h0_fsot_canonical| < (0.11 : ℝ) := by
  refine ⟨
    by unfold bubble_bleed_nebula_count; norm_num,
    by unfold bubble_bleed_frb_count; norm_num,
    by unfold bubble_bleed_h0_sector_count; norm_num,
    by unfold bubble_bleed_framework_count; norm_num,
    by unfold bubble_bleed_wh_closure_count; norm_num,
    by unfold bubble_bleed_bh_spin_count; norm_num,
    by unfold bubble_bleed_observable_count; norm_num,
    bubble_bleed_framework_fit_le_total,
    bubble_bleed_wh_closure_match_le_total,
    bubble_bleed_bh_spin_match_le_total,
    bubble_bleed_nebula_match_le_total,
    bubble_bleed_frb_match_le_total,
    bubble_bleed_observability_ratio_nonneg,
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