#!/usr/bin/env python3
"""Turn a local drive path into a repo path or a public citation.

No returned field contains a drive letter. Checksums below were hashed from
the local files on 2026-10-02. This module does not read those drives.
"""
from __future__ import annotations

import re

from check_internal_links import path_exists, tracked_index

HOST = "https://github.com/dappalumbo91/FSOT-2.1-Lean/tree/main/"
REPO_ROOTS = (
    "C:/Users/damia/Desktop/FSOT-2.1-Lean/",
    "I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full/",
)
REMAP = {
    "data/preregistered_predictions_manifest.yaml": (
        "predictions/preregistered_predictions_manifest.yaml"
    ),
}
BY_NAME = {
    "warp_actuation_formula_fsot21.json": (
        "vendor/verified_desktop/legacy_physics/warp_actuation_formula_fsot21.json"
    ),
    "tier94_anage_longevity_catalog.json": (
        "vendor/longevity_genetics/tier94_anage_longevity_catalog.json"
    ),
}
IN_REPO_NOTE = (
    "In-repo path. Rebuild notes stay in ingest scripts and data/api_requirements.yaml."
)
SPECIAL_NOTES = {
    "vendor/verified_desktop/legacy_physics/warp_actuation_formula_fsot21.json": (
        "In-repo copy of the legacy-physics warp actuation formula. "
        "SHA-256 97cd202b77da9915f537437e7274328f65e4395541a2d1b1d4d36da889213513."
    ),
    "vendor/longevity_genetics/tier94_anage_longevity_catalog.json": (
        "In-repo AnAge longevity catalog. SHA-256 "
        "a33ee5e95d8af532cc744bb7ff889e3a4cfcdcad6948a7f74f6f6d2685258d94. "
        "Source: Human Ageing Genomic Resources AnAge. Download "
        "https://genomics.senescence.info/species/dataset.zip and unzip anage_data.txt. "
        "Ingested anage_data.txt SHA-256 "
        "98867969fbd4d0bed6bab415c2715bb19079dbd7f92bdc26e5961856aa1c1519."
    ),
    "vendor/trinary_os": (
        "In-repo trinary OS tree. A separate local public-data directory is not "
        "published, and no extra checksum is recorded for it."
    ),
    "data/consciousness_reference_observables.json": (
        "In-repo species reference used by the consciousness species panel."
    ),
    "data/consciousness_resonance_reference.json": (
        "In-repo microtubule resonance reference. The observer cache that pointed "
        "here is not tracked. Local cache SHA-256 "
        "308d76f3f0fc73a0c52243294d7f8fbaf33ce2c11a07bab46ea7941dc2fc4282. "
        "No public DOI or upstream checksum is recorded for that cache."
    ),
}

