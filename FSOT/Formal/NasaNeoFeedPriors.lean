/-
  FSOT Formal NasaNeoFeedPriors — Tier 80 government open data (NASA_NEO_Feed_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nasa_neo_feed_observable_count : ℕ := 68
def nasa_neo_feed_median_error_pct : ℝ := (0.021097 : ℝ)
def nasa_neo_feed_D_eff : ℕ := 18

theorem nasa_neo_feed_observable_count_pos : 0 < nasa_neo_feed_observable_count := by
  unfold nasa_neo_feed_observable_count; norm_num

theorem nasa_neo_feed_median_error_under_five_pct :
    nasa_neo_feed_median_error_pct < (5 : ℝ) := by
  unfold nasa_neo_feed_median_error_pct; norm_num

theorem nasa_neo_feed_bundle :
    nasa_neo_feed_observable_count = 68 ∧
    nasa_neo_feed_D_eff = 18 ∧
    nasa_neo_feed_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "astronomical") > 0 := by
  refine ⟨
    by unfold nasa_neo_feed_observable_count; norm_num,
    by unfold nasa_neo_feed_D_eff; norm_num,
    nasa_neo_feed_median_error_under_five_pct,
    astronomical_raw_S_positive
  ⟩

end

end FSOT.Formal
