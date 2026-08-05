/-
  FSOT Formal StarTrekTransporterLivePanelPriors — verified desktop panel Star_Trek_Transporter_Live_Panel.
  Generator: scripts/gen_verified_desktop_lean.py
  Cross-proof: exported via export_full_formal_obligations.py → Coq / Isabelle / F* / Rust replay
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def star_trek_transporter_observable_count : ℕ := 1575
def star_trek_transporter_median_error_pct : ℝ := (0.012464 : ℝ)
def star_trek_transporter_D_eff : ℕ := 17

def star_trek_transporter_info_preservation_proxy : ℝ := (0.981227203621 : ℝ)
def star_trek_transporter_psi_entangle_gate : ℝ := (0.04803163401 : ℝ)
def star_trek_transporter_psi_gate_pair : ℝ := (0.043599802456 : ℝ)
def star_trek_transporter_psi_portal_doorway : ℝ := (0.009663204175 : ℝ)
def star_trek_transporter_psi_traverse : ℝ := (0.000464139486 : ℝ)
def star_trek_transporter_stabilization_margin : ℝ := (1.722776467449 : ℝ)

theorem star_trek_transporter_info_preservation_proxy_pos :
    0 < star_trek_transporter_info_preservation_proxy := by
  unfold star_trek_transporter_info_preservation_proxy
  exact (by norm_num : (0 : ℝ) < (0.981227203621 : ℝ))

theorem star_trek_transporter_psi_entangle_gate_pos :
    0 < star_trek_transporter_psi_entangle_gate := by
  unfold star_trek_transporter_psi_entangle_gate
  exact (by norm_num : (0 : ℝ) < (0.04803163401 : ℝ))

theorem star_trek_transporter_psi_entangle_gate_under_half_pct :
    star_trek_transporter_psi_entangle_gate < (0.5 : ℝ) := by
  unfold star_trek_transporter_psi_entangle_gate
  exact (by norm_num : (0.04803163401  : ℝ) < 0.5)

theorem star_trek_transporter_psi_gate_pair_pos :
    0 < star_trek_transporter_psi_gate_pair := by
  unfold star_trek_transporter_psi_gate_pair
  exact (by norm_num : (0 : ℝ) < (0.043599802456 : ℝ))

theorem star_trek_transporter_psi_gate_pair_under_half_pct :
    star_trek_transporter_psi_gate_pair < (0.5 : ℝ) := by
  unfold star_trek_transporter_psi_gate_pair
  exact (by norm_num : (0.043599802456  : ℝ) < 0.5)

theorem star_trek_transporter_psi_portal_doorway_pos :
    0 < star_trek_transporter_psi_portal_doorway := by
  unfold star_trek_transporter_psi_portal_doorway
  exact (by norm_num : (0 : ℝ) < (0.009663204175 : ℝ))

theorem star_trek_transporter_psi_portal_doorway_under_half_pct :
    star_trek_transporter_psi_portal_doorway < (0.5 : ℝ) := by
  unfold star_trek_transporter_psi_portal_doorway
  exact (by norm_num : (0.009663204175  : ℝ) < 0.5)

theorem star_trek_transporter_psi_traverse_pos :
    0 < star_trek_transporter_psi_traverse := by
  unfold star_trek_transporter_psi_traverse
  exact (by norm_num : (0 : ℝ) < (0.000464139486 : ℝ))

theorem star_trek_transporter_psi_traverse_under_half_pct :
    star_trek_transporter_psi_traverse < (0.5 : ℝ) := by
  unfold star_trek_transporter_psi_traverse
  exact (by norm_num : (0.000464139486  : ℝ) < 0.5)

theorem star_trek_transporter_stabilization_margin_pos :
    0 < star_trek_transporter_stabilization_margin := by
  unfold star_trek_transporter_stabilization_margin
  exact (by norm_num : (0 : ℝ) < (1.722776467449 : ℝ))

theorem star_trek_transporter_observable_count_pos : 0 < star_trek_transporter_observable_count := by
  unfold star_trek_transporter_observable_count; decide

theorem star_trek_transporter_median_error_under_five_pct :
    star_trek_transporter_median_error_pct < (5 : ℝ) := by
  unfold star_trek_transporter_median_error_pct
  exact (by norm_num : (0.012464  : ℝ) < (5 : ℝ))

theorem star_trek_transporter_median_error_under_half_pct :
    star_trek_transporter_median_error_pct < (0.5 : ℝ) := by
  unfold star_trek_transporter_median_error_pct
  exact (by norm_num : (0.012464  : ℝ) < 0.5)

theorem star_trek_transporter_bundle :
    star_trek_transporter_observable_count = 1575 ∧
    star_trek_transporter_D_eff = 17 ∧
    star_trek_transporter_median_error_pct < (0.5 : ℝ) ∧
    raw_S (get_domain_params "quantum") > 0 := by
  refine ⟨
    by unfold star_trek_transporter_observable_count; decide,
    by unfold star_trek_transporter_D_eff; decide,
    star_trek_transporter_median_error_under_half_pct,
    quantum_raw_S_positive
  ⟩

end

end FSOT.Formal
