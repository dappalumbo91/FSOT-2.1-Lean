#!/usr/bin/env python3
"""Generate FSOT/Formal/HydrologyPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "hydrology_usgs_manifest.yaml"
BENCH = ROOT / "data" / "hydrology_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "HydrologyPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("record_count") or bench.get("observable_count") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    rate = float(bench.get("stability_match_rate") or 0.0)
    d_eff = int(bench.get("D_eff") or 15)
    stn = int(bench.get("station_count") or 0)
    sign = cfg.get("lean", {}).get("sign_theorem", "energy_raw_S_positive")
    return f"""/-
  FSOT Formal HydrologyPriors — USGS streamflow anomaly classifier.
  Generator: scripts/gen_hydrology_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def hydrology_month_count : ℕ := {n}
def hydrology_station_count : ℕ := {stn}
def hydrology_stability_match_count : ℕ := {match_n}
def hydrology_D_eff : ℕ := {d_eff}
def hydrology_stability_match_rate : ℝ := ({rate} : ℝ)

theorem hydrology_month_count_pos : 0 < hydrology_month_count := by
  unfold hydrology_month_count; norm_num

theorem hydrology_stability_match_le_total :
    hydrology_stability_match_count ≤ hydrology_month_count := by
  unfold hydrology_stability_match_count hydrology_month_count; norm_num

theorem hydrology_stability_match_rate_nonneg : (0 : ℝ) ≤ hydrology_stability_match_rate := by
  unfold hydrology_stability_match_rate; norm_num

theorem hydrology_bundle :
    hydrology_month_count = {n} ∧
    hydrology_station_count = {stn} ∧
    hydrology_stability_match_count = {match_n} ∧
    hydrology_D_eff = {d_eff} ∧
    hydrology_stability_match_count ≤ hydrology_month_count ∧
    (0 : ℝ) ≤ hydrology_stability_match_rate ∧
    raw_S (get_domain_params "energy") > 0 := by
  refine ⟨
    by unfold hydrology_month_count; norm_num,
    by unfold hydrology_station_count; norm_num,
    by unfold hydrology_stability_match_count; norm_num,
    by unfold hydrology_D_eff; norm_num,
    hydrology_stability_match_le_total,
    hydrology_stability_match_rate_nonneg,
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
    parser.add_argument("--bench", type=Path, default=BENCH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not args.bench.exists():
        print(f"Missing {args.bench} — run build_hydrology_benchmark.py first", file=__import__("sys").stderr)
        return 1
    bench = json.loads(args.bench.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(bench, cfg), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())