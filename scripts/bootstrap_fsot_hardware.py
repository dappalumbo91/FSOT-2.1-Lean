#!/usr/bin/env python3
"""Bootstrap FSOT scientific hardware stack: CUDA + audio + report active Python."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    print(f"Active Python: {sys.executable}")
    print("Note: FSOT uses whichever `python` is first on PATH.")
    print("      Hermes agent venv is incidental — not part of FSOT architecture.")
    print("      Set FSOT_PYTHON to pin a specific interpreter if desired.\n")

    checks = [
        [sys.executable, str(ROOT / "scripts" / "verify_fsot_cuda.py")],
        [sys.executable, str(ROOT / "scripts" / "verify_fsot_audio.py")],
    ]
    results: dict[str, int] = {}
    for cmd in checks:
        name = Path(cmd[1]).stem
        proc = subprocess.run(cmd, capture_output=True, text=True)
        results[name] = proc.returncode
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr[-500:])
        print(f"{name}: {'PASS' if proc.returncode == 0 else 'FAIL'} ({proc.returncode})\n")

    ok = all(code == 0 for code in results.values())
    report = {
        "python": sys.executable,
        "checks": results,
        "overall_ok": ok,
    }
    out = ROOT / "data" / "fsot_hardware_bootstrap_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())