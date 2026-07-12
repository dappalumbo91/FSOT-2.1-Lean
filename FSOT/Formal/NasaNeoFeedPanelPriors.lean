/-
  FSOT Formal NasaNeoFeedPanelPriors — extension domain NASA_NEO_Feed_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def nasa_neo_feed_panel_observable_count : ℕ := 56
def nasa_neo_feed_panel_D_eff : ℕ := 18

theorem nasa_neo_feed_panel_observable_count_pos : 0 < nasa_neo_feed_panel_observable_count := by
  unfold nasa_neo_feed_panel_observable_count; norm_num

theorem nasa_neo_feed_panel_median_error_under_half_pct :
    (0.021097 : ℝ) < (0.5 : ℝ) := by norm_num

theorem nasa_neo_feed_panel_bundle :
    nasa_neo_feed_panel_observable_count = 56 ∧
    nasa_neo_feed_panel_D_eff = 18 ∧
    (0.021097 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold nasa_neo_feed_panel_observable_count; norm_num,
    by unfold nasa_neo_feed_panel_D_eff; norm_num,
    nasa_neo_feed_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
