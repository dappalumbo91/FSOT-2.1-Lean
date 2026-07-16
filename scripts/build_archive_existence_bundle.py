#!/usr/bin/env python3
"""Archive existence bundle — sync stack, coupling sim, existence sim, FluidLink."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "publication" / "archive_existence_bundle_report.json"

STEPS = [
    ("Domain coupling simulation", ["scripts/build_domain_coupling_simulation.py"]),
    ("Orbital prediction analysis", ["scripts/analyze_domain_orbital_predictions.py"]),
    ("Existence simulation gap fill", ["scripts/run_existence_simulation.py"]),
    ("Existence simulation benchmark", ["scripts/build_existence_simulation_benchmark.py"]),
    ("Ring in existence failures", ["scripts/ring_in_existence_failures.py"]),
    ("Existence refinement benchmark", ["scripts/build_existence_refinement_benchmark.py"]),
    ("Verify independent predictions", ["scripts/verify_independent_predictions.py"]),
    ("FluidLink local bundle", ["scripts/build_fluidlink_local_bundle.py"]),
    ("Sync verification stack → I:", ["scripts/sync_archive_verification_stack.py"]),
]


def main() -> int:
    results: list[dict] = []
    for label, args in STEPS:
        cmd = [sys.executable, str(ROOT / args[0]), *args[1:]]
        try:
            r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=900)
            ok = r.returncode == 0
            tail = (r.stdout or r.stderr or "")[-600:]
        except Exception as exc:
            ok = False
            tail = str(exc)
        results.append({"step": label, "ok": ok, "tail": tail})
        print(f"{'OK' if ok else 'FAIL'} — {label}")

    sim_report = ROOT / "data" / "publication" / "existence_simulation_report.json"
    sim_summary = {}
    if sim_report.is_file():
        sim_summary = json.loads(sim_report.read_text(encoding="utf-8"))

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "steps": results,
        "all_ok": all(r["ok"] for r in results),
        "archive_root": r"I:\FSOT-Physical-Archive\09_Local-Verification-Stack",
        "existence_simulation": sim_summary,
        "independent_prediction_ledger": "data/publication/independent_prediction_ledger.yaml",
        "policy": "synthetic gap fill + locked FSOT predictions for real-data verification",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  all_ok={doc['all_ok']}")
    if sim_summary:
        print(f"  gap_fill_count={sim_summary.get('gap_fill_count')}")
        print(f"  verify_median={sim_summary.get('verification_pooled_median_error_pct')}%")
    return 0 if doc["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())