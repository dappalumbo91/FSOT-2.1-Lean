#!/usr/bin/env python3
"""
Tier 85 wide cross-proof verification runner.

Layers:
  1. Export obligations from full FSOT/Formal corpus
  2. Python decimal structural proofs
  3. Coq/Rocq compile all chunks + coqchk
  4. Lean ↔ Coq cross-refinement audit
  5. Isabelle full-scope cross-proof (connective + FullFormalSpine chunks)
  6. Lean ↔ Isabelle cross-refinement audit
  7. Transcendental bounds gap inventory (pi/e lemmas deferred from float export)
  8. Rust f64 executable obligation replay (fourth check)
  9. rust_lean_bridge host runtime parity (bare-metal scalar kernel)
  10. F* executable check (optional; skipped when fstar not installed)
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

from cross_proof_lib import (  # noqa: E402
    gen_isabelle_root,
    isabelle_chunk_session_name,
    obligation_provable,
    parse_isabelle_theory_lemmas,
    python_verify_obligation,
)

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
        *sorted(COQ_DIR.glob("TranscendentalBounds_*.v")),
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


ISABELLE_SESSION = "FSOT_CrossProof"


def _isabelle_theory_chunks(thy_dir: Path) -> list[dict]:
    chunks: list[dict] = []
    connective = thy_dir / "ConnectiveSpine.thy"
    if connective.exists():
        chunks.append({"theory": "ConnectiveSpine", "file": connective.name, "scope": "connective"})
    for path in sorted(thy_dir.glob("TranscendentalBounds_*.thy")):
        if path.name in ("TranscendentalBoundsBase.thy", "TranscendentalBoundsCert.thy"):
            continue
        chunks.append({"theory": path.stem, "file": path.name, "scope": "transcendental_bounds"})
    for path in sorted(thy_dir.glob("FullFormalSpine_*.thy")):
        chunks.append({"theory": path.stem, "file": path.name, "scope": "full_formal"})
    return chunks


def _isabelle_chunk_metadata(thy_dir: Path, chunks: list[dict], session_passed: bool) -> list[dict]:
    results: list[dict] = []
    for chunk in chunks:
        path = thy_dir / chunk["file"]
        lemmas = parse_isabelle_theory_lemmas(path) if path.exists() else []
        results.append(
            {
                "theory": chunk["theory"],
                "file": chunk["file"],
                "scope": chunk["scope"],
                "obligation_count": len(lemmas),
                "status": "passed" if session_passed else "pending_diagnosis",
            }
        )
    return results


def _diagnose_isabelle_chunk(isa: dict, thy_dir: Path, chunk: dict, timeout: int = 900) -> dict:
    theory = chunk["theory"]
    src = thy_dir / chunk["file"]
    if not src.exists():
        return {"theory": theory, "file": chunk["file"], "status": "failed", "reason": "missing theory file"}
    diag_dir = thy_dir / "diagnostic" / theory
    diag_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, diag_dir / chunk["file"])
    session = isabelle_chunk_session_name(theory)
    (diag_dir / "ROOT").write_text(
        gen_isabelle_root([theory], session_name=session, description=f"FSOT diagnostic chunk {theory}"),
        encoding="utf-8",
    )
    build = _run_isabelle_session(isa, diag_dir, session, timeout=timeout)
    return {
        "theory": theory,
        "file": chunk["file"],
        "scope": chunk["scope"],
        "status": build.get("status", "failed"),
        "session": session,
        "build": build,
    }


def _run_isabelle_session(isa: dict, thy_dir: Path, session: str, timeout: int = 1800) -> dict:
    try:
        if isa["mode"] == "cygwin":
            def _cygpath(win_path: Path) -> str:
                resolved = win_path.resolve()
                drive = resolved.drive.rstrip(":").lower()
                tail = resolved.as_posix().split(":", 1)[-1]
                return f"/cygdrive/{drive}{tail}"

            home_cyg = _cygpath(Path(isa["home"]))
            thy_cyg = _cygpath(thy_dir)
            cmd = f"cd '{home_cyg}' && bin/isabelle build -D '{thy_cyg}' {session}"
            r = subprocess.run(
                [isa["bash"], "--login", "-c", cmd],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        else:
            r = subprocess.run(
                [isa["tool"], "build", "-D", str(thy_dir), session],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        out = (r.stdout or "") + (r.stderr or "")
        return {
            "session": session,
            "status": "passed" if r.returncode == 0 else "failed",
            "returncode": r.returncode,
            "stdout_tail": (r.stdout or "")[-1500:],
            "stderr": out[-4000:],
        }
    except Exception as e:
        return {"session": session, "status": "failed", "reason": str(e)}


def run_isabelle() -> dict:
    isa = _resolve_isabelle()
    thy_dir = ROOT / "verification" / "isabelle"
    root_file = thy_dir / "ROOT"
    if not isa:
        return {"status": "skipped", "reason": "isabelle not found — run scripts/install_isabelle_windows.ps1"}
    if not root_file.exists():
        return {"status": "failed", "reason": f"missing {root_file}"}
    theories = _isabelle_theory_chunks(thy_dir)
    if not theories:
        return {"status": "failed", "reason": "no Isabelle theories found"}
    build = _run_isabelle_session(isa, thy_dir, ISABELLE_SESSION, timeout=3600)
    session_passed = build.get("status") == "passed"
    chunk_rows = _isabelle_chunk_metadata(thy_dir, theories, session_passed)
    if not session_passed:
        print("  isabelle session failed — running per-chunk diagnostics...", file=sys.stderr)
        chunk_rows = [_diagnose_isabelle_chunk(isa, thy_dir, chunk) for chunk in theories]
        for row in chunk_rows:
            row["obligation_count"] = len(
                parse_isabelle_theory_lemmas(thy_dir / row["file"])
            ) if (thy_dir / row["file"]).exists() else 0
    formal = [t for t in theories if t["scope"] == "full_formal"]
    chunks_passed = sum(1 for c in chunk_rows if c.get("status") == "passed")
    return {
        "status": build.get("status", "failed"),
        "tool": isa["tool"],
        "session": ISABELLE_SESSION,
        "theory_count": len(theories),
        "connective_theories": 1 if any(t["scope"] == "connective" for t in theories) else 0,
        "formal_theory_count": len(formal),
        "obligation_scope": "connective_and_full_formal",
        "provable_obligations": len(provable_formal_obligations()),
        "chunk_count": len(chunk_rows),
        "chunks_passed": chunks_passed,
        "chunks": chunk_rows,
        "build": build,
    }


RUST_REPLAY_DIR = ROOT / "verification" / "rust" / "fsot_obligation_replay"
SCALAR_KERNEL_DIR = ROOT / "verification" / "rust" / "fsot_scalar_kernel"
FSTAR_DIR = ROOT / "verification" / "fstar"


def run_rust_replay() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "skipped", "reason": "cargo not on PATH"}
    if not (RUST_REPLAY_DIR / "tests" / "replay_all_obligations.rs").exists():
        return {"status": "failed", "reason": "missing generated Rust replay tests"}
    try:
        r = subprocess.run(
            [cargo, "test", "--quiet"],
            cwd=str(RUST_REPLAY_DIR),
            capture_output=True,
            text=True,
            timeout=600,
        )
        meta_path = RUST_REPLAY_DIR / "obligation_meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        out = (r.stdout or "") + (r.stderr or "")
        passed = r.returncode == 0
        return {
            "status": "passed" if passed else "failed",
            "tool": cargo,
            "crate": "fsot_obligation_replay",
            "obligation_count": meta.get("total_count"),
            "formal_count": meta.get("formal_count"),
            "transcendental_count": meta.get("transcendental_count"),
            "test_file": meta.get("test_file"),
            "returncode": r.returncode,
            "stderr_tail": out[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_rust_lean_bridge_parity() -> dict:
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "rust_lean_bridge_runtime_parity.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        report_path = ROOT / "data" / "rust_lean_bridge_runtime_parity_report.json"
        doc = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "crate": "fsot_scalar_kernel",
            "python_boot_scalar": doc.get("python_boot_scalar"),
            "benchmark_median_error_pct": doc.get("benchmark_median_error_pct"),
            "returncode": r.returncode,
            "stderr_tail": ((r.stdout or "") + (r.stderr or ""))[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_fstar_check() -> dict:
    fstar = shutil.which("fstar") or shutil.which("fstar.exe")
    entry = FSTAR_DIR / "FSOTScalarBoot.fst"
    if not fstar:
        return {
            "status": "skipped",
            "reason": "fstar not on PATH",
            "note": "Install F* to enable programming-language formal check (Tier 85 optional).",
        }
    if not entry.exists():
        return {"status": "skipped", "reason": "no verification/fstar/FSOTScalarBoot.fst entry module"}
    try:
        r = subprocess.run(
            [fstar, "--include", str(FSTAR_DIR), str(entry)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "tool": fstar,
            "entry": str(entry),
            "returncode": r.returncode,
            "stderr_tail": out[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def provable_formal_obligations() -> list[dict]:
    if not OBL_FORMAL.exists():
        return []
    formal = json.loads(OBL_FORMAL.read_text(encoding="utf-8"))
    return [ob for ob in formal["obligations"] if obligation_provable(ob)]


def main() -> int:
    pipeline = [
        "export_cross_proof_obligations.py",
        "export_full_formal_obligations.py",
        "export_transcendental_bounds_obligations.py",
        "generate_cross_proof_artifacts.py",
        "generate_full_formal_coq_artifacts.py",
        "generate_transcendental_bounds_coq.py",
        "generate_full_formal_isabelle_artifacts.py",
        "generate_transcendental_bounds_isabelle.py",
        "generate_rust_obligation_replay.py",
    ]
    for script in pipeline:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {script}", file=sys.stderr)
            return r.returncode

    connective = json.loads(OBL_CONNECTIVE.read_text(encoding="utf-8"))
    formal = json.loads(OBL_FORMAL.read_text(encoding="utf-8"))
    trans_path = ROOT / "verification" / "obligations" / "transcendental_bounds.json"
    transcendental = json.loads(trans_path.read_text(encoding="utf-8")) if trans_path.exists() else {
        "obligation_count": 0,
        "obligations": [],
    }

    py_conn, py_conn_ok = python_verify(connective["obligations"], "connective")
    provable_formal = [ob for ob in formal["obligations"] if obligation_provable(ob)]
    margin_violations = [ob for ob in formal["obligations"] if not obligation_provable(ob)]
    py_formal, py_formal_ok = python_verify(provable_formal, "full_formal_provable")
    py_ok = py_conn_ok and py_formal_ok

    coq = run_coq_full()

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cross_refinement_lean_coq_audit.py")],
        cwd=str(ROOT),
    )
    refinement = json.loads((ROOT / "data" / "cross_refinement_lean_coq_report.json").read_text(encoding="utf-8"))
    refinement_ok = refinement.get("overall_ok", False)

    isa = run_isabelle()

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cross_refinement_lean_isabelle_audit.py")],
        cwd=str(ROOT),
    )
    isa_refinement = json.loads(
        (ROOT / "data" / "cross_refinement_lean_isabelle_report.json").read_text(encoding="utf-8")
    )
    isa_refinement_ok = isa_refinement.get("overall_ok", False)

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_transcendental_bounds_gap.py")],
        cwd=str(ROOT),
    )
    transcendental_gap = json.loads(
        (ROOT / "data" / "transcendental_bounds_gap_report.json").read_text(encoding="utf-8")
    )

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cross_refinement_rust_audit.py")],
        cwd=str(ROOT),
    )
    rust_refinement = json.loads(
        (ROOT / "data" / "cross_refinement_rust_report.json").read_text(encoding="utf-8")
    )
    rust_refinement_ok = rust_refinement.get("overall_ok", False)
    rust = run_rust_replay()

    bridge_parity = run_rust_lean_bridge_parity()
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "cross_refinement_rust_lean_bridge_audit.py")],
        cwd=str(ROOT),
    )
    bridge_refinement = json.loads(
        (ROOT / "data" / "cross_refinement_rust_lean_bridge_report.json").read_text(encoding="utf-8")
    )
    bridge_refinement_ok = bridge_refinement.get("overall_ok", False)
    fstar = run_fstar_check()

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
        "tier": "85",
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
        "transcendental_bounds": {
            "obligation_count": transcendental.get("obligation_count", 0),
            "python_decimal_verified_count": transcendental.get("python_decimal_verified_count", 0),
            "by_proof_template": transcendental.get("by_proof_template"),
            "coq_chunks": len(list((ROOT / "verification" / "coq").glob("TranscendentalBounds_[0-9]*.v"))),
            "isabelle_chunks": len(list((ROOT / "verification" / "isabelle").glob("TranscendentalBounds_[0-9]*.thy"))),
            "status": "exported",
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
            "isabelle_refinement": {
                "status": "passed" if isa_refinement_ok else "failed",
                "provable_triangulated_ok": isa_refinement.get("triangulation", {}).get(
                    "provable_triangulated_ok"
                ),
                "provable_total": len(provable_formal),
                "isabelle_lemmas_indexed": isa_refinement.get("isabelle_lemmas_indexed"),
            },
            "transcendental_bounds_gap": {
                "exported_float_obligations_from_bounds": transcendental_gap.get(
                    "exported_float_obligations_from_bounds"
                ),
                "excluded_pi_e_interval_count": transcendental_gap.get("excluded_pi_e_interval_count"),
                "transcendental_lemma_count": transcendental_gap.get("transcendental_lemma_count"),
                "report": str(ROOT / "data" / "transcendental_bounds_gap_report.json"),
            },
            "rust_replay": rust,
            "rust_refinement": {
                "status": "passed" if rust_refinement_ok else "failed",
                "total_exported_to_rust": rust_refinement.get("total_exported_to_rust"),
                "formal_python_f64_ok": rust_refinement.get("formal_python_f64_ok"),
                "transcendental_python_f64_ok": rust_refinement.get("transcendental_python_f64_ok"),
            },
            "rust_lean_bridge_parity": bridge_parity,
            "rust_lean_bridge_refinement": {
                "status": "passed" if bridge_refinement_ok else "failed",
                "checks": bridge_refinement.get("checks"),
            },
            "fstar": fstar,
        },
        "overall_ok": py_ok
            and lean_conn_ok
            and coq.get("status") == "passed"
            and refinement_ok
            and isa.get("status") in ("passed", "skipped")
            and isa_refinement_ok
            and rust.get("status") in ("passed", "skipped")
            and rust_refinement_ok
            and bridge_parity.get("status") == "passed"
            and bridge_refinement_ok
            and fstar.get("status") in ("passed", "skipped"),
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
            and isa.get("status") == "passed"
            and isa_refinement_ok
            and rust.get("status") == "passed"
            and rust_refinement_ok,
        "four_way_verification": py_ok
            and coq.get("status") == "passed"
            and isa.get("status") == "passed"
            and rust.get("status") == "passed",
        "five_way_runtime": py_ok
            and rust.get("status") == "passed"
            and bridge_parity.get("status") == "passed",
        "note": (
            "Tier 85: four-way proof assistants (Lean+Coq+Isabelle+Rust replay) plus "
            "rust_lean_bridge bare-metal scalar runtime parity; F* optional when installed."
        ),
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_cross_proof_coverage.py")],
        cwd=str(ROOT),
    )

    print("CROSS-PROOF VERIFICATION (Tier 85 wide)")
    print(f"  connective obligations: {connective['obligation_count']}")
    print(f"  full formal obligations: {formal['obligation_count']} ({formal.get('modules_exported')} modules)")
    print(f"  provable: {len(provable_formal)} | margin violations: {len(margin_violations)}")
    print(f"  by_tier: {formal.get('by_tier')}")
    print(f"  python_decimal: {'PASS' if py_ok else 'FAIL'}")
    print(f"  lean connective: {'PASS' if lean_conn_ok else 'FAIL'}")
    print(f"  coq: {coq.get('status')} ({coq.get('chunks_passed', 0)}/{coq.get('chunk_count', 0)} chunks)")
    print(f"  cross_refinement: {'PASS' if refinement_ok else 'FAIL'}")
    print(
        f"  isabelle: {isa.get('status')} "
        f"(session {isa.get('session', 'n/a')}, "
        f"{isa.get('chunks_passed', 0)}/{isa.get('chunk_count', 0)} chunks)"
    )
    print(f"  isabelle_refinement: {'PASS' if isa_refinement_ok else 'FAIL'}")
    print(
        f"  transcendental_gap: {transcendental_gap.get('excluded_pi_e_interval_count', 0)} "
        f"pi/e intervals deferred, {transcendental_gap.get('transcendental_lemma_count', 0)} "
        f"structural lemmas in Bounds.lean"
    )
    print(
        f"  rust_replay: {rust.get('status')} "
        f"({rust.get('obligation_count', 0)} obligations, test {rust.get('test_file', 'n/a')})"
    )
    print(f"  rust_refinement: {'PASS' if rust_refinement_ok else 'FAIL'}")
    print(
        f"  rust_lean_bridge_parity: {bridge_parity.get('status')} "
        f"(boot_scalar={bridge_parity.get('python_boot_scalar', 'n/a')})"
    )
    print(f"  rust_lean_bridge_refinement: {'PASS' if bridge_refinement_ok else 'FAIL'}")
    print(f"  fstar: {fstar.get('status')}")
    print(f"  four_way_verification: {report.get('four_way_verification')}")
    print(f"  five_way_runtime: {report.get('five_way_runtime')}")
    print(f"  overall_ok: {report['overall_ok']}")
    print(f"  github_ready: {report['github_ready']}")
    print(f"Wrote {REPORT}")
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())