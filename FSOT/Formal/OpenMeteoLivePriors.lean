/-
  FSOT Formal OpenMeteoLivePriors — Tier 81 credential-free public (Open_Meteo_Live_Panel).
  Generator: scripts/gen_tier81_public_verifiable_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def open_meteo_live_observable_count : ℕ := 432
def open_meteo_live_median_error_pct : ℝ := (0.026204 : ℝ)
def open_meteo_live_D_eff : ℕ := 16

theorem open_meteo_live_observable_count_pos : 0 < open_meteo_live_observable_count := by
  unfold open_meteo_live_observable_count; decide

theorem open_meteo_live_median_error_under_five_pct :
    open_meteo_live_median_error_pct < (5 : ℝ) := by
  unfold open_meteo_live_median_error_pct
  exact (by norm_num : (0.026204  : ℝ) < (5 : ℝ))

theorem open_meteo_live_bundle :
    open_meteo_live_observable_count = 432 ∧
    open_meteo_live_D_eff = 16 ∧
    open_meteo_live_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold open_meteo_live_observable_count; decide,
    by unfold open_meteo_live_D_eff; decide,
    open_meteo_live_median_error_under_five_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
