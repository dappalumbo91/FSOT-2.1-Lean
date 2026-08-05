#!/usr/bin/env python3
"""Build public citation / provenance ledger for every green residual benchmark.

For multiprover + empirical reproducibility: each panel lists the **public**
datasets, APIs, catalogs, and literature anchors used as measured targets —
not only FSOT self-citations.

Outputs:
  data/benchmark_anchor_citation_ledger.json
  docs/BENCHMARK_DATA_CITATIONS.md
  data/domain_citations/benchmark_public_anchors.bib
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
EXT_MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
API_REQ = ROOT / "data" / "api_requirements.yaml"
OUT_JSON = ROOT / "data" / "benchmark_anchor_citation_ledger.json"
OUT_MD = ROOT / "docs" / "BENCHMARK_DATA_CITATIONS.md"
OUT_BIB = ROOT / "data" / "domain_citations" / "benchmark_public_anchors.bib"

# Curated public anchors: token (normalized) → citation record
# Prefer official landing pages / DOI / stable API docs.
PUBLIC_ANCHORS: dict[str, dict[str, str]] = {
    "mpcorb": {
        "kind": "dataset",
        "title": "Minor Planet Center Orbit Database (MPCORB)",
        "publisher": "IAU Minor Planet Center / Harvard-Smithsonian CfA",
        "url": "https://minorplanetcenter.net/data",
        "note": "Full minor-planet catalog used by MPCORB panel",
    },
    "minor planet center": {
        "kind": "dataset",
        "title": "Minor Planet Center data services",
        "publisher": "IAU MPC / CFA Harvard",
        "url": "https://minorplanetcenter.net/",
    },
    "nist": {
        "kind": "dataset",
        "title": "NIST CODATA / Constants",
        "publisher": "NIST",
        "url": "https://physics.nist.gov/cuu/Constants/",
    },
    "nist_codata": {
        "kind": "dataset",
        "title": "NIST CODATA recommended values (ASCII table)",
        "publisher": "NIST",
        "url": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
    },
    "codata": {
        "kind": "dataset",
        "title": "CODATA fundamental physical constants",
        "publisher": "CODATA / NIST",
        "url": "https://physics.nist.gov/cuu/Constants/",
    },
    "pdg": {
        "kind": "dataset",
        "title": "Particle Data Group Review of Particle Physics",
        "publisher": "Particle Data Group",
        "url": "https://pdg.lbl.gov/",
    },
    "planck": {
        "kind": "dataset",
        "title": "Planck Collaboration cosmological parameters",
        "publisher": "ESA Planck",
        "url": "https://www.cosmos.esa.int/web/planck",
    },
    "gbif": {
        "kind": "api",
        "title": "GBIF Occurrence API",
        "publisher": "Global Biodiversity Information Facility",
        "url": "https://api.gbif.org/v1/",
    },
    "pubchem": {
        "kind": "api",
        "title": "PubChem PUG REST",
        "publisher": "NCBI / NLM",
        "url": "https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest",
    },
    "nasa": {
        "kind": "api",
        "title": "NASA open data portals (SSD/JPL, DONKI, Exoplanet Archive as cited per panel)",
        "publisher": "NASA",
        "url": "https://api.nasa.gov/",
    },
    "jpl": {
        "kind": "api",
        "title": "JPL Solar System Dynamics / Horizons",
        "publisher": "NASA JPL",
        "url": "https://ssd.jpl.nasa.gov/",
    },
    "horizons": {
        "kind": "api",
        "title": "JPL Horizons system",
        "publisher": "NASA JPL",
        "url": "https://ssd.jpl.nasa.gov/horizons/",
    },
    "gaia": {
        "kind": "dataset",
        "title": "Gaia DR3 catalog (ESA)",
        "publisher": "ESA Gaia / CDS TAP",
        "url": "https://gea.esac.esa.int/archive/",
    },
    "simbad": {
        "kind": "api",
        "title": "SIMBAD astronomical database",
        "publisher": "CDS Strasbourg",
        "url": "https://simbad.cds.unistra.fr/simbad/",
    },
    "usgs": {
        "kind": "api",
        "title": "USGS earthquake / water / hazards open APIs",
        "publisher": "USGS",
        "url": "https://earthquake.usgs.gov/fdsnws/event/1/",
    },
    "noaa": {
        "kind": "api",
        "title": "NOAA tides, climate, space-weather open services",
        "publisher": "NOAA",
        "url": "https://www.noaa.gov/",
    },
    "ncei": {
        "kind": "dataset",
        "title": "NOAA NCEI climate data",
        "publisher": "NOAA NCEI",
        "url": "https://www.ncei.noaa.gov/",
    },
    "world bank": {
        "kind": "api",
        "title": "World Bank Open Data Indicators API",
        "publisher": "World Bank",
        "url": "https://api.worldbank.org/v2/",
    },
    "world_bank": {
        "kind": "api",
        "title": "World Bank Open Data Indicators API",
        "publisher": "World Bank",
        "url": "https://api.worldbank.org/v2/",
    },
    "openalex": {
        "kind": "api",
        "title": "OpenAlex scholarly graph API",
        "publisher": "OurResearch",
        "url": "https://api.openalex.org/",
    },
    "arxiv": {
        "kind": "api",
        "title": "arXiv API / metadata",
        "publisher": "Cornell arXiv",
        "url": "https://arxiv.org/help/api/",
    },
    "uniprot": {
        "kind": "api",
        "title": "UniProt REST API",
        "publisher": "UniProt Consortium",
        "url": "https://www.uniprot.org/help/api",
    },
    "ensembl": {
        "kind": "api",
        "title": "Ensembl REST API",
        "publisher": "EMBL-EBI",
        "url": "https://rest.ensembl.org/",
    },
    "ncbi": {
        "kind": "api",
        "title": "NCBI E-utilities / Gene / datasets",
        "publisher": "NCBI / NLM",
        "url": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
    },
    "allen": {
        "kind": "dataset",
        "title": "Allen Institute cell types / brain atlas (as cached per panel)",
        "publisher": "Allen Institute for Brain Science",
        "url": "https://celltypes.brain-map.org/",
    },
    "rcsb": {
        "kind": "api",
        "title": "RCSB PDB REST API",
        "publisher": "RCSB Protein Data Bank",
        "url": "https://data.rcsb.org/",
    },
    "cern": {
        "kind": "dataset",
        "title": "CERN Open Data",
        "publisher": "CERN",
        "url": "https://opendata.cern.ch/",
    },
    "ssa": {
        "kind": "dataset",
        "title": "SSA Office of the Chief Actuary life tables",
        "publisher": "U.S. Social Security Administration",
        "url": "https://www.ssa.gov/oact/STATS/table4c6.html",
    },
    "kepler": {
        "kind": "dataset",
        "title": "NASA Kepler / exoplanet archives (as cited per panel)",
        "publisher": "NASA",
        "url": "https://exoplanetarchive.ipac.caltech.edu/",
    },
    "exoplanet": {
        "kind": "api",
        "title": "NASA Exoplanet Archive TAP",
        "publisher": "NASA/IPAC",
        "url": "https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html",
    },
    "desi": {
        "kind": "dataset",
        "title": "DESI cosmological results (public releases)",
        "publisher": "DESI Collaboration",
        "url": "https://data.desi.lbl.gov/",
    },
    "sh0es": {
        "kind": "literature",
        "title": "SH0ES / local distance ladder H0 (Riess et al. series)",
        "publisher": "literature",
        "url": "https://ui.adsabs.harvard.edu/",
        "note": "Contested H0 anchor — see contested sector panel",
    },
    "ads": {
        "kind": "api",
        "title": "NASA ADS / Harvard CfA bibliographic services",
        "publisher": "SAO/NASA ADS",
        "url": "https://ui.adsabs.harvard.edu/",
    },
    "harvard": {
        "kind": "dataset",
        "title": "Harvard / CfA hosted catalogs (MPC, ADS as cited)",
        "publisher": "Harvard-Smithsonian Center for Astrophysics",
        "url": "https://www.cfa.harvard.edu/",
    },
    "bard, parsons": {
        "kind": "literature",
        "title": "Bard, Parsons & Jordan (1985) — Standard Potentials in Aqueous Solution",
        "publisher": "literature / IUPAC electrochemistry",
        "url": "https://www.routledge.com/",
        "note": "Electrochemistry reference tables used as measured anchors",
    },
    "long & greenwood": {
        "kind": "literature",
        "title": "Long & Greenwood (1997) — materials / thermoelectric class reference",
        "publisher": "literature",
        "url": "https://ui.adsabs.harvard.edu/",
        "note": "Materials panel literature anchor",
    },
    "snyder & toberer": {
        "kind": "literature",
        "title": "Snyder & Toberer, Nature Materials 7, 105 (2008)",
        "publisher": "Nature Materials",
        "url": "https://doi.org/10.1038/nmat2090",
        "note": "Thermoelectric materials review",
    },
    "anderson (1966)": {
        "kind": "literature",
        "title": "Anderson (1966) — localization / condensed-matter classic",
        "publisher": "literature",
        "url": "https://ui.adsabs.harvard.edu/",
    },
    "andersen et al., jpcrd": {
        "kind": "literature",
        "title": "Andersen et al., J. Phys. Chem. Ref. Data 28 (1999)",
        "publisher": "JPCRD / NIST",
        "url": "https://www.nist.gov/pml/journal-physical-and-chemical-reference-data",
    },
    "crc / riddick": {
        "kind": "dataset",
        "title": "CRC / Riddick organic solvents handbook class",
        "publisher": "CRC Press literature tables",
        "url": "https://www.routledge.com/",
        "note": "Handbook constants as measured targets",
    },
    "brenda": {
        "kind": "dataset",
        "title": "BRENDA enzyme database",
        "publisher": "BRENDA / TU Braunschweig",
        "url": "https://www.brenda-enzymes.org/",
    },
    "chembl": {
        "kind": "api",
        "title": "ChEMBL API",
        "publisher": "EMBL-EBI",
        "url": "https://www.ebi.ac.uk/chembl/",
    },
    "open-meteo": {
        "kind": "api",
        "title": "Open-Meteo weather API / archive",
        "publisher": "Open-Meteo",
        "url": "https://open-meteo.com/",
    },
    "openssl": {
        "kind": "dataset",
        "title": "OpenSSL source corpus (GitHub OSS genome)",
        "publisher": "OpenSSL Project",
        "url": "https://github.com/openssl/openssl",
    },
    "torvalds/linux": {
        "kind": "dataset",
        "title": "Linux kernel source corpus (GitHub OSS genome)",
        "publisher": "Linux kernel",
        "url": "https://github.com/torvalds/linux",
    },
    "rust-lang/rust": {
        "kind": "dataset",
        "title": "Rust compiler source corpus",
        "publisher": "Rust Project",
        "url": "https://github.com/rust-lang/rust",
    },
    "python/cpython": {
        "kind": "dataset",
        "title": "CPython source corpus",
        "publisher": "Python Software Foundation",
        "url": "https://github.com/python/cpython",
    },
    "nodejs/node": {
        "kind": "dataset",
        "title": "Node.js source corpus",
        "publisher": "OpenJS Foundation",
        "url": "https://github.com/nodejs/node",
    },
    "formula_corpus": {
        "kind": "dataset",
        "title": "FSOT strict empirical formula corpus (in-repo)",
        "publisher": "FSOT-2.1-Lean vendor cache",
        "url": "https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/vendor/formula_corpus",
        "note": "Seed formulas vs public target_quantity; not a free-param fit store",
    },
    "strict_empirical": {
        "kind": "dataset",
        "title": "vendor/formula_corpus/by_domain/strict_empirical.jsonl",
        "publisher": "FSOT-2.1-Lean",
        "url": "https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/formula_corpus/by_domain/strict_empirical.jsonl",
    },
    "fsot_compute": {
        "kind": "software",
        "title": "FSOT scalar authority (pin D1D38A)",
        "publisher": "FSOT-2.1-Lean",
        "url": "https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/vendor/fsot_compute.py",
    },
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _load_api_registry() -> list[dict[str, str]]:
    if not API_REQ.exists() or yaml is None:
        return []
    doc = yaml.safe_load(API_REQ.read_text(encoding="utf-8")) or {}
    rows: list[dict[str, str]] = []
    for family, block in (doc.get("api_sources") or {}).items():
        for src in block.get("sources") or []:
            if not isinstance(src, dict):
                continue
            rows.append(
                {
                    "id": str(src.get("id") or ""),
                    "kind": "api",
                    "title": str(src.get("id") or family),
                    "url": str(src.get("url") or ""),
                    "family": family,
                    "auth": str(src.get("auth") or "none"),
                    "note": str(src.get("note") or block.get("description") or ""),
                }
            )
    return rows


def _load_open_sources() -> list[dict[str, str]]:
    try:
        from open_science_sources_lib import OPEN_SOURCES  # noqa: WPS433
    except Exception:
        return []
    return [
        {
            "id": s.id,
            "kind": "api",
            "title": s.description,
            "url": s.url,
            "family": s.family,
            "auth": s.auth,
            "note": s.notes,
        }
        for s in OPEN_SOURCES
    ]


def _resolve_token(token: str, api_index: dict[str, dict], open_index: dict[str, dict]) -> dict[str, str] | None:
    t = _norm(token)
    process_tags = (
        "c_thin_depth_pass",
        "fsot_proper_densify",
        "fsot_proper_green_remediation",
        "fsot_proper_densify_remediation",
        "fsot_proper_hardware_clean",
        "fsot_proper_spine_clean",
        "extension_domains_manifest",
    )
    if not t or t in process_tags or t in (".", "y", "2", "literature"):
        return {
            "kind": "process",
            "title": token,
            "note": "internal densify/process/noise tag — not a measurement authority",
        }
    # GitHub owner/repo corpora
    if re.fullmatch(r"[a-z0-9_.-]+/[a-z0-9_.-]+", t):
        return {
            "kind": "dataset",
            "title": f"GitHub OSS corpus {token}",
            "url": f"https://github.com/{token}",
            "note": "Code-genome / OSS structure panel source",
        }
    # path-like vendor/data
    if "strict_empirical" in t or "formula_corpus" in t:
        return dict(PUBLIC_ANCHORS["strict_empirical"])
    if "fsot_compute" in t:
        return dict(PUBLIC_ANCHORS["fsot_compute"])
    if t.endswith(".json") or t.endswith(".yaml") or t.startswith("data/") or t.startswith("vendor/"):
        return {
            "kind": "vendor_cache",
            "title": token,
            "url": f"https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/{token.replace(chr(92), '/')}",
            "note": "In-repo portable cache; rebuild path in ingest scripts / api_requirements.yaml",
        }
    # direct curated
    for key, rec in PUBLIC_ANCHORS.items():
        if key in t or t in key:
            out = dict(rec)
            out["matched_token"] = token
            return out
    # api registry id
    if t in api_index:
        r = dict(api_index[t])
        r["matched_token"] = token
        return r
    for aid, rec in api_index.items():
        if aid and aid in t:
            r = dict(rec)
            r["matched_token"] = token
            return r
    if t in open_index:
        r = dict(open_index[t])
        r["matched_token"] = token
        return r
    # URL
    if t.startswith("http://") or t.startswith("https://"):
        return {"kind": "url", "title": token, "url": token.strip()}
    return {
        "kind": "unresolved",
        "title": token,
        "note": "Named in panel source; add explicit public URL if this is an external authority",
    }


def _bench_paths_from_margin() -> list[Path]:
    paths: list[Path] = []
    if MARGIN.exists():
        doc = json.loads(MARGIN.read_text(encoding="utf-8"))
        for row in doc.get("all_domains") or []:
            if not isinstance(row, dict):
                continue
            rel = row.get("file") or row.get("benchmark_file") or row.get("path")
            if rel:
                p = ROOT / "data" / rel if not str(rel).startswith("data") else ROOT / rel
                if not p.exists():
                    p = ROOT / "data" / Path(rel).name
                if p.exists():
                    paths.append(p)
    if paths:
        return sorted(set(paths))
    # fallback: all data/*benchmark*.json
    return sorted(ROOT.joinpath("data").glob("*benchmark*.json"))


def _collect_source_tokens(bench: dict) -> list[str]:
    tokens: list[str] = []
    src = bench.get("source")
    if isinstance(src, list):
        tokens.extend(str(x) for x in src if x)
    elif isinstance(src, str) and src.strip():
        tokens.append(src.strip())
    for key in ("sources", "data_sources", "provenance", "citations", "reference"):
        val = bench.get(key)
        if isinstance(val, list):
            tokens.extend(str(x) for x in val if x)
        elif isinstance(val, str) and val.strip():
            tokens.append(val.strip())
    # record-level verification_citations (sample up to 20 unique)
    seen: set[str] = set()
    for rec in (bench.get("material_records") or bench.get("records") or [])[:500]:
        if not isinstance(rec, dict):
            continue
        vc = rec.get("verification_citations") or rec.get("citations") or rec.get("source")
        if isinstance(vc, list):
            for item in vc:
                s = str(item)
                if s not in seen:
                    seen.add(s)
                    tokens.append(s)
        elif isinstance(vc, str) and vc not in seen:
            seen.add(vc)
            tokens.append(vc)
        if len(seen) >= 40:
            break
    # dedupe preserve order
    out: list[str] = []
    hit: set[str] = set()
    for t in tokens:
        k = _norm(t)
        if k in hit:
            continue
        hit.add(k)
        out.append(t)
    return out


def build() -> dict[str, Any]:
    api_rows = _load_api_registry()
    open_rows = _load_open_sources()
    api_index = { _norm(r["id"]): r for r in api_rows if r.get("id") }
    open_index = { _norm(r["id"]): r for r in open_rows if r.get("id") }

    ext_map: dict[str, dict] = {}
    if yaml and EXT_MANIFEST.exists():
        ext_map = yaml.safe_load(EXT_MANIFEST.read_text(encoding="utf-8")).get("extension_domains") or {}

    panels: list[dict[str, Any]] = []
    global_anchors: dict[str, dict[str, Any]] = {}
    kind_counts: Counter[str] = Counter()
    unresolved: Counter[str] = Counter()

    for path in _bench_paths_from_margin():
        try:
            bench = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        domain = str(bench.get("domain") or path.stem)
        tokens = _collect_source_tokens(bench)
        # attach ingest/build from extension manifest when domain matches
        cfg = ext_map.get(domain) or {}
        if cfg.get("ingest_script"):
            tokens.append(f"ingest:{cfg['ingest_script']}")
        resolved: list[dict[str, str]] = []
        for tok in tokens:
            if tok.startswith("ingest:"):
                resolved.append(
                    {
                        "kind": "ingest_script",
                        "title": tok.split(":", 1)[1],
                        "url": f"https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/{tok.split(':',1)[1]}",
                        "note": "Rebuild path for live public fetch when network available",
                    }
                )
                kind_counts["ingest_script"] += 1
                continue
            rec = _resolve_token(tok, api_index, open_index)
            if rec is None:
                continue
            kind_counts[rec.get("kind", "unknown")] += 1
            if rec.get("kind") == "unresolved":
                unresolved[tok] += 1
            resolved.append(rec)
            # index global unique by title+url
            key = _norm(rec.get("url") or rec.get("title") or tok)
            if key not in global_anchors:
                global_anchors[key] = {**rec, "panels": [domain], "token_examples": [tok]}
            else:
                if domain not in global_anchors[key]["panels"]:
                    global_anchors[key]["panels"].append(domain)
                if tok not in global_anchors[key]["token_examples"] and len(global_anchors[key]["token_examples"]) < 5:
                    global_anchors[key]["token_examples"].append(tok)

        panels.append(
            {
                "domain": domain,
                "benchmark_file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "record_count": bench.get("record_count") or bench.get("observable_count"),
                "pooled_median_error_pct": bench.get("pooled_median_error_pct") or bench.get("median_error_pct"),
                "source_tokens": tokens,
                "public_anchors": resolved,
                "maps_to_lean": bench.get("maps_to_lean"),
                "lean_module": cfg.get("lean_module"),
                "ingest_script": cfg.get("ingest_script"),
                "build_script": cfg.get("build_script") or cfg.get("benchmark_script"),
            }
        )

    # Always include full API registry + open sources as global index
    registry_catalog = {
        "api_requirements_sources": api_rows,
        "open_science_no_key_sources": open_rows,
    }

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": (
            "Public provenance for residual benchmarks used in multiprover green gates. "
            "Each panel lists datasets/APIs/literature anchors so independent readers can "
            "reproduce measured targets without private data."
        ),
        "policy": {
            "full_catalog": "Cite catalog as one dataset (e.g. MPCORB / Harvard-hosted MPC)",
            "individual": "List each distinct public source token when not a bulk catalog",
            "api": "List API base URL + id from data/api_requirements.yaml",
            "vendor_cache": "Portable path is listed; live rebuild uses ingest scripts",
        },
        "summary": {
            "panels_scanned": len(panels),
            "unique_public_anchors": len(global_anchors),
            "kind_counts": dict(kind_counts),
            "unresolved_token_count": len(unresolved),
            "unresolved_top": unresolved.most_common(40),
            "api_registry_entries": len(api_rows),
            "open_science_entries": len(open_rows),
        },
        "global_anchors": sorted(global_anchors.values(), key=lambda r: (r.get("kind") or "", r.get("title") or "")),
        "registry_catalog": registry_catalog,
        "panels": sorted(panels, key=lambda p: p["domain"]),
    }
    return doc


def write_markdown(doc: dict[str, Any]) -> None:
    s = doc["summary"]
    lines = [
        "# Benchmark data citations & public anchors",
        "",
        f"**Generated:** `{doc['generated_at']}`  ",
        f"**Panels scanned:** {s['panels_scanned']}  ",
        f"**Unique resolved anchors:** {s['unique_public_anchors']}  ",
        f"**API registry entries:** {s['api_registry_entries']} · open-science no-key: {s['open_science_entries']}",
        "",
        "This ledger supports **multiprover + empirical reproducibility**: measured targets ",
        "are tied to **public datasets, APIs, or literature landing pages**, not private files.",
        "",
        "## Policy",
        "",
        "| Case | How we cite |",
        "|------|-------------|",
        "| Full catalog (e.g. MPCORB / Harvard–CfA MPC) | One dataset entry + official URL |",
        "| Individual public tables | Each named source + URL when known |",
        "| Live API ingest | API id + base URL from `data/api_requirements.yaml` |",
        "| Portable vendor cache | In-repo path + ingest script to rebuild from public net |",
        "",
        "## Kind summary",
        "",
        "| Kind | Count |",
        "|------|------:|",
    ]
    for k, n in sorted((s.get("kind_counts") or {}).items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{k}` | {n} |")
    lines += [
        "",
        "## Global public anchors (deduplicated)",
        "",
        "| Kind | Title | URL / location | # panels |",
        "|------|-------|----------------|---------:|",
    ]
    for a in doc["global_anchors"]:
        if a.get("kind") in ("process",):
            continue
        url = a.get("url") or a.get("note") or ""
        title = (a.get("title") or "").replace("|", "/")
        url = url.replace("|", "/")
        n = len(a.get("panels") or [])
        lines.append(f"| {a.get('kind')} | {title} | {url} | {n} |")

    lines += [
        "",
        "## Unresolved source tokens (need explicit public URL)",
        "",
        "These strings appear in panel `source` fields but were not mapped to a known public landing page. ",
        "They remain listed for honesty; prefer promoting them into `PUBLIC_ANCHORS` or `api_requirements.yaml`.",
        "",
    ]
    top = s.get("unresolved_top") or []
    if not top:
        lines.append("_None — all tokens resolved or classified._")
    else:
        lines.append("| Token | Panels mentioning |")
        lines.append("|-------|------------------:|")
        for tok, n in top[:60]:
            lines.append(f"| `{tok[:80]}` | {n} |")

    lines += [
        "",
        "## Per-panel anchors (compact)",
        "",
        "Full machine detail: `data/benchmark_anchor_citation_ledger.json`.",
        "",
    ]
    for p in doc["panels"][:]:
        anchors = [a for a in (p.get("public_anchors") or []) if a.get("kind") not in ("process",)]
        if not anchors and not p.get("source_tokens"):
            continue
        lines.append(f"### {p['domain']}")
        lines.append("")
        lines.append(
            f"- Benchmark: `{p['benchmark_file']}` · records={p.get('record_count')} · "
            f"median%={p.get('pooled_median_error_pct')}"
        )
        if p.get("ingest_script"):
            lines.append(f"- Ingest: `{p['ingest_script']}`")
        if p.get("lean_module"):
            lines.append(f"- Lean: `{p['lean_module']}`")
        lines.append("- Public / portable anchors:")
        for a in anchors[:25]:
            bit = a.get("url") or a.get("note") or ""
            lines.append(f"  - **{a.get('kind')}**: {a.get('title')} — {bit}")
        if len(anchors) > 25:
            lines.append(f"  - … +{len(anchors)-25} more in JSON")
        lines.append("")

    lines += [
        "## API registry (full list)",
        "",
        "From `data/api_requirements.yaml` — live rebuild channels:",
        "",
    ]
    for row in doc["registry_catalog"]["api_requirements_sources"]:
        lines.append(
            f"- `{row.get('id')}` ({row.get('family')}): {row.get('url')} "
            f"[auth={row.get('auth')}]"
        )
    lines += [
        "",
        "## Open science no-key probes",
        "",
        "From `scripts/open_science_sources_lib.py`:",
        "",
    ]
    for row in doc["registry_catalog"]["open_science_no_key_sources"]:
        lines.append(f"- `{row.get('id')}`: {row.get('title')} — {row.get('url')}")

    lines += [
        "",
        "## Regenerate",
        "",
        "```powershell",
        "python scripts/build_benchmark_anchor_citation_ledger.py",
        "python scripts/run_cross_proof_verification.py",
        "```",
        "",
        "Machine JSON: [`data/benchmark_anchor_citation_ledger.json`](../data/benchmark_anchor_citation_ledger.json)  ",
        "BibTeX: [`data/domain_citations/benchmark_public_anchors.bib`](../data/domain_citations/benchmark_public_anchors.bib)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_bibtex(doc: dict[str, Any]) -> None:
    entries: list[str] = []
    for i, a in enumerate(doc["global_anchors"]):
        if a.get("kind") in ("process", "unresolved", "vendor_cache"):
            continue
        slug = re.sub(r"[^a-z0-9]+", "", (a.get("title") or f"anchor{i}").lower())[:40] or f"a{i}"
        year = "2026"
        url = a.get("url") or ""
        note = a.get("note") or f"Used by {len(a.get('panels') or [])} FSOT panels"
        kind = a.get("kind") or "misc"
        entries.append(
            f"@misc{{fsot_anchor_{slug}_{i},\n"
            f"  title = {{{(a.get('title') or '').replace('{', '').replace('}', '')}}},\n"
            f"  howpublished = {{\\url{{{url}}}}},\n"
            f"  year = {{{year}}},\n"
            f"  note = {{FSOT public anchor ({kind}); {note.replace('{', '').replace('}', '')}}}\n"
            f"}}"
        )
    OUT_BIB.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"% FSOT public benchmark anchors — generated {doc['generated_at']}\n"
        f"% Repository: https://github.com/dappalumbo91/FSOT-2.1-Lean\n"
        f"% Companion: docs/BENCHMARK_DATA_CITATIONS.md\n\n"
    )
    OUT_BIB.write_text(header + "\n\n".join(entries) + "\n", encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_markdown(doc)
    write_bibtex(doc)
    s = doc["summary"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_BIB}")
    print(
        f"  panels={s['panels_scanned']} anchors={s['unique_public_anchors']} "
        f"unresolved={s['unresolved_token_count']} kinds={s['kind_counts']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
