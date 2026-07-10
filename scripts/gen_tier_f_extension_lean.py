#!/usr/bin/env python3
"""Generate Lean priors for Tier F extension domains (science-gap fill)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_f_extension_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Paleontology": ("paleontology_ext", "energy", "energy_raw_S_positive", "PaleontologyExtensionPriors"),
    "Marine_Biology": ("marine_biology_ext", "biological", "biological_raw_S_positive", "MarineBiologyExtensionPriors"),
    "Mycology": ("mycology_ext", "biological", "biological_raw_S_positive", "MycologyExtensionPriors"),
    "Entomology": ("entomology_ext", "biological", "biological_raw_S_positive", "EntomologyExtensionPriors"),
    "Virology": ("virology_ext", "medical", "medical_raw_S_positive", "VirologyExtensionPriors"),
    "Epidemiology": ("epidemiology_ext", "medical", "medical_raw_S_positive", "EpidemiologyExtensionPriors"),
    "Cardiology": ("cardiology_ext", "medical", "medical_raw_S_positive", "CardiologyExtensionPriors"),
    "Civil_Engineering": ("civil_engineering_ext", "material", "material_raw_S_positive", "CivilEngineeringExtensionPriors"),
    "Mechanical_Engineering": ("mechanical_engineering_ext", "material", "material_raw_S_positive", "MechanicalEngineeringExtensionPriors"),
    "Robotics_Control_Systems": ("robotics_control_ext", "consciousness", "consciousness_raw_S_positive", "RoboticsControlSystemsExtensionPriors"),
    "Neuroeconomics": ("neuroeconomics_ext", "consciousness", "consciousness_raw_S_positive", "NeuroeconomicsExtensionPriors"),
    "Paleoclimate": ("paleoclimate_ext", "energy", "energy_raw_S_positive", "PaleoclimateExtensionPriors"),
    "Speleology": ("speleology_ext", "energy", "energy_raw_S_positive", "SpeleologyExtensionPriors"),
    "Exogeology": ("exogeology_ext", "galactic", "galactic_raw_S_positive", "ExogeologyExtensionPriors"),
    "Pure_Mathematics": ("pure_mathematics_ext", "particle", "particle_raw_S_positive", "PureMathematicsExtensionPriors"),
    "History": ("history_ext", "consciousness", "consciousness_raw_S_positive", "HistoryExtensionPriors"),
    "Law_Policy": ("law_policy_ext", "consciousness", "consciousness_raw_S_positive", "LawPolicyExtensionPriors"),
    "Finance_Markets": ("finance_markets_ext", "consciousness", "consciousness_raw_S_positive", "FinanceMarketsExtensionPriors"),
    "Supply_Chain_Logistics": ("supply_chain_ext", "consciousness", "consciousness_raw_S_positive", "SupplyChainLogisticsExtensionPriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, lean_domain, sign, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier F science-gap extension (real API anchors).
  Generator: scripts/gen_tier_f_extension_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 14))}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_five_pct :
    {prefix}_pooled_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

theorem {prefix}_headline_median_under_five_pct :
    {prefix}_headline_median_error_pct < (5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num

theorem {prefix}_beats_sota_headlines_pos : 0 < {prefix}_beats_sota_headlines := by
  unfold {prefix}_beats_sota_headlines; norm_num

theorem {prefix}_bundle :
    {prefix}_observable_count = {n} ∧
    {prefix}_pooled_median_error_pct < (5 : ℝ) ∧
    {prefix}_headline_median_error_pct < (5 : ℝ) ∧
    0 < {prefix}_beats_sota_headlines ∧
    raw_S (get_domain_params "{lean_domain}") > 0 := by
  refine ⟨
    by unfold {prefix}_observable_count; norm_num,
    {prefix}_pooled_median_under_five_pct,
    {prefix}_headline_median_under_five_pct,
    {prefix}_beats_sota_headlines_pos,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(BUILDERS.keys())
    for domain in domains:
        bench_path = output_path(domain)
        if not bench_path.exists():
            bench_path.write_text(json.dumps(BUILDERS[domain](), indent=2), encoding="utf-8")
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        module_stem = LEAN_MAP[domain][3]
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(build_lean(bench, domain), encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())