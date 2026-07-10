#!/usr/bin/env python3
"""Audit Lean/JSON vs Rust executable obligation replay coverage."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import obligation_provable, python_verify_obligation  # noqa: E402
from rust_replay_lib import (  # noqa: E402
    OBL_FORMAL,
    OBL_TRANSCENDENTAL,
    RUST_DIR,
    python_verify_transcendental,
)

OUT = ROOT / "data" / "cross_refinement_rust_report.json"


def main() -> int:
    formal = json.loads(OBL_FORMAL.read_text(encoding="utf-8"))
    provable = [ob for ob in formal["obligations"] if obligation_provable(ob)]
    trans = []
    if OBL_TRANSCENDENTAL.exists():
        trans = json.loads(OBL_TRANSCENDENTAL.read_text(encoding="utf-8")).get("obligations") or []

    meta_path = RUST_DIR / "obligation_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    formal_ok = sum(1 for ob in provable if python_verify_obligation(ob))
    trans_results: list[dict] = []
    trans_ok = 0
    for ob in trans:
        py = python_verify_transcendental(ob)
        ok = py is True
        trans_ok += int(ok)
        trans_results.append({"id": ob["id"], "python_f64_ok": ok, "skipped": py is None})

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "84_cross_refinement_rust",
        "formal_provable_count": len(provable),
        "formal_python_f64_ok": formal_ok,
        "transcendental_count": len(trans),
        "transcendental_python_f64_ok": trans_ok,
        "rust_meta": meta,
        "total_exported_to_rust": meta.get("total_count", 0),
        "overall_ok": formal_ok == len(provable)
            and trans_ok == len(trans)
            and meta.get("total_count") == len(provable) + len(trans),
        "note": (
            "Rust replay uses f64 execution; formal spine matches Python decimal when obligations are float-stable."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-REFINEMENT RUST EXECUTABLE AUDIT")
    print(f"  formal provable: {len(provable)} (f64 oracle {formal_ok})")
    print(f"  transcendental: {len(trans)} (f64 oracle {trans_ok})")
    print(f"  rust exported: {meta.get('total_count', 0)}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())