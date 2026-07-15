#!/usr/bin/env python3
"""Build FSOT domain navigator — queryable index for discovery by domain and problem intent.

Produces:
  data/fsot_domain_navigator.db   — SQLite + FTS5 (local browse/query)
  data/fsot_domain_navigator.json — portable index for GitHub consumers without SQLite

This is a verification/discovery layer on top of extension_domains_manifest.yaml and
scientific_domain_expansion_map.json. It does not replace FSOT_UNIFIED.db (formula corpus).
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "fsot_domain_navigator.db"
JSON_PATH = ROOT / "data" / "fsot_domain_navigator.json"

# Curated problem-intent routes (keyword → core domain + exemplar panels)
PROBLEM_ROUTES: list[dict] = [
    {
        "intent": "superconductivity_tc",
        "keywords": ["superconductivity", "tc", "cuprate", "bcs", "critical temperature"],
        "core_domain": "Condensed_Matter",
        "panels": ["Condensed_Matter_Superconductivity_Depth_Panel", "Quantum_Materials"],
    },
    {
        "intent": "quantum_entanglement",
        "keywords": ["entanglement", "bell", "decoherence", "measurement", "epr"],
        "core_domain": "Quantum_Mechanics",
        "panels": ["Quantum_Mechanics_Entanglement_Depth_Panel", "Quantum_Computing_Math_Depth_Panel"],
    },
    {
        "intent": "developmental_biology",
        "keywords": ["developmental", "embryogenesis", "gestation", "neurulation", "structural biology"],
        "core_domain": "Biology",
        "panels": ["Biology_Developmental_Structural_Depth_Panel", "Genomics"],
    },
    {
        "intent": "psychometrics_rct",
        "keywords": ["psychometrics", "cronbach", "rct", "clinical trial", "cognition", "effect size"],
        "core_domain": "Psychology",
        "panels": ["Psychology_Psychometrics_Depth_Panel", "Neuroscience_Connectomics_Depth_Panel"],
    },
    {
        "intent": "materials_mechanics",
        "keywords": ["creep", "fracture", "yield", "modulus", "fatigue"],
        "core_domain": "Materials_Science",
        "panels": ["Materials_Creep_Fracture_Depth_Panel", "Materials_Project"],
    },
    {
        "intent": "neuroscience_connectomics",
        "keywords": ["connectomics", "neuron", "firing", "openneuro", "brain"],
        "core_domain": "Neuroscience",
        "panels": ["Neuroscience_Connectomics_Depth_Panel"],
    },
    {
        "intent": "optics_interferometry",
        "keywords": ["ligo", "interferometry", "jwst", "wavelength", "strain sensitivity"],
        "core_domain": "Optics",
        "panels": ["Optics_Interferometry_Depth_Panel"],
    },
    {
        "intent": "fluid_dynamics",
        "keywords": ["turbulence", "navier", "reynolds", "cfd", "fluid"],
        "core_domain": "Fluid_Dynamics",
        "panels": ["Fluid_Dynamics", "Fluid_Spacetime"],
    },
    {
        "intent": "formal_proof",
        "keywords": ["lean", "coq", "proof", "sorry", "transcendental", "structural spine"],
        "core_domain": "Pure_Mathematics",
        "panels": ["Certified_Agent_Formal_Panel", "Rust_Lean_Bridge_Panel", "Early_Lean_MC_Panel"],
    },
    {
        "intent": "desktop_application",
        "keywords": ["desktop", "tokenization", "decoder", "oracle", "solver", "bibliography"],
        "core_domain": "Computer_Science",
        "panels": [
            "Tokenization_Live_Panel",
            "Binary_Decoder_Panel",
            "Bibliography_Corpus_Panel",
            "Canonical_Oracle_Panel",
            "Scalar_Solver_35_Panel",
            "VL_Agent_Distill_Panel",
            "Physarum_Biological_CUDA_Panel",
        ],
    },
    {
        "intent": "cosmology_cmb",
        "keywords": ["cmb", "hubble", "lambda cdm", "dark energy", "inflation"],
        "core_domain": "Cosmology",
        "panels": ["Cosmology_Extended", "Cosmology"],
    },
    {
        "intent": "climate_paleo",
        "keywords": ["climate", "ice core", "temperature anomaly", "co2", "paleo"],
        "core_domain": "Atmospheric_Physics",
        "panels": ["Climate_Science"],
    },
    {
        "intent": "particle_physics",
        "keywords": ["higgs", "pdg", "cross section", "cern", "standard model"],
        "core_domain": "Particle_Physics",
        "panels": ["Particle_Physics", "Higgs_Mass"],
    },
    {
        "intent": "seismology",
        "keywords": ["earthquake", "magnitude", "usgs", "moment tensor"],
        "core_domain": "Seismology",
        "panels": ["Seismology"],
    },
    {
        "intent": "consciousness",
        "keywords": ["consciousness", "observer", "microtubule", "species"],
        "core_domain": "Psychology",
        "panels": [
            "Observer_Effect_Cross_Species_Panel",
            "Microtubule_Quantum_Consciousness_Panel",
            "Consciousness_Species_Multi_Panel",
        ],
    },
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _slug_tokens(name: str) -> list[str]:
    return [t for t in re.split(r"[_\s]+", name.lower()) if len(t) > 2]


def _infer_core_domain(panel: str, cfg: dict, exp_by_name: dict) -> str:
    if cfg.get("routes_to_core"):
        return str(cfg["routes_to_core"])
    exp = exp_by_name.get(panel) or {}
    lean = str(exp.get("lean_domain") or "")
    if lean:
        return lean
    # Heuristic from panel name
    for core in (
        "Quantum_Mechanics",
        "Condensed_Matter",
        "Biology",
        "Psychology",
        "Neuroscience",
        "Materials_Science",
        "Optics",
        "Cosmology",
        "Fluid_Dynamics",
        "Particle_Physics",
        "Computer_Science",
    ):
        if core.lower().replace("_", "") in panel.lower().replace("_", ""):
            return core
    maps = cfg.get("maps_to_lean") or []
    map_to_core = {
        "biological": "Biology",
        "medical": "Biochemistry",
        "neural": "Neuroscience",
        "quantum": "Quantum_Mechanics",
        "material": "Materials_Science",
        "astronomical": "Astronomy",
        "galactic": "Astrophysics",
        "energy": "Thermodynamics",
        "consciousness": "Psychology",
        "ai": "Computer_Science",
        "mathematical": "Pure_Mathematics",
    }
    for tag in maps:
        if tag in map_to_core:
            return map_to_core[tag]
    return "General"


def _download_bundle(cfg: dict) -> dict:
    return {
        "benchmark_data": cfg.get("benchmark_data"),
        "ingest_script": cfg.get("ingest_script"),
        "build_script": cfg.get("build_script") or cfg.get("benchmark_script"),
        "manifest": cfg.get("manifest"),
        "lean_module": cfg.get("lean_module"),
    }


def _field_breadth() -> dict:
    try:
        import audit_full_system_coverage as audit  # noqa: WPS433

        return audit.FIELD_BREADTH
    except Exception:
        return {}


def build_navigator() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")

    ext_doc = yaml.safe_load((ROOT / "data" / "extension_domains_manifest.yaml").read_text(encoding="utf-8"))
    ext = ext_doc.get("extension_domains") or {}
    sci = _load_json(ROOT / "data" / "scientific_domain_expansion_map.json")
    crosswalk = _load_json(ROOT / "data" / "desktop_project_crosswalk.json")
    breadth = _field_breadth()

    exp_ext = {d["domain"]: d for d in (sci.get("extension_domains") or [])}
    exp_core = {d["domain"]: d for d in (sci.get("neurolab_domains") or [])}

    core_domains: list[dict] = []
    for name, row in sorted(exp_core.items()):
        fb = breadth.get(name, {})
        studied = int(fb.get("studied_subfields") or 0)
        touched = int(fb.get("touched") or 0)
        core_domains.append(
            {
                "name": name,
                "lean_domain": row.get("lean_domain"),
                "empirical_records": row.get("empirical_records"),
                "median_error_pct": row.get("median_error_pct"),
                "coverage_tier": row.get("coverage_tier"),
                "breadth_pct": round(100.0 * touched / studied, 1) if studied else None,
                "subfields_touched": touched,
                "subfields_studied": studied,
                "breadth_note": fb.get("note"),
                "labs": row.get("labs") or [],
            }
        )

    extension_panels: list[dict] = []
    by_core: dict[str, list[str]] = {}
    for panel, cfg in sorted(ext.items()):
        exp = exp_ext.get(panel) or {}
        core = _infer_core_domain(panel, cfg, exp_core)
        tier_band = exp.get("coverage_tier") or "unverified"
        entry = {
            "panel": panel,
            "tier": cfg.get("tier"),
            "routes_to_core": core,
            "record_count": exp.get("record_count"),
            "median_error_pct": exp.get("median_error_pct"),
            "coverage_tier": tier_band,
            "lean_module": cfg.get("lean_module") or exp.get("lean_module"),
            "maps_to_lean": cfg.get("maps_to_lean") or [],
            "tags": _slug_tokens(panel),
            "download_bundle": _download_bundle(cfg),
        }
        extension_panels.append(entry)
        by_core.setdefault(core, []).append(panel)

    subfields: list[dict] = []
    for name, fb in sorted(breadth.items()):
        studied = int(fb.get("studied_subfields") or 0)
        touched = int(fb.get("touched") or 0)
        subfields.append(
            {
                "core_domain": name,
                "subfields_studied": studied,
                "subfields_touched": touched,
                "breadth_pct": round(100.0 * touched / studied, 1) if studied else None,
                "note": fb.get("note"),
            }
        )

    problem_routes: list[dict] = []
    panel_set = set(ext.keys())
    for route in PROBLEM_ROUTES:
        panels = [p for p in route["panels"] if p in panel_set or p in exp_core]
        if not panels:
            panels = [
                p["panel"]
                for p in extension_panels
                if p["routes_to_core"] == route["core_domain"]
            ][:5]
        bundles = []
        for p in panels:
            if p in ext:
                bundles.append({"panel": p, **_download_bundle(ext[p])})
            elif p in exp_core:
                bundles.append({"panel": p, "benchmark_data": f"data/{p.lower()}_benchmark.json"})
        problem_routes.append(
            {
                "intent": route["intent"],
                "keywords": route["keywords"],
                "core_domain": route["core_domain"],
                "panels": panels,
                "download_bundles": bundles,
            }
        )

    desktop_projects = [
        {
            "folder": p.get("folder"),
            "theme": p.get("theme"),
            "theme_label": p.get("theme_label"),
            "lean_lab": p.get("lean_lab"),
            "wire_status": p.get("wire_status"),
        }
        for p in (crosswalk.get("projects") or [])
        if p.get("exists")
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "summary": {
            "core_domains": len(core_domains),
            "extension_panels": len(extension_panels),
            "problem_routes": len(problem_routes),
            "desktop_projects": len(desktop_projects),
            "total_empirical_records": sci.get("summary", {}).get("total_empirical_records"),
            "c_thin_panels": sci.get("summary", {}).get("tier_distribution", {}).get("C_thin"),
        },
        "core_domains": core_domains,
        "extension_panels": extension_panels,
        "by_core_domain": {k: sorted(v) for k, v in sorted(by_core.items())},
        "subfields": subfields,
        "problem_routes": problem_routes,
        "desktop_projects": desktop_projects,
        "reproduce": "python scripts/build_fsot_domain_navigator_db.py",
        "query_example": 'python scripts/build_fsot_domain_navigator_db.py --query "entanglement"',
    }


def _write_sqlite(doc: dict, db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE core_domains (
            name TEXT PRIMARY KEY,
            lean_domain TEXT,
            empirical_records INTEGER,
            median_error_pct REAL,
            coverage_tier TEXT,
            breadth_pct REAL,
            breadth_note TEXT
        );
        CREATE TABLE extension_panels (
            panel TEXT PRIMARY KEY,
            tier INTEGER,
            routes_to_core TEXT,
            record_count INTEGER,
            median_error_pct REAL,
            coverage_tier TEXT,
            lean_module TEXT,
            benchmark_path TEXT,
            ingest_script TEXT,
            build_script TEXT,
            maps_to_lean TEXT,
            tags TEXT
        );
        CREATE TABLE subfields (
            core_domain TEXT PRIMARY KEY,
            subfields_studied INTEGER,
            subfields_touched INTEGER,
            breadth_pct REAL,
            note TEXT
        );
        CREATE TABLE problem_routes (
            intent TEXT PRIMARY KEY,
            keywords TEXT,
            core_domain TEXT,
            panels TEXT
        );
        CREATE TABLE desktop_projects (
            folder TEXT PRIMARY KEY,
            theme TEXT,
            theme_label TEXT,
            lean_lab TEXT,
            wire_status TEXT
        );
        CREATE VIRTUAL TABLE search_fts USING fts5(
            kind UNINDEXED,
            name,
            core_domain,
            keywords,
            lean_module,
            tags,
            tokenize='porter'
        );
        """
    )

    def _fts_insert(kind: str, name: str, core: str, keywords: str, lean: str, tags: str) -> None:
        cur.execute(
            "INSERT INTO search_fts(kind, name, core_domain, keywords, lean_module, tags) "
            "VALUES (?,?,?,?,?,?)",
            (kind, name, core, keywords, lean, tags),
        )

    for row in doc["core_domains"]:
        cur.execute(
            "INSERT INTO core_domains VALUES (?,?,?,?,?,?,?)",
            (
                row["name"],
                row.get("lean_domain"),
                row.get("empirical_records"),
                row.get("median_error_pct"),
                row.get("coverage_tier"),
                row.get("breadth_pct"),
                row.get("breadth_note"),
            ),
        )
        _fts_insert(
            "core",
            row["name"],
            row["name"],
            row.get("breadth_note") or "",
            "",
            "",
        )

    for row in doc["extension_panels"]:
        bundle = row.get("download_bundle") or {}
        cur.execute(
            "INSERT INTO extension_panels VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                row["panel"],
                row.get("tier"),
                row.get("routes_to_core"),
                row.get("record_count"),
                row.get("median_error_pct"),
                row.get("coverage_tier"),
                row.get("lean_module"),
                bundle.get("benchmark_data"),
                bundle.get("ingest_script"),
                bundle.get("build_script"),
                json.dumps(row.get("maps_to_lean") or []),
                " ".join(row.get("tags") or []),
            ),
        )
        _fts_insert(
            "panel",
            row["panel"],
            row.get("routes_to_core") or "",
            " ".join(row.get("tags") or []),
            row.get("lean_module") or "",
            " ".join(row.get("maps_to_lean") or []),
        )

    for row in doc["subfields"]:
        cur.execute(
            "INSERT INTO subfields VALUES (?,?,?,?,?)",
            (
                row["core_domain"],
                row.get("subfields_studied"),
                row.get("subfields_touched"),
                row.get("breadth_pct"),
                row.get("note"),
            ),
        )

    for row in doc["problem_routes"]:
        cur.execute(
            "INSERT INTO problem_routes VALUES (?,?,?,?)",
            (
                row["intent"],
                " ".join(row.get("keywords") or []),
                row.get("core_domain"),
                json.dumps(row.get("panels") or []),
            ),
        )
        _fts_insert(
            "intent",
            row["intent"],
            row.get("core_domain") or "",
            " ".join(row.get("keywords") or []),
            "",
            " ".join(row.get("panels") or []),
        )

    for row in doc["desktop_projects"]:
        cur.execute(
            "INSERT INTO desktop_projects VALUES (?,?,?,?,?)",
            (
                row.get("folder"),
                row.get("theme"),
                row.get("theme_label"),
                row.get("lean_lab"),
                row.get("wire_status"),
            ),
        )

    conn.commit()
    conn.close()


