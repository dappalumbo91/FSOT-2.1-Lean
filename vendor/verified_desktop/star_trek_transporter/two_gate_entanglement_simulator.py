#!/usr/bin/env python3
"""
FSOT transporter — two-gate entanglement pair (pad A ↔ pad B).

Models entangled gate coupling via warp actuation psi_gate_pair and phi_lock channel.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

OUT_DEFAULT = Path(__file__).with_name("two_gate_entanglement_results.json")

PHI_LOCK = 0.95
S_QM = 0.9555063001027196
INFO_PRESERVE = 0.981227203621


def run_sim() -> dict:
    psi_gate_pair = 0.043599802456
    psi_entangle = (PHI_LOCK**2) * (S_QM**2) * 0.059407798774 * INFO_PRESERVE
    gates = [
        {
            "gate_id": "transporter_pad_a",
            "role": "dematerialization_emitter",
            "portal_scalar": 0.009663204175,
            "phase_lock": PHI_LOCK,
        },
        {
            "gate_id": "transporter_pad_b",
            "role": "reassembly_receiver",
            "portal_scalar": 0.009663204175,
            "phase_lock": PHI_LOCK,
        },
    ]
    pair_rows = []
    for step in range(8):
        coupling = psi_gate_pair * (1.0 + 0.002 * math.sin(step * 0.7))
        fidelity = psi_entangle * (1.0 - 0.001 * step)
        pair_rows.append(
            {
                "step": step,
                "gate_pair_coupling": coupling,
                "entanglement_channel_fidelity": fidelity,
                "traverse_readiness": coupling * fidelity,
                "information_preserved": INFO_PRESERVE * (1.0 - 0.0003 * step),
            }
        )
    summary = {
        "mean_gate_pair_coupling": sum(r["gate_pair_coupling"] for r in pair_rows) / len(pair_rows),
        "mean_entanglement_fidelity": sum(r["entanglement_channel_fidelity"] for r in pair_rows) / len(pair_rows),
        "mean_traverse_readiness": sum(r["traverse_readiness"] for r in pair_rows) / len(pair_rows),
        "phi_lock": PHI_LOCK,
        "psi_gate_pair": psi_gate_pair,
        "psi_entangle_gate": psi_entangle,
    }
    observables = [{"name": k, "value": v, "unit": "dimensionless"} for k, v in summary.items()]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "simulator": "two_gate_entanglement_simulator",
        "gates": gates,
        "pair_steps": pair_rows,
        "summary": summary,
        "observables": observables,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT two-gate entanglement pair simulator")
    parser.add_argument("--output", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    doc = run_sim()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  traverse_readiness: {doc['summary']['mean_traverse_readiness']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())