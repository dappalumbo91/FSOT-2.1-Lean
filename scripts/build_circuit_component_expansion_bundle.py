#!/usr/bin/env python3
"""Orchestrate Tier 96 Phase 1 — catalog ingest, benchmarks, Lean priors, spine refresh."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "circuit_component_expansion_report.json"

STEPS = [
    ("Industry catalog ingest", ["scripts/ingest_circuit_component_catalogs.py"]),
    ("Circuit emergence benchmarks", ["scripts/build_circuit_component_emergence_benchmarks.py", "--skip-ingest"]),
    ("Circuit Lean priors", ["scripts/gen_circuit_component_emergence_lean.py"]),
    ("Circuit atlas scaffold refresh", ["scripts/build_circuit_component_atlas_scaffold.py"]),
]


def main() -> int:
    results: list[dict] = []
    for label, args in STEPS:
        cmd = [sys.executable, str(ROOT / args[0]), *args[1:]]
        try:
            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=600)
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
        "phase": "1",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())