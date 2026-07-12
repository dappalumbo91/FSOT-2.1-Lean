#!/usr/bin/env python3
"""Tier 68 — Materials Project, PubChem live, OpenNeuro, VizieR WDS TAP ingest with bundled fallback."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
MP_BUNDLED = VENDOR / "materials_live" / "materials_project_bundled.json"
MP_EXPANSION = VENDOR / "materials_live" / "materials_project_expansion.json"
PUBCHEM_BUNDLED = VENDOR / "public_data" / "pubchem" / "pubchem_summary.json"
OPENNEURO_BUNDLED = VENDOR / "public_data" / "consciousness" / "openneuro_summary.json"
WDS_BUNDLED = VENDOR / "stellar_structures" / "wds_multiplicity_expanded.json"

VIZIER_TAP = "https://tapvizier.cds.unistra.fr/TAPVizierTap/sync"
VIZIER_VOTABLE = "https://cdsarc.cds.unistra.fr/viz-bin/votable"


def _wds_adql() -> str:
    from live_api_limits import wds_vizier_top_limit  # noqa: WPS433

    top = wds_vizier_top_limit()
    return (
        f"SELECT TOP {top} WDS, RAdeg, DEdeg, Sep, mag1, mag2, comp "
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
    from live_api_limits import materials_project_api_limit  # noqa: WPS433

    out_path = cache_root() / "materials_project_live_cache.json"
    bundled = json.loads(MP_BUNDLED.read_text(encoding="utf-8")) if MP_BUNDLED.exists() else {"materials": []}
    materials = list(bundled.get("materials") or [])
    if MP_EXPANSION.exists():
        expansion = json.loads(MP_EXPANSION.read_text(encoding="utf-8"))
        seen = {str(m.get("mp_id")) for m in materials}
        for row in expansion.get("materials") or []:
            mp_id = str(row.get("mp_id"))
            if mp_id and mp_id not in seen:
                materials.append(row)
                seen.add(mp_id)
    source = "materials_project_bundled"
    api_key = os.environ.get("MP_API_KEY", "").strip()
    limit = materials_project_api_limit()
    if api_key:
        try:
            url = (
                "https://api.materialsproject.org/materials/summary/"
                f"?fields=material_id,formula_pretty,band_gap,formation_energy_per_atom,bulk_modulus&_limit={limit}"
            )
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
    from pubchem_live_lib import ingest_pubchem_live as _ingest  # noqa: WPS433

    out_path = cache_root() / "pubchem_live_cache.json"
    return _ingest(cache_path=out_path)


def ingest_openneuro_full() -> dict:
    from live_api_limits import (  # noqa: WPS433
        openneuro_dataset_cap,
        openneuro_graphql_pages,
        openneuro_page_size,
    )
    from openneuro_live_lib import fetch_openneuro_datasets  # noqa: WPS433

    out_path = cache_root() / "openneuro_full_cache.json"
    bundled = json.loads(OPENNEURO_BUNDLED.read_text(encoding="utf-8")) if OPENNEURO_BUNDLED.exists() else {"datasets": []}
    datasets = list(bundled.get("datasets") or [])
    source = bundled.get("source") or "openneuro_bundled"
    try:
        live = fetch_openneuro_datasets(
            pages=openneuro_graphql_pages(),
            page_size=openneuro_page_size(),
        )
        if live:
            datasets = live[: openneuro_dataset_cap()]
            source = "https://openneuro.org/crn/graphql"
    except Exception:
        pass
    doc = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "dataset_count": len(datasets),
        "datasets": datasets,
    }
    _write(out_path, doc)
    if source.startswith("https://"):
        OPENNEURO_BUNDLED.parent.mkdir(parents=True, exist_ok=True)
        OPENNEURO_BUNDLED.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def _vizier_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    try:
        import certifi  # noqa: WPS433

        ctx.load_verify_locations(certifi.where())
    except Exception:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _urlopen_json(url: str, *, timeout: int = 120) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/tier68"})
    ctx = _vizier_ssl_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_vizier_rows(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        for key in ("data", "rows", "result"):
            data = payload.get(key)
            if isinstance(data, list):
                return [r for r in data if isinstance(r, dict)]
    return []


def _fetch_vizier_tap(adql: str) -> list[dict]:
    errors: list[str] = []
    tap_params = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
    )
    for url in (
        f"{VIZIER_TAP}?{tap_params}",
        f"{VIZIER_VOTABLE}?{urllib.parse.urlencode({'-source': 'II/213/wds', '-out': 'JSON', '-query': adql})}",
    ):
        try:
            rows = _parse_vizier_rows(_urlopen_json(url))
            if rows:
                return rows
        except Exception as exc:
            errors.append(f"{url}: {exc}")
    if errors:
        raise RuntimeError("; ".join(errors[-2:]))
    return []


def ingest_vizier_wds_tap() -> dict:
    out_path = cache_root() / "vizier_wds_tap_live_cache.json"
    bundled = json.loads(WDS_BUNDLED.read_text(encoding="utf-8")) if WDS_BUNDLED.exists() else {"systems": []}
    systems = list(bundled.get("systems") or [])
    source = "wds_bundled"
    try:
        rows = _fetch_vizier_tap(_wds_adql())
        live = []
        from live_api_limits import wds_vizier_top_limit  # noqa: WPS433

        for row in rows[: wds_vizier_top_limit()]:
            sep = row.get("Sep") or row.get("sep") or row.get("SEPARATION")
            live.append(
                {
                    "id": row.get("WDS") or row.get("wds"),
                    "separation_arcsec": float(sep) if sep is not None else None,
                    "mag1": row.get("mag1") or row.get("MAG1"),
                    "mag2": row.get("mag2") or row.get("MAG2"),
                    "multiplicity": row.get("comp") or row.get("COMP"),
                    "source": "vizier_wds_tap_live",
                }
            )
        live = [r for r in live if r.get("id")]
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
    parser.add_argument("--deep", action="store_true", help="PubChem: live-refresh all bundled CIDs")
    args = parser.parse_args()
    if args.deep:
        os.environ["FSOT_TIER68_DEEP"] = "1"
        os.environ.setdefault("FSOT_API_MEGA_DEEP", os.environ.get("FSOT_API_MEGA_DEEP", ""))
    for name in args.only or sorted(INGESTERS.keys()):
        doc = INGESTERS[name]()
        count = len(doc.get("materials") or doc.get("compounds") or doc.get("datasets") or doc.get("systems") or [])
        print(f"{name}: {count} records from {doc.get('source')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())