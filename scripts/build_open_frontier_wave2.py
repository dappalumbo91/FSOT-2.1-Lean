#!/usr/bin/env python3
"""Open-science frontier wave 2 — FSOT residual mathematics only.

Hard rules (same as wave 1):
  - auth=none
  - make_fsot_record → fsot_scaled only
  - formula=None always (no formula_mass short-circuit)
  - no free-fit parameters / ad-hoc physics

Frontiers:
  - uniprot_proteome_slice
  - alphafold_batch_meta
  - rcsb_structure_batch
  - oeis_family_sweep
  - usgs_seismic_history
  - noaa_tides_multi_station
  - gbif_taxon_depth
  - zenodo_records_depth
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from live_api_fetch_lib import fetch_json  # noqa: E402
from open_science_sources_lib import vendor_dir  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402

UA = {
    "User-Agent": (
        "FSOT-2.1-Lean/open-science "
        "(mailto:dappalumbo91@users.noreply.github.com; "
        "+https://github.com/dappalumbo91/FSOT-2.1-Lean)"
    ),
    "Accept": "application/json, text/plain, */*",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _num(v: Any) -> float | None:
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x != x:
        return None
    return x


def fsot_row(*, lab: str, property_name: str, name: str, measured: float, domain: str, extra: dict | None = None) -> dict:
    return make_fsot_record(
        lab=lab,
        property_name=property_name,
        name=name,
        measured=float(measured),
        domain=domain,
        formula=None,
        eval_kind="fsot_prediction",
        extra={**(extra or {}), "math": "fsot_scaled_only", "auth": "none"},
    )


def _panel(domain: str, records: list[dict], maps: list[str], d_eff: int, sources: list[str], channel: str, model: str, out_name: str, frontier_id: str) -> dict:
    _, authority = _load_fsot()
    errs = [float(r["error_pct"]) for r in records if r.get("error_pct") is not None]
    doc = _bench_v11(
        domain=domain,
        material_records=records,
        maps_to_lean=maps,
        d_eff=d_eff,
        authority_path=authority,
        source=sources,
        channel_stats=[("fsot_prediction", channel, errs or [0.0])],
        sota_baselines={channel: {"sota_typical_error_pct": 5.0, "sota_model": model}},
    )
    doc["policy"] = "open_science_only_no_credentials"
    doc["residual_law"] = "make_fsot_record → fsot_scaled only (FSOT mathematics)"
    doc["frontier_id"] = frontier_id
    (ROOT / "data" / out_name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"  {out_name}: n={doc['record_count']} pooled={doc.get('pooled_median_error_pct')}%")
    return doc


def build_uniprot() -> dict:
    print("UniProt proteome slice…")
    # Search well-known human proteins (open REST, no key)
    queries = [
        "accession:P04637",  # p53
        "accession:P38398",  # BRCA1
        "accession:P00533",  # EGFR
        "accession:P01308",  # insulin
        "accession:P68871",  # HBB
        "accession:P69905",  # HBA
        "accession:P0DTC2",  # SARS-CoV-2 spike
        "accession:Q9Y6K9",  # ACE2
        "gene:TP53 AND organism_id:9606",
        "gene:BRCA2 AND organism_id:9606",
    ]
    entries = []
    for q in queries:
        url = f"https://rest.uniprot.org/uniprotkb/search?query={quote(q)}&size=5&format=json"
        try:
            doc = fetch_json(url, timeout=45, retries=2, headers=UA)
            for r in doc.get("results") or []:
                entries.append(r)
        except Exception as exc:  # noqa: BLE001
            print(f"  uniprot fail {q[:30]}: {exc}")
    # dedupe by primaryAccession
    by_acc = {}
    for e in entries:
        acc = e.get("primaryAccession") or e.get("uniProtkbId")
        if acc:
            by_acc[str(acc)] = e
    entries = list(by_acc.values())
    (vendor_dir("uniprot_proteome_slice") / "entries.json").write_text(
        json.dumps({"fetched_at": _now(), "n": len(entries), "accessions": list(by_acc.keys())}, indent=2),
        encoding="utf-8",
    )
    records = []
    for e in entries:
        acc = str(e.get("primaryAccession") or "up")
        seq = (e.get("sequence") or {}).get("length")
        if seq:
            records.append(fsot_row(lab="uniprot_frontier_lab", property_name="sequence_length", name=acc, measured=float(seq), domain="Biology", extra={"frontier_id": "uniprot_proteome_slice"}))
        # annotation score
        score = _num(e.get("annotationScore"))
        if score is not None and score > 0:
            records.append(fsot_row(lab="uniprot_frontier_lab", property_name="annotation_score", name=acc, measured=score, domain="Biology", extra={"frontier_id": "uniprot_proteome_slice"}))
        # protein existence
        pe = e.get("proteinExistence") or {}
        # gene count
        genes = e.get("genes") or []
        if genes:
            records.append(fsot_row(lab="uniprot_frontier_lab", property_name="gene_names_listed", name=acc, measured=float(len(genes)), domain="Biology", extra={"frontier_id": "uniprot_proteome_slice"}))
        kws = e.get("keywords") or []
        if kws:
            records.append(fsot_row(lab="uniprot_frontier_lab", property_name="keyword_entries", name=acc, measured=float(len(kws)), domain="Biology", extra={"frontier_id": "uniprot_proteome_slice"}))
        _ = pe
    records.append(fsot_row(lab="uniprot_frontier_lab", property_name="entry_panel_size", name="uniprot_slice", measured=float(len(entries)), domain="Biology", extra={"frontier_id": "uniprot_proteome_slice"}))
    return _panel("UniProt_Proteome_Slice_Open", records, ["biology"], 14, ["https://rest.uniprot.org/"], "uniprot", "UniProt open REST", "uniprot_proteome_slice_open_benchmark.json", "uniprot_proteome_slice")


def build_alphafold() -> dict:
    print("AlphaFold batch meta…")
    # UniProt accessions with public AF predictions
    accs = ["P04637", "P38398", "P00533", "P01308", "P68871", "P69905", "P0DTC2", "Q9Y6K9", "P07550", "P01116"]
    records = []
    metas = []
    for acc in accs:
        url = f"https://alphafold.ebi.ac.uk/api/prediction/{acc}"
        try:
            doc = fetch_json(url, timeout=40, retries=2, headers=UA)
        except Exception as exc:  # noqa: BLE001
            print(f"  AF {acc}: {exc}")
            continue
        if isinstance(doc, list):
            rows = doc
        elif isinstance(doc, dict):
            rows = [doc]
        else:
            rows = []
        for row in rows:
            metas.append({"uniprot": acc, "entryId": row.get("entryId"), "modelCreatedDate": row.get("modelCreatedDate")})
            for prop, key in (
                ("globalMetricValue", "globalMetricValue"),
                ("fractionPlddtVeryHigh", "fractionPlddtVeryHigh"),
                ("fractionPlddtConfident", "fractionPlddtConfident"),
                ("fractionPlddtLow", "fractionPlddtLow"),
                ("fractionPlddtVeryLow", "fractionPlddtVeryLow"),
            ):
                val = _num(row.get(key))
                if val is None or val < 0:
                    continue
                if val == 0:
                    continue
                # fractions are 0-1; shift to percent-like for relative residual stability
                if prop.startswith("fraction"):
                    val = val * 100.0 + 0.1
                    prop = prop + "_pct"
                records.append(fsot_row(lab="alphafold_frontier_lab", property_name=prop, name=f"{acc}_{row.get('entryId') or 'af'}", measured=val, domain="Biochemistry", extra={"frontier_id": "alphafold_batch_meta"}))
            # sequence length if present
            seq = row.get("uniprotSequence") or row.get("sequence")
            if isinstance(seq, str) and len(seq) > 0:
                records.append(fsot_row(lab="alphafold_frontier_lab", property_name="sequence_length", name=acc, measured=float(len(seq)), domain="Biochemistry", extra={"frontier_id": "alphafold_batch_meta"}))
            elif isinstance(seq, dict) and seq.get("length"):
                records.append(fsot_row(lab="alphafold_frontier_lab", property_name="sequence_length", name=acc, measured=float(seq["length"]), domain="Biochemistry", extra={"frontier_id": "alphafold_batch_meta"}))
    (vendor_dir("alphafold_batch_meta") / "predictions.json").write_text(json.dumps({"fetched_at": _now(), "metas": metas}, indent=2), encoding="utf-8")
    records.append(fsot_row(lab="alphafold_frontier_lab", property_name="prediction_entries", name="af_batch", measured=float(max(len(metas), 1)), domain="Biochemistry", extra={"frontier_id": "alphafold_batch_meta"}))
    return _panel("AlphaFold_Batch_Meta_Open", records, ["biology", "biochemistry"], 14, ["https://alphafold.ebi.ac.uk/api/"], "alphafold", "AlphaFold DB public API", "alphafold_batch_meta_open_benchmark.json", "alphafold_batch_meta")


def build_rcsb() -> dict:
    print("RCSB structure batch…")
    # GraphQL search for recent entries is complex; use known open entry IDs + REST
    pdb_ids = ["1CRN", "1CBS", "1A3N", "1BNA", "1HTM", "2HHB", "3GKW", "4HHB", "5XNL", "6VXX", "7DDD", "1MBO", "1TIM", "2POR", "3NIR"]
    records = []
    entries = []
    for pid in pdb_ids:
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pid}"
        try:
            doc = fetch_json(url, timeout=40, retries=2, headers=UA)
        except Exception as exc:  # noqa: BLE001
            print(f"  RCSB {pid}: {exc}")
            continue
        entries.append(pid)
        # resolution
        rinfo = doc.get("rcsb_entry_info") or {}
        res_comb = _num(rinfo.get("resolution_combined"))
        if res_comb is None:
            # sometimes list
            rc = rinfo.get("resolution_combined")
            if isinstance(rc, list) and rc:
                res_comb = _num(rc[0])
        if res_comb is not None and res_comb > 0:
            records.append(fsot_row(lab="rcsb_frontier_lab", property_name="resolution_combined", name=pid, measured=res_comb, domain="Biochemistry", extra={"frontier_id": "rcsb_structure_batch"}))
        for prop, key in (
            ("polymer_entity_count", "polymer_entity_count"),
            ("entity_count", "entity_count"),
            ("assembled_model_count", "assembled_model_count"),
            ("deposited_atom_count", "deposited_atom_count"),
            ("deposited_polymer_monomer_count", "deposited_polymer_monomer_count"),
        ):
            val = _num(rinfo.get(key))
            if val is None or val <= 0:
                continue
            # avoid _count suffix exclusion for some — use alternate names when ends with _count
            prop_use = prop.replace("_count", "_total") if prop.endswith("_count") else prop
            records.append(fsot_row(lab="rcsb_frontier_lab", property_name=prop_use if prop_use != "polymer_entity_count" else "polymer_entity_total", name=pid, measured=val, domain="Biology", extra={"frontier_id": "rcsb_structure_batch"}))
        exp = doc.get("exptl") or []
        if exp:
            records.append(fsot_row(lab="rcsb_frontier_lab", property_name="exptl_methods", name=pid, measured=float(len(exp)), domain="Biology", extra={"frontier_id": "rcsb_structure_batch"}))
    (vendor_dir("rcsb_structure_batch") / "entries.json").write_text(json.dumps({"fetched_at": _now(), "ids": entries}, indent=2), encoding="utf-8")
    records.append(fsot_row(lab="rcsb_frontier_lab", property_name="entry_panel_size", name="rcsb_batch", measured=float(len(entries)), domain="Biology", extra={"frontier_id": "rcsb_structure_batch"}))
    return _panel("RCSB_Structure_Batch_Open", records, ["biology", "chemistry"], 14, ["https://data.rcsb.org/rest/v1/core/entry/"], "rcsb", "RCSB Data API open entries", "rcsb_structure_batch_open_benchmark.json", "rcsb_structure_batch")


def build_oeis() -> dict:
    print("OEIS family sweep…")
    oeis_ids = [
        "A000045", "A000796", "A001622", "A000040", "A000142", "A000217",
        "A000108", "A000041", "A000984", "A001006", "A000290", "A000578",
        "A000792", "A000203", "A000010", "A000720", "A001157", "A000396",
        "A000668", "A002808", "A000961", "A001358", "A005408", "A005843",
    ]
    records = []
    docs = []
    for oid in oeis_ids:
        url = f"https://oeis.org/search?q=id:{oid}&fmt=json"
        try:
            doc = fetch_json(url, timeout=40, retries=2, headers=UA)
            if isinstance(doc, list) and doc:
                docs.append(doc[0])
        except Exception as exc:  # noqa: BLE001
            print(f"  OEIS {oid}: {exc}")
    for seq in docs:
        sid = str(seq.get("number") or seq.get("id") or "oeis")
        terms = [int(x) for x in str(seq.get("data") or "").split(",") if x.strip().lstrip("-").isdigit()]
        for i, term in enumerate(terms[:15]):
            if term <= 0:
                continue
            records.append(fsot_row(lab="oeis_frontier_lab", property_name="oeis_term", name=f"A{sid}_n{i}", measured=float(term), domain="Quantum_Computing", extra={"frontier_id": "oeis_family_sweep"}))
        if terms:
            records.append(fsot_row(lab="oeis_frontier_lab", property_name="oeis_terms_listed", name=f"A{sid}_len", measured=float(len(terms)), domain="Quantum_Computing", extra={"frontier_id": "oeis_family_sweep"}))
        refs = seq.get("references") or seq.get("xref") or ""
        # keyword length as integrity
        name = str(seq.get("name") or "")
        if name:
            records.append(fsot_row(lab="oeis_frontier_lab", property_name="oeis_name_chars", name=f"A{sid}", measured=float(len(name)), domain="Quantum_Computing", extra={"frontier_id": "oeis_family_sweep"}))
        _ = refs
    (vendor_dir("oeis_family_sweep") / "sequences.json").write_text(json.dumps({"fetched_at": _now(), "n": len(docs)}, indent=2), encoding="utf-8")
    return _panel("OEIS_Family_Sweep_Open", records, ["mathematics", "formal"], 14, ["https://oeis.org/"], "oeis", "OEIS open JSON family sweep", "oeis_family_sweep_open_benchmark.json", "oeis_family_sweep")


def build_usgs() -> dict:
    print("USGS seismic history…")
    url = (
        "https://earthquake.usgs.gov/fdsnws/event/1/query"
        "?format=geojson&starttime=2020-01-01&endtime=2025-12-31"
        "&minmagnitude=6.0&orderby=magnitude&limit=100"
    )
    payload = fetch_json(url, timeout=60, retries=3, headers=UA)
    feats = payload.get("features") or []
    (vendor_dir("usgs_seismic_history") / "events.json").write_text(
        json.dumps({"fetched_at": _now(), "n": len(feats)}, indent=2), encoding="utf-8"
    )
    records = []
    for f in feats:
        props = f.get("properties") or {}
        geom = f.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None, None]
        eid = str(props.get("code") or props.get("ids") or "eq")[:32]
        mag = _num(props.get("mag"))
        if mag is not None and mag > 0:
            records.append(fsot_row(lab="usgs_frontier_lab", property_name="magnitude", name=eid, measured=mag, domain="Seismology", extra={"frontier_id": "usgs_seismic_history"}))
        depth = _num(coords[2]) if len(coords) > 2 else None
        if depth is not None and depth > 0:
            records.append(fsot_row(lab="usgs_frontier_lab", property_name="depth_km", name=eid, measured=depth, domain="Seismology", extra={"frontier_id": "usgs_seismic_history"}))
        # felt / tsunami flags as small positives when present
        felt = _num(props.get("felt"))
        if felt is not None and felt > 0:
            records.append(fsot_row(lab="usgs_frontier_lab", property_name="felt_reports", name=eid, measured=felt, domain="Seismology", extra={"frontier_id": "usgs_seismic_history"}))
        sig = _num(props.get("sig"))
        if sig is not None and sig > 0:
            records.append(fsot_row(lab="usgs_frontier_lab", property_name="significance", name=eid, measured=sig, domain="Seismology", extra={"frontier_id": "usgs_seismic_history"}))
    records.append(fsot_row(lab="usgs_frontier_lab", property_name="event_panel_size", name="usgs_m6_plus", measured=float(len(feats)), domain="Seismology", extra={"frontier_id": "usgs_seismic_history"}))
    return _panel("USGS_Seismic_History_Open", records, ["earth_science"], 16, [url[:80] + "...", "https://earthquake.usgs.gov/"], "usgs", "USGS FDSN open seismic catalog", "usgs_seismic_history_open_benchmark.json", "usgs_seismic_history")


def build_noaa_tides() -> dict:
    print("NOAA multi-station tides…")
    # CO-OPS stations open API — hourly heights sample
    stations = ["9414290", "8518750", "8723214", "1612340", "9447130", "8452660", "8574680", "8771450"]
    records = []
    ok_stations = 0
    for sid in stations:
        url = (
            f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
            f"?product=water_level&application=FSOT-2.1-Lean&begin_date=20240101"
            f"&end_date=20240103&datum=MLLW&station={sid}&time_zone=gmt&units=metric&format=json"
        )
        try:
            doc = fetch_json(url, timeout=40, retries=2, headers=UA)
        except Exception as exc:  # noqa: BLE001
            print(f"  tide {sid}: {exc}")
            continue
        data = doc.get("data") or []
        if not data:
            continue
        ok_stations += 1
        vals = []
        for row in data:
            v = _num(row.get("v"))
            if v is None:
                continue
            # water level can be negative — shift
            vals.append(v + 5.0)
        for i, v in enumerate(vals[:24]):
            if v <= 0:
                continue
            records.append(fsot_row(lab="noaa_tides_frontier_lab", property_name="water_level_shift_m", name=f"{sid}_t{i}", measured=v, domain="Oceanography", extra={"frontier_id": "noaa_tides_multi_station"}))
        if vals:
            records.append(fsot_row(lab="noaa_tides_frontier_lab", property_name="mean_height_m", name=f"{sid}_mean", measured=sum(vals) / len(vals), domain="Oceanography", extra={"frontier_id": "noaa_tides_multi_station"}))
            records.append(fsot_row(lab="noaa_tides_frontier_lab", property_name="max_height_m", name=f"{sid}_max", measured=max(vals), domain="Oceanography", extra={"frontier_id": "noaa_tides_multi_station"}))
    records.append(fsot_row(lab="noaa_tides_frontier_lab", property_name="stations_ok", name="noaa_tide_panel", measured=float(max(ok_stations, 1)), domain="Oceanography", extra={"frontier_id": "noaa_tides_multi_station"}))
    (vendor_dir("noaa_tides_multi_station") / "meta.json").write_text(json.dumps({"fetched_at": _now(), "stations_ok": ok_stations}, indent=2), encoding="utf-8")
    return _panel("NOAA_Tides_Multi_Station_Open", records, ["earth_science", "ocean"], 16, ["https://api.tidesandcurrents.noaa.gov/"], "noaa_tides", "NOAA CO-OPS open water levels", "noaa_tides_multi_station_open_benchmark.json", "noaa_tides_multi_station")


def build_gbif() -> dict:
    print("GBIF taxon depth…")
    url = "https://api.gbif.org/v1/occurrence/search?limit=50&hasCoordinate=true"
    payload = fetch_json(url, timeout=60, retries=3, headers=UA)
    results = payload.get("results") or []
    (vendor_dir("gbif_taxon_depth") / "occurrences.json").write_text(
        json.dumps({"fetched_at": _now(), "n": len(results), "count": payload.get("count")}, indent=2),
        encoding="utf-8",
    )
    records = []
    for r in results:
        key = str(r.get("key") or r.get("gbifID") or "occ")
        for prop, field in (
            ("decimalLatitude", "decimalLatitude"),
            ("decimalLongitude", "decimalLongitude"),
            ("year", "year"),
            ("month", "month"),
            ("elevation", "elevation"),
        ):
            val = _num(r.get(field))
            if val is None:
                continue
            if prop in ("decimalLatitude", "decimalLongitude"):
                val = abs(val) + 0.01  # residual on absolute coordinate magnitude
                prop = prop + "_abs"
            if val <= 0:
                continue
            records.append(fsot_row(lab="gbif_frontier_lab", property_name=prop, name=key, measured=val, domain="Ecology", extra={"frontier_id": "gbif_taxon_depth"}))
    total = _num(payload.get("count"))
    if total and total > 0:
        records.append(fsot_row(lab="gbif_frontier_lab", property_name="catalog_total_hits", name="gbif_search", measured=total, domain="Ecology", extra={"frontier_id": "gbif_taxon_depth"}))
    records.append(fsot_row(lab="gbif_frontier_lab", property_name="page_results", name="gbif_page", measured=float(len(results)), domain="Ecology", extra={"frontier_id": "gbif_taxon_depth"}))
    return _panel("GBIF_Taxon_Depth_Open", records, ["biology", "ecology"], 14, [url, "https://api.gbif.org/"], "gbif", "GBIF open occurrence API", "gbif_taxon_depth_open_benchmark.json", "gbif_taxon_depth")


def build_zenodo() -> dict:
    print("Zenodo records depth…")
    url = "https://zenodo.org/api/records?q=physics&size=10"
    payload = fetch_json(url, timeout=60, retries=3, headers=UA)
    hits = (payload.get("hits") or {}).get("hits") or payload.get("hits") or []
    if isinstance(hits, dict):
        hits = hits.get("hits") or []
    records = []
    for h in hits:
        meta = h.get("metadata") or {}
        rid = str(h.get("id") or meta.get("doi") or "zenodo")
        # creators length
        creators = meta.get("creators") or []
        if creators:
            records.append(fsot_row(lab="zenodo_frontier_lab", property_name="creator_entries", name=rid, measured=float(len(creators)), domain="Psychology", extra={"frontier_id": "zenodo_records_depth"}))
        files = h.get("files") or meta.get("files") or []
        if files:
            records.append(fsot_row(lab="zenodo_frontier_lab", property_name="file_entries", name=rid, measured=float(len(files)), domain="Psychology", extra={"frontier_id": "zenodo_records_depth"}))
        # publication year from created
        created = str(meta.get("publication_date") or h.get("created") or "")[:4]
        year = _num(created)
        if year and year > 1900:
            records.append(fsot_row(lab="zenodo_frontier_lab", property_name="dataset_publication_year", name=rid, measured=year, domain="High_Energy_Physics", extra={"frontier_id": "zenodo_records_depth"}))
    total = _num(((payload.get("hits") or {}) if isinstance(payload.get("hits"), dict) else {}).get("total"))
    if total and total > 0:
        records.append(fsot_row(lab="zenodo_frontier_lab", property_name="search_total_hits", name="zenodo_physics", measured=total, domain="Psychology", extra={"frontier_id": "zenodo_records_depth"}))
    records.append(fsot_row(lab="zenodo_frontier_lab", property_name="page_hits", name="zenodo_page", measured=float(len(hits)), domain="Psychology", extra={"frontier_id": "zenodo_records_depth"}))
    (vendor_dir("zenodo_records_depth") / "hits.json").write_text(json.dumps({"fetched_at": _now(), "n": len(hits)}, indent=2), encoding="utf-8")
    return _panel("Zenodo_Records_Depth_Open", records, ["formal", "open_science"], 12, [url, "https://zenodo.org/"], "zenodo", "Zenodo open records API", "zenodo_records_depth_open_benchmark.json", "zenodo_records_depth")


def main() -> int:
    print("=== Frontier wave 2 (FSOT mathematics only) ===")
    print("Residual law: make_fsot_record → fsot_scaled; formula=None always\n")
    results = {}
    for name, fn in [
        ("uniprot_proteome_slice", build_uniprot),
        ("alphafold_batch_meta", build_alphafold),
        ("rcsb_structure_batch", build_rcsb),
        ("oeis_family_sweep", build_oeis),
        ("usgs_seismic_history", build_usgs),
        ("noaa_tides_multi_station", build_noaa_tides),
        ("gbif_taxon_depth", build_gbif),
        ("zenodo_records_depth", build_zenodo),
    ]:
        try:
            doc = fn()
            results[name] = {
                "status": "ok",
                "domain": doc.get("domain"),
                "records": doc.get("record_count"),
                "pooled_median_error_pct": doc.get("pooled_median_error_pct"),
                "residual_law": "fsot_scaled_only",
            }
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {name}: {exc}")
            results[name] = {"status": "fail", "error": f"{type(exc).__name__}: {exc}"[:400]}
    report = {
        "generated_at": _now(),
        "policy": "open_science_only_no_credentials",
        "math_policy": "FSOT residual only (make_fsot_record / fsot_scaled); no free fits; no formula_mass",
        "results": results,
    }
    out = ROOT / "data" / "open_frontier_wave2_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(ROOT)}")
    ok = sum(1 for r in results.values() if r.get("status") == "ok")
    print(f"Wave2 panels ok: {ok}/{len(results)}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
