#!/usr/bin/env python3
"""Tier 87 — build bootloader disk image from vendor/rust_lean_bridge."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_ROOT = ROOT / "vendor" / "rust_lean_bridge"
OUT_IMAGE = ROOT / "verification" / "qemu" / "fsot-kernel-bios.bin"
REPORT = ROOT / "data" / "rust_lean_bridge_bootimage_report.json"


def _find_cargo() -> str | None:
    return shutil.which("cargo")


def _find_bootimage() -> str | None:
    return shutil.which("bootimage") or shutil.which("bootimage.exe")


def build_bootimage() -> dict:
    cargo = _find_cargo()
    if not cargo:
        return {"status": "failed", "reason": "cargo not on PATH"}

    env = os.environ.copy()
    env["CARGO_MANIFEST_DIR"] = str(KERNEL_ROOT)

    try:
        r = subprocess.run(
            [cargo, "bootimage", "--release"],
            cwd=str(KERNEL_ROOT),
            capture_output=True,
            text=True,
            timeout=1800,
            env=env,
        )
        out = (r.stdout or "") + (r.stderr or "")
        candidates = sorted(
            KERNEL_ROOT.glob("target/**/release/bootimage-fsot-observer-kernel.bin"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            return {
                "status": "failed",
                "reason": "bootimage output not found",
                "returncode": r.returncode,
                "stderr_tail": out[-3000:],
            }
        src = candidates[0]
        OUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, OUT_IMAGE)
        sig = OUT_IMAGE.read_bytes()[510:512]
        return {
            "status": "passed" if r.returncode == 0 and sig == b"\x55\xaa" else "failed",
            "source": str(src),
            "output": str(OUT_IMAGE),
            "size_bytes": OUT_IMAGE.stat().st_size,
            "boot_signature": sig.hex(),
            "returncode": r.returncode,
            "stderr_tail": out[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def main() -> int:
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "87_rust_lean_bridge_bootimage",
        "kernel_root": str(KERNEL_ROOT),
        "bootimage": _find_bootimage(),
        "build": build_bootimage(),
        "overall_ok": False,
    }
    doc["overall_ok"] = doc["build"].get("status") == "passed"
    REPORT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print("RUST_LEAN_BRIDGE BOOTIMAGE (Tier 87)")
    print(f"  build: {doc['build'].get('status')} -> {doc['build'].get('output', 'n/a')}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {REPORT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())