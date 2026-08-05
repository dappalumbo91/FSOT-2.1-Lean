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
MATTER = ROOT / "data" / "matter_antimatter_research.json"
CROSS = ROOT / "data" / "cross_proof_verification_report.json"
GRSM = ROOT / "data" / "gr_sm_ckm_verification_report.json"
COMPLETE = ROOT / "data" / "fsot_complete_system_audit.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"

# Core + known quantum / sector tags for Reality OS coverage map
SECTOR_MAP: dict[str, dict[str, Any]] = {
    "engine": {
        "title": "Scalar engine + residual law",
        "paths": [
            "vendor/fsot_compute.py",
            "scripts/fsot_api_predict_lib.py",
            "vendor/fsot_dynamics.py",
        ],
        "reality_os": ["S", "predict", "seeds", "boot"],
    },
    "quantum": {
        "title": "Quantum mechanics / information / optics / gravity / entanglement",
        "core_domains": [
            "Quantum_Mechanics",
            "Quantum_Computing",
            "Quantum_Optics",
            "Quantum_Gravity",
        ],
        "extension_patterns": ["Quantum_", "quantum_"],
        "paths": [
            "data/quantum_mechanics_entanglement_depth_panel_benchmark.json",
            "data/quantum_information_benchmark.json",
            "data/quantum_trinary_syntax_benchmark.json",
            "vendor/fsot_quantum_trinary_syntax.py",
        ],
        "reality_os": ["quantum", "quantum-depth", "S", "predict", "interfaces"],
    },
    "trinary_syntax": {
        "title": "Trinary string language (Metatron opcodes / trit = sign(S))",
        "paths": [
            "vendor/trinary_os/isa/fsotb_opcode_registry.json",
            "data/trinary_os_tier_e_benchmark.json",
            "data/quantum_trinary_syntax_benchmark.json",
            "vendor/fsot_quantum_trinary_syntax.py",
        ],
        "reality_os": ["trinary", "syntax", "quantum-depth"],
    },
    "particle_nuclear": {
        "title": "Particle / nuclear / high energy",
        "core_domains": ["Particle_Physics", "Nuclear_Physics", "High_Energy_Physics", "Atomic_Physics"],
        "reality_os": ["S", "predict", "sectors"],
    },
    "matter_antimatter": {
        "title": "Matter / antimatter duals + baryon asymmetry",
        "paths": ["vendor/fsot_matter_antimatter.py", "data/matter_antimatter_benchmark.json"],
        "reality_os": ["dual", "matter"],
    },
    "cosmology_astro": {
        "title": "Cosmology / astronomy / planetary",
        "core_domains": ["Cosmology", "Astronomy", "Astrophysics", "Planetary_Science", "Particle_Astrophysics"],
        "reality_os": ["S", "hierarchy", "neighbors"],
    },
    "gr_sm": {
        "title": "GR recovery + SM force package + CKM/PMNS",
        "paths": ["vendor/fsot_gr_sm.py", "vendor/fsot_ckm_pmns.py", "data/gr_sm_ckm_verification_report.json"],
        "reality_os": ["multiprover", "snapshot"],
    },
    "life_mind": {
        "title": "Biology / neuroscience / intelligence",
        "core_domains": ["Biology", "Neuroscience", "Psychology", "Biochemistry"],
        "paths": ["data/intelligence_compression_benchmark.json"],
        "reality_os": ["S", "interfaces"],
    },
    "earth_climate": {
        "title": "Earth / climate / fluids",
        "core_domains": ["Meteorology", "Oceanography", "Seismology", "Geophysics", "Fluid_Dynamics", "Atmospheric_Physics"],
        "reality_os": ["S", "interfaces"],
    },
    "open_science": {
        "title": "Open residual atlas panels",
        "paths": ["data/fsot_atlas.sqlite", "data/benchmark_margin_audit.json"],
        "reality_os": ["atlas-stats", "interfaces"],
    },
    "connective_hierarchy": {
        "title": "Building-block hierarchy + network strings",
        "paths": [
            "data/fsot_building_block_hierarchy.json",
            "data/fsot_domain_formula_network.json",
            "data/reality_building_blocks_simulation.json",
        ],
        "reality_os": ["hierarchy", "neighbors", "rules"],
    },
    "formal_multiprover": {
        "title": "Lean/Coq/Isabelle/SMT multiprover",
        "paths": ["data/cross_proof_verification_report.json", "verification/obligations/"],
        "reality_os": ["multiprover"],
    },
    "hardware_bare_metal": {
        "title": "Rust scalar kernel + QEMU + trinary OS",
        "paths": [
            "verification/rust/fsot_scalar_kernel",
            "verification/qemu",
            "vendor/trinary_os",
            "scripts/run_fsot_hardware_bare_metal.py",
        ],
        "reality_os": ["hardware"],
    },
}


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
    quantum: dict[str, Any] | None = None
    multiprover: dict[str, Any] | None = None
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
    """Inventory of the *real* OS execution path (Rust + QEMU), not a Python stand-in.

    Python residual CLI is the formula shell only. The OS spine lives under
    verification/rust/* + vendor/rust_lean_bridge + verification/qemu and is
    exercised by run_fsot_hardware_bare_metal / run_rust_lean_bridge_qemu_harness.
    """
    from living_fsot_lib import qemu_available

    q_ok, q_path = qemu_available()
    crates = {
        "fsot_scalar_kernel": ROOT / "verification/rust/fsot_scalar_kernel",
        "fsot_hardware_kernel": ROOT / "verification/rust/fsot_hardware_kernel",
        "fsot_observer_serial": ROOT / "verification/rust/fsot_observer_serial",
        "fsot_obligation_replay": ROOT / "verification/rust/fsot_obligation_replay",
        "rust_lean_bridge": ROOT / "vendor/rust_lean_bridge",
    }
    runners = {
        "bare_metal": ROOT / "scripts/run_fsot_hardware_bare_metal.py",
        "qemu_harness": ROOT / "scripts/run_rust_lean_bridge_qemu_harness.py",
        "esp32_observer": ROOT / "verification/esp32/fsot_esp32_observer",
    }
    present = {k: p.exists() for k, p in crates.items()}
    runner_ok = {k: p.exists() for k, p in runners.items()}
    spine_ready = (
        q_ok
        and present.get("fsot_scalar_kernel")
        and present.get("fsot_hardware_kernel")
        and present.get("rust_lean_bridge")
        and runner_ok.get("bare_metal")
        and runner_ok.get("qemu_harness")
        and (ROOT / "verification/qemu").exists()
    )
    return {
        "os_spine": "rust_qemu",
        "formula_shell": "python_pin_D1D38A",
        "spine_ready": spine_ready,
        "qemu_available": q_ok,
        "qemu_path": q_path,
        "crates": {k: str(p) for k, p in crates.items()},
        "crates_present": present,
        "runners": {k: str(p) for k, p in runners.items()},
        "runners_present": runner_ok,
        "qemu_dir": str(ROOT / "verification/qemu"),
        "qemu_dir_present": (ROOT / "verification/qemu").exists(),
        "trinary_os": (ROOT / "vendor/trinary_os").exists(),
        "trinary_hardware": (ROOT / "vendor/trinary_hardware").exists(),
        "path_note": (
            "Reality OS execution spine = Rust no_std scalar/hardware kernels + "
            "QEMU disk/serial harness (already in this monorepo). Python is residual "
            "authority only — not the OS. Run: python scripts/run_fsot_reality_os.py hardware --run"
        ),
    }


