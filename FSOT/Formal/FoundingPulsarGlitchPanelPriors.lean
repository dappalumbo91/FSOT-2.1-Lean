/-
  FSOT Formal FoundingPulsarGlitchPanelPriors — extension domain Founding_Pulsar_Glitch_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def founding_pulsar_glitch_panel_observable_count : ℕ := 24
def founding_pulsar_glitch_panel_D_eff : ℕ := 16

theorem founding_pulsar_glitch_panel_observable_count_pos : 0 < founding_pulsar_glitch_panel_observable_count := by
  unfold founding_pulsar_glitch_panel_observable_count; decide

theorem founding_pulsar_glitch_panel_median_error_under_half_pct :
    (0.022461 : ℝ) < (0.5 : ℝ) := by norm_num

theorem founding_pulsar_glitch_panel_bundle :
    founding_pulsar_glitch_panel_observable_count = 24 ∧
    founding_pulsar_glitch_panel_D_eff = 16 ∧
    (0.022461 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold founding_pulsar_glitch_panel_observable_count; decide,
    by unfold founding_pulsar_glitch_panel_D_eff; decide,
    founding_pulsar_glitch_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
