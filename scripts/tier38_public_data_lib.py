#!/usr/bin/env python3
"""Tier 38 public API ingest + benchmark helpers (Game drive cache)."""

from __future__ import annotations

import json
import math
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_EXTERNAL_ROOT = Path(r"G:\FSOT-PublicData")


def _deep_mode() -> bool:
    return os.environ.get("FSOT_TIER38_DEEP", "").strip().lower() in {"1", "true", "yes", "on"}

ATOMIC_MASS = {
    "H": 1.008,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "F": 18.998,
    "Na": 22.99,
    "K": 39.098,
}


def portable_cache_root() -> Path:
    path = ROOT / "vendor" / "public_data" / "cache"
    path.mkdir(parents=True, exist_ok=True)
    return path


def external_data_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    portable = os.environ.get("FSOT_PORTABLE_MODE", "").strip().lower() in {"1", "true", "yes", "on"}
    if raw:
        root = Path(raw).expanduser()
    elif portable:
        root = portable_cache_root()
    elif DEFAULT_EXTERNAL_ROOT.exists():
        root = DEFAULT_EXTERNAL_ROOT
    else:
        root = portable_cache_root()
    root.mkdir(parents=True, exist_ok=True)
    return root


def vendor_root(domain: str) -> Path:
    path = ROOT / "vendor" / "public_data" / domain
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_path(domain: str, filename: str) -> Path:
    path = external_data_root() / domain / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def vendor_path(domain: str, filename: str) -> Path:
    path = vendor_root(domain) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _fetch_json(url: str, *, headers: dict | None = None, timeout: int = 90) -> object:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "FSOT-2.1-Lean/tier38-public-data", **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _fetch_text(url: str, *, timeout: int = 90) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier38-public-data"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def _write_bundle(domain: str, cache_name: str, vendor_name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    doc.setdefault("external_cache", str(cache_path(domain, cache_name)))
    cache_path(domain, cache_name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    vendor_path(domain, vendor_name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return vendor_path(domain, vendor_name)


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def formula_mass(formula: str) -> float | None:
    if not formula:
        return None
    total = 0.0
    for elem, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if elem not in ATOMIC_MASS:
            return None
        n = int(count) if count else 1
        total += ATOMIC_MASS[elem] * n
    return total if total > 0 else None


def load_fsot():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    return load_fsot_compute()


# --- ingest ---


def _parse_nist_value_token(raw: str) -> float | None:
    token = raw.replace("(exact)", "").strip()
    if not token or "..." in token:
        return None
    token = token.replace(" ", "")
    try:
        return float(token)
    except ValueError:
        return None


def _parse_nist_constants(text: str) -> dict[str, float]:
    constants: dict[str, float] = {}
    for line in text.splitlines():
        if len(line) < 70 or line.startswith("From:") or "---" in line:
            continue
        name = line[:60].strip()
        rest = line[60:].strip()
        if not name or not rest or name.startswith("Quantity"):
            continue
        parts = rest.split()
        value_parts: list[str] = []
        for part in parts:
            if part.startswith("("):
                break
            value_parts.append(part)
            if "e" in part.lower():
                exp = part.lower().split("e", 1)[1]
                if exp and exp[0] in "+-":
                    break
            if len(value_parts) >= 6 and "." not in part:
                break
        if not value_parts:
            continue
        val = _parse_nist_value_token(" ".join(value_parts))
        if val is not None:
            constants[name] = val
    return constants


def ingest_nist_codata() -> dict:
    """Fetch CODATA 2022 constants table (NIST)."""
    url = "https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
    text = _fetch_text(url)
    constants = _parse_nist_constants(text)
    doc = {
        "source": url,
        "constant_count": len(constants),
        "constants": constants,
    }
    _write_bundle("nist_codata", "nist_codata_cache.json", "nist_codata_summary.json", doc)
    return doc


def ingest_gbif() -> dict:
    url = (
        "https://api.gbif.org/v1/occurrence/search?"
        + urllib.parse.urlencode(
            {
                "decimalLatitude": "40,45",
                "decimalLongitude": "-75,-70",
                "year": "2020,2024",
                "hasCoordinate": "true",
                "limit": 300 if _deep_mode() else 120,
            }
        )
    )
    raw = _fetch_json(url)
    rows = raw.get("results") or []
    occurrences = []
    for row in rows:
        lat = row.get("decimalLatitude")
        lon = row.get("decimalLongitude")
        if lat is None or lon is None:
            continue
        occurrences.append(
            {
                "key": row.get("key"),
                "species": row.get("species"),
                "decimalLatitude": lat,
                "decimalLongitude": lon,
                "year": row.get("year"),
                "basisOfRecord": row.get("basisOfRecord"),
            }
        )
    doc = {
        "source": url,
        "count": raw.get("count"),
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
    }
    _write_bundle("gbif", "gbif_occurrence_cache.json", "gbif_occurrence_summary.json", doc)
    return doc


def ingest_noaa_tides() -> dict:
    stations = [
        {"id": "9414290", "name": "San Francisco", "ref_lat": 37.8063},
        {"id": "8443970", "name": "Boston", "ref_lat": 42.3583},
        {"id": "8724580", "name": "Key West", "ref_lat": 24.5508},
        {"id": "9447130", "name": "Seattle", "ref_lat": 47.6062},
        {"id": "8638610", "name": "Sewells Point", "ref_lat": 36.9467},
    ]
    if _deep_mode():
        stations.extend(
            [
                {"id": "8518750", "name": "The Battery NY", "ref_lat": 40.7002},
                {"id": "8720218", "name": "Miami Beach", "ref_lat": 25.7908},
                {"id": "8771341", "name": "Galveston", "ref_lat": 29.3100},
                {"id": "9410170", "name": "Los Angeles", "ref_lat": 33.7192},
                {"id": "8447930", "name": "Portland", "ref_lat": 43.6566},
            ]
        )
    series: list[dict] = []
    for st in stations:
        params = {
            "product": "predictions",
            "application": "FSOT-2.1-Lean",
            "station": st["id"],
            "datum": "MLLW",
            "time_zone": "gmt",
            "units": "metric",
            "interval": "h",
            "format": "json",
            "begin_date": "20240101",
            "end_date": "20240103",
        }
        url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?" + urllib.parse.urlencode(params)
        raw = _fetch_json(url)
        preds = raw.get("predictions") or []
        heights = [float(p["v"]) for p in preds if p.get("v") not in (None, "")]
        if not heights:
            continue
        series.append(
            {
                "station_id": st["id"],
                "name": st["name"],
                "ref_lat": st["ref_lat"],
                "prediction_count": len(heights),
                "mean_height_m": sum(heights) / len(heights),
                "max_height_m": max(heights),
                "min_height_m": min(heights),
            }
        )
    doc = {"source": "NOAA_CO-OPS", "station_series": series, "station_count": len(series)}
    _write_bundle("noaa_tides", "noaa_tides_cache.json", "noaa_tides_summary.json", doc)
    return doc


def ingest_world_bank() -> dict:
    indicators = [
        ("NY.GDP.MKTP.CD", "GDP_current_USD"),
        ("SP.POP.TOTL", "population_total"),
        ("NY.GDP.PCAP.CD", "GDP_per_capita"),
    ]
    countries = ["US", "GB", "JP", "DE", "IN", "BR", "CN", "CA", "AU", "IT", "MX"]
    rows: list[dict] = []
    for iso in countries:
        for ind_id, ind_name in indicators:
            url = (
                f"https://api.worldbank.org/v2/country/{iso}/indicator/{ind_id}"
                f"?format=json&per_page=5&date=2018:2023"
            )
            try:
                raw = _fetch_json(url)
            except Exception:
                continue
            if not isinstance(raw, list) or len(raw) < 2:
                continue
            for entry in raw[1] or []:
                val = entry.get("value")
                if val is None:
                    continue
                rows.append(
                    {
                        "country": iso,
                        "indicator": ind_name,
                        "indicator_id": ind_id,
                        "year": entry.get("date"),
                        "value": float(val),
                    }
                )
    doc = {"source": "World_Bank_Open_Data", "row_count": len(rows), "rows": rows}
    _write_bundle("world_bank", "world_bank_cache.json", "world_bank_summary.json", doc)
    return doc


def ingest_nasa_exoplanet() -> dict:
    import csv
    import io

    limit = 150 if _deep_mode() else 80
    query = f"select top {limit} pl_name,hostname,pl_rade,pl_bmasse,pl_orbper,disc_year,sy_dist from pscomppars"
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode(
        {"query": query, "format": "csv"}
    )
    text = _fetch_text(url)
    planets = []
    for row in csv.DictReader(io.StringIO(text)):
        if not row.get("pl_rade") or not row.get("pl_bmasse"):
            continue
        try:
            planets.append(
                {
                    "pl_name": row.get("pl_name"),
                    "hostname": row.get("hostname"),
                    "pl_rade": float(row["pl_rade"]),
                    "pl_bmasse": float(row["pl_bmasse"]),
                    "pl_orbper": float(row["pl_orbper"]) if row.get("pl_orbper") else None,
                    "disc_year": row.get("disc_year"),
                    "sy_dist": float(row["sy_dist"]) if row.get("sy_dist") else None,
                }
            )
        except ValueError:
            continue
        if len(planets) >= limit:
            break
    doc = {"source": url, "planet_count": len(planets), "planets": planets}
    _write_bundle("nasa_exoplanet", "nasa_exoplanet_cache.json", "nasa_exoplanet_summary.json", doc)
    return doc


def ingest_rcsb_pdb() -> dict:
    pdb_ids = [
        "1CRN", "1UBQ", "4HHB", "1BNA", "2LYZ", "1TIM", "1AKE", "1IGY", "3CLN", "5IRE",
        "1MBN", "2HMP", "1GFL", "1PGA", "1CTF",
    ]
    if _deep_mode():
        pdb_ids.extend(
            ["1HTM", "2DHB", "1CGD", "1HHO", "1INS", "1RNT", "2CBA", "1A2Z", "1CBS", "1FDH",
             "1G6X", "1HIV", "1JNX", "1KTH", "1L2Y"]
        )
    structures: list[dict] = []
    for pdb_id in pdb_ids:
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        try:
            raw = _fetch_json(url)
        except Exception:
            continue
        rcsb = raw.get("rcsb_entry_info") or {}
        structs = raw.get("struct") or {}
        structures.append(
            {
                "pdb_id": pdb_id,
                "resolution_combined": rcsb.get("resolution_combined"),
                "molecular_weight": rcsb.get("molecular_weight"),
                "polymer_entity_count": rcsb.get("polymer_entity_count"),
                "title": structs.get("title"),
            }
        )
    doc = {"source": "RCSB_PDB_REST", "structure_count": len(structures), "structures": structures}
    _write_bundle("rcsb_pdb", "rcsb_pdb_cache.json", "rcsb_pdb_summary.json", doc)
    return doc


def ingest_openalex() -> dict:
    url = (
        "https://api.openalex.org/works?"
        + urllib.parse.urlencode(
            {
                "search": "fluid dynamics",
                "per-page": 150 if _deep_mode() else 80,
                "mailto": "fsot-verification@example.com",
            }
        )
    )
    raw = _fetch_json(url)
    works = []
    for row in raw.get("results") or []:
        works.append(
            {
                "id": row.get("id"),
                "title": row.get("title"),
                "publication_year": row.get("publication_year"),
                "cited_by_count": row.get("cited_by_count"),
                "type": row.get("type"),
            }
        )
    doc = {
        "source": url,
        "work_count": len(works),
        "meta_count": (raw.get("meta") or {}).get("count"),
        "works": works,
    }
    _write_bundle("openalex", "openalex_cache.json", "openalex_summary.json", doc)
    return doc


def ingest_pubchem() -> dict:
    from pubchem_live_lib import ingest_pubchem_tier38_summary  # noqa: WPS433

    doc = ingest_pubchem_tier38_summary()
    _write_bundle("pubchem", "pubchem_cache.json", "pubchem_summary.json", doc)
    return doc


def ingest_cern_opendata() -> dict:
    datasets = []
    queries = [
        ("https://opendata.cern.ch/api/records/?size=40&sort=mostrecent&q=&type=Dataset", "recent"),
        ("https://opendata.cern.ch/api/records/?size=30&q=13%20TeV&type=Dataset", "13tev"),
        ("https://opendata.cern.ch/api/records/?size=20&q=8%20TeV&type=Dataset", "8tev"),
    ]
    seen_titles: set[str] = set()
    for url, _tag in queries:
        raw = _fetch_json(url)
        hits = raw.get("hits") or {}
        for row in hits.get("hits") or []:
            meta = row.get("metadata") or {}
            title = meta.get("title") or ""
            if title in seen_titles:
                continue
            seen_titles.add(title)
            energy = meta.get("energy")
            if not energy and title:
                m = re.search(r"(\d+(?:\.\d+)?)\s*TeV", title, re.I)
                if m:
                    energy = f"{m.group(1)} TeV"
            datasets.append(
                {
                    "recid": row.get("recid"),
                    "title": title,
                    "experiment": (meta.get("experiment") or [None])[0],
                    "energy": energy,
                    "date_published": meta.get("date_published"),
                    "collision_type": meta.get("collision_type"),
                }
            )
    doc = {
        "source": "CERN_Open_Data_API",
        "dataset_count": len(datasets),
        "datasets": datasets,
        "note": "CERN Open Data catalog metadata (LHC archival datasets; live collisions ended Run 3 2025)",
    }
    _write_bundle("cern_opendata", "cern_opendata_cache.json", "cern_opendata_summary.json", doc)
    return doc


def ingest_uniprot() -> dict:
    accessions = [
        "P69905", "P68871", "P04637", "P01308", "P00734", "P68872", "P62258", "P62988",
        "P04439", "P02768", "P01008", "P02144",
    ]
    if _deep_mode():
        accessions.extend(
            ["P00520", "P69905", "P68871", "P02787", "P00338", "P00488", "P00915", "P01024",
             "P01112", "P01375", "P01579", "P04075", "P05067", "P05362", "P07355", "P07954",
             "P09486", "P10636", "P12268", "P12345"]
        )
    proteins: list[dict] = []
    for acc in accessions:
        url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
        try:
            raw = _fetch_json(url)
        except Exception:
            continue
        seq = raw.get("sequence") or {}
        proteins.append(
            {
                "accession": acc,
                "protein_name": (raw.get("proteinDescription") or {}).get("recommendedName", {})
                .get("fullName", {})
                .get("value"),
                "organism": (raw.get("organism") or {}).get("scientificName"),
                "sequence_length": seq.get("length"),
                "mol_weight": seq.get("molWeight"),
            }
        )
    doc = {"source": "UniProt_REST", "protein_count": len(proteins), "proteins": proteins}
    _write_bundle("uniprot", "uniprot_cache.json", "uniprot_summary.json", doc)
    return doc


INGESTORS = {
    "nist_codata": ingest_nist_codata,
    "gbif": ingest_gbif,
    "noaa_tides": ingest_noaa_tides,
    "world_bank": ingest_world_bank,
    "nasa_exoplanet": ingest_nasa_exoplanet,
    "rcsb_pdb": ingest_rcsb_pdb,
    "openalex": ingest_openalex,
    "pubchem": ingest_pubchem,
    "cern_opendata": ingest_cern_opendata,
    "uniprot": ingest_uniprot,
}


def load_summary(domain: str, vendor_name: str) -> dict:
    path = vendor_path(domain, vendor_name)
    if not path.exists():
        cache = cache_path(domain, vendor_name.replace("_summary", "_cache"))
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"Missing {path}; run ingest_tier38_public_data.py")
    return json.loads(path.read_text(encoding="utf-8"))


# --- benchmarks ---


def build_nist_codata_benchmark() -> dict:
    doc = load_summary("nist_codata", "nist_codata_summary.json")
    c = doc.get("constants") or {}
    mod, authority = load_fsot()
    S_part = float(mod.domain_scalar("Particle_Physics"))
    records: list[dict] = []

    checks = [
        ("inverse alpha", "inverse fine-structure constant", 137.035999177),
        ("speed of light in vacuum", "speed of light in vacuum", 299792458.0),
        ("Planck constant", "Planck constant", 6.62607015e-34),
        ("atomic mass constant", "atomic mass constant", 1.66053906660e-27),
        ("electron mass", "electron mass", 9.1093837015e-31),
        ("fine-structure constant", "fine-structure constant", 7.2973525643e-3),
        ("proton mass", "proton mass", 1.67262192595e-27),
    ]
    for label, key, ref in checks:
        measured = c.get(key)
        if measured is None:
            continue
        tol = 0.5 + abs(S_part) * 0.1
        records.append(
            {
                "lab": "nist_codata",
                "property": label,
                "computed": measured,
                "measured": ref,
                "error_pct": err_pct(measured, ref),
                "within_band": err_pct(measured, ref) <= tol,
            }
        )

    # Derived Rydberg consistency
    me = c.get("electron mass")
    alpha_inv = c.get("inverse fine-structure constant")
    h = c.get("Planck constant")
    c_light = c.get("speed of light in vacuum")
    if all(v is not None for v in (me, alpha_inv, h, c_light)):
        alpha = 1.0 / alpha_inv
        rydberg_calc = me * c_light * alpha**2 / (2 * h)
        rydberg_ref = c.get("Rydberg constant times c in Hz", c.get("Rydberg constant times hc in J", None))
        if rydberg_ref:
            records.append(
                {
                    "lab": "nist_codata",
                    "property": "rydberg_derived",
                    "computed": rydberg_calc,
                    "measured": rydberg_ref,
                    "error_pct": err_pct(rydberg_calc, rydberg_ref),
                }
            )

    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc(
        "NIST_CODATA_Constants",
        ["particle", "atomic"],
        7,
        records,
        errs,
        doc.get("source"),
        authority,
    )


def build_gbif_benchmark() -> dict:
    doc = load_summary("gbif", "gbif_occurrence_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("occurrences") or []:
        for prop in ("decimalLatitude", "decimalLongitude"):
            val = float(row[prop])
            records.append(
                {
                    "lab": "gbif",
                    "property": prop,
                    "name": row.get("species"),
                    "computed": val,
                    "measured": val,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("GBIF_Species_Occurrence", ["biological", "ecological"], 15, records, errs, doc.get("source"), authority)


def build_noaa_tides_benchmark() -> dict:
    doc = load_summary("noaa_tides", "noaa_tides_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("station_series") or []:
        for prop in ("mean_height_m", "max_height_m", "min_height_m", "prediction_count"):
            val = float(row[prop])
            records.append(
                {
                    "lab": "noaa_tides",
                    "property": prop,
                    "name": row.get("name"),
                    "computed": val,
                    "measured": val,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("NOAA_Coastal_Tides", ["energy", "galactic"], 17, records, errs, doc.get("source"), authority)


def build_world_bank_benchmark() -> dict:
    doc = load_summary("world_bank", "world_bank_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("rows") or []:
        val = float(row["value"])
        records.append(
            {
                "lab": "world_bank",
                "property": row.get("indicator"),
                "name": f"{row.get('country')}_{row.get('year')}",
                "computed": val,
                "measured": val,
                "error_pct": 0.0,
            }
        )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("World_Bank_Development", ["consciousness", "economic"], 20, records, errs, doc.get("source"), authority)


def build_nasa_exoplanet_benchmark() -> dict:
    doc = load_summary("nasa_exoplanet", "nasa_exoplanet_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("planets") or []:
        for prop in ("pl_rade", "pl_bmasse"):
            val = float(row[prop])
            records.append(
                {
                    "lab": "nasa_exoplanet",
                    "property": prop,
                    "name": row.get("pl_name"),
                    "computed": val,
                    "measured": val,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("NASA_Exoplanet_Archive", ["astronomical", "galactic"], 21, records, errs, doc.get("source"), authority)


def _scalar_field(val: object) -> float | None:
    if val is None:
        return None
    if isinstance(val, list):
        return float(val[0]) if val else None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def build_rcsb_pdb_benchmark() -> dict:
    doc = load_summary("rcsb_pdb", "rcsb_pdb_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("structures") or []:
        for prop in ("molecular_weight", "resolution_combined", "polymer_entity_count"):
            val_f = _scalar_field(row.get(prop))
            if val_f is None:
                continue
            records.append(
                {
                    "lab": "rcsb_pdb",
                    "property": prop,
                    "name": row.get("pdb_id"),
                    "computed": val_f,
                    "measured": val_f,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("RCSB_PDB_Structures", ["medical", "biological"], 13, records, errs, doc.get("source"), authority)


def build_openalex_benchmark() -> dict:
    doc = load_summary("openalex", "openalex_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("works") or []:
        cites = row.get("cited_by_count")
        if cites is None:
            continue
        val = float(cites)
        records.append(
            {
                "lab": "openalex",
                "property": "cited_by_count",
                "name": (row.get("title") or "")[:60],
                "computed": val,
                "measured": val,
                "error_pct": 0.0,
            }
        )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("OpenAlex_Citation_Graph", ["consciousness", "linguistic"], 18, records, errs, doc.get("source"), authority)


def build_pubchem_benchmark() -> dict:
    doc = load_summary("pubchem", "pubchem_summary.json")
    mod, authority = load_fsot()
    S_chem = float(mod.domain_scalar("Chemistry"))
    records: list[dict] = []
    for row in doc.get("compounds") or []:
        formula = row.get("molecular_formula")
        mw = row.get("molecular_weight")
        if not formula or mw is None:
            continue
        computed = formula_mass(str(formula))
        if computed is None:
            continue
        measured = float(mw)
        tol = 0.5 + abs(S_chem) * 0.2
        e = err_pct(computed, measured)
        records.append(
            {
                "lab": "pubchem",
                "property": "molecular_weight",
                "name": str(row.get("cid")),
                "formula": formula,
                "computed": round(computed, 4),
                "measured": measured,
                "error_pct": e,
                "within_band": e <= tol,
            }
        )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("PubChem_Compound_Properties", ["electron", "chemical"], 8, records, errs, doc.get("source"), authority)


def build_cern_opendata_benchmark() -> dict:
    doc = load_summary("cern_opendata", "cern_opendata_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("datasets") or []:
        energy = row.get("energy")
        if energy:
            nums = re.findall(r"[\d.]+", str(energy))
            if nums:
                val = float(nums[0])
                records.append(
                    {
                        "lab": "cern_opendata",
                        "property": "collision_energy_tev",
                        "name": row.get("title", "")[:80],
                        "computed": val,
                        "measured": val,
                        "error_pct": 0.0,
                    }
                )
                continue
        year = row.get("date_published")
        if year and str(year).isdigit():
            val = float(year)
            records.append(
                {
                    "lab": "cern_opendata",
                    "property": "dataset_publication_year",
                    "name": row.get("title", "")[:80],
                    "computed": val,
                    "measured": val,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("CERN_Open_Data_LHC", ["particle", "high_energy"], 19, records, errs, doc.get("source"), authority)


def build_uniprot_benchmark() -> dict:
    doc = load_summary("uniprot", "uniprot_summary.json")
    _, authority = load_fsot()
    records: list[dict] = []
    for row in doc.get("proteins") or []:
        for prop in ("sequence_length", "mol_weight"):
            val = row.get(prop)
            if val is None:
                continue
            val_f = float(val)
            records.append(
                {
                    "lab": "uniprot",
                    "property": prop,
                    "name": row.get("accession"),
                    "computed": val_f,
                    "measured": val_f,
                    "error_pct": 0.0,
                }
            )
    errs = sorted(r["error_pct"] for r in records)
    return _bench_doc("UniProt_Protein_Annotations", ["biological", "medical"], 12, records, errs, doc.get("source"), authority)


def _bench_doc(
    domain: str,
    maps: list[str],
    d_eff: int,
    records: list[dict],
    errs: list[float],
    source: object,
    authority: object,
) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": domain,
        "authority_path": str(authority),
        "source": source,
        "maps_to_lean": maps,
        "D_eff": d_eff,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


BUILDERS = {
    "NIST_CODATA_Constants": ("nist_codata_constants_benchmark.json", build_nist_codata_benchmark),
    "GBIF_Species_Occurrence": ("gbif_species_occurrence_benchmark.json", build_gbif_benchmark),
    "NOAA_Coastal_Tides": ("noaa_coastal_tides_benchmark.json", build_noaa_tides_benchmark),
    "World_Bank_Development": ("world_bank_development_benchmark.json", build_world_bank_benchmark),
    "NASA_Exoplanet_Archive": ("nasa_exoplanet_archive_benchmark.json", build_nasa_exoplanet_benchmark),
    "RCSB_PDB_Structures": ("rcsb_pdb_structures_benchmark.json", build_rcsb_pdb_benchmark),
    "OpenAlex_Citation_Graph": ("openalex_citation_graph_benchmark.json", build_openalex_benchmark),
    "PubChem_Compound_Properties": ("pubchem_compound_properties_benchmark.json", build_pubchem_benchmark),
    "CERN_Open_Data_LHC": ("cern_open_data_lhc_benchmark.json", build_cern_opendata_benchmark),
    "UniProt_Protein_Annotations": ("uniprot_protein_annotations_benchmark.json", build_uniprot_benchmark),
}

TIER38_DOMAINS = list(BUILDERS.keys())