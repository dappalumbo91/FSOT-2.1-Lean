#!/usr/bin/env python3
"""Tier 86 — triangulate F* spec constants against Rust/Python oracle."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fstar_verification_lib import parse_fstar_constants, run_fstar_verify  # noqa: E402
from rust_lean_bridge_lib import (  # noqa: E402
    A_BLEED,
    A_IN,
    ALPHA,
    BETA,
    B_IN,
    BOOT_D_EFF,
    BOOT_DELTA_PSI,
    BOOT_RECENT_HITS,
    BOOT_SCALAR,
    C_EFF,
    C_FACTOR,
    CHAOS,
    ETA_EFF,
    GAMMA_EULER,
    K,
    PHI,
    PI,
    POOF,
    PSI_CON,
    P_NEW,
    P_VAR,
    SUCTION,
    THETA_S,
    boot_scalar,
)

OUT = ROOT / "data" / "cross_refinement_fstar_report.json"
FSTAR_REPORT = ROOT / "data" / "fstar_verification_report.json"
REAL_RE = re.compile(r"let\s+(\w+)\s*:\s*real\s*=\s*([0-9.]+)R")


def _parse_kernel_oracle_literals() -> dict[str, float]:
    text = (ROOT / "verification" / "fstar" / "FSOTScalarKernel.fst").read_text(encoding="utf-8")
    out: dict[str, float] = {}
    for name, val in REAL_RE.findall(text):
        if name.endswith("_boot") or name in {"sqrt_boot_d", "log_d25_boot"}:
            out[name] = float(val)
    for name in ("cos_psi_eta_boot", "cos_dp_pvar_boot", "cos_theta_pi_boot", "log_d25_boot"):
        m = re.search(
            rf"let {name}\s*:\s*real\s*=\s*0\.0R\s*-\.\s*([0-9.]+)R",
            text,
        )
        if m:
            out[name] = -float(m.group(1))
    return out


def _kernel_expansion_scalar(lits: dict[str, float]) -> float:
    import math

    n = 1.0
    p = 1.0
    d = BOOT_D_EFF
    dp = BOOT_DELTA_PSI
    hits = BOOT_RECENT_HITS
    sqrt_d = lits["sqrt_boot_d"]
    growth = math.exp(ALPHA * (1.0 - hits / n) * GAMMA_EULER / PHI)
    base = (
        (n * p / sqrt_d)
        * lits["cos_psi_eta_boot"]
        * math.exp(-ALPHA * hits / n + 1.0 + B_IN * dp)
        * (1.0 + growth * C_EFF)
    )
    t1_base = base * (1.0 + P_NEW * lits["log_d25_boot"])
    t1 = t1_base * math.exp(C_FACTOR * P_VAR) * lits["cos_dp_pvar_boot"]
    valve = (
        BETA
        * lits["cos_dp_boot"]
        * (n * p / sqrt_d)
        * (1.0 + CHAOS * (d - 25.0) / 25.0)
        * (1.0 + POOF * lits["cos_theta_pi_boot"] + SUCTION * lits["sin_theta_boot"])
    )
    acoustic = (
        1.0
        + (A_BLEED * lits["sin_1_boot"] * lits["sin_1_boot"]) / PHI
        + (A_IN * lits["cos_1_boot"] * lits["cos_1_boot"]) / PHI
    )
    phase = 1.0 + B_IN * P_VAR
    t3 = valve * acoustic * phase
    return K * (t1 + t3)


def main() -> int:
    fstar = run_fstar_verify()
    consts = parse_fstar_constants()
    py_boot = boot_scalar()

    kernel_text = (ROOT / "verification" / "fstar" / "FSOTScalarKernel.fst").read_text(encoding="utf-8")
    assumed_primitives = [
        name
        for name in ("cos", "sin", "sqrt")
        if f"assume val {name}" in kernel_text
    ]
    assumed_lemmas = [
        line.strip()
        for line in (ROOT / "verification" / "fstar" / "FSOTScalarBoot.fst").read_text(encoding="utf-8").splitlines()
        if re.search(r"\bassume\b", line, re.I) and not line.strip().startswith("///")
    ]

    kernel_lits = _parse_kernel_oracle_literals()
    kernel_expansion = _kernel_expansion_scalar(kernel_lits)

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
        "fstar_no_transcendental_assumes": len(assumed_primitives) == 0,
        "fstar_kernel_expansion_matches_oracle": abs(kernel_expansion - BOOT_SCALAR) < 1e-17,
    }

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "86_cross_refinement_fstar",
        "fstar_constants": consts,
        "fstar_kernel_expansion_scalar": kernel_expansion,
        "python_boot_scalar": py_boot,
        "checks": checks,
        "numeric_shell_note": (
            "F* boot kernel uses oracle literals at POC transcendental evaluation sites; "
            "exp/log remain primitive; triangulated against Rust/Python f64."
        ),
        "fstar_assumed_primitives": assumed_primitives,
        "fstar_assumed_lemmas": assumed_lemmas,
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