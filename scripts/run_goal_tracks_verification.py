#!/usr/bin/env python3
"""Rebuild goal-track artifacts and run the uniqueness multi-prover gauntlet.

Tracks: path-sum, process-time (D12), market class, sickness two-system.
Provers: Python decimal, Rust, Z3, Coq, Isabelle (file), F* when present,
plus lake build of ScalarEngineStructure + UniquenessAttractor.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "goal_tracks_verification_report.json"


def _run(args: list[str], timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(ROOT), timeout=timeout)


def main() -> int:
    steps: list[dict] = []
    overall = True

    def step(name: str, args: list[str], timeout: int = 600) -> None:
        nonlocal overall
        print(f"\n=== {name} ===")
        r = _run(args, timeout=timeout)
        ok = r.returncode == 0
        overall = overall and ok
        steps.append({"name": name, "ok": ok, "returncode": r.returncode})
        print(f"{name}: {'PASS' if ok else 'FAIL'} (exit {r.returncode})")

    step("path_sum", [sys.executable, str(ROOT / "vendor" / "fsot_path_sum.py")])
    step("market_process", [sys.executable, str(ROOT / "scripts" / "build_market_process_layer.py")])
    step("sickness_two_system", [sys.executable, str(ROOT / "scripts" / "smoke_sickness_two_system.py")])
    step("process_time_smoke", [sys.executable, str(ROOT / "scripts" / "smoke_dynamic_forecast_potentials.py")])
    step("weather_24h_retro", [sys.executable, str(ROOT / "scripts" / "retro_weather_24h.py")], timeout=300)
    step(
        "uniqueness_multiprover",
        [sys.executable, str(ROOT / "scripts" / "run_uniqueness_research_verification.py")],
        timeout=1200,
    )

    lake = subprocess.run(
        [
            "lake",
            "build",
            "FSOT.Formal.ScalarEngineStructure",
            "FSOT.Formal.UniquenessAttractor",
            "FSOT.Formal.UniquenessResearchSpine",
        ],
        cwd=str(ROOT),
        timeout=1200,
    )
    lake_ok = lake.returncode == 0
    overall = overall and lake_ok
    steps.append({"name": "lake_lean_mathlib", "ok": lake_ok, "returncode": lake.returncode})
    print(f"lake Lean/Mathlib: {'PASS' if lake_ok else 'FAIL'}")

    uniq = {}
    up = ROOT / "data" / "uniqueness_research_verification_report.json"
    if up.is_file():
        uniq = json.loads(up.read_text(encoding="utf-8"))
    pp = uniq.get("provers_passed") or {}

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_ok": overall,
        "steps": steps,
        "uniqueness_report": {
            "obligation_count": uniq.get("obligation_count"),
            "python": (uniq.get("python_decimal") or {}).get("status"),
            "rust": (uniq.get("rust_f64_replay") or {}).get("status"),
            "smt": (uniq.get("smt_z3") or {}).get("status"),
            "coq": (uniq.get("coq_uniqueness") or {}).get("status"),
            "isabelle": (uniq.get("isabelle_uniqueness") or {}).get("status"),
            "fstar": (uniq.get("fstar") or {}).get("status"),
            "provers_passed": pp,
            "overall_ok": uniq.get("overall_ok"),
        },
        "classical_ym_path_integral": "OPEN_NOT_CLAIMED",
    }
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {REPORT} overall_ok={overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
