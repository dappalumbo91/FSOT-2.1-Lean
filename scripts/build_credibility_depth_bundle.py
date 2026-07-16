#!/usr/bin/env python3
"""Credibility depth orchestration — lean routes, live ingest, circuit Phase 1, hardening audit."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "credibility_depth_bundle_report.json"

STEPS = [
    ("Lean route credibility expansion", ["scripts/build_lean_route_credibility_expansion.py"]),
    ("Live ingest refresh", ["scripts/build_live_ingest_refresh_bundle.py"]),
    ("Formula corpus honesty", ["scripts/build_formula_corpus_honesty_report.py"]),
    ("Wet-lab longevity refresh", ["scripts/build_wetlab_longevity_expansion_bundle.py"]),
    ("Tier 96 circuit Phase 1", ["scripts/build_circuit_component_expansion_bundle.py"]),
    ("Credibility hardening audit", ["scripts/build_credibility_hardening_audit.py"]),
]


def main() -> int:
    results: list[dict] = []
    for label, args in STEPS:
        cmd = [sys.executable, str(ROOT / args[0]), *args[1:]]
        try:
            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=900)
            ok = r.returncode == 0
            tail = (r.stdout or r.stderr or "")[-500:]
        except Exception as exc:
            ok = False
            tail = str(exc)
        results.append({"step": label, "ok": ok, "tail": tail})
        print(f"{'OK' if ok else 'FAIL'} — {label}")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "steps": results,
        "all_ok": all(r["ok"] for r in results),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())