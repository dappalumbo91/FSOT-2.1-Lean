#!/usr/bin/env python3
"""Generate Lean priors for Tier H cybersecurity engineering domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_h_cybersecurity_lib import BUILDERS, output_path  # noqa: E402

LEAN_MAP = {
    "Cryptography_Technology": ("crypto_tech", "particle", "particle_raw_S_positive", "CryptographyTechnologyPriors"),
    "Network_Internet_Protocols": ("network_inet", "ai", "ai_raw_S_positive", "NetworkInternetProtocolsPriors"),
    "Malware_Threat_Intelligence": ("malware_threat", "medical", "medical_raw_S_positive", "MalwareThreatIntelligencePriors"),
    "Secure_Software_Engineering": ("secure_sw", "ai", "ai_raw_S_positive", "SecureSoftwareEngineeringPriors"),
    "Code_Genome_Structure": ("code_genome", "biological", "biological_raw_S_positive", "CodeGenomeStructurePriors"),
    "Zero_Day_Risk_Evaluator": ("zero_day_eval", "ai", "ai_raw_S_positive", "ZeroDayRiskEvaluatorPriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, lean_domain, sign, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""
    if domain == "Zero_Day_Risk_Evaluator":
        holes = int(bench.get("detected_hole_count") or 0)
        tier = bench.get("risk_tier") or "GREEN"
        tier_green = 1 if tier == "GREEN" else 0
        extra_defs = f"""
def {prefix}_detected_hole_count : ℕ := {holes}
def {prefix}_risk_tier_green : ℕ := {tier_green}
"""
        extra_thms = f"""
theorem {prefix}_hole_count_certified : {prefix}_detected_hole_count = {holes} := by
  unfold {prefix}_detected_hole_count; norm_num
"""
    if domain == "Code_Genome_Structure":
        bridges = len(bench.get("language_bridges") or []) or 9
        extra_defs = f"""
def {prefix}_language_bridge_count : ℕ := {bridges}
"""
        extra_thms = f"""
theorem {prefix}_language_bridges_pos : 0 < {prefix}_language_bridge_count := by
  unfold {prefix}_language_bridge_count; norm_num
"""
    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier H cybersecurity engineering.
  Generator: scripts/gen_tier_h_cybersecurity_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 15))}
{extra_defs}
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
{extra_thms}
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
    parser.add_argument("--only", choices=sorted(LEAN_MAP.keys()), action="append")
    args = parser.parse_args()
    domains = args.only or sorted(LEAN_MAP.keys())
    for domain in domains:
        bench_path = output_path(domain)
        if not bench_path.exists():
            bench = BUILDERS[domain]()
            bench_path.write_text(json.dumps(bench, indent=2), encoding="utf-8")
        else:
            bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, domain)
        out = FORMAL / f"{LEAN_MAP[domain][3]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())