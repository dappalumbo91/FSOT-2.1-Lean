"""Tier 85 rust_lean_bridge runtime parity helpers."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_DIR = ROOT / "verification" / "rust" / "fsot_scalar_kernel"
SUMMARY_PATH = ROOT / "vendor" / "rust_lean_bridge" / "rust_lean_bridge_summary.json"
BENCH_PATH = ROOT / "data" / "rust_lean_bridge_benchmark.json"

# Mirrors verification/rust/fsot_scalar_kernel/src/lib.rs (simplified POC kernel).
K = 0.4202216641606967
ALPHA = 0.0008082937414140405
PSI_CON = 0.6321205588285577
ETA_EFF = 0.46694220692425986
BETA = 2.620866911333223e-17
C_EFF = 0.9577022026205613
A_BLEED = 1.046973630587551
B_IN = 0.7879407922764435
A_IN = 1.6668538450045731
CHAOS = -0.33102418261048183
P_NEW = 0.30030227667037146
C_FACTOR = 0.28760015181918397
POOF = 0.1534822148944508
THETA_S = 0.29089654054517305
SUCTION = 0.14703398542810284
P_VAR = 0.9579871226722757
GAMMA_EULER = 0.5772156649
PHI = 1.6180339887
PI = math.pi

BOOT_D_EFF = 8.0
BOOT_DELTA_PSI = 0.7
BOOT_RECENT_HITS = 0.0
BOOT_OBSERVED = True
BOOT_SCALAR = 0.09928895626861721


def compute_fsot_scalar(d_eff: float, delta_psi: float, observed: bool, recent_hits: float) -> float:
    n = 1.0
    p = 1.0
    d = max(d_eff, 1.0)
    dp = delta_psi
    hits = recent_hits

    growth = math.exp(ALPHA * (1.0 - hits / n) * GAMMA_EULER / PHI)
    base = (
        (n * p / math.sqrt(d))
        * math.cos((PSI_CON + dp) / ETA_EFF)
        * math.exp(-ALPHA * hits / n + 1.0 + B_IN * dp)
        * (1.0 + growth * C_EFF)
    )
    t1 = base * (1.0 + P_NEW * math.log(d / 25.0))
    if observed:
        t1 = t1 * math.exp(C_FACTOR * P_VAR) * math.cos(dp + P_VAR)

    t2 = 0.0

    valve = (
        BETA
        * math.cos(dp)
        * (n * p / math.sqrt(d))
        * (1.0 + CHAOS * (d - 25.0) / 25.0)
        * (1.0 + POOF * math.cos(THETA_S + PI) + SUCTION * math.sin(THETA_S))
    )
    acoustic = 1.0 + (A_BLEED * math.sin(1.0) ** 2) / PHI + (A_IN * math.cos(1.0) ** 2) / PHI
    phase = 1.0 + B_IN * P_VAR
    t3 = valve * acoustic * phase

    return K * (t1 + t2 + t3)


def boot_scalar() -> float:
    return compute_fsot_scalar(BOOT_D_EFF, BOOT_DELTA_PSI, BOOT_OBSERVED, BOOT_RECENT_HITS)


def load_summary() -> dict:
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def refresh_summary_boot_scalar() -> dict:
    summary = load_summary()
    s = boot_scalar()
    summary["boot_scalar"] = s
    summary["boot_scalar_positive"] = s > 0.0
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def run_cargo_runtime_parity() -> dict:
    cargo = shutil.which("cargo")
    if not cargo:
        return {"status": "skipped", "reason": "cargo not on PATH"}
    if not (KERNEL_DIR / "tests" / "runtime_parity.rs").exists():
        return {"status": "failed", "reason": "missing runtime_parity tests"}
    try:
        r = subprocess.run(
            [cargo, "test", "--quiet"],
            cwd=str(KERNEL_DIR),
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return {
            "status": "passed" if r.returncode == 0 else "failed",
            "tool": cargo,
            "crate": "fsot_scalar_kernel",
            "test_file": "runtime_parity.rs",
            "returncode": r.returncode,
            "stderr_tail": out[-2000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}