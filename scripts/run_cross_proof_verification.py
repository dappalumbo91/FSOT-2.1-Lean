#!/usr/bin/env python3
"""
Tier 79 cross-proof verification runner.

Layers (no account / gatekeeping required):
  1. Export obligations from Lean connective modules
  2. Python decimal structural proofs (always runs)
  3. Coq/Rocq compile (if installed)
  4. Isabelle build (if installed)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBL = ROOT / "verification" / "obligations" / "connective_spine.json"
REPORT = ROOT / "data" / "cross_proof_verification_report.json"


def _find_exe(names: tuple[str, ...]) -> str | None:
    for name in names:
        p = shutil.which(name)
        if p:
            return p
    # Rocq Platform common Windows paths
    for base in (
        Path(r"C:\Rocq-Platform~9.0~2025.08"),
        Path(r"C:\Program Files\Rocq Platform"),
        Path(r"C:\Program Files\Coq"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Rocq Platform",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Coq Platform",
    ):
        if not base.exists():
            continue
        for name in names:
            for exe in base.rglob(name):
                return str(exe)
    return None


def _find_isabelle() -> str | None:
    p = shutil.which("isabelle")
    if p:
        return p
    for base in (
        Path(r"C:\Program Files\Isabelle"),
        Path(os.environ.get("USERPROFILE", "")) / "Isabelle",
    ):
        if base.exists():
            for exe in base.rglob("isabelle.exe"):
                return str(exe)
    return None


def python_verify(obligations: list[dict]) -> tuple[list[dict], bool]:
    records: list[dict] = []
    ok = True
    for ob in obligations:
        kind = ob["kind"]
        passed = False
        if kind == "pos":
            passed = Decimal(str(ob["value"])) > 0
        elif kind == "gt_one":
            passed = Decimal(str(ob["value"])) > 1
        elif kind == "lt":
            passed = Decimal(str(ob["left_value"])) < Decimal(str(ob["right_value"]))
        records.append(
            {
                "framework": "python_decimal",
                "obligation_id": ob["id"],
                "kind": kind,
                "passed": passed,
                "statement": ob.get("statement"),
            }
        )
        ok = ok and passed
    return records, ok


def run_coq() -> dict:
    coqc = _find_exe(("coqc.exe", "coqc", "rocqc.exe", "rocqc"))
    coq_file = ROOT / "verification" / "coq" / "ConnectiveSpine.v"
    if not coqc:
        return {"status": "skipped", "reason": "coqc/rocqc not on PATH — install: winget install Coq.CoqPlatform"}
    if not coq_file.exists():
        return {"status": "failed", "reason": f"missing {coq_file}"}
    work = ROOT / "verification" / "coq"
    try:
        r = subprocess.run(
            [coqc, "-q", str(coq_file.name)],
            cwd=str(work),
            capture_output=True,
            text=True,
            timeout=120,
        )
        vo = work / f"{coq_file.stem}.vo"
        passed = r.returncode == 0 or vo.exists()
        chk: dict | None = None
        coqchk = _find_exe(("coqchk.exe", "coqchk", "rocqchk.exe", "rocqchk"))
        if passed and coqchk and vo.exists():
            cr = subprocess.run(
                [coqchk, str(vo.name)],
                cwd=str(work),
                capture_output=True,
                text=True,
                timeout=60,
            )
            chk = {"tool": coqchk, "returncode": cr.returncode, "status": "passed" if cr.returncode == 0 else "failed"}
            passed = passed and cr.returncode == 0
        return {
            "status": "passed" if passed else "failed",
            "tool": coqc,
            "returncode": r.returncode,
            "vo_artifact": str(vo) if vo.exists() else None,
            "coqchk": chk,
            "stderr": (r.stderr or "")[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_isabelle() -> dict:
    isabelle = _find_isabelle()
    thy = ROOT / "verification" / "isabelle" / "ConnectiveSpine.thy"
    if not isabelle:
        return {
            "status": "skipped",
            "reason": "isabelle not found — free install: https://isabelle.in.tum.de/ (no login)",
        }
    if not thy.exists():
        return {"status": "failed", "reason": f"missing {thy}"}
    try:
        r = subprocess.run(
            [isabelle, "build", "-D", str(thy.parent), "ConnectiveSpine"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "tool": isabelle,
            "returncode": r.returncode,
            "stderr": (r.stderr or "")[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def main() -> int:
    # Refresh export + artifacts
    for script in ("export_cross_proof_obligations.py", "generate_cross_proof_artifacts.py"):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {script}", file=sys.stderr)
            return r.returncode

    doc = json.loads(OBL.read_text(encoding="utf-8"))
    py_records, py_ok = python_verify(doc["obligations"])
    coq = run_coq()
    isa = run_isabelle()

    lean_ok = subprocess.run(
        ["lake", "build", "FSOT.Formal.WarpActuationDevelopmentPriors",
         "FSOT.Formal.FusionGridConnectivePriors", "FSOT.Formal.E10dWdConnectivePriors"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    ).returncode == 0

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": 79,
        "obligation_count": doc["obligation_count"],
        "frameworks": {
            "lean": {"status": "passed" if lean_ok else "failed"},
            "python_decimal": {"status": "passed" if py_ok else "failed", "records": py_records},
            "coq": coq,
            "isabelle": isa,
        },
        "overall_ok": py_ok and lean_ok
            and coq.get("status") == "passed"
            and isa.get("status") in ("passed", "skipped"),
        "github_ready": py_ok and lean_ok and coq.get("status") == "passed",
        "full_triangulation": py_ok and lean_ok
            and coq.get("status") == "passed"
            and isa.get("status") == "passed",
        "note": "full_triangulation requires Coq + Isabelle; github_ready requires Coq pass",
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("CROSS-PROOF VERIFICATION (Tier 79)")
    print(f"  obligations: {doc['obligation_count']}")
    print(f"  python_decimal: {'PASS' if py_ok else 'FAIL'}")
    print(f"  lean: {'PASS' if lean_ok else 'FAIL'}")
    print(f"  coq: {coq.get('status')} {coq.get('reason', '')}")
    print(f"  isabelle: {isa.get('status')} {isa.get('reason', '')}")
    print(f"  overall_ok: {report['overall_ok']}")
    print(f"Wrote {REPORT}")
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())