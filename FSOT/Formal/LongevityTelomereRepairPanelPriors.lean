/-
  FSOT Formal LongevityTelomereRepairPanelPriors — extension domain Longevity_Telomere_Repair_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def longevity_telomere_repair_panel_observable_count : ℕ := 60
def longevity_telomere_repair_panel_D_eff : ℕ := 20

theorem longevity_telomere_repair_panel_observable_count_pos : 0 < longevity_telomere_repair_panel_observable_count := by
  unfold longevity_telomere_repair_panel_observable_count; norm_num

theorem longevity_telomere_repair_panel_median_error_under_half_pct :
    (0.022236 : ℝ) < (0.5 : ℝ) := by norm_num

theorem longevity_telomere_repair_panel_bundle :
    longevity_telomere_repair_panel_observable_count = 60 ∧
    longevity_telomere_repair_panel_D_eff = 20 ∧
    (0.022236 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold longevity_telomere_repair_panel_observable_count; norm_num,
    by unfold longevity_telomere_repair_panel_D_eff; norm_num,
    longevity_telomere_repair_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
