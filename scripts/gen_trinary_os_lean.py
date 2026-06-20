#!/usr/bin/env python3
"""Generate FSOT/Formal/TrinaryOSPriors.lean from trinary_os registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"
OUTPUT_PATH = ROOT / "FSOT" / "Formal" / "TrinaryOSPriors.lean"


def build_lean(registry: dict) -> str:
    tri = registry.get("trinary_os", {})
    consts = tri.get("constants", {})
    slots = consts.get("num_task_slots", 8)
    width = consts.get("trit_word_width", 27)
    layers = consts.get("cortical_layers", 6)
    hello_sz = tri.get("hello_file_size", 264)
    call_sz = tri.get("call_ret_file_size", 312)
    spawn_sz = tri.get("spawn_join_file_size", 440)

    return f"""/-
  FSOT Formal TrinaryOSPriors — FSOTB oracle and ISA-derived constant certificates.

  Source: Fsot trinary/fsot_os target/*.oracle.json
  Generator: scripts/gen_trinary_os_lean.py
-/

import FSOT.Formal.Bounds
import FSOT.Formal.Scalar

namespace FSOT.Formal

noncomputable section

def trinary_os_task_slots : ℕ := {slots}
def trinary_os_word_width : ℕ := {width}
def trinary_os_cortical_layers : ℕ := {layers}
def trinary_os_hello_bytes : ℕ := {hello_sz}
def trinary_os_call_ret_bytes : ℕ := {call_sz}
def trinary_os_spawn_join_bytes : ℕ := {spawn_sz}

theorem trinary_os_word_width_eq_27 : trinary_os_word_width = 27 := by
  unfold trinary_os_word_width; norm_num

theorem trinary_os_hello_smaller_than_spawn :
    trinary_os_hello_bytes < trinary_os_spawn_join_bytes := by
  unfold trinary_os_hello_bytes trinary_os_spawn_join_bytes; norm_num

/-- Bundle: FSOTB regression sizes and derived trinary ISA geometry (K coupling positive). -/
theorem trinary_os_fsotb_bundle :
    trinary_os_task_slots = {slots} ∧
    trinary_os_word_width = {width} ∧
    trinary_os_cortical_layers = {layers} ∧
    trinary_os_hello_bytes = {hello_sz} ∧
    trinary_os_call_ret_bytes = {call_sz} ∧
    trinary_os_spawn_join_bytes = {spawn_sz} ∧
    trinary_os_hello_bytes < trinary_os_spawn_join_bytes ∧
    (0.42 : ℝ) < k := by
  refine ⟨
    by unfold trinary_os_task_slots; norm_num,
    by unfold trinary_os_word_width; norm_num,
    by unfold trinary_os_cortical_layers; norm_num,
    by unfold trinary_os_hello_bytes; norm_num,
    by unfold trinary_os_call_ret_bytes; norm_num,
    by unfold trinary_os_spawn_join_bytes; norm_num,
    trinary_os_hello_smaller_than_spawn,
    k_gt_0420
  ⟩

end

end FSOT.Formal
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TrinaryOSPriors.lean")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    args.output.write_text(build_lean(registry), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())