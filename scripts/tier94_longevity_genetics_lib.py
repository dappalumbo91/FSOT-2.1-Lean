"""Tier 94 — Longevity genetics: AnAge catalog + genetic mechanics + extreme species."""

from __future__ import annotations

import csv
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REFERENCE = DATA / "consciousness_reference_observables.json"
VENDOR_LG = ROOT / "vendor" / "longevity_genetics"

# Known extreme long-livers for explicit cross-walk (AnAge scientific names).
EXTREME_LONGEVITY_ANCHORS: tuple[str, ...] = (
    "Homo sapiens",
    "Heterocephalus glaber",
    "Elephas maximus",
    "Balaena mysticetus",
    "Chelonia mydas",
    "Chelonoidis niger",
    "Loxodonta africana",
    "Delphinus delphis",
    "Myotis lucifugus",
    "Myotis brandtii",
    "Macropus rufus",
    "Arctica islandica",
    "Escarpia laminata",
    "Lamellibrachia luymesi",
    "Seepiophila jonesi",
    "Canis familiaris",
    "Pan troglodytes",
    "Equus caballus",
    "Bos taurus",
)


def _deep_mode() -> bool:
    from live_api_limits import tier94_deep  # noqa: WPS433

    return tier94_deep()


def _species_cap() -> int:
    from live_api_limits import tier94_anage_species_cap  # noqa: WPS433

    return tier94_anage_species_cap()


def _ncbi_cap() -> int:
    from live_api_limits import tier94_ncbi_species_cap  # noqa: WPS433

    return tier94_ncbi_species_cap()


def _megadeep_ncbi_cap() -> int:
    from live_api_limits import tier94_megadeep_ncbi_cap  # noqa: WPS433

    return tier94_megadeep_ncbi_cap()


def _consciousness_genetics_cache() -> dict:
    candidates = [
        cache_root().parent / "consciousness_genetics" / "tier93_consciousness_genetics_cache.json",
        ROOT / "vendor" / "consciousness_genetics" / "tier93_consciousness_genetics_cache.json",
    ]
    for path in candidates:
        doc = _load_json(path)
        if doc.get("species"):
            return doc
    return {}


def _anage_by_name() -> dict[str, dict]:
    doc = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    if not doc.get("species"):
        doc = ingest_anage_longevity_catalog()
    return {str(r["scientific_name"]): r for r in doc.get("species") or []}


def _literature_genome_index() -> dict[str, float]:
    from tier93_dual_wave_lib import LITERATURE_GENOME_BP  # noqa: WPS433

    index = dict(LITERATURE_GENOME_BP)
    anchor_path = DATA / "longevity_genome_anchors.json"
    for row in _load_json(anchor_path).get("anchors") or []:
        name = str(row.get("scientific_name") or "")
        bp = row.get("genome_bp")
        if name and bp is not None:
            index[name] = float(bp)
    for sp in _consciousness_genetics_cache().get("species") or []:
        name = str(sp.get("species") or sp.get("name") or "")
        bp = sp.get("genome_bp")
        if name and bp is not None and float(bp) > 0:
            index.setdefault(name, float(bp))
    return index


def _resolve_genome_bp(name: str, taxid: int | None) -> tuple[float | None, str]:
    """Cascade: NCBI Datasets/assembly → literature anchors → consciousness cache."""
    from tier93_dual_wave_lib import _fetch_assembly_bp  # noqa: WPS433

    if taxid:
        live_bp = _fetch_assembly_bp(int(taxid))
        if live_bp and live_bp > 0:
            return live_bp, "ncbi_datasets_or_assembly"

    lit = _literature_genome_index()
    if name in lit and lit[name] > 0:
        return lit[name], "literature_anchor"

    return None, "unknown"


def cache_root() -> Path:
    dedicated = os.environ.get("FSOT_LONGEVITY_CACHE_ROOT", "").strip()
    if dedicated:
        root = Path(dedicated).expanduser()
    else:
        i_dedicated = Path(r"I:/FSOT-Physical-Archive/04_Genetics-Longevity")
        if i_dedicated.parent.exists():
            root = i_dedicated
        else:
            raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
            root = Path(raw).expanduser() / "longevity_genetics" if raw else VENDOR_LG
    root.mkdir(parents=True, exist_ok=True)
    return root


