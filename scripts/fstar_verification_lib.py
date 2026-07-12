"""Tier 86 F* verification helpers."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import fstar_install_root  # noqa: E402

FSTAR_DIR = ROOT / "verification" / "fstar"
BOOT_MODULE = FSTAR_DIR / "FSOTScalarBoot.fst"


def resolve_fstar_exe() -> str | None:
    for name in ("fstar.exe", "fstar"):
        found = shutil.which(name)
        if found:
            return found
    root = fstar_install_root(require=False)
    if root is not None:
        candidate = root / "bin" / "fstar.exe"
        if candidate.exists():
            return str(candidate)
    return None


def run_fstar_verify() -> dict:
    fstar = resolve_fstar_exe()
    if not fstar:
        return {"status": "skipped", "reason": "fstar not on PATH and FSTAR_HOME missing"}
    if not BOOT_MODULE.exists():
        return {"status": "failed", "reason": f"missing {BOOT_MODULE}"}
    try:
        r = subprocess.run(
            [fstar, "--include", str(FSTAR_DIR), str(BOOT_MODULE)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = (r.stdout or "") + (r.stderr or "")
        verified = "Verified module: FSOTScalarBoot" in out and r.returncode == 0
        return {
            "status": "passed" if verified else "failed",
            "tool": fstar,
            "entry": str(BOOT_MODULE),
            "modules": ["FSOTScalarKernel", "FSOTScalarBoot"],
            "returncode": r.returncode,
            "stderr_tail": out[-3000:],
        }
    except Exception as e:
        return {"status": "failed", "reason": str(e)}


def parse_fstar_constants() -> dict[str, float]:
    kernel = FSTAR_DIR / "FSOTScalarKernel.fst"
    text = kernel.read_text(encoding="utf-8")
    out: dict[str, float] = {}
    for name in (
        "k_fsot",
        "boot_d_eff",
        "boot_delta_psi",
        "boot_scalar_canonical",
    ):
        m = re.search(rf"let {name}\s*:\s*real\s*=\s*([0-9.]+)R", text)
        if m:
            out[name] = float(m.group(1))
    return out