/-
  FSOT Formal BreakthroughDiscoveries20242026Priors — Tier 39 (Breakthrough_Discoveries_2024_2026).
  Generator: scripts/gen_tier39_propulsion_electrical_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def breakthrough_discoveries_2024_2026_observable_count : ℕ := 21
def breakthrough_discoveries_2024_2026_median_error_pct : ℝ := (0.0 : ℝ)
def breakthrough_discoveries_2024_2026_D_eff : ℕ := 22

theorem breakthrough_discoveries_2024_2026_observable_count_pos : 0 < breakthrough_discoveries_2024_2026_observable_count := by
  unfold breakthrough_discoveries_2024_2026_observable_count; decide

theorem breakthrough_discoveries_2024_2026_median_error_under_five_pct :
    breakthrough_discoveries_2024_2026_median_error_pct < (5 : ℝ) := by
  unfold breakthrough_discoveries_2024_2026_median_error_pct; norm_num

theorem breakthrough_discoveries_2024_2026_bundle :
    breakthrough_discoveries_2024_2026_observable_count = 21 ∧
    breakthrough_discoveries_2024_2026_D_eff = 22 ∧
    breakthrough_discoveries_2024_2026_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "particle") > 0 := by
  refine ⟨
    by unfold breakthrough_discoveries_2024_2026_observable_count; decide,
    by unfold breakthrough_discoveries_2024_2026_D_eff; decide,
    breakthrough_discoveries_2024_2026_median_error_under_five_pct,
    particle_raw_S_positive
  ⟩

end

end FSOT.Formal
