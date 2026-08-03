"""Resolve local verification tools (Z3, CVC5, TLC, F*) from repo tools/ or PATH."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
TOOL_PATHS = TOOLS / "tool_paths.json"


def _load_map() -> dict:
    if TOOL_PATHS.exists():
        try:
            return json.loads(TOOL_PATHS.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def find_z3() -> str | None:
    m = _load_map()
    if m.get("z3") and Path(m["z3"]).exists():
        return m["z3"]
    for name in ("z3", "z3.exe"):
        p = shutil.which(name)
        if p:
            return p
    hits = list(TOOLS.glob("z3/**/z3.exe"))
    return str(hits[0]) if hits else None


def find_cvc5() -> str | None:
    m = _load_map()
    if m.get("cvc5") and Path(m["cvc5"]).exists():
        return m["cvc5"]
    for name in ("cvc5", "cvc5.exe"):
        p = shutil.which(name)
        if p:
            return p
    hits = list(TOOLS.glob("cvc5/**/cvc5.exe"))
    return str(hits[0]) if hits else None


def find_tla2tools_jar() -> str | None:
    m = _load_map()
    if m.get("tla2tools_jar") and Path(m["tla2tools_jar"]).exists():
        return m["tla2tools_jar"]
    jar = TOOLS / "tla" / "tla2tools.jar"
    return str(jar) if jar.exists() else None


def find_fstar() -> str | None:
    m = _load_map()
    if m.get("fstar_exe") and Path(m["fstar_exe"]).exists():
        return m["fstar_exe"]
    for name in ("fstar.exe", "fstar"):
        p = shutil.which(name)
        if p:
            return p
    home = os.environ.get("FSTAR_HOME")
    if home:
        cand = Path(home) / "bin" / "fstar.exe"
        if cand.exists():
            return str(cand)
    for cand in (
        Path(r"I:\FSOT-Physical-Archive\07_Portable-Toolchain\fstar\bin\fstar.exe"),
        Path.home() / "tools" / "fstar-v2026.07.05" / "bin" / "fstar.exe",
        TOOLS / "fstar" / "bin" / "fstar.exe",
    ):
        if cand.exists():
            return str(cand)
    return None
