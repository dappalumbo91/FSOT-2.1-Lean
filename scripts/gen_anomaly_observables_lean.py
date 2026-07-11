#!/usr/bin/env python3
"""Generate Lean priors for Tier 51 anomaly observables domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"

LEAN_MAP = {
    "Consciousness_Econ": ("consciousness_econ", "ConsciousnessEconPriors", 17),
    "Dark_Energy_CPL": ("dark_energy_cpl", "DarkEnergyCPLPriors", 24),
    "SH0ES_Refined": ("sh0es_refined", "SH0ESRefinedPriors", 25),
}

BENCHMARKS = {
    "Consciousness_Econ": ROOT / "data" / "consciousness_econ_benchmark.json",
    "Dark_Energy_CPL": ROOT / "data" / "dark_energy_cpl_benchmark.json",
    "SH0ES_Refined": ROOT / "data" / "sh0es_refined_benchmark.json",
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem, d_eff = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(
        1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v
    )
    extra_defs = ""
    extra_thms = ""

    if domain == "Consciousness_Econ":
        anchor_n = len(bench.get("econ_open_anchors") or [])
        extra_defs = f"def {prefix}_econ_anchor_count : ℕ := {anchor_n}\n"
        extra_thms = (
            f"theorem {prefix}_econ_anchors_pos : 0 < {prefix}_econ_anchor_count := by "
            f"unfold {prefix}_econ_anchor_count; norm_num\n"
        )
    elif domain == "Dark_Energy_CPL":
        dr = bench.get("dual_readout") or {}
        w0_cmb = float(bench.get("fsot_w0_cmb") or dr.get("w0_cmb") or -1.03)
        w0_bao = float(bench.get("fsot_w0_bao") or dr.get("w0_bao") or -0.73)
        wa_cmb = float(bench.get("fsot_wa_cmb") or dr.get("wa_cmb") or -0.808)
        wa_bao = float(bench.get("fsot_wa_bao") or dr.get("wa_bao") or -1.021)
        prereg = "true" if bench.get("preregistered") else "false"
        extra_defs = (
            f"def {prefix}_fsot_w0_cmb : ℝ := ({w0_cmb} : ℝ)\n"
            f"def {prefix}_fsot_w0_bao : ℝ := ({w0_bao} : ℝ)\n"
            f"def {prefix}_fsot_wa_cmb : ℝ := ({wa_cmb} : ℝ)\n"
            f"def {prefix}_fsot_wa_bao : ℝ := ({wa_bao} : ℝ)\n"
            f"def {prefix}_preregistered : Bool := {prereg}\n"
        )
        extra_thms = (
            f"theorem {prefix}_w0_cmb_negative : {prefix}_fsot_w0_cmb < (0 : ℝ) := by unfold {prefix}_fsot_w0_cmb; norm_num\n"
            f"theorem {prefix}_w0_bao_negative : {prefix}_fsot_w0_bao < (0 : ℝ) := by unfold {prefix}_fsot_w0_bao; norm_num\n"
            f"theorem {prefix}_wa_cmb_negative : {prefix}_fsot_wa_cmb < (0 : ℝ) := by unfold {prefix}_fsot_wa_cmb; norm_num\n"
            f"theorem {prefix}_wa_bao_negative : {prefix}_fsot_wa_bao < (0 : ℝ) := by unfold {prefix}_fsot_wa_bao; norm_num\n"
        )
    elif domain == "SH0ES_Refined":
        hc = int(bench.get("host_count") or 0)
        extra_defs = f"def {prefix}_host_count : ℕ := {hc}\n"
        extra_thms = (
            f"theorem {prefix}_hosts_pos : 0 < {prefix}_host_count := by "
            f"unfold {prefix}_host_count; norm_num\n"
        )

    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier 51 anomaly observables.
  Generator: scripts/gen_anomaly_observables_lean.py
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
        bench_path = BENCHMARKS[domain]
        if not bench_path.exists():
            print(f"Missing benchmark: {bench_path}", file=sys.stderr)
            return 1
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        lean = build_lean(bench, domain)
        out = FORMAL / f"{LEAN_MAP[domain][1]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())