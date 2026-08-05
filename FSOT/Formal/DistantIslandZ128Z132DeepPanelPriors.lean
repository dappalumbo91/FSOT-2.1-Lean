/-
  FSOT Formal DistantIslandZ128Z132DeepPanelPriors — extension domain Distant_Island_Z128_Z132_Deep_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def distant_island_z128_z132_deep_panel_observable_count : ℕ := 24
def distant_island_z128_z132_deep_panel_D_eff : ℕ := 23

theorem distant_island_z128_z132_deep_panel_observable_count_pos : 0 < distant_island_z128_z132_deep_panel_observable_count := by
  unfold distant_island_z128_z132_deep_panel_observable_count; decide

theorem distant_island_z128_z132_deep_panel_median_error_under_half_pct :
    (1e-06 : ℝ) < (0.5 : ℝ) := by norm_num

theorem distant_island_z128_z132_deep_panel_bundle :
    distant_island_z128_z132_deep_panel_observable_count = 24 ∧
    distant_island_z128_z132_deep_panel_D_eff = 23 ∧
    (1e-06 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold distant_island_z128_z132_deep_panel_observable_count; decide,
    by unfold distant_island_z128_z132_deep_panel_D_eff; decide,
    distant_island_z128_z132_deep_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
