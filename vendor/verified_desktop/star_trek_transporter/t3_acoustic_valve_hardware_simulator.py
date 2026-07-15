#!/usr/bin/env python3
"""
FSOT transporter — T3 acoustic phase valve hardware prototype.

Models piezo-stack actuator + resonant cavity phase valve that locks scan-grid
acoustic phase to the pattern-buffer T3 channel (pad A emitter side).
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

OUT_DEFAULT = Path(__file__).with_name("t3_acoustic_valve_hardware_results.json")

# Murata-class 40 kHz ultrasonic transducer envelope (hardware prototype spec)
RESONANCE_HZ = 40_000.0
PIEZO_STACK_V_PP = 24.0
CAVITY_LENGTH_M = 0.042
ACOUSTIC_IMPEDANCE_KG_M2_S = 1.48e6
T3_PHASE_TARGET = 1.0
PHI_LOCK = 0.95


def run_sim(*, steps: int = 12) -> dict:
    poof = math.exp((-math.log(math.pi) / math.e) / ((1 / (math.pi - 1)) * math.log((1 + math.sqrt(5)) / 2)))
    scan_coupling = poof * PHI_LOCK
    actuator_rows = []
    for step in range(steps):
        phase_cmd = T3_PHASE_TARGET * (1.0 + 0.0015 * math.sin(step * 0.55))
        drive_v = PIEZO_STACK_V_PP * phase_cmd * scan_coupling
        cavity_phase = phase_cmd * (1.0 - 0.0008 * step)
        q_factor = 42.0 * (1.0 - 0.002 * step)
        impedance_match = 1.0 - abs(cavity_phase - T3_PHASE_TARGET) * 0.04
        beam_coupling = scan_coupling * impedance_match * (q_factor / 50.0)
        actuator_rows.append(
            {
                "step": step,
                "piezo_drive_v_pp": drive_v,
                "cavity_phase_rad": cavity_phase * math.pi,
                "resonance_hz": RESONANCE_HZ,
                "acoustic_q_factor": q_factor,
                "impedance_match_ratio": impedance_match,
                "t3_phase_lock_error": abs(cavity_phase - T3_PHASE_TARGET),
                "beam_coupling_efficiency": beam_coupling,
            }
        )
    summary = {
        "resonance_hz": RESONANCE_HZ,
        "piezo_stack_v_pp_nominal": PIEZO_STACK_V_PP,
        "cavity_length_m": CAVITY_LENGTH_M,
        "acoustic_impedance_kg_m2_s": ACOUSTIC_IMPEDANCE_KG_M2_S,
        "mean_t3_phase_lock_error": sum(r["t3_phase_lock_error"] for r in actuator_rows) / len(actuator_rows),
        "mean_beam_coupling_efficiency": sum(r["beam_coupling_efficiency"] for r in actuator_rows) / len(actuator_rows),
        "mean_impedance_match_ratio": sum(r["impedance_match_ratio"] for r in actuator_rows) / len(actuator_rows),
        "phi_lock_hardware": PHI_LOCK,
        "t3_valve_acoustic_phase": T3_PHASE_TARGET,
    }
    observables = [{"name": k, "value": v, "unit": "dimensionless" if "hz" not in k and "m" not in k and "kg" not in k and "v_pp" not in k else ("Hz" if "hz" in k else ("m" if k.endswith("_m") else ("V" if "v_pp" in k else "kg/(m²·s)")))} for k, v in summary.items()]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "simulator": "t3_acoustic_valve_hardware_simulator",
        "hardware_frame": {
            "actuator": "piezo_stack_PZT-5A_class",
            "valve_mechanism": "resonant_cavity_phase_lock",
            "pad_role": "transporter_pad_a_emitter",
            "coupling_channel": "pattern_buffer_t3_scan_grid",
        },
        "actuator_steps": actuator_rows,
        "summary": summary,
        "observables": observables,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT T3 acoustic valve hardware prototype simulator")
    parser.add_argument("--output", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args()
    doc = run_sim(steps=args.steps)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  mean beam coupling: {doc['summary']['mean_beam_coupling_efficiency']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())