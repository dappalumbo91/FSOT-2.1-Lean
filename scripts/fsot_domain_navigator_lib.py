"""Shared FSOT domain navigator — query, scientific metadata, reproduction bundles."""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data" / "fsot_domain_navigator.json"
DB_PATH = ROOT / "data" / "fsot_domain_navigator.db"
MANIFEST_PATH = ROOT / "data" / "extension_domains_manifest.yaml"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_navigator(*, rebuild: bool = False) -> dict:
    if rebuild or not JSON_PATH.exists():
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_fsot_domain_navigator_db.py"), "--no-html"], cwd=ROOT)
    return _load_json(JSON_PATH)


def load_manifest() -> dict[str, dict]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required") from exc
    doc = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    return doc.get("extension_domains") or {}


def scientific_summary_from_benchmark(bench_path: Path) -> dict[str, Any]:
    if not bench_path.is_file():
        return {"benchmark_exists": False, "benchmark_path": str(bench_path)}
    doc = _load_json(bench_path)
    sota = doc.get("sota_comparison") or {}
    baselines = sota.get("operational_baselines") or {}
    sota_models = [v.get("sota_model") for v in baselines.values() if isinstance(v, dict)]
    sources = doc.get("source") or []
    if isinstance(sources, str):
        sources = [sources]
    rel_sources = []
    for s in sources:
        p = Path(str(s))
        if p.is_absolute():
            try:
                rel_sources.append(str(p.relative_to(ROOT)))
            except ValueError:
                rel_sources.append(str(s))
        else:
            rel_sources.append(str(s))
    return {
        "benchmark_exists": True,
        "benchmark_path": str(bench_path.relative_to(ROOT)).replace("\\", "/"),
        "domain": doc.get("domain"),
        "record_count": doc.get("record_count") or doc.get("observable_count"),
        "pooled_median_error_pct": doc.get("pooled_median_error_pct") or doc.get("median_error_pct"),
        "generated_at": doc.get("generated_at"),
        "maps_to_lean": doc.get("maps_to_lean") or [],
        "D_eff": doc.get("D_eff"),
        "sources": rel_sources,
        "sota_models": [m for m in sota_models if m],
        "beats_sota": (sota.get("beats_sota_summary") or {}),
        "authority_path": doc.get("authority_path"),
    }


def enrich_panel(panel: str, cfg: dict | None = None) -> dict[str, Any]:
    ext = load_manifest()
    cfg = cfg or ext.get(panel) or {}
    bench_rel = cfg.get("benchmark_data") or ""
    bench_path = ROOT / bench_rel if bench_rel else Path()
    sci = scientific_summary_from_benchmark(bench_path)
    return {
        "panel": panel,
        "tier": cfg.get("tier"),
        "routes_to_core": cfg.get("routes_to_core"),
        "lean_module": cfg.get("lean_module"),
        "maps_to_lean": cfg.get("maps_to_lean") or sci.get("maps_to_lean") or [],
        "ingest_script": cfg.get("ingest_script"),
        "build_script": cfg.get("build_script") or cfg.get("benchmark_script"),
        "manifest": cfg.get("manifest"),
        "scientific": sci,
        "reproduce": {
            "ingest": f"python {cfg['ingest_script']} --deep" if cfg.get("ingest_script") else None,
            "build": f"python {cfg['build_script']} --skip-ingest" if cfg.get("build_script") else None,
            "verify_panel": f"python scripts/reproduce_domain_panel.py --panel {panel}",
            "verify_all_extensions": "python scripts/verify_extension_domains.py",
        },
    }