def run_hardware_spine(*, skip_qemu: bool = False) -> dict[str, Any]:
    """Execute monorepo Rust processor gates + QEMU harness (the real OS path)."""
    import subprocess
    import sys

    status = hardware_status()
    results: dict[str, Any] = {
        "os_spine": "rust_qemu",
        "inventory": status,
        "steps": {},
    }
    if not status.get("spine_ready") and not status.get("crates_present", {}).get(
        "fsot_hardware_kernel"
    ):
        results["overall_ok"] = False
        results["reason"] = "Rust/QEMU spine crates missing from monorepo"
        return results

    steps = [
        ("bare_metal", ROOT / "scripts/run_fsot_hardware_bare_metal.py"),
    ]
    if not skip_qemu:
        steps.append(
            ("qemu_harness", ROOT / "scripts/run_rust_lean_bridge_qemu_harness.py")
        )

    all_ok = True
    for name, script in steps:
        if not script.exists():
            results["steps"][name] = {"status": "missing", "path": str(script)}
            all_ok = False
            continue
        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=900,
            )
            results["steps"][name] = {
                "status": "passed" if proc.returncode == 0 else "failed",
                "returncode": proc.returncode,
                "stdout_tail": (proc.stdout or "")[-1500:],
                "stderr_tail": (proc.stderr or "")[-800:],
            }
            if proc.returncode != 0:
                all_ok = False
        except Exception as exc:  # noqa: BLE001
            results["steps"][name] = {"status": "error", "error": str(exc)}
            all_ok = False

    results["overall_ok"] = all_ok
    results["command"] = "python scripts/run_fsot_reality_os.py hardware --run"
    return results


