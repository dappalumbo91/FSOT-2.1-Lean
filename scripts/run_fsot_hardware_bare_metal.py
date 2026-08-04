#!/usr/bin/env python3
"""Tier 91 hardware — Rust processor/RAM gates + serial markers + optional QEMU chain.

Runs the same seed-closed processor/RAM laws as Lean residual panels on:
  1) host Rust tests (fsot_hardware_kernel)
  2) host serial binary (FSOT_HW_* markers)
  3) existing QEMU disk boot (scalar bare-metal still required green)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HW_CRATE = ROOT / "verification" / "rust" / "fsot_hardware_kernel"
OUT = ROOT / "data" / "fsot_hardware_bare_metal_report.json"

# Archive / panel goldens
COLLAPSE_THETA = 0.9174663774653723
C_EFF = 0.9577022026205613
VRAM_USABLE = C_EFF * 12800.0
VRAM_MEASURED = 12226.56
GREEN_PCT = 0.5


def _cargo_env() -> dict[str, str]:
    env = os.environ.copy()
    target = Path(tempfile.gettempdir()) / "fsot_hardware_kernel_target"
    target.mkdir(parents=True, exist_ok=True)
    env["CARGO_TARGET_DIR"] = str(target)
    return env


def _parse_hw_markers(text: str) -> dict:
    out: dict = {}
    patterns = {
        "collapse_theta": r"FSOT_HW_COLLAPSE_THETA=([0-9.eE+-]+)",
        "c_eff": r"FSOT_HW_C_EFF=([0-9.eE+-]+)",
        "states_per_u64": r"FSOT_HW_STATES_PER_U64=(\d+)",
        "warp_size": r"FSOT_HW_WARP_SIZE=(\d+)",
        "vram_usable_mib": r"FSOT_HW_VRAM_USABLE_MIB=([0-9.eE+-]+)",
        "vram_measured_mib": r"FSOT_HW_VRAM_MEASURED_MIB=([0-9.eE+-]+)",
        "vram_err_pct": r"FSOT_HW_VRAM_ERR_PCT=([0-9.eE+-]+)",
        "sm_count": r"FSOT_HW_SM_COUNT=(\d+)",
        "density_gain": r"FSOT_HW_DENSITY_GAIN=(\d+)",
        "sectors": r"FSOT_HW_SECTORS=(\d+)",
        "pack_word": r"FSOT_HW_PACK_WORD=(\d+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if not m:
            continue
        if key in ("states_per_u64", "warp_size", "sm_count", "density_gain", "sectors", "pack_word"):
            out[key] = int(m.group(1))
        else:
            out[key] = float(m.group(1))
    out["overall"] = "ok" if "FSOT_HW_OVERALL=ok" in text else "fail"
    return out


def run_cargo_tests() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "failed", "reason": "cargo not on PATH"}
    try:
        # --lib only: avoids LNK1104 on Windows when the serial bin is locked
        r = subprocess.run(
            [cargo, "test", "--release", "--quiet", "--lib"],
            cwd=str(HW_CRATE),
            capture_output=True,
            text=True,
            timeout=600,
            env=_cargo_env(),
        )
        out = (r.stdout or "") + (r.stderr or "")
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "crate": "fsot_hardware_kernel",
            "returncode": r.returncode,
            "stderr_tail": out[-2500:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_hardware_serial() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "failed", "reason": "cargo not on PATH"}
    try:
        r = subprocess.run(
            [cargo, "run", "--release", "--quiet", "--bin", "fsot_hardware_serial"],
            cwd=str(HW_CRATE),
            capture_output=True,
            text=True,
            timeout=600,
            env=_cargo_env(),
        )
        out = (r.stdout or "") + (r.stderr or "")
        markers = _parse_hw_markers(out)
        checks = {
            "exit_ok": r.returncode == 0,
            "overall_ok": markers.get("overall") == "ok",
            "theta_ok": abs(markers.get("collapse_theta", -1) - COLLAPSE_THETA) < 1e-12,
            "warp_ok": markers.get("states_per_u64") == 32 and markers.get("warp_size") == 32,
            "sm_ok": markers.get("sm_count") == 48,
            "vram_err_ok": float(markers.get("vram_err_pct", 99)) < GREEN_PCT,
            "density_ok": markers.get("density_gain") == 4,
            "sectors_ok": markers.get("sectors") == 6,
            "emergence": "POSITIVE (Hardware gates green)" in out,
        }
        passed = all(checks.values())
        return {
            "status": "passed" if passed else "failed",
            "crate": "fsot_hardware_serial",
            "markers": markers,
            "checks": checks,
            "returncode": r.returncode,
            "stderr_tail": out[-2500:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_qemu_chain() -> dict:
    """Existing Tier 87 QEMU disk boot — proves no_std scalar path still green."""
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_rust_lean_bridge_qemu_harness.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        report_path = ROOT / "data" / "rust_lean_bridge_qemu_harness_report.json"
        doc = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
        return {
            "status": "passed" if r.returncode == 0 and doc.get("overall_ok") else "failed",
            "overall_ok": doc.get("overall_ok"),
            "serial": (doc.get("serial_harness") or {}).get("status"),
            "disk": (doc.get("disk_boot") or {}).get("status"),
            "qemu": (doc.get("qemu") or {}).get("status"),
            "returncode": r.returncode,
            "stderr_tail": ((r.stdout or "") + (r.stderr or ""))[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def main() -> int:
    tests = run_cargo_tests()
    serial = run_hardware_serial()
    qemu = run_qemu_chain()
    overall = (
        tests.get("status") == "passed"
        and serial.get("status") == "passed"
        and qemu.get("status") == "passed"
    )
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "91_hardware_processor_ram_bare_metal",
        "purpose": (
            "Executable processor/RAM FSOT laws on host Rust + serial markers, "
            "chained with QEMU no_std bare-metal scalar boot."
        ),
        "cargo_tests": tests,
        "hardware_serial": serial,
        "qemu_bare_metal": qemu,
        "overall_ok": overall,
        "seed_refs": {
            "collapse_theta": COLLAPSE_THETA,
            "c_eff": C_EFF,
            "vram_usable_mib": VRAM_USABLE,
            "vram_measured_mib": VRAM_MEASURED,
            "green_pct": GREEN_PCT,
        },
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print("FSOT HARDWARE BARE-METAL (processor + RAM)")
    print(f"  cargo_tests: {tests.get('status')}")
    print(f"  hardware_serial: {serial.get('status')} overall={ (serial.get('markers') or {}).get('overall') }")
    print(
        f"  qemu_chain: {qemu.get('status')} "
        f"(serial={qemu.get('serial')}, disk={qemu.get('disk')}, qemu={qemu.get('qemu')})"
    )
    print(f"  overall_ok: {overall}")
    print(f"Wrote {OUT}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
