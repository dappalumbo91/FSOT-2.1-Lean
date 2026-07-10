#!/usr/bin/env python3
"""Tier 86 — triangulate F* spec constants against Rust/Python oracle."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fstar_verification_lib import parse_fstar_constants, run_fstar_verify  # noqa: E402
from rust_lean_bridge_lib import BOOT_SCALAR, boot_scalar  # noqa: E402

OUT = ROOT / "data" / "cross_refinement_fstar_report.json"
FSTAR_REPORT = ROOT / "data" / "fstar_verification_report.json"


def main() -> int:
    fstar = run_fstar_verify()
    consts = parse_fstar_constants()
    py_boot = boot_scalar()

    checks = {
        "fstar_verify_passed": fstar.get("status") == "passed",
        "fstar_k_matches_rust": abs(consts.get("k_fsot", 0) - 0.4202216641606967) < 1e-15,
        "fstar_boot_scalar_canonical_matches": abs(
            consts.get("boot_scalar_canonical", 0) - BOOT_SCALAR
        )
        < 1e-17,
        "python_boot_matches_fstar_canonical": abs(py_boot - consts.get("boot_scalar_canonical", -1)) < 1e-17,
        "python_boot_matches_rust_oracle": abs(py_boot - BOOT_SCALAR) < 1e-17,
        "fstar_boot_params_match": consts.get("boot_d_eff") == 8.0
        and abs(consts.get("boot_delta_psi", 0) - 0.7) < 1e-15,
    }

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "86_cross_refinement_fstar",
        "fstar_constants": consts,
        "python_boot_scalar": py_boot,
        "checks": checks,
        "numeric_shell_note": (
            "F* boot_scalar_positive / boot_scalar_matches_canonical use admit() for "
            "transcendental shell; numeric truth triangulated via Rust/Python f64."
        ),
        "overall_ok": all(checks.values()),
        "fstar_report": str(FSTAR_REPORT),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    print("CROSS-REFINEMENT FSTAR AUDIT")
    for k, v in checks.items():
        print(f"  {k}: {v}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())