# Full forward-slash tokens that are not a tracked file under a repo root.
EXPLICIT: dict[str, dict[str, str]] = {
    "G:/FSOT-PublicData/the_well/the_well_catalog_cache.json": {
        "kind": "dataset",
        "title": "The Well catalog (Polymathic AI)",
        "url": "https://arxiv.org/abs/2412.00568",
        "note": (
            "Local catalog cache is not tracked. Ohana et al., arXiv:2412.00568. "
            "Download the code and data from https://github.com/PolymathicAI/the_well "
            "(about 15 TB; streaming via hf://datasets/polymathic-ai/). "
            "Hugging Face collection: https://huggingface.co/collections/polymathic-ai/the-well. "
            "Local aggregate-stats cache SHA-256 "
            "f3abed951c0c479823b162411d3591551143f89f058a7a7ba6254a75b555c5dc. "
            "Upstream dataset checksums are not copied here."
        ),
    },
    "G:/FSOT-PublicData/the_well/the_well_spot_checks_cache.json": {
        "kind": "dataset",
        "title": "The Well spot-check scalars",
        "url": "https://github.com/PolymathicAI/the_well",
        "note": (
            "Local spot-check cache is not tracked. Same release as The Well, "
            "arXiv:2412.00568. Download from https://github.com/PolymathicAI/the_well. "
            "Local cache SHA-256 "
            "5eb63c8aebe3a31515f6f7745c2654543ef6ac6023ccb061c281564d8cc858d8."
        ),
    },
    "G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_microtubule_observer_cache.json": {
        "kind": "dataset",
        "title": "Microtubule observer cache (not tracked)",
        "url": HOST + "data/consciousness_resonance_reference.json",
        "note": SPECIAL_NOTES["data/consciousness_resonance_reference.json"],
    },
    "G:/FSOT-PublicData/anomaly_observables/consciousness/tier90_species_panel_cache.json": {
        "kind": "dataset",
        "title": "AnAge consciousness species panel",
        "url": "https://genomics.senescence.info/species/dataset.zip",
        "note": (
            "Human Ageing Genomic Resources AnAge. Download dataset.zip and unzip "
            "anage_data.txt. Ingested anage_data.txt SHA-256 "
            "98867969fbd4d0bed6bab415c2715bb19079dbd7f92bdc26e5961856aa1c1519. "
            "In-repo species reference: data/consciousness_reference_observables.json. "
            "Local species-panel cache is not tracked. SHA-256 "
            "052a681f41c5bcabe963cc93faeeeb21494a06b7f006891d4a94f2fa7bca9de9."
        ),
    },
    "G:/FSOT-PublicData/anomaly_observables/consciousness/anage": {
        "kind": "dataset",
        "title": "AnAge species dataset",
        "url": "https://genomics.senescence.info/species/dataset.zip",
        "note": (
            "Human Ageing Genomic Resources AnAge. Download dataset.zip and unzip "
            "anage_data.txt. Ingested anage_data.txt SHA-256 "
            "98867969fbd4d0bed6bab415c2715bb19079dbd7f92bdc26e5961856aa1c1519."
        ),
    },
    "I:/FSOT-Physical-Archive/03_FSOT-PublicData/consciousness/anage/anage_data.txt": {
        "kind": "dataset",
        "title": "AnAge anage_data.txt",
        "url": "https://genomics.senescence.info/species/dataset.zip",
        "note": (
            "Human Ageing Genomic Resources AnAge. Download dataset.zip and unzip "
            "anage_data.txt. Ingested file SHA-256 "
            "98867969fbd4d0bed6bab415c2715bb19079dbd7f92bdc26e5961856aa1c1519."
        ),
    },
    "G:/FSOT-PublicData/anomaly_observables/sh0es": {
        "kind": "dataset",
        "title": "Pantheon+SH0ES DataRelease",
        "url": "https://github.com/PantheonPlusSH0ES/DataRelease",
        "note": (
            "Clone https://github.com/PantheonPlusSH0ES/DataRelease. "
            "The file list used here is in data/anomaly_observables_manifest.yaml "
            "under sh0es_ceph. No single release checksum is recorded in this repository."
        ),
    },
    "G:/FSOT-PublicData/fringe_desktop/symbolic_encoding/fsot_mythology_graph.json": {
        "kind": "unresolved",
        "title": "FSOT mythology graph (not tracked)",
        "note": (
            "fsot_mythology_graph.json is not in this repository. No public URL, DOI, "
            "or upstream checksum is recorded. Local file SHA-256 "
            "2741a3298cd320473c1b843e41d00d0cd1408b39375e4d531eb944f8500d55ce."
        ),
    },
    "G:/FSOT-PublicData/trinary_os": {
        "kind": "vendor_cache",
        "title": "vendor/trinary_os",
        "url": HOST + "vendor/trinary_os",
        "note": SPECIAL_NOTES["vendor/trinary_os"],
    },
    "I:/FSOT-Physical-Archive/08_Verified-Desktop-Projects/star_trek_transporter/pattern_buffer_scan_results.json": {
        "kind": "unresolved",
        "title": "Pattern-buffer scan results (not tracked)",
        "note": (
            "pattern_buffer_scan_results.json is a local simulator scan and is not "
            "in this repository. No public URL or DOI is recorded. Local file SHA-256 "
            "645fcb2a21817ef7ac8c8cf6bfbe749ceb8feb7f3a0edf110e00647aa7bbcc8c."
        ),
    },
    "I:/FSOT-Physical-Archive/08_Verified-Desktop-Projects/fuel_lab/engine_simulator/REAL_DATA_PROVENANCE.md": {
        "kind": "dataset",
        "title": "Fuel-lab engine simulator provenance",
        "url": "https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest",
        "note": (
            "The provenance note is not in this repository. It records PubChem PUG REST "
            "for compound properties, with a NIST property lookup when PubChem has no "
            "result. Local note SHA-256 "
            "3497c80ed65e6bfe79c01565a6aa66b9b6fe49d9026ae1549584b3db2ea3b95c."
        ),
    },
    "I:/Protofluid-Language-Translator-2.0-Zig": {
        "kind": "url",
        "title": "Protofluid Language Translator 2.0 (Zig)",
        "url": "https://github.com/dappalumbo91/Protofluid-Language-Translator-2.0-Zig",
        "note": (
            "Public repository. Clone that URL. No release checksum is recorded here."
        ),
    },
    "I:/fsot-neuron-zig": {
        "kind": "url",
        "title": "fsot-neuron-zig",
        "url": "https://github.com/dappalumbo91/fsot-neuron-zig",
        "note": (
            "Public repository. Clone that URL. No release checksum is recorded here."
        ),
    },
    "I:/FSOT-Physical-Archive/02_FSOT-2.1-Lean-Full": {
        "kind": "url",
        "title": "FSOT-2.1-Lean",
        "url": "https://github.com/dappalumbo91/FSOT-2.1-Lean",
        "note": "Clone the public repository. Do not use a local archive path.",
    },
    "C:/Users/damia/Desktop/fsot code language": {
        "kind": "unresolved",
        "title": "fsot code language (not tracked)",
        "note": (
            "Named as a local desktop code-language tree. It is not in this "
            "repository. No public URL, DOI, or checksum is recorded."
        ),
    },
    "C:/Users/damia/Desktop/gpu exparment for lean coq isabell andf star": {
        "kind": "unresolved",
        "title": "GPU experiment for Lean, Coq, Isabelle, and Star (not tracked)",
        "note": (
            "Named as a local desktop GPU experiment. It is not in this repository. "
            "No public URL, DOI, or checksum is recorded."
        ),
    },
}

