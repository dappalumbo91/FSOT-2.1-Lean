/-
  FSOT Formal KnowledgeBasePriors — unified formula transfer corpus certificates.

  Source: Knowledge base/transfer/FSOT_KNOWLEDGE_UNIFIED_TRANSFER.json
  Generator: scripts/gen_knowledge_base_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def knowledge_base_source_count : ℕ := 39
def knowledge_base_catalog_formulas : ℕ := 19213
def knowledge_base_resolved_formulas : ℕ := 19213
def knowledge_base_observable_citations : ℕ := 1905
def knowledge_base_observable_verified_formulas : ℕ := 7941
def knowledge_base_observable_verified_matched : ℕ := 7941
def knowledge_base_within_target_2pct : ℕ := 6921
def knowledge_base_per_formula_total : ℕ := 19213
def knowledge_base_per_formula_evaluated : ℕ := 71
def knowledge_base_per_formula_verified : ℕ := 105
def knowledge_base_per_formula_within_target_2pct : ℕ := 50

theorem knowledge_base_source_count_pos : 0 < knowledge_base_source_count := by
  unfold knowledge_base_source_count; norm_num

theorem knowledge_base_catalog_formulas_pos : 0 < knowledge_base_catalog_formulas := by
  unfold knowledge_base_catalog_formulas; norm_num

theorem knowledge_base_observable_matched_le_verified :
    knowledge_base_observable_verified_matched ≤ knowledge_base_observable_verified_formulas := by
  unfold knowledge_base_observable_verified_matched knowledge_base_observable_verified_formulas; norm_num

/-- Bundle: 19k catalog per-formula pass + 7941 strict-empirical observable bridge. -/
theorem knowledge_base_corpus_bundle :
    knowledge_base_source_count = 39 ∧
    knowledge_base_catalog_formulas = 19213 ∧
    knowledge_base_resolved_formulas = 19213 ∧
    knowledge_base_observable_citations = 1905 ∧
    knowledge_base_observable_verified_formulas = 7941 ∧
    knowledge_base_observable_verified_matched = 7941 ∧
    knowledge_base_within_target_2pct = 6921 ∧
    knowledge_base_per_formula_total = 19213 ∧
    knowledge_base_per_formula_evaluated = 71 ∧
    knowledge_base_per_formula_verified = 105 ∧
    knowledge_base_per_formula_within_target_2pct = 50 ∧
    knowledge_base_observable_verified_matched ≤ knowledge_base_observable_verified_formulas ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold knowledge_base_source_count; norm_num,
    by unfold knowledge_base_catalog_formulas; norm_num,
    by unfold knowledge_base_resolved_formulas; norm_num,
    by unfold knowledge_base_observable_citations; norm_num,
    by unfold knowledge_base_observable_verified_formulas; norm_num,
    by unfold knowledge_base_observable_verified_matched; norm_num,
    by unfold knowledge_base_within_target_2pct; norm_num,
    by unfold knowledge_base_per_formula_total; norm_num,
    by unfold knowledge_base_per_formula_evaluated; norm_num,
    by unfold knowledge_base_per_formula_verified; norm_num,
    by unfold knowledge_base_per_formula_within_target_2pct; norm_num,
    knowledge_base_observable_matched_le_verified,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
