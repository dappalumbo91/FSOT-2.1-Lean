#!/usr/bin/env python3
"""Tier 85 — rust_lean_bridge host runtime parity (Python f64 oracle + cargo test)."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rust_lean_bridge_lib import (  # noqa: E402
    BENCH_PATH,
    BOOT_SCALAR,
    boot_scalar,
    refresh_summary_boot_scalar,
    run_cargo_runtime_parity,
)

OUT = ROOT / "data" / "rust_lean_bridge_runtime_parity_report.json"


def main() -> int:
    py_boot = boot_scalar()
    py_ok = abs(py_boot - BOOT_SCALAR) < 1e-14 and py_boot > 0.0

    summary = refresh_summary_boot_scalar()
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_rust_lean_bridge_benchmark.py")],
        cwd=str(ROOT),
        check=False,
    )
    bench = json.loads(BENCH_PATH.read_text(encoding="utf-8")) if BENCH_PATH.exists() else {}
    cargo = run_cargo_runtime_parity()

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "85_rust_lean_bridge_runtime_parity",
        "python_boot_scalar": py_boot,
        "canonical_boot_scalar": BOOT_SCALAR,
        "python_boot_ok": py_ok,
        "summary_boot_scalar": summary.get("boot_scalar"),
        "benchmark_median_error_pct": bench.get("median_error_pct"),
        "benchmark_record_count": bench.get("record_count"),
        "cargo_runtime_parity": cargo,
        "overall_ok": py_ok
            and cargo.get("status") == "passed"
            and bench.get("median_error_pct", 99) <= 1.0
            and bench.get("record_count", 0) >= 5,
        "note": (
            "Host-runnable scalar kernel matches bare-metal POC summary; "
            "cargo test exercises boot + dynamic spot checks."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("RUST_LEAN_BRIDGE RUNTIME PARITY (Tier 85)")
    print(f"  python boot_scalar: {py_boot} (ok={py_ok})")
    print(f"  cargo: {cargo.get('status')}")
    print(f"  benchmark median_err: {bench.get('median_error_pct')}%")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())