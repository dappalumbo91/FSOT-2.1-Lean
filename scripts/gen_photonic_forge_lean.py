#!/usr/bin/env python3
"""Generate FSOT/Formal/PhotonicForge.lean from photonic_forge registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "PhotonicForge.lean"


def build_lean(registry: dict) -> str:
    photonic = registry.get("photonic_forge", {})
    voxels = photonic.get("voxel_count", 180)
    counts = photonic.get("trinary_counts", {"-1": 40, "0": 60, "1": 80})
    neg = counts.get(-1, counts.get("-1", 40))
    zero = counts.get(0, counts.get("0", 60))
    pos = counts.get(1, counts.get("1", 80))

    return f"""/-
  FSOT Formal PhotonicForge — virtual crystal VRAM trinary payload certificates.

  Source: FSOT Photonic V2 Experiments/fsot_vram_payload.json
  Generator: scripts/gen_photonic_forge_lean.py
-/

import FSOT.Formal.Domains

namespace FSOT.Formal

noncomputable section

def photonic_voxel_count : ℕ := {voxels}
def photonic_trinary_neg_count : ℕ := {neg}
def photonic_trinary_zero_count : ℕ := {zero}
def photonic_trinary_pos_count : ℕ := {pos}

theorem photonic_trinary_partition :
    photonic_trinary_neg_count + photonic_trinary_zero_count + photonic_trinary_pos_count
      = photonic_voxel_count := by
  unfold photonic_trinary_neg_count photonic_trinary_zero_count photonic_trinary_pos_count photonic_voxel_count; norm_num

theorem photonic_voxel_count_pos : 0 < photonic_voxel_count := by
  unfold photonic_voxel_count; norm_num

/-- Bundle: 180-voxel trinary crystal grid with electron-domain sign certificate. -/
theorem photonic_forge_bundle :
    photonic_voxel_count = {voxels} ∧
    photonic_trinary_neg_count + photonic_trinary_zero_count + photonic_trinary_pos_count = photonic_voxel_count ∧
    photonic_trinary_neg_count = {neg} ∧
    photonic_trinary_zero_count = {zero} ∧
    photonic_trinary_pos_count = {pos} ∧
    (0 : ℝ) < raw_S (get_domain_params "electron") := by
  refine ⟨
    by unfold photonic_voxel_count; norm_num,
    photonic_trinary_partition,
    by unfold photonic_trinary_neg_count; norm_num,
    by unfold photonic_trinary_zero_count; norm_num,
    by unfold photonic_trinary_pos_count; norm_num,
    electron_raw_S_positive
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PhotonicForge.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())