def pin_prefix() -> str:
    p = ROOT / "vendor/fsot_compute_AUTHORITY_PIN.json"
    if not p.exists():
        return "unknown"
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        for key in ("pin", "sha256_prefix", "authority_pin", "authority_sha256", "sha256", "prefix"):
            if doc.get(key):
                val = str(doc[key])
                # Prefer short pin style (first 6 hex) for banner
                if len(val) >= 6 and key in ("authority_sha256", "sha256"):
                    return val[:6].upper()
                return val[:32]
        return "D1D38A"
    except Exception:
        return "unknown"


def seeds_table() -> list[dict[str, Any]]:
    conn = atlas_connect()
    if conn is not None:
        cur = conn.cursor()
        try:
            rows = cur.execute("SELECT id, symbol, value, role, code FROM engine_seeds").fetchall()
            conn.close()
            if rows:
                return [
                    {"id": a, "symbol": b, "value": c, "role": d, "code": e}
                    for a, b, c, d, e in rows
                ]
        except Exception:
            conn.close()
    if MATH_AUDIT.exists():
        audit = json.loads(MATH_AUDIT.read_text(encoding="utf-8"))
        return list((audit.get("seeds") or {}).get("nodes") or [])
    return []


def derived_table(layer: int | None = None) -> list[dict[str, Any]]:
    conn = atlas_connect()
    if conn is None:
        return []
    cur = conn.cursor()
    try:
        if layer is None:
            rows = cur.execute(
                "SELECT id, layer, formula, value, role, section FROM engine_derived ORDER BY layer, id"
            ).fetchall()
        else:
            rows = cur.execute(
                "SELECT id, layer, formula, value, role, section FROM engine_derived WHERE layer=? ORDER BY id",
                (layer,),
            ).fetchall()
        conn.close()
        return [
            {"id": a, "layer": b, "formula": c, "value": d, "role": e, "section": f}
            for a, b, c, d, e, f in rows
        ]
    except Exception:
        conn.close()
        return []


