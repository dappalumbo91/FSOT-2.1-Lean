/-
  FSOT Formal CryptographyTechnologyPriors — Cryptography_Technology Tier H cybersecurity engineering.
  Generator: scripts/gen_tier_h_cybersecurity_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def crypto_tech_observable_count : ℕ := 44
def crypto_tech_pooled_median_error_pct : ℝ := (0.047520672006218234 : ℝ)
def crypto_tech_headline_median_error_pct : ℝ := (0.047520672006218234 : ℝ)
def crypto_tech_beats_sota_headlines : ℕ := 2
def crypto_tech_D_eff : ℕ := 16

theorem crypto_tech_observable_count_pos : 0 < crypto_tech_observable_count := by
  unfold crypto_tech_observable_count; norm_num

theorem crypto_tech_pooled_median_under_half_pct :
    crypto_tech_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold crypto_tech_pooled_median_error_pct; norm_num

theorem crypto_tech_headline_median_under_half_pct :
    crypto_tech_headline_median_error_pct < (0.5 : ℝ) := by
  unfold crypto_tech_headline_median_error_pct; norm_num

theorem crypto_tech_beats_sota_headlines_pos : 0 < crypto_tech_beats_sota_headlines := by
  unfold crypto_tech_beats_sota_headlines; norm_num

theorem crypto_tech_bundle :
    crypto_tech_observable_count = 44 ∧
    crypto_tech_pooled_median_error_pct < (0.5 : ℝ) ∧
    crypto_tech_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold crypto_tech_observable_count; norm_num
  · exact crypto_tech_pooled_median_under_half_pct
  · exact crypto_tech_beats_sota_headlines_pos

end
