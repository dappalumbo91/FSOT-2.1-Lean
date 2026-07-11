#!/usr/bin/env python3
"""Tier 88 — build ESP32 fsot_esp32_observer firmware."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from esp32_fsot_serial_lib import build_esp32_firmware  # noqa: E402


def main() -> int:
    result = build_esp32_firmware()
    print("ESP32 FSOT OBSERVER BUILD (Tier 88)")
    print(f"  status: {result.get('status')}")
    print(f"  elf: {result.get('elf', 'n/a')}")
    print(f"  bin: {result.get('bin', 'n/a')}")
    if result.get("status") != "passed":
        print(result.get("stderr_tail", ""))
    return 0 if result.get("status") == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())