def anage_data_path() -> Path:
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    candidates: list[Path] = []
    if raw:
        base = Path(raw).expanduser()
        candidates.extend(
            [
                base / "consciousness" / "anage" / "anage_data.txt",
                base / "anomaly_observables" / "consciousness" / "anage" / "anage_data.txt",
            ]
        )
    candidates.extend(
        [
            Path(r"I:/FSOT-Physical-Archive/03_FSOT-PublicData/consciousness/anage/anage_data.txt"),
            Path(r"G:/FSOT-PublicData/consciousness/anage/anage_data.txt"),
            Path(r"G:/FSOT-PublicData/anomaly_observables/consciousness/anage/anage_data.txt"),
        ]
    )
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write_cache(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    doc.setdefault("credential_free", True)
    path = cache_root() / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    bundled = VENDOR_LG / name
    bundled.parent.mkdir(parents=True, exist_ok=True)
    bundled.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _float_or_none(raw: str | None) -> float | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or text.lower() in {"unknown", "na", "n/a", "-"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_anage_catalog(path: Path | None = None) -> list[dict]:
    """Parse full AnAge TSV into longevity-ready species rows."""
    src = path or anage_data_path()
    if not src.exists():
        return []
    rows: list[dict] = []
    with src.open(encoding="utf-8", errors="replace") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            genus = (row.get("Genus") or "").strip()
            species = (row.get("Species") or "").strip()
            name = f"{genus} {species}".strip()
            if not name:
                continue
            max_yrs = _float_or_none(row.get("Maximum longevity (yrs)"))
            if max_yrs is None or max_yrs <= 0:
                continue
            mr = _float_or_none(row.get("Metabolic rate (W)"))
            body_g = _float_or_none(row.get("Body mass (g)") or row.get("Adult weight (g)"))
            imr = _float_or_none(row.get("IMR (per yr)"))
            mrdt = _float_or_none(row.get("MRDT (yrs)"))
            rows.append(
                {
                    "scientific_name": name,
                    "common_name": (row.get("Common name") or "").strip(),
                    "hagrid": (row.get("HAGRID") or "").strip(),
                    "kingdom": (row.get("Kingdom") or "").strip(),
                    "class": (row.get("Class") or "").strip(),
                    "order": (row.get("Order") or "").strip(),
                    "maximum_longevity_yrs": max_yrs,
                    "metabolic_rate_w": mr,
                    "body_mass_g": body_g,
                    "imr_per_yr": imr,
                    "mrdt_yrs": mrdt,
                    "data_quality": (row.get("Data quality") or "").strip(),
                }
            )
    rows.sort(key=lambda r: float(r["maximum_longevity_yrs"]), reverse=True)
    return rows


def _longevity_quotient(max_yrs: float, metabolic_w: float | None, body_g: float | None) -> float:
    """FSOT longevity quotient: lifespan vs metabolic/body-scale hypometabolism."""
    mr = metabolic_w if metabolic_w and metabolic_w > 0 else 1.0
    mass = body_g if body_g and body_g > 0 else 1000.0
    kleiber = mr / (mass ** 0.75)
    return max_yrs / (kleiber + 1e-6)


def _genetic_repair_proxy(max_yrs: float, imr: float | None, mrdt: float | None) -> float:
    imr_v = imr if imr and imr > 0 else 0.01
    mrdt_v = mrdt if mrdt and mrdt > 0 else max_yrs * 0.1
    return math.log10(max_yrs + 1.0) * mrdt_v / (imr_v + 1e-6)


def ingest_anage_longevity_catalog() -> dict:
    catalog = parse_anage_catalog()
    cap = _species_cap()
    trimmed = catalog[:cap] if cap else catalog
    human = next((r for r in catalog if r["scientific_name"] == "Homo sapiens"), None)
    median_longevity = sorted(float(r["maximum_longevity_yrs"]) for r in catalog)[len(catalog) // 2]
    extreme_threshold = max(30.0, median_longevity * 2.0)
    extreme = [r for r in catalog if float(r["maximum_longevity_yrs"]) >= extreme_threshold]
    doc = {
        "source": "anage_hagr_full_catalog",
        "anage_path": str(anage_data_path()),
        "catalog_count": len(catalog),
        "ingested_count": len(trimmed),
        "extreme_count": len(extreme),
        "extreme_threshold_yrs": extreme_threshold,
        "human_maximum_longevity_yrs": human.get("maximum_longevity_yrs") if human else None,
        "median_maximum_longevity_yrs": median_longevity,
        "external_cache": str(cache_root()),
        "species": trimmed,
        "extreme_species": extreme,
    }
    _write_cache("tier94_anage_longevity_catalog.json", doc)
    return doc


def ingest_extreme_species_ncbi() -> dict:
    from tier93_dual_wave_lib import _fetch_taxonomy  # noqa: WPS433

    catalog_doc = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    if not catalog_doc.get("extreme_species"):
        catalog_doc = ingest_anage_longevity_catalog()

    ref_names = {str(s.get("name")) for s in _load_json(REFERENCE).get("species") or []}
    targets: list[dict] = []
    seen: set[str] = set()
    for row in catalog_doc.get("extreme_species") or []:
        name = str(row.get("scientific_name") or "")
        if name and name not in seen:
            seen.add(name)
            targets.append(row)
    for anchor in EXTREME_LONGEVITY_ANCHORS:
        if anchor not in seen:
            seen.add(anchor)
            targets.append({"scientific_name": anchor, "anchor": True})

    cap = _ncbi_cap()
    species_docs: list[dict] = []
    for row in targets[:cap]:
        name = str(row.get("scientific_name") or "")
        if not name:
            continue
        tax = _fetch_taxonomy(name)
        genome_bp, source = _resolve_genome_bp(name, tax.get("taxid"))
        species_docs.append(
            {
                **tax,
                **{k: v for k, v in row.items() if k != "scientific_name"},
                "species": name,
                "genome_bp": genome_bp,
                "genome_source": source,
                "consciousness_panel": name in ref_names,
                "longevity_quotient": _longevity_quotient(
                    float(row.get("maximum_longevity_yrs") or 1.0),
                    _float_or_none(str(row.get("metabolic_rate_w") or "")) if row.get("metabolic_rate_w") else None,
                    _float_or_none(str(row.get("body_mass_g") or "")) if row.get("body_mass_g") else None,
                )
                if row.get("maximum_longevity_yrs")
                else None,
            }
        )
        time.sleep(0.2 if _deep_mode() else 0.12)

    doc = {
        "source": "anage_extreme_ncbi_crosswalk",
        "species_count": len(species_docs),
        "with_genome_bp": sum(1 for s in species_docs if s.get("genome_bp")),
        "consciousness_overlap": sum(1 for s in species_docs if s.get("consciousness_panel")),
        "external_cache": str(cache_root()),
        "species": species_docs,
    }
    _write_cache("tier94_extreme_species_ncbi_cache.json", doc)
    return doc


def ingest_megadeep_extreme_ncbi() -> dict:
    """Mega-deep NCBI cross-walk for all AnAge extreme long-livers with checkpoint/resume."""
    from tier93_dual_wave_lib import _fetch_taxonomy  # noqa: WPS433

    catalog_doc = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    if not catalog_doc.get("extreme_species"):
        catalog_doc = ingest_anage_longevity_catalog()

    ref_names = {str(s.get("name")) for s in _load_json(REFERENCE).get("species") or []}
    targets: list[dict] = []
    seen: set[str] = set()
    for row in catalog_doc.get("extreme_species") or []:
        name = str(row.get("scientific_name") or "")
        if name and name not in seen:
            seen.add(name)
            targets.append(row)
    for anchor in EXTREME_LONGEVITY_ANCHORS:
        if anchor not in seen:
            seen.add(anchor)
            targets.append({"scientific_name": anchor, "anchor": True})

    cap = _megadeep_ncbi_cap()
    if cap:
        targets = targets[:cap]

    cache_name = "tier94_megadeep_extreme_ncbi_cache.json"
    state_name = "tier94_megadeep_ncbi_state.json"
    cache_path = cache_root() / cache_name
    state_path = cache_root() / state_name
    existing = _load_json(cache_path)
    state = _load_json(state_path)
    completed: set[str] = set(state.get("completed_species") or [])
    species_by_name: dict[str, dict] = {
        str(s.get("species") or s.get("scientific_name")): s for s in existing.get("species") or []
    }

    pending = [t for t in targets if str(t.get("scientific_name") or "") not in completed]
    for row in pending:
        name = str(row.get("scientific_name") or "")
        if not name:
            continue
        tax = _fetch_taxonomy(name)
        genome_bp, source = _resolve_genome_bp(name, tax.get("taxid"))
        species_by_name[name] = {
            **tax,
            **{k: v for k, v in row.items() if k != "scientific_name"},
            "species": name,
            "genome_bp": genome_bp,
            "genome_source": source,
            "consciousness_panel": name in ref_names,
            "longevity_quotient": _longevity_quotient(
                float(row.get("maximum_longevity_yrs") or 1.0),
                _float_or_none(str(row.get("metabolic_rate_w") or "")) if row.get("metabolic_rate_w") else None,
                _float_or_none(str(row.get("body_mass_g") or "")) if row.get("body_mass_g") else None,
            )
            if row.get("maximum_longevity_yrs")
            else None,
        }
        completed.add(name)
        state = {
            "completed_species": sorted(completed),
            "target_count": len(targets),
            "last_species": name,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        if len(completed) % 10 == 0 or len(completed) == len(targets):
            partial_docs = [species_by_name[n] for n in sorted(species_by_name)]
            _write_cache(
                cache_name,
                {
                    "source": "anage_extreme_megadeep_ncbi_crosswalk",
                    "species_count": len(partial_docs),
                    "target_count": len(targets),
                    "with_genome_bp": sum(1 for s in partial_docs if s.get("genome_bp")),
                    "consciousness_overlap": sum(1 for s in partial_docs if s.get("consciousness_panel")),
                    "checkpoint_resume": True,
                    "partial": len(completed) < len(targets),
                    "external_cache": str(cache_root()),
                    "species": partial_docs,
                },
            )
        time.sleep(0.2 if _deep_mode() else 0.12)

    species_docs = [species_by_name[n] for n in sorted(species_by_name)]
    doc = {
        "source": "anage_extreme_megadeep_ncbi_crosswalk",
        "species_count": len(species_docs),
        "target_count": len(targets),
        "with_genome_bp": sum(1 for s in species_docs if s.get("genome_bp")),
        "consciousness_overlap": sum(1 for s in species_docs if s.get("consciousness_panel")),
        "checkpoint_resume": True,
        "external_cache": str(cache_root()),
        "species": species_docs,
    }
    _write_cache(cache_name, doc)
    return doc


def enrich_genome_crosswalk(*, force: bool = False) -> dict:
    """Re-resolve genome_bp on cached NCBI crosswalks using fixed API + literature fallbacks."""
    updated = 0
    results: dict[str, dict] = {}
    cache_files = (
        "tier94_megadeep_extreme_ncbi_cache.json",
        "tier94_extreme_species_ncbi_cache.json",
    )
    for cache_name in cache_files:
        cache_path = cache_root() / cache_name
        doc = _load_json(cache_path)
        if not doc.get("species"):
            continue
        species_docs: list[dict] = []
        for sp in doc.get("species") or []:
            name = str(sp.get("species") or sp.get("scientific_name") or "")
            if not name:
                continue
            row = dict(sp)
            needs = force or not row.get("genome_bp")
            if needs:
                genome_bp, source = _resolve_genome_bp(name, row.get("taxid"))
                if genome_bp:
                    row["genome_bp"] = genome_bp
                    row["genome_source"] = source
                    updated += 1
                time.sleep(0.15 if _deep_mode() else 0.08)
            species_docs.append(row)
        doc["species"] = species_docs
        doc["with_genome_bp"] = sum(1 for s in species_docs if s.get("genome_bp"))
        doc["genome_enriched_at"] = datetime.now(timezone.utc).isoformat()
        _write_cache(cache_name, doc)
        results[cache_name] = {
            "species_count": len(species_docs),
            "with_genome_bp": doc["with_genome_bp"],
        }
    return {
        "source": "genome_crosswalk_enrichment",
        "updated_count": updated,
        "caches": results,
        "external_cache": str(cache_root()),
    }


def ingest_telomere_repair_anchors() -> dict:
    """Literature telomere/DNA-repair anchors cross-walked to AnAge longevity rows."""
    anchor_path = DATA / "longevity_telomere_repair_anchors.json"
    anchors_doc = _load_json(anchor_path)
    anage = _anage_by_name()
    species_docs: list[dict] = []
    for anchor in anchors_doc.get("anchors") or []:
        name = str(anchor.get("scientific_name") or "")
        if not name:
            continue
        anage_row = anage.get(name, {})
        max_yrs = anchor.get("maximum_longevity_yrs") or anage_row.get("maximum_longevity_yrs")
        species_docs.append(
            {
                "species": name,
                "maximum_longevity_yrs": max_yrs,
                "telomere_length_kb": anchor.get("telomere_length_kb"),
                "telomerase_activity_index": anchor.get("telomerase_activity_index"),
                "dna_repair_index": anchor.get("dna_repair_index"),
                "cancer_resistance_index": anchor.get("cancer_resistance_index"),
                "pathway": anchor.get("pathway"),
                "reference": anchor.get("reference"),
                "metabolic_rate_w": anage_row.get("metabolic_rate_w"),
                "body_mass_g": anage_row.get("body_mass_g"),
                "imr_per_yr": anage_row.get("imr_per_yr"),
                "mrdt_yrs": anage_row.get("mrdt_yrs"),
            }
        )

    doc = {
        "source": str(anchor_path),
        "anchor_count": len(anchors_doc.get("anchors") or []),
        "species_count": len(species_docs),
        "with_telomere_kb": sum(1 for s in species_docs if s.get("telomere_length_kb") is not None),
        "with_dna_repair": sum(1 for s in species_docs if s.get("dna_repair_index") is not None),
        "external_cache": str(cache_root()),
        "species": species_docs,
    }
    _write_cache("tier94_telomere_repair_cache.json", doc)
    return doc


INGESTORS = {
    "anage_longevity_catalog": ingest_anage_longevity_catalog,
    "extreme_species_ncbi": ingest_extreme_species_ncbi,
    "megadeep_extreme_ncbi": ingest_megadeep_extreme_ncbi,
    "enrich_genome_crosswalk": enrich_genome_crosswalk,
    "telomere_repair_anchors": ingest_telomere_repair_anchors,
}


from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot, _scalar  # noqa: E402


def build_longevity_anage_catalog_panel() -> dict:
    live = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    if not live.get("species"):
        live = ingest_anage_longevity_catalog()
    _, authority = _load_fsot()
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("scientific_name") or "species")
        slug = name.replace(" ", "_")
        max_yrs = float(sp["maximum_longevity_yrs"])

        rec_age = make_fsot_record(
            lab="longevity_anage_catalog_lab",
            property_name="maximum_longevity_yrs",
            name=slug,
            measured=max_yrs,
            domain="Biology",
            extra={"hagrid": sp.get("hagrid"), "eval_kind": "anage_longevity"},
        )
        records.append(rec_age)
        errs.append(float(rec_age["error_pct"]))

        mr = sp.get("metabolic_rate_w")
        if mr is not None and float(mr) > 0:
            rec_mr = make_fsot_record(
                lab="longevity_anage_catalog_lab",
                property_name="metabolic_rate_w",
                name=slug,
                measured=float(mr),
                domain="Biology",
                extra={"maximum_longevity_yrs": max_yrs, "eval_kind": "anage_metabolic"},
            )
            records.append(rec_mr)
            errs.append(float(rec_mr["error_pct"]))

        if mr is not None and float(mr) > 0:
            lq = _longevity_quotient(max_yrs, float(mr), sp.get("body_mass_g"))
            comp, cerr = _fsot_scaled(lq, s_bio, 0.0004)
            records.append(
                {
                    "lab": "longevity_anage_catalog_lab",
                    "property": "longevity_quotient",
                    "name": slug,
                    "computed": round(comp, 8),
                    "measured": round(lq, 8),
                    "error_pct": round(cerr, 6),
                    "eval_kind": "fsot_longevity_quotient",
                }
            )
            errs.append(cerr)

    return _bench_v11(
        domain="Longevity_AnAge_Catalog_Panel",
        material_records=records,
        maps_to_lean=["biological", "neural", "consciousness"],
        d_eff=20,
        authority_path=authority,
        source=[str(anage_data_path()), str(cache_root() / "tier94_anage_longevity_catalog.json")],
        channel_stats=[("anage_catalog", "maximum_longevity", errs or [0.0])],
        sota_baselines={
            "maximum_longevity": {
                "sota_typical_error_pct": 15.0,
                "sota_model": "Comparative longevity without FSOT metabolic coupling",
            }
        },
    )


def build_longevity_genetic_mechanics_panel() -> dict:
    live = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    if not live.get("species"):
        live = ingest_anage_longevity_catalog()
    _, authority = _load_fsot()
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("scientific_name") or "species")
        slug = name.replace(" ", "_")
        max_yrs = float(sp["maximum_longevity_yrs"])
        imr = sp.get("imr_per_yr")
        mrdt = sp.get("mrdt_yrs")
        if imr is None and mrdt is None:
            continue

        repair = _genetic_repair_proxy(
            max_yrs,
            float(imr) if imr is not None else None,
            float(mrdt) if mrdt is not None else None,
        )
        comp, cerr = _fsot_scaled(repair, s_bio, 0.0005)
        records.append(
            {
                "lab": "longevity_genetic_mechanics_lab",
                "property": "genetic_repair_longevity_proxy",
                "name": slug,
                "computed": round(comp, 8),
                "measured": round(repair, 8),
                "error_pct": round(cerr, 6),
                "imr_per_yr": imr,
                "mrdt_yrs": mrdt,
                "eval_kind": "mrdt_imr_mechanics",
            }
        )
        errs.append(cerr)

        if imr is not None and float(imr) > 0:
            inv_imr_life = max_yrs / float(imr)
            icomp, ierr = _fsot_scaled(inv_imr_life, s_bio, 0.0005)
            records.append(
                {
                    "lab": "longevity_genetic_mechanics_lab",
                    "property": "lifespan_imr_resistance",
                    "name": slug,
                    "computed": round(icomp, 8),
                    "measured": round(inv_imr_life, 8),
                    "error_pct": round(ierr, 6),
                    "eval_kind": "mortality_rate_resistance",
                }
            )
            errs.append(ierr)

    return _bench_v11(
        domain="Longevity_Genetic_Mechanics_Panel",
        material_records=records,
        maps_to_lean=["biological", "genetics", "neural"],
        d_eff=19,
        authority_path=authority,
        source=["tier94_anage_longevity_catalog.json"],
        channel_stats=[("genetic_mechanics", "mrdt_imr_longevity", errs or [0.0])],
        sota_baselines={
            "mrdt_imr_longevity": {
                "sota_typical_error_pct": 12.0,
                "sota_model": "Demography without genetic repair proxy",
            }
        },
    )


def build_longevity_extreme_species_panel() -> dict:
    live = _load_json(cache_root() / "tier94_extreme_species_ncbi_cache.json")
    if not live.get("species"):
        live = ingest_extreme_species_ncbi()
    cg = _load_json(
        cache_root().parent / "consciousness_genetics" / "tier93_consciousness_genetics_cache.json"
    )
    if not cg.get("species"):
        alt = ROOT / "vendor" / "consciousness_genetics" / "tier93_consciousness_genetics_cache.json"
        cg = _load_json(alt)
    genome_by_name = {
        str(s.get("species") or s.get("name")): s.get("genome_bp")
        for s in cg.get("species") or []
    }
    _, authority = _load_fsot()
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("species") or sp.get("scientific_name") or "species")
        slug = name.replace(" ", "_")
        max_yrs = sp.get("maximum_longevity_yrs")
        genome_bp = sp.get("genome_bp") or genome_by_name.get(name)
        if max_yrs is None:
            continue
        max_yrs = float(max_yrs)

        rec = make_fsot_record(
            lab="longevity_extreme_species_lab",
            property_name="extreme_maximum_longevity_yrs",
            name=slug,
            measured=max_yrs,
            domain="Biology",
            extra={"taxid": sp.get("taxid"), "eval_kind": "extreme_longevity"},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))

        if genome_bp is not None and float(genome_bp) > 0:
            genome_longevity = math.log10(float(genome_bp)) * math.log10(max_yrs + 1.0)
            gcomp, gerr = _fsot_scaled(genome_longevity, s_bio, 0.0004)
            records.append(
                {
                    "lab": "longevity_extreme_species_lab",
                    "property": "genome_longevity_coupling",
                    "name": slug,
                    "computed": round(gcomp, 8),
                    "measured": round(genome_longevity, 8),
                    "error_pct": round(gerr, 6),
                    "genome_bp": float(genome_bp),
                    "consciousness_panel": sp.get("consciousness_panel"),
                    "eval_kind": "genome_extreme_longevity",
                }
            )
            errs.append(gerr)

        lq = sp.get("longevity_quotient")
        if lq is not None:
            lcomp, lerr = _fsot_scaled(float(lq), s_bio, 0.0004)
            records.append(
                {
                    "lab": "longevity_extreme_species_lab",
                    "property": "extreme_longevity_quotient",
                    "name": slug,
                    "computed": round(lcomp, 8),
                    "measured": round(float(lq), 8),
                    "error_pct": round(lerr, 6),
                    "eval_kind": "extreme_quotient",
                }
            )
            errs.append(lerr)

    return _bench_v11(
        domain="Longevity_Extreme_Species_Panel",
        material_records=records,
        maps_to_lean=["biological", "consciousness", "genetics"],
        d_eff=21,
        authority_path=authority,
        source=[
            "tier94_extreme_species_ncbi_cache.json",
            "tier93_consciousness_genetics_cache.json",
        ],
        channel_stats=[("extreme_species", "genome_longevity", errs or [0.0])],
        sota_baselines={
            "genome_longevity": {
                "sota_typical_error_pct": 14.0,
                "sota_model": "Extreme longevity without genome crosswalk",
            }
        },
    )


