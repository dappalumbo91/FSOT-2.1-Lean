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
  python scripts/run_fsot_reality_os.py hardware
  python scripts/run_fsot_reality_os.py rebuild   # math audit + atlas DB
  python scripts/run_fsot_reality_os.py audit     # complete system audit

Bare-metal / QEMU path remains verification/rust/fsot_scalar_kernel +
scripts/run_fsot_hardware_bare_metal.py — this CLI is the host OS of the fabric.
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
    hardware_status,
    hierarchy_head,
    list_interfaces,
    neighbors,
    predict_demo,
    residual_predict,
    snapshot,
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


def cmd_hardware(_: argparse.Namespace) -> int:
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
            },
            indent=2,
        )
    )
    return 0


def cmd_rebuild(_: argparse.Namespace) -> int:
    steps = [
        ["build_fsot_system_math_audit.py"],
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


def main() -> int:
    p = argparse.ArgumentParser(description="FSOT Reality OS — singular complete-engine runtime")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("boot", help="Print Reality OS boot banner").set_defaults(func=cmd_boot)
    sub.add_parser("snapshot", help="JSON fabric snapshot").set_defaults(func=cmd_snapshot)
    sub.add_parser("atlas-stats", help="SQLite atlas stats").set_defaults(func=cmd_atlas)
    sub.add_parser("hardware", help="Rust/QEMU/trinary path status").set_defaults(func=cmd_hardware)
    sub.add_parser("hierarchy", help="Building-block hierarchy head").set_defaults(func=cmd_hierarchy)
    sub.add_parser("rebuild", help="Rebuild math audit + atlas DB + system audit").set_defaults(func=cmd_rebuild)
    sub.add_parser("audit", help="Run complete system connective audit").set_defaults(func=cmd_audit)

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
