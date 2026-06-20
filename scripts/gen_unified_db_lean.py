#!/usr/bin/env python3
"""Generate FSOT/Formal/UnifiedDBPriors.lean from unified_db registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "UnifiedDBPriors.lean"


def build_lean(registry: dict) -> str:
    u = registry.get("unified_db", {})
    total = u.get("total_candidates", 13637)
    strict = u.get("strict_empirical", 9403)
    eval_ok = u.get("evaluation_ok", 146)
    records_total = u.get("records_total", 30000)
    top_project_count = u.get("top_project_count", 15)

    return f"""/-
  FSOT Formal UnifiedDBPriors — unified observable database meta-certificate.

  Source: FSOT_UNIFIED_DATABASE_SYSTEM/database/FSOT_OBSERVABLE_VERIFICATION_REPORT.json
  Generator: scripts/gen_unified_db_lean.py
-/

import FSOT.Formal.Domains
import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

def unified_db_total_candidates : ℕ := {total}
def unified_db_strict_empirical : ℕ := {strict}
def unified_db_evaluation_ok : ℕ := {eval_ok}
def unified_db_records_total : ℕ := {records_total}
def unified_db_top_project_count : ℕ := {top_project_count}

theorem unified_db_strict_le_total :
    unified_db_strict_empirical ≤ unified_db_total_candidates := by
  unfold unified_db_strict_empirical unified_db_total_candidates; norm_num

theorem unified_db_evaluation_ok_pos : 0 < unified_db_evaluation_ok := by
  unfold unified_db_evaluation_ok; norm_num

theorem unified_db_records_total_pos : 0 < unified_db_records_total := by
  unfold unified_db_records_total; norm_num

theorem unified_db_top_project_count_pos : 0 < unified_db_top_project_count := by
  unfold unified_db_top_project_count; norm_num

/-- Bundle: 30k+ indexed records with 13k+ candidates and molecular-domain sign proxy. -/
theorem unified_db_meta_bundle :
    unified_db_total_candidates = {total} ∧
    unified_db_strict_empirical = {strict} ∧
    unified_db_evaluation_ok = {eval_ok} ∧
    unified_db_records_total = {records_total} ∧
    unified_db_top_project_count = {top_project_count} ∧
    unified_db_strict_empirical ≤ unified_db_total_candidates ∧
    (0 : ℝ) < raw_S (get_domain_params "molecular") := by
  refine ⟨
    by unfold unified_db_total_candidates; norm_num,
    by unfold unified_db_strict_empirical; norm_num,
    by unfold unified_db_evaluation_ok; norm_num,
    by unfold unified_db_records_total; norm_num,
    by unfold unified_db_top_project_count; norm_num,
    unified_db_strict_le_total,
    lab_molecular_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate UnifiedDBPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())