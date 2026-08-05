#!/usr/bin/env python3
"""Build reality-vs-fiction calibration + historical re-eval ledger.

Research track only — not residual green expansion.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_reality_fiction_calibration import results_as_dicts, run_all, summary  # noqa: E402

OUT = ROOT / "data" / "reality_fiction_calibration.json"
LEDGER = ROOT / "data" / "historical_reeval_ledger.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build() -> dict:
    results = run_all()
    s = summary(results)
    cases = results_as_dicts(results)

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "track": "reality_fiction_calibration",
        "authority_pin": "D1D38A",
        "residual_open_count_contribution": 0,
        "purpose": (
            "Calibrate ToE discernment: known reality holds, known fiction damps, "
            "historically early disproofs open for re-eval under residual+dampening+prereg."
        ),
        "summary": s,
        "cases": cases,
        "claim_language": {
            "allowed": [
                "Known fictions fail as load-bearing under FSOT dampening/filters.",
                "Known realities hold (emergence, scales, attractors).",
                "Historical disproofs can be reopened as REEVAL_OPEN candidates with new machinery.",
                "Classical continuum necessity claims can damp when dependent physics is closed under FSOT.",
            ],
            "forbidden": [
                "REEVAL_OPEN means the claim is proved true.",
                "Damping a necessity meta-claim means QCD residual physics is false.",
                "Calibration failure ⇒ reopen residual debt without diagnosis.",
                "Inverted polarity: open classical problem ⇒ FSOT incomplete.",
            ],
        },
        "modules": {
            "calibration": "vendor/fsot_reality_fiction_calibration.py",
            "confinement": "vendor/fsot_uniqueness_confinement.py",
            "spine_doc": "docs/UNIQUENESS_RESEARCH_SPINE.md",
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    reeval_cases = [c for c in cases if c["tier"] == "reeval_candidate"]
    ledger = {
        "generated_at": _now(),
        "version": "1.0",
        "title": "Historical re-evaluation ledger",
        "policy": (
            "Topics dismissed or 'disproved' before residual closure + multiprover + dampening "
            "may be reconsidered under those tools. Entry here is NOT endorsement."
        ),
        "status_values": {
            "REEVAL_OPEN": "Eligible for honest re-test; not asserted true",
            "FICTION_DAMPED": "Fails load-bearing under FSOT (known fiction calibration)",
            "REALITY_HOLDS": "Settled structure still holds",
        },
        "entries": [
            {
                "id": c["id"],
                "title": c["title"],
                "status": c["verdict"],
                "detail": c["detail"],
                "formula": c["formula"],
                "pass_calibration": c["pass_calibration"],
            }
            for c in reeval_cases
        ],
        "not_on_this_ledger": [
            {
                "id": "fluid_spacetime_omni",
                "note": "NOT re-eval — known reality R6/R7. FSOT is the fluid across all scales.",
            },
            {
                "id": "absolute_rest_frame",
                "note": "NOT re-eval — known fiction F3. Damps. Do not conflate with the fluid.",
            },
        ],
        "future_candidates_not_yet_cased": [
            {
                "id": "X1_modified_newtonian_dynamics_class",
                "note": "Re-eval only under contested cosmology prereg — not free fit",
            },
            {
                "id": "X2_hidden_variable_completions",
                "note": "Structure tests only; no claim of full completion",
            },
        ],
        "calibration_artifact": str(OUT.relative_to(ROOT)).replace("\\", "/"),
    }
    LEDGER.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return doc


def main() -> int:
    doc = build()
    s = doc["summary"]
    print(f"Wrote {OUT}")
    print(f"Wrote {LEDGER}")
    print(f"  verdict={s['verdict']} calibration_ok={s['calibration_ok']}")
    print(f"  reality pass={s['known_reality']['pass']}/{s['known_reality']['count']}")
    print(f"  fiction pass={s['known_fiction']['pass']}/{s['known_fiction']['count']}")
    print(f"  reeval  pass={s['reeval_candidate']['pass']}/{s['reeval_candidate']['count']}")
    return 0 if s["calibration_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
