#!/usr/bin/env python3
"""Focused multi-prover verification of the uniqueness research spine.

Mirrors run_gr_sm_ckm_verification.py:
  regenerate artifacts → Python decimal → Rust f64 → Z3 SMT → optional Coq
  → data/uniqueness_research_verification_report.json
"""

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

OBL = ROOT / "verification" / "obligations" / "uniqueness_research_spine.json"
SMT2 = ROOT / "verification" / "smt" / "uniqueness_research_bounds.smt2"
RUST = ROOT / "verification" / "rust" / "fsot_uniqueness_research_replay"
COQ_V = ROOT / "verification" / "coq" / "UniquenessResearchSpine.v"
REPORT = ROOT / "data" / "uniqueness_research_verification_report.json"
GEN = ROOT / "scripts" / "export_and_generate_uniqueness_research_artifacts.py"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    print("=== Uniqueness research multi-prover verification ===")
    r = subprocess.run([sys.executable, str(GEN)], cwd=str(ROOT))
    if r.returncode != 0:
        print("FAILED: artifact generation", file=sys.stderr)
        return r.returncode

    obl = json.loads(OBL.read_text(encoding="utf-8"))
    obs = obl.get("obligations") or []
    py_pass = sum(1 for o in obs if python_verify_obligation(o))
    py_ok = py_pass == len(obs)
    print(f"Python decimal: {py_pass}/{len(obs)}  ok={py_ok}")

    rust_status = "skipped"
    rust_detail = ""
    if (RUST / "Cargo.toml").exists() and shutil.which("cargo"):
        rr = None
        for _attempt in range(2):
            rr = subprocess.run(
                ["cargo", "test", "--manifest-path", str(RUST / "Cargo.toml"), "--", "--nocapture"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            if rr.returncode == 0:
                break
        rust_status = "passed" if rr and rr.returncode == 0 else "failed"
        rust_detail = ((rr.stdout or "") if rr else "")[-1500:] + ((rr.stderr or "") if rr else "")[-500:]
        print(f"Rust cargo test: {rust_status}")
        if rust_status == "failed":
            print(rust_detail[-400:])
    else:
        print("Rust: skipped (no cargo)")

    smt_status = "skipped"
    smt_out = ""
    z3 = find_z3()
    if z3 and SMT2.exists():
        sr = subprocess.run([z3, str(SMT2)], capture_output=True, text=True)
        lines = (sr.stdout or sr.stderr or "").strip().splitlines()
        last = lines[-1].strip() if lines else ""
        smt_status = "passed" if last == "sat" else "failed"
        smt_out = "\n".join(lines)[-200:]
        print(f"Z3 SMT: {smt_status}  (last={last!r})")
    else:
        print("Z3: skipped")

    coq_status = "skipped"
    coqc = shutil.which("coqc")
    if coqc and COQ_V.exists():
        cr = subprocess.run(
            [coqc, "-Q", str(COQ_V.parent), "", str(COQ_V)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=600,
        )
        coq_status = "passed" if cr.returncode == 0 else "failed"
        print(f"Coq UniquenessResearchSpine: {coq_status}")
        if coq_status == "failed":
            print((cr.stderr or cr.stdout or "")[-400:])
    else:
        print("Coq: skipped (coqc not on PATH)")

    fstar_status = "skipped"
    fstar = shutil.which("fstar.exe") or shutil.which("fstar")
    fstar_file = ROOT / "verification" / "fstar" / "FSOTUniquenessResearch.fst"
    if fstar and fstar_file.exists():
        try:
            fr = subprocess.run(
                [fstar, str(fstar_file)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=300,
            )
            fstar_status = "passed" if fr.returncode == 0 else "failed"
            print(f"F*: {fstar_status}")
        except OSError as exc:
            fstar_status = "skipped"
            print(f"F*: skipped (cannot exec: {exc})")
    else:
        print("F*: skipped")

    overall = py_ok and rust_status in ("passed", "skipped") and smt_status in ("passed", "skipped")
    if rust_status == "failed" or smt_status == "failed" or coq_status == "failed" or fstar_status == "failed":
        overall = False
    if rust_status == "skipped" and smt_status == "skipped":
        overall = py_ok

    report = {
        "generated_at": _now(),
        "spine": "uniqueness_research",
        "obligation_count": len(obs),
        "ontology": obl.get("ontology"),
        "python_decimal": {
            "passed": py_pass,
            "total": len(obs),
            "status": "passed" if py_ok else "failed",
        },
        "rust_f64_replay": {"status": rust_status, "detail_tail": rust_detail[-800:]},
        "smt_z3": {"status": smt_status, "output": smt_out[:200], "path": str(SMT2)},
        "coq_uniqueness": {"status": coq_status, "file": str(COQ_V)},
        "fstar": {"status": fstar_status, "file": str(fstar_file)},
        "artifacts": {
            "obligations": str(OBL.relative_to(ROOT)).replace("\\", "/"),
            "lean": "FSOT/Formal/UniquenessResearchSpine.lean",
            "coq": "verification/coq/UniquenessResearchSpine.v",
            "isabelle": "verification/isabelle/UniquenessResearchSpine.thy",
            "fstar": "verification/fstar/FSOTUniquenessResearch.fst",
            "smt": "verification/smt/uniqueness_research_bounds.smt2",
            "tla": "verification/tla/FSOTUniquenessResearch.tla",
            "rust": "verification/rust/fsot_uniqueness_research_replay",
            "confinement_research": "data/uniqueness_confinement_research.json",
            "reality_fiction_calibration": "data/reality_fiction_calibration.json",
        },
        "source_summaries": obl.get("source_summaries"),
        "honest_scope": obl.get("honest_scope"),
        "overall_ok": overall,
        "github_ready": overall and py_ok,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT}")
    print(f"overall_ok={overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
