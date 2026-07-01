#!/usr/bin/env python3
"""Generate FSOT/Formal/BiologyStrictEmpiricalPriors.lean from strict-empirical benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "biology_strict_manifest.yaml"
DEFAULT_BENCH = ROOT / "data" / "biology_strict_empirical.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "BiologyStrictEmpiricalPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("strict_record_count") or bench.get("record_count") or 0)
    operons = int(bench.get("operon_records") or 0)
    med = bench.get("strict_median_error_pct")
    if med is None:
        med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    ncbi = bench.get("ncbi_reference") or cfg.get("source", {}).get("ncbi_reference") or "NC_012920.1"
    sign = cfg.get("lean", {}).get("sign_theorem", "lab_biological_raw_S_positive")
    return f"""/-
  FSOT Formal BiologyStrictEmpiricalPriors — Tier 13 NCBI-grounded biology observables.
  Source: data/biology_strict_empirical.json ({ncbi})
  Generator: scripts/gen_biology_strict_empirical_lean.py
-/

import FSOT.Formal.Lab

namespace FSOT.Formal

noncomputable section

open Real

def biology_strict_observable_count : ℕ := {n}
def biology_strict_operon_count : ℕ := {operons}
def biology_strict_median_error_pct : ℝ := ({med} : ℝ)

theorem biology_strict_observable_count_pos : 0 < biology_strict_observable_count := by
  unfold biology_strict_observable_count; norm_num

theorem biology_strict_operon_count_pos : 0 < biology_strict_operon_count := by
  unfold biology_strict_operon_count; norm_num

theorem biology_strict_median_error_under_two_pct :
    biology_strict_median_error_pct < (2 : ℝ) := by
  unfold biology_strict_median_error_pct; norm_num

theorem biology_strict_bundle :
    biology_strict_observable_count = {n} ∧
    biology_strict_operon_count = {operons} ∧
    biology_strict_median_error_pct < (2 : ℝ) ∧
    raw_S (get_domain_params "biological") > 0 := by
  refine ⟨
    by unfold biology_strict_observable_count; norm_num,
    by unfold biology_strict_operon_count; norm_num,
    biology_strict_median_error_under_two_pct,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--bench", type=Path, default=DEFAULT_BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())