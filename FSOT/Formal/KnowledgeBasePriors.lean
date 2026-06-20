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

theorem knowledge_base_source_count_pos : 0 < knowledge_base_source_count := by
  unfold knowledge_base_source_count; norm_num

theorem knowledge_base_catalog_formulas_pos : 0 < knowledge_base_catalog_formulas := by
  unfold knowledge_base_catalog_formulas; norm_num

/-- Bundle: 19k+ catalog formulas with molecular-domain sign proxy. -/
theorem knowledge_base_corpus_bundle :
    knowledge_base_source_count = 39 ∧
    knowledge_base_catalog_formulas = 19213 ∧
    knowledge_base_resolved_formulas = 19213 ∧
    knowledge_base_observable_citations = 1905 ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold knowledge_base_source_count; norm_num,
    by unfold knowledge_base_catalog_formulas; norm_num,
    by unfold knowledge_base_resolved_formulas; norm_num,
    by unfold knowledge_base_observable_citations; norm_num,
    molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
