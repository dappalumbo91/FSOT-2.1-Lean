/-
  FSOT Formal NistAsdMultiSpeciesOpenPriors — open-science frontier residual panel.
  Residual law: make_fsot_record / fsot_scaled only (FSOT mathematics).
  Generator: scripts/gen_open_frontier_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def nist_asd_multi_species_open_observable_count : ℕ := 26
def nist_asd_multi_species_open_pooled_median_error_pct : ℝ := (0.073582 : ℝ)
def nist_asd_multi_species_open_headline_median_error_pct : ℝ := (0.073582 : ℝ)
def nist_asd_multi_species_open_D_eff : ℕ := 12

theorem nist_asd_multi_species_open_observable_count_pos : 0 < nist_asd_multi_species_open_observable_count := by
  unfold nist_asd_multi_species_open_observable_count; decide

theorem nist_asd_multi_species_open_pooled_median_under_half_pct :
    nist_asd_multi_species_open_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold nist_asd_multi_species_open_pooled_median_error_pct
  exact (by norm_num : (0.073582  : ℝ) < 0.5)

theorem nist_asd_multi_species_open_headline_median_under_half_pct :
    nist_asd_multi_species_open_headline_median_error_pct < (0.5 : ℝ) := by
  unfold nist_asd_multi_species_open_headline_median_error_pct
  exact (by norm_num : (0.073582  : ℝ) < 0.5)

theorem nist_asd_multi_species_open_bundle :
    nist_asd_multi_species_open_observable_count = 26 ∧
    nist_asd_multi_species_open_D_eff = 12 ∧
    nist_asd_multi_species_open_pooled_median_error_pct < (0.5 : ℝ) := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold nist_asd_multi_species_open_observable_count; decide
  · unfold nist_asd_multi_species_open_D_eff; decide
  · exact nist_asd_multi_species_open_pooled_median_under_half_pct

end
