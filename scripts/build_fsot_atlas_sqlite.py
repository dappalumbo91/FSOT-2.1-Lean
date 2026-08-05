#!/usr/bin/env python3
"""Build data/fsot_atlas.sqlite — professional residual atlas (math unchanged).

Open-science only: no credentials. Rebuilds from:
  - data/benchmark_margin_audit.json
  - data/*benchmark*.json material_records
  - data/benchmark_anchor_citation_ledger.json (if present)
  - data/api_requirements.yaml (auth: none)
  - scripts/open_science_sources_lib.py
  - curated high-value open gaps

Does NOT recompute FSOT seeds. Authority remains vendor/fsot_compute.py.
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
CITATION_LEDGER = ROOT / "data" / "benchmark_anchor_citation_ledger.json"
API_REQ = ROOT / "data" / "api_requirements.yaml"
OUT_DB = ROOT / "data" / "fsot_atlas.sqlite"
OUT_REPORT = ROOT / "data" / "fsot_atlas_build_report.json"
MATH_AUDIT = ROOT / "data" / "fsot_system_math_audit.json"
HIERARCHY = ROOT / "data" / "fsot_building_block_hierarchy.json"
NETWORK = ROOT / "data" / "fsot_domain_formula_network.json"

# Huge catalogs: store sample only (full JSON remains authority)
LARGE_RECORD_THRESHOLD = 10_000
LARGE_SAMPLE_N = 5_000

FAMILY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("physics_particle_cosmo", re.compile(
        r"phys|particle|plasma|quantum|higgs|ckm|pmns|neutrino|fusion|nuclear|atomic|"
        r"cosmo|gravity|einstein|h0|planck|desi|sh0es|dark_energy|pdg|orbital|stellar|"
        r"galactic|black.?hole|spacetime|mpcorb|gaia|exoplanet|relativ|gr_sm|toe_|"
        r"founding_|weak_field|perihelion|friedmann|cmb|bao|pulsar|cosmic",
        re.I,
    )),
    ("chemistry_materials", re.compile(
        r"chem|material|pubchem|smiles|crc|metamaterial|semiconductor|periodic|"
        r"superheavy|island|alloy|polymer|rcsb|chembl",
        re.I,
    )),
    ("biology_life", re.compile(
        r"bio|genom|gene|protein|uniprot|ncbi|cell|neuron|neuro|immun|oncol|"
        r"longevity|species|ecology|igem|synthetic|brenda|allen|zebra|virology|"
        r"clinical|pharmac|ensembl|alphafold|openneuro",
        re.I,
    )),
    ("earth_climate", re.compile(
        r"climate|atmospher|ocean|seism|geo|hydro|cryo|magnetosphere|weather|"
        r"soil|tectonic|ozone|usgs|noaa|ncei",
        re.I,
    )),
    ("math_formal_compute", re.compile(
        r"math|formula|proof|lean|formal|trinary|fractal|comput|dlmf|oeis|scalar",
        re.I,
    )),
    ("consciousness_social", re.compile(
        r"conscious|soul|psych|econ|linguis|social|music|creative|archetype|philosophy",
        re.I,
    )),
    ("engineering_hardware", re.compile(
        r"fuel|propulsion|hardware|esp32|qemu|circuit|engineering|transport|"
        r"desktop|gpu|ram|cache|os_path|trinary_os|pack",
        re.I,
    )),
    ("open_science_meta", re.compile(
        r"open.?science|citation|cross.?proof|verification|prereg|portable|"
        r"navigator|adversarial|atlas|inventory",
        re.I,
    )),
]

# High-value gaps: open data only (no credentials)
HIGH_VALUE_GAPS: list[dict[str, str]] = [
    {
        "id": "condensed_matter_open_cod",
        "family": "chemistry_materials",
        "title": "Crystallography Open Database / open materials structures",
        "open_url": "https://www.crystallography.net/cod/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: COD OPTIMADE residual panel (open MP substitute). "
            "data/cod_optimade_structures_benchmark.json via "
            "scripts/build_open_credential_replacements.py."
        ),
    },
    {
        "id": "nuclear_endf_public",
        "family": "physics_particle_cosmo",
        "title": "ENDF/B or IAEA public nuclear data evaluations",
        "open_url": "https://www-nds.iaea.org/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: IAEA Live Chart ground states + AME2020 open mass table. "
            "data/nuclear_iaea_open_benchmark.json"
        ),
    },
    {
        "id": "nist_asd_spectroscopy",
        "family": "physics_particle_cosmo",
        "title": "NIST Atomic Spectra Database",
        "open_url": "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: NIST handbook H/He/Na/Ca line anchors + handbook page. "
            "data/nist_asd_spectroscopy_open_benchmark.json"
        ),
    },
    {
        "id": "nufit_neutrino",
        "family": "physics_particle_cosmo",
        "title": "NuFIT open neutrino oscillation parameters",
        "open_url": "http://www.nu-fit.org/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: NuFit-6.0 open literature table (arXiv:2410.05380). "
            "data/nufit_neutrino_open_benchmark.json"
        ),
    },
    {
        "id": "gwtc_catalog",
        "family": "physics_particle_cosmo",
        "title": "GWTC gravitational-wave event catalog (GWOSC)",
        "open_url": "https://gwosc.org/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: live GWTC catalog residual panel (masses, chirp, distance, SNR). "
            "data/gwtc_catalog_open_benchmark.json"
        ),
    },
    {
        "id": "desi_public_dr",
        "family": "physics_particle_cosmo",
        "title": "DESI public data releases",
        "open_url": "https://data.desi.lbl.gov/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: public portal + BAO/cosmology open literature anchors + wa panel. "
            "data/desi_public_depth_open_benchmark.json"
        ),
    },
    {
        "id": "era5_climate_open",
        "family": "earth_climate",
        "title": "Climate reanalysis open subsets (NCEI open substitute for CDS)",
        "open_url": "https://www.ncei.noaa.gov/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered via NCEI Climate-at-a-Glance open global land+ocean series "
            "(no CDS account). data/ncei_climate_open_benchmark.json"
        ),
    },
    {
        "id": "owid_epidemiology",
        "family": "biology_life",
        "title": "Our World in Data public health / epidemiology CSVs",
        "open_url": "https://github.com/owid/covid-19-data",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: OWID covid latest CSV multi-country residual panel. "
            "data/owid_epidemiology_open_benchmark.json"
        ),
    },
    {
        "id": "chembl_deep",
        "family": "chemistry_materials",
        "title": "ChEMBL open pharmacology (deeper than single-molecule probes)",
        "open_url": "https://www.ebi.ac.uk/chembl/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: multi-molecule ChEMBL property panel (MW, ALogP, PSA, …). "
            "data/chembl_deep_open_benchmark.json"
        ),
    },
    {
        "id": "openneuro_depth",
        "family": "biology_life",
        "title": "OpenNeuro public BIDS datasets",
        "open_url": "https://openneuro.org/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: public S3 BIDS dataset_description panel (15 datasets) + bundled summary. "
            "data/openneuro_depth_open_benchmark.json"
        ),
    },
    {
        "id": "world_bank_macro_open",
        "family": "consciousness_social",
        "title": "World Bank Open Data macro series (FRED substitute)",
        "open_url": "https://api.worldbank.org/v2/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: replaces FRED API key. data/world_bank_macro_open_benchmark.json "
            "(GDP, unemployment, CPI, population) + existing world_bank_development green."
        ),
    },
    {
        "id": "jarvis_dft_open",
        "family": "chemistry_materials",
        "title": "JARVIS-DFT via OPTIMADE (Materials Project substitute)",
        "open_url": "https://jarvis.nist.gov/optimade/jarvisdft/v1/structures",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: replaces Materials Project key path. "
            "data/jarvis_dft_open_panel_benchmark.json via open OPTIMADE (auth=none)."
        ),
    },
    {
        "id": "lmfdb_math",
        "family": "math_formal_compute",
        "title": "LMFDB / OEIS open mathematical databases",
        "open_url": "https://www.lmfdb.org/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: LMFDB quadratic fields API + OEIS sequences. "
            "data/lmfdb_oeis_math_open_benchmark.json"
        ),
    },
    {
        "id": "exoplanet_spectra",
        "family": "physics_particle_cosmo",
        "title": "NASA Exoplanet Archive open TAP / spectra products",
        "open_url": "https://exoplanetarchive.ipac.caltech.edu/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: pscomppars TAP depth (radius, mass, period, Teq, host stars). "
            "data/exoplanet_archive_depth_open_benchmark.json"
        ),
    },
    # --- Frontier wave 1 (FSOT residual only; auth=none) ---
    {
        "id": "pdg_live_depth",
        "family": "physics_particle_cosmo",
        "title": "PDG Review particle anchors (open literature depth)",
        "open_url": "https://pdg.lbl.gov/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/pdg_live_depth_open_benchmark.json",
    },
    {
        "id": "gaia_source_sample",
        "family": "physics_particle_cosmo",
        "title": "Gaia DR3 public TAP source sample",
        "open_url": "https://gea.esac.esa.int/tap-server/tap",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/gaia_dr3_source_sample_open_benchmark.json",
    },
    {
        "id": "simbad_identity_depth",
        "family": "physics_particle_cosmo",
        "title": "SIMBAD public TAP identity depth",
        "open_url": "https://simbad.cds.unistra.fr/simbad/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/simbad_identity_depth_open_benchmark.json",
    },
    {
        "id": "lmfdb_elliptic_curves",
        "family": "math_formal_compute",
        "title": "LMFDB elliptic curves open API",
        "open_url": "https://www.lmfdb.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/lmfdb_elliptic_curves_open_benchmark.json",
    },
    {
        "id": "gwas_catalog_depth",
        "family": "biology_life",
        "title": "EBI GWAS Catalog open REST depth",
        "open_url": "https://www.ebi.ac.uk/gwas/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/gwas_catalog_depth_open_benchmark.json",
    },
    {
        "id": "pubchem_assay_depth",
        "family": "chemistry_materials",
        "title": "PubChem multi-CID open property depth",
        "open_url": "https://pubchem.ncbi.nlm.nih.gov/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only (no formula_mass path). data/pubchem_depth_open_benchmark.json",
    },
    {
        "id": "openalex_citation_depth",
        "family": "open_science_meta",
        "title": "OpenAlex scholarly citation depth",
        "open_url": "https://api.openalex.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/openalex_citation_depth_open_benchmark.json",
    },
    # --- Frontier wave 2 (FSOT residual only) ---
    {
        "id": "uniprot_proteome_slice",
        "family": "biology_life",
        "title": "UniProt open REST proteome slice",
        "open_url": "https://rest.uniprot.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/uniprot_proteome_slice_open_benchmark.json",
    },
    {
        "id": "alphafold_batch_meta",
        "family": "biology_life",
        "title": "AlphaFold DB public prediction metadata",
        "open_url": "https://alphafold.ebi.ac.uk/api/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/alphafold_batch_meta_open_benchmark.json",
    },
    {
        "id": "rcsb_structure_batch",
        "family": "chemistry_materials",
        "title": "RCSB PDB structure batch (open REST)",
        "open_url": "https://data.rcsb.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/rcsb_structure_batch_open_benchmark.json",
    },
    {
        "id": "oeis_family_sweep",
        "family": "math_formal_compute",
        "title": "OEIS sequence family sweep",
        "open_url": "https://oeis.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/oeis_family_sweep_open_benchmark.json",
    },
    {
        "id": "usgs_seismic_history",
        "family": "earth_climate",
        "title": "USGS FDSN seismic catalog (M≥6 history)",
        "open_url": "https://earthquake.usgs.gov/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/usgs_seismic_history_open_benchmark.json",
    },
    {
        "id": "noaa_tides_multi_station",
        "family": "earth_climate",
        "title": "NOAA CO-OPS multi-station water levels",
        "open_url": "https://api.tidesandcurrents.noaa.gov/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/noaa_tides_multi_station_open_benchmark.json",
    },
    {
        "id": "gbif_taxon_depth",
        "family": "biology_life",
        "title": "GBIF occurrence / taxon depth",
        "open_url": "https://api.gbif.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/gbif_taxon_depth_open_benchmark.json",
    },
    {
        "id": "zenodo_records_depth",
        "family": "open_science_meta",
        "title": "Zenodo open research records depth",
        "open_url": "https://zenodo.org/api/records",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/zenodo_records_depth_open_benchmark.json",
    },
    # --- Frontier wave 3 ---
    {
        "id": "endf_reaction_subset",
        "family": "physics_particle_cosmo",
        "title": "IAEA Live Chart levels/gammas (ENDF-class open nuclear)",
        "open_url": "https://www-nds.iaea.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/endf_iaea_nuclear_open_benchmark.json",
    },
    {
        "id": "nist_asd_multi_species",
        "family": "physics_particle_cosmo",
        "title": "NIST multi-species spectroscopic line anchors",
        "open_url": "https://physics.nist.gov/PhysRefData/ASD/lines_form.html",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/nist_asd_multi_species_open_benchmark.json",
    },
    {
        "id": "desi_edr_table_slice",
        "family": "physics_particle_cosmo",
        "title": "DESI public portal + open BAO literature slice",
        "open_url": "https://data.desi.lbl.gov/public/",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: portal + BAO anchors + FITS residual attach. "
            "data/desi_edr_table_slice_open_benchmark.json · "
            "data/desi_edr_fits_residual_benchmark.json "
            "(zall-pix-fuji.fits on external multi-drive root)."
        ),
    },
    {
        "id": "desi_edr_fits_residual",
        "family": "physics_particle_cosmo",
        "title": "DESI EDR zall FITS residual (ZWARN=0 sample)",
        "open_url": "https://data.desi.lbl.gov/public/edr/spectro/redux/fuji/zcatalog/zall-pix-fuji.fits",
        "auth": "none",
        "status": "covered",
        "note": (
            "Covered: FSOT residual on redshift/flux/chi2 from local public FITS. "
            "scripts/build_desi_fits_residual_panel.py → data/desi_edr_fits_residual_benchmark.json"
        ),
    },
    {
        "id": "gwosc_strain_metadata",
        "family": "physics_particle_cosmo",
        "title": "GWOSC open strain archive JSON metadata",
        "open_url": "https://gwosc.org/",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/gwosc_strain_metadata_open_benchmark.json",
    },
    {
        "id": "codata_full_table",
        "family": "physics_particle_cosmo",
        "title": "NIST CODATA complete constants residual sweep",
        "open_url": "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
        "auth": "none",
        "status": "covered",
        "note": "Covered: FSOT residual only. data/codata_full_table_open_benchmark.json",
    },
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _family(domain: str, file_name: str) -> str:
    blob = f"{domain} {file_name}"
    for name, pat in FAMILY_PATTERNS:
        if pat.search(blob):
            return name
    return "other"


def _pin_prefix() -> str:
    path = ROOT / "vendor" / "fsot_compute.py"
    if not path.exists():
        return "unknown"
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest().upper()[:6]


def _ingest_engine_math(cur: sqlite3.Cursor) -> dict[str, Any]:
    """Load seeds, derived constants, formula branches, all domain interfaces, edges."""
    stats: dict[str, Any] = {
        "seeds": 0,
        "derived": 0,
        "branches": 0,
        "interfaces": 0,
        "edges": 0,
        "source": None,
    }
    if not MATH_AUDIT.exists():
        # Soft-generate if missing
        try:
            import subprocess

            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build_fsot_system_math_audit.py")],
                cwd=str(ROOT),
                check=False,
                timeout=300,
            )
        except Exception:
            pass
    if not MATH_AUDIT.exists():
        stats["source"] = "missing"
        return stats

    audit = json.loads(MATH_AUDIT.read_text(encoding="utf-8"))
    stats["source"] = "data/fsot_system_math_audit.json"

    for n in (audit.get("seeds") or {}).get("nodes") or []:
        cur.execute(
            "INSERT OR REPLACE INTO engine_seeds(id, symbol, value, role, code) VALUES (?,?,?,?,?)",
            (n.get("id"), n.get("symbol"), n.get("value"), n.get("role"), n.get("code")),
        )
        stats["seeds"] += 1

    for layer_key, layer_num in (
        ("layer1_primary_derived", 1),
        ("layer2_composite_derived", 2),
    ):
        for n in (audit.get(layer_key) or {}).get("nodes") or []:
            cur.execute(
                "INSERT OR REPLACE INTO engine_derived(id, layer, formula, value, role, section) "
                "VALUES (?,?,?,?,?,?)",
                (
                    n.get("id"),
                    layer_num,
                    n.get("formula"),
                    n.get("value"),
                    n.get("role"),
                    n.get("section"),
                ),
            )
            stats["derived"] += 1

    for b in (audit.get("formula_branches") or {}).get("branches") or []:
        cur.execute(
            "INSERT OR REPLACE INTO formula_branches(id, name, role, structure_json, fluid_note) "
            "VALUES (?,?,?,?,?)",
            (
                b.get("id"),
                b.get("name"),
                b.get("role"),
                json.dumps(b.get("structure") or b.get("depends") or []),
                b.get("fluid_note"),
            ),
        )
        stats["branches"] += 1

    for d in audit.get("domains") or []:
        cur.execute(
            """
            INSERT OR REPLACE INTO domain_interfaces(
              domain, kind, d_eff, hits, delta_psi, observed, s_scalar, sign, band,
              domain_factor_f, pure_residual_floor_pct, routes_to_core
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                d.get("domain"),
                d.get("kind"),
                d.get("D_eff"),
                d.get("hits"),
                d.get("delta_psi"),
                1 if d.get("observed") else 0,
                d.get("S"),
                d.get("sign"),
                d.get("band"),
                d.get("domain_factor_f"),
                d.get("pure_residual_floor_pct"),
                d.get("routes_to_core"),
            ),
        )
        stats["interfaces"] += 1

    # Connective edges from hierarchy + network (cap size for SQLite)
    edges: list[tuple[str, str, str, float]] = []
    if HIERARCHY.exists():
        hier = json.loads(HIERARCHY.read_text(encoding="utf-8"))
        for e in hier.get("edges") or []:
            edges.append(
                (
                    str(e.get("from") or ""),
                    str(e.get("to") or ""),
                    str(e.get("rel") or "hier"),
                    1.0,
                )
            )
    if NETWORK.exists():
        net = json.loads(NETWORK.read_text(encoding="utf-8"))
        for e in net.get("domain_domain_links") or []:
            edges.append(
                (
                    str(e.get("source") or ""),
                    str(e.get("target") or ""),
                    str(e.get("kind") or "network"),
                    float(e.get("weight") or 1.0),
                )
            )
        # seed strings: store unique seed→domain as compact sample if huge
        for e in (net.get("seed_domain_links") or [])[:2500]:
            edges.append(
                (
                    str(e.get("source") or ""),
                    str(e.get("target") or ""),
                    "seed_domain",
                    1.0,
                )
            )

    # Dedup lightly
    seen: set[tuple[str, str, str]] = set()
    batch = []
    for src, dst, rel, w in edges:
        if not src or not dst:
            continue
        key = (src, dst, rel)
        if key in seen:
            continue
        seen.add(key)
        batch.append((src, dst, rel, w))
        if len(batch) >= 5000:
            cur.executemany(
                "INSERT INTO connective_edges(src, dst, rel, weight) VALUES (?,?,?,?)",
                batch,
            )
            stats["edges"] += len(batch)
            batch = []
    if batch:
        cur.executemany(
            "INSERT INTO connective_edges(src, dst, rel, weight) VALUES (?,?,?,?)",
            batch,
        )
        stats["edges"] += len(batch)

    cur.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        ("engine_math_interfaces", str(stats["interfaces"])),
    )
    cur.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        ("engine_math_edges", str(stats["edges"])),
    )
    cur.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        ("master_formula", "S = K * (T1 + T2 + T3); c = m * (1 + |S| * f)"),
    )
    return stats