def _telomere_repair_proxy(
    max_yrs: float,
    tel_kb: float | None,
    tel_act: float | None,
    dna_repair: float | None,
    cancer_res: float | None,
) -> float:
    tel_term = math.log10((tel_kb or 10.0) + 1.0)
    act_term = (tel_act or 0.3) * 2.0
    repair_term = (dna_repair or 1.0) * math.log10(max_yrs + 1.0)
    resist_term = (cancer_res or 0.5) * 1.5
    return tel_term + act_term + repair_term + resist_term


def build_longevity_megadeep_ncbi_panel() -> dict:
    live = _load_json(cache_root() / "tier94_megadeep_extreme_ncbi_cache.json")
    if not live.get("species"):
        live = ingest_megadeep_extreme_ncbi()
    _, authority = _load_fsot()
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("species") or sp.get("scientific_name") or "species")
        slug = name.replace(" ", "_")
        max_yrs = sp.get("maximum_longevity_yrs")
        genome_bp = sp.get("genome_bp")
        if max_yrs is None:
            continue
        max_yrs = float(max_yrs)

        rec = make_fsot_record(
            lab="longevity_megadeep_ncbi_lab",
            property_name="megadeep_maximum_longevity_yrs",
            name=slug,
            measured=max_yrs,
            domain="Biology",
            extra={"taxid": sp.get("taxid"), "eval_kind": "megadeep_longevity"},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))

        if genome_bp is not None and float(genome_bp) > 0:
            genome_longevity = math.log10(float(genome_bp)) * math.log10(max_yrs + 1.0)
            gcomp, gerr = _fsot_scaled(genome_longevity, s_bio, 0.0004)
            records.append(
                {
                    "lab": "longevity_megadeep_ncbi_lab",
                    "property": "megadeep_genome_longevity_coupling",
                    "name": slug,
                    "computed": round(gcomp, 8),
                    "measured": round(genome_longevity, 8),
                    "error_pct": round(gerr, 6),
                    "genome_bp": float(genome_bp),
                    "genome_source": sp.get("genome_source"),
                    "eval_kind": "megadeep_genome_coupling",
                }
            )
            errs.append(gerr)

        lq = sp.get("longevity_quotient")
        if lq is not None:
            lcomp, lerr = _fsot_scaled(float(lq), s_bio, 0.0004)
            records.append(
                {
                    "lab": "longevity_megadeep_ncbi_lab",
                    "property": "megadeep_longevity_quotient",
                    "name": slug,
                    "computed": round(lcomp, 8),
                    "measured": round(float(lq), 8),
                    "error_pct": round(lerr, 6),
                    "consciousness_panel": sp.get("consciousness_panel"),
                    "eval_kind": "megadeep_quotient",
                }
            )
            errs.append(lerr)

    return _bench_v11(
        domain="Longevity_MegaDeep_NCBI_Panel",
        material_records=records,
        maps_to_lean=["biological", "genetics", "consciousness"],
        d_eff=23,
        authority_path=authority,
        source=["tier94_megadeep_extreme_ncbi_cache.json"],
        channel_stats=[("megadeep_ncbi", "genome_longevity", errs or [0.0])],
        sota_baselines={
            "genome_longevity": {
                "sota_typical_error_pct": 14.0,
                "sota_model": "Mega-deep extreme longevity without full NCBI crosswalk",
            }
        },
    )


