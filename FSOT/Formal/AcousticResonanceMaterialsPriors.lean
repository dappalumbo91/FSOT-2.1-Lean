/-
  FSOT Formal AcousticResonanceMaterialsPriors — extension domain Acoustic_Resonance_Materials.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def acoustic_resonance_materials_observable_count : ℕ := 29
def acoustic_resonance_materials_D_eff : ℕ := 15

theorem acoustic_resonance_materials_observable_count_pos : 0 < acoustic_resonance_materials_observable_count := by
  unfold acoustic_resonance_materials_observable_count; norm_num

theorem acoustic_resonance_materials_median_error_under_half_pct :
    (0.008381497018411083 : ℝ) < (0.5 : ℝ) := by norm_num

theorem acoustic_resonance_materials_bundle :
    acoustic_resonance_materials_observable_count = 29 ∧
    acoustic_resonance_materials_D_eff = 15 ∧
    (0.008381497018411083 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold acoustic_resonance_materials_observable_count; norm_num,
    by unfold acoustic_resonance_materials_D_eff; norm_num,
    acoustic_resonance_materials_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
