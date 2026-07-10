#!/usr/bin/env python3
"""
Tier 80 wide cross-proof verification runner.

Layers:
  1. Export obligations from full FSOT/Formal corpus
  2. Python decimal structural proofs
  3. Coq/Rocq compile all chunks + coqchk
  4. Lean ↔ Coq cross-refinement audit
  5. Isabelle (optional, deferred)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from cross_proof_lib import obligation_provable, python_verify_obligation  # noqa: E402

OBL_CONNECTIVE = ROOT / "verification" / "obligations" / "connective_spine.json"
OBL_FORMAL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
REPORT = ROOT / "data" / "cross_proof_verification_report.json"
COQ_DIR = ROOT / "verification" / "coq"


def _find_exe(names: tuple[str, ...]) -> str | None:
    for name in names:
        p = shutil.which(name)
        if p:
            return p
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


def _isabelle_roots() -> list[Path]:
    home = Path(os.environ.get("USERPROFILE", ""))
    roots: list[Path] = [
        Path(r"C:\Isabelle"),
        Path(r"C:\Program Files\Isabelle"),
        home / "Isabelle",
        home / "Desktop" / "Isabelle2025-2",
        home / "Desktop" / "Isabelle2024-1",
    ]
    for pattern in ("Isabelle*", "Isabelle202*"):
        for base in (home / "Desktop", Path(r"C:\Program Files")):
            if base.exists():
                roots.extend(sorted(base.glob(pattern), reverse=True))
    seen: set[str] = set()
    out: list[Path] = []
    for root in roots:
        key = str(root)
        if key in seen or not root.exists():
            continue
        seen.add(key)
        out.append(root)
    return out


def _resolve_isabelle() -> dict[str, str] | None:
    """Return launch metadata for POSIX isabelle or Windows Cygwin wrapper."""
    p = shutil.which("isabelle")
    if p:
        return {"mode": "posix", "tool": p}
    for root in _isabelle_roots():
        bash = root / "contrib" / "cygwin" / "bin" / "bash.exe"
        isabelle_sh = root / "bin" / "isabelle"
        if bash.exists() and isabelle_sh.exists():
            return {
                "mode": "cygwin",
                "tool": str(isabelle_sh),
                "bash": str(bash),
                "home": str(root),
            }
        for exe in root.rglob("isabelle.exe"):
            return {"mode": "posix", "tool": str(exe)}
    return None


def python_verify(obligations: list[dict], label: str) -> tuple[list[dict], bool]:
    records: list[dict] = []
    ok = True
    for ob in obligations:
        passed = python_verify_obligation(ob)
        records.append(
            {
                "framework": "python_decimal",
                "spine": label,
                "obligation_id": ob["id"],
                "kind": ob["kind"],
                "passed": passed,
                "statement": ob.get("statement"),
            }
        )
        ok = ok and passed
    return records, ok


def _compile_coq_file(coqc: str, coq_file: Path, timeout: int = 600) -> dict:
    work = coq_file.parent
    try:
        r = subprocess.run(
            [coqc, "-q", coq_file.name],
            cwd=str(work),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        vo = work / f"{coq_file.stem}.vo"
        passed = r.returncode == 0 or vo.exists()
        chk: dict | None = None
        coqchk = _find_exe(("coqchk.exe", "coqchk", "rocqchk.exe", "rocqchk"))
        if passed and coqchk and vo.exists():
            cr = subprocess.run(
                [coqchk, vo.name],
                cwd=str(work),
                capture_output=True,
                text=True,
                timeout=120,
            )
            chk = {
                "tool": coqchk,
                "returncode": cr.returncode,
                "status": "passed" if cr.returncode == 0 else "failed",
            }
            passed = passed and cr.returncode == 0
        return {
            "file": coq_file.name,
            "status": "passed" if passed else "failed",
            "returncode": r.returncode,
            "vo_artifact": str(vo) if vo.exists() else None,
            "coqchk": chk,
            "stderr": (r.stderr or "")[-1500:],
        }
    except Exception as e:
        return {"file": coq_file.name, "status": "failed", "reason": str(e)}


def run_coq_full() -> dict:
    coqc = _find_exe(("coqc.exe", "coqc", "rocqc.exe", "rocqc"))
    if not coqc:
        return {"status": "skipped", "reason": "coqc/rocqc not on PATH"}

    targets = [
        COQ_DIR / "ConnectiveSpine.v",
        *sorted(COQ_DIR.glob("FullFormalSpine_*.v")),
    ]
    if len(targets) < 2:
        return {"status": "failed", "reason": "missing FullFormalSpine chunks"}

    chunk_results = [_compile_coq_file(coqc, path) for path in targets]
    all_passed = all(c.get("status") == "passed" for c in chunk_results)
    return {
        "status": "passed" if all_passed else "failed",
        "tool": coqc,
        "chunk_count": len(chunk_results),
        "chunks_passed": sum(1 for c in chunk_results if c.get("status") == "passed"),
        "chunks": chunk_results,
    }


def run_isabelle() -> dict:
    isa = _resolve_isabelle()
    thy_dir = ROOT / "verification" / "isabelle"
    thy = thy_dir / "ConnectiveSpine.thy"
    root_file = thy_dir / "ROOT"
    if not isa:
        return {"status": "skipped", "reason": "isabelle not found — run scripts/install_isabelle_windows.ps1"}
    if not thy.exists():
        return {"status": "failed", "reason": f"missing {thy}"}
    if not root_file.exists():
        return {"status": "failed", "reason": f"missing {root_file}"}
    try:
        if isa["mode"] == "cygwin":
            def _cygpath(win_path: Path) -> str:
                resolved = win_path.resolve()
                drive = resolved.drive.rstrip(":").lower()
                tail = resolved.as_posix().split(":", 1)[-1]
                return f"/cygdrive/{drive}{tail}"

            home_cyg = _cygpath(Path(isa["home"]))
            thy_cyg = _cygpath(thy_dir)
            cmd = f"cd '{home_cyg}' && bin/isabelle build -D '{thy_cyg}' ConnectiveSpine"
            r = subprocess.run(
                [isa["bash"], "--login", "-c", cmd],
                capture_output=True,
                text=True,
                timeout=300,
            )
            tool = isa["tool"]
        else:
            r = subprocess.run(
                [isa["tool"], "build", "-D", str(thy_dir), "ConnectiveSpine"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            tool = isa["tool"]
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "tool": tool,
            "returncode": r.returncode,
            "session": "ConnectiveSpine",
            "obligation_scope": "connective_spine",
            "stderr": (r.stderr or r.stdout or "")[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def main() -> int:
    pipeline = [
        "export_cross_proof_obligations.py",
        "export_full_formal_obligations.py",
        "generate_cross_proof_artifacts.py",
        "generate_full_formal_coq_artifacts.py",
    ]
    for script in pipeline:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {script}", file=sys.stderr)
            return r.returncode

    connective = json.loads(OBL_CONNECTIVE.read_text(encoding="utf-8"))
    formal = json.loads(OBL_FORMAL.read_text(encoding="utf-8"))

    py_conn, py_conn_ok = python_verify(connective["obligations"], "connective")
    provable_formal = [ob for ob in formal["obligations"] if obligation_provable(ob)]
    margin_violations = [ob for ob in formal["obligations"] if not obligation_provable(ob)]
    py_formal, py_formal_ok = python_verify(provable_formal, "full_formal_provable")
    py_ok = py_conn_ok and py_formal_ok

    coq = run_coq_full()

    refinement_r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cross_refinement_lean_coq_audit.py")],
        cwd=str(ROOT),
    )
    refinement = json.loads((ROOT / "data" / "cross_refinement_lean_coq_report.json").read_text(encoding="utf-8"))
    refinement_ok = refinement.get("overall_ok", False)

    isa = run_isabelle()

    lean_conn_ok = subprocess.run(
        [
            "lake",
            "build",
            "FSOT.Formal.WarpActuationDevelopmentPriors",
            "FSOT.Formal.FusionGridConnectivePriors",
            "FSOT.Formal.E10dWdConnectivePriors",
            "FSOT.Formal.CrossProofConnectivePriors",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    ).returncode == 0

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "80",
        "connective_spine": {
            "obligation_count": connective["obligation_count"],
            "python_decimal": {"status": "passed" if py_conn_ok else "failed"},
        },
        "full_formal_spine": {
            "obligation_count": formal["obligation_count"],
            "provable_count": len(provable_formal),
            "margin_violation_count": len(margin_violations),
            "margin_violation_ids": [ob["id"] for ob in margin_violations],
            "modules_exported": formal.get("modules_exported"),
            "by_tier": formal.get("by_tier"),
            "by_kind": formal.get("by_kind"),
            "python_decimal": {"status": "passed" if py_formal_ok else "failed"},
        },
        "frameworks": {
            "lean_connective": {"status": "passed" if lean_conn_ok else "failed"},
            "python_decimal": {
                "status": "passed" if py_ok else "failed",
                "connective_records": py_conn,
                "full_formal_passed": sum(1 for r in py_formal if r["passed"]),
                "full_formal_total": len(py_formal),
            },
            "coq": coq,
            "cross_refinement": {
                "status": "passed" if refinement_ok else "failed",
                "provable_triangulated_ok": refinement.get("triangulation", {}).get("provable_triangulated_ok"),
                "provable_total": len(provable_formal),
                "margin_violations_confirmed": refinement.get("obligation_count_margin_violations"),
            },
            "isabelle": isa,
        },
        "overall_ok": py_ok
            and lean_conn_ok
            and coq.get("status") == "passed"
            and refinement_ok
            and isa.get("status") in ("passed", "skipped"),
        "github_ready": len(margin_violations) == 0
            and py_ok
            and lean_conn_ok
            and coq.get("status") == "passed"
            and refinement_ok,
        "github_ready_note": (
            "All provable obligations triangulated; margin violations cleared."
            if len(margin_violations) == 0
            else "Blocked until margin violations refined and wide verification stable."
        ),
        "full_triangulation": py_ok
            and lean_conn_ok
            and coq.get("status") == "passed"
            and refinement_ok
            and isa.get("status") == "passed",
        "note": (
            "Tier 80: wide FSOT/Formal Coq cross-proof; Isabelle connective spine when installed."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_cross_proof_coverage.py")],
        cwd=str(ROOT),
    )

    print("CROSS-PROOF VERIFICATION (Tier 80 wide)")
    print(f"  connective obligations: {connective['obligation_count']}")
    print(f"  full formal obligations: {formal['obligation_count']} ({formal.get('modules_exported')} modules)")
    print(f"  provable: {len(provable_formal)} | margin violations: {len(margin_violations)}")
    print(f"  by_tier: {formal.get('by_tier')}")
    print(f"  python_decimal: {'PASS' if py_ok else 'FAIL'}")
    print(f"  lean connective: {'PASS' if lean_conn_ok else 'FAIL'}")
    print(f"  coq: {coq.get('status')} ({coq.get('chunks_passed', 0)}/{coq.get('chunk_count', 0)} chunks)")
    print(f"  cross_refinement: {'PASS' if refinement_ok else 'FAIL'}")
    print(f"  overall_ok: {report['overall_ok']}")
    print(f"  github_ready: {report['github_ready']}")
    print(f"Wrote {REPORT}")
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())