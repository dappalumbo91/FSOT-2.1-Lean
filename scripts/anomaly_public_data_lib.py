"""Public anomaly observables ingest — consciousness, SH0ES, dark-energy CPL (G: cache)."""

from __future__ import annotations

import csv
import json
import os
import re
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = Path(r"G:\FSOT-PublicData\anomaly_observables")

SH0ES_FILES = (
    "SH0ES_Data/optical_wes_R22_for19fromR16.dat",
    "SH0ES_Data/R22_orig19_NIR.out",
    "SH0ES_Data/lstsq_results.txt",
    "SH0ES_Data/README.md",
    "SH0ES_Data/table2.README",
)
SH0ES_FITS = (
    "SH0ES_Data/alll_shoes_ceph_topantheonwt6.0_112221.fits",
    "SH0ES_Data/ally_shoes_ceph_topantheonwt6.0_112221.fits",
    "SH0ES_Data/allc_shoes_ceph_topantheonwt6.0_112221.fits",
)
SH0ES_RAW = "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main"
ANAGE_URL = "https://genomics.senescence.info/species/dataset.zip"
OPENNEURO_URL = "https://openneuro.org/crn/graphql"

HOST_ALIASES = {
    "N1015": "NGC1015",
    "N1309": "NGC1309",
    "N1365": "NGC1365",
    "N1448": "NGC1448",
    "N2442": "NGC2442",
    "N3021": "NGC3021",
    "N3370": "NGC3370",
    "N3447": "NGC3447",
    "N3972": "NGC3972",
    "N3982": "NGC3982",
    "N4038": "NGC4038",
    "N4258": "NGC4258",
    "N4424": "NGC4424",
    "N4536": "NGC4536",
    "N4639": "NGC4639",
    "N5584": "NGC5584",
    "N5917": "NGC5917",
    "N7250": "NGC7250",
    "U9391": "UGC9391",
}

ORDER_BRAIN_FRAC = {
    "Primates": 0.22,
    "Rodentia": 0.10,
    "Carnivora": 0.15,
    "Chiroptera": 0.08,
    "Artiodactyla": 0.12,
    "Cetacea": 0.10,
    "Proboscidea": 0.12,
    "Lagomorpha": 0.11,
    "Diprotodontia": 0.09,
    "Perissodactyla": 0.11,
    "Sirenia": 0.09,
    "Pholidota": 0.10,
    "Macroscelidea": 0.11,
}
DEFAULT_MAMMAL_FRAC = 0.12

MANUAL_SPECIES = {
    "Homo sapiens",
    "Pan troglodytes",
    "Macaca mulatta",
    "Mus musculus",
    "Rattus norvegicus",
    "Canis familiaris",
    "Heterocephalus glaber",
    "Elephas maximus",
    "Balaena mysticetus",
    "Delphinus delphis",
}


