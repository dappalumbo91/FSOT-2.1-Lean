#!/usr/bin/env python3
"""Ingest zebrafish reference anchors from leading public data resources."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from live_api_fetch_lib import fetch_json  # noqa: E402
from tier95_zebrahub_development_lib import SPECIES, ZEBRAFISH_GENOME_BP, _longevity_zebrafish  # noqa: E402

OUT = ROOT / "data" / "tier95_zebrafish_reference_anchors.json"
VENDOR_OUT = ROOT / "vendor" / "zebrahub_development" / "tier95_zebrafish_reference_anchors.json"

# Literature CV bands for 3D cell-tracking lineage observables (CTC / light-sheet practice).
MECHANISTIC_LITERATURE_ANCHORS: dict[str, dict] = {
    "division_rate": {
        "literature_cv_pct": 15.0,
        "reference_uncertainty_pct": 15.0,
        "unit": "dimensionless",
        "reference": "Ultrack/Zebrahub lineage assignment; CTC-style division-link uncertainty (~10–20% CV)",
        "source": "zebrahub_czbiohub + cell_tracking_challenge_literature",
    },
    "mean_track_duration_steps": {
        "literature_cv_pct": 12.0,
        "reference_uncertainty_pct": 12.0,
        "unit": "imaging_frames",
        "reference": "3D track fragmentation / gap-closing uncertainty in developmental light-sheet imaging",
        "source": "keller_2008_scanned_light_sheet + ultrack_methods",
    },
    "mean_displacement_um": {
        "literature_cv_pct": 8.0,
        "reference_uncertainty_pct": 8.0,
        "unit": "micrometers",
        "reference": "Voxel calibration (±2–5%) + segmentation boundary variability in mesoscale motility",
        "source": "zebrahub_ome_zarr_metadata + developmental_imaging_metrology",
    },
    "developmental_stability_proxy": {
        "literature_cv_pct": 18.0,
        "reference_uncertainty_pct": 18.0,
        "unit": "dimensionless",
        "reference": "Derived stability index — propagates division + duration uncertainties",
        "source": "fsot_developmental_stability_definition",
    },
}


def _fetch_ensembl() -> dict:
    doc = fetch_json("https://rest.ensembl.org/info/genomes/danio_rerio?content-type=application/json")
    return {
        "source": "ensembl_rest",
        "url": "https://rest.ensembl.org/info/genomes/danio_rerio",
        "scientific_name": SPECIES,
        "assembly_name": doc.get("assembly_name"),
        "assembly_id": doc.get("assembly_id"),
        "genebuild": doc.get("genebuild"),
        "division": doc.get("division"),
    }


def _fetch_gbif() -> dict:
    doc = fetch_json("https://api.gbif.org/v1/species/match?name=Danio%20rerio")
    return {
        "source": "gbif_species_match",
        "url": "https://api.gbif.org/v1/species/match?name=Danio%20rerio",
        "usage_key": doc.get("usageKey"),
        "scientific_name": doc.get("scientificName"),
        "rank": doc.get("rank"),
        "kingdom": doc.get("kingdom"),
        "phylum": doc.get("phylum"),
        "class": doc.get("class"),
        "order": doc.get("order"),
        "family": doc.get("family"),
    }


def _fetch_uniprot_taxonomy() -> dict:
    doc = fetch_json("https://rest.uniprot.org/taxonomy/7955")
    return {
        "source": "uniprot_taxonomy",
        "url": "https://rest.uniprot.org/taxonomy/7955",
        "taxon_id": doc.get("taxonId"),
        "scientific_name": doc.get("scientificName"),
        "rank": doc.get("rank"),
        "lineage": doc.get("lineage"),
    }


def _species_longevity_anchor() -> dict:
    sp = _longevity_zebrafish()
    return {
        "source": "anage_hagr_tier94",
        "scientific_name": sp.get("scientific_name") or SPECIES,
        "maximum_longevity_yrs": float(sp.get("maximum_longevity_yrs") or 5.5),
        "metabolic_rate_w": float(sp.get("metabolic_rate_w") or 0.35),
        "body_mass_g": sp.get("body_mass_g"),
        "reference": "AnAge / HAGR longevity catalog (Tier 94 ingest)",
    }


def ingest_zebrafish_reference_anchors(*, live: bool = True) -> dict:
    errors: list[str] = []
    ensembl = gbif = uniprot = None

    if live:
        for name, fn in (
            ("ensembl", _fetch_ensembl),
            ("gbif", _fetch_gbif),
            ("uniprot", _fetch_uniprot_taxonomy),
        ):
            try:
                if name == "ensembl":
                    ensembl = fn()
                elif name == "gbif":
                    gbif = fn()
                else:
                    uniprot = fn()
            except Exception as exc:
                errors.append(f"{name}: {exc}")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "species": SPECIES,
        "credential_free": True,
        "genome_bp_anchor": {
            "measured": ZEBRAFISH_GENOME_BP,
            "unit": "base_pairs",
            "reference": "GRCz11 reference assembly (Ensembl/NCBI consensus ~1.37 Gbp)",
            "source": "ensembl_grcz11_consensus",
            "reference_uncertainty_pct": 0.5,
        },
        "longevity_anchor": _species_longevity_anchor(),
        "mechanistic_property_anchors": MECHANISTIC_LITERATURE_ANCHORS,
        "live_resources": {
            "ensembl": ensembl,
            "gbif": gbif,
            "uniprot_taxonomy": uniprot,
        },
        "ingest_errors": errors,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    VENDOR_OUT.parent.mkdir(parents=True, exist_ok=True)
    VENDOR_OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


def load_zebrafish_reference_anchors() -> dict:
    for path in (OUT, VENDOR_OUT):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return ingest_zebrafish_reference_anchors(live=True)


def anchor_for_property(property_name: str) -> dict:
    doc = load_zebrafish_reference_anchors()
    return dict((doc.get("mechanistic_property_anchors") or {}).get(property_name) or {})


def main() -> int:
    doc = ingest_zebrafish_reference_anchors(live=True)
    print(f"Wrote {OUT}")
    print(f"species={doc['species']} genome_bp={doc['genome_bp_anchor']['measured']:.3e}")
    live = doc.get("live_resources") or {}
    if live.get("ensembl"):
        print(f"ensembl assembly={live['ensembl'].get('assembly_name')}")
    if live.get("gbif"):
        print(f"gbif usage_key={live['gbif'].get('usage_key')}")
    if doc.get("ingest_errors"):
        print("errors:", doc["ingest_errors"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())