def quantum_status() -> dict[str, Any]:
    """Quantum mechanics / science coverage inside Reality OS fabric."""
    cores = []
    extensions = []
    green_panels = []
    conn = atlas_connect()
    if conn is not None:
        cur = conn.cursor()
        try:
            for row in cur.execute(
                "SELECT domain, kind, d_eff, s_scalar, sign, domain_factor_f "
                "FROM domain_interfaces WHERE domain LIKE '%Quantum%' OR domain LIKE '%quantum%' "
                "ORDER BY d_eff, domain"
            ):
                rec = {
                    "domain": row[0],
                    "kind": row[1],
                    "D_eff": row[2],
                    "S": row[3],
                    "sign": row[4],
                    "f": row[5],
                }
                if row[1] == "core":
                    cores.append(rec)
                else:
                    extensions.append(rec)
            for row in cur.execute(
                "SELECT domain, file_name, green_gate_pass, pooled_median_error_pct, scalar_count "
                "FROM domains WHERE lower(domain) LIKE '%quantum%' OR lower(file_name) LIKE '%quantum%' "
                "ORDER BY domain"
            ):
                green_panels.append(
                    {
                        "domain": row[0],
                        "file": row[1],
                        "green": bool(row[2]),
                        "pooled_median_error_pct": row[3],
                        "scalar_count": row[4],
                    }
                )
        finally:
            conn.close()
    # Live S for primary QM
    try:
        s_qm = compute_domain_S("Quantum_Mechanics")
        s_qc = compute_domain_S("Quantum_Computing")
        s_qo = compute_domain_S("Quantum_Optics")
        s_qg = compute_domain_S("Quantum_Gravity")
        live = {
            "Quantum_Mechanics": s_qm,
            "Quantum_Computing": s_qc,
            "Quantum_Optics": s_qo,
            "Quantum_Gravity": s_qg,
        }
    except Exception as exc:  # noqa: BLE001
        live = {"error": str(exc)}

    return {
        "covered": True,
        "note": (
            "Quantum is first-class in FSOT: core interfaces Quantum_Mechanics (D=6 emergence), "
            "Quantum_Optics, Quantum_Computing, Quantum_Gravity + extension panels "
            "(information, materials, entanglement depth, vacuum, microtubule). "
            "Same residual law as every other domain — not a separate bolted theory."
        ),
        "live_core_S": live,
        "core_interfaces": cores,
        "extension_interfaces": extensions,
        "green_residual_panels": green_panels,
        "core_count": len(cores),
        "extension_count": len(extensions),
        "green_panel_count": len(green_panels),
        "all_green": all(p.get("green") for p in green_panels) if green_panels else False,
    }


def matter_dual_status() -> dict[str, Any]:
    out: dict[str, Any] = {"available": MATTER.exists()}
    if MATTER.exists():
        doc = json.loads(MATTER.read_text(encoding="utf-8"))
        out["summary"] = doc.get("summary") or doc.get("summary_physics") or doc
        out["benchmark"] = "data/matter_antimatter_benchmark.json"
    try:
        from fsot_matter_antimatter import (  # type: ignore
            antimatter_conjugate_S,
            matter_S,
            seed_eta_baryon_photon,
            seed_Omega_b_h2,
        )

        out["live"] = {
            "S_matter": matter_S("Particle_Physics"),
            "S_conjugate": antimatter_conjugate_S("Particle_Physics"),
            "eta": seed_eta_baryon_photon(),
            "Omega_b_h2": seed_Omega_b_h2(),
        }
    except Exception as exc:  # noqa: BLE001
        out["live_error"] = str(exc)
    return out


def multiprover_status() -> dict[str, Any]:
    out: dict[str, Any] = {}
    if CROSS.exists():
        c = json.loads(CROSS.read_text(encoding="utf-8"))
        out["cross_proof"] = {
            "overall_ok": c.get("overall_ok"),
            "github_ready": c.get("github_ready"),
            "generated_at": c.get("generated_at"),
        }
    if GRSM.exists():
        g = json.loads(GRSM.read_text(encoding="utf-8"))
        out["gr_sm_ckm"] = {
            "overall_ok": g.get("overall_ok"),
            "obligation_count": g.get("obligation_count"),
        }
    uniq = ROOT / "data/uniqueness_research_verification_report.json"
    if uniq.exists():
        u = json.loads(uniq.read_text(encoding="utf-8"))
        out["uniqueness_research"] = {
            "overall_ok": u.get("overall_ok"),
            "obligation_count": u.get("obligation_count"),
            "note": "research leaf — not trunk",
        }
    return out


def reality_syntax_rules() -> list[dict[str, Any]]:
    if SIM.exists():
        doc = json.loads(SIM.read_text(encoding="utf-8"))
        return list(doc.get("reality_syntax_rules") or [])
    return []


