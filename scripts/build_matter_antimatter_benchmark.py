#!/usr/bin/env python3
"""Build matter/antimatter + baryon asymmetry residual panel.

FSOT mathematics only (seeds + domain_scalar duals). No free fits.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_matter_antimatter import run_matter_antimatter_suite, suite_summary  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402
from benchmark_margin_lib import classify_record  # noqa: E402

OUT = ROOT / "data" / "matter_antimatter_benchmark.json"
REPORT = ROOT / "data" / "matter_antimatter_research.json"
MANIFEST = ROOT / "data" / "matter_antimatter_manifest.yaml"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    _, authority = _load_fsot()
    rows = run_matter_antimatter_suite()
    summary = suite_summary(rows)

    # Material: all rows; classify will mark identities/structural
    scalar_errs = [
        float(r["error_pct"])
        for r in rows
        if classify_record(r) == "scalar" and r.get("error_pct") is not None
    ]
    # For identities error is 0 — still include all residual-capable
    all_errs = [float(r["error_pct"]) for r in rows]

    doc = _bench_v11(
        domain="Matter_Antimatter",
        material_records=rows,
        maps_to_lean=["particle", "nuclear", "cosmological"],
        d_eff=5,
        authority_path=authority,
        source=[
            "vendor/fsot_matter_antimatter.py",
            "vendor/fsot_compute.py wave1 Omega_b_h2 / wave10 eta_baryon_photon",
            "PDG 2024 mass anchors",
            "Planck 2018 eta / Omega_b h2 class",
        ],
        channel_stats=[
            ("fsot_prediction", "matter_antimatter", all_errs or [0.0]),
            ("seed_identity", "cpt_and_thresholds", scalar_errs or [0.0]),
        ],
        sota_baselines={
            "sakharov_qualitative": {
                "sota_typical_error_pct": 50.0,
                "sota_model": "Qualitative baryogenesis (no unique seed η in SM alone)",
            },
            "pdg_mass_equality": {
                "sota_typical_error_pct": 0.01,
                "sota_model": "PDG CPT tests / mass equality",
            },
        },
    )
    doc["policy"] = "fsot_seed_locked_matter_antimatter"
    doc["residual_law"] = "make_fsot_record / seed identities + domain duals"
    doc["ontology"] = summary["ontology"]
    doc["honest_scope"] = summary["honest_scope"]
    doc["summary_physics"] = {
        "eta_baryon_photon": summary["eta_baryon_photon"],
        "Omega_b_h2": summary["Omega_b_h2"],
        "S_matter_particle": summary["S_matter_particle"],
        "S_antimatter_conjugate": summary["S_antimatter_conjugate"],
        "asymmetry_emergence_factor": summary["asymmetry_emergence_factor"],
        "bulk_antimatter_damped": summary["bulk_antimatter_damped"],
    }
    doc["generated_at"] = _now()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    research = {
        "generated_at": _now(),
        "version": "1.0",
        "track": "matter_antimatter",
        "benchmark": "data/matter_antimatter_benchmark.json",
        "module": "vendor/fsot_matter_antimatter.py",
        "builder": "scripts/build_matter_antimatter_benchmark.py",
        "summary": summary,
        "claims_allowed": [
            "CPT mass equality residual identity under FSOT conjugate mode",
            "Pair thresholds 2m as structural identities",
            "Seed η = Poof^11/(πγ) residual-gated to Planck class",
            "Ω_b h² = |S_cosmo|(1−S_quant) residual-gated",
            "Matter emergence S>0; conjugate dual distinct; bulk antimatter damped with S_cosmo<0",
        ],
        "claims_forbidden": [
            "Full continuum Sakharov path-integral baryogenesis theorem proved",
            "Antimatter is a separate free-parameter Lagrangian sector",
            "Absolute rest aether required for antimatter",
        ],
        "hierarchy_attachment": {
            "seeds": ["pi", "e", "phi", "gamma", "G_Catalan", "POOF"],
            "interfaces": ["Particle_Physics", "Nuclear_Physics", "Cosmology", "Quantum_Mechanics"],
            "emergence_ladder_note": (
                "Micro particle interface (D~5) hosts matter/antimatter duals; "
                "cosmology ceiling (D=25) damps bulk antimatter residual density via η≪1"
            ),
        },
        "prior_fsot_compute": {
            "eta_baryon_photon": "vendor/fsot_compute.py wave10",
            "Omega_b_h2": "vendor/fsot_compute.py wave1",
        },
    }
    REPORT.write_text(json.dumps(research, indent=2), encoding="utf-8")

    MANIFEST.write_text(
        "\n".join(
            [
                "# Matter / antimatter + baryon asymmetry (FSOT fluid-scalar)",
                "version: '1.0'",
                "updated: '2026-08-05'",
                "domain: Matter_Antimatter",
                "D_eff: 5",
                "maps_to_lean: [particle, nuclear, cosmological]",
                "module: vendor/fsot_matter_antimatter.py",
                "build: scripts/build_matter_antimatter_benchmark.py",
                "benchmark: data/matter_antimatter_benchmark.json",
                "research: data/matter_antimatter_research.json",
                "ontology: fluid_spacetime_omni",
                "note: >",
                "  Matter emergence + antimatter conjugate dual + seed η/Ω_b.",
                "  Not a separate free-parameter antimatter sector.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote {OUT}")
    print(f"  n={doc.get('record_count')} pooled={doc.get('pooled_median_error_pct')}%")
    print(f"  eta={summary['eta_baryon_photon']:.6e} Omega_b_h2={summary['Omega_b_h2']:.6g}")
    print(f"  S_m={summary['S_matter_particle']:.6g} S_conj={summary['S_antimatter_conjugate']:.6g}")
    print(f"Wrote {REPORT}")
    print(f"Wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
