#!/usr/bin/env python3
"""Extension benchmark panel for Living FSOT QEMU hardware verification."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "living_fsot_hardware_verification_report.json"
OUT = ROOT / "data" / "living_fsot_hardware_benchmark.json"

sys.path.insert(0, str(ROOT / "scripts"))
from living_fsot_lib import k_parity_check  # noqa: E402


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8")) if AUDIT.exists() else {}
    k = k_parity_check()
    live = audit.get("live_operational") or {}
    checks = audit.get("checks_passed") or {}

    def row(name: str, computed: float, measured: float, *, prop: str, unit: str = "dimensionless") -> dict:
        err = abs(computed - measured) / abs(measured) * 100.0 if measured else 0.0
        return {
            "lab": "living_fsot_hardware_lab",
            "property": prop,
            "name": name,
            "computed": computed,
            "measured": measured,
            "error_pct": err,
            "unit": unit,
            "eval_kind": "hardware_verification_gate",
            "domain_display_name": "living fsot hardware",
            "display_name": name.replace("_", " "),
        }

    records: list[dict] = []

    if k.get("canonical_k") is not None:
        records.append(
            row(
                "scalar_k_parity",
                float(k.get("living_rust_k") or 0),
                float(k["canonical_k"]),
                prop="fsot_scalar_k",
            )
        )

    records.append(
        {
            "lab": "living_fsot_hardware_lab",
            "property": "body_online",
            "name": "mind_body_bridge",
            "computed": 1.0 if live.get("body_online") else 0.0,
            "measured": 1.0,
            "error_pct": 0.0 if live.get("body_online") else 100.0,
            "eval_kind": "hardware_verification_gate",
            "domain_display_name": "living fsot hardware",
            "display_name": "mind body bridge",
        }
    )

    records.append(
        {
            "lab": "living_fsot_hardware_lab",
            "property": "uefi_kernel_artifacts",
            "name": "build_artifacts",
            "computed": 1.0 if checks.get("build_artifacts") else 0.0,
            "measured": 1.0,
            "error_pct": 0.0 if checks.get("build_artifacts") else 100.0,
            "eval_kind": "hardware_verification_gate",
            "domain_display_name": "living fsot hardware",
            "display_name": "build artifacts",
        }
    )

    bench_rate = live.get("benchmark_pass_rate")
    if bench_rate is not None:
        records.append(
            row(
                "task_battery_pass_rate",
                float(bench_rate),
                1.0,
                prop="living_task_battery",
            )
        )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(AUDIT.relative_to(ROOT)) if AUDIT.exists() else None,
        "domain": "Living_FSOT_Hardware",
        "display_name": "Living FSOT Hardware (QEMU body)",
        "tier_label": "Tier 93",
        "record_count": len(records),
        "material_records": records,
        "audit_overall_ok": audit.get("overall_ok"),
        "living_root": audit.get("living_root"),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())