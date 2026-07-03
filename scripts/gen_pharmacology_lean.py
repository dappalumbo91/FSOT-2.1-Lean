#!/usr/bin/env python3
"""Generate FSOT/Formal/PharmacologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pharmacology_chembl_manifest.yaml"
BENCH = ROOT / "data" / "pharmacology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "PharmacologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("observable_count") or 0)
    med = bench.get("median_error_pct") or 0.0
    med = float(med)
    d_eff = 14
    sign = cfg.get("lean", {}).get("sign_theorem", "medical_raw_S_positive")
    return f"""/-
  FSOT Formal PharmacologyPriors — ChEMBL molecular-weight verification.
  Generator: scripts/gen_pharmacology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def pharmacology_observable_count : ℕ := {n}
def pharmacology_median_error_pct : ℝ := ({med} : ℝ)
def pharmacology_D_eff : ℕ := {d_eff}

theorem pharmacology_observable_count_pos : 0 < pharmacology_observable_count := by
  unfold pharmacology_observable_count; norm_num

theorem pharmacology_median_error_under_five_pct :
    pharmacology_median_error_pct < (5 : ℝ) := by
  unfold pharmacology_median_error_pct; norm_num

theorem pharmacology_bundle :
    pharmacology_observable_count = {n} ∧
    pharmacology_D_eff = {d_eff} ∧
    pharmacology_median_error_pct < (5 : ℝ) ∧
    raw_S (get_domain_params "medical") > 0 := by
  refine ⟨
    by unfold pharmacology_observable_count; norm_num,
    by unfold pharmacology_D_eff; norm_num,
    pharmacology_median_error_under_five_pct,
    {sign}
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())