#!/usr/bin/env python3
"""Complete FSOT system connective audit — reorient to the whole engine.

Not a free-color tunnel. Inventory every major layer and flag buried/missing
connective pieces so the reality OS can sit on a coherent fabric.

Outputs:
  data/fsot_complete_system_audit.json
  docs/FSOT_COMPLETE_SYSTEM_AUDIT.md
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "data" / "fsot_complete_system_audit.json"
OUT_DOC = ROOT / "docs" / "FSOT_COMPLETE_SYSTEM_AUDIT.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def _json(rel: str) -> dict[str, Any] | None:
    p = ROOT / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _count_glob(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def audit() -> dict[str, Any]:
    layers: list[dict[str, Any]] = []

    def layer(id_: str, title: str, status: str, pieces: list[dict[str, Any]], note: str = "") -> None:
        layers.append(
            {
                "id": id_,
                "title": title,
                "status": status,
                "pieces": pieces,
                "note": note,
            }
        )

    # --- L0 Engine ---
    pin = _json("vendor/fsot_compute_AUTHORITY_PIN.json") or {}
    try:
        from fsot_compute import DOMAINS, domain_scalar, compute_scalar  # noqa: F401

        n_core = len(DOMAINS)
        engine_ok = True
        s_part = float(domain_scalar("Particle_Physics"))
        s_cos = float(domain_scalar("Cosmology"))
    except Exception as exc:  # noqa: BLE001
        n_core = 0
        engine_ok = False
        s_part = s_cos = None
        pin = {"error": str(exc)}

    layer(
        "L0_engine",
        "Scalar engine (authority)",
        "ok" if engine_ok else "broken",
        [
            {"path": "vendor/fsot_compute.py", "role": "S=K(T1+T2+T3) seeds L0–L2, 35 cores"},
            {"path": "vendor/fsot_compute_AUTHORITY_PIN.json", "role": "pin", "data": pin},
            {"path": "vendor/fsot_dynamics.py", "role": "T2 fluid continuum"},
            {"path": "vendor/fsot_gr_sm.py", "role": "GR/SM force package"},
            {"path": "vendor/fsot_seed_flavor.py", "role": "CKM/mass seed ladder"},
            {"path": "vendor/fsot_ckm_pmns.py", "role": "CKM/PMNS suite"},
            {"path": "scripts/fsot_api_predict_lib.py", "role": "fsot_scaled residual law"},
            {"path": "verification/rust/fsot_scalar_kernel", "role": "no_std Rust scalar port"},
        ],
        note=f"core_domains={n_core} S_particle={s_part} S_cosmo={s_cos}",
    )

    # --- L1 Domains full ---
    math_audit = _json("data/fsot_system_math_audit.json") or {}
    counts = math_audit.get("counts") or {}
    layer(
        "L1_interfaces",
        "Domain interfaces (core + expansion)",
        "ok" if (counts.get("total_domain_interfaces") or 0) >= 400 else "thin",
        [
            {"path": "data/fsot_system_math_audit.json", "role": "live S all interfaces"},
            {"path": "data/extension_domains_manifest.yaml", "role": "371 extensions"},
            {"path": "data/publication/domain_atlas.csv", "role": "publication atlas"},
            {"path": "data/fsot_building_block_hierarchy.json", "role": "hierarchy graph"},
            {"path": "data/fsot_domain_formula_network.json", "role": "network strings"},
        ],
        note=str(counts),
    )

    # --- L2 Residual atlas ---
    margin = _json("data/benchmark_margin_audit.json") or {}
    layer(
        "L2_residual_atlas",
        "Empirical residual atlas (green gates)",
        "ok" if (margin.get("green_gate_fail_count") or 0) == 0 and margin else "gap",
        [
            {
                "path": "data/benchmark_margin_audit.json",
                "green": margin.get("green_gate_pass_count"),
                "files": margin.get("benchmark_file_count"),
                "fails": margin.get("green_gate_fail_count"),
            },
            {"path": "data/fsot_atlas.sqlite", "role": "queryable atlas DB"},
            {"path": "data/*benchmark*.json", "count": _count_glob("data/*benchmark*.json")},
        ],
    )

    # --- L3 Formal multiprover ---
    cross = _json("data/cross_proof_verification_report.json") or {}
    grsm = _json("data/gr_sm_ckm_verification_report.json") or {}
    uniq = _json("data/uniqueness_research_verification_report.json") or {}
    layer(
        "L3_formal",
        "Multiprover / formal spines",
        "ok" if cross.get("overall_ok") else "check",
        [
            {
                "path": "data/cross_proof_verification_report.json",
                "overall_ok": cross.get("overall_ok"),
                "github_ready": cross.get("github_ready"),
            },
            {"path": "data/gr_sm_ckm_verification_report.json", "overall_ok": grsm.get("overall_ok")},
            {
                "path": "data/uniqueness_research_verification_report.json",
                "overall_ok": uniq.get("overall_ok"),
                "note": "one research spine among many — not the whole ToE",
            },
            {"path": "verification/obligations/", "role": "exported spines"},
            {"path": "FSOT/Formal/", "lean_count": _count_glob("FSOT/Formal/*.lean")},
        ],
    )

    # --- L4 Waves buried in fsot_compute ---
    compute_path = ROOT / "vendor" / "fsot_compute.py"
    wave_names = []
    if compute_path.exists():
        text = compute_path.read_text(encoding="utf-8", errors="replace")
        for name in (
            "wave1",
            "wave2",
            "wave3",
            "wave10",
            "validation_suite",
            "lepton_ratios",
            "chemistry_electronegativity",
            "dynamical_systems",
        ):
            if f"def {name}" in text:
                wave_names.append(name)
    layer(
        "L4_buried_waves",
        "Seed derivation waves in fsot_compute (must stay connected)",
        "ok" if wave_names else "gap",
        [{"function": n, "path": "vendor/fsot_compute.py"} for n in wave_names]
        + [
            {
                "role": "already_surfaced_panels",
                "examples": [
                    "eta_baryon_photon → matter_antimatter",
                    "Omega_b_h2 → matter_antimatter + cosmology",
                    "alpha_s / H0 / T_CMB → wave1 cosmology residual lineage",
                ],
            }
        ],
        note="Waves are formula inventory — residual panels should map back so nothing stays orphaned.",
    )

    # --- L5 Sectors (balanced) ---
    sectors = [
        ("particle_sm", ["data/particle_physics_benchmark.json", "data/pdg_particle_properties_benchmark.json", "data/toe_ckm_pmns_benchmark.json"]),
        ("matter_antimatter", ["data/matter_antimatter_benchmark.json", "docs/MATTER_ANTIMATTER.md"]),
        ("cosmology", ["data/cosmology_extended_benchmark.json", "data/toe_contested_sector_refresh.json"]),
        ("gr_sm", ["data/toe_gr_sm_deep_benchmark.json", "data/toe_limit_recovery_benchmark.json"]),
        ("open_science", ["data/open_frontier_wave1_report.json", "docs/OPEN_SCIENCE_NEW_FRONTIERS.md"]),
        ("intelligence", ["data/intelligence_compression_benchmark.json"]),
        ("hardware", [
            "verification/rust/fsot_scalar_kernel",
            "verification/rust/fsot_hardware_kernel",
            "verification/qemu",
            "vendor/trinary_os",
            "vendor/trinary_hardware",
            "scripts/run_fsot_hardware_bare_metal.py",
            "scripts/living_fsot_lib.py",
        ]),
        ("dynamics_fluid", ["vendor/fsot_dynamics.py", "data/toe_dynamics_benchmark.json"]),
    ]
    sector_pieces = []
    for sid, paths in sectors:
        present = sum(1 for p in paths if _exists(p))
        sector_pieces.append(
            {
                "sector": sid,
                "present": present,
                "total": len(paths),
                "status": "ok" if present == len(paths) else ("partial" if present else "missing"),
                "paths": paths,
            }
        )
    layer(
        "L5_sectors",
        "Scientific + hardware sectors (balanced inventory)",
        "ok",
        sector_pieces,
        note="All sectors matter equally for the reality OS — no single research track owns the ToE.",
    )

    # --- L6 Atlas DB ---
    atlas_stats: dict[str, Any] = {"exists": _exists("data/fsot_atlas.sqlite")}
    if atlas_stats["exists"]:
        try:
            conn = sqlite3.connect(ROOT / "data" / "fsot_atlas.sqlite")
            tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            atlas_stats["tables"] = tables
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
                    atlas_stats[t] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            conn.close()
        except Exception as exc:  # noqa: BLE001
            atlas_stats["error"] = str(exc)
    has_math = (atlas_stats.get("engine_seeds") or 0) > 0
    layer(
        "L6_atlas_db",
        "SQLite atlas (must hold residuals AND engine math)",
        "ok" if has_math else "needs_rebuild",
        [atlas_stats],
        note="Rebuild with scripts/build_fsot_atlas_sqlite.py after math audit so engine_seeds/interfaces exist.",
    )

    # --- L7 Reality OS / condensation ---
    layer(
        "L7_reality_os",
        "Singular runtime (condense the mess)",
        "ok" if _exists("scripts/run_fsot_reality_os.py") else "scaffolding",
        [
            {"path": "scripts/run_fsot_reality_os.py", "role": "single CLI entry"},
            {"path": "vendor/fsot_reality_os.py", "role": "library core"},
            {"path": "verification/rust/fsot_scalar_kernel", "role": "bare-metal scalar path"},
            {"path": "verification/qemu", "role": "QEMU hardware verification"},
            {"path": "data/reality_building_blocks_simulation.json", "role": "hierarchy sim state"},
        ],
        note="Goal: one program that runs the complete engine + atlas connectives, path to OS of reality.",
    )

    # Connective gaps (honest, broad)
    gaps = []
    if not has_math:
        gaps.append(
            {
                "id": "atlas_missing_engine_math_tables",
                "severity": "high",
                "fix": "Rebuild atlas SQLite to include seeds/derived/interfaces/edges",
            }
        )
    if not _exists("scripts/run_fsot_reality_os.py"):
        gaps.append(
            {
                "id": "no_singular_reality_os_cli",
                "severity": "high",
                "fix": "Create run_fsot_reality_os.py consolidating engine+atlas+hardware status",
            }
        )
    # Wave inventory without dedicated residual panels
    gaps.append(
        {
            "id": "wave_inventory_connection",
            "severity": "medium",
            "fix": (
                "Ensure fsot_compute wave* Results are either residual panels or explicit "
                "inventory rows in atlas formulas — avoid orphan wave numbers."
            ),
        }
    )
    if (margin.get("green_gate_fail_count") or 0) > 0:
        gaps.append({"id": "green_fails", "severity": "high", "fix": "Close green residual fails"})

    # Buried good pieces to keep visible
    connectives_ok = [
        "Seeds → domain_scalar → fsot_scaled → green benchmarks",
        "Extension folds → core factors",
        "GR/SM multiprover + scientific catalog multiprover",
        "Fluid dynamics T2 + cosmology S damping + particle S emergence",
        "Matter/antimatter duals + η/Ω_b seeds",
        "Rust scalar kernel + QEMU/hardware path",
        "Hierarchy network + building-blocks simulation",
    ]

    status = "COHERENT"
    if any(g["severity"] == "high" for g in gaps):
        status = "NEEDS_CONNECTIVE_WORK"
    if not engine_ok:
        status = "ENGINE_BROKEN"

    return {
        "generated_at": _now(),
        "version": "1.0",
        "status": status,
        "orientation": (
            "Full FSOT fabric: one fluid spacetime engine, residual atlas, multiprover, "
            "hardware path. Research tracks (uniqueness, etc.) are leaves — not the trunk."
        ),
        "master_formula": "S = K*(T1+T2+T3); c = m*(1+|S|*f)",
        "layers": layers,
        "connectives_ok": connectives_ok,
        "gaps": gaps,
        "commands": {
            "math_audit": "python scripts/build_fsot_system_math_audit.py",
            "atlas_rebuild": "python scripts/build_fsot_atlas_sqlite.py",
            "reality_os": "python scripts/run_fsot_reality_os.py",
            "margins": "python scripts/audit_all_benchmark_margins.py",
            "building_blocks_sim": "python scripts/run_reality_building_blocks_simulation.py",
        },
    }


def write_doc(doc: dict) -> None:
    lines = [
        "# FSOT complete system audit",
        "",
        f"**Status:** `{doc['status']}`  ",
        f"**Generated:** {doc['generated_at']}",
        "",
        doc["orientation"],
        "",
        f"**Master formula:** `{doc['master_formula']}`",
        "",
        "## Layers",
        "",
    ]
    for lay in doc["layers"]:
        lines.append(f"### {lay['id']} — {lay['title']} [{lay['status']}]")
        lines.append("")
        if lay.get("note"):
            lines.append(lay["note"])
            lines.append("")
        for p in lay.get("pieces") or []:
            lines.append(f"- `{json.dumps(p, default=str)[:200]}`")
        lines.append("")
    lines += ["## Connectives OK", ""]
    for c in doc["connectives_ok"]:
        lines.append(f"- {c}")
    lines += ["", "## Gaps / connective work", ""]
    if not doc["gaps"]:
        lines.append("- None flagged.")
    for g in doc["gaps"]:
        lines.append(f"- **{g['severity']}** `{g['id']}`: {g['fix']}")
    lines += ["", "## Commands", ""]
    for k, v in (doc.get("commands") or {}).items():
        lines.append(f"- **{k}:** `{v}`")
    lines.append("")
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    doc = audit()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_doc(doc)
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_DOC}")
    print(f"  status={doc['status']} layers={len(doc['layers'])} gaps={len(doc['gaps'])}")
    return 0 if doc["status"] != "ENGINE_BROKEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
