#!/usr/bin/env python3
"""Tier 88 — flash fsot-esp32-observer to CP210x ESP32 (manual BOOT if auto-reset fails)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from esp32_fsot_serial_lib import detect_cp210x_port, flash_esp32_firmware  # noqa: E402


def main() -> int:
    port = detect_cp210x_port()
    print("ESP32 FSOT FLASH (Tier 91)")
    print(f"  detected port: {port or 'none'}")
    if not port:
        print("  Connect CP210x ESP32 and retry.")
        return 1
    print("  If auto-reset fails: hold BOOT, tap EN/RST, release EN, release BOOT during connect.")
    result = flash_esp32_firmware(port)
    print(f"  status: {result.get('status')}")
    if result.get("remediation"):
        print(f"  remediation: {result['remediation']}")
    if result.get("status") != "passed":
        print(result.get("stderr_tail", ""))
    return 0 if result.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())