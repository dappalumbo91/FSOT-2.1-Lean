#!/usr/bin/env python3
"""Generate FSOT.Formal.WarpBhWhPortalPriors from warp BH/WH portal benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FORMAL = ROOT / "FSOT" / "Formal"
BENCH = DATA / "warp_bh_wh_portal_benchmark.json"
LEGACY_FORMULA = Path(
    r"C:\Users\damia\Desktop\FSOT-Legacy-Physics-Connections\concept_refinement\warp_actuation_formula_fsot21.json"
)


def _r(v: float) -> str:
    return f"({v} : ℝ)"


def build_lean(bench: dict, steps: dict) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)

    return f"""/-
  FSOT Formal WarpBhWhPortalPriors — Tier 78 BH/WH micro-portal + entanglement gate.
  Generator: scripts/gen_warp_bh_wh_portal_lean.py

  Synthetic stabilized blackhole↔whitehole doorway (user theory) crosswalked to:
  - BlackHoleThesisPriors (28/28 BH thermo observables)
  - Warp actuation stabilization band (Λ_stab > 1)
  - Quantum entanglement gate pair (φ_lock² · |S_QM|²)
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

/-! ## Panel certificates -/

def warp_bh_wh_portal_observable_count : ℕ := {n}
def warp_bh_wh_portal_pooled_median_error_pct : ℝ := {_r(pooled)}
def warp_bh_wh_portal_headline_median_error_pct : ℝ := {_r(headline)}
def warp_bh_wh_portal_beats_sota_headlines : ℕ := {beats}
def warp_bh_wh_portal_D_eff : ℕ := 29

/-! ## BH/WH doorway scalars (Steps 9–11) -/

def warp_psi_bh_inlet : ℝ := {_r(float(steps.get("psi_bh_inlet", 0)))}
def warp_psi_wh_outlet : ℝ := {_r(float(steps.get("psi_wh_outlet", 0)))}
def warp_psi_portal_doorway : ℝ := {_r(float(steps.get("psi_portal_doorway", 0)))}
def warp_info_preservation_proxy : ℝ := {_r(float(steps.get("info_preservation_proxy", 0)))}
def warp_psi_entangle_gate : ℝ := {_r(float(steps.get("psi_entangle_gate", 0)))}
def warp_psi_gate_pair : ℝ := {_r(float(steps.get("psi_gate_pair", 0)))}
def warp_psi_traverse : ℝ := {_r(float(steps.get("psi_traverse", 0)))}
def warp_stabilization_margin_portal : ℝ := {_r(float(steps.get("stabilization_margin", 0)))}

/-! ## Positivity + portal certificates -/

theorem warp_bh_wh_portal_observable_count_pos : 0 < warp_bh_wh_portal_observable_count := by
  unfold warp_bh_wh_portal_observable_count; norm_num

theorem warp_bh_wh_portal_pooled_under_half_pct :
    warp_bh_wh_portal_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold warp_bh_wh_portal_pooled_median_error_pct; norm_num

theorem warp_psi_bh_inlet_pos : (0 : ℝ) < warp_psi_bh_inlet := by
  unfold warp_psi_bh_inlet; norm_num

theorem warp_psi_wh_outlet_pos : (0 : ℝ) < warp_psi_wh_outlet := by
  unfold warp_psi_wh_outlet; norm_num

theorem warp_psi_portal_doorway_pos : (0 : ℝ) < warp_psi_portal_doorway := by
  unfold warp_psi_portal_doorway; norm_num

theorem warp_info_preservation_pos : (0 : ℝ) < warp_info_preservation_proxy := by
  unfold warp_info_preservation_proxy; norm_num

theorem warp_psi_entangle_gate_pos : (0 : ℝ) < warp_psi_entangle_gate := by
  unfold warp_psi_entangle_gate; norm_num

theorem warp_psi_traverse_pos : (0 : ℝ) < warp_psi_traverse := by
  unfold warp_psi_traverse; norm_num

theorem warp_portal_stabilization_margin_gt_one :
    (1 : ℝ) < warp_stabilization_margin_portal := by
  unfold warp_stabilization_margin_portal; norm_num

theorem warp_bh_wh_linked_to_blackhole_domain :
    (0 : ℝ) < raw_S (get_domain_params "blackhole") := by
  exact blackhole_raw_S_positive

theorem warp_bh_wh_portal_bundle :
    warp_bh_wh_portal_observable_count = {n} ∧
    warp_bh_wh_portal_pooled_median_error_pct < (0.5 : ℝ) ∧
    (0 : ℝ) < warp_psi_portal_doorway ∧
    (0 : ℝ) < warp_psi_entangle_gate ∧
    (1 : ℝ) < warp_stabilization_margin_portal ∧
    (0 : ℝ) < raw_S (get_domain_params "blackhole") := by
  refine ⟨?h1, ?h2, ?h3, ?h4, ?h5, ?h6⟩
  · unfold warp_bh_wh_portal_observable_count; norm_num
  · exact warp_bh_wh_portal_pooled_under_half_pct
  · exact warp_psi_portal_doorway_pos
  · exact warp_psi_entangle_gate_pos
  · exact warp_portal_stabilization_margin_gt_one
  · exact blackhole_raw_S_positive

end
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--formula", type=Path, default=LEGACY_FORMULA)
    parser.add_argument("--output", type=Path, default=FORMAL / "WarpBhWhPortalPriors.lean")
    args = parser.parse_args()

    if not args.bench.exists():
        print(f"Run build_warp_bh_wh_portal_benchmark.py first: {args.bench}", file=sys.stderr)
        return 1
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    steps = {}
    if args.formula.exists():
        steps = json.loads(args.formula.read_text(encoding="utf-8")).get("formula_steps") or {}
    args.output.write_text(build_lean(bench, steps), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())