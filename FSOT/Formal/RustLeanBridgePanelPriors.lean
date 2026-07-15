/-
  FSOT Formal RustLeanBridgePanelPriors — Tier 88 application wiring (Rust_Lean_Bridge_Panel).
  Generator: scripts/gen_tier88_application_wiring_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def rust_lean_bridge_observable_count : ℕ := 8
def rust_lean_bridge_median_error_pct : ℝ := (0.014767 : ℝ)
def rust_lean_bridge_D_eff : ℕ := 13

theorem rust_lean_bridge_observable_count_pos : 0 < rust_lean_bridge_observable_count := by
  unfold rust_lean_bridge_observable_count; norm_num

theorem rust_lean_bridge_median_error_under_five_pct :
    rust_lean_bridge_median_error_pct < (5 : ℝ) := by
  unfold rust_lean_bridge_median_error_pct; norm_num

theorem rust_lean_bridge_bundle :
    rust_lean_bridge_observable_count = 8 ∧
    rust_lean_bridge_D_eff = 13 ∧
    rust_lean_bridge_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "mathematical") > 0 := by
  refine ⟨
    by unfold rust_lean_bridge_observable_count; norm_num,
    by unfold rust_lean_bridge_D_eff; norm_num,
    rust_lean_bridge_median_error_under_five_pct,
    mathematical_raw_S_positive
  ⟩

end

end FSOT.Formal
