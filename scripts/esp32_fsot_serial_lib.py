"""Tier 88 ESP32 UART / serial harness helpers."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ESP32_CRATE = ROOT / "verification" / "esp32" / "fsot_esp32_observer"
GOLDEN_SERIAL = ROOT / "verification" / "esp32" / "golden_boot_serial.txt"
BOOT_SCALAR = 0.09928895626861721
SCALAR_TOLERANCE = 5e-17
DEFAULT_BAUD = 115_200
DEFAULT_CAPTURE_S = 12


def resolve_espflash() -> str | None:
    for name in ("espflash", "espflash.exe"):
        found = shutil.which(name)
        if found:
            return found
    cargo_bin = Path.home() / ".cargo" / "bin" / "espflash.exe"
    if cargo_bin.exists():
        return str(cargo_bin)
    return None


def detect_cp210x_port() -> str | None:
    try:
        import serial.tools.list_ports

        for port in serial.tools.list_ports.comports():
            desc = (port.description or "").lower()
            if "cp210" in desc or "silicon labs" in desc:
                return port.device
    except Exception:
        pass

    try:
        import subprocess as sp

        r = sp.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-WmiObject Win32_SerialPort | Where-Object { $_.Description -match 'CP210' }).DeviceID",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        line = (r.stdout or "").strip().splitlines()
        if line and line[0].startswith("COM"):
            return line[0]
    except Exception:
        pass
    return None


def build_esp32_firmware() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "skipped", "reason": "cargo not on PATH"}
    env = os.environ.copy()
    export_ps1 = Path.home() / "export-esp.ps1"
    if export_ps1.exists():
        r = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f". '{export_ps1}'; cargo +esp build --release",
            ],
            cwd=str(ESP32_CRATE),
            capture_output=True,
            text=True,
            timeout=900,
        )
    else:
        r = subprocess.run(
            [cargo, "+esp", "build", "--release"],
            cwd=str(ESP32_CRATE),
            capture_output=True,
            text=True,
            timeout=900,
            env=env,
        )
    out = (r.stdout or "") + (r.stderr or "")
    elf_candidates = sorted(
        ESP32_CRATE.glob("target/xtensa-esp32-none-elf/release/fsot-esp32-observer"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    bin_candidates = sorted(
        ESP32_CRATE.glob("target/xtensa-esp32-none-elf/release/fsot-esp32-observer.bin"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return {
        "status": "passed" if r.returncode == 0 and elf_candidates else "failed",
        "crate": "fsot_esp32_observer",
        "elf": str(elf_candidates[0]) if elf_candidates else None,
        "bin": str(bin_candidates[0]) if bin_candidates else None,
        "returncode": r.returncode,
        "stderr_tail": out[-4000:],
    }


def flash_esp32_firmware(port: str | None = None) -> dict:
    espflash = resolve_espflash()
    if not espflash:
        return {
            "status": "skipped",
            "reason": "espflash not on PATH",
            "note": "Run: cargo install espflash --locked",
        }
    build = build_esp32_firmware()
    if build.get("status") != "passed":
        return {"status": "failed", "reason": "firmware build failed", "build": build}

    port = port or detect_cp210x_port()
    if not port:
        return {"status": "skipped", "reason": "no CP210x COM port detected"}

    elf = build.get("elf")
    if not elf:
        return {"status": "failed", "reason": "ELF artifact missing after build"}

    boot_mode_hint = (
        "If flash fails with boot mode 0x13: hold BOOT, tap EN/RST, release EN, release BOOT, "
        "then re-run the harness while keeping BOOT held during 'Connecting...'."
    )
    try:
        r = subprocess.run(
            [espflash, "flash", "--chip", "esp32", "--port", port, "--baud", "115200", elf],
            capture_output=True,
            text=True,
            timeout=180,
        )
        out = (r.stdout or "") + (r.stderr or "")
        boot_mode_blocked = "boot mode" in out.lower() or "download mode" in out.lower()
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "tool": espflash,
            "port": port,
            "elf": elf,
            "returncode": r.returncode,
            "boot_mode_manual_required": boot_mode_blocked,
            "remediation": boot_mode_hint if boot_mode_blocked else None,
            "stderr_tail": out[-4000:],
        }
    except Exception as e:
        return {
            "status": "failed",
            "reason": str(e),
            "port": port,
            "remediation": boot_mode_hint,
        }


def capture_serial_output(port: str | None = None, seconds: int = DEFAULT_CAPTURE_S) -> dict:
    port = port or detect_cp210x_port()
    if not port:
        return {"status": "skipped", "reason": "no CP210x COM port detected"}

    try:
        import serial
    except ImportError:
        return {"status": "skipped", "reason": "pyserial not installed"}

    chunks: list[str] = []
    try:
        with serial.Serial(port, DEFAULT_BAUD, timeout=0.5) as ser:
            ser.reset_input_buffer()
            deadline = time.time() + seconds
            while time.time() < deadline:
                raw = ser.read(4096)
                if raw:
                    chunks.append(raw.decode("utf-8", errors="replace"))
                if "FSOT_ESP32_HARDWARE_BOOT=ok" in "".join(chunks):
                    break
                time.sleep(0.05)
        text = "".join(chunks)
        markers = _parse_esp32_markers(text)
        golden = _parse_esp32_markers(GOLDEN_SERIAL.read_text(encoding="utf-8")) if GOLDEN_SERIAL.exists() else {}
        boot_ok = abs(markers.get("boot_scalar", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        canonical_ok = abs(markers.get("canonical", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        dynamic_ok = abs(markers.get("dynamic_check", -1) - BOOT_SCALAR) < SCALAR_TOLERANCE
        hardware_ok = markers.get("hardware_boot") == "ok"
        golden_ok = markers == golden if golden else True
        emergence_ok = "POSITIVE (Emergence)" in text
        return {
            "status": "passed"
            if boot_ok and canonical_ok and dynamic_ok and hardware_ok and emergence_ok and golden_ok
            else "failed",
            "port": port,
            "baud": DEFAULT_BAUD,
            "boot_scalar": markers.get("boot_scalar"),
            "canonical": markers.get("canonical"),
            "dynamic_check": markers.get("dynamic_check"),
            "hardware_boot": markers.get("hardware_boot"),
            "golden_match": golden_ok,
            "emergence_detected": emergence_ok,
            "serial_capture": text[-4000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e), "port": port}


def run_esp32_hardware_harness(port: str | None = None, flash: bool = True) -> dict:
    flash_result = flash_esp32_firmware(port) if flash else {"status": "skipped", "note": "flash skipped"}
    if flash and flash_result.get("status") != "passed":
        return {
            "status": "failed",
            "flash": flash_result,
            "serial_capture": {"status": "skipped", "reason": "flash failed"},
        }

    time.sleep(1.5)
    serial = capture_serial_output(port)
    return {
        "status": "passed"
        if serial.get("status") == "passed" and flash_result.get("status") in ("passed", "skipped")
        else "failed",
        "flash": flash_result,
        "serial_capture": serial,
        "note": (
            "Tier 88 validates ESP32 UART boot with FSOT_ESP32_* markers, "
            "chaining Tier 87 QEMU disk boot parity."
        ),
    }


def _parse_esp32_markers(text: str) -> dict:
    out: dict = {}
    patterns = {
        "boot_scalar": r"FSOT_ESP32_BOOT_SCALAR=([0-9.eE+-]+)",
        "canonical": r"FSOT_ESP32_CANONICAL=([0-9.eE+-]+)",
        "dynamic_check": r"FSOT_ESP32_DYNAMIC_CHECK=([0-9.eE+-]+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = float(m.group(1))
    if "FSOT_ESP32_HARDWARE_BOOT=ok" in text:
        out["hardware_boot"] = "ok"
    return out