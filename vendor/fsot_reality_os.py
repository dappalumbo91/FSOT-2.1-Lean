#!/usr/bin/env python3
"""FSOT Reality OS — singular runtime over the complete engine.

Condenses the atlas of scripts/panels into one library that:

  - runs the seed scalar engine (authority: fsot_compute)
  - routes residual predictions (fsot_api_predict_lib)
  - reads domain interfaces + connectives from the atlas SQLite
  - reports hardware/QEMU/Rust path status
  - exposes hierarchy / building-block ladder

This is the software kernel of an “operating system of reality”:
one process, one formula fabric, many dimensional interfaces.

Bare-metal path: verification/rust/fsot_scalar_kernel + QEMU/hardware kits.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

ATLAS = ROOT / "data" / "fsot_atlas.sqlite"
MATH_AUDIT = ROOT / "data" / "fsot_system_math_audit.json"
SIM = ROOT / "data" / "reality_building_blocks_simulation.json"


@dataclass
class RealityState:
    """Snapshot of the OS of reality fabric."""

    pin: str
    master_formula: str
    core_domains: int
    extension_domains: int
    green_panels: int
    atlas_records: int
    engine_interfaces: int
    connective_edges: int
    hardware: dict[str, Any]
    ontology: str = "fluid_spacetime_omni_D_eff_ceiling_25"


def _f(x: Any) -> float:
    return float(x)


def compute_domain_S(domain: str) -> float:
    from fsot_compute import domain_scalar

    return _f(domain_scalar(domain))


def compute_S_raw(
    d_eff: float,
    delta_psi: float = 1.0,
    observed: bool = True,
    recent_hits: float = 0.0,
    delta_theta: float = 1.0,
) -> float:
    from fsot_compute import ScalarInput, compute_scalar
    from mpmath import mpf

    si = ScalarInput(
        N=mpf(1),
        P=mpf(1),
        D_eff=mpf(d_eff),
        delta_psi=mpf(delta_psi),
        delta_theta=mpf(delta_theta),
        recent_hits=mpf(recent_hits),
        observed=observed,
        rho=mpf(1),
        scale=mpf(1),
        amplitude=mpf(1),
    )
    return _f(compute_scalar(si))


def residual_predict(measured: float, domain: str) -> tuple[float, float]:
    from fsot_api_predict_lib import fsot_scaled

    return fsot_scaled(measured, domain)


def atlas_connect() -> sqlite3.Connection | None:
    if not ATLAS.exists():
        return None
    return sqlite3.connect(str(ATLAS))


def atlas_stats() -> dict[str, Any]:
    conn = atlas_connect()
    if conn is None:
        return {"exists": False}
    cur = conn.cursor()
    out: dict[str, Any] = {"exists": True}
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    out["tables"] = tables
    for t in (
        "domains",
        "records",
        "formulas",
        "engine_seeds",
        "engine_derived",
        "domain_interfaces",
        "connective_edges",
    ):
        if t in tables:
            out[t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    meta = dict(cur.execute("SELECT key, value FROM meta").fetchall())
    out["meta"] = meta
    conn.close()
    return out


def list_interfaces(kind: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    conn = atlas_connect()
    if conn is None:
        # fallback math audit
        if not MATH_AUDIT.exists():
            return []
        audit = json.loads(MATH_AUDIT.read_text(encoding="utf-8"))
        rows = audit.get("domains") or []
        if kind:
            rows = [r for r in rows if r.get("kind") == kind]
        return rows[:limit]
    cur = conn.cursor()
    if kind:
        cur.execute(
            "SELECT domain, kind, d_eff, s_scalar, sign, band, domain_factor_f "
            "FROM domain_interfaces WHERE kind=? ORDER BY d_eff, domain LIMIT ?",
            (kind, limit),
        )
    else:
        cur.execute(
            "SELECT domain, kind, d_eff, s_scalar, sign, band, domain_factor_f "
            "FROM domain_interfaces ORDER BY d_eff, domain LIMIT ?",
            (limit,),
        )
    cols = [d[0] for d in cur.description]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    conn.close()
    return rows


def neighbors(domain: str, limit: int = 20) -> list[dict[str, Any]]:
    conn = atlas_connect()
    if conn is None:
        return []
    cur = conn.cursor()
    cur.execute(
        "SELECT src, dst, rel, weight FROM connective_edges "
        "WHERE src=? OR dst=? ORDER BY weight DESC LIMIT ?",
        (domain, domain, limit),
    )
    rows = [
        {"src": a, "dst": b, "rel": r, "weight": w}
        for a, b, r, w in cur.fetchall()
    ]
    conn.close()
    return rows


def hardware_status() -> dict[str, Any]:
    from living_fsot_lib import qemu_available

    q_ok, q_path = qemu_available()
    return {
        "qemu_available": q_ok,
        "qemu_path": q_path,
        "rust_scalar_kernel": (ROOT / "verification/rust/fsot_scalar_kernel").exists(),
        "rust_hardware_kernel": (ROOT / "verification/rust/fsot_hardware_kernel").exists(),
        "qemu_dir": (ROOT / "verification/qemu").exists(),
        "trinary_os": (ROOT / "vendor/trinary_os").exists(),
        "trinary_hardware": (ROOT / "vendor/trinary_hardware").exists(),
        "bare_metal_runner": (ROOT / "scripts/run_fsot_hardware_bare_metal.py").exists(),
        "path_note": (
            "Host Reality OS uses Python authority engine; bare-metal path is "
            "fsot_scalar_kernel (no_std) + QEMU/ESP32 kits."
        ),
    }


def pin_prefix() -> str:
    p = ROOT / "vendor/fsot_compute_AUTHORITY_PIN.json"
    if not p.exists():
        return "unknown"
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        return str(doc.get("pin") or doc.get("sha256_prefix") or doc)[:16]
    except Exception:
        return "unknown"


def snapshot() -> RealityState:
    stats = atlas_stats()
    math = {}
    if MATH_AUDIT.exists():
        math = json.loads(MATH_AUDIT.read_text(encoding="utf-8"))
    counts = math.get("counts") or {}
    margin = {}
    mp = ROOT / "data/benchmark_margin_audit.json"
    if mp.exists():
        margin = json.loads(mp.read_text(encoding="utf-8"))
    return RealityState(
        pin=pin_prefix(),
        master_formula="S = K*(T1+T2+T3); c = m*(1+|S|*f)",
        core_domains=int(counts.get("core_domains") or 35),
        extension_domains=int(counts.get("extension_domains") or 0),
        green_panels=int(margin.get("green_gate_pass_count") or stats.get("domains") or 0),
        atlas_records=int(stats.get("records") or 0),
        engine_interfaces=int(stats.get("domain_interfaces") or counts.get("total_domain_interfaces") or 0),
        connective_edges=int(stats.get("connective_edges") or 0),
        hardware=hardware_status(),
    )


def boot_message() -> str:
    st = snapshot()
    lines = [
        "FSOT Reality OS",
        f"  pin={st.pin}",
        f"  formula={st.master_formula}",
        f"  ontology={st.ontology}",
        f"  interfaces={st.engine_interfaces} (core={st.core_domains} ext={st.extension_domains})",
        f"  green_panels={st.green_panels} atlas_records={st.atlas_records}",
        f"  connective_edges={st.connective_edges}",
        f"  qemu={st.hardware.get('qemu_available')} rust_kernel={st.hardware.get('rust_scalar_kernel')}",
    ]
    return "\n".join(lines)


def predict_demo(domain: str = "Planetary_Science", measured: float = 1.0) -> dict[str, Any]:
    s = compute_domain_S(domain)
    c, err = residual_predict(measured, domain)
    return {
        "domain": domain,
        "S": s,
        "measured": measured,
        "computed": c,
        "error_pct": err,
        "law": "c = m * (1 + |S| * f_domain)",
    }


def hierarchy_head(n: int = 10) -> list[dict[str, Any]]:
    if SIM.exists():
        doc = json.loads(SIM.read_text(encoding="utf-8"))
        return (doc.get("hierarchy_ladder_head") or [])[:n]
    return list_interfaces(limit=n)
