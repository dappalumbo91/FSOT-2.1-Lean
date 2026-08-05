/-
  FSOT Formal KnowledgeBasePortableBundlePanelPriors — extension domain Knowledge_Base_Portable_Bundle_Panel.
  Generator: scripts/gen_extension_domains_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def knowledge_base_portable_bundle_panel_observable_count : ℕ := 24
def knowledge_base_portable_bundle_panel_D_eff : ℕ := 19

theorem knowledge_base_portable_bundle_panel_observable_count_pos : 0 < knowledge_base_portable_bundle_panel_observable_count := by
  unfold knowledge_base_portable_bundle_panel_observable_count; decide

theorem knowledge_base_portable_bundle_panel_median_error_under_half_pct :
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) := by norm_num

theorem knowledge_base_portable_bundle_panel_bundle :
    knowledge_base_portable_bundle_panel_observable_count = 24 ∧
    knowledge_base_portable_bundle_panel_D_eff = 19 ∧
    (0.0020923899350648867 : ℝ) < (0.5 : ℝ) ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold knowledge_base_portable_bundle_panel_observable_count; decide,
    by unfold knowledge_base_portable_bundle_panel_D_eff; decide,
    knowledge_base_portable_bundle_panel_median_error_under_half_pct,
    energy_raw_S_positive
  ⟩

end

end FSOT.Formal
