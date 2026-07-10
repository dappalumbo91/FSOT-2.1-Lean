#!/usr/bin/env python3
"""Run FSOT Time Emergence / Fluid Phase Current simulation against real anchors."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from time_emergence_lib import (  # noqa: E402
    REAL_ANCHORS,
    build_time_emergence_benchmark,
    compute_fpc,
    domain_input,
    fsot,
    load_fsot_compute,
)

OUT_BENCH = ROOT / "data" / "time_emergence_simulation_benchmark.json"
OUT_REPORT = ROOT / "data" / "time_emergence_simulation_report.json"


def main() -> int:
    fsot_mod, auth = load_fsot_compute()
    print("=" * 80)
    print("FSOT TIME EMERGENCE / FLUID PHASE CURRENT (FPC) SIMULATION")
    print("Engine:", auth)
    print("Hypothesis: time = emergent phase-current byproduct, not fundamental coordinate")
    print("=" * 80)
    print("\n[Real observational anchors]")
    for key, meta in REAL_ANCHORS.items():
        print(f"  {key}: {meta['value']} {meta.get('unit', '')} — {meta['source']}")

    doc = build_time_emergence_benchmark()
    OUT_BENCH.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_BENCH}")
    print(f"  records={doc.get('record_count')} pooled_median={doc.get('pooled_median_error_pct')}")
    print(f"  status={doc.get('simulation_status')}")
    val = doc.get("validation_summary") or {}
    print(f"  max_material_err={val.get('max_material_error_pct')}% fsot_aligned={val.get('fsot_precision_aligned')}")

    # Console summary of key FPC rows
    print("\n[Multi-scale FPC panel]")
    for r in doc.get("material_records") or []:
        if r.get("lab") == "time_emergence_lab" and r.get("property") in {
            "fast_tick_log_ratio",
            "gr_dilation_factor",
            "bh_dilation_photon_sphere",
            "bh_dilation_isco",
            "emergence_damping_arrow",
        }:
            extra = ""
            if r.get("dilation_horizon_corrected") is not None:
                extra = (
                    f" raw={r.get('dilation_raw_ratio')} horizon={r.get('dilation_horizon_corrected')}"
                    f" tunnel={r.get('quantum_tunnel_burst')} eddy={r.get('whirlpool_eddy_horizon')}"
                )
            print(f"  {r['name']}: computed={r['computed']} measured={r['measured']} err={r['error_pct']}%{extra}")

    print("\n[NULL Island diurnal — prime meridian 0N 0E]")
    for r in doc.get("material_records") or []:
        if r.get("lab") == "null_island_diurnal_lab" and r.get("property") == "time_solidification":
            print(f"  {r['name']} phase={r.get('earth_phase_rad')} solid={r['computed']} fpc_rate={r.get('fpc_rate_proxy')}")

    print("\n[Navigation modes — sailor/submarine analogy]")
    for r in doc.get("material_records") or []:
        if r.get("lab") == "fpc_navigation_lab" and r.get("property") == "navigation_mode":
            print(f"  {r['name']}: FPC_rate={r['computed']} S={r.get('S')} flow={r.get('flow_balance')}")

    # Quick engine spot-check (atomic domain default)
    atomic_si = domain_input("Atomic_Physics")
    atomic_fpc = compute_fpc(atomic_si)
    print("\n[Engine spot-check Atomic_Physics]")
    print(f"  S={atomic_fpc['S']:.6f} quirk={atomic_fpc['quirk_mod']:.4f} FPC_rate={atomic_fpc['fpc_rate_proxy']:.4f}")

    val = doc.get("validation_summary") or {}
    report = {
        "generated_at": doc.get("generated_at"),
        "physics_ontology": {
            "name": "Fluid Phase Current",
            "shorthand": "FPC / phase current",
            "liquid_state": "unobserved superfluid possibility space",
            "solidification": "quirk_mod + observed=True locks sequential now",
            "reversal_deSolidify": "observed=False re-fluidizes definite sequence",
            "reversal_valve": "BH poof/suction swap enables local counter-current / eddy",
            "time_fold_back": "Tier-49 fold_valve_relief — poof backflow at compression valves (theoretically allows local counter-current; global arrow preserved)",
        },
        "simulation_status": doc.get("simulation_status"),
        "record_count": doc.get("record_count"),
        "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
        "null_island_anchor": doc.get("null_island_anchor"),
        "fold_correction": doc.get("fold_correction"),
        "validation_summary": val,
        "bh_dilation_remedy": {
            "prior_error_pct": 12.2,
            "intermediate_error_pct": 1.39,
            "current_error_pct": val.get("bh_dilation_error_pct"),
            "root_cause": "asymmetric flow branch + unmodeled EH froth/tunnel/eddy currents",
            "fix": "unified tau_rate + fold/tunnel/eddy + froth_tau_bleed (POOF/φ³)",
            "whirlpool_analogy": "observe froth layer at EH, not interior suction vortex; 25D fluid poof tunnel",
        },
        "fsot_precision_alignment": {
            "pattern": val.get("validation_pattern"),
            "max_material_error_pct": val.get("max_material_error_pct"),
            "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
            "aligned": val.get("fsot_precision_aligned"),
            "tier_49_comparable_median_pct": 0.022,
        },
        "official_domain": True,
        "tier": 50,
        "next_steps": [
            "python scripts/build_tier_o_time_emergence_benchmarks.py",
            "python scripts/gen_time_emergence_lean.py",
            "python scripts/build_domain_coupling_simulation.py",
        ],
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_REPORT}")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())