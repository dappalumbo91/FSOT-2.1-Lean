#!/usr/bin/env python3
"""Generate FSOT/Formal/TrinaryOSTierEPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "trinary_os_tier_e_manifest.yaml"
BENCH = ROOT / "data" / "trinary_os_tier_e_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "TrinaryOSTierEPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    lean = cfg.get("lean") or {}
    prefix = "trinary_os_tier_e"
    sign = lean.get("sign_theorem", "consciousness_raw_S_positive")
    lean_domain = lean.get("lean_domain", "consciousness")
    n = int(bench.get("observable_count") or bench.get("record_count") or 0)
    pooled = float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0)
    headline = float(bench.get("headline_median_error_pct") or pooled)
    beats = sum(1 for v in ((bench.get("sota_comparison") or {}).get("beats_sota_summary") or {}).values() if v)
    oracle_n = int(bench.get("oracle_count") or 0)
    opcode_n = int(bench.get("opcode_count") or 0)
    program_n = int(bench.get("program_count") or 0)
    d_eff = int(bench.get("D_eff", 12))
    return f"""/-
  FSOT Formal TrinaryOSTierEPriors — Tier E portable Trinary-OS oracle (FSOTB + ISA + round-trip).
  Generator: scripts/gen_trinary_os_tier_e_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def {prefix}_observable_count : ℕ := {n}
def {prefix}_oracle_count : ℕ := {oracle_n}
def {prefix}_opcode_count : ℕ := {opcode_n}
def {prefix}_program_count : ℕ := {program_n}
def {prefix}_pooled_median_error_pct : ℝ := ({pooled} : ℝ)
def {prefix}_headline_median_error_pct : ℝ := ({headline} : ℝ)
def {prefix}_beats_sota_headlines : ℕ := {beats}
def {prefix}_D_eff : ℕ := {d_eff}

theorem {prefix}_observable_count_pos : 0 < {prefix}_observable_count := by
  unfold {prefix}_observable_count; norm_num

theorem {prefix}_oracle_count_pos : 0 < {prefix}_oracle_count := by
  unfold {prefix}_oracle_count; norm_num

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
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())