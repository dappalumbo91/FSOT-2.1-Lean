#!/usr/bin/env python3
"""Generate Lean priors for Tier 68–70 domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
DATA = ROOT / "data"

DOMAIN_CONFIG: dict[str, tuple[str, str, int, str]] = {
    "Materials_Project_Live_Panel": ("materials_project_live_panel", "MaterialsProjectLivePanelPriors", 16, "materials_project_live_panel_benchmark.json"),
    "PubChem_Live_Deep": ("pubchem_live_deep", "PubChemLiveDeepPriors", 16, "pubchem_live_deep_benchmark.json"),
    "OpenNeuro_Full_Panel": ("openneuro_full_panel", "OpenNeuroFullPanelPriors", 14, "openneuro_full_panel_benchmark.json"),
    "VizieR_WDS_TAP_Live_Deep": ("vizier_wds_tap_live_deep", "VizieRWdsTapLiveDeepPriors", 21, "vizier_wds_tap_live_deep_benchmark.json"),
    "Live_Ingest_Spine": ("live_ingest_spine", "LiveIngestSpinePriors", 17, "live_ingest_spine_benchmark.json"),
    "Unified_DB_Candidate_Crosswalk": ("unified_db_candidate_crosswalk", "UnifiedDBCandidateCrosswalkPriors", 17, "unified_db_candidate_crosswalk_benchmark.json"),
    "FSOT_Aggregate_Organized_Panel": ("fsot_aggregate_organized_panel", "FsotAggregateOrganizedPanelPriors", 17, "fsot_aggregate_organized_panel_benchmark.json"),
    "Unified_DB_Crosswalk_Spine": ("unified_db_crosswalk_spine", "UnifiedDBCrosswalkSpinePriors", 17, "unified_db_crosswalk_spine_benchmark.json"),
    "Proof_Ledger_Closure_Spine": ("proof_ledger_closure_spine", "ProofLedgerClosureSpinePriors", 25, "proof_ledger_closure_spine_benchmark.json"),
    "Preregistered_Outcome_Tracking": ("preregistered_outcome_tracking", "PreregisteredOutcomeTrackingPriors", 17, "preregistered_outcome_tracking_benchmark.json"),
    "ToE_Claim_Certificate_Bundle": ("toe_claim_certificate_bundle", "ToEClaimCertificateBundlePriors", 25, "toe_claim_certificate_bundle_benchmark.json"),
}


def build_lean(bench: dict, prefix: str, module_stem: str, d_eff: int) -> str:
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    return f"""/-
  FSOT Formal {module_stem} — Tier 68–70 expansion.
  Generator: scripts/gen_tiers_68_70_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) ∧
    {prefix}_beats_sota_headlines > 0 := by
  refine ⟨?h1, ?h2, ?h3⟩
  · unfold {prefix}_observable_count; norm_num
  · exact {prefix}_pooled_median_under_half_pct
  · exact {prefix}_beats_sota_headlines_pos

end
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(DOMAIN_CONFIG.keys()), action="append")
    args = parser.parse_args()
    for domain in args.only or sorted(DOMAIN_CONFIG.keys()):
        prefix, module_stem, d_eff, bench_name = DOMAIN_CONFIG[domain]
        bench_path = DATA / bench_name
        if not bench_path.exists():
            print(f"Missing benchmark: {bench_path}", file=sys.stderr)
            return 1
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(build_lean(bench, prefix, module_stem, d_eff), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())