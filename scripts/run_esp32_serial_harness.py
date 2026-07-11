#!/usr/bin/env python3
"""Tier 88 — ESP32 UART bare-metal harness (flash + serial marker capture)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from esp32_fsot_serial_lib import (  # noqa: E402
    detect_cp210x_port,
    run_esp32_hardware_harness,
)

OUT = ROOT / "data" / "esp32_fsot_serial_harness_report.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Tier 88 ESP32 serial harness")
    parser.add_argument("--port", help="COM port override (e.g. COM3)")
    parser.add_argument("--no-flash", action="store_true", help="Only capture serial; do not flash")
    args = parser.parse_args()

    port = args.port or detect_cp210x_port()
    harness = run_esp32_hardware_harness(port=port, flash=not args.no_flash)
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "91_esp32_rf_observer_enow",
        "port": port,
        "harness": harness,
        "overall_ok": harness.get("status") == "passed",
        "note": (
            "Flashes fsot-esp32-observer to CP210x ESP32 and captures FSOT_ESP32_* UART markers "
            "for eight-way bare-metal verification."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    serial = harness.get("serial_capture") or {}
    print("ESP32 FSOT SERIAL HARNESS (Tier 91)")
    print(f"  port: {port or 'n/a'}")
    print(f"  flash: {(harness.get('flash') or {}).get('status', 'n/a')}")
    print(
        f"  serial: {serial.get('status')} boot={serial.get('boot_scalar')} "
        f"hardware_boot={serial.get('hardware_boot')}"
    )
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())