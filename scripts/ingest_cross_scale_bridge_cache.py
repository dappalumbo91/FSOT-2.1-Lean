#!/usr/bin/env python3
"""Cache cross-scale bridge validation data on external drive (G:/FSOT-PublicData)."""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXTERNAL = Path(os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "G:/FSOT-PublicData")) / "cross_scale_bridges"


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _median_err(doc: dict) -> float:
    rows = doc.get("material_records") or doc.get("records") or []
    errs = [float(r["error_pct"]) for r in rows if r.get("error_pct") is not None]
    if not errs:
        return float(doc.get("pooled_median_error_pct") or doc.get("median_error_pct") or 0.0)
    errs.sort()
    return errs[len(errs) // 2]


def build_self_similarity_index() -> dict:
    pairs = [
        ("Immunology", DATA / "immunology_benchmark.json", "Climate_Science", DATA / "climate_observed_benchmark.json"),
        ("External_OSS_Code_Genome", DATA / "external_oss_code_genome_benchmark.json", "Cosmology_Extended", DATA / "cosmology_extended_benchmark.json"),
        ("Neuroimmunology", DATA / "neuroimmunology_benchmark.json", "Planetary_Structure", DATA / "planetary_structure_benchmark.json"),
        ("Phi_Morphogenetic_Scaling", DATA / "phi_morphogenetic_scaling_benchmark.json", "Cosmology_Extended", DATA / "cosmology_extended_benchmark.json"),
        ("Acoustic_Resonance_Materials", DATA / "acoustic_resonance_materials_benchmark.json", "Magnetosphere", DATA / "magnetosphere_benchmark.json"),
    ]
    motifs: list[dict] = []
    for small_name, small_path, large_name, large_path in pairs:
        small = _load_json(small_path)
        large = _load_json(large_path)
        if not small or not large:
            continue
        sm = _median_err(small)
        lg = _median_err(large)
        motifs.append(
            {
                "small_scale_domain": small_name,
                "large_scale_domain": large_name,
                "small_median_error_pct": sm,
                "large_median_error_pct": lg,
                "coherence_delta_pct": abs(sm - lg),
                "claim": "same_scalar_architecture_different_observational_scale",
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "external_cache_root": str(EXTERNAL),
        "motif_count": len(motifs),
        "cross_scale_motifs": motifs,
        "scientific_framing": "orbital_bridge_scientific_framing.yaml",
    }


def fetch_nasa_exoplanet_sample() -> dict:
    """Small NASA Exoplanet Archive sample — stored on external drive only."""
    url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
        "query=select+top+50+pl_name,discoverymethod,pl_orbper,pl_rade,pl_eqt+from+pscomppars+where+default_flag=1&format=json"
    )
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = payload if isinstance(payload, list) else payload.get("data") or []
        return {"source": "nasa_exoplanet_archive", "record_count": len(rows), "records": rows[:50]}
    except Exception as exc:
        return {"source": "nasa_exoplanet_archive", "error": str(exc), "records": []}


def main() -> int:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    index = build_self_similarity_index()
    index_path = EXTERNAL / "cross_scale_self_similarity_index.json"
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Wrote {index_path} motifs={index['motif_count']}")

    exo = fetch_nasa_exoplanet_sample()
    exo_path = EXTERNAL / "nasa_exoplanet_sample.json"
    exo_path.write_text(json.dumps(exo, indent=2), encoding="utf-8")
    print(f"Wrote {exo_path} records={exo.get('record_count', len(exo.get('records') or []))}")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cache_root": str(EXTERNAL),
        "files": [
            "cross_scale_self_similarity_index.json",
            "nasa_exoplanet_sample.json",
        ],
        "note": "Bulk cross-scale validation cache — not stored on main system drive.",
    }
    (EXTERNAL / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Cross-scale bridge cache ready at {EXTERNAL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())