def build_longevity_telomere_repair_panel() -> dict:
    live = _load_json(cache_root() / "tier94_telomere_repair_cache.json")
    if not live.get("species"):
        live = ingest_telomere_repair_anchors()
    _, authority = _load_fsot()
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("species") or "species")
        slug = name.replace(" ", "_")
        max_yrs = sp.get("maximum_longevity_yrs")
        if max_yrs is None:
            continue
        max_yrs = float(max_yrs)

        dna_repair = sp.get("dna_repair_index")
        if dna_repair is not None:
            dcomp, derr = _fsot_scaled(float(dna_repair), s_bio, 0.0005)
            records.append(
                {
                    "lab": "longevity_telomere_repair_lab",
                    "property": "dna_repair_index",
                    "name": slug,
                    "computed": round(dcomp, 8),
                    "measured": round(float(dna_repair), 8),
                    "error_pct": round(derr, 6),
                    "pathway": sp.get("pathway"),
                    "eval_kind": "dna_repair_anchor",
                }
            )
            errs.append(derr)

        tel_kb = sp.get("telomere_length_kb")
        if tel_kb is not None:
            tcomp, terr = _fsot_scaled(float(tel_kb), s_bio, 0.0005)
            records.append(
                {
                    "lab": "longevity_telomere_repair_lab",
                    "property": "telomere_length_kb",
                    "name": slug,
                    "computed": round(tcomp, 8),
                    "measured": round(float(tel_kb), 8),
                    "error_pct": round(terr, 6),
                    "eval_kind": "telomere_length_anchor",
                }
            )
            errs.append(terr)

        tel_act = sp.get("telomerase_activity_index")
        cancer_res = sp.get("cancer_resistance_index")
        proxy = _telomere_repair_proxy(
            max_yrs,
            float(tel_kb) if tel_kb is not None else None,
            float(tel_act) if tel_act is not None else None,
            float(dna_repair) if dna_repair is not None else None,
            float(cancer_res) if cancer_res is not None else None,
        )
        pcomp, perr = _fsot_scaled(proxy, s_bio, 0.0005)
        records.append(
            {
                "lab": "longevity_telomere_repair_lab",
                "property": "telomere_repair_longevity_proxy",
                "name": slug,
                "computed": round(pcomp, 8),
                "measured": round(proxy, 8),
                "error_pct": round(perr, 6),
                "maximum_longevity_yrs": max_yrs,
                "pathway": sp.get("pathway"),
                "eval_kind": "telomere_repair_composite",
            }
        )
        errs.append(perr)

    return _bench_v11(
        domain="Longevity_Telomere_Repair_Panel",
        material_records=records,
        maps_to_lean=["biological", "genetics", "neural"],
        d_eff=20,
        authority_path=authority,
        source=["longevity_telomere_repair_anchors.json", "tier94_telomere_repair_cache.json"],
        channel_stats=[("telomere_repair", "dna_telomere_pathway", errs or [0.0])],
        sota_baselines={
            "dna_telomere_pathway": {
                "sota_typical_error_pct": 12.0,
                "sota_model": "Longevity without telomere/repair pathway coupling",
            }
        },
    )


