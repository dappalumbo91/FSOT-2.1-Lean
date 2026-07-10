#!/usr/bin/env python3
"""Tier 85 — triangulate rust_lean_bridge summary, Python oracle, and runtime parity."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_paths import rust_lean_bridge_summary_path, vl_distill_atlas_summary_path  # noqa: E402
from rust_lean_bridge_lib import BOOT_SCALAR, boot_scalar, load_summary  # noqa: E402

OUT = ROOT / "data" / "cross_refinement_rust_lean_bridge_report.json"
PARITY = ROOT / "data" / "rust_lean_bridge_runtime_parity_report.json"


def main() -> int:
    summary = load_summary()
    atlas = json.loads(vl_distill_atlas_summary_path().read_text(encoding="utf-8"))
    py_boot = boot_scalar()
    parity = json.loads(PARITY.read_text(encoding="utf-8")) if PARITY.exists() else {}

    k_rust = float(summary.get("K") or 0)
    k_atlas = float(atlas.get("K_FSOT") or summary.get("atlas_K_FSOT") or 0)
    summary_boot = float(summary.get("boot_scalar") or 0)

    checks = {
        "python_boot_matches_canonical": abs(py_boot - BOOT_SCALAR) < 1e-14,
        "summary_boot_matches_canonical": abs(summary_boot - BOOT_SCALAR) < 1e-14,
        "python_summary_agree": abs(py_boot - summary_boot) < 1e-14,
        "k_matches_atlas": abs(k_rust - k_atlas) < 1e-12,
        "boot_scalar_positive": bool(summary.get("boot_scalar_positive")),
        "cargo_runtime_passed": parity.get("cargo_runtime_parity", {}).get("status") == "passed",
    }

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "85_cross_refinement_rust_lean_bridge",
        "summary_source": str(rust_lean_bridge_summary_path()),
        "python_boot_scalar": py_boot,
        "summary_boot_scalar": summary_boot,
        "canonical_boot_scalar": BOOT_SCALAR,
        "K_rust": k_rust,
        "K_atlas": k_atlas,
        "checks": checks,
        "overall_ok": all(checks.values()),
        "runtime_parity_report": str(PARITY),
        "note": (
            "Triangulates bare-metal POC constants/scalar against Python f64 oracle "
            "and host cargo runtime parity."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-REFINEMENT RUST_LEAN_BRIDGE AUDIT")
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())