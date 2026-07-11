"""Resolve Living FSOT project paths and shared hardware verification helpers."""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "living_fsot_project_manifest.yaml"


def _yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def resolve_living_root(explicit: str | Path | None = None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.exists() else None
    doc = _yaml(MANIFEST)
    default = doc.get("default_root") or ""
    if default:
        p = Path(default)
        if p.exists():
            return p
    for candidate in (
        Path(r"C:\Users\damia\Desktop\living fsot\files-e5887462"),
        Path.home() / "Desktop" / "living fsot" / "files-e5887462",
    ):
        if candidate.exists():
            return candidate
    return None


def living_paths(root: Path) -> dict[str, Path]:
    doc = _yaml(MANIFEST)
    comps = doc.get("components") or {}
    out: dict[str, Path] = {"root": root}
    for key, cfg in comps.items():
        rel = (cfg or {}).get("rel")
        if rel:
            out[key] = root / rel
    return out


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def qemu_available() -> tuple[bool, str | None]:
    for name in ("qemu-system-x86_64", "qemu-system-x86_64.exe"):
        found = shutil.which(name)
        if found:
            return True, found
    for base in (
        Path(r"C:\Program Files\qemu"),
        Path(r"C:\Program Files\QEMU"),
    ):
        exe = base / "qemu-system-x86_64.exe"
        if exe.exists():
            return True, str(exe)
    return False, None


def living_rust_k() -> float:
    """Recompute FSOT k from living-rust scalar.rs constants (f64)."""
    phi = 1.618033988749895
    e = math.e
    pi = math.pi
    sqrt2 = math.sqrt(2.0)
    perceived_param_base = 0.5772156649015329 / e
    return phi * (perceived_param_base * sqrt2) / math.log(pi) * 0.99


def canonical_k() -> float | None:
    doc = load_json(ROOT / "data" / "canonical_constants.json")
    if not doc:
        return None
    try:
        return float((doc.get("layer2") or {})["k"])
    except (KeyError, TypeError, ValueError):
        return None


def k_parity_check(tolerance: float = 1e-12) -> dict[str, Any]:
    ck = canonical_k()
    lk = living_rust_k()
    if ck is None:
        return {"ok": False, "reason": "canonical_k_missing"}
    delta = abs(lk - ck)
    rel = delta / abs(ck) if ck else delta
    return {
        "ok": delta <= tolerance or rel <= 1e-14,
        "canonical_k": ck,
        "living_rust_k": lk,
        "abs_delta": delta,
        "rel_delta": rel,
    }