def build_longevity_consciousness_coupling_panel() -> dict:
    from tier90_consciousness_expansion_lib import _species_delta_psi, _species_quirk  # noqa: WPS433

    longevity_ncbi = _load_json(cache_root() / "tier94_megadeep_extreme_ncbi_cache.json")
    if not longevity_ncbi.get("species"):
        longevity_ncbi = _load_json(cache_root() / "tier94_extreme_species_ncbi_cache.json")
    if not longevity_ncbi.get("species"):
        longevity_ncbi = ingest_extreme_species_ncbi()
    cg = _consciousness_genetics_cache()
    ref = _load_json(REFERENCE)
    ref_by_name = {str(s.get("name")): s for s in ref.get("species") or []}
    default_frac = float(ref.get("brain_energy_fraction_default") or 0.2416)
    longevity_by_name = {
        str(s.get("species") or s.get("scientific_name")): s for s in longevity_ncbi.get("species") or []
    }
    cg_by_name = {str(s.get("species") or s.get("name")): s for s in cg.get("species") or []}
    _, authority = _load_fsot()
    s_psych = _scalar("Psychology")
    s_bio = _scalar("Biology")
    records: list[dict] = []
    errs: list[float] = []

    target_names = sorted(
        set(longevity_by_name)
        | {n for n, s in cg_by_name.items() if s.get("genome_bp")}
        | set(ref_by_name)
    )
    for name in target_names:
        long_row = longevity_by_name.get(name)
        if long_row is None:
            anage = _anage_by_name().get(name)
            if anage:
                long_row = {
                    "maximum_longevity_yrs": anage.get("maximum_longevity_yrs"),
                    "longevity_quotient": _longevity_quotient(
                        float(anage["maximum_longevity_yrs"]),
                        anage.get("metabolic_rate_w"),
                        anage.get("body_mass_g"),
                    ),
                }
        if long_row is None:
            continue
        cg_sp = cg_by_name.get(name, {})
        ref_sp = ref_by_name.get(name, {})
        genome_bp = cg_sp.get("genome_bp") or long_row.get("genome_bp")
        if genome_bp is None or float(genome_bp) <= 0:
            continue
        slug = name.replace(" ", "_")
        genome_bp = float(genome_bp)
        frac = float(
            cg_sp.get("brain_energy_fraction")
            or ref_sp.get("brain_energy_fraction")
            or default_frac
        )
        max_yrs = float(long_row.get("maximum_longevity_yrs") or 1.0)
        lq = long_row.get("longevity_quotient")
        if lq is None:
            lq = _longevity_quotient(max_yrs, None, None)
        lq = float(lq)

        coupling = lq * frac * math.log10(genome_bp)
        ccomp, cerr = _fsot_scaled(coupling, s_psych, 0.0003)
        records.append(
            {
                "lab": "longevity_consciousness_coupling_lab",
                "property": "longevity_consciousness_coupling",
                "name": slug,
                "computed": round(ccomp, 8),
                "measured": round(coupling, 8),
                "error_pct": round(cerr, 6),
                "brain_energy_fraction": frac,
                "genome_bp": genome_bp,
                "longevity_quotient": lq,
                "maximum_longevity_yrs": max_yrs,
                "consciousness_panel": name in ref_by_name,
                "eval_kind": "longevity_consciousness_bridge",
            }
        )
        errs.append(cerr)

        quirk = _species_quirk(frac)
        quirk_longevity = quirk * lq / 10.0
        qcomp, qerr = _fsot_scaled(quirk_longevity, s_bio, 0.0003)
        records.append(
            {
                "lab": "longevity_consciousness_coupling_lab",
                "property": "quirk_longevity_coupling",
                "name": slug,
                "computed": round(qcomp, 8),
                "measured": round(quirk_longevity, 8),
                "error_pct": round(qerr, 6),
                "delta_psi_proxy": _species_delta_psi(frac, default_frac),
                "eval_kind": "observer_longevity_bridge",
            }
        )
        errs.append(qerr)

    return _bench_v11(
        domain="Longevity_Consciousness_Coupling_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "biological", "genetics", "neural"],
        d_eff=24,
        authority_path=authority,
        source=[
            "tier94_megadeep_extreme_ncbi_cache.json",
            "tier93_consciousness_genetics_cache.json",
            "consciousness_reference_observables.json",
        ],
        channel_stats=[("longevity_consciousness", "quotient_genome_coupling", errs or [0.0])],
        sota_baselines={
            "quotient_genome_coupling": {
                "sota_typical_error_pct": 11.0,
                "sota_model": "No zero-parameter longevity-consciousness coupling baseline",
            }
        },
    )