def cache_root() -> Path:
    raw = os.environ.get("FSOT_ANOMALY_CACHE_ROOT", "").strip()
    if raw:
        root = Path(raw).expanduser()
    elif DEFAULT_CACHE.exists() or Path("G:/").exists():
        root = DEFAULT_CACHE
    else:
        root = ROOT / "data" / "anomaly_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def vendor_path(domain: str, filename: str) -> Path:
    path = ROOT / "vendor" / "public_data" / domain / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/anomaly-ingest"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def _graphql(query: str) -> dict:
    req = urllib.request.Request(
        OPENNEURO_URL,
        data=json.dumps({"query": query}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "FSOT-2.1-Lean/anomaly-ingest"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def _float_or_none(val: str | None) -> float | None:
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_ceph_dat(path: Path) -> tuple[list[dict], int]:
    hosts: dict[str, dict] = {}
    cepheid_count = 0
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("-") or line.startswith("Host"):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                ra = float(parts[1])
                dec = float(parts[2])
            except ValueError:
                continue
            host = parts[0]
            cepheid_count += 1
            bucket = hosts.setdefault(
                host, {"host": host, "cepheid_count": 0, "ra_vals": [], "dec_vals": []}
            )
            bucket["cepheid_count"] += 1
            bucket["ra_vals"].append(ra)
            bucket["dec_vals"].append(dec)

    host_list = []
    for host, row in sorted(hosts.items()):
        ra_vals = row["ra_vals"]
        dec_vals = row["dec_vals"]
        canonical = HOST_ALIASES.get(host, host)
        host_list.append(
            {
                "host": host,
                "canonical_name": canonical,
                "cepheid_count": row["cepheid_count"],
                "ra_deg_mean": sum(ra_vals) / len(ra_vals),
                "dec_deg_mean": sum(dec_vals) / len(dec_vals),
            }
        )
    return host_list, cepheid_count


def _parse_lstsq(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                val = float(parts[0])
                err = float(parts[1])
            except ValueError:
                continue
            rows.append({"row": idx, "value": val, "sigma": err})
    return rows


def ingest_anage() -> dict:
    cache = cache_root() / "consciousness"
    zip_path = cache / "anage_dataset.zip"
    extract_dir = cache / "anage"
    if not (extract_dir / "anage_data.txt").exists():
        _fetch(ANAGE_URL, zip_path)
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

    data_path = extract_dir / "anage_data.txt"
    species_rows: list[dict] = []
    with_metabolic = 0
    with data_path.open(encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            mr = (row.get("Metabolic rate (W)") or "").strip()
            if not mr:
                continue
            with_metabolic += 1
            genus = (row.get("Genus") or "").strip()
            species = (row.get("Species") or "").strip()
            species_rows.append(
                {
                    "hagrid": row.get("HAGRID"),
                    "name": f"{genus} {species}".strip(),
                    "common_name": row.get("Common name"),
                    "metabolic_rate_w": float(mr),
                    "body_mass_g": _float_or_none(row.get("Body mass (g)")),
                    "adult_weight_g": _float_or_none(row.get("Adult weight (g)")),
                    "kingdom": row.get("Kingdom"),
                    "class": row.get("Class"),
                    "order": row.get("Order"),
                    "family": row.get("Family"),
                }
            )

    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_url": ANAGE_URL,
        "cache_path": str(data_path),
        "species_with_metabolic_rate": with_metabolic,
        "rows": species_rows,
    }
    vendor_path("consciousness", "anage_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


def ingest_consciousness_species_panel() -> dict:
    """Build AnAge mammal cross-species panel with taxon brain-energy fractions."""
    anage_summary = vendor_path("consciousness", "anage_summary.json")
    if not anage_summary.exists():
        ingest_anage()
    rows = json.loads(anage_summary.read_text(encoding="utf-8")).get("rows") or []
    mammals = [r for r in rows if (r.get("class") or "").strip() == "Mammalia"]
    by_order: dict[str, list[dict]] = {}
    for row in mammals:
        order = (row.get("order") or "Unknown").strip()
        by_order.setdefault(order, []).append(row)

    panel: list[dict] = []
    for order, order_rows in sorted(by_order.items()):
        order_rows.sort(key=lambda r: float(r["metabolic_rate_w"]))
        picks = []
        if len(order_rows) <= 3:
            picks = order_rows
        else:
            picks = [order_rows[0], order_rows[len(order_rows) // 2], order_rows[-1]]
        frac = ORDER_BRAIN_FRAC.get(order, DEFAULT_MAMMAL_FRAC)
        for row in picks:
            name = str(row["name"])
            if name in MANUAL_SPECIES:
                continue
            panel.append(
                {
                    "name": name,
                    "anage_hagrid": row.get("hagrid"),
                    "total_metabolic_w": float(row["metabolic_rate_w"]),
                    "brain_energy_fraction": frac,
                    "order": order,
                    "family": row.get("family"),
                    "reference": f"AnAge_HAGR_{order.lower()}_taxon_fraction",
                }
            )

    cache = cache_root() / "consciousness"
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / "anage_species_panel.json"
    doc = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "mammal_count": len(mammals),
        "panel_count": len(panel),
        "orders_represented": sorted(by_order.keys()),
        "species": panel,
    }
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    vendor_path("consciousness", "anage_species_panel.json").write_text(
        json.dumps(doc, indent=2), encoding="utf-8"
    )

    ref_path = ROOT / "data" / "consciousness_reference_observables.json"
    ref = json.loads(ref_path.read_text(encoding="utf-8"))
    manual = ref.get("species") or []
    manual_names = {str(s["name"]) for s in manual}
    merged = manual + [s for s in panel if s["name"] not in manual_names]
    ref["species"] = merged
    ref["anage_panel_count"] = len(panel)
    ref["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ref_path.write_text(json.dumps(ref, indent=2), encoding="utf-8")
    doc["reference_path"] = str(ref_path)
    doc["merged_species_count"] = len(merged)
    return doc


def ingest_openneuro() -> dict:
    """Cache OpenNeuro EEG/MRI dataset metadata for consciousness channel proxies."""
    cache = cache_root() / "consciousness" / "openneuro"
    cache.mkdir(parents=True, exist_ok=True)
    datasets: list[dict] = []
    for modality in ("EEG", "MRI"):
        cursor = None
        pages = 0
        while pages < 6:
            after = f', after: "{cursor}"' if cursor else ""
            q = (
                "{ datasets(first: 10, modality: \"%s\"%s) {"
                " pageInfo { hasNextPage }"
                " edges { cursor node { id name } } } }"
            ) % (modality, after)
            payload = _graphql(q)
            block = (payload.get("data") or {}).get("datasets") or {}
            edges = block.get("edges") or []
            for edge in edges:
                node = edge.get("node") or {}
                datasets.append(
                    {
                        "id": node.get("id"),
                        "name": node.get("name"),
                        "modality_filter": modality,
                    }
                )
            page = block.get("pageInfo") or {}
            if not page.get("hasNextPage") or not edges:
                break
            cursor = edges[-1].get("cursor")
            pages += 1

    curated_ids = ("ds000224", "ds001787", "ds003645", "ds004148")
    for ds_id in curated_ids:
        try:
            q = '{ dataset(id: "%s") { id name } }' % ds_id
            payload = _graphql(q)
            node = (payload.get("data") or {}).get("dataset")
            if node:
                datasets.append(
                    {
                        "id": node.get("id"),
                        "name": node.get("name"),
                        "modality_filter": "curated",
                    }
                )
        except Exception:
            continue

    seen: set[str] = set()
    unique: list[dict] = []
    for row in datasets:
        ds_id = str(row.get("id") or "")
        if not ds_id or ds_id in seen:
            continue
        seen.add(ds_id)
        unique.append(row)

    out = cache / "openneuro_index.json"
    doc = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source": OPENNEURO_URL,
        "dataset_count": len(unique),
        "datasets": unique[:60],
    }
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    vendor_path("consciousness", "openneuro_summary.json").write_text(
        json.dumps(doc, indent=2), encoding="utf-8"
    )
    return doc


def ingest_sh0es() -> dict:
    cache = cache_root() / "sh0es"
    cache.mkdir(parents=True, exist_ok=True)
    for rel in SH0ES_FILES + SH0ES_FITS:
        dest = cache / Path(rel).name
        if not dest.exists() or dest.stat().st_size < 100:
            _fetch(f"{SH0ES_RAW}/{rel}", dest)

    optical_hosts, optical_cepheids = _parse_ceph_dat(cache / "optical_wes_R22_for19fromR16.dat")
    nir_hosts, nir_cepheids = _parse_ceph_dat(cache / "R22_orig19_NIR.out")
    lstsq = _parse_lstsq(cache / "lstsq_results.txt")

    merged_hosts: dict[str, dict] = {}
    for source, rows in (("optical", optical_hosts), ("nir", nir_hosts)):
        for row in rows:
            host = str(row["host"])
            bucket = merged_hosts.setdefault(
                host,
                {
                    "host": host,
                    "canonical_name": row.get("canonical_name") or HOST_ALIASES.get(host, host),
                    "optical_cepheid_count": 0,
                    "nir_cepheid_count": 0,
                    "ra_deg_mean": row["ra_deg_mean"],
                    "dec_deg_mean": row["dec_deg_mean"],
                },
            )
            if source == "optical":
                bucket["optical_cepheid_count"] = row["cepheid_count"]
                bucket["ra_deg_mean"] = row["ra_deg_mean"]
                bucket["dec_deg_mean"] = row["dec_deg_mean"]
            else:
                bucket["nir_cepheid_count"] = row["cepheid_count"]

    host_list = sorted(merged_hosts.values(), key=lambda r: r["host"])
    for row in host_list:
        row["cepheid_count"] = int(row.get("optical_cepheid_count") or 0) + int(
            row.get("nir_cepheid_count") or 0
        )

    fits_sizes = {
        p.name: p.stat().st_size for p in cache.glob("*.fits") if p.exists()
    }

    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_repo": "PantheonPlusSH0ES/DataRelease",
        "cache_dir": str(cache),
        "optical_cepheid_row_count": optical_cepheids,
        "nir_cepheid_row_count": nir_cepheids,
        "host_count": len(host_list),
        "hosts": host_list,
        "lstsq_rows": lstsq[:40],
        "fits_file_bytes": fits_sizes,
    }
    vendor_path("sh0es", "sh0es_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (cache / "sh0es_hosts_parsed.json").write_text(json.dumps(host_list, indent=2), encoding="utf-8")
    return summary


def ingest_dark_energy_cpl() -> dict:
    ref_path = ROOT / "data" / "dark_energy_cpl_reference.json"
    ref = json.loads(ref_path.read_text(encoding="utf-8"))
    cache = cache_root() / "dark_energy_cpl"
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / "cpl_reference.json"
    out.write_text(json.dumps(ref, indent=2), encoding="utf-8")
    summary = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "cache_path": str(out),
        "constraint_count": len(ref.get("published_constraints") or []),
        "fsot_w0": ref["fsot_prediction"]["w0"],
        "fsot_wa": ref["fsot_prediction"]["wa"],
        "status": ref["fsot_prediction"]["status"],
    }
    vendor_path("dark_energy_cpl", "cpl_constraints_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


INGESTORS = {
    "consciousness_anage": ingest_anage,
    "consciousness_species_panel": ingest_consciousness_species_panel,
    "consciousness_openneuro": ingest_openneuro,
    "sh0es_ceph": ingest_sh0es,
    "dark_energy_cpl": ingest_dark_energy_cpl,
}