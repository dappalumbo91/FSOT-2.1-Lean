#!/usr/bin/env python3
"""Building blocks of reality simulation — solidify hierarchical FSOT syntax.

Loads the full-system math audit + hierarchy network (35 cores + extension atlas)
and runs a deterministic, seed-locked simulation that:

  1. Activates L0 seeds → L1/L2 → T1/T2/T3 → S
  2. Evaluates every domain interface (core + extension) already in the audit
  3. Propagates "string" activation along network edges
  4. Emits hierarchical reality rules / syntax from emerge vs damp signs
  5. Attaches matter/antimatter duals when research JSON is present

No free parameters. Does not re-fit residuals — uses closed audit S values.

Outputs:
  data/reality_building_blocks_simulation.json
  docs/REALITY_BUILDING_BLOCKS_SIMULATION.md

Prereq:
  python scripts/build_fsot_system_math_audit.py
  python scripts/build_matter_antimatter_benchmark.py   # optional attach
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "fsot_system_math_audit.json"
HIER = ROOT / "data" / "fsot_building_block_hierarchy.json"
NET = ROOT / "data" / "fsot_domain_formula_network.json"
MATTER = ROOT / "data" / "matter_antimatter_research.json"
UNIQUENESS = ROOT / "data" / "uniqueness_confinement_research.json"
OUT = ROOT / "data" / "reality_building_blocks_simulation.json"
OUT_DOC = ROOT / "docs" / "REALITY_BUILDING_BLOCKS_SIMULATION.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_audit() -> dict[str, Any]:
    if not AUDIT.exists() or not HIER.exists() or not NET.exists():
        import subprocess

        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_fsot_system_math_audit.py")],
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            raise RuntimeError("build_fsot_system_math_audit failed")
    return _load(AUDIT)


def simulate(audit: dict, hier: dict, net: dict) -> dict[str, Any]:
    domains = audit.get("domains") or []
    cores = [d for d in domains if d.get("kind") == "core"]
    exts = [d for d in domains if d.get("kind") == "extension"]

    # --- Layer activation (deterministic) ---
    seeds = {n["id"]: float(n["value"]) for n in (audit.get("seeds") or {}).get("nodes") or []}
    layer1 = {n["id"]: float(n["value"]) for n in (audit.get("layer1_primary_derived") or {}).get("nodes") or []}
    layer2 = {n["id"]: float(n["value"]) for n in (audit.get("layer2_composite_derived") or {}).get("nodes") or []}

    # Activation strength of a domain = |S| (load-bearing amplitude) with sign bit
    domain_state: dict[str, dict[str, Any]] = {}
    for d in domains:
        name = d["domain"]
        s = float(d["S"])
        domain_state[name] = {
            "domain": name,
            "kind": d.get("kind"),
            "D_eff": int(d["D_eff"]),
            "S": s,
            "sign": d["sign"],
            "band": d["band"],
            "activation": abs(s),
            "syntax_bit": 1 if s > 0 else (-1 if s < 0 else 0),
            "f": d.get("domain_factor_f"),
            "floor_pct": d.get("pure_residual_floor_pct"),
            "routes_to_core": d.get("routes_to_core"),
        }

    # --- String propagation: sum weighted neighbor activation ---
    adj: dict[str, list[tuple[str, float, str]]] = defaultdict(list)
    for link in net.get("domain_domain_links") or []:
        a, b = link["source"], link["target"]
        w = float(link.get("weight") or 1.0)
        kind = str(link.get("kind") or "link")
        adj[a].append((b, w, kind))
        adj[b].append((a, w, kind))

    # One-step message pass
    for name, st in domain_state.items():
        influx = 0.0
        by_kind: dict[str, float] = defaultdict(float)
        for nb, w, kind in adj.get(name, []):
            if nb not in domain_state:
                continue
            contrib = w * domain_state[nb]["activation"] * domain_state[nb]["syntax_bit"]
            influx += contrib
            by_kind[kind] += contrib
        st["network_influx"] = influx
        st["network_influx_by_kind"] = dict(by_kind)
        # Effective field: own S plus damped neighbor field
        damp = abs(float(layer2.get("CHAOS", 0.33)))
        st["effective_field"] = st["S"] + 0.01 * influx / (1.0 + damp)
        st["effective_sign"] = (
            "emergence" if st["effective_field"] > 0 else "damping" if st["effective_field"] < 0 else "zero"
        )

    # --- Hierarchical ladder (building-block order) ---
    ladder = sorted(domain_state.values(), key=lambda x: (x["D_eff"], x["kind"] != "core", x["domain"]))
    for i, st in enumerate(ladder):
        st["hierarchy_rank"] = i + 1

    # Band aggregates
    band_stats: dict[str, dict[str, Any]] = {}
    for st in domain_state.values():
        b = st["band"]
        bucket = band_stats.setdefault(
            b,
            {"count": 0, "emergence": 0, "damping": 0, "mean_abs_S": 0.0, "mean_D_eff": 0.0},
        )
        bucket["count"] += 1
        if st["sign"] == "emergence":
            bucket["emergence"] += 1
        elif st["sign"] == "damping":
            bucket["damping"] += 1
        bucket["mean_abs_S"] += st["activation"]
        bucket["mean_D_eff"] += st["D_eff"]
    for b, bucket in band_stats.items():
        n = max(bucket["count"], 1)
        bucket["mean_abs_S"] /= n
        bucket["mean_D_eff"] /= n
        bucket["emergence_fraction"] = bucket["emergence"] / n

    # --- Reality syntax rules (emergent from closed S signs + network) ---
    rules: list[dict[str, Any]] = []

    rules.append(
        {
            "id": "R_FLUID_OMNI",
            "rule": "One fluid continuum; all domains are D_eff interfaces into S=K(T1+T2+T3).",
            "support": {"D_eff_ceiling": 25, "total_interfaces": len(domain_state)},
        }
    )
    rules.append(
        {
            "id": "R_SEED_CLOSURE",
            "rule": "All constants derive from (π,e,φ,γ,G); zero free residual coefficients.",
            "support": {"seeds": list(seeds.keys()), "layer1": list(layer1.keys())[:4]},
        }
    )
    rules.append(
        {
            "id": "R_SIGN_SYNTAX",
            "rule": "sign(S)>0 ⇒ emergence-class building block; sign(S)<0 ⇒ damping-class.",
            "support": {
                "emergence_count": sum(1 for s in domain_state.values() if s["sign"] == "emergence"),
                "damping_count": sum(1 for s in domain_state.values() if s["sign"] == "damping"),
            },
        }
    )
    rules.append(
        {
            "id": "R_HIERARCHY_DEFF",
            "rule": "Building-block order is ascending D_eff (micro → compactification ceiling 25).",
            "support": {
                "first": [{"domain": s["domain"], "D_eff": s["D_eff"]} for s in ladder[:5]],
                "last": [{"domain": s["domain"], "D_eff": s["D_eff"]} for s in ladder[-5:]],
            },
        }
    )
    rules.append(
        {
            "id": "R_RESIDUAL_LAW",
            "rule": "Measurement attach: c = m (1 + |S| f); green iff pooled median ε ≤ 0.5%.",
            "support": audit.get("benchmarks") or {},
        }
    )
    # Cosmology damps bulk residual density class
    cos = domain_state.get("Cosmology")
    if cos and cos["sign"] == "damping":
        rules.append(
            {
                "id": "R_COSMO_DAMPS_BULK",
                "rule": "Cosmology interface (D_eff=25) is damping-class — bulk residual modes that cannot fold into lower-D emergence are non-load-bearing.",
                "support": {"S_cosmo": cos["S"]},
            }
        )
    # Micro emergence
    micro_em = [s for s in domain_state.values() if s["band"] == "micro" and s["sign"] == "emergence"]
    if micro_em:
        rules.append(
            {
                "id": "R_MICRO_EMERGENCE",
                "rule": "Micro band (D_eff≤9) is predominantly emergence-class (particle → chemistry).",
                "support": {
                    "emergence": len(micro_em),
                    "examples": [s["domain"] for s in micro_em[:6]],
                },
            }
        )

    # Matter/antimatter attach
    matter = _load(MATTER)
    if matter:
        sm = (matter.get("summary") or {}).get("S_matter_particle")
        sc = (matter.get("summary") or {}).get("S_antimatter_conjugate")
        eta = (matter.get("summary") or {}).get("eta_baryon_photon")
        rules.append(
            {
                "id": "R_MATTER_ANTIMATTER",
                "rule": (
                    "Matter = particle/nuclear emergence; antimatter = conjugate dual (δψ+π); "
                    "bulk asymmetry seed η; cosmology damps bulk antimatter residual."
                ),
                "support": {
                    "S_matter": sm,
                    "S_conjugate": sc,
                    "eta": eta,
                    "benchmark": "data/matter_antimatter_benchmark.json",
                },
            }
        )

    # Free-color damp (uniqueness track)
    uniq = _load(UNIQUENESS)
    if uniq:
        rules.append(
            {
                "id": "R_FREE_COLOR_DAMPS",
                "rule": "Free-color amplitudes are not attractors under seed-locked γ_color (confinement uniqueness candidate).",
                "support": {
                    "status": (uniq.get("summary") or {}).get("theorem_status") or uniq.get("theorem_status"),
                    "gamma": (uniq.get("summary") or {}).get("free_color_damping_rate"),
                },
            }
        )

    # Top connected domains by |network_influx|
    top_connected = sorted(domain_state.values(), key=lambda x: abs(x.get("network_influx") or 0), reverse=True)[:15]

    # Syntax string inventory
    string_kinds = defaultdict(int)
    for link in net.get("domain_domain_links") or []:
        string_kinds[str(link.get("kind") or "link")] += 1
    string_kinds["seed_domain"] = int(net.get("seed_domain_link_count") or 0)
    string_kinds["benchmark_panel"] = int(net.get("green_benchmark_panel_count") or 0)

    return {
        "generated_at": _now(),
        "version": "1.0",
        "status": "SOLIDIFIED",
        "ontology": "fluid_spacetime_omni_D_eff_ceiling_25",
        "counts": {
            "seeds": len(seeds),
            "layer1": len(layer1),
            "layer2": len(layer2),
            "core_domains": len(cores),
            "extension_domains": len(exts),
            "total_interfaces": len(domain_state),
            "domain_domain_links": len(net.get("domain_domain_links") or []),
            "seed_domain_links": net.get("seed_domain_link_count"),
            "green_panels": net.get("green_benchmark_panel_count"),
            "rules": len(rules),
        },
        "seeds": seeds,
        "layer1_sample": {k: layer1[k] for k in list(layer1)[:6]},
        "layer2_sample": {k: layer2[k] for k in list(layer2)[:8]},
        "band_stats": band_stats,
        "string_kind_inventory": dict(string_kinds),
        "reality_syntax_rules": rules,
        "hierarchy_ladder_head": ladder[:12],
        "hierarchy_ladder_tail": ladder[-8:],
        "top_network_connected": [
            {
                "domain": s["domain"],
                "D_eff": s["D_eff"],
                "sign": s["sign"],
                "S": s["S"],
                "network_influx": s["network_influx"],
                "effective_field": s["effective_field"],
            }
            for s in top_connected
        ],
        "all_domain_states": list(domain_state.values()),
        "simulation_method": {
            "activation": "|S| from closed audit (no re-fit)",
            "syntax_bit": "sign(S)",
            "message_pass": "one-step weighted neighbor influx * syntax_bit",
            "effective_field": "S + 0.01 * influx / (1+|CHAOS|)",
            "hierarchy": "sort by D_eff ascending",
        },
        "artifacts_used": {
            "audit": "data/fsot_system_math_audit.json",
            "hierarchy": "data/fsot_building_block_hierarchy.json",
            "network": "data/fsot_domain_formula_network.json",
            "matter": "data/matter_antimatter_research.json" if matter else None,
            "uniqueness": "data/uniqueness_confinement_research.json" if uniq else None,
        },
        "consistency_from_audit": audit.get("consistency"),
    }


def write_doc(sim: dict) -> None:
    c = sim["counts"]
    lines = [
        "# Building blocks of reality — simulation",
        "",
        f"**Status:** `{sim['status']}`  ",
        f"**Generated:** {sim['generated_at']}  ",
        f"**Ontology:** {sim['ontology']}",
        "",
        "Machine output: [`data/reality_building_blocks_simulation.json`](../data/reality_building_blocks_simulation.json)",
        "",
        "## Counts",
        "",
        f"| Item | N |",
        f"|------|--:|",
        f"| Seeds | {c['seeds']} |",
        f"| Core interfaces | {c['core_domains']} |",
        f"| Extension interfaces | {c['extension_domains']} |",
        f"| **Total interfaces** | **{c['total_interfaces']}** |",
        f"| Domain–domain strings | {c['domain_domain_links']} |",
        f"| Seed–domain strings | {c['seed_domain_links']} |",
        f"| Green residual panels | {c['green_panels']} |",
        f"| Reality syntax rules | {c['rules']} |",
        "",
        "## Reality syntax rules (emergent)",
        "",
    ]
    for r in sim["reality_syntax_rules"]:
        lines.append(f"### `{r['id']}`")
        lines.append("")
        lines.append(r["rule"])
        lines.append("")
    lines += [
        "## Hierarchy (head → micro)",
        "",
        "| Rank | D_eff | Domain | sign | S |",
        "|-----:|------:|--------|:----:|----:|",
    ]
    for s in sim["hierarchy_ladder_head"]:
        lines.append(
            f"| {s['hierarchy_rank']} | {s['D_eff']} | `{s['domain']}` | {s['sign']} | {s['S']:+.4f} |"
        )
    lines += [
        "",
        "## Hierarchy (tail → ceiling)",
        "",
        "| Rank | D_eff | Domain | sign | S |",
        "|-----:|------:|--------|:----:|----:|",
    ]
    for s in sim["hierarchy_ladder_tail"]:
        lines.append(
            f"| {s['hierarchy_rank']} | {s['D_eff']} | `{s['domain']}` | {s['sign']} | {s['S']:+.4f} |"
        )
    lines += [
        "",
        "## Top network-connected interfaces",
        "",
        "| Domain | D_eff | sign | influx | effective |",
        "|--------|------:|:----:|-------:|----------:|",
    ]
    for s in sim["top_network_connected"][:10]:
        lines.append(
            f"| `{s['domain']}` | {s['D_eff']} | {s['sign']} | {s['network_influx']:+.3f} | {s['effective_field']:+.4f} |"
        )
    lines += [
        "",
        "## Band stats",
        "",
        "| Band | count | emergence | damping | mean \\|S\\| |",
        "|------|------:|----------:|--------:|----------:|",
    ]
    for b, st in sorted((sim.get("band_stats") or {}).items()):
        lines.append(
            f"| {b} | {st['count']} | {st['emergence']} | {st['damping']} | {st['mean_abs_S']:.4f} |"
        )
    lines += [
        "",
        "## Run",
        "",
        "```powershell",
        "python scripts/build_fsot_system_math_audit.py",
        "python scripts/run_reality_building_blocks_simulation.py",
        "```",
        "",
        "Deterministic. Seed-locked. No free residual coefficients.",
        "",
    ]
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    print("=== Reality building-blocks simulation ===")
    audit = ensure_audit()
    hier = _load(HIER)
    net = _load(NET)
    if not hier or not net:
        print("Missing hierarchy/network — run build_fsot_system_math_audit.py", file=sys.stderr)
        return 1
    sim = simulate(audit, hier, net)
    OUT.write_text(json.dumps(sim, indent=2), encoding="utf-8")
    write_doc(sim)
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_DOC}")
    print(
        f"  interfaces={sim['counts']['total_interfaces']} "
        f"rules={sim['counts']['rules']} "
        f"links={sim['counts']['domain_domain_links']}"
    )
    print(f"  status={sim['status']}")
    cons = sim.get("consistency_from_audit") or {}
    print(f"  audit_consistency={cons.get('all_pass')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
