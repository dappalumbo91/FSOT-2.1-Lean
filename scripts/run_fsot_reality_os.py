#!/usr/bin/env python3
"""FSOT Reality OS CLI — singular entry to the complete engine.

Condense scripts/panels into one running program:

  python scripts/run_fsot_reality_os.py boot
  python scripts/run_fsot_reality_os.py S Particle_Physics
  python scripts/run_fsot_reality_os.py predict Planetary_Science 2.77
  python scripts/run_fsot_reality_os.py interfaces --kind core
  python scripts/run_fsot_reality_os.py neighbors Cosmology
  python scripts/run_fsot_reality_os.py hierarchy
  python scripts/run_fsot_reality_os.py atlas-stats
  python scripts/run_fsot_reality_os.py hardware          # inventory Rust/QEMU spine
  python scripts/run_fsot_reality_os.py hardware --run    # EXECUTE bare-metal + QEMU
  python scripts/run_fsot_reality_os.py rebuild   # math audit + atlas DB
  python scripts/run_fsot_reality_os.py audit     # complete system audit

OS execution spine (not optional later): verification/rust/fsot_scalar_kernel +
fsot_hardware_kernel + vendor/rust_lean_bridge + verification/qemu, driven by
scripts/run_fsot_hardware_bare_metal.py and run_rust_lean_bridge_qemu_harness.py.
Python residual CLI is formula authority only — not the operating system.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_reality_os import (  # noqa: E402
    atlas_stats,
    boot_message,
    compute_domain_S,
    compute_S_raw,
    coverage_checklist,
    derived_table,
    hardware_status,
    run_hardware_spine,
    hierarchy_head,
    list_interfaces,
    matter_dual_status,
    multiprover_status,
    neighbors,
    predict_demo,
    quantum_depth_status,
    quantum_status,
    reality_syntax_rules,
    residual_predict,
    sector_coverage,
    seeds_table,
    snapshot,
    trinary_syntax_status,
)


def cmd_boot(_: argparse.Namespace) -> int:
    print(boot_message())
    return 0


def cmd_S(args: argparse.Namespace) -> int:
    if args.domain:
        s = compute_domain_S(args.domain)
        print(json.dumps({"domain": args.domain, "S": s}, indent=2))
    else:
        s = compute_S_raw(args.d_eff, args.delta_psi, not args.unobserved, args.hits)
        print(
            json.dumps(
                {
                    "D_eff": args.d_eff,
                    "delta_psi": args.delta_psi,
                    "observed": not args.unobserved,
                    "hits": args.hits,
                    "S": s,
                },
                indent=2,
            )
        )
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    if args.domain and args.measured is not None:
        c, err = residual_predict(float(args.measured), args.domain)
        s = compute_domain_S(args.domain)
        print(
            json.dumps(
                {
                    "domain": args.domain,
                    "S": s,
                    "measured": float(args.measured),
                    "computed": c,
                    "error_pct": err,
                    "law": "c = m * (1 + |S| * f)",
                },
                indent=2,
            )
        )
    else:
        print(json.dumps(predict_demo(), indent=2))
    return 0


def cmd_interfaces(args: argparse.Namespace) -> int:
    rows = list_interfaces(kind=args.kind, limit=args.limit)
    print(json.dumps({"count": len(rows), "interfaces": rows}, indent=2))
    return 0


def cmd_neighbors(args: argparse.Namespace) -> int:
    print(json.dumps({"domain": args.domain, "neighbors": neighbors(args.domain, args.limit)}, indent=2))
    return 0


def cmd_hierarchy(_: argparse.Namespace) -> int:
    print(json.dumps({"hierarchy_head": hierarchy_head(15)}, indent=2))
    return 0


def cmd_atlas(_: argparse.Namespace) -> int:
    print(json.dumps(atlas_stats(), indent=2))
    return 0


def cmd_hardware(args: argparse.Namespace) -> int:
    if getattr(args, "run", False):
        doc = run_hardware_spine(skip_qemu=bool(getattr(args, "skip_qemu", False)))
        print(json.dumps(doc, indent=2))
        return 0 if doc.get("overall_ok") else 1
    print(json.dumps(hardware_status(), indent=2))
    return 0


def cmd_snapshot(_: argparse.Namespace) -> int:
    st = snapshot()
    print(
        json.dumps(
            {
                "pin": st.pin,
                "master_formula": st.master_formula,
                "ontology": st.ontology,
                "core_domains": st.core_domains,
                "extension_domains": st.extension_domains,
                "green_panels": st.green_panels,
                "atlas_records": st.atlas_records,
                "engine_interfaces": st.engine_interfaces,
                "connective_edges": st.connective_edges,
                "hardware": st.hardware,
                "quantum": {
                    "core_count": (st.quantum or {}).get("core_count"),
                    "extension_count": (st.quantum or {}).get("extension_count"),
                    "green_panel_count": (st.quantum or {}).get("green_panel_count"),
                    "all_green": (st.quantum or {}).get("all_green"),
                    "live_core_S": (st.quantum or {}).get("live_core_S"),
                },
                "multiprover": st.multiprover,
            },
            indent=2,
        )
    )
    return 0


def cmd_rebuild(_: argparse.Namespace) -> int:
    steps = [
        ["build_fsot_system_math_audit.py"],
        ["build_quantum_trinary_syntax_benchmark.py"],
        ["run_reality_building_blocks_simulation.py"],
        ["build_fsot_atlas_sqlite.py"],
        ["audit_fsot_complete_system.py"],
    ]
    for script in steps:
        path = ROOT / "scripts" / script[0]
        print(f"=== {script[0]} ===")
        r = subprocess.run([sys.executable, str(path)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED {script[0]}", file=sys.stderr)
            return r.returncode
    print(boot_message())
    return 0


def cmd_audit(_: argparse.Namespace) -> int:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "audit_fsot_complete_system.py")],
        cwd=str(ROOT),
    )
    return r.returncode


def cmd_quantum(_: argparse.Namespace) -> int:
    print(json.dumps(quantum_status(), indent=2))
    return 0


def cmd_dual(_: argparse.Namespace) -> int:
    print(json.dumps(matter_dual_status(), indent=2))
    return 0


def cmd_matter(args: argparse.Namespace) -> int:
    # alias of dual + particle S
    out = matter_dual_status()
    try:
        out["S_particle"] = compute_domain_S("Particle_Physics")
        out["S_nuclear"] = compute_domain_S("Nuclear_Physics")
        out["S_quantum"] = compute_domain_S("Quantum_Mechanics")
    except Exception as exc:  # noqa: BLE001
        out["live_S_error"] = str(exc)
    print(json.dumps(out, indent=2))
    return 0


def cmd_multiprover(_: argparse.Namespace) -> int:
    print(json.dumps(multiprover_status(), indent=2))
    return 0


def cmd_sectors(_: argparse.Namespace) -> int:
    print(json.dumps(sector_coverage(), indent=2))
    return 0


def cmd_coverage(_: argparse.Namespace) -> int:
    print(json.dumps(coverage_checklist(), indent=2))
    return 0


def cmd_rules(_: argparse.Namespace) -> int:
    print(json.dumps({"reality_syntax_rules": reality_syntax_rules()}, indent=2))
    return 0


def cmd_seeds(args: argparse.Namespace) -> int:
    out: dict = {"seeds": seeds_table()}
    if args.derived:
        out["derived"] = derived_table(args.layer)
    print(json.dumps(out, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="FSOT Reality OS — singular complete-engine runtime")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("boot", help="Print Reality OS boot banner").set_defaults(func=cmd_boot)
    sub.add_parser("snapshot", help="JSON fabric snapshot").set_defaults(func=cmd_snapshot)
    sub.add_parser("atlas-stats", help="SQLite atlas stats").set_defaults(func=cmd_atlas)
    hw = sub.add_parser(
        "hardware",
        help="Rust/QEMU OS spine inventory; use --run to execute bare-metal + QEMU",
    )
    hw.add_argument(
        "--run",
        action="store_true",
        help="Execute fsot_hardware_bare_metal + rust_lean_bridge QEMU harness",
    )
    hw.add_argument(
        "--skip-qemu",
        action="store_true",
        help="With --run: only host Rust hardware kernel tests (no QEMU)",
    )
    hw.set_defaults(func=cmd_hardware)
    sub.add_parser("hierarchy", help="Building-block hierarchy head").set_defaults(func=cmd_hierarchy)
    sub.add_parser("rebuild", help="Rebuild math audit + atlas DB + system audit").set_defaults(func=cmd_rebuild)
    sub.add_parser("audit", help="Run complete system connective audit").set_defaults(func=cmd_audit)
    sub.add_parser("quantum", help="Quantum mechanics/science coverage + live S").set_defaults(func=cmd_quantum)

    def _cmd_qdepth(_: argparse.Namespace) -> int:
        print(json.dumps(quantum_depth_status(), indent=2))
        return 0

    def _cmd_trinary(_: argparse.Namespace) -> int:
        print(json.dumps(trinary_syntax_status(), indent=2))
        return 0

    sub.add_parser("quantum-depth", help="Entanglement/QI depth + unified suite").set_defaults(func=_cmd_qdepth)
    sub.add_parser("trinary", help="Trinary OS string syntax (opcodes, trit=sign S)").set_defaults(func=_cmd_trinary)
    sub.add_parser("syntax", help="Alias of trinary (reality string language)").set_defaults(func=_cmd_trinary)
    sub.add_parser("dual", help="Matter/antimatter conjugate duals + eta").set_defaults(func=cmd_dual)
    sub.add_parser("matter", help="Matter sector (particle/nuclear/QM + duals)").set_defaults(func=cmd_matter)
    sub.add_parser("multiprover", help="Cross-proof / GR-SM multiprover status").set_defaults(func=cmd_multiprover)
    sub.add_parser("sectors", help="All fabric sectors mapped into Reality OS").set_defaults(func=cmd_sectors)
    sub.add_parser("coverage", help="Not-missing checklist for Reality OS").set_defaults(func=cmd_coverage)
    sub.add_parser("rules", help="Reality syntax rules from building-blocks sim").set_defaults(func=cmd_rules)

    sp_seeds = sub.add_parser("seeds", help="Engine seeds (+ optional derived stack)")
    sp_seeds.add_argument("--derived", action="store_true", help="Include L1/L2 derived constants")
    sp_seeds.add_argument("--layer", type=int, default=None, help="Filter derived layer 1 or 2")
    sp_seeds.set_defaults(func=cmd_seeds)

    sp = sub.add_parser("S", help="Compute domain or raw S")
    sp.add_argument("domain", nargs="?", help="Named core domain")
    sp.add_argument("--d-eff", type=float, default=12.0)
    sp.add_argument("--delta-psi", type=float, default=1.0)
    sp.add_argument("--hits", type=float, default=0.0)
    sp.add_argument("--unobserved", action="store_true")
    sp.set_defaults(func=cmd_S)

    pp = sub.add_parser("predict", help="Residual prediction c=m(1+|S|f)")
    pp.add_argument("domain", nargs="?", default="Planetary_Science")
    pp.add_argument("measured", nargs="?", type=float, default=1.0)
    pp.set_defaults(func=cmd_predict)

    ip = sub.add_parser("interfaces", help="List domain interfaces from atlas")
    ip.add_argument("--kind", choices=["core", "extension"], default=None)
    ip.add_argument("--limit", type=int, default=40)
    ip.set_defaults(func=cmd_interfaces)

    np_ = sub.add_parser("neighbors", help="Connective neighbors of a domain")
    np_.add_argument("domain")
    np_.add_argument("--limit", type=int, default=20)
    np_.set_defaults(func=cmd_neighbors)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
