#!/usr/bin/env python3
"""
FSOT transporter — pad B receiver hardware prototype.

Models reassembly-side acoustic phase capture valve coupled to two-gate entanglement
pair (pad A emitter ↔ pad B receiver) via psi_gate_pair and pattern-buffer lock.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

OUT_DEFAULT = Path(__file__).with_name("pad_b_receiver_hardware_results.json")

RESONANCE_HZ = 40_000.0
CAPTURE_COIL_V_PP = 18.0
RECEIVER_CAVITY_M = 0.044
PHI_LOCK = 0.95
PSI_GATE_PAIR = 0.043599802456
INFO_PRESERVE = 0.981227203621
REASSEMBLY_PHASE_TARGET = 1.0


def run_sim(*, steps: int = 12) -> dict:
    poof = math.exp((-math.log(math.pi) / math.e) / ((1 / (math.pi - 1)) * math.log((1 + math.sqrt(5)) / 2)))
    gate_coupling = PSI_GATE_PAIR * PHI_LOCK * poof
    receiver_rows = []
    for step in range(steps):
        phase_capture = REASSEMBLY_PHASE_TARGET * (1.0 - 0.0012 * step + 0.0009 * math.sin(step * 0.48))
        capture_v = CAPTURE_COIL_V_PP * phase_capture * gate_coupling
        impedance_match = 1.0 - abs(phase_capture - REASSEMBLY_PHASE_TARGET) * 0.035
        pattern_capture = gate_coupling * impedance_match * (1.0 - 0.0006 * step)
        reassembly_lock = pattern_capture * INFO_PRESERVE * (1.0 - 0.0004 * step)
        receiver_rows.append(
            {
                "step": step,
                "capture_coil_v_pp": capture_v,
                "receiver_phase_rad": phase_capture * math.pi,
                "resonance_hz": RESONANCE_HZ,
                "impedance_match_ratio": impedance_match,
                "reassembly_phase_lock_error": abs(phase_capture - REASSEMBLY_PHASE_TARGET),
                "pattern_capture_efficiency": pattern_capture,
                "matter_stream_lock_fidelity": reassembly_lock,
            }
        )
    summary = {
        "resonance_hz": RESONANCE_HZ,
        "capture_coil_v_pp_nominal": CAPTURE_COIL_V_PP,
        "receiver_cavity_m": RECEIVER_CAVITY_M,
        "mean_reassembly_phase_lock_error": sum(r["reassembly_phase_lock_error"] for r in receiver_rows) / len(receiver_rows),
        "mean_pattern_capture_efficiency": sum(r["pattern_capture_efficiency"] for r in receiver_rows) / len(receiver_rows),
        "mean_matter_stream_lock_fidelity": sum(r["matter_stream_lock_fidelity"] for r in receiver_rows) / len(receiver_rows),
        "phi_lock_receiver": PHI_LOCK,
        "psi_gate_pair_coupling": PSI_GATE_PAIR,
        "reassembly_phase_target": REASSEMBLY_PHASE_TARGET,
    }
    observables = [
        {
            "name": k,
            "value": v,
            "unit": (
                "dimensionless"
                if "hz" not in k and "m" not in k and "v_pp" not in k
                else ("Hz" if "hz" in k else ("m" if k.endswith("_m") else "V"))
            ),
        }
        for k, v in summary.items()
    ]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "simulator": "pad_b_receiver_hardware_simulator",
        "hardware_frame": {
            "actuator": "capture_coil_PZT-5A_class",
            "valve_mechanism": "phase_conjugate_reassembly_lock",
            "pad_role": "transporter_pad_b_receiver",
            "coupling_channel": "two_gate_entanglement_pair",
        },
        "receiver_steps": receiver_rows,
        "summary": summary,
        "observables": observables,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT pad B receiver hardware prototype simulator")
    parser.add_argument("--output", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--steps", type=int, default=12)
    args = parser.parse_args()
    doc = run_sim(steps=args.steps)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  mean matter-stream lock: {doc['summary']['mean_matter_stream_lock_fidelity']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())