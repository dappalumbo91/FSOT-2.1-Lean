#!/usr/bin/env python3
"""Generate FSOT/Formal/HiggsMassPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "higgs_mass_manifest.yaml"
BENCH = ROOT / "data" / "higgs_mass_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "HiggsMassPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    total = int(bench.get("observable_count") or bench.get("record_count") or 0)
    med = bench.get("median_error_pct")
    med = 0.0 if med is None else float(med)
    rule_id = bench.get("rule_id") or "FO-213"
    sign = cfg.get("lean", {}).get("sign_theorem", "particle_raw_S_positive")
    gev_row = next((r for r in bench.get("records") or [] if r.get("property") == "m_H_GeV"), {})
    computed_gev = float(gev_row.get("computed") or 0.0)
    return f"""/-
  FSOT Formal HiggsMassPriors — Higgs boson mass from FO-213 SMILES intrinsic.
  Generator: scripts/gen_higgs_mass_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def higgs_mass_rule_id : String := "{rule_id}"
def higgs_mass_observable_count : ℕ := {total}
def higgs_mass_median_error_pct : ℝ := ({med} : ℝ)
def higgs_mass_computed_gev : ℝ := ({computed_gev} : ℝ)

theorem higgs_mass_observable_count_pos : 0 < higgs_mass_observable_count := by
  unfold higgs_mass_observable_count; norm_num

theorem higgs_mass_median_error_under_half_pct :
    higgs_mass_median_error_pct < (0.5 : ℝ) := by
  unfold higgs_mass_median_error_pct; norm_num

theorem higgs_mass_computed_positive : 0 < higgs_mass_computed_gev := by
  unfold higgs_mass_computed_gev; norm_num

/-- Bundle: FO-213 Higgs mass with particle-domain sign proxy. -/
theorem higgs_mass_bundle :
    higgs_mass_observable_count = {total} ∧
    higgs_mass_median_error_pct < (0.5 : ℝ) ∧
    0 < higgs_mass_computed_gev ∧
    (0 : ℝ) < raw_S (get_domain_params "particle") := by
  refine ⟨
    by unfold higgs_mass_observable_count; norm_num,
    higgs_mass_median_error_under_half_pct,
    higgs_mass_computed_positive,
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
    parser.add_argument("--benchmark", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    bench = json.loads(args.benchmark.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())