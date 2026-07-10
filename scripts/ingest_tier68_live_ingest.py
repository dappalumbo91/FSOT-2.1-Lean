#!/usr/bin/env python3
"""Tier 68 — Materials Project, PubChem live, OpenNeuro, VizieR WDS TAP ingest with bundled fallback."""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
MP_BUNDLED = VENDOR / "materials_live" / "materials_project_bundled.json"
PUBCHEM_BUNDLED = VENDOR / "public_data" / "pubchem" / "pubchem_summary.json"
OPENNEURO_BUNDLED = VENDOR / "public_data" / "consciousness" / "openneuro_summary.json"
WDS_BUNDLED = VENDOR / "stellar_structures" / "wds_multiplicity_expanded.json"

VIZIER_TAP = "https://cdsarc.cds.unistra.fr/viz-bin/votable"
WDS_ADQL = (
    "SELECT TOP 40 WDS, RAdeg, DEdeg, Sep, mag1, mag2, comp "
    "FROM \"II/213/wds\" WHERE Sep IS NOT NULL ORDER BY Sep"
)


def cache_root() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() / "tier68_live_ingest" if raw else VENDOR / "live_cache" / "tier68"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def ingest_materials_project() -> dict:
    out_path = cache_root() / "materials_project_live_cache.json"
    bundled = json.loads(MP_BUNDLED.read_text(encoding="utf-8")) if MP_BUNDLED.exists() else {"materials": []}
    materials = list(bundled.get("materials") or [])
    source = "materials_project_bundled"
    api_key = os.environ.get("MP_API_KEY", "").strip()
    if api_key:
        try:
            url = "https://api.materialsproject.org/materials/summary/?fields=material_id,formula_pretty,band_gap,formation_energy_per_atom,bulk_modulus&_limit=20"
            req = urllib.request.Request(url, headers={"X-API-KEY": api_key, "User-Agent": "FSOT-2.1-Lean/tier68"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            live = []
            for row in payload.get("data") or []:
                live.append(
                    {
                        "mp_id": row.get("material_id"),
                        "formula": row.get("formula_pretty"),
                        "band_gap_eV": row.get("band_gap"),
                        "formation_energy_eV_per_atom": row.get("formation_energy_per_atom"),
                        "bulk_modulus_GPa": row.get("bulk_modulus"),
                        "source": "materials_project_api_live",
                    }
                )
            if live:
                materials = live
                source = "materials_project_api_live"
        except Exception:
            pass
    doc = {"ingested_at": datetime.now(timezone.utc).isoformat(), "source": source, "materials": materials}
    _write(out_path, doc)
    return doc


def ingest_pubchem_live() -> dict:
    out_path = cache_root() / "pubchem_live_cache.json"
    bundled = json.loads(PUBCHEM_BUNDLED.read_text(encoding="utf-8")) if PUBCHEM_BUNDLED.exists() else {"compounds": []}
    compounds = list(bundled.get("compounds") or [])
    source = "pubchem_bundled"
    extra_cids = [962, 241, 3386, 5284373, 5462311]
    live: list[dict] = []
    for cid in extra_cids:
        try:
            url = (
                f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/"
                "property/MolecularWeight,MolecularFormula,IUPACName/JSON"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier68"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            props = (payload.get("PropertyTable") or {}).get("Properties") or [{}]
            row = props[0] if props else {}
            if row:
                live.append(
                    {
                        "cid": cid,
                        "molecular_formula": row.get("MolecularFormula"),
                        "molecular_weight": row.get("MolecularWeight"),
                        "iupac_name": row.get("IUPACName"),
                        "source": "pubchem_pug_live",
                    }
                )
        except Exception:
            continue
    if live:
        seen = {c["cid"] for c in compounds}
        compounds.extend(c for c in live if c["cid"] not in seen)
        source = "pubchem_pug_live+bundled"
    doc = {"ingested_at": datetime.now(timezone.utc).isoformat(), "source": source, "compounds": compounds}
    _write(out_path, doc)
    return doc


def ingest_openneuro_full() -> dict:
    out_path = cache_root() / "openneuro_full_cache.json"
    bundled = json.loads(OPENNEURO_BUNDLED.read_text(encoding="utf-8")) if OPENNEURO_BUNDLED.exists() else {"datasets": []}
    doc = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": bundled.get("source") or "openneuro_bundled",
        "dataset_count": int(bundled.get("dataset_count") or len(bundled.get("datasets") or [])),
        "datasets": bundled.get("datasets") or [],
    }
    _write(out_path, doc)
    return doc


def ingest_vizier_wds_tap() -> dict:
    out_path = cache_root() / "vizier_wds_tap_live_cache.json"
    bundled = json.loads(WDS_BUNDLED.read_text(encoding="utf-8")) if WDS_BUNDLED.exists() else {"systems": []}
    systems = list(bundled.get("systems") or [])
    source = "wds_bundled"
    try:
        params = urllib.parse.urlencode({"-source": "II/213/wds", "-out": "JSON", "-query": WDS_ADQL})
        url = f"{VIZIER_TAP}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier68"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = payload if isinstance(payload, list) else payload.get("data") or []
        live = []
        for row in rows[:40]:
            if isinstance(row, dict):
                live.append(
                    {
                        "id": row.get("WDS") or row.get("wds"),
                        "separation_arcsec": row.get("Sep") or row.get("sep"),
                        "mag1": row.get("mag1"),
                        "mag2": row.get("mag2"),
                        "source": "vizier_wds_tap_live",
                    }
                )
        if live:
            systems = live
            source = "vizier_wds_tap_live"
    except Exception:
        pass
    doc = {"ingested_at": datetime.now(timezone.utc).isoformat(), "source": source, "systems": systems, "objects": systems}
    _write(out_path, doc)
    return doc


INGESTERS = {
    "materials_project": ingest_materials_project,
    "pubchem_live": ingest_pubchem_live,
    "openneuro_full": ingest_openneuro_full,
    "vizier_wds_tap": ingest_vizier_wds_tap,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(INGESTERS.keys()), action="append")
    args = parser.parse_args()
    for name in args.only or sorted(INGESTERS.keys()):
        doc = INGESTERS[name]()
        count = len(doc.get("materials") or doc.get("compounds") or doc.get("datasets") or doc.get("systems") or [])
        print(f"{name}: {count} records from {doc.get('source')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())