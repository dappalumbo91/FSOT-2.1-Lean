#!/usr/bin/env python3
"""Verify Matter + Quantum/Trinary multiprover spine (Python/Rust/Z3/Coq)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import python_verify_obligation  # noqa: E402
from tool_path_lib import find_z3  # noqa: E402

GEN = ROOT / "scripts" / "export_and_generate_matter_quantum_trinary_artifacts.py"
OBL = ROOT / "verification" / "obligations" / "matter_quantum_trinary_spine.json"
SMT2 = ROOT / "verification" / "smt" / "matter_quantum_trinary_bounds.smt2"
RUST = ROOT / "verification" / "rust" / "fsot_matter_quantum_trinary_replay"
COQ_V = ROOT / "verification" / "coq" / "MatterQuantumTrinarySpine.v"
REPORT = ROOT / "data" / "matter_quantum_trinary_verification_report.json"


def main() -> int:
    print("=== Matter + Quantum/Trinary multiprover ===")
    r = subprocess.run([sys.executable, str(GEN)], cwd=str(ROOT))
    if r.returncode != 0:
        return r.returncode

    # Refresh margin so catalog export can see the panels
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_all_benchmark_margins.py")],
        cwd=str(ROOT),
        check=False,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "export_scientific_catalog_obligations.py")],
        cwd=str(ROOT),
        check=False,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_scientific_catalog_artifacts.py")],
        cwd=str(ROOT),
        check=False,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "export_full_priors_obligations.py")],
        cwd=str(ROOT),
        check=False,
    )

    obl = json.loads(OBL.read_text(encoding="utf-8"))
    obs = obl.get("obligations") or []
    py_pass = sum(1 for o in obs if python_verify_obligation(o))
    py_ok = py_pass == len(obs)
    print(f"Python: {py_pass}/{len(obs)}")

    rust_status = "skipped"
    if (RUST / "Cargo.toml").exists() and shutil.which("cargo"):
        rr = subprocess.run(
            ["cargo", "test", "--manifest-path", str(RUST / "Cargo.toml"), "--", "--nocapture"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        rust_status = "passed" if rr.returncode == 0 else "failed"
        print(f"Rust: {rust_status}")

    smt_status = "skipped"
    z3 = find_z3()
    if z3 and SMT2.exists():
        sr = subprocess.run([z3, str(SMT2)], capture_output=True, text=True)
        last = (sr.stdout or sr.stderr or "").strip().splitlines()
        smt_status = "passed" if last and last[-1].strip() == "sat" else "failed"
        print(f"Z3: {smt_status}")

    coq_status = "skipped"
    if shutil.which("coqc") and COQ_V.exists():
        cr = subprocess.run(
            [shutil.which("coqc"), "-Q", str(COQ_V.parent), "", str(COQ_V)],
            capture_output=True,
            text=True,
            timeout=600,
        )
        coq_status = "passed" if cr.returncode == 0 else "failed"
        print(f"Coq: {coq_status}")

    overall = py_ok and rust_status in ("passed", "skipped") and smt_status in ("passed", "skipped")
    if rust_status == "failed" or smt_status == "failed" or coq_status == "failed":
        overall = False

    cat = ROOT / "verification" / "obligations" / "scientific_catalog_spine.json"
    cat_n = None
    if cat.exists():
        cat_n = json.loads(cat.read_text(encoding="utf-8")).get("obligation_count")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "spine": "matter_quantum_trinary",
        "obligation_count": len(obs),
        "python_decimal": {"passed": py_pass, "total": len(obs), "status": "passed" if py_ok else "failed"},
        "rust_f64_replay": {"status": rust_status},
        "smt_z3": {"status": smt_status},
        "coq": {"status": coq_status},
        "scientific_catalog_obligation_count": cat_n,
        "lean_modules": [
            "FSOT/Formal/MatterAntimatterPriors.lean",
            "FSOT/Formal/QuantumTrinarySyntaxPriors.lean",
        ],
        "overall_ok": overall,
        "github_ready": overall and py_ok,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"overall_ok={overall} catalog_obs={cat_n}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