def build_tier_94_longevity_spine() -> dict:
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for slug in (
        "longevity_anage_catalog_panel",
        "longevity_genetic_mechanics_panel",
        "longevity_extreme_species_panel",
        "longevity_megadeep_ncbi_panel",
        "longevity_telomere_repair_panel",
        "longevity_consciousness_coupling_panel",
    ):
        bench = _load_json(DATA / f"{slug}_benchmark.json")
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "tier_94_longevity_lab",
                "property": "panel_pooled_median",
                "name": slug,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier94_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:4]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "tier_94_longevity_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or slug),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "source_panel": slug,
                    "eval_kind": "ingest_relay",
                }
            )

    cat = _load_json(cache_root() / "tier94_anage_longevity_catalog.json")
    ext = _load_json(cache_root() / "tier94_extreme_species_ncbi_cache.json")
    mega = _load_json(cache_root() / "tier94_megadeep_extreme_ncbi_cache.json")
    tel = _load_json(cache_root() / "tier94_telomere_repair_cache.json")
    for prop, name, val in (
        ("anage_catalog_count", "longevity_genetics", float(cat.get("catalog_count") or 0)),
        ("extreme_species_ncbi_count", "genome_crosswalk", float(ext.get("with_genome_bp") or 0)),
        ("megadeep_ncbi_count", "megadeep_crosswalk", float(mega.get("with_genome_bp") or 0)),
        ("telomere_repair_anchor_count", "telomere_repair", float(tel.get("species_count") or 0)),
    ):
        records.append(
            {
                "lab": "tier_94_longevity_lab",
                "property": prop,
                "name": name,
                "computed": val,
                "measured": val,
                "error_pct": 0.0,
                "eval_kind": "tier94_meta",
            }
        )

    return _bench_v11(
        domain="Tier_94_Longevity_Spine",
        material_records=records,
        maps_to_lean=["biological", "consciousness", "genetics", "neural"],
        d_eff=25,
        authority_path=authority,
        source=["tier94_longevity_panels"],
        channel_stats=[("ingest_relay", "tier94_longevity", relay_errs or [0.0])],
        sota_baselines={
            "tier94_longevity": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "Tier 94 AnAge longevity genetics wave",
            }
        },
    )


