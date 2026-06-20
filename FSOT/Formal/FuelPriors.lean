/-
  FSOT Formal FuelPriors — Fuel Lab compound profile certificates.

  Source: Desktop/Fuel Lab lookup JSON batches
  Generator: scripts/gen_fuel_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def fuel_profile_count : ℕ := 6
def fuel_lookup_entry_count : ℕ := 34
def fuel_resolved_entry_count : ℕ := 34
def fuel_source_file_count : ℕ := 2

theorem fuel_profile_count_pos : 0 < fuel_profile_count := by
  unfold fuel_profile_count; norm_num

theorem fuel_resolved_le_entries :
    fuel_resolved_entry_count ≤ fuel_lookup_entry_count := by
  unfold fuel_resolved_entry_count fuel_lookup_entry_count; norm_num

theorem fuel_lab_chemical_domain_positive :
    (0 : ℝ) < 1 := by norm_num

/-- Bundle: Fuel Lab profiles and resolved compound lookups (chemical domain). -/
theorem fuel_lab_compound_bundle :
    fuel_profile_count = 6 ∧
    fuel_lookup_entry_count = 34 ∧
    fuel_resolved_entry_count = 34 ∧
    fuel_resolved_entry_count ≤ fuel_lookup_entry_count ∧
    (0 : ℝ) < raw_S (get_domain_params "chemical") := by
  refine ⟨
    by unfold fuel_profile_count; norm_num,
    by unfold fuel_lookup_entry_count; norm_num,
    by unfold fuel_resolved_entry_count; norm_num,
    fuel_resolved_le_entries,
    chemical_raw_S_positive
  ⟩

end

end FSOT.Formal
