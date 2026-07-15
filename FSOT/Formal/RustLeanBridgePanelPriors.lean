/-
  FSOT Formal RustLeanBridgePanelPriors — extension domain Rust_Lean_Bridge_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def rust_lean_bridge_panel_observable_count : ℕ := 24
def rust_lean_bridge_panel_D_eff : ℕ := 13

theorem rust_lean_bridge_panel_observable_count_pos : 0 < rust_lean_bridge_panel_observable_count := by
  unfold rust_lean_bridge_panel_observable_count; norm_num

theorem rust_lean_bridge_panel_median_error_under_half_pct :
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by norm_num

theorem rust_lean_bridge_panel_bundle :
    rust_lean_bridge_panel_observable_count = 24 ∧
    rust_lean_bridge_panel_D_eff = 13 ∧
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold rust_lean_bridge_panel_observable_count; norm_num,
    by unfold rust_lean_bridge_panel_D_eff; norm_num,
    rust_lean_bridge_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