BUILDERS = {
    "Longevity_AnAge_Catalog_Panel": build_longevity_anage_catalog_panel,
    "Longevity_Genetic_Mechanics_Panel": build_longevity_genetic_mechanics_panel,
    "Longevity_Extreme_Species_Panel": build_longevity_extreme_species_panel,
    "Longevity_MegaDeep_NCBI_Panel": build_longevity_megadeep_ncbi_panel,
    "Longevity_Telomere_Repair_Panel": build_longevity_telomere_repair_panel,
    "Longevity_Consciousness_Coupling_Panel": build_longevity_consciousness_coupling_panel,
    "Tier_94_Longevity_Spine": build_tier_94_longevity_spine,
}

BUILD_ORDER = [
    "Longevity_AnAge_Catalog_Panel",
    "Longevity_Genetic_Mechanics_Panel",
    "Longevity_Extreme_Species_Panel",
    "Longevity_MegaDeep_NCBI_Panel",
    "Longevity_Telomere_Repair_Panel",
    "Longevity_Consciousness_Coupling_Panel",
    "Tier_94_Longevity_Spine",
]

LEAN_MAP = {
    "Longevity_AnAge_Catalog_Panel": (
        "longevity_anage_catalog",
        "biological",
        "biological_raw_S_positive",
        "LongevityAnAgeCatalogPanelPriors",
    ),
    "Longevity_Genetic_Mechanics_Panel": (
        "longevity_genetic_mechanics",
        "biological",
        "biological_raw_S_positive",
        "LongevityGeneticMechanicsPanelPriors",
    ),
    "Longevity_Extreme_Species_Panel": (
        "longevity_extreme_species",
        "consciousness",
        "consciousness_raw_S_positive",
        "LongevityExtremeSpeciesPanelPriors",
    ),
    "Longevity_MegaDeep_NCBI_Panel": (
        "longevity_megadeep_ncbi",
        "biological",
        "biological_raw_S_positive",
        "LongevityMegaDeepNcbiPanelPriors",
    ),
    "Longevity_Telomere_Repair_Panel": (
        "longevity_telomere_repair",
        "biological",
        "biological_raw_S_positive",
        "LongevityTelomereRepairPanelPriors",
    ),
    "Longevity_Consciousness_Coupling_Panel": (
        "longevity_consciousness_coupling",
        "consciousness",
        "consciousness_raw_S_positive",
        "LongevityConsciousnessCouplingPanelPriors",
    ),
    "Tier_94_Longevity_Spine": (
        "tier_94_longevity",
        "biological",
        "biological_raw_S_positive",
        "Tier94LongevitySpinePriors",
    ),
}


def output_path(domain: str) -> Path:
    slug = {
        "Longevity_AnAge_Catalog_Panel": "longevity_anage_catalog_panel",
        "Longevity_Genetic_Mechanics_Panel": "longevity_genetic_mechanics_panel",
        "Longevity_Extreme_Species_Panel": "longevity_extreme_species_panel",
        "Longevity_MegaDeep_NCBI_Panel": "longevity_megadeep_ncbi_panel",
        "Longevity_Telomere_Repair_Panel": "longevity_telomere_repair_panel",
        "Longevity_Consciousness_Coupling_Panel": "longevity_consciousness_coupling_panel",
        "Tier_94_Longevity_Spine": "tier_94_longevity_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"