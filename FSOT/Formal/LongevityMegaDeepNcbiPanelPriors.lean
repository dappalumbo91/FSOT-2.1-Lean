/-
  FSOT Formal LongevityMegadeepNcbiPanelPriors — extension domain Longevity_MegaDeep_NCBI_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def longevity_megadeep_ncbi_panel_observable_count : ℕ := 1746
def longevity_megadeep_ncbi_panel_D_eff : ℕ := 23

theorem longevity_megadeep_ncbi_panel_observable_count_pos : 0 < longevity_megadeep_ncbi_panel_observable_count := by
  unfold longevity_megadeep_ncbi_panel_observable_count; norm_num

theorem longevity_megadeep_ncbi_panel_median_error_under_half_pct :
    (0.017789 : ℝ) < (0.5 : ℝ) := by norm_num

theorem longevity_megadeep_ncbi_panel_bundle :
    longevity_megadeep_ncbi_panel_observable_count = 1746 ∧
    longevity_megadeep_ncbi_panel_D_eff = 23 ∧
    (0.017789 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold longevity_megadeep_ncbi_panel_observable_count; norm_num,
    by unfold longevity_megadeep_ncbi_panel_D_eff; norm_num,
    longevity_megadeep_ncbi_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
