#!/usr/bin/env python3
"""Generate FSOT/Formal/CosmologyAnomaliesPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "cosmology_anomalies_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "CosmologyAnomaliesPriors.lean"


def build_lean(bench: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    resolved = int(bench.get("resolved_within_15pct_count") or 0)
    med = float(bench.get("median_error_pct") or 0.0)
    return f"""/-
  FSOT Formal CosmologyAnomaliesPriors — H0/S8/lithium/CMB/JWST/FRB tensions.
  Generator: scripts/gen_cosmology_anomalies_lean.py
-/

import FSOT.Formal.Cosmology

namespace FSOT.Formal

noncomputable section

open Real

def cosmology_anomalies_count : ℕ := {n}
def cosmology_anomalies_resolved_count : ℕ := {resolved}
def cosmology_anomalies_median_error : ℝ := ({med} : ℝ)

theorem cosmology_anomalies_count_pos : 0 < cosmology_anomalies_count := by
  unfold cosmology_anomalies_count; norm_num

theorem cosmology_anomalies_resolved_le_total :
    cosmology_anomalies_resolved_count ≤ cosmology_anomalies_count := by
  unfold cosmology_anomalies_resolved_count cosmology_anomalies_count; norm_num

theorem cosmology_anomalies_bundle :
    cosmology_anomalies_count = {n} ∧
    cosmology_anomalies_resolved_count ≤ cosmology_anomalies_count ∧
    |h0_fsot S_cosm_cached - h0_fsot_canonical| < (0.11 : ℝ) := by
  refine ⟨by unfold cosmology_anomalies_count; norm_num,
    cosmology_anomalies_resolved_le_total,
    h0_fsot_cached_approx_value⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())