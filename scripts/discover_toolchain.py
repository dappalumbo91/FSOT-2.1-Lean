#!/usr/bin/env python3
"""Discover proof-assistant toolchains (host + I: portable bundle)."""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "data" / "toolchain_discovery.json"


def _archive_root() -> Path | None:
    from fsot_paths import archive_root  # noqa: WPS433

    return archive_root()


def _bundled(name: str) -> Path | None:
    ar = _archive_root()
    if ar is None:
        return None
    p = ar / "07_Portable-Toolchain" / name
    return p if p.is_dir() else None


def _find_coq() -> str | None:
    bundled = _bundled("rocq")
    if bundled is not None:
        for name in ("coqc.exe", "coqc"):
            hit = bundled / "bin" / name
            if hit.exists():
                return str(hit)
    for name in ("coqc.exe", "coqc", "rocqc.exe", "rocqc"):
        p = shutil.which(name)
        if p:
            return p
    for base in (
        Path(r"C:\Rocq-Platform~9.0~2025.08"),
        Path(r"C:\Program Files\Rocq Platform"),
    ):
        if base is None or not base.exists():
            continue
        for name in ("coqc.exe", "coqc"):
            for exe in base.rglob(name):
                return str(exe)
    return None


def _find_isabelle() -> dict | None:
    roots: list[Path] = []
    b = _bundled("isabelle")
    if b is not None:
        roots.append(b)
    roots.extend([Path(r"C:\Users\damia\Desktop\Isabelle2025-2"), Path(r"C:\Isabelle")])
    for root in roots:
        if root is None or not root.exists():
            continue
        bash = root / "contrib" / "cygwin" / "bin" / "bash.exe"
        isabelle_sh = root / "bin" / "isabelle"
        if bash.exists() and isabelle_sh.exists():
            return {"home": str(root), "mode": "cygwin", "bash": str(bash), "tool": str(isabelle_sh)}
        for exe in root.rglob("isabelle.exe"):
            return {"home": str(root), "mode": "posix", "tool": str(exe)}
    p = shutil.which("isabelle")
    if p:
        return {"mode": "posix", "tool": p}
    return None


def _find_fstar() -> str | None:
    from fsot_paths import fstar_install_root  # noqa: WPS433

    b = _bundled("fstar")
    if b is not None:
        hit = b / "bin" / "fstar.exe"
        if hit.exists():
            return str(hit)
    for name in ("fstar.exe", "fstar"):
        p = shutil.which(name)
        if p:
            return p
    root = fstar_install_root(require=False)
    if root is not None:
        candidate = root / "bin" / "fstar.exe"
        if candidate.exists():
            return str(candidate)
    return None


def _find_rust_tool(name: str) -> str | None:
    b = _bundled("cargo")
    if b is not None:
        hit = b / "bin" / f"{name}.exe"
        if hit.exists():
            return str(hit)
    return shutil.which(name)


def _find_elan_tool(name: str) -> str | None:
    b = _bundled("elan")
    if b is not None:
        hit = b / "bin" / f"{name}.exe"
        if hit.exists():
            return str(hit)
    return shutil.which(name)


def discover() -> dict:
    ar = _archive_root()
    bundled = ar / "07_Portable-Toolchain" if ar else None
    bundled_items = []
    if bundled and bundled.exists():
        bundled_items = sorted(p.name for p in bundled.iterdir() if p.is_dir())
    tools = {
        "python": shutil.which("python"),
        "lake": _find_elan_tool("lake"),
        "elan": _find_elan_tool("elan"),
        "coqc": _find_coq(),
        "isabelle": _find_isabelle(),
        "fstar": _find_fstar(),
        "rustc": _find_rust_tool("rustc"),
        "cargo": _find_rust_tool("cargo"),
    }
    return {
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(ar) if ar else None,
        "bundled_toolchain_root": str(bundled) if bundled and bundled.exists() else None,
        "bundled_items": bundled_items,
        "tools": tools,
        "all_seven_way_present": all(
            [
                tools["coqc"],
                tools["isabelle"],
                tools["fstar"],
                tools["lake"],
                tools["cargo"],
                tools["python"],
            ]
        ),
    }


def main() -> int:
    doc = discover()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())