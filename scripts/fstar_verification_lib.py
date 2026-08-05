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


def _fstar_runs(exe: str | Path) -> bool:
    """True if the binary is a real Win32 app that at least answers --version."""
    try:
        r = subprocess.run(
            [str(exe), "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # WinError 193 often surfaces as FileNotFoundError/OSError before run
        return r.returncode == 0 or "F*" in ((r.stdout or "") + (r.stderr or ""))
    except OSError:
        return False
    except Exception:
        return False


def resolve_fstar_exe() -> str | None:
    """Prefer local working installs; skip broken PATH / removable-drive stubs (WinError 193)."""
    candidates: list[Path] = []
    home = os.environ.get("FSTAR_HOME")
    if home:
        candidates.append(Path(home) / "bin" / "fstar.exe")
    candidates.extend(
        [
            Path.home() / "tools" / "fstar-v2026.07.05" / "bin" / "fstar.exe",
            ROOT / "tools" / "fstar" / "bin" / "fstar.exe",
        ]
    )
    try:
        from tool_path_lib import find_fstar  # noqa: WPS433

        hit = find_fstar()
        if hit:
            candidates.append(Path(hit))
    except Exception:
        pass
    for name in ("fstar.exe", "fstar"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    root = fstar_install_root(require=False)
    if root is not None:
        candidates.append(root / "bin" / "fstar.exe")
    candidates.append(Path(r"I:\FSOT-Physical-Archive\07_Portable-Toolchain\fstar\bin\fstar.exe"))

    seen: set[str] = set()
    for cand in candidates:
        key = str(cand)
        if key in seen or not cand.exists():
            continue
        seen.add(key)
        if _fstar_runs(cand):
            return str(cand)
    return None


def run_fstar_verify() -> dict:
    fstar = resolve_fstar_exe()
    if not fstar:
        return {
            "status": "skipped",
            "reason": "no working fstar.exe (PATH may point at broken I: archive binary)",
        }
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
    except OSError as e:
        # Broken PE / wrong architecture on PATH
        return {"status": "skipped", "reason": f"fstar not executable: {e}"}
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