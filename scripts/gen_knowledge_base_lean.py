#!/usr/bin/env python3
"""Generate FSOT/Formal/KnowledgeBasePriors.lean from knowledge_base registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "KnowledgeBasePriors.lean"


def build_lean(registry: dict) -> str:
    kb = registry.get("knowledge_base", {})
    sources = kb.get("source_count", 30)
    catalog = kb.get("catalog_formulas", 19000)
    resolved = kb.get("resolved_formulas", 0)
    citations = kb.get("observable_citations", 1800)

    return f"""/-
  FSOT Formal KnowledgeBasePriors — unified formula transfer corpus certificates.

  Source: Knowledge base/transfer/FSOT_KNOWLEDGE_UNIFIED_TRANSFER.json
  Generator: scripts/gen_knowledge_base_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def knowledge_base_source_count : ℕ := {sources}
def knowledge_base_catalog_formulas : ℕ := {catalog}
def knowledge_base_resolved_formulas : ℕ := {resolved}
def knowledge_base_observable_citations : ℕ := {citations}

theorem knowledge_base_source_count_pos : 0 < knowledge_base_source_count := by
  unfold knowledge_base_source_count; norm_num

theorem knowledge_base_catalog_formulas_pos : 0 < knowledge_base_catalog_formulas := by
  unfold knowledge_base_catalog_formulas; norm_num

/-- Bundle: 19k+ catalog formulas with molecular-domain sign proxy. -/
theorem knowledge_base_corpus_bundle :
    knowledge_base_source_count = {sources} ∧
    knowledge_base_catalog_formulas = {catalog} ∧
    knowledge_base_resolved_formulas = {resolved} ∧
    knowledge_base_observable_citations = {citations} ∧
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
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate KnowledgeBasePriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())