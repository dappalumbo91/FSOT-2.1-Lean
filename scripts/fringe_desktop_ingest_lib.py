"""Fringe desktop trace ingest — Soul Simulator, FIC, VibraFSOT, symbolic encoding graph."""

from __future__ import annotations

import csv
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = Path(r"G:\FSOT-PublicData\fringe_desktop")
DESKTOP = Path.home() / "Desktop"


def cache_root() -> Path:
    override = os.environ.get("FSOT_FRINGE_CACHE_ROOT", "").strip()
    if override:
        return Path(override)
    return DEFAULT_CACHE


def _desktop_path(rel: str) -> Path:
    return DESKTOP / rel


def _read_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_json_first_object(path: Path) -> dict:
    """Parse first JSON object from a file (handles truncated desktop exports)."""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    try:
        doc = json.loads(text)
        if isinstance(doc, list) and doc:
            return doc[0] if isinstance(doc[0], dict) else {}
        if isinstance(doc, dict):
            return doc
    except json.JSONDecodeError:
        pass
    import re

    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text)
    if match:
        try:
            obj = json.loads(match.group(0))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    return {}


def _write_summary(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def ingest_soul_simulator_manifest(
    desktop_rel: str = "Soul Simulator/data/processed/manifest.json",
    vendor_out: Path | None = None,
) -> dict[str, Any]:
    src = _desktop_path(desktop_rel)
    vendor_out = vendor_out or ROOT / "vendor/fringe_desktop/soul_simulator_manifest_summary.json"
    if not src.exists():
        return {"ok": False, "error": f"missing {src}"}
    manifest = _read_json(src)
    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(src),
        "records_processed": int(manifest.get("records_processed") or 0),
        "file_count": int(manifest.get("file_count") or 0),
        "types": manifest.get("types") or {},
        "processed_at": manifest.get("processed_at"),
    }
    _write_summary(vendor_out, summary)
    return {"ok": True, "summary": summary, "vendor_path": str(vendor_out)}


def ingest_intelligence_compressor(
    states_rel: str = "FSOT-2.0-code/IntelligenceCompressor/intelligence_states.json",
    sweep_rel: str = "FSOT-2.0-code/IntelligenceCompressor/fic_sensitivity_sweep.csv",
    vendor_out: Path | None = None,
    sweep_out: Path | None = None,
) -> dict[str, Any]:
    states_path = _desktop_path(states_rel)
    sweep_path = _desktop_path(sweep_rel)
    vendor_out = vendor_out or ROOT / "vendor/fringe_desktop/intelligence_compressor_summary.json"
    sweep_out = sweep_out or ROOT / "vendor/fringe_desktop/fic_sensitivity_sweep_summary.json"
    if not states_path.exists():
        vendor_fallback = ROOT / "vendor/fringe_desktop/intelligence_compressor_summary.json"
        if vendor_fallback.exists():
            return {"ok": True, "summary": _read_json(vendor_fallback), "vendor_path": str(vendor_fallback), "fallback": True}
        return {"ok": False, "error": f"missing {states_path}"}
    head = _read_json_first_object(states_path)
    if not head:
        return {"ok": False, "error": f"could not parse headline from {states_path}"}
    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(states_path),
        "state_count": 1,
        "headline": {
            "D_eff": head.get("D_eff"),
            "delta_psi": head.get("delta_psi"),
            "recent_hits": head.get("recent_hits"),
            "S_final": head.get("S_final"),
            "observer_boost": head.get("observer_boost"),
            "compression_ratio": head.get("compression_ratio"),
            "reconstruction_fidelity": head.get("reconstruction_fidelity"),
            "intelligence_score": head.get("intelligence_score"),
            "fertile": head.get("fertile"),
        },
    }
    _write_summary(vendor_out, summary)

    sweep_summary: dict[str, Any] = {"ok": False}
    if sweep_path.exists():
        rows: list[dict] = []
        with sweep_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows.append(row)
        fertile = [r for r in rows if str(r.get("fertile", "")).lower() in ("true", "1", "yes")]
        sweep_summary = {
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "source_path": str(sweep_path),
            "row_count": len(rows),
            "fertile_count": len(fertile),
            "optimal_D_eff_12_fertile": sum(
                1 for r in fertile if int(r.get("D_eff") or 0) == 12
            ),
        }
        _write_summary(sweep_out, sweep_summary)

    return {
        "ok": True,
        "summary": summary,
        "sweep_summary": sweep_summary,
        "vendor_path": str(vendor_out),
    }


def ingest_vibrafsot_progress(
    desktop_rel: str = "VibraFSOT/artifacts/vibrafsot_final_progress.json",
    vendor_out: Path | None = None,
) -> dict[str, Any]:
    src = _desktop_path(desktop_rel)
    vendor_out = vendor_out or ROOT / "vendor/fringe_desktop/vibrafsot_progress_summary.json"
    if not src.exists():
        return {"ok": False, "error": f"missing {src}"}
    doc = _read_json(src)
    trials = doc.get("vib_trials") or []
    head = trials[0] if trials else {}
    meta = doc.get("metadata") or {}
    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(src),
        "trial_count": len(trials),
        "base_freq_hz": meta.get("base_freq_hz"),
        "d_eff": meta.get("d_eff"),
        "headline": {
            "pattern_stability": head.get("pattern_stability"),
            "avg_S": head.get("avg_S"),
            "stability": head.get("stability"),
            "effective_frequency_hz": (head.get("std_units") or {}).get("effective_frequency_hz"),
            "fsot_validation_score": (head.get("std_units") or {}).get("fsot_validation_score"),
        },
    }
    _write_summary(vendor_out, summary)
    return {"ok": True, "summary": summary, "vendor_path": str(vendor_out)}


def ingest_symbolic_encoding_graph(
    desktop_rel: str = (
        "Fluid spacetime omni-theory, FSOT, and the Holy Bible"
        "/analysis/religious/fsot_mythology_graph.json"
    ),
    vendor_out: Path | None = None,
    cache_copy_name: str = "symbolic_encoding/fsot_mythology_graph.json",
) -> dict[str, Any]:
    src = _desktop_path(desktop_rel)
    vendor_out = vendor_out or ROOT / "vendor/fringe_desktop/symbolic_encoding_graph_summary.json"
    if not src.exists():
        return {"ok": False, "error": f"missing {src}"}
    graph = _read_json(src)
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    archetypes: dict[str, list[float]] = {}
    sources: set[str] = set()
    for node in nodes:
        arch = str(node.get("myth_pattern_archetype") or "unknown")
        archetypes.setdefault(arch, []).append(float(node.get("S") or 0.0))
        sources.add(str(node.get("source") or ""))
    arch_stats = {
        k: {"count": len(v), "mean_S": sum(v) / len(v) if v else 0.0}
        for k, v in sorted(archetypes.items())
    }
    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_path": str(src),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "source_corpus_count": len(sources),
        "archetype_stats": arch_stats,
    }
    _write_summary(vendor_out, summary)

    cache = cache_root()
    cache.mkdir(parents=True, exist_ok=True)
    cache_path = cache / cache_copy_name
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, cache_path)
    summary["cache_path"] = str(cache_path)
    _write_summary(vendor_out, summary)
    return {"ok": True, "summary": summary, "vendor_path": str(vendor_out), "cache_path": str(cache_path)}


def load_vendor_summary(name: str) -> dict[str, Any]:
    path = ROOT / "vendor" / "fringe_desktop" / name
    if not path.exists():
        return {}
    return _read_json(path)