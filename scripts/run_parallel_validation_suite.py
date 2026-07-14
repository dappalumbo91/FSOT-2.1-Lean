#!/usr/bin/env python3
"""Parallel validation: granular bench + intrinsic prediction + formal oracle checks."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "data" / "parallel_validation_suite_report.json"


def _run(script: str, *extra: str) -> dict:
    cmd = [sys.executable, str(SCRIPTS / script), *extra]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "script": script,
        "exit_code": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def main() -> int:
    steps = [
        _run("analyze_tier95_granular.py"),
        _run("run_tier95_predictive_crossval.py"),
        _run("verify_extension_domains.py"),
    ]

    cross_path = ROOT / "data" / "cross_proof_verification_report.json"
    cross_ok = None
    if cross_path.exists():
        cross_ok = json.loads(cross_path.read_text(encoding="utf-8")).get("overall_ok")

    pred = json.loads((ROOT / "data" / "tier95_predictive_crossval_report.json").read_text(encoding="utf-8"))
    granular = json.loads((ROOT / "data" / "tier95_granular_accuracy_report.json").read_text(encoding="utf-8"))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
        "granular_unique_error_pct": {
            p["domain"]: p.get("unique_reported_error_pct_values")
            for p in granular.get("panels") or []
        },
        "intrinsic_prediction": pred.get("mechanistic_median_error_pct"),
        "mpmath_equivalence_ok": pred.get("formal_oracle", {}).get("mpmath_float64_equiv_ok"),
        "cross_proof_overall_ok": cross_ok,
        "overall_ok": all(s["exit_code"] == 0 for s in steps),
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=== Parallel validation suite ===")
    for step in steps:
        print(f"  {step['script']}: {'PASS' if step['exit_code'] == 0 else 'FAIL'}")
    print(f"  mechanistic median (operational): {pred.get('mechanistic_median_error_pct', {}).get('operational')}%")
    print(f"  mpmath≡float64: {report['mpmath_equivalence_ok']}")
    print(f"Wrote {OUT}")
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())