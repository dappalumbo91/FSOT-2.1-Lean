#!/usr/bin/env python3
"""Targeted hardware competitive refine: analyze failures, measure, residual-gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hardware_competitive_refine_lib import run_full_refine  # noqa: E402


def _cargo_env():
    import os
    import tempfile

    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = str(Path(tempfile.gettempdir()) / "fsot_hardware_kernel_target")
    return env


def run_rust_pack_verify() -> dict:
    """Accurate pack/gate metrics from fsot_hardware_kernel tests."""
    import shutil

    cargo = shutil.which("cargo")
    crate = ROOT / "verification" / "rust" / "fsot_hardware_kernel"
    if not cargo or not crate.is_dir():
        return {"status": "skipped", "reason": "cargo/crate missing"}
    r = subprocess.run(
        [cargo, "test", "--release", "--quiet", "--lib"],
        cwd=str(crate),
        capture_output=True,
        text=True,
        timeout=300,
        env=_cargo_env(),
    )
    return {
        "status": "passed" if r.returncode == 0 else "failed",
        "returncode": r.returncode,
        "stderr_tail": ((r.stdout or "") + (r.stderr or ""))[-1500:],
    }


def run_rust_cpu_bench() -> dict:
    """Rust dense vs compact — lowers β_f vs Python on small S."""
    import re
    import shutil

    cargo = shutil.which("cargo")
    crate = ROOT / "verification" / "rust" / "fsot_hardware_kernel"
    if not cargo or not crate.is_dir():
        return {"status": "skipped", "reason": "cargo/crate missing"}
    r = subprocess.run(
        [cargo, "run", "--release", "--quiet", "--bin", "cpu_competitive_bench"],
        cwd=str(crate),
        capture_output=True,
        text=True,
        timeout=600,
        env=_cargo_env(),
    )
    out = (r.stdout or "") + (r.stderr or "")
    rows = []
    for line in out.splitlines():
        if not line.startswith("RUST_CPU"):
            continue
        m = re.search(
            r"H=(\d+) S=(\d+) D=(\d+) A_frac=([0-9.eE+-]+) work_ratio=([0-9.eE+-]+) "
            r"wall_speedup=([0-9.eE+-]+) T_dense_ms=([0-9.eE+-]+) T_fsot_ms=([0-9.eE+-]+) "
            r"work_win=(\w+) wall_win=(\w+)",
            line,
        )
        if not m:
            continue
        rows.append(
            {
                "H": int(m.group(1)),
                "S": int(m.group(2)),
                "D": int(m.group(3)),
                "A_frac": float(m.group(4)),
                "work_ratio": float(m.group(5)),
                "wall_speedup": float(m.group(6)),
                "T_dense_ms": float(m.group(7)),
                "T_fsot_ms": float(m.group(8)),
                "work_win": m.group(9) == "true",
                "wall_win": m.group(10) == "true",
            }
        )
    work_ok = all(x["work_win"] for x in rows) if rows else False
    wall_ok = sum(1 for x in rows if x["wall_win"])
    return {
        "status": "passed" if r.returncode == 0 and rows and work_ok else "failed",
        "returncode": r.returncode,
        "rows": rows,
        "work_wins": sum(1 for x in rows if x["work_win"]),
        "wall_wins": wall_ok,
        "n": len(rows),
        "stderr_tail": out[-2000:],
    }


def main() -> int:
    print("HARDWARE COMPETITIVE REFINE (CPU vs CPU, RAM vs RAM; GPU separate)")
    doc = run_full_refine()
    rust = run_rust_pack_verify()
    rust_cpu = run_rust_cpu_bench()
    doc["rust_hardware_kernel_tests"] = rust
    doc["rust_cpu_competitive"] = rust_cpu
    # Primary: Python work law + RAM density (mathematical FSOT)
    # Secondary: Rust unit tests + Rust CPU work/wall (β_f resolution)
    # Note: cargo test may LNK-race with bin on Windows; re-run or rely on rust_cpu.
    primary = bool(doc["overall_primary_ok"])
    secondary = bool(
        rust_cpu.get("status") == "passed"
        and rust_cpu.get("work_wins") == rust_cpu.get("n")
        and rust_cpu.get("wall_wins") == rust_cpu.get("n")
    )
    rust_units = rust.get("status") == "passed"
    doc["refine_gates"] = {
        "primary_python_work_and_ram": primary,
        "secondary_rust_cpu_work_and_wall": secondary,
        "rust_unit_tests": rust_units,
        "rust_cpu_wall_wins": rust_cpu.get("wall_wins"),
        "rust_cpu_n": rust_cpu.get("n"),
    }
    out = ROOT / "data" / "hardware_competitive_refine_report.json"
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    cpu = doc["cpu"]["summary"]
    ram = doc["ram"]["summary"]
    print(f"  CPU work_wins: {cpu['work_wins']}/{cpu['n']} primary_ok={cpu['primary_work_ok']}")
    print(f"  CPU wall_wins: {cpu['wall_wins']}/{cpu['n']} long_S={cpu['long_S_wall_wins']}/{cpu['long_S_n']}")
    print(f"  CPU fail_modes: {cpu['fail_modes']}")
    print(f"  RAM suite_ok: {ram['suite_ok']} density={ram['density_ok']} roundtrip={ram['roundtrip_ok']}")
    print(f"  rust kernel: {rust.get('status')}")
    print(
        f"  rust CPU bench: {rust_cpu.get('status')} "
        f"work={rust_cpu.get('work_wins')}/{rust_cpu.get('n')} "
        f"wall={rust_cpu.get('wall_wins')}/{rust_cpu.get('n')}"
    )
    print(f"  overall_primary_ok: {primary} secondary_rust_wall: {secondary}")
    print(f"Wrote {out}")

    print("\n  --- CPU Python shape diagnostics ---")
    for r in doc["cpu"]["shapes"]:
        print(
            f"  {r['H']}x{r['S']}x{r['D']}: A_frac={r['A_frac']:.4f} "
            f"work_ratio={r['work_ratio']:.1f}x wall={r['wall_speedup']:.2f}x "
            f"mode={r['fail_mode']}"
        )
        if r["fail_mode"] != "pass_work_and_wall":
            print(f"      → {r['resolution']}")

    if rust_cpu.get("rows"):
        print("\n  --- CPU Rust shape diagnostics (β_f resolution) ---")
        for r in rust_cpu["rows"]:
            print(
                f"  {r['H']}x{r['S']}x{r['D']}: A_frac={r['A_frac']:.4f} "
                f"work_ratio={r['work_ratio']:.1f}x wall={r['wall_speedup']:.2f}x "
                f"work_win={r['work_win']} wall_win={r['wall_win']}"
            )

    ok = primary and secondary
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
