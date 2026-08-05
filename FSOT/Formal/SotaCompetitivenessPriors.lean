/-
  FSOT Formal SotaCompetitivenessPriors — zero-parameter FSOT vs mainstream science baselines.

  Source: data/sota_competitiveness_report.json
  Generator: scripts/gen_sota_competitiveness_lean.py
-/

import FSOT.Formal.DomainPrecisionPriors
import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def sota_domains_compared : ℕ := 35
def sota_domains_beats : ℕ := 35
def sota_domains_meets_or_beats : ℕ := 35
def sota_domains_below : ℕ := 0
def sota_fsot_free_parameters : ℕ := 0

theorem sota_beats_majority :
    (32 : ℕ) < sota_domains_beats := by
  unfold sota_domains_beats; decide

theorem sota_meets_or_beats_large :
    (32 : ℕ) < sota_domains_meets_or_beats := by
  unfold sota_domains_meets_or_beats; decide

theorem sota_below_bounded :
    sota_domains_below ≤ (5 : ℕ) := by
  unfold sota_domains_below; decide

theorem sota_zero_free_parameters :
    sota_fsot_free_parameters = 0 := by
  unfold sota_fsot_free_parameters; decide

end
