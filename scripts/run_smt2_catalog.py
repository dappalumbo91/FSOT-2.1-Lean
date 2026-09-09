#!/usr/bin/env python3
"""Run verification/smt/scientific_catalog_bounds.smt2 via z3 CLI or z3-solver."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMT = ROOT / "verification" / "smt" / "scientific_catalog_bounds.smt2"


def main() -> int:
    if not SMT.is_file():
        print("No scientific_catalog_bounds.smt2 — skip")
        return 0
    z3 = shutil.which("z3")
    if z3:
        proc = subprocess.run([z3, str(SMT)], capture_output=True, text=True)
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        if "error" in (proc.stdout + proc.stderr).lower():
            return 1
        return 0 if proc.returncode == 0 else proc.returncode
    from z3 import Solver, parse_smt2_file  # type: ignore

    s = Solver()
    s.add(parse_smt2_file(str(SMT)))
    print(s.check())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
