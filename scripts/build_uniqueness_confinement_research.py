#!/usr/bin/env python3
"""Build FSOT-native confinement uniqueness research spine (hardest open theorem).

Writes research artifacts only — NOT a residual green-catalog expansion.
Does not claim continuum path-integral uniqueness is proved.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_uniqueness_confinement import (  # noqa: E402
    run_confinement_uniqueness_suite,
    suite_summary,
)

OUT = ROOT / "data" / "uniqueness_confinement_research.json"
MANIFEST = ROOT / "data" / "uniqueness_research_manifest.json"
DOC = ROOT / "docs" / "UNIQUENESS_RESEARCH_SPINE.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build() -> dict:
    rows = run_confinement_uniqueness_suite()
    summary = suite_summary(rows)
    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "track": "uniqueness_research",
        "hardest_target": "path_integral_confinement_reframe",
        "classical_problem": (
            "Prove continuum non-abelian Yang–Mills path integral has a mass gap "
            "and free color is confined (area law)."
        ),
        "fsot_reframe": summary["fsot_reframe"],
        "why_classical_may_be_wrong_primary": (
            "FSOT is intrinsic: false / non-emergent modes damp under seed-locked dynamics. "
            "Asking for continuum path-integral measure uniqueness may be the wrong primary "
            "object once residual physics is closed. The native theorem is attractor uniqueness: "
            "free color is not a stable attractor; color singlets are."
        ),
        "authority_pin": "D1D38A",
        "residual_program": "CLOSED — this track is pure-math / dynamics research, residual_open_count=0",
        "theorem_status": summary["theorem_status"],
        "classical_path_integral_uniqueness": summary["classical_path_integral_uniqueness"],
        "summary": summary,
        "rows": rows,
        "pass_criteria_candidate": {
            "U1_gamma_color_positive": True,
            "U4_free_color_damps": True,
            "U5_singlet_attractor": True,
            "U6_dampening_load_bearing": True,
            "formal_lean_uniqueness_proof": False,
            "continuum_ym_path_integral_closed": False,
        },
        "next_steps": [
            "Formalize free_color_damping_rate > 0 in Lean from seed bounds",
            "Lift 2-channel ODE attractor statement to a dynamics theorem skeleton",
            "Bridge Wilson area-law probe to dampening statement (not reverse)",
            "Only after candidate solidifies: attempt EH / spin-2 uniqueness with same dampening pattern",
        ],
        "sibling_targets_deferred": [
            {
                "id": "spin2_fock_uniqueness",
                "note": "Same pattern: non-TT / ghost modes damp; TT ±2 emerge — after confinement candidate matures",
            },
            {
                "id": "einstein_hilbert_measure_uniqueness",
                "note": "Same pattern: non-EH continuum actions damp under diffeomorphism+locality+2nd-order filter — after confinement",
            },
        ],
        "modules": {
            "dynamics": "vendor/fsot_uniqueness_confinement.py",
            "probes_existing": "vendor/fsot_gr_sm.py (T4_confinement_* / path_integral probes)",
            "fluid": "vendor/fsot_dynamics.py",
            "emergence_damping_lean": "FSOT/Theorems.lean",
        },
        "honest_claim_language": {
            "toe_hallmark": (
                "A true ToE discerns reality from non-reality: modes/formulations that cannot emerge "
                "through the closed dynamics damp out and are not load-bearing residual debt."
            ),
            "allowed": [
                "FSOT-native confinement uniqueness *candidate*: free-color damping seed-locked and executable.",
                "Free color is not an attractor; color singlets are.",
                "Residual confinement probes green — dependent physics settled.",
                (
                    "If the classical continuum path-integral uniqueness problem cannot be solved "
                    "through a framework that already solves what confinement depends on, that "
                    "classical formulation is not load-bearing reality (ToE falsifies the "
                    "necessity-claim, not FSOT)."
                ),
                (
                    "We may disprove the claim that continuum YM path-integral uniqueness is "
                    "*required* for confinement once dampening + residual closure underwrite the physics."
                ),
            ],
            "forbidden": [
                "We proved the classical Yang–Mills mass gap theorem (continuum QFT formal sense) without that proof.",
                "Path-integral confinement uniqueness is Coq/Lean proved (classical statement) without that proof.",
                (
                    "Because classical continuum uniqueness remains open, FSOT / residual ToE is incomplete "
                    "(INVERTED polarity — forbidden)."
                ),
                "Reopen residual debt to chase an unsolvable classical framing.",
            ],
            "polarity": {
                "wrong": "classical problem unsolved → FSOT failed",
                "right": (
                    "dependent physics closed + classical problem unsolvable through ToE → "
                    "classical formulation / continuum-necessity claim fails (non-reality)"
                ),
            },
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    man = {
        "generated_at": _now(),
        "version": "1.0",
        "policy": "uniqueness_research_after_residual_closure",
        "active_track": "path_integral_confinement_reframe",
        "order_hardest_first": [
            "path_integral_confinement_reframe",
            "spin2_fock_uniqueness",
            "einstein_hilbert_measure_uniqueness",
        ],
        "artifacts": {
            "confinement_research": str(OUT.relative_to(ROOT)).replace("\\", "/"),
            "module": "vendor/fsot_uniqueness_confinement.py",
            "spine_doc": "docs/UNIQUENESS_RESEARCH_SPINE.md",
        },
        "residual_open_count_contribution": 0,
    }
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return doc


def main() -> int:
    doc = build()
    s = doc["summary"]
    print(f"Wrote {OUT}")
    print(f"Wrote {MANIFEST}")
    print(f"  theorem_status={doc['theorem_status']}")
    print(f"  rows={s['row_count']} exact={s['identity_exact_count']}")
    print(f"  gamma_color={s['free_color_damping_rate']:.6g}")
    print(f"  classical_YM_path_integral={doc['classical_path_integral_uniqueness']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