def _load_margin_domains() -> list[dict[str, Any]]:
    if not MARGIN.exists():
        return []
    doc = json.loads(MARGIN.read_text(encoding="utf-8"))
    return [r for r in (doc.get("all_domains") or []) if isinstance(r, dict) and not r.get("excluded")]


def _resolve_bench_path(file_field: str) -> Path | None:
    if not file_field:
        return None
    candidates = [
        ROOT / "data" / file_field,
        ROOT / file_field,
        ROOT / "data" / Path(file_field).name,
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def _material_rows(doc: dict) -> list[dict]:
    mat = doc.get("material_records")
    if isinstance(mat, list) and mat:
        return [r for r in mat if isinstance(r, dict)]
    recs = doc.get("records")
    if isinstance(recs, list):
        return [r for r in recs if isinstance(r, dict) and r.get("computed") is not None]
    return []


def build() -> dict[str, Any]:
    if OUT_DB.exists():
        OUT_DB.unlink()

    conn = sqlite3.connect(str(OUT_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE meta (
          key TEXT PRIMARY KEY,
          value TEXT
        );
        CREATE TABLE domains (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          domain TEXT NOT NULL,
          file_name TEXT,
          family TEXT,
          green_gate_pass INTEGER,
          pooled_median_error_pct REAL,
          max_scalar_error_pct REAL,
          scalar_count INTEGER,
          record_count INTEGER,
          records_stored INTEGER,
          records_sampled INTEGER,
          full_json_path TEXT,
          maps_to_lean TEXT,
          d_eff INTEGER,
          lean_module TEXT
        );
        CREATE INDEX idx_domains_domain ON domains(domain);
        CREATE INDEX idx_domains_family ON domains(family);
        CREATE INDEX idx_domains_green ON domains(green_gate_pass);

        CREATE TABLE records (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          domain_id INTEGER NOT NULL,
          lab TEXT,
          property TEXT,
          name TEXT,
          computed REAL,
          measured REAL,
          error_pct REAL,
          eval_kind TEXT,
          formula TEXT,
          FOREIGN KEY(domain_id) REFERENCES domains(id)
        );
        CREATE INDEX idx_records_domain ON records(domain_id);
        CREATE INDEX idx_records_property ON records(property);
        CREATE INDEX idx_records_error ON records(error_pct);

        CREATE TABLE formulas (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          formula TEXT UNIQUE,
          use_count INTEGER,
          example_domain TEXT
        );

        CREATE TABLE citations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          kind TEXT,
          title TEXT,
          url TEXT,
          panel_count INTEGER,
          note TEXT
        );

        CREATE TABLE open_sources (
          id TEXT PRIMARY KEY,
          family TEXT,
          url TEXT,
          description TEXT,
          auth TEXT,
          notes TEXT
        );

        CREATE TABLE high_value_gaps (
          id TEXT PRIMARY KEY,
          family TEXT,
          title TEXT,
          open_url TEXT,
          auth TEXT,
          status TEXT,
          note TEXT
        );

        CREATE VIRTUAL TABLE fts_domains USING fts5(
          domain, file_name, family, content='domains', content_rowid='id'
        );

        -- Engine math (from system audit / fsot_compute) — full formula fabric
        CREATE TABLE engine_seeds (
          id TEXT PRIMARY KEY,
          symbol TEXT,
          value REAL,
          role TEXT,
          code TEXT
        );
        CREATE TABLE engine_derived (
          id TEXT PRIMARY KEY,
          layer INTEGER,
          formula TEXT,
          value REAL,
          role TEXT,
          section TEXT
        );
        CREATE TABLE formula_branches (
          id TEXT PRIMARY KEY,
          name TEXT,
          role TEXT,
          structure_json TEXT,
          fluid_note TEXT
        );
        CREATE TABLE domain_interfaces (
          domain TEXT PRIMARY KEY,
          kind TEXT,
          d_eff INTEGER,
          hits INTEGER,
          delta_psi REAL,
          observed INTEGER,
          s_scalar REAL,
          sign TEXT,
          band TEXT,
          domain_factor_f REAL,
          pure_residual_floor_pct REAL,
          routes_to_core TEXT
        );
        CREATE INDEX idx_interfaces_deff ON domain_interfaces(d_eff);
        CREATE INDEX idx_interfaces_sign ON domain_interfaces(sign);
        CREATE TABLE connective_edges (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          src TEXT,
          dst TEXT,
          rel TEXT,
          weight REAL
        );
        CREATE INDEX idx_edges_src ON connective_edges(src);
        CREATE INDEX idx_edges_dst ON connective_edges(dst);
        """
    )

    pin = _pin_prefix()
    domains = _load_margin_domains()
    green_n = sum(1 for d in domains if d.get("green_gate_pass"))

    meta = {
        "generated_at": _now(),
        "pin_prefix": pin,
        "green_domains": str(green_n),
        "margin_domains": str(len(domains)),
        "policy": "open_science_only_no_credentials",
        "authority": "vendor/fsot_compute.py + green JSON benchmarks",
        "large_record_threshold": str(LARGE_RECORD_THRESHOLD),
    }
    cur.executemany("INSERT INTO meta(key, value) VALUES (?, ?)", list(meta.items()))

    formula_counts: dict[str, dict[str, Any]] = {}
    total_records_seen = 0
    total_records_stored = 0
    sampled_domains = 0
    missing_files = 0

    insert_rec = (
        "INSERT INTO records(domain_id, lab, property, name, computed, measured, error_pct, eval_kind, formula) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )

    for row in domains:
        domain = str(row.get("domain") or Path(str(row.get("file") or "unknown")).stem)
        file_name = str(row.get("file") or "")
        family = _family(domain, file_name)
        path = _resolve_bench_path(file_name)
        full_json = None
        maps = None
        d_eff = None
        lean = None
        rec_count = row.get("scalar_count")
        mat: list[dict] = []
        sampled = 0

        if path is not None:
            full_json = str(path.relative_to(ROOT)).replace("\\", "/")
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                doc = {}
                missing_files += 1
            mat = _material_rows(doc)
            rec_count = int(doc.get("record_count") or doc.get("observable_count") or len(mat) or rec_count or 0)
            maps = json.dumps(doc.get("maps_to_lean") or [])
            d_eff = doc.get("D_eff")
            lean = doc.get("lean_module")
        else:
            missing_files += 1

        store = mat
        if len(mat) > LARGE_RECORD_THRESHOLD:
            store = mat[:LARGE_SAMPLE_N]
            sampled = 1
            sampled_domains += 1
        total_records_seen += len(mat)
        total_records_stored += len(store)

        cur.execute(
            """
            INSERT INTO domains(
              domain, file_name, family, green_gate_pass, pooled_median_error_pct,
              max_scalar_error_pct, scalar_count, record_count, records_stored,
              records_sampled, full_json_path, maps_to_lean, d_eff, lean_module
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                domain,
                file_name,
                family,
                1 if row.get("green_gate_pass") else 0,
                row.get("pooled_median_error_pct"),
                row.get("max_scalar_error_pct"),
                row.get("scalar_count"),
                rec_count,
                len(store),
                sampled,
                full_json,
                maps,
                d_eff,
                lean,
            ),
        )
        domain_id = cur.lastrowid

        batch: list[tuple] = []
        for r in store:
            formula = r.get("formula")
            if formula:
                fkey = str(formula)
                if fkey not in formula_counts:
                    formula_counts[fkey] = {"use_count": 0, "example_domain": domain}
                formula_counts[fkey]["use_count"] += 1
            def _f(x: Any) -> float | None:
                if x is None:
                    return None
                try:
                    return float(x)
                except (TypeError, ValueError):
                    return None

            batch.append(
                (
                    domain_id,
                    r.get("lab"),
                    r.get("property"),
                    r.get("name"),
                    _f(r.get("computed")),
                    _f(r.get("measured")),
                    _f(r.get("error_pct")),
                    r.get("eval_kind"),
                    str(formula) if formula is not None else None,
                )
            )
        if batch:
            cur.executemany(insert_rec, batch)

    for formula, meta_f in formula_counts.items():
        cur.execute(
            "INSERT INTO formulas(formula, use_count, example_domain) VALUES (?, ?, ?)",
            (formula, meta_f["use_count"], meta_f["example_domain"]),
        )

    # Citations
    cit_n = 0
    if CITATION_LEDGER.exists():
        ledger = json.loads(CITATION_LEDGER.read_text(encoding="utf-8"))
        for a in ledger.get("global_anchors") or []:
            if not isinstance(a, dict):
                continue
            if a.get("kind") in ("process",):
                continue
            cur.execute(
                "INSERT INTO citations(kind, title, url, panel_count, note) VALUES (?, ?, ?, ?, ?)",
                (
                    a.get("kind"),
                    a.get("title"),
                    a.get("url"),
                    len(a.get("panels") or []),
                    a.get("note"),
                ),
            )
            cit_n += 1

    # Open sources (no-key)
    open_n = 0
    try:
        from open_science_sources_lib import OPEN_SOURCES  # noqa: E402

        for s in OPEN_SOURCES:
            cur.execute(
                "INSERT OR REPLACE INTO open_sources(id, family, url, description, auth, notes) VALUES (?,?,?,?,?,?)",
                (s.id, s.family, s.url, s.description, s.auth, s.notes),
            )
            open_n += 1
    except Exception:
        pass

    if API_REQ.exists() and yaml is not None:
        api = yaml.safe_load(API_REQ.read_text(encoding="utf-8")) or {}
        for family, block in (api.get("api_sources") or {}).items():
            for src in block.get("sources") or []:
                if not isinstance(src, dict):
                    continue
                auth = str(src.get("auth") or "none").lower()
                if auth not in ("none", "optional", ""):
                    continue
                sid = str(src.get("id") or "")
                if not sid:
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO open_sources(id, family, url, description, auth, notes) VALUES (?,?,?,?,?,?)",
                    (
                        sid,
                        family,
                        str(src.get("url") or ""),
                        str(block.get("description") or sid),
                        "none",
                        str(src.get("note") or ""),
                    ),
                )
                open_n += 1

    for g in HIGH_VALUE_GAPS:
        cur.execute(
            "INSERT INTO high_value_gaps(id, family, title, open_url, auth, status, note) VALUES (?,?,?,?,?,?,?)",
            (g["id"], g["family"], g["title"], g["open_url"], g["auth"], g["status"], g["note"]),
        )

    # FTS
    cur.execute(
        "INSERT INTO fts_domains(rowid, domain, file_name, family) "
        "SELECT id, domain, file_name, family FROM domains"
    )

    # Engine math + domain interfaces + connective edges (full formula fabric)
    math_stats = _ingest_engine_math(cur)

    conn.commit()

    # Stats
    cur.execute("SELECT family, COUNT(*) FROM domains GROUP BY family ORDER BY COUNT(*) DESC")
    by_family = {k: v for k, v in cur.fetchall()}
    cur.execute("SELECT COUNT(*) FROM records")
    n_rec = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM formulas")
    n_form = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM high_value_gaps WHERE status IN ('gap','partial')")
    n_gaps = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM high_value_gaps WHERE status LIKE 'skipped%'")
    n_skip = cur.fetchone()[0]
    conn.close()

    report = {
        "generated_at": meta["generated_at"],
        "db_path": str(OUT_DB.relative_to(ROOT)).replace("\\", "/"),
        "pin_prefix": pin,
        "domains": len(domains),
        "green_domains": green_n,
        "records_seen_in_json": total_records_seen,
        "records_stored": total_records_stored,
        "records_table_count": n_rec,
        "formulas": n_form,
        "citations": cit_n,
        "open_sources": open_n,
        "high_value_gaps_open": n_gaps,
        "high_value_gaps_skipped_credentials": n_skip,
        "sampled_large_domains": sampled_domains,
        "missing_benchmark_files": missing_files,
        "by_family": by_family,
        "engine_math": math_stats,
        "policy": "open_science_only_no_credentials",
        "query": "python scripts/query_fsot_atlas.py --stats",
        "reality_os": "python scripts/run_fsot_reality_os.py",
    }
    OUT_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    report = build()
    print(f"Wrote {OUT_DB}")
    print(f"Wrote {OUT_REPORT}")
    print(
        f"  domains={report['domains']} green={report['green_domains']} "
        f"records_stored={report['records_stored']} formulas={report['formulas']} "
        f"open_sources={report['open_sources']} gaps_open={report['high_value_gaps_open']} "
        f"skipped_cred={report['high_value_gaps_skipped_credentials']}"
    )
    print(f"  by_family={report['by_family']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
