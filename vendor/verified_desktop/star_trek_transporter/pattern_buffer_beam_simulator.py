#!/usr/bin/env python3
"""
FSOT Star Trek Transporter — pattern buffer + beam-forming scan simulator.

Models dematerialization scan grid, T3 valve acoustic phase lock, and reassembly
fidelity using FSOT seed-derived portal constants (poof, suction, coherence).
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path

OUT_DEFAULT = Path(__file__).with_name("pattern_buffer_scan_results.json")

# Human-scale transport envelope (adult male, 70 kg reference)
SCAN_VOLUME_M3 = 0.085
MASS_KG = 70.0
BEAM_RESOLUTION_M = 0.001
SCAN_TIME_MS = 50.0


def fsot_portal_constants() -> dict[str, float]:
    pi = math.pi
    e = math.e
    phi = (1 + math.sqrt(5)) / 2
    gamma = 0.57721566490153286060651209
    g_cat = 0.91596559417721901505460351
    psi_con = 1 - math.exp(-1)
    eta_eff = 1 / (pi - 1)
    theta_s = math.sin(psi_con * eta_eff)
    poof = math.exp((-math.log(pi) / e) / (eta_eff * math.log(phi)))
    c_eff = (1 - poof * math.sin(theta_s)) * (1 + 0.01 * g_cat / (pi * phi))
    suction = poof * (-math.cos(theta_s - pi))
    k = phi * (gamma / e) * math.sqrt(2) / math.log(pi) * 0.99
    return {
        "poof": poof,
        "suction": suction,
        "c_eff": c_eff,
        "k_coupling": k,
        "theta_s": theta_s,
        "coherence_efficiency": 0.9577,
        "information_preservation": 0.99,
        "t3_valve_acoustic_phase": 1.0,
    }


def run_sim(*, deep: bool = False) -> dict:
    c = fsot_portal_constants()
    res = BEAM_RESOLUTION_M
    voxels_per_axis = max(1, int(round((SCAN_VOLUME_M3 ** (1 / 3)) / res)))
    voxel_count = voxels_per_axis**3
    bits_per_voxel = 24.0
    pattern_buffer_bits = voxel_count * bits_per_voxel
    scan_steps = max(8, voxels_per_axis if deep else 12)
    beam_layers = []
    for step in range(scan_steps):
        phase = c["t3_valve_acoustic_phase"] * (1.0 - 0.001 * (step % 7))
        layer_coherence = c["coherence_efficiency"] * (1.0 - 0.0005 * step)
        layer_fidelity = c["information_preservation"] * layer_coherence * c["c_eff"]
        beam_layers.append(
            {
                "step": step,
                "t3_phase_lock": phase,
                "beam_layer_coherence": layer_coherence,
                "pattern_slice_fidelity": layer_fidelity,
                "poof_local": c["poof"] * (1.0 + 0.01 * math.sin(step * c["theta_s"])),
                "suction_local": c["suction"] * (1.0 + 0.01 * math.cos(step * c["theta_s"])),
            }
        )
    grid_medians = {
        "voxel_grid_count": float(voxel_count),
        "pattern_buffer_gbits": pattern_buffer_bits / 1e9,
        "beam_forming_layers": float(len(beam_layers)),
        "mean_layer_fidelity": sum(r["pattern_slice_fidelity"] for r in beam_layers) / len(beam_layers),
        "t3_phase_lock_mean": sum(r["t3_phase_lock"] for r in beam_layers) / len(beam_layers),
        "t3_phase_lock_min": min(r["t3_phase_lock"] for r in beam_layers),
        "dematerialization_scan_ms": SCAN_TIME_MS,
        "reassembly_lock_precision_m": res,
        "matter_stream_coherence": c["coherence_efficiency"] * c["k_coupling"],
        "transport_energy_proxy_MJ": pattern_buffer_bits * 1e-21 * 6.022e23 / MASS_KG,
        "bio_integrity_post_transport": c["information_preservation"] * c["coherence_efficiency"],
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "simulator": "pattern_buffer_beam_simulator",
        "desktop_folder": "FSOT, Star Trek Transporter",
        "scan_envelope": {
            "volume_m3": SCAN_VOLUME_M3,
            "mass_kg": MASS_KG,
            "beam_resolution_m": res,
        },
        "fsot_constants": c,
        "beam_layers": beam_layers if deep else beam_layers[:12],
        "grid_summary": grid_medians,
        "observables": [
            {"name": k, "value": v, "unit": "dimensionless" if "gbits" not in k and "MJ" not in k and "ms" not in k and "_m" not in k else "scaled"}
            for k, v in grid_medians.items()
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="FSOT transporter pattern buffer beam simulator")
    parser.add_argument("--deep", action="store_true", help="Full beam-layer sweep")
    parser.add_argument("--output", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    doc = run_sim(deep=args.deep)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  voxels: {doc['grid_summary']['voxel_grid_count']:.0f}")
    print(f"  mean layer fidelity: {doc['grid_summary']['mean_layer_fidelity']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())