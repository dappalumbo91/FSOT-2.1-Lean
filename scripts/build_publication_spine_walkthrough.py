#!/usr/bin/env python3
"""Build publication spine walkthrough JSON — seeds → raw_S → domain → observable."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from domain_scalar_oracle import (  # noqa: E402
    ALPHA,
    CONSCIOUSNESS_FACTOR,
    ETA_EFF,
    FSOTParams,
    K,
    PSI_CON,
    raw_S,
)

OUT = ROOT / "data" / "publication_spine_walkthrough.json"
EMPIRICAL = ROOT / "data" / "empirical_accuracy_closure.json"
CONTESTED = ROOT / "data" / "contested_observables_closure.json"
H0_BENCH = ROOT / "data" / "h0_planck_benchmark.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def build() -> dict:
    empirical = _load(EMPIRICAL)
    contested = _load(CONTESTED)
    h0 = _load(H0_BENCH)

    cosmology_raw = raw_S(
        FSOTParams(D_eff=25, recent_hits=3, delta_psi=1.0, delta_theta=1.0, observed=False)
    )
    quantum_raw = raw_S(
        FSOTParams(D_eff=18, recent_hits=3, delta_psi=0.88, delta_theta=1.0, observed=True)
    )

    h0_row = next(
        (r for r in (h0.get("records") or []) if r.get("property") == "H0_planck_km_s_Mpc"),
        {},
    )
    h0_contested = [
        o
        for o in (contested.get("observables") or [])
        if str(o.get("property") or "") == "hubble_constant"
    ]

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "title": "FSOT single-spine fractal walkthrough",
        "chain": [
            {
                "step": 1,
                "label": "Geometric seeds",
                "detail": "π, e, φ (golden ratio), γ (Euler–Mascheroni), G (Catalan)",
                "artifact": "FSOT/Scalar.lean lines 17–23",
            },
            {
                "step": 2,
                "label": "Intrinsic constants (no per-observable tuning)",
                "detail": {
                    "alpha": round(ALPHA, 12),
                    "psi_con": round(PSI_CON, 12),
                    "eta_eff": round(ETA_EFF, 12),
                    "consciousness_factor": round(CONSCIOUSNESS_FACTOR, 12),
                    "k": round(K, 12),
                },
                "artifact": "FSOT/Scalar.lean + domain_scalar_oracle.py",
            },
            {
                "step": 3,
                "label": "Core scalar engine",
                "formula": "raw_S = term1_final + term2 + term3",
                "term1": "(N·P/√D_eff)·cos((ψ_con+δψ)/η_eff)·growth·coherence·perceived_adjust × quirk_mod(observed)",
                "term2": "scale·amplitude + trend_bias",
                "term3": "chaotic bleed (β, δψ, δθ, D_eff coupling)",
                "artifact": "FSOT/Scalar.lean compute_raw_S_D_chaotic",
            },
            {
                "step": 4,
                "label": "Fractal domain fold",
                "detail": "D_eff, δψ, recent_hits, observed — manifest-declared fold of the same engine per scale",
                "examples": {
                    "cosmological": {"D_eff": 25, "raw_S_oracle": round(cosmology_raw, 6)},
                    "quantum_observed": {"D_eff": 18, "raw_S_oracle": round(quantum_raw, 6)},
                },
                "artifact": "data/extension_domains_manifest.yaml + proof_ledger.yaml",
            },
            {
                "step": 5,
                "label": "Formula corpus → observable",
                "detail": "1,325 unique observables live-recompute from spine (no least-squares per row)",
                "stats": empirical.get("formula_corpus_unique") or {},
                "artifact": "vendor/formula_corpus/by_domain/strict_empirical.jsonl",
            },
            {
                "step": 6,
                "label": "Public measurement cross-check",
                "detail": "374 benchmark files vs Planck, Riess, DESI, Zebrahub, NOAA, The Well, …",
                "stats": empirical.get("benchmark_envelope") or {},
                "artifact": "data/benchmark_margin_audit.json",
            },
        ],
        "worked_example_h0_planck": {
            "observable": "H0_planck_km_s_Mpc",
            "measured": h0_row.get("measured"),
            "measured_uncertainty": h0_row.get("measured_uncertainty"),
            "fsot_computed": h0_row.get("computed"),
            "error_pct": h0_row.get("error_pct"),
            "formula": h0_row.get("formula"),
            "reference": h0_row.get("reference"),
        },
        "contested_sector_summary": contested.get("panel_summary") or {},
        "h0_readouts": h0_contested,
        "cross_proof": {
            "github_ready": _load(ROOT / "data" / "cross_proof_verification_report.json").get(
                "github_ready"
            ),
            "seven_way_bare_metal": _load(ROOT / "data" / "cross_proof_verification_report.json").get(
                "seven_way_bare_metal"
            ),
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def main() -> int:
    doc = build()
    print(f"Wrote {OUT}")
    print(f"  chain steps: {len(doc.get('chain') or [])}")
    print(f"  H0 Planck error: {(doc.get('worked_example_h0_planck') or {}).get('error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())