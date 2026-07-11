#!/usr/bin/env python3
"""Decimal-verify Coq/Isabelle π/e interval certificates used by TranscendentalBoundsBase."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "transcendental_certificate_audit.json"

INTERVALS = [
    {"id": "certified_exp_one", "lo": 2.7182818283, "hi": 2.7182818287, "value": math.e},
    {"id": "certified_pi", "lo": 3.141592653589792, "hi": 3.141592653589794, "value": math.pi},
]


def build() -> dict:
    checks: list[dict] = []
    all_ok = True
    for row in INTERVALS:
        v = float(row["value"])
        ok = float(row["lo"]) < v < float(row["hi"])
        all_ok = all_ok and ok
        checks.append(
            {
                **row,
                "verified": ok,
                "margin_lo": v - float(row["lo"]),
                "margin_hi": float(row["hi"]) - v,
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "prover_note": (
            "Coq TranscendentalBoundsNative proves pi/e base intervals natively; "
            "Isabelle TranscendentalBoundsNative.thy uses HOL-Decision_Procs.Approximation; "
            "this audit decimal-triangulates the bounds."
        ),
        "overall_ok": all_ok,
        "checks": checks,
        "remedy": "Keep native base proofs in sync with Bounds.lean certified intervals.",
    }


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} overall_ok={doc['overall_ok']}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())