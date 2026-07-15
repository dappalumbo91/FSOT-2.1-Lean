"""Tier 87 QEMU / serial / disk-boot harness helpers."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERIAL_CRATE = ROOT / "verification" / "rust" / "fsot_observer_serial"
GOLDEN_SERIAL = ROOT / "verification" / "qemu" / "golden_boot_serial.txt"
GOLDEN_DISK = ROOT / "verification" / "qemu" / "golden_boot_disk.txt"
DISK_IMAGE = ROOT / "verification" / "qemu" / "fsot-kernel-bios.bin"
KERNEL_ROOT = ROOT / "vendor" / "rust_lean_bridge"
BOOT_SCALAR = 0.09928895626861721
SCALAR_TOLERANCE = 5e-17


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


def resolve_bios_rom() -> str | None:
    for path in (
        Path(r"C:\Program Files\qemu\share\bios.bin"),
        Path(r"C:\Program Files\QEMU\share\bios.bin"),
        Path("/usr/share/seabios/bios.bin"),
        Path("/usr/share/qemu/bios.bin"),
    ):
        if path.exists():
            return str(path)
    return None


def _qemu_base_args(qemu: str, image: Path) -> list[str]:
    args = [qemu, "-display", "none"]
    bios = resolve_bios_rom()
    if bios:
        args.extend(["-bios", bios])
    args.extend(
        [
            "-drive",
            f"format=raw,file={image}",
            "-device",
            "isa-debug-exit,iobase=0xf4,iosize=0x04",
            "-no-reboot",
        ]
    )
    return args


def _serial_cargo_env() -> dict[str, str]:
    """Host temp target dir avoids LNK1104 / Access denied on removable I: drives."""
    env = os.environ.copy()
    target = Path(tempfile.gettempdir()) / "fsot_observer_serial_target"
    target.mkdir(parents=True, exist_ok=True)
    env["CARGO_TARGET_DIR"] = str(target)
    return env


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
            env=_serial_cargo_env(),
        )
        out = (r.stdout or "") + (r.stderr or "")
        markers = _parse_serial_markers(out)
        golden = _parse_serial_markers(GOLDEN_SERIAL.read_text(encoding="utf-8")) if GOLDEN_SERIAL.exists() else {}
        boot_ok = abs(markers.get("boot_scalar", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        canonical_ok = abs(markers.get("canonical", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        dynamic_ok = abs(markers.get("dynamic_check", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
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


def _resolve_disk_image() -> Path | None:
    if DISK_IMAGE.exists():
        return DISK_IMAGE
    candidates = sorted(
        KERNEL_ROOT.glob("target/**/release/bootimage-fsot-observer-kernel.bin"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def run_qemu_disk_boot(timeout_s: int = 90) -> dict:
    qemu = resolve_qemu()
    if not qemu:
        return {
            "status": "skipped",
            "reason": "qemu-system-x86_64 not on PATH",
            "note": "Run scripts/install_qemu_windows.ps1 to enable disk boot layer.",
        }
    image = _resolve_disk_image()
    if not image:
        return {"status": "failed", "reason": "bootimage not found; run build_rust_lean_bridge_bootimage.py"}

    serial_log = Path(tempfile.gettempdir()) / "fsot_qemu_disk_serial.log"
    serial_log.write_text("", encoding="utf-8")
    cmd = _qemu_base_args(qemu, image) + ["-serial", f"file:{serial_log}"]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
        out = serial_log.read_text(encoding="utf-8", errors="replace")
        markers = _parse_disk_markers(out)
        golden = _parse_disk_markers(GOLDEN_DISK.read_text(encoding="utf-8")) if GOLDEN_DISK.exists() else {}
        boot_ok = abs(markers.get("boot_scalar", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        canonical_ok = abs(markers.get("canonical", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        disk_ok = markers.get("disk_boot") == "ok"
        golden_ok = markers == golden if golden else True
        emergence_ok = "POSITIVE (Emergence)" in out
        success_exit = r.returncode in (0, 33)
        return {
            "status": "passed"
            if success_exit and boot_ok and canonical_ok and disk_ok and emergence_ok and golden_ok
            else "failed",
            "tool": qemu,
            "image": str(image),
            "bios": resolve_bios_rom(),
            "boot_scalar": markers.get("boot_scalar"),
            "canonical": markers.get("canonical"),
            "disk_boot": markers.get("disk_boot"),
            "golden_match": golden_ok,
            "emergence_detected": emergence_ok,
            "returncode": r.returncode,
            "serial_capture": out[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"status": "failed", "reason": f"QEMU disk boot timed out after {timeout_s}s", "image": str(image)}
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
        disk = run_qemu_disk_boot()
        return {
            "status": "passed"
            if r.returncode == 0 and serial.get("status") == "passed" and disk.get("status") == "passed"
            else "failed",
            "tool": qemu,
            "version": version_line,
            "harness_mode": "serial_stdout_parity_plus_disk_boot",
            "note": (
                "Tier 87 validates full no_std bootloader disk image boot with harness markers "
                "and chains Tier 86 serial stdout parity."
            ),
            "serial_parity": serial,
            "disk_boot": disk,
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


def _parse_disk_markers(text: str) -> dict:
    out: dict = {}
    patterns = {
        "boot_scalar": r"FSOT_QEMU_BOOT_SCALAR=([0-9.eE+-]+)",
        "canonical": r"FSOT_QEMU_CANONICAL=([0-9.eE+-]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = float(m.group(1))
    if "FSOT_QEMU_DISK_BOOT=ok" in text:
        out["disk_boot"] = "ok"
    return out