#!/usr/bin/env python3
"""Orchestrate practical pipeline — blueprints, observer arch, founding reconcile, volumes."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "practical_pipeline_bundle_report.json"

STEPS = [
    ("Tech blueprints registry", ["scripts/build_tech_blueprints_registry.py"]),
    ("Consciousness observer architecture", ["scripts/build_consciousness_observer_architecture.py"]),
    ("Practical pipeline volume", ["scripts/build_practical_pipeline_volume.py"]),
    ("Founding corpus reconcile", ["scripts/reconcile_founding_corpus.py"]),
    ("Credibility depth refresh", ["scripts/build_credibility_hardening_audit.py"]),
]


def main() -> int:
    results: list[dict] = []
    for label, args in STEPS:
        cmd = [sys.executable, str(ROOT / args[0]), *args[1:]]
        try:
            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=300)
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
        "esp32_policy": "deferred",
        "embodiment": "Living_FSOT_QEMU + desktop_observer_loop",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())