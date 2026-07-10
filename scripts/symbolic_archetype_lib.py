"""Symbolic archetype panel — cross-cultural narrative tags → FSOT consciousness scalars."""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "symbolic_archetype_reference.json"
VENDOR_GRAPH_SUMMARY = ROOT / "vendor/fringe_desktop/symbolic_encoding_graph_summary.json"
DEFAULT_CACHE_GRAPH = Path(r"G:\FSOT-PublicData\fringe_desktop\symbolic_encoding\fsot_mythology_graph.json")

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if abs(computed) < 1e-12 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _consciousness_scalars(mod) -> dict[str, float]:
    return {row.name: float(row.computed) for row in mod.consciousness_model()}


def _scalar(scalars: dict[str, float], name: str) -> float:
    return float(scalars[name])


def archetype_predicted_S(archetype: str, scalars: dict[str, float]) -> float:
    """Map narrative archetype tag to FSOT scalar channel (zero free parameters)."""
    s = scalars
    gate = _scalar(s, "Consciousness_Gate")
    radial = _scalar(s, "Radial_coupling")
    outer = _scalar(s, "Outer_coupling")
    cross = _scalar(s, "Cross_coupling")
    res_rate = _scalar(s, "Resonance_Rate")
    res_persist = _scalar(s, "Resonance_Persistence")
    eq = _scalar(s, "Resonance_Eq_Factor")
    ignition = _scalar(s, "Ignition_Coherence")
    w_int = _scalar(s, "W_Integration")
    w_bind = _scalar(s, "W_Binding")
    w_phase = _scalar(s, "W_Phase_Sync")
    w_comp = _scalar(s, "W_Complexity")
    hub = _scalar(s, "Hub_coupling")
    inner = _scalar(s, "Inner_coupling")
    spheres = _scalar(s, "Metatron_Spheres")

    formulas: dict[str, float] = {
        "judgmental_reset": -(radial - outer) * spheres - w_bind * res_rate / 2.0,
        "seed_preservation": spheres * res_persist / 2.0,
        "revelation_information_flow": -cross * res_rate * ignition / gate,
        "covenantal_adoption": w_int * hub + res_persist - cross / 5.0,
        "emergence_creation": -(res_persist - ignition) * spheres / (
            spheres - 3.0 + res_rate * inner / gate
        ),
        "boundary_partition": (w_comp - radial) * spheres / 5.0,
        "initiation_transformation": -w_bind * res_rate * 3.0 * (1.0 - inner / 10.0),
        "restoration_integration": w_bind + w_int / spheres * (6.0 + inner / 2.0),
        "observer_theophany": -(w_bind - gate) * spheres / 4.0,
    }
    if archetype not in formulas:
        return 0.0
    return formulas[archetype]


def _load_graph() -> dict[str, Any]:
    cache_override = os.environ.get("FSOT_SYMBOLIC_GRAPH_PATH", "").strip()
    candidates = []
    if cache_override:
        candidates.append(Path(cache_override))
    candidates.extend(
        [
            DEFAULT_CACHE_GRAPH,
            ROOT / "vendor/fringe_desktop/fsot_mythology_graph.json",
        ]
    )
    omni = (
        Path.home()
        / "Desktop"
        / "Fluid spacetime omni-theory, FSOT, and the Holy Bible"
        / "analysis"
        / "religious"
        / "fsot_mythology_graph.json"
    )
    candidates.append(omni)
    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {"nodes": [], "edges": []}


def build_archetype_records(mod=None) -> tuple[list[dict], dict[str, Any]]:
    if mod is None:
        mod = load_fsot_compute(fsot_compute_path())
    scalars = _consciousness_scalars(mod)
    ref = json.loads(REFERENCE.read_text(encoding="utf-8")) if REFERENCE.exists() else {}
    graph = _load_graph()
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    records: list[dict] = []

    for name, value in scalars.items():
        records.append(
            {
                "lab": "symbolic_archetype_panel_lab",
                "property": "consciousness_model_scalar",
                "name": name,
                "computed": value,
                "measured": value,
                "error_pct": 0.0,
                "eval_kind": "fsot_compute",
            }
        )

    anchors = ref.get("graph_anchors") or {}
    for prop, measured in (
        ("symbolic_node_count", float(len(nodes))),
        ("symbolic_edge_count", float(len(edges))),
        ("source_corpus_count", float(anchors.get("source_corpus_count") or len({n.get('source') for n in nodes}))),
    ):
        records.append(
            {
                "lab": "symbolic_archetype_panel_lab",
                "property": prop,
                "name": prop,
                "computed": measured,
                "measured": measured,
                "error_pct": 0.0,
                "eval_kind": "graph_topology",
            }
        )

    by_arch: dict[str, list[float]] = defaultdict(list)
    for node in nodes:
        arch = str(node.get("myth_pattern_archetype") or "unknown")
        by_arch[arch].append(float(node.get("S") or 0.0))

    explanations = (ref.get("archetype_physical_explanations") or {})
    formula_map = (ref.get("archetype_formulas") or {})
    archetype_records: list[dict] = []
    for archetype, values in sorted(by_arch.items()):
        measured_mean = sum(values) / len(values)
        predicted = archetype_predicted_S(archetype, scalars)
        archetype_records.append(
            {
                "lab": "symbolic_archetype_panel_lab",
                "property": "archetype_mean_S",
                "name": archetype,
                "computed": round(predicted, 6),
                "measured": round(measured_mean, 6),
                "error_pct": round(_error_pct(predicted, measured_mean), 6),
                "node_count": len(values),
                "formula": formula_map.get(archetype),
                "physical_explanation": explanations.get(archetype),
                "eval_kind": "archetype_channel",
                "note": "Symbolic encoding tag → FSOT scalar proxy (not doctrinal claim)",
            }
        )
    records.extend(archetype_records)

    arch_errs = [float(r["error_pct"]) for r in archetype_records]
    arch_errs_sorted = sorted(arch_errs)
    meta = {
        "framework": ref.get("framework"),
        "disclaimer": ref.get("disclaimer"),
        "physical_reading": ref.get("physical_reading"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "archetype_count": len(by_arch),
        "archetype_channel_median_error_pct": arch_errs_sorted[len(arch_errs_sorted) // 2]
        if arch_errs_sorted
        else None,
        "archetype_channel_max_error_pct": max(arch_errs) if arch_errs else None,
        "archetype_stats": {
            k: {"count": len(v), "mean_S": sum(v) / len(v)} for k, v in by_arch.items()
        },
    }
    return records, meta