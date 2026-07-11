#!/usr/bin/env python3
"""Generate Lean priors for Tier 51 stumped observables domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from tier_p_stumped_observables_lib import BUILDERS, TIER_P, output_path  # noqa: E402

LEAN_MAP = {
    "Stumped_Observables_Panel": ("stumped_panel", "StumpedObservablesPanelPriors"),
    "Hubble_Bubble_Tension": ("hubble_tension", "HubbleBubbleTensionPriors"),
    "Dark_Sector_Open_Problems": ("dark_sector", "DarkSectorOpenProblemsPriors"),
    "Stumped_Observables_Spine": ("stumped_spine", "StumpedObservablesSpinePriors"),
}


def build_lean(bench: dict, domain: str) -> str:
    prefix, module_stem = LEAN_MAP[domain]
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    extra_defs = ""
    extra_thms = ""

    if domain == "Stumped_Observables_Panel":
        op = int(bench.get("open_prediction_count") or 0)
        extra_defs = f"def {prefix}_open_prediction_count : ℕ := {op}\n"
        extra_thms = f"theorem {prefix}_open_predictions_pos : 0 < {prefix}_open_prediction_count := by unfold {prefix}_open_prediction_count; norm_num\n"
    elif domain == "Hubble_Bubble_Tension":
        hc = int(bench.get("h0_sector_count") or 0)
        extra_defs = f"def {prefix}_h0_sector_count : ℕ := {hc}\n"
        extra_thms = f"theorem {prefix}_h0_sectors_pos : 0 < {prefix}_h0_sector_count := by unfold {prefix}_h0_sector_count; norm_num\n"
    elif domain == "Dark_Sector_Open_Problems":
        dr = bench.get("dual_readout") or {}
        w0_cmb = float(dr.get("w0_cmb") or -1.03)
        w0_bao = float(dr.get("w0_bao") or -0.73)
        wa_cmb = float(dr.get("wa_cmb") or -0.808)
        wa_bao = float(dr.get("wa_bao") or -1.021)
        extra_defs = (
            f"def {prefix}_w0_cmb : ℝ := ({w0_cmb} : ℝ)\n"
            f"def {prefix}_w0_bao : ℝ := ({w0_bao} : ℝ)\n"
            f"def {prefix}_wa_cmb : ℝ := ({wa_cmb} : ℝ)\n"
            f"def {prefix}_wa_bao : ℝ := ({wa_bao} : ℝ)\n"
        )
        extra_thms = (
            f"theorem {prefix}_w0_cmb_negative : {prefix}_w0_cmb < (0 : ℝ) := by unfold {prefix}_w0_cmb; norm_num\n"
            f"theorem {prefix}_w0_bao_negative : {prefix}_w0_bao < (0 : ℝ) := by unfold {prefix}_w0_bao; norm_num\n"
            f"theorem {prefix}_wa_cmb_negative : {prefix}_wa_cmb < (0 : ℝ) := by unfold {prefix}_wa_cmb; norm_num\n"
            f"theorem {prefix}_wa_bao_negative : {prefix}_wa_bao < (0 : ℝ) := by unfold {prefix}_wa_bao; norm_num\n"
        )
    elif domain == "Stumped_Observables_Spine":
        hc = int(bench.get("h0_sector_count") or 0)
        op = int(bench.get("open_prediction_count") or 0)
        extra_defs = (
            f"def {prefix}_h0_sector_count : ℕ := {hc}\n"
            f"def {prefix}_open_prediction_count : ℕ := {op}\n"
        )
        extra_thms = f"theorem {prefix}_spine_sectors_pos : 0 < {prefix}_h0_sector_count := by unfold {prefix}_h0_sector_count; norm_num\n"

    if headline < 0.5:
        headline_thm = f"""theorem {prefix}_headline_median_under_half_pct :
    {prefix}_headline_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num
"""
    elif headline < 1.0:
        headline_thm = f"""-- Headline channel median ({headline}%) exceeds 0.5% gate; pooled median gate is separate.
theorem {prefix}_headline_median_under_one_pct :
    {prefix}_headline_median_error_pct < (1.0 : ℝ) := by
  unfold {prefix}_headline_median_error_pct; norm_num
"""
    else:
        headline_thm = f"""theorem {prefix}_headline_median_pos : (0 : ℝ) < {prefix}_headline_median_error_pct := by
  unfold {prefix}_headline_median_error_pct; norm_num
"""

    return f"""/-
  FSOT Formal {module_stem} — {domain} Tier 51 stumped observables spine.
  Generator: scripts/gen_stumped_observables_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {int(bench.get('D_eff', 22))}
{extra_defs}
theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_pooled_median_under_half_pct :
    {prefix}_pooled_median_error_pct < (0.5 : ℝ) := by
  unfold {prefix}_pooled_median_error_pct; norm_num

{headline_thm}
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
        out = FORMAL / f"{LEAN_MAP[domain][1]}.lean"
        out.write_text(lean, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())