def search_fts(query: str, *, limit: int = 25) -> list[dict]:
    if not DB_PATH.exists():
        load_navigator()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT kind, name, core_domain, keywords, lean_module, tags
        FROM search_fts
        WHERE search_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """,
        (query.strip(), limit),
    ).fetchall()
    cols = [d[0] for d in cur.description or []]
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


def search_json(doc: dict, query: str, *, kind: str | None = None) -> list[dict]:
    tokens = [t for t in re.split(r"\s+", query.lower()) if t]
    hits: list[dict] = []
    for row in doc.get("extension_panels") or []:
        if kind and kind != "panel":
            continue
        hay = " ".join(
            [
                row.get("panel", ""),
                row.get("routes_to_core", ""),
                row.get("lean_module", ""),
                " ".join(row.get("maps_to_lean") or []),
                " ".join(row.get("tags") or []),
            ]
        ).lower()
        if not tokens or all(t in hay for t in tokens):
            hits.append({"kind": "panel", "name": row["panel"], "core_domain": row.get("routes_to_core")})
    for row in doc.get("core_domains") or []:
        if kind and kind != "core":
            continue
        hay = f"{row.get('name')} {row.get('breadth_note')} {' '.join(row.get('labs') or [])}".lower()
        if not tokens or all(t in hay for t in tokens):
            hits.append({"kind": "core", "name": row["name"], "core_domain": row["name"]})
    for row in doc.get("problem_routes") or []:
        if kind and kind != "intent":
            continue
        hay = " ".join([row.get("intent", ""), row.get("core_domain", ""), " ".join(row.get("keywords") or [])]).lower()
        if not tokens or all(t in hay for t in tokens):
            hits.append({"kind": "intent", "name": row["intent"], "core_domain": row.get("core_domain")})
    return hits


def panels_for_core(doc: dict, core: str) -> list[str]:
    return list((doc.get("by_core_domain") or {}).get(core) or [])


def problem_route(doc: dict, intent: str) -> dict | None:
    for row in doc.get("problem_routes") or []:
        if row.get("intent") == intent:
            return row
    return None


def build_repro_bundle(
    *,
    core: str | None = None,
    intent: str | None = None,
    panel: str | None = None,
    query: str | None = None,
) -> dict[str, Any]:
    doc = load_navigator()
    ext = load_manifest()
    panel_names: list[str] = []

    if panel:
        panel_names = [panel]
    elif intent:
        route = problem_route(doc, intent)
        if not route:
            raise SystemExit(f"Unknown intent: {intent}")
        panel_names = list(route.get("panels") or [])
        core = route.get("core_domain")
    elif core:
        panel_names = panels_for_core(doc, core)
    elif query:
        for hit in search_fts(query) or search_json(doc, query):
            if hit["kind"] == "panel":
                panel_names.append(hit["name"])
            elif hit["kind"] == "core" and not panel_names:
                panel_names = panels_for_core(doc, hit["name"])[:12]
        panel_names = list(dict.fromkeys(panel_names))
    else:
        raise SystemExit("Specify --core, --intent, --panel, or --query")

    panels_detail = []
    file_manifest: list[str] = []
    external_sources: list[str] = []
    for name in panel_names:
        if name not in ext and name not in {c["name"] for c in doc.get("core_domains") or []}:
            continue
        if name in ext:
            detail = enrich_panel(name, ext[name])
            panels_detail.append(detail)
            sci = detail.get("scientific") or {}
            if sci.get("benchmark_path"):
                file_manifest.append(sci["benchmark_path"])
            for src in sci.get("sources") or []:
                src_path = Path(src)
                if not src_path.is_absolute():
                    src_path = ROOT / src_path
                try:
                    rel = src_path.relative_to(ROOT)
                    if src_path.is_file():
                        file_manifest.append(str(rel).replace("\\", "/"))
                except ValueError:
                    if src_path.is_file():
                        external_sources.append(str(src_path))
            for key in ("ingest_script", "build_script", "manifest"):
                val = detail.get(key) or (ext[name].get(key))
                if val and (ROOT / val).exists():
                    file_manifest.append(str(val).replace("\\", "/"))

    slug = panel or intent or core or re.sub(r"[^a-z0-9]+", "_", (query or "bundle").lower()).strip("_")
    commands = ["python scripts/verify_extension_domains.py"]
    ingest_scripts = sorted({p["reproduce"]["ingest"] for p in panels_detail if p["reproduce"].get("ingest")})
    build_scripts = sorted({p["reproduce"]["build"] for p in panels_detail if p["reproduce"].get("build")})
    commands = ingest_scripts + build_scripts + commands

    total_records = sum((p.get("scientific") or {}).get("record_count") or 0 for p in panels_detail)

    return {
        "bundle_id": slug,
        "core_domain": core,
        "intent": intent,
        "query": query,
        "panel_count": len(panels_detail),
        "total_empirical_records": total_records,
        "panels": panels_detail,
        "file_manifest": sorted(set(file_manifest)),
        "external_sources": sorted(set(external_sources)),
        "reproduce_commands": commands,
        "citation": {
            "repository": "https://github.com/dappalumbo91/FSOT-2.1-Lean",
            "navigator_index": "data/fsot_domain_navigator.json",
            "verification_standard": "Per-record numeric precision + Lean certificate; 0 sorry",
        },
    }