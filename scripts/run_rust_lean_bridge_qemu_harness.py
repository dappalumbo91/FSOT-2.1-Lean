#!/usr/bin/env python3
"""Tier 86 — QEMU bare-metal harness (serial stdout parity + QEMU smoke)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rust_lean_bridge_qemu_lib import run_qemu_smoke, run_serial_harness  # noqa: E402

OUT = ROOT / "data" / "rust_lean_bridge_qemu_harness_report.json"


def main() -> int:
    serial = run_serial_harness()
    qemu = run_qemu_smoke()
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "86_rust_lean_bridge_qemu_harness",
        "serial_harness": serial,
        "qemu": qemu,
        "overall_ok": serial.get("status") == "passed"
            and qemu.get("status") in ("passed", "skipped"),
        "note": (
            "Serial harness mirrors bare-metal VGA boot lines; QEMU layer confirms "
            "emulator availability and chains serial parity."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print("RUST_LEAN_BRIDGE QEMU HARNESS (Tier 86)")
    print(f"  serial: {serial.get('status')} boot={serial.get('boot_scalar')}")
    print(f"  qemu: {qemu.get('status')} ({qemu.get('version', qemu.get('reason', 'n/a'))})")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())