def _query_db(db_path: Path, q: str) -> list[dict]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    term = q.strip().replace('"', '""')
    rows = cur.execute(
        f"""
        SELECT kind, name, core_domain, keywords, lean_module, tags
        FROM search_fts
        WHERE search_fts MATCH ?
        ORDER BY rank
        LIMIT 25
        """,
        (term,),
    ).fetchall()
    cols = [d[0] for d in cur.description or []]
    conn.close()
    return [dict(zip(cols, row)) for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build FSOT domain navigator index")
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--json", type=Path, default=JSON_PATH)
    parser.add_argument("--query", type=str, default="", help="FTS query against built DB")
    args = parser.parse_args()

    doc = build_navigator()
    args.json.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    _write_sqlite(doc, args.db)

    print(f"Wrote {args.json}")
    print(f"Wrote {args.db}")
    print(f"  core_domains: {doc['summary']['core_domains']}")
    print(f"  extension_panels: {doc['summary']['extension_panels']}")
    print(f"  problem_routes: {doc['summary']['problem_routes']}")
    print(f"  c_thin_panels: {doc['summary']['c_thin_panels']}")

    if args.query:
        hits = _query_db(args.db, args.query)
        print(f"\nQuery '{args.query}' → {len(hits)} hits:")
        for hit in hits:
            print(f"  [{hit['kind']}] {hit['name']} → {hit['core_domain']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())