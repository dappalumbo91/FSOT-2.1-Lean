/-
  FSOT Formal SeismologyPriors — USGS earthquake depth classifier.
  Generator: scripts/gen_seismology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def seismology_event_count : ℕ := 500
def seismology_match_count : ℕ := 493
def seismology_D_eff : ℕ := 18
def seismology_match_rate : ℝ := (0.986 : ℝ)

theorem seismology_event_count_pos : 0 < seismology_event_count := by
  unfold seismology_event_count; norm_num

theorem seismology_match_le_total : seismology_match_count ≤ seismology_event_count := by
  unfold seismology_match_count seismology_event_count; norm_num

theorem seismology_bundle :
    seismology_event_count = 500 ∧
    seismology_match_count = 493 ∧
    seismology_D_eff = 18 ∧
    seismology_match_count ≤ seismology_event_count ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold seismology_event_count; norm_num,
    by unfold seismology_match_count; norm_num,
    by unfold seismology_D_eff; norm_num,
    seismology_match_le_total,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
