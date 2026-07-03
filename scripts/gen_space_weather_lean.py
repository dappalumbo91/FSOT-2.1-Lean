#!/usr/bin/env python3
"""Generate FSOT/Formal/SpaceWeatherPriors.lean."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "space_weather_manifest.yaml"
BENCH = ROOT / "data" / "space_weather_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "SpaceWeatherPriors.lean"


def build_lean(bench: dict, cfg: dict) -> str:
    n = int(bench.get("kp_record_count") or bench.get("observable_count") or 0)
    ap_n = int(bench.get("ap_record_count") or 0)
    match_n = int(bench.get("stability_match_count") or 0)
    rate = bench.get("stability_match_rate") or 0.0
    rate = float(rate)
    d_eff = int(bench.get("D_eff") or 14)
    sign = cfg.get("lean", {}).get("sign_theorem", "fusion_raw_S_positive")
    return f"""/-
  FSOT Formal SpaceWeatherPriors — NOAA SWPC Kp/Ap space weather observables.
  Generator: scripts/gen_space_weather_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

open Real

def space_weather_kp_record_count : ℕ := {n}
def space_weather_ap_record_count : ℕ := {ap_n}
def space_weather_stability_match_count : ℕ := {match_n}
def space_weather_D_eff : ℕ := {d_eff}
def space_weather_stability_match_rate : ℝ := ({rate} : ℝ)

theorem space_weather_kp_record_count_pos : 0 < space_weather_kp_record_count := by
  unfold space_weather_kp_record_count; norm_num

theorem space_weather_stability_match_le_total :
    space_weather_stability_match_count ≤ space_weather_kp_record_count := by
  unfold space_weather_stability_match_count space_weather_kp_record_count; norm_num

theorem space_weather_stability_match_rate_nonneg : (0 : ℝ) ≤ space_weather_stability_match_rate := by
  unfold space_weather_stability_match_rate; norm_num

/-- Bundle: NOAA Kp storm classifier bridged to fusion-domain sign proxy. -/
theorem space_weather_bundle :
    space_weather_kp_record_count = {n} ∧
    space_weather_ap_record_count = {ap_n} ∧
    space_weather_stability_match_count = {match_n} ∧
    space_weather_D_eff = {d_eff} ∧
    space_weather_stability_match_count ≤ space_weather_kp_record_count ∧
    (0 : ℝ) < raw_S (get_domain_params "fusion") := by
  refine ⟨
    by unfold space_weather_kp_record_count; norm_num,
    by unfold space_weather_ap_record_count; norm_num,
    by unfold space_weather_stability_match_count; norm_num,
    by unfold space_weather_D_eff; norm_num,
    space_weather_stability_match_le_total,
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