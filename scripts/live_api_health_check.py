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
        # clinicaltrials.gov often returns 403 to non-browser / some network paths.
        # Try official v2 first with research UA; fall back to Europe PMC clinical stream.
        headers = {
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (compatible; FSOT-2.1-Lean/1.0; "
                "+https://github.com/dappalumbo91/FSOT-2.1-Lean)"
            ),
        }
        ct_urls = (
            "https://clinicaltrials.gov/api/v2/studies?format=json&pageSize=3",
            "https://clinicaltrials.gov/api/v2/studies?query.cond=diabetes&pageSize=3",
        )
        last_err: Exception | None = None
        for url in ct_urls:
            try:
                data = fetch_json(url, timeout=45, retries=2, headers=headers)
                n = len(data.get("studies") or [])
                if n:
                    return f"studies={n} source=clinicaltrials.gov"
            except Exception as exc:  # noqa: BLE001
                last_err = exc
        # Europe PMC: live clinical/medical literature stream (no CT.gov dependency).
        try:
            data = fetch_json(
                "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                "?query=SRC:MED%20AND%20(clinical%20trial)&format=json&pageSize=3",
                timeout=45,
                retries=2,
            )
            hits = int(data.get("hitCount") or 0)
            n = len(((data.get("resultList") or {}).get("result")) or [])
            if hits or n:
                return f"europepmc_clinical_hits={hits} page_results={n} (ct.gov_blocked)"
        except Exception as exc:  # noqa: BLE001
            last_err = exc
        raise RuntimeError(f"clinical stream unavailable: {last_err}")

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
        # World Bank can be slow; use longer timeout + light retry and a simpler indicator first.
        urls = (
            "https://api.worldbank.org/v2/country/USA/indicator/SP.POP.TOTL?format=json&per_page=3",
            "https://api.worldbank.org/v2/country/USA/indicator/SH.DYN.NMRT?format=json&per_page=3",
        )
        last_err: Exception | None = None
        for url in urls:
            try:
                data = fetch_json(url, timeout=90, retries=3, backoff_s=2.0)
                rows = data[1] if isinstance(data, list) and len(data) > 1 else []
                if rows:
                    ind = (rows[0].get("indicator") or {}).get("id") if isinstance(rows[0], dict) else "?"
                    return f"rows={len(rows)} indicator={ind}"
            except Exception as exc:  # noqa: BLE001
                last_err = exc
        raise RuntimeError(f"world_bank: {last_err}")

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
        # Archive API rejects some pre-coverage windows (1900 → 400). Use a modern week.
        data = fetch_json(
            "https://archive-api.open-meteo.com/v1/archive?"
            "latitude=52.52&longitude=13.41"
            "&start_date=2023-06-01&end_date=2023-06-07"
            "&daily=temperature_2m_mean&timezone=UTC",
            timeout=60,
            retries=2,
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

    def tier87_arxiv_quantph():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://export.arxiv.org/api/query?search_query=cat:quant-ph&max_results=2",
            timeout=30,
        )
        return f"bytes={len(raw)}"

    def tier89_the_well_stats():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://huggingface.co/datasets/polymathic-ai/active_matter/raw/main/stats.yaml",
            timeout=30,
        )
        return f"bytes={len(raw)}"

    # ---- Open-science expansion (no credentials / no signup) ----
    def open_openfda():
        data = fetch_json("https://api.fda.gov/drug/label.json?limit=1", timeout=45)
        return f"results={len(data.get('results') or [])}"

    def open_ensembl():
        data = fetch_json(
            "https://rest.ensembl.org/lookup/id/ENSG00000139618?content-type=application/json",
            timeout=45,
            headers={"Content-Type": "application/json"},
        )
        return f"gene={data.get('display_name') or data.get('id')}"

    def open_gwas():
        data = fetch_json("https://www.ebi.ac.uk/gwas/rest/api/studies?size=2", timeout=45)
        emb = (data.get("_embedded") or {}).get("studies") or []
        return f"studies={len(emb)}"

    def open_chembl():
        data = fetch_json(
            "https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json",
            timeout=45,
        )
        return f"pref={data.get('pref_name')}"

    def open_usgs_quakes():
        data = fetch_json(
            "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=5&orderby=time&minmagnitude=4.5",
            timeout=45,
        )
        return f"features={len(data.get('features') or [])}"

    def open_stringdb():
        data = fetch_json("https://string-db.org/api/json/version", timeout=30)
        if isinstance(data, list) and data:
            return f"version={data[0].get('string_version')}"
        return f"type={type(data).__name__}"

    def open_alphafold():
        data = fetch_json("https://alphafold.ebi.ac.uk/api/prediction/P04637", timeout=45)
        return f"rows={len(data) if isinstance(data, list) else 1}"

    def open_cern_opendata():
        data = fetch_json("https://opendata.cern.ch/api/records/?q=collision&size=2", timeout=45)
        hits = (data.get("hits") or {}).get("hits") if isinstance(data, dict) else None
        if hits is None and isinstance(data, dict):
            return f"keys={list(data.keys())[:4]}"
        return f"hits={len(hits or [])}"

    def open_pubmed_hubble():
        data = fetch_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Hubble+tension&retmode=json&retmax=3",
            timeout=45,
        )
        n = len(((data.get("esearchresult") or {}).get("idlist")) or [])
        return f"ids={n}"

    def open_owid_co2():
        from live_api_fetch_lib import fetch_bytes  # noqa: WPS433

        raw = fetch_bytes(
            "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv",
            timeout=45,
        )
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
        ("tier87_arxiv_quantph", tier87_arxiv_quantph),
        ("tier89_the_well_stats", tier89_the_well_stats),
        ("open_openfda", open_openfda),
        ("open_ensembl", open_ensembl),
        ("open_gwas", open_gwas),
        ("open_chembl", open_chembl),
        ("open_usgs_quakes", open_usgs_quakes),
        ("open_stringdb", open_stringdb),
        ("open_alphafold", open_alphafold),
        ("open_cern_opendata", open_cern_opendata),
        ("open_pubmed_hubble", open_pubmed_hubble),
        ("open_owid_co2", open_owid_co2),
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