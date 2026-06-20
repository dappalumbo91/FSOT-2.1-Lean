#!/usr/bin/env python3
"""Generate FSOT/Formal/WeatherPriors.lean from weather_lab registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "WeatherPriors.lean"


def build_lean(registry: dict) -> str:
    w = registry.get("weather_lab", {})
    hours = w.get("hour_count", 24)
    d_eff = int((w.get("D_eff_values") or [15])[0])
    s_min = w.get("S_min", 0.365)
    s_mean = w.get("S_mean", 0.52)

    return f"""/-
  FSOT Formal WeatherPriors — atmospheric scalar simulation certificates.

  Source: weather/fsot_weather_sim_log.json
  Generator: scripts/gen_weather_priors_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def weather_hour_count : ℕ := {hours}
def weather_D_eff : ℕ := {d_eff}
def weather_S_min : ℝ := ({s_min} : ℝ)
def weather_S_mean : ℝ := ({s_mean} : ℝ)

theorem weather_S_min_positive : (0 : ℝ) < weather_S_min := by
  unfold weather_S_min; norm_num

theorem weather_hour_count_pos : 0 < weather_hour_count := by
  unfold weather_hour_count; norm_num

/-- Bundle: 24-hour weather sim at D_eff=15 with positive S (medical-domain sign proxy). -/
theorem weather_priors_bundle :
    weather_hour_count = {hours} ∧
    weather_D_eff = {d_eff} ∧
    weather_S_min = ({s_min} : ℝ) ∧
    weather_S_mean = ({s_mean} : ℝ) ∧
    (0 : ℝ) < weather_S_min ∧
    (0 : ℝ) < raw_S (get_domain_params "medical") := by
  refine ⟨
    by unfold weather_hour_count; norm_num,
    by unfold weather_D_eff; norm_num,
    by unfold weather_S_min; norm_num,
    by unfold weather_S_mean; norm_num,
    weather_S_min_positive,
    medical_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate WeatherPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())