def sector_coverage() -> dict[str, Any]:
    """Map every major fabric sector into Reality OS commands + path presence."""
    sectors = {}
    for sid, spec in SECTOR_MAP.items():
        paths = spec.get("paths") or []
        cores = spec.get("core_domains") or []
        path_ok = sum(1 for p in paths if (ROOT / p).exists()) if paths else None
        core_ok = 0
        core_detail = []
        for d in cores:
            try:
                s = compute_domain_S(d)
                core_ok += 1
                core_detail.append({"domain": d, "S": s})
            except Exception:
                core_detail.append({"domain": d, "S": None, "error": "missing"})
        sectors[sid] = {
            "title": spec.get("title"),
            "reality_os_commands": spec.get("reality_os") or [],
            "paths_present": path_ok,
            "paths_total": len(paths) if paths else 0,
            "core_domains_ok": core_ok,
            "core_domains_total": len(cores),
            "core_live": core_detail,
            "status": (
                "ok"
                if (path_ok is None or path_ok == len(paths))
                and (not cores or core_ok == len(cores))
                else "partial"
            ),
        }
    q = quantum_status()
    sectors["quantum"]["quantum_detail"] = {
        "core_count": q.get("core_count"),
        "extension_count": q.get("extension_count"),
        "green_panel_count": q.get("green_panel_count"),
        "all_green": q.get("all_green"),
        "note": q.get("note"),
    }
    return {
        "sectors": sectors,
        "missing_or_thin": [k for k, v in sectors.items() if v["status"] != "ok"],
        "orientation": (
            "Reality OS is the host kernel of the full fabric. "
            "Quantum, particle, cosmo, life, hardware are all first-class interfaces — "
            "not optional add-ons."
        ),
    }


def coverage_checklist() -> dict[str, Any]:
    """Explicit not-missing list for Reality OS vs whole program."""
    q = quantum_status()
    st = snapshot()
    items = [
        {"id": "engine_S", "present": True, "via": "S / predict"},
        {"id": "seeds_L0", "present": len(seeds_table()) >= 5, "via": "seeds"},
        {"id": "derived_L1_L2", "present": len(derived_table()) >= 10, "via": "seeds --derived"},
        {"id": "core_35", "present": st.core_domains >= 35, "via": "interfaces --kind core"},
        {"id": "extensions_300plus", "present": st.extension_domains >= 300, "via": "interfaces --kind extension"},
        {"id": "green_atlas", "present": st.green_panels >= 400, "via": "atlas-stats"},
        {"id": "quantum_core", "present": (q.get("core_count") or 0) >= 4, "via": "quantum"},
        {"id": "quantum_extensions", "present": (q.get("extension_count") or 0) >= 3, "via": "quantum"},
        {"id": "quantum_green_panels", "present": (q.get("green_panel_count") or 0) >= 5, "via": "quantum"},
        {
            "id": "quantum_trinary_unified_panel",
            "present": (ROOT / "data/quantum_trinary_syntax_benchmark.json").exists(),
            "via": "quantum-depth / trinary",
        },
        {
            "id": "trinary_opcode_abi",
            "present": (ROOT / "vendor/trinary_os/isa/fsotb_opcode_registry.json").exists(),
            "via": "trinary",
        },
        {"id": "matter_antimatter", "present": MATTER.exists(), "via": "dual"},
        {"id": "hierarchy_sim", "present": SIM.exists(), "via": "hierarchy / rules"},
        {"id": "connective_edges", "present": st.connective_edges > 1000, "via": "neighbors"},
        {"id": "multiprover", "present": CROSS.exists(), "via": "multiprover"},
        {"id": "hardware_qemu_rust", "present": bool(st.hardware.get("qemu_available") and st.hardware.get("rust_scalar_kernel")), "via": "hardware"},
        {"id": "complete_system_audit", "present": COMPLETE.exists(), "via": "audit"},
    ]
    missing = [i for i in items if not i["present"]]
    return {
        "items": items,
        "present_count": sum(1 for i in items if i["present"]),
        "missing_count": len(missing),
        "missing": missing,
        "complete": len(missing) == 0,
    }


def snapshot() -> RealityState:
    stats = atlas_stats()
    math = {}
    if MATH_AUDIT.exists():
        math = json.loads(MATH_AUDIT.read_text(encoding="utf-8"))
    counts = math.get("counts") or {}
    margin = {}
    if MARGIN.exists():
        margin = json.loads(MARGIN.read_text(encoding="utf-8"))
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
        quantum=quantum_status(),
        multiprover=multiprover_status(),
    )


def boot_message() -> str:
    st = snapshot()
    q = st.quantum or {}
    lines = [
        "FSOT Reality OS",
        f"  pin={st.pin}",
        f"  formula={st.master_formula}",
        f"  ontology={st.ontology}",
        f"  interfaces={st.engine_interfaces} (core={st.core_domains} ext={st.extension_domains})",
        f"  green_panels={st.green_panels} atlas_records={st.atlas_records}",
        f"  connective_edges={st.connective_edges}",
        f"  quantum_cores={q.get('core_count')} quantum_ext={q.get('extension_count')} "
        f"quantum_green={q.get('green_panel_count')} all_green={q.get('all_green')}",
        f"  qemu={st.hardware.get('qemu_available')} rust_kernel={st.hardware.get('rust_scalar_kernel')}",
        f"  multiprover_ok={(st.multiprover or {}).get('cross_proof', {}).get('overall_ok')}",
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


def quantum_depth_status() -> dict[str, Any]:
    """Entanglement / QI depth + live residual panel if built."""
    out: dict[str, Any] = {
        "base_quantum": quantum_status(),
        "related_panels": [],
    }
    for rel in (
        "data/quantum_mechanics_entanglement_depth_panel_benchmark.json",
        "data/quantum_information_benchmark.json",
        "data/quantum_computing_math_depth_panel_benchmark.json",
        "data/quantum_trinary_syntax_benchmark.json",
    ):
        p = ROOT / rel
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            out["related_panels"].append(
                {
                    "path": rel,
                    "domain": d.get("domain"),
                    "pooled_median_error_pct": d.get("pooled_median_error_pct"),
                    "record_count": d.get("record_count"),
                }
            )
        except Exception:
            out["related_panels"].append({"path": rel, "error": "unreadable"})
    try:
        from fsot_quantum_trinary_syntax import suite_summary  # type: ignore

        out["unified_suite"] = suite_summary()
    except Exception as exc:  # noqa: BLE001
        out["unified_suite_error"] = str(exc)
    return out


def trinary_syntax_status() -> dict[str, Any]:
    """Trinary OS as string language of the continuum."""
    out: dict[str, Any] = {"available": True}
    reg_path = ROOT / "vendor/trinary_os/isa/fsotb_opcode_registry.json"
    if reg_path.exists():
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        out["abi"] = {
            "opcodes": len(reg.get("opcodes") or []),
            "word_width_trits": reg.get("word_width_trits"),
            "register_count": reg.get("register_count"),
            "cortical_layers": reg.get("cortical_layers"),
            "source": reg.get("source"),
        }
    try:
        from fsot_quantum_trinary_syntax import (  # type: ignore
            encode_string_from_domains,
            suite_summary,
        )

        enc = encode_string_from_domains(
            [
                "Particle_Physics",
                "Quantum_Mechanics",
                "Atomic_Physics",
                "Chemistry",
                "Biology",
                "Neuroscience",
                "Nuclear_Physics",
                "Astronomy",
                "Planetary_Science",
                "Cosmology",
            ]
        )
        out["reality_string"] = "".join(e["symbol"] for e in enc)
        out["encoding"] = enc
        out["suite"] = suite_summary()
        out["note"] = (
            "Balanced trit = sign(S): + emerge, 0 null, - damp. "
            "27 Metatron opcodes = 3³; 25 registers = D_eff ceiling. "
            "Same S as the residual atlas — machine syntax of fluid spacetime."
        )
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)
    for rel in (
        "data/trinary_os_tier_e_benchmark.json",
        "data/trinary_os_portable_benchmark.json",
        "data/quantum_trinary_syntax_benchmark.json",
    ):
        p = ROOT / rel
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            out.setdefault("panels", []).append(
                {
                    "path": rel,
                    "domain": d.get("domain"),
                    "pooled": d.get("pooled_median_error_pct"),
                    "records": d.get("record_count"),
                }
            )
    return out
