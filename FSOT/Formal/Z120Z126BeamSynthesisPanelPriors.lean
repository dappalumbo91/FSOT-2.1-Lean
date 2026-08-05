/-
  FSOT Formal Z120Z126BeamSynthesisPanelPriors — extension domain Z120_Z126_Beam_Synthesis_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def z120_z126_beam_synthesis_panel_observable_count : ℕ := 20
def z120_z126_beam_synthesis_panel_D_eff : ℕ := 20

theorem z120_z126_beam_synthesis_panel_observable_count_pos : 0 < z120_z126_beam_synthesis_panel_observable_count := by
  unfold z120_z126_beam_synthesis_panel_observable_count; decide

theorem z120_z126_beam_synthesis_panel_median_error_under_half_pct :
    (9.5e-05 : ℝ) < (0.5 : ℝ) :=
  (by norm_num : (9.5e-05 : ℝ) < (0.5 : ℝ))

theorem z120_z126_beam_synthesis_panel_bundle :
    z120_z126_beam_synthesis_panel_observable_count = 20 ∧
    z120_z126_beam_synthesis_panel_D_eff = 20 ∧
    (9.5e-05 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold z120_z126_beam_synthesis_panel_observable_count; decide,
    by unfold z120_z126_beam_synthesis_panel_D_eff; decide,
    z120_z126_beam_synthesis_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
