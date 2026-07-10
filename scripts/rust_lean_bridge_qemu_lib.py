"""Tier 86 QEMU / serial harness helpers."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIAL_CRATE = ROOT / "verification" / "rust" / "fsot_observer_serial"
GOLDEN = ROOT / "verification" / "qemu" / "golden_boot_serial.txt"
BOOT_SCALAR = 0.09928895626861721


def resolve_qemu() -> str | None:
    for name in ("qemu-system-x86_64", "qemu-system-x86_64.exe"):
        found = shutil.which(name)
        if found:
            return found
    for base in (
        Path(r"C:\Program Files\qemu"),
        Path(r"C:\Program Files\QEMU"),
    ):
        exe = base / "qemu-system-x86_64.exe"
        if exe.exists():
            return str(exe)
    return None


def run_serial_harness() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "skipped", "reason": "cargo not on PATH"}
    try:
        r = subprocess.run(
            [cargo, "run", "--quiet", "--release"],
            cwd=str(SERIAL_CRATE),
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = (r.stdout or "") + (r.stderr or "")
        markers = _parse_serial_markers(out)
        golden = _parse_serial_markers(GOLDEN.read_text(encoding="utf-8")) if GOLDEN.exists() else {}
        boot_ok = abs(markers.get("boot_scalar", -1) - BOOT_SCALAR) < 1e-17
        canonical_ok = abs(markers.get("canonical", -1) - BOOT_SCALAR) < 1e-17
        dynamic_ok = abs(markers.get("dynamic_check", -1) - BOOT_SCALAR) < 1e-17
        golden_ok = markers == golden if golden else True
        emergence_ok = "POSITIVE (Emergence)" in out
        return {
            "status": "passed"
            if r.returncode == 0 and boot_ok and canonical_ok and dynamic_ok and emergence_ok
            else "failed",
            "crate": "fsot_observer_serial",
            "boot_scalar": markers.get("boot_scalar"),
            "canonical": markers.get("canonical"),
            "dynamic_check": markers.get("dynamic_check"),
            "golden_match": golden_ok,
            "emergence_detected": emergence_ok,
            "returncode": r.returncode,
            "stderr_tail": out[-2500:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def run_qemu_smoke() -> dict:
    qemu = resolve_qemu()
    if not qemu:
        return {
            "status": "skipped",
            "reason": "qemu-system-x86_64 not on PATH",
            "note": "Run scripts/install_qemu_windows.ps1 to enable full QEMU layer.",
        }
    try:
        r = subprocess.run(
            [qemu, "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = (r.stdout or "") + (r.stderr or "")
        version_line = out.strip().splitlines()[0] if out.strip() else ""
        serial = run_serial_harness()
        return {
            "status": "passed" if r.returncode == 0 and serial.get("status") == "passed" else "failed",
            "tool": qemu,
            "version": version_line,
            "harness_mode": "serial_stdout_parity",
            "note": (
                "QEMU available; Tier 86 validates serial boot capture that mirrors VGA POC. "
                "Full no_std disk image boot is Tier 87."
            ),
            "serial_parity": serial,
            "returncode": r.returncode,
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def _parse_serial_markers(text: str) -> dict[str, float]:
    out: dict[str, float] = {}
    patterns = {
        "boot_scalar": r"FSOT_SERIAL_BOOT_SCALAR=([0-9.eE+-]+)",
        "canonical": r"FSOT_SERIAL_CANONICAL=([0-9.eE+-]+)",
        "dynamic_check": r"FSOT_SERIAL_DYNAMIC_CHECK=([0-9.eE+-]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = float(m.group(1))
    return out