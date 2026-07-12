#!/usr/bin/env python3
"""Probe every FSOT live API channel and report status (not rate-limit guessing)."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from live_api_fetch_lib import fetch_json, ssl_context  # noqa: E402
from live_api_limits import (  # noqa: E402
    gaia_top_limit,
    materials_project_api_limit,
    mega_deep,
    wds_vizier_top_limit,
)

OUT = ROOT / "data" / "live_api_health_report.json"


def _probe(name: str, fn) -> dict:
    try:
        detail = fn()
        return {"channel": name, "status": "ok", "detail": detail}
    except Exception as exc:
        return {
            "channel": name,
            "status": "fail",
            "error_type": type(exc).__name__,
            "error": str(exc)[:500],
        }


def main() -> int:
    deep = mega_deep() or os.environ.get("FSOT_TIER68_DEEP", "")
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "mega_deep": bool(deep),
        "channels": [],
    }

    def gbif():
        url = "https://api.gbif.org/v1/occurrence/search?limit=3&hasCoordinate=true"
        data = fetch_json(url, timeout=30)
        return f"count={data.get('count')}"

    def gwosc():
        data = fetch_json("https://www.gw-openscience.org/eventapi/json/", timeout=30)
        return f"catalogs={len(data) if isinstance(data, dict) else len(data)}"

    def simbad():
        import urllib.parse

        adql = "SELECT TOP 3 main_id FROM basic"
        p = urllib.parse.urlencode(
            {"request": "doQuery", "lang": "adql", "format": "json", "query": adql}
        )
        url = f"https://simbad.cds.unistra.fr/simbad/sim-tap/sync?{p}"
        data = fetch_json(url, timeout=60)
        return f"rows={len(data.get('data') or [])}"

    def gaia():
        import urllib.parse

        adql = "SELECT TOP 3 source_id FROM gaiadr3.gaia_source"
        p = urllib.parse.urlencode(
            {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": adql}
        )
        url = f"https://gea.esac.esa.int/tap-server/tap/sync?{p}"
        data = fetch_json(url, timeout=90)
        return f"rows={len(data.get('data') or [])}"

    def vizier_wds():
        from vizier_wds_fetch_lib import fetch_wds_systems  # noqa: WPS433

        systems, src = fetch_wds_systems(top=min(10, wds_vizier_top_limit()))
        return f"source={src} n={len(systems)}"

    def materials():
        key = os.environ.get("MP_API_KEY", "").strip()
        if not key:
            return "skipped_no_MP_API_KEY (bundled+expansion panel used)"
        url = (
            "https://api.materialsproject.org/materials/summary/"
            f"?_limit={min(5, materials_project_api_limit())}"
        )
        req = urllib.request.Request(
            url, headers={"X-API-KEY": key, "User-Agent": "FSOT-health"}
        )
        with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as resp:
            data = json.loads(resp.read().decode())
        return f"rows={len(data.get('data') or [])}"

    def openneuro():
        from openneuro_live_lib import fetch_openneuro_datasets  # noqa: WPS433

        ds = fetch_openneuro_datasets(pages=1, page_size=3)
        return f"datasets={len(ds)}"

    def pubchem():
        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/property/"
            "MolecularWeight/JSON"
        )
        data = fetch_json(url, timeout=30)
        return "cid=2244 ok"

    def jpl_ssd_cad():
        url = "https://ssd-api.jpl.nasa.gov/cad.api?date-min=2025-06-01&date-max=2025-06-07&limit=5"
        data = fetch_json(url, timeout=30)
        return f"count={data.get('count')}"

    def noaa_goes_xray():
        data = fetch_json("https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json", timeout=30)
        return f"rows={len(data) if isinstance(data, list) else 0}"

    def clinicaltrials():
        data = fetch_json(
            "https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=3",
            timeout=30,
        )
        return f"studies={len(data.get('studies') or [])}"

    def osti():
        data = fetch_json("https://www.osti.gov/api/v1/records?rows=3", timeout=30)
        rows = data if isinstance(data, list) else (data.get("records") or [])
        return f"records={len(rows)}"

    def uap_war_gov():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://huggingface.co/datasets/MTSlive/war-gov-uap-release-1/resolve/main/documents.jsonl",
            timeout=45,
        ).decode("utf-8")
        n = sum(1 for line in raw.splitlines() if line.strip())
        return f"documents_jsonl_lines={n}"

    def ncbi_gene():
        data = fetch_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=672&retmode=json",
            timeout=30,
        )
        name = ((data.get("result") or {}).get("672") or {}).get("name")
        return f"gene={name}"

    def crossref_works():
        data = fetch_json("https://api.crossref.org/works?rows=3", timeout=30)
        return f"items={len((data.get('message') or {}).get('items') or [])}"

    def inaturalist_obs():
        data = fetch_json(
            "https://api.inaturalist.org/v1/observations?per_page=3&has_geo=true",
            timeout=30,
        )
        return f"results={len(data.get('results') or [])}"

    def noaa_ndbc_buoy():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes("https://www.ndbc.noaa.gov/data/realtime2/46026.txt", timeout=30)
        return f"bytes={len(raw)}"

    def open_meteo_forecast():
        data = fetch_json(
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=38.9&longitude=-77.0&hourly=temperature_2m&forecast_days=1",
            timeout=30,
        )
        hours = (data.get("hourly") or {}).get("temperature_2m") or []
        return f"hours={len(hours)}"

    def tier82_usgs_nwis():
        data = fetch_json(
            "https://waterservices.usgs.gov/nwis/iv/?format=json"
            "&sites=01646500&parameterCd=00010&period=P1D",
            timeout=30,
        )
        series = ((data.get("value") or {}).get("timeSeries")) or []
        return f"series={len(series)}"

    def tier82_soilgrids():
        data = fetch_json(
            "https://rest.isric.org/soilgrids/v2.0/properties/query?"
            "lon=-95&lat=37&property=bdod&depth=0-5cm&value=mean",
            timeout=30,
        )
        return f"layers={len((data.get('properties') or {}).get('layers') or [])}"

    def tier82_natural_earth():
        data = fetch_json(
            "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
            "geojson/ne_110m_admin_0_countries.geojson",
            timeout=30,
        )
        return f"features={len(data.get('features') or [])}"

    def tier84_world_bank():
        data = fetch_json(
            "https://api.worldbank.org/v2/country/USA/indicator/SH.DYN.NMRT?format=json&per_page=3",
            timeout=30,
        )
        rows = data[1] if isinstance(data, list) and len(data) > 1 else []
        return f"rows={len(rows)}"

    def tier84_arxiv_grqc():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "http://export.arxiv.org/api/query?search_query=cat:gr-qc&max_results=2",
            timeout=30,
        )
        return f"bytes={len(raw)}"

    def tier84_pbdb():
        data = fetch_json(
            "https://paleobiodb.org/data1.2/occs/list.json?"
            "limit=3&show=coords,ages&taxon_name=Ammonoidea",
            timeout=30,
        )
        return f"records={len(data.get('records') or [])}"

    def tier84_obis():
        data = fetch_json("https://api.obis.org/v3/occurrence?limit=3", timeout=30)
        return f"results={len(data.get('results') or [])}"

    def tier85_exoplanet_tap():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
            "query=select+top+1+pl_name+from+pscomppars&format=csv",
            timeout=45,
        )
        return f"bytes={len(raw)}"

    def tier85_open_meteo_archive():
        data = fetch_json(
            "https://archive-api.open-meteo.com/v1/archive?"
            "latitude=52.5&longitude=13.4&start_date=1900-01-01&end_date=1900-01-07"
            "&daily=temperature_2m_mean",
            timeout=45,
        )
        return f"daily={len((data.get('daily') or {}).get('time') or [])}"

    def tier85_crossref_history():
        data = fetch_json(
            "https://api.crossref.org/works?query=history&rows=2&select=DOI,title",
            timeout=30,
        )
        return f"items={len((data.get('message') or {}).get('items') or [])}"

    def tier86_nist_codata():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes("https://physics.nist.gov/cuu/Constants/Table/allascii.txt", timeout=30)
        return f"bytes={len(raw)}"

    for name, fn in (
        ("gbif", gbif),
        ("gwosc", gwosc),
        ("simbad_tap", simbad),
        ("gaia_dr3_tap", gaia),
        ("vizier_wds", vizier_wds),
        ("materials_project", materials),
        ("openneuro_graphql", openneuro),
        ("pubchem_pug", pubchem),
        ("jpl_ssd_cad", jpl_ssd_cad),
        ("noaa_goes_xray", noaa_goes_xray),
        ("clinicaltrials_v2", clinicaltrials),
        ("osti_doe_records", osti),
        ("uap_war_gov_hf", uap_war_gov),
        ("ncbi_gene_eutils", ncbi_gene),
        ("crossref_works", crossref_works),
        ("inaturalist_obs", inaturalist_obs),
        ("noaa_ndbc_buoy", noaa_ndbc_buoy),
        ("open_meteo_forecast", open_meteo_forecast),
        ("tier82_usgs_nwis", tier82_usgs_nwis),
        ("tier82_soilgrids", tier82_soilgrids),
        ("tier82_natural_earth", tier82_natural_earth),
        ("tier84_world_bank", tier84_world_bank),
        ("tier84_arxiv_grqc", tier84_arxiv_grqc),
        ("tier84_pbdb", tier84_pbdb),
        ("tier84_obis", tier84_obis),
        ("tier85_exoplanet_tap", tier85_exoplanet_tap),
        ("tier85_open_meteo_archive", tier85_open_meteo_archive),
        ("tier85_crossref_history", tier85_crossref_history),
        ("tier86_nist_codata", tier86_nist_codata),
    ):
        row = _probe(name, fn)
        report["channels"].append(row)
        tag = "OK" if row["status"] == "ok" else "FAIL"
        print(f"{tag} {name}: {row.get('detail') or row.get('error')}")

    fails = [c for c in report["channels"] if c["status"] == "fail"]
    report["fail_count"] = len(fails)
    report["ok_count"] = len(report["channels"]) - len(fails)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT} ({report['ok_count']} ok / {report['fail_count']} fail)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())