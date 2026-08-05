/-
  FSOT Formal UapWarGovReleasePriors — Tier 80 government open data (UAP_War_Gov_Release_Panel).
  Generator: scripts/gen_tier80_government_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def uap_war_gov_release_observable_count : ℕ := 542
def uap_war_gov_release_median_error_pct : ℝ := (0.008488 : ℝ)
def uap_war_gov_release_D_eff : ℕ := 20

theorem uap_war_gov_release_observable_count_pos : 0 < uap_war_gov_release_observable_count := by
  unfold uap_war_gov_release_observable_count; decide

theorem uap_war_gov_release_median_error_under_five_pct :
    uap_war_gov_release_median_error_pct < (5 : ℝ) := by
  unfold uap_war_gov_release_median_error_pct; norm_num

theorem uap_war_gov_release_bundle :
    uap_war_gov_release_observable_count = 542 ∧
    uap_war_gov_release_D_eff = 20 ∧
    uap_war_gov_release_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold uap_war_gov_release_observable_count; decide,
    by unfold uap_war_gov_release_D_eff; decide,
    uap_war_gov_release_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
