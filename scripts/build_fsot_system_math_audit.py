#!/usr/bin/env python3
"""Full-system FSOT math audit + hierarchical building-block network.

Produces machine artifacts for:
  - Mathematician / scientist analysis (docs updated separately)
  - Downstream simulation of seed→domain→benchmark string networks

Outputs:
  data/fsot_system_math_audit.json
  data/fsot_building_block_hierarchy.json
  data/fsot_domain_formula_network.json
  docs/FSOT_SYSTEM_MATH_AUDIT.md  (summary tables)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import (  # noqa: E402
    A_BLEED,
    A_IN,
    ALPHA,
    B_IN,
    BETA,
    C_COSM,
    C_EFF,
    C_FACTOR,
    CHAOS,
    DOMAINS,
    E,
    ETA_EFF,
    G_CAT,
    GAMMA,
    GAMMA_C,
    K,
    OMEGA,
    P_BASE,
    P_NEW,
    P_VAR,
    PHI,
    PI,
    POOF,
    PSI_CON,
    SUCTION,
    THETA_S,
    compute_scalar,
    domain_scalar,
    ScalarInput,
)
from fsot_api_predict_lib import DOMAIN_FACTORS, PROPERTY_ROUTING  # noqa: E402
from mpmath import mpf  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

OUT_AUDIT = ROOT / "data" / "fsot_system_math_audit.json"
OUT_HIER = ROOT / "data" / "fsot_building_block_hierarchy.json"
OUT_NET = ROOT / "data" / "fsot_domain_formula_network.json"
OUT_DOC = ROOT / "docs" / "FSOT_SYSTEM_MATH_AUDIT.md"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
PIN = ROOT / "vendor" / "fsot_compute_AUTHORITY_PIN.json"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
ATLAS_CSV = ROOT / "data" / "publication" / "domain_atlas.csv"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _f(x) -> float:
    return float(x)


def seed_layer() -> dict[str, Any]:
    return {
        "layer": 0,
        "name": "foundational_seeds",
        "free_parameters": 0,
        "nodes": [
            {"id": "pi", "symbol": "π", "value": _f(PI), "role": "cyclic / geometric structure", "code": "PI"},
            {"id": "e", "symbol": "e", "value": _f(E), "role": "growth / decay", "code": "E"},
            {
                "id": "phi",
                "symbol": "φ",
                "value": _f(PHI),
                "role": "self-similar folds",
                "code": "PHI",
                "definition": "(1+√5)/2",
            },
            {
                "id": "gamma",
                "symbol": "γ",
                "value": _f(GAMMA),
                "role": "discrete ↔ continuous",
                "code": "GAMMA",
            },
            {
                "id": "G_Catalan",
                "symbol": "G",
                "value": _f(G_CAT),
                "role": "secondary geometric coupling",
                "code": "G_CAT",
            },
        ],
        "authority": "vendor/fsot_compute.py §1",
    }


def layer1() -> dict[str, Any]:
    return {
        "layer": 1,
        "name": "primary_derived",
        "depends_on": ["pi", "e", "phi", "gamma"],
        "nodes": [
            {"id": "ALPHA", "formula": "ln(π)/(e·φ¹³)", "value": _f(ALPHA), "section": "2.1"},
            {"id": "PSI_CON", "formula": "1-exp(-1)=(e-1)/e", "value": _f(PSI_CON), "section": "2.2"},
            {"id": "ETA_EFF", "formula": "1/(π-1)", "value": _f(ETA_EFF), "section": "2.3"},
            {"id": "BETA", "formula": "1/exp(π^π+(e-1))", "value": _f(BETA), "section": "2.4"},
            {"id": "GAMMA_C", "formula": "-ln(2)/φ", "value": _f(GAMMA_C), "section": "2.5"},
            {"id": "OMEGA", "formula": "sin(π/e)·√2", "value": _f(OMEGA), "section": "2.6"},
            {"id": "THETA_S", "formula": "sin(ψ_con·η_eff)", "value": _f(THETA_S), "section": "2.7"},
            {
                "id": "POOF",
                "formula": "exp((-ln(π)/e)/(η_eff·ln(φ)))",
                "value": _f(POOF),
                "section": "2.8",
                "role": "valve / collapse scale",
            },
        ],
    }


def layer2() -> dict[str, Any]:
    return {
        "layer": 2,
        "name": "composite_derived",
        "depends_on": ["layer1", "G_Catalan"],
        "nodes": [
            {
                "id": "C_EFF",
                "formula": "(1-POOF·sin(θ_S))·(1+0.01·G/(π·φ))",
                "value": _f(C_EFF),
                "section": "3.1",
                "role": "effective continuum speed / fluid scale",
            },
            {
                "id": "A_BLEED",
                "formula": "sin(π/e)·φ/√2",
                "value": _f(A_BLEED),
                "section": "3.2",
                "role": "inter-scale bleed",
            },
            {"id": "P_VAR", "formula": "-cos(θ_S+π)", "value": _f(P_VAR), "section": "3.3"},
            {"id": "B_IN", "formula": "C_eff·(1-sin(θ_S)/φ)", "value": _f(B_IN), "section": "3.4"},
            {"id": "A_IN", "formula": "A_bleed·(1+cos(θ_S)/φ)", "value": _f(A_IN), "section": "3.5"},
            {
                "id": "SUCTION",
                "formula": "POOF·(-cos(θ_S-π))",
                "value": _f(SUCTION),
                "section": "3.6",
                "role": "yin–yang complement of POOF",
            },
            {
                "id": "CHAOS",
                "formula": "γ_c/Ω",
                "value": _f(CHAOS),
                "section": "3.7",
                "role": "instability; engages with (D_eff-25)",
            },
            {"id": "P_BASE", "formula": "γ/e", "value": _f(P_BASE), "section": "3.8"},
            {"id": "P_NEW", "formula": "P_base·√2", "value": _f(P_NEW), "section": "3.9"},
            {
                "id": "C_FACTOR",
                "formula": "C_eff·P_new",
                "value": _f(C_FACTOR),
                "section": "3.10",
                "role": "consciousness / observer factor",
            },
            {
                "id": "K",
                "formula": "φ·(γ/e)·√2/ln(π)·0.99",
                "value": _f(K),
                "section": "3.11",
                "role": "global scale of S",
            },
            {
                "id": "C_COSM",
                "formula": "1/(φ·10)",
                "value": _f(C_COSM),
                "section": "3.12",
                "role": "cosmology interface constant",
            },
        ],
    }


def formula_branches() -> dict[str, Any]:
    return {
        "master": "S = K · (T1 + T2 + T3)",
        "code": "vendor/fsot_compute.py::compute_scalar",
        "formal": ["FSOT/Formal/Scalar.lean", "FSOT/Theorems.lean"],
        "branches": [
            {
                "id": "T1",
                "name": "observer_modulated_base",
                "role": "Dimensional base + growth + optional observer branch",
                "depends": [
                    "N",
                    "P",
                    "D_eff",
                    "ALPHA",
                    "GAMMA",
                    "PHI",
                    "PSI_CON",
                    "ETA_EFF",
                    "B_IN",
                    "C_EFF",
                    "P_NEW",
                    "hits",
                    "delta_psi",
                    "observed",
                    "C_FACTOR",
                    "P_VAR",
                ],
                "structure": [
                    "growth = exp(α·(1-hits/N)·γ/φ)",
                    "base = (N·P/√D)·cos((ψ_con+δψ)/η_eff)·exp(-α·hits/N+ρ+B_in·δψ)·(1+growth·C_eff)",
                    "T1 = base·(1+P_new·ln(D/25))",
                    "if observed: T1 *= exp(C_factor·P_var)·cos(δψ+P_var)",
                ],
                "fluid_note": "ln(D/25) folds about compactification ceiling D_eff=25",
            },
            {
                "id": "T2",
                "name": "linear_modulation",
                "role": "Scale / amplitude / trend (defaults 1,1,0 on domain routes)",
                "depends": ["scale", "amplitude", "trend_bias"],
                "structure": ["T2 = scale·amplitude + trend_bias"],
            },
            {
                "id": "T3",
                "name": "valve_acoustic_phase",
                "role": "POOF/SUCTION valves, chaos(D-25), acoustic bleed — fluid dynamics heart",
                "depends": [
                    "BETA",
                    "CHAOS",
                    "POOF",
                    "SUCTION",
                    "THETA_S",
                    "A_BLEED",
                    "A_IN",
                    "B_IN",
                    "P_VAR",
                    "PHI",
                    "D_eff",
                    "delta_psi",
                    "delta_theta",
                ],
                "structure": [
                    "valve = β·cos(δψ)·(N·P/√D)·(1+chaos·(D-25)/25)·(1+poof·cos(θ_S+π)+suction·sin(θ_S))",
                    "acoustic = 1 + (A_bleed·sin²δθ)/φ + (A_in·cos²δθ)/φ",
                    "phase = 1 + B_in·P_var",
                    "T3 = valve · acoustic · phase",
                ],
                "fluid_note": "Chaos term vanishes at D=25 ceiling; valves are continuum fluid switches",
            },
            {
                "id": "K_scale",
                "name": "global_scale",
                "role": "S = K·(T1+T2+T3)",
                "depends": ["K", "T1", "T2", "T3"],
            },
        ],
        "residual_law": {
            "formula": "c = m · (1 + |S(domain)| · f_domain)",
            "code": "scripts/fsot_api_predict_lib.py::fsot_scaled",
            "error_pct": "ε = 100·|c-m|/max(|m|,ε_floor)",
            "green_gate": "pooled median ε ≤ 0.5%",
            "tier_aspiration": "pooled median ε ≤ 0.05%",
        },
        "sign_interpretation": {
            "S_gt_0": "emergence (Theorems.lean positive_S_means_emergence)",
            "S_lt_0": "damping (Theorems.lean negative_S_means_damping)",
            "nuclear_emergence": "domain_scalar(Nuclear_Physics) > 0",
            "cosmology_damping": "domain_scalar(Cosmology) < 0 at D_eff=25",
        },
    }


def _band(d_eff: int) -> str:
    if d_eff <= 9:
        return "micro"
    if d_eff <= 15:
        return "meso"
    if d_eff <= 19:
        return "geo_climate"
    return "astro"


def _nearest_core_by_deff(d_eff: int) -> str:
    """Map extension D_eff to nearest core domain name for residual-factor inheritance."""
    best = None
    best_dist = 10**9
    for name, cfg in DOMAINS.items():
        dist = abs(int(cfg.D_eff) - int(d_eff))
        if dist < best_dist or (dist == best_dist and (best is None or name < best)):
            best_dist = dist
            best = name
    return best or "Cosmology"


def _resolve_factor(domain_name: str, d_eff: int, routes_to_core: str | None = None) -> tuple[float | None, str]:
    if domain_name in DOMAIN_FACTORS:
        return float(DOMAIN_FACTORS[domain_name]), domain_name
    if domain_name == "Molecular_Chemistry":
        return float(DOMAIN_FACTORS.get("Chemistry", 0.001)), "Chemistry"
    if routes_to_core and routes_to_core in DOMAIN_FACTORS:
        return float(DOMAIN_FACTORS[routes_to_core]), routes_to_core
    core = _nearest_core_by_deff(d_eff)
    f = DOMAIN_FACTORS.get(core)
    if f is None:
        f = 0.001
        return float(f), "default_0.001"
    return float(f), core


def _compute_S(d_eff: int, hits: int, delta_psi: float, delta_theta: float, observed: bool) -> float:
    return _f(
        compute_scalar(
            ScalarInput(
                N=mpf(1),
                P=mpf(1),
                D_eff=mpf(d_eff),
                delta_psi=mpf(delta_psi),
                delta_theta=mpf(delta_theta),
                recent_hits=mpf(hits),
                observed=observed,
                rho=mpf(1),
                scale=mpf(1),
                amplitude=mpf(1),
            )
        )
    )


def core_domain_table() -> list[dict[str, Any]]:
    rows = []
    for name, d in sorted(DOMAINS.items(), key=lambda x: (x[1].D_eff, x[0])):
        s = _f(domain_scalar(name))
        factor, factor_src = _resolve_factor(name, int(d.D_eff))
        floor = abs(s) * float(factor) * 100.0 if factor is not None else None
        rows.append(
            {
                "domain": name,
                "kind": "core",
                "D_eff": int(d.D_eff),
                "hits": int(d.hits),
                "delta_psi": _f(d.delta_psi),
                "delta_theta": _f(d.delta_theta),
                "observed": bool(d.observed),
                "C_interpretation": _f(d.C),
                "S": s,
                "sign": "emergence" if s > 0 else "damping" if s < 0 else "zero",
                "domain_factor_f": factor,
                "factor_source": factor_src,
                "pure_residual_floor_pct": floor,
                "band": _band(int(d.D_eff)),
                "compactification_distance": int(d.D_eff) - 25,
                "routes_to_core": name,
            }
        )
    return rows


def extension_domain_table() -> list[dict[str, Any]]:
    """All extension domains from extension_domains_manifest.yaml (full atlas expansion)."""
    if yaml is None or not EXT_MANIFEST.exists():
        return []
    doc = yaml.safe_load(EXT_MANIFEST.read_text(encoding="utf-8")) or {}
    eds = doc.get("extension_domains") or {}
    rows: list[dict[str, Any]] = []
    for name, spec in sorted(eds.items(), key=lambda x: (int((x[1] or {}).get("D_eff") or 25), x[0])):
        if not isinstance(spec, dict):
            continue
        d_eff = int(spec.get("D_eff") or 25)
        hits = int(spec.get("recent_hits") or 0)
        delta_psi = float(spec.get("delta_psi") or 1.0)
        delta_theta = float(spec.get("delta_theta") or 1.0)
        observed = bool(spec.get("observed", True))
        routes = spec.get("routes_to_core")
        if isinstance(routes, list):
            routes = routes[0] if routes else None
        s = _compute_S(d_eff, hits, delta_psi, delta_theta, observed)
        factor, factor_src = _resolve_factor(str(name), d_eff, str(routes) if routes else None)
        floor = abs(s) * float(factor) * 100.0 if factor is not None else None
        rows.append(
            {
                "domain": name,
                "kind": "extension",
                "D_eff": d_eff,
                "hits": hits,
                "delta_psi": delta_psi,
                "delta_theta": delta_theta,
                "observed": observed,
                "S": s,
                "sign": "emergence" if s > 0 else "damping" if s < 0 else "zero",
                "domain_factor_f": factor,
                "factor_source": factor_src,
                "pure_residual_floor_pct": floor,
                "band": _band(d_eff),
                "compactification_distance": d_eff - 25,
                "routes_to_core": routes or factor_src if factor_src in DOMAINS else _nearest_core_by_deff(d_eff),
                "tier": spec.get("tier"),
                "benchmark_data": spec.get("benchmark_data"),
                "lean_module": spec.get("lean_module"),
                "maps_to_lean": spec.get("maps_to_lean") or [],
            }
        )
    return rows


def domain_table() -> list[dict[str, Any]]:
    """Core 35 + full extension expansion (400+ total)."""
    return core_domain_table() + extension_domain_table()


def atlas_snapshot() -> dict[str, Any]:
    if not ATLAS_CSV.exists():
        return {"row_count": 0}
    import csv

    rows = list(csv.DictReader(ATLAS_CSV.open(encoding="utf-8")))
    kinds: dict[str, int] = {}
    for r in rows:
        k = r.get("kind") or "unknown"
        kinds[k] = kinds.get(k, 0) + 1
    return {
        "path": "data/publication/domain_atlas.csv",
        "row_count": len(rows),
        "kinds": kinds,
        "sample_domains": [r.get("domain") for r in rows[:8]],
    }


def benchmark_links(all_domains: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if not MARGIN.exists():
        return {"benchmark_file_count": 0, "green": 0, "by_domain_guess": {}}
    margin = json.loads(MARGIN.read_text(encoding="utf-8"))
    rows = margin.get("all_domains") or []
    green = [r for r in rows if r.get("green_gate_pass") and not r.get("excluded")]
    # Index all domain names (core + extension) for attachment
    name_set = {d["domain"] for d in (all_domains or [])}
    core_names = set(DOMAINS.keys())
    by_core: dict[str, list[str]] = {n: [] for n in core_names}
    by_named: dict[str, list[str]] = {}
    unmapped: list[str] = []
    green_list: list[dict[str, Any]] = []
    for r in green:
        fname = str(r.get("file") or "")
        dom = str(r.get("domain") or "")
        pooled = r.get("official_pooled_median_error_pct")
        if pooled is None:
            pooled = r.get("scalar_pooled_median_error_pct")
        green_list.append(
            {
                "file": fname,
                "domain": dom,
                "records": r.get("records") or r.get("scalar_count"),
                "pooled_median_error_pct": pooled,
                "tier_scalar_pass": r.get("tier_scalar_pass"),
            }
        )
        hit = None
        # exact domain name match first
        if dom in name_set:
            hit = dom
        else:
            for cn in sorted(core_names, key=len, reverse=True):
                key = cn.lower().replace("_", "")
                blob = (fname + " " + dom).lower().replace("_", "").replace(" ", "")
                if key in blob or cn.lower() in (fname + " " + dom).lower():
                    hit = cn
                    break
        if hit:
            if hit in by_core:
                by_core[hit].append(fname)
            by_named.setdefault(hit, []).append(fname)
        else:
            unmapped.append(fname or dom)
    return {
        "benchmark_file_count": margin.get("benchmark_file_count"),
        "green_gate_pass_count": margin.get("green_gate_pass_count")
        or sum(1 for r in rows if r.get("green_gate_pass")),
        "green_gate_fail_count": margin.get("green_gate_fail_count"),
        "tier_scalar_fail_count": margin.get("tier_scalar_fail_count"),
        "green_panel_count": len(green_list),
        "core_domain_green_panel_counts": {k: len(v) for k, v in by_core.items() if v},
        "named_domain_attachment_count": len(by_named),
        "unmapped_green_panels_sample": unmapped[:40],
        "unmapped_green_count": len(unmapped),
        "green_panels": green_list,  # full list for simulation
    }


def hierarchy(domains: list[dict], branches: dict) -> dict[str, Any]:
    """Hierarchical building blocks for reality-syntax simulation (core + full expansion)."""
    edges: list[dict[str, str]] = []
    nodes: list[dict[str, Any]] = []
    seen_nodes: set[str] = set()

    def node(nid: str, kind: str, **extra: Any) -> None:
        if nid in seen_nodes:
            return
        seen_nodes.add(nid)
        nodes.append({"id": nid, "kind": kind, **extra})

    for s in seed_layer()["nodes"]:
        node(s["id"], "seed", symbol=s.get("symbol"), value=s.get("value"))
    for s in layer1()["nodes"]:
        node(s["id"], "layer1", formula=s.get("formula"), value=s.get("value"))
        for dep in ("pi", "e", "phi", "gamma"):
            edges.append({"from": dep, "to": s["id"], "rel": "derives"})
    for s in layer2()["nodes"]:
        node(s["id"], "layer2", formula=s.get("formula"), value=s.get("value"), role=s.get("role"))
        edges.append({"from": "layer1_bundle", "to": s["id"], "rel": "composes"})
    node("layer1_bundle", "bundle", label="primary_derived_bundle")

    for b in branches["branches"]:
        node(b["id"], "formula_branch", name=b.get("name"), role=b.get("role"))
        for dep in b.get("depends") or []:
            if dep in (
                "N", "P", "D_eff", "hits", "scale", "amplitude", "trend_bias",
                "observed", "delta_psi", "delta_theta", "rho",
            ):
                node(f"input_{dep}", "engine_input", name=dep)
                edges.append({"from": f"input_{dep}", "to": b["id"], "rel": "inputs"})
            else:
                edges.append({"from": dep, "to": b["id"], "rel": "feeds"})
    node("S", "scalar", formula="K*(T1+T2+T3)")
    for t in ("T1", "T2", "T3"):
        edges.append({"from": t, "to": "S", "rel": "sums_into"})
    edges.append({"from": "K", "to": "S", "rel": "scales_into"})

    node("D_eff_ceiling_25", "architecture", role="fluid_compactification_ceiling")
    edges.append({"from": "D_eff_ceiling_25", "to": "T1", "rel": "ln(D/25)_fold"})
    edges.append({"from": "D_eff_ceiling_25", "to": "T3", "rel": "chaos_(D-25)_term"})
    node("fluid_spacetime", "ontology", role="omni_medium_across_scales")
    edges.append({"from": "fluid_spacetime", "to": "D_eff_ceiling_25", "rel": "defines"})
    edges.append({"from": "fluid_spacetime", "to": "C_EFF", "rel": "manifests_as"})

    n_core = sum(1 for d in domains if d.get("kind") == "core")
    n_ext = sum(1 for d in domains if d.get("kind") == "extension")

    for d in domains:
        did = f"domain_{d['domain']}"
        node(
            did,
            "domain_interface",
            domain=d["domain"],
            domain_kind=d.get("kind") or "core",
            D_eff=d["D_eff"],
            S=d["S"],
            sign=d["sign"],
            band=d["band"],
            f=d["domain_factor_f"],
        )
        edges.append({"from": "S", "to": did, "rel": "evaluated_at"})
        edges.append({"from": "input_D_eff", "to": did, "rel": "sets_D"})
        # Extension folds onto core residual factor source
        core = d.get("routes_to_core") or d.get("factor_source")
        if d.get("kind") == "extension" and core and core in DOMAINS:
            edges.append({"from": did, "to": f"domain_{core}", "rel": "extension_fold_of"})
        if d.get("domain_factor_f") is not None:
            # Share factor nodes by source core when possible
            fsrc = d.get("factor_source") or d["domain"]
            fid = f"factor_{fsrc}"
            node(fid, "residual_factor", value=d["domain_factor_f"], source=fsrc)
            edges.append({"from": did, "to": fid, "rel": "pairs_with"})
            rid = f"residual_law_{fsrc}"
            node(rid, "residual_law", formula="c=m(1+|S|f)")
            edges.append({"from": fid, "to": rid, "rel": "applies"})
            edges.append({"from": did, "to": rid, "rel": "S_channel"})

    order = sorted(domains, key=lambda x: (x["D_eff"], x.get("kind") != "core", x["domain"]))
    emergence_ladder = [
        {
            "rank": i + 1,
            "domain": d["domain"],
            "kind": d.get("kind"),
            "D_eff": d["D_eff"],
            "S": d["S"],
            "sign": d["sign"],
            "band": d["band"],
            "routes_to_core": d.get("routes_to_core"),
            "syntax_note": "emergence_class" if d["sign"] == "emergence" else "damping_class",
        }
        for i, d in enumerate(order)
    ]

    return {
        "generated_at": _now(),
        "version": "2.0",
        "purpose": (
            "Hierarchical building blocks: seeds → derived → T1/T2/T3 → S → "
            "core+extension domain interfaces (full atlas expansion) → residual law."
        ),
        "ontology": "fluid_spacetime_omni_D_eff_ceiling_25",
        "core_domain_count": n_core,
        "extension_domain_count": n_ext,
        "total_domain_interfaces": n_core + n_ext,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "emergence_ladder_by_D_eff": emergence_ladder,
        "simulation_hooks": {
            "seed_vector": ["pi", "e", "phi", "gamma", "G_Catalan"],
            "evaluate_core": "domain_scalar(name) → S",
            "evaluate_extension": (
                "compute_scalar(ScalarInput(D_eff, hits, delta_psi, observed from extension_domains_manifest))"
            ),
            "residual": "c = m*(1+|S|*f); f from DOMAIN_FACTORS[core] or nearest-core inheritance",
            "string_between_domains": (
                "shared seeds + T1/T2/T3; differ by interface tuple; extensions fold to cores"
            ),
            "hierarchy_rule": (
                "Lower D_eff = micro building blocks; higher D_eff folds toward ceiling 25. "
                "Full expansion (~400 domains) uses same formula as the 35 cores."
            ),
        },
    }


def network_for_sim(domains: list[dict], bench: dict) -> dict[str, Any]:
    """Domain network: core pairwise + extension→core folds + seed strings for ALL domains."""
    cores = [d for d in domains if d.get("kind") == "core"]
    exts = [d for d in domains if d.get("kind") == "extension"]
    links: list[dict[str, Any]] = []

    def score_pair(a: dict, b: dict) -> tuple[float, list[str]]:
        score = 0.0
        reasons: list[str] = []
        if a["band"] == b["band"]:
            score += 1.0
            reasons.append("same_band")
        if a["sign"] == b["sign"]:
            score += 0.5
            reasons.append("same_sign")
        if abs(a["D_eff"] - b["D_eff"]) <= 1:
            score += 0.75
            reasons.append("adjacent_D_eff")
        if a.get("observed") == b.get("observed"):
            score += 0.25
            reasons.append("same_observer_flag")
        if a.get("domain_factor_f") and b.get("domain_factor_f"):
            if abs(float(a["domain_factor_f"]) - float(b["domain_factor_f"])) < 1e-9:
                score += 0.5
                reasons.append("same_factor")
        return score, reasons

    # Full pairwise among cores
    for i, a in enumerate(cores):
        for b in cores[i + 1 :]:
            score, reasons = score_pair(a, b)
            if score >= 1.0:
                links.append(
                    {"source": a["domain"], "target": b["domain"], "weight": score, "reasons": reasons, "kind": "core_core"}
                )

    # Extensions: link to route core + high-score same-band cores only
    core_by_name = {c["domain"]: c for c in cores}
    for e in exts:
        route = e.get("routes_to_core")
        if route and route in core_by_name:
            links.append(
                {
                    "source": e["domain"],
                    "target": route,
                    "weight": 2.0,
                    "reasons": ["extension_fold_of_core"],
                    "kind": "extension_core",
                }
            )
        for c in cores:
            if c["domain"] == route:
                continue
            score, reasons = score_pair(e, c)
            if score >= 1.5:
                links.append(
                    {
                        "source": e["domain"],
                        "target": c["domain"],
                        "weight": score,
                        "reasons": reasons,
                        "kind": "extension_core_neighbor",
                    }
                )

    # Extension–extension: only adjacent D_eff + same band (keep graph tractable)
    by_deff: dict[int, list[dict]] = {}
    for e in exts:
        by_deff.setdefault(int(e["D_eff"]), []).append(e)
    for deff, group in by_deff.items():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                if a["band"] == b["band"] and a["sign"] == b["sign"]:
                    links.append(
                        {
                            "source": a["domain"],
                            "target": b["domain"],
                            "weight": 1.25,
                            "reasons": ["same_D_eff", "same_band", "same_sign"],
                            "kind": "extension_extension",
                        }
                    )
        # adjacent D_eff bucket
        for other in by_deff.get(deff + 1, []):
            for a in group:
                if a["band"] == other["band"]:
                    links.append(
                        {
                            "source": a["domain"],
                            "target": other["domain"],
                            "weight": 1.0,
                            "reasons": ["adjacent_D_eff", "same_band"],
                            "kind": "extension_extension",
                        }
                    )

    seed_strings = [
        {"source": s, "target": d["domain"], "weight": 1.0, "reasons": ["seed_to_domain_via_S"], "kind": "seed_domain"}
        for s in ("pi", "e", "phi", "gamma", "G_Catalan")
        for d in domains
    ]

    # Benchmark panel → domain attachments
    panel_links = []
    for p in bench.get("green_panels") or []:
        panel_links.append(
            {
                "source": p.get("file") or p.get("domain"),
                "target_domain": p.get("domain"),
                "pooled_median_error_pct": p.get("pooled_median_error_pct"),
                "records": p.get("records"),
                "kind": "benchmark_panel",
            }
        )

    return {
        "generated_at": _now(),
        "version": "2.0",
        "core_domain_count": len(cores),
        "extension_domain_count": len(exts),
        "total_domain_interfaces": len(domains),
        "domain_domain_links": links,
        "domain_domain_link_count": len(links),
        "seed_domain_links": seed_strings,
        "seed_domain_link_count": len(seed_strings),
        "green_benchmark_panels": panel_links,
        "green_benchmark_panel_count": len(panel_links),
        "benchmark_attachment_core_counts": bench.get("core_domain_green_panel_counts") or {},
        "how_to_simulate": {
            "1": "Load seeds L0; derive L1/L2 as fsot_compute",
            "2": "Evaluate S for all 35 cores via domain_scalar",
            "3": "Evaluate S for all extensions via ScalarInput from extension_domains_manifest",
            "4": "Apply residual law with inherited/core DOMAIN_FACTORS",
            "5": "Use extension_fold_of_core edges + seed strings + green panel list",
            "6": "Emergence ladder = all domains sorted by D_eff (micro→ceiling 25)",
            "7": "Sign(S) is local emerge/damp syntax bit across the full atlas",
        },
    }


def consistency_checks(domains: list[dict]) -> dict[str, Any]:
    checks = []
    ok = True

    def add(name: str, passed: bool, detail: str) -> None:
        nonlocal ok
        checks.append({"id": name, "pass": passed, "detail": detail})
        if not passed:
            ok = False

    cores = [d for d in domains if d.get("kind") == "core"]
    exts = [d for d in domains if d.get("kind") == "extension"]
    add("n_core_domains_35", len(cores) == 35, f"n_core={len(cores)}")
    add("n_extension_domains_ge_300", len(exts) >= 300, f"n_ext={len(exts)}")
    add("n_total_interfaces_ge_400", len(domains) >= 400, f"n_total={len(domains)}")

    cos = next(d for d in cores if d["domain"] == "Cosmology")
    add("cosmology_D25", cos["D_eff"] == 25, f"D={cos['D_eff']}")
    add("cosmology_damping", cos["S"] < 0, f"S={cos['S']}")
    nuc = next(d for d in cores if d["domain"] == "Nuclear_Physics")
    add("nuclear_emergence", nuc["S"] > 0, f"S={nuc['S']}")
    part = next(d for d in cores if d["domain"] == "Particle_Physics")
    add("particle_emergence", part["S"] > 0, f"S={part['S']}")

    missing_f = [d["domain"] for d in cores if d["domain_factor_f"] is None]
    add("core_factors_present", len(missing_f) == 0, f"missing={missing_f}")

    for d in cores:
        cfg = DOMAINS[d["domain"]]
        s2 = _compute_S(int(cfg.D_eff), int(cfg.hits), _f(cfg.delta_psi), _f(cfg.delta_theta), bool(cfg.observed))
        if abs(s2 - d["S"]) >= 1e-9:
            add(f"S_recompute_{d['domain']}", False, f"{s2} vs {d['S']}")
            break
    else:
        add("S_recompute_all_cores", True, "all 35 cores match")

    # Spot-check extension recompute
    if exts:
        e0 = exts[0]
        s2 = _compute_S(e0["D_eff"], e0["hits"], e0["delta_psi"], e0["delta_theta"], e0["observed"])
        add("S_recompute_extension_sample", abs(s2 - e0["S"]) < 1e-9, f"{e0['domain']}: {s2} vs {e0['S']}")

    for d in domains:
        f = d["domain_factor_f"]
        if f is None:
            continue
        floor = abs(d["S"]) * float(f) * 100.0
        if abs(floor - (d["pure_residual_floor_pct"] or 0)) > 1e-6:
            add(f"floor_{d['domain']}", False, "floor mismatch")
            break
    else:
        add("residual_floor_consistent_all", True, f"floor=|S|f*100 for {len(domains)} interfaces")

    add("K_pos", _f(K) > 0, f"K={_f(K)}")
    add("C_EFF_pos", _f(C_EFF) > 0, f"C_EFF={_f(C_EFF)}")
    add("POOF_pos", _f(POOF) > 0, f"POOF={_f(POOF)}")

    pin_ok = PIN.exists()
    pin_data = json.loads(PIN.read_text(encoding="utf-8")) if pin_ok else {}
    add("authority_pin_file", pin_ok, str(pin_data.get("pin") or pin_data)[:80])

    atlas = atlas_snapshot()
    add("atlas_rows_ge_400", atlas.get("row_count", 0) >= 400, f"atlas={atlas.get('row_count')}")

    return {
        "all_pass": ok,
        "checks": checks,
        "pass_count": sum(1 for c in checks if c["pass"]),
        "fail_count": sum(1 for c in checks if not c["pass"]),
    }


def write_doc(audit: dict) -> None:
    cores = audit.get("core_domains") or [d for d in audit["domains"] if d.get("kind") == "core"]
    exts = audit.get("extension_domains") or [d for d in audit["domains"] if d.get("kind") == "extension"]
    cons = audit["consistency"]
    counts = audit.get("counts") or {}
    n_ok = cons["pass_count"]
    n_tot = cons["pass_count"] + cons["fail_count"]
    lines = [
        "# FSOT system math audit — summary",
        "",
        f"**Generated:** {audit['generated_at']}  ",
        f"**Authority pin file:** `vendor/fsot_compute_AUTHORITY_PIN.json`  ",
        f"**Consistency:** {'PASS' if cons['all_pass'] else 'FAIL'} ({n_ok}/{n_tot})",
        "",
        "## Scope (not core-only)",
        "",
        f"| Layer | Count |",
        f"|-------|------:|",
        f"| Core domain interfaces | {counts.get('core_domains', len(cores))} |",
        f"| Extension domain interfaces | {counts.get('extension_domains', len(exts))} |",
        f"| **Total formula interfaces** | **{counts.get('total_domain_interfaces', len(cores)+len(exts))}** |",
        f"| Publication atlas rows | {counts.get('atlas_rows')} |",
        f"| Green residual benchmark panels | {counts.get('green_benchmark_panels')} |",
        f"| Benchmark files (margin audit) | {counts.get('benchmark_files')} |",
        "",
        "Machine dump: [`data/fsot_system_math_audit.json`](../data/fsot_system_math_audit.json)  ",
        "Hierarchy: [`data/fsot_building_block_hierarchy.json`](../data/fsot_building_block_hierarchy.json)  ",
        "Network + green panels: [`data/fsot_domain_formula_network.json`](../data/fsot_domain_formula_network.json)  ",
        "Extensions source: [`data/extension_domains_manifest.yaml`](../data/extension_domains_manifest.yaml)  ",
        "Atlas: [`data/publication/domain_atlas.csv`](../data/publication/domain_atlas.csv)  ",
        "Guide: [`FSOT_MATHEMATICIAN_HOWTO.md`](FSOT_MATHEMATICIAN_HOWTO.md) · Key: [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md)",
        "",
        "## Ontology",
        "",
        "FSOT is **fluid spacetime omni-theory** with compactification ceiling "
        r"\(D_{\mathrm{eff}}=25\). **All** domains (core + expansion) are dimensional "
        "interfaces into one medium and one \(S=K(T_1+T_2+T_3)\).",
        "",
        "## Master formula",
        "",
        "```",
        "S = K · (T1 + T2 + T3)",
        "c = m · (1 + |S(interface)| · f)",
        "# extensions: same law; f inherited from core / nearest-core DOMAIN_FACTORS",
        "```",
        "",
        "## 35 core domains (live S)",
        "",
        "| D_eff | Domain | obs | S | sign | f | floor % |",
        "|------:|--------|:---:|-----:|:----:|------:|--------:|",
    ]
    for d in cores:
        f = d["domain_factor_f"]
        floor = d["pure_residual_floor_pct"]
        fs = f"{f}" if f is not None else "—"
        fl = f"{floor:.6f}" if floor is not None else "—"
        lines.append(
            f"| {d['D_eff']} | `{d['domain']}` | {str(d['observed'])} | {d['S']:+.6f} | "
            f"{d['sign']} | {fs} | {fl} |"
        )
    # Extension band summary
    from collections import Counter

    band_c = Counter(d["band"] for d in exts)
    sign_c = Counter(d["sign"] for d in exts)
    lines += [
        "",
        f"## Extension expansion ({len(exts)} domains)",
        "",
        "Full per-domain \(S\) lives in the JSON (`extension_domains` array). Summary:",
        "",
        f"- By band: {dict(band_c)}",
        f"- By sign: {dict(sign_c)}",
        f"- Sample: " + ", ".join(f"`{d['domain']}`(D={d['D_eff']},S={d['S']:+.3f})" for d in exts[:8]),
        "",
        "## Consistency checks",
        "",
    ]
    for c in cons["checks"]:
        flag = "PASS" if c["pass"] else "FAIL"
        lines.append(f"- **{flag}** `{c['id']}` — {c['detail']}")
    lines += [
        "",
        "## Benchmark envelope",
        "",
        f"- Green panels: {audit['benchmarks'].get('green_gate_pass_count')} / "
        f"{audit['benchmarks'].get('benchmark_file_count')}",
        f"- Tier-scalar fails: {audit['benchmarks'].get('tier_scalar_fail_count')}",
        f"- Unmapped green (name heuristic): {audit['benchmarks'].get('unmapped_green_count')}",
        "",
        "Regenerate:",
        "",
        "```powershell",
        "python scripts/build_fsot_system_math_audit.py",
        "```",
        "",
    ]
    OUT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    pin = {}
    if PIN.exists():
        pin = json.loads(PIN.read_text(encoding="utf-8"))

    domains = domain_table()
    cores = [d for d in domains if d.get("kind") == "core"]
    exts = [d for d in domains if d.get("kind") == "extension"]
    branches = formula_branches()
    bench = benchmark_links(domains)
    atlas = atlas_snapshot()
    hier = hierarchy(domains, branches)
    net = network_for_sim(domains, bench)
    cons = consistency_checks(domains)

    # Compact audit JSON: full domain list is required for the sim — keep it
    audit = {
        "generated_at": _now(),
        "version": "2.0",
        "authority_pin": pin,
        "ontology": {
            "statement": "FSOT is fluid spacetime omni-theory math across all scales",
            "D_eff_ceiling": 25,
            "compactification": True,
            "absolute_rest_frame": "fiction_damped",
            "fluid_medium": "load_bearing_reality",
            "scope": "35 core interfaces + full extension atlas expansion (not core-only)",
        },
        "counts": {
            "core_domains": len(cores),
            "extension_domains": len(exts),
            "total_domain_interfaces": len(domains),
            "atlas_rows": atlas.get("row_count"),
            "green_benchmark_panels": bench.get("green_panel_count"),
            "benchmark_files": bench.get("benchmark_file_count"),
        },
        "seeds": seed_layer(),
        "layer1_primary_derived": layer1(),
        "layer2_composite_derived": layer2(),
        "formula_branches": branches,
        "core_domains": cores,
        "extension_domains": exts,
        "domains": domains,
        "domain_count": len(domains),
        "domain_factors_table": DOMAIN_FACTORS,
        "property_routing_count": len(PROPERTY_ROUTING),
        "atlas": atlas,
        "benchmarks": {
            k: v
            for k, v in bench.items()
            if k != "green_panels"  # panels live in network JSON to keep audit lighter
        },
        "benchmarks_green_panels_path": "data/fsot_domain_formula_network.json → green_benchmark_panels",
        "consistency": cons,
        "related": {
            "math_key": "docs/FSOT_MATH_KEY.md",
            "mathematician_howto": "docs/FSOT_MATHEMATICIAN_HOWTO.md",
            "uniqueness_research": "data/uniqueness_research_verification_report.json",
            "reality_fiction": "data/reality_fiction_calibration.json",
            "hierarchy": "data/fsot_building_block_hierarchy.json",
            "network": "data/fsot_domain_formula_network.json",
            "extension_manifest": "data/extension_domains_manifest.yaml",
            "domain_atlas": "data/publication/domain_atlas.csv",
        },
    }
    # Put full green panel list on audit too for single-file sim load
    audit["green_benchmark_panels"] = bench.get("green_panels") or []

    OUT_AUDIT.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    OUT_HIER.write_text(json.dumps(hier, indent=2), encoding="utf-8")
    OUT_NET.write_text(json.dumps(net, indent=2), encoding="utf-8")
    write_doc(audit)

    print(f"Wrote {OUT_AUDIT}")
    print(f"  cores={len(cores)} extensions={len(exts)} total={len(domains)}")
    print(f"  atlas={atlas.get('row_count')} green_panels={bench.get('green_panel_count')}")
    print(f"Wrote {OUT_HIER} nodes={hier['node_count']} edges={hier['edge_count']}")
    print(f"Wrote {OUT_NET} domain_links={len(net['domain_domain_links'])} seed_links={len(net['seed_domain_links'])}")
    print(f"Wrote {OUT_DOC}")
    print(f"consistency all_pass={cons['all_pass']} {cons['pass_count']}/{cons['pass_count']+cons['fail_count']}")
    return 0 if cons["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
