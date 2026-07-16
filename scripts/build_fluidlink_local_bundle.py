#!/usr/bin/env python3
"""FluidLink local bundle — Kronos archive sync, Tier 50, observer loop, Living FSOT audit."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "fluidlink_local_bundle_report.json"

STEPS = [
    ("Sync Kronos → I: archive", ["scripts/sync_kronos_to_archive.py"]),
    ("Ingest Kronos metrology", ["scripts/ingest_kronos_lab.py"]),
    ("Tier 50 / FluidLink benchmarks", ["scripts/build_tier_o_time_emergence_benchmarks.py"]),
    ("Desktop observer loop", ["scripts/run_desktop_observer_loop.py"]),
    ("Observer loop benchmark", ["scripts/build_desktop_observer_loop_benchmark.py"]),
    ("Living FSOT hardware audit", ["scripts/audit_living_fsot_hardware.py"]),
    ("Blueprint reverify (BH/WH)", ["scripts/reverify_blueprint_claim.py", "--blueprint", "bh_wh_cycle"]),
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
        "kronos_archive": r"I:\FSOT-Physical-Archive\06_Kronos-FluidLink\Kronos",
        "esp32": "deferred",
        "observer": "timing+display_proxy (no mic/camera)",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())