_DRIVE_START = re.compile(r"^[A-Za-z]:[/\\]")
_HUB_DRIVE = re.compile(
    r"https://github\.com/dappalumbo91/FSOT-2\.1-Lean/(?:blob|tree)/[^/]+/([A-Za-z]:/.+)$",
    re.IGNORECASE,
)


def _norm(token: str) -> str:
    return token.strip().replace("\\", "/").rstrip("/")


def _repo_record(rel: str) -> dict[str, str]:
    note = SPECIAL_NOTES.get(rel, IN_REPO_NOTE)
    return {
        "kind": "vendor_cache",
        "title": rel,
        "url": HOST + rel,
        "note": note,
    }


def cite_local_path(token: str) -> dict[str, str] | None:
    """Citation for a drive path or a hub URL that embeds one. None if neither."""
    raw = token.strip()
    hub = _HUB_DRIVE.search(raw.replace("\\", "/"))
    if hub:
        key = _norm(hub.group(1))
    elif _DRIVE_START.match(raw):
        key = _norm(raw)
    else:
        return None
    explicit = EXPLICIT.get(key)
    if explicit is not None:
        return dict(explicit)
    files, _by_name = tracked_index()
    rel = None
    for root in REPO_ROOTS:
        if key.startswith(root):
            rel = REMAP.get(key[len(root) :], key[len(root) :])
            break
    if rel is None:
        rel = BY_NAME.get(key.split("/")[-1])
    if rel and path_exists(rel, files):
        return _repo_record(rel)
    return {
        "kind": "unresolved",
        "title": "local path not tracked in this repository",
        "note": (
            "A local machine path was named. It is not tracked here, and no public "
            "URL, DOI, or checksum is recorded."
        ),
    }
