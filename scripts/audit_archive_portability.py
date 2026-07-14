#!/usr/bin/env python3
"""Audit I: physical archive vs C: mirror vs GitHub for plug-and-play portability."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_paths import (  # noqa: E402
    archive_root,
    canonical_archive_mode,
    founding_archive_roots,
    fsot_compute_path,
)

OUT = ROOT / "data" / "archive_portability_audit.json"
DESKTOP_MIRROR = Path(
    r"C:\Users\damia\Desktop\FSOT-2.1-Lean\FSOT-2.1-Lean-main\FSOT-2.1-Lean-main"
)
GITHUB_REMOTE = "https://github.com/dappalumbo91/FSOT-2.1-Lean.git"
REQUIRED_PYTHON = ("numpy", "mpmath", "sympy", "yaml", "pypdf", "pytest")
HOST_TOOLS = ("python", "lake", "elan", "rustc", "cargo", "coqc", "isabelle")
ARCHIVE_SECTIONS = (
    "01_SR-ITE-USB-Original",
    "02_FSOT-2.1-Lean-Full",
    "03_FSOT-PublicData",
    "04_Genetics-Longevity",
    "05_Zebrahub-Development",
    "06_Founding-Archives",
)


def _dir_stats(path: Path, *, quick: bool = False) -> dict:
    if not path.is_dir():
        return {"exists": False, "file_count": 0, "size_bytes": 0}
    if quick:
        return {"exists": True, "file_count": None, "size_bytes": None, "quick": True}
    count = 0
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            count += 1
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return {"exists": True, "file_count": count, "size_bytes": total}


def _git_head(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else None


def _git_origin_head(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    subprocess.run(["git", "fetch", "origin"], cwd=path, capture_output=True, check=False)
    proc = subprocess.run(
        ["git", "rev-parse", "origin/main"],
        cwd=path,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout.strip() if proc.returncode == 0 else None


def _compare_trees(a: Path, b: Path, rel_dirs: tuple[str, ...]) -> list[dict]:
    rows: list[dict] = []
    for name in rel_dirs:
        ap = a / name
        bp = b / name
        sa = _dir_stats(ap)
        sb = _dir_stats(bp)
        rows.append(
            {
                "path": name,
                "a_exists": sa["exists"],
                "b_exists": sb["exists"],
                "a_files": sa["file_count"],
                "b_files": sb["file_count"],
                "a_bytes": sa["size_bytes"],
                "b_bytes": sb["size_bytes"],
                "delta_files": sa["file_count"] - sb["file_count"],
            }
        )
    return rows


def _check_python_packages() -> dict[str, bool]:
    out: dict[str, bool] = {}
    for pkg in REQUIRED_PYTHON:
        mod = "yaml" if pkg == "yaml" else pkg
        try:
            __import__(mod)
            out[pkg] = True
        except ImportError:
            out[pkg] = False
    return out


def _check_host_tools() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for tool in HOST_TOOLS:
        found = shutil.which(tool)
        out[tool] = found
    return out


def _run_sub_audit(script: str) -> dict:
    path = ROOT / "scripts" / script
    if not path.exists():
        return {"ran": False, "ok": False, "error": "missing script"}
    proc = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    payload: dict = {"ran": True, "ok": proc.returncode == 0, "exit_code": proc.returncode}
    for out_path in (
        ROOT / "data" / "archive_independence_audit.json",
        ROOT / "data" / "portable_vendor_coverage_audit.json",
    ):
        if out_path.exists():
            try:
                payload[out_path.name] = json.loads(out_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    if proc.stderr.strip():
        payload["stderr_tail"] = proc.stderr.strip()[-500:]
    return payload


def audit(*, skip_fetch: bool = False, quick: bool = False) -> dict:
    ar = archive_root()
    founding = founding_archive_roots()
    py_pkgs = _check_python_packages()
    tools = _check_host_tools()

    i_head = _git_head(ROOT)
    origin_head = None if skip_fetch else _git_origin_head(ROOT)
    c_head = _git_head(DESKTOP_MIRROR) if DESKTOP_MIRROR.exists() else None

    section_stats: list[dict] = []
    if ar is not None:
        for sec in ARCHIVE_SECTIONS:
            st = _dir_stats(ar / sec, quick=quick)
            section_stats.append({"section": sec, **st})

    mirror_compare = []
    if DESKTOP_MIRROR.exists():
        if not quick:
            mirror_compare = _compare_trees(ROOT, DESKTOP_MIRROR, (".lake", "vendor", "data", "scripts", "FSOT"))

    vendor_audit = _run_sub_audit("audit_portable_vendor_coverage.py")
    indep_audit = _run_sub_audit("audit_archive_independence.py")
    vendor_cov = (vendor_audit.get("portable_vendor_coverage_audit.json") or {})
    indep_cov = (indep_audit.get("archive_independence_audit.json") or {})

    blockers: list[str] = []
    warnings: list[str] = []

    if not canonical_archive_mode():
        blockers.append("Not running from canonical archive hub (.fsot-canonical-hub missing)")
    if not all(py_pkgs.values()):
        missing = [k for k, v in py_pkgs.items() if not v]
        blockers.append(f"Host Python packages missing (not bundled on drive): {', '.join(missing)}")
    if tools.get("python") is None:
        blockers.append("Python interpreter not on PATH (not bundled on drive)")
    if not tools.get("lake"):
        warnings.append("Lean lake not on PATH — use --skip-lean for portable verify")
    if not tools.get("coqc"):
        warnings.append("Coq not on PATH — cross-proof Coq tier skipped on fresh laptop")
    if not tools.get("isabelle"):
        warnings.append("Isabelle not on PATH — cross-proof Isabelle tier skipped on fresh laptop")

    if vendor_cov.get("missing_bundled_assets"):
        blockers.append(f"Missing bundled vendor assets: {vendor_cov['missing_bundled_assets']}")
    if vendor_cov.get("missing_benchmark_domains"):
        blockers.append(f"Missing benchmark domains: {vendor_cov['missing_benchmark_domains']}")

    if ar is None:
        blockers.append("archive_root() unresolved — set FSOT_ARCHIVE_ROOT")
    else:
        for sec in ("03_FSOT-PublicData", "06_Founding-Archives"):
            if not (ar / sec).is_dir():
                blockers.append(f"Archive section missing: {sec}")
        if not founding:
            blockers.append("No founding archive roots found")

    if i_head and origin_head and i_head != origin_head:
        warnings.append(f"I: git HEAD {i_head[:8]} differs from origin/main {origin_head[:8]}")
    if c_head and i_head and c_head != i_head:
        warnings.append(f"C: Desktop mirror at {c_head[:8]} — do not verify from C:")

    plug_and_play_data = (
        vendor_cov.get("all_extension_benchmarks_present")
        and vendor_cov.get("all_bundled_assets_present")
        and indep_cov.get("ok")
        and bool(founding)
        and ar is not None
    )
    plug_and_play_runtime = plug_and_play_data and all(py_pkgs.values()) and tools.get("python") is not None

    return {
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(ar) if ar else None,
        "lean_hub": str(ROOT),
        "drive_letter_independent": ar is not None and (ROOT / ".fsot-canonical-hub").is_file(),
        "founding_roots": [str(p) for p in founding],
        "fsot_compute": str(fsot_compute_path()),
        "locations": {
            "i_drive_lean_hub": {
                "path": str(ROOT),
                "git_head": i_head,
                "origin_main": origin_head,
                "github_remote": GITHUB_REMOTE,
            },
            "c_desktop_mirror": {
                "path": str(DESKTOP_MIRROR),
                "exists": DESKTOP_MIRROR.exists(),
                "git_head": c_head,
                "policy": "deprecated read-only mirror — never verify or push from here",
            },
            "github": {
                "remote": GITHUB_REMOTE,
                "origin_main": origin_head,
                "note": "Code + JSON on GitHub; .lake cache and large vendor blobs archive-only",
            },
        },
        "archive_sections": section_stats,
        "i_vs_c_mirror": mirror_compare,
        "host_toolchain": tools,
        "python_packages": py_pkgs,
        "sub_audits": {
            "portable_vendor_coverage": {
                "ran": vendor_audit.get("ran"),
                "ok": vendor_audit.get("ok"),
                "missing_benchmark_domains": vendor_cov.get("missing_benchmark_domains", []),
                "missing_bundled_assets": vendor_cov.get("missing_bundled_assets", []),
                "extension_domain_count": vendor_cov.get("extension_domain_count"),
                "all_extension_benchmarks_present": vendor_cov.get("all_extension_benchmarks_present"),
                "all_bundled_assets_present": vendor_cov.get("all_bundled_assets_present"),
            },
            "archive_independence": {
                "ran": indep_audit.get("ran"),
                "ok": indep_cov.get("ok"),
                "critical_count": indep_cov.get("critical_count", 0),
            },
        },
        "plug_and_play": {
            "data_complete_on_drive": plug_and_play_data,
            "runnable_without_downloads": plug_and_play_runtime,
            "requires_one_time_host_install": [
                "Python 3.10+",
                "pip install -r requirements.txt (numpy, mpmath, sympy, PyYAML, pypdf, pytest)",
                "Optional: elan + Lean 4.31 for lake build",
                "Optional: Rust for obligation replay cross-proof tier",
                "Optional: Coq, Isabelle, F* for full seven-way cross-proof",
            ],
            "offline_verification_mode": "PLAY.ps1 → portable runner with --skip-lean --portable --founding-corpus",
            "live_api_rebuild": "Not required for scientific verification — uses cached benchmarks in data/ and 03_FSOT-PublicData",
        },
        "blockers": blockers,
        "warnings": warnings,
        "ok": len(blockers) == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--skip-fetch", action="store_true")
    parser.add_argument("--quick", action="store_true", help="Skip slow directory size scans")
    args = parser.parse_args()
    doc = audit(skip_fetch=args.skip_fetch, quick=args.quick)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps(doc, indent=2))
    return 0 if doc["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())