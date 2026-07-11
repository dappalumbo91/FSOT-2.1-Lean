"""First-class reference anchor benchmarks — PDG, CRC handbook, NIST DLMF."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_paths import (  # noqa: E402
    authority_path_for_export,
    fsot_compute_path,
    smiles_dataset_path,
    thesis_root,
)

DLMF_TARGETS: dict[str, dict[str, Any]] = {
    "Bessel_J0_zero1": {
        "name": "Bessel_J0_first_zero",
        "measured": 2.4048255577,
        "unit": "dimensionless",
        "reference": "NIST DLMF §10.21",
        "dlmf_section": "10.21",
    },
    "Bessel_J1_zero1": {
        "name": "Bessel_J1_first_zero",
        "measured": 3.8317059702075125,
        "unit": "dimensionless",
        "reference": "NIST DLMF §10.21",
        "dlmf_section": "10.21",
    },
    "Airy_Ai_zero1": {
        "name": "Airy_Ai_first_zero",
        "measured": 2.338107410459767,
        "unit": "dimensionless",
        "reference": "NIST DLMF §9.9 (|Ai'(x)| first zero magnitude)",
        "dlmf_section": "9.9",
    },
    "gamma1_Stieltjes": {
        "name": "gamma_1_Stieltjes",
        "measured": -0.0728158454838,
        "unit": "dimensionless",
        "reference": "NIST DLMF §5.17",
        "dlmf_section": "5.17",
    },

    "First_Riemann_zero": {
        "name": "First_Riemann_zero",
        "measured": 14.134725141734693,
        "unit": "dimensionless",
        "reference": "Odlyzko / LMFDB zeta zeros",
        "dlmf_section": "25.10",
    },
}


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _bench_doc(
    domain: str,
    maps: list[str],
    d_eff: int,
    records: list[dict],
    source: object,
    authority: object,
) -> dict:
    errs = sorted(float(r["error_pct"]) for r in records)
    med = errs[len(errs) // 2] if errs else None
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "domain": domain,
        "authority_path": authority_path_for_export(Path(str(authority))),
        "source": source,
        "maps_to_lean": maps,
        "D_eff": d_eff,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": med,
        "pooled_median_error_pct": med,
        "max_error_pct": max(errs) if errs else None,
        "records": records,
    }


def _load_smiles_rows() -> list[dict]:
    path = smiles_dataset_path()
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return list(raw.get("records") or raw.get("data") or [])
    return list(raw)


def _source_match(row: dict, token: str) -> bool:
    return token.lower() in str(row.get("source") or "").lower()


def build_pdg_particle_benchmark() -> dict:
    records: list[dict] = []
    for row in _load_smiles_rows():
        if not _source_match(row, "PDG"):
            continue
        computed = row.get("computed_value")
        measured = row.get("target_value")
        if computed is None or measured is None:
            continue
        records.append(
            {
                "lab": "pdg_particle",
                "property": row.get("section"),
                "name": row.get("name"),
                "computed": float(computed),
                "measured": float(measured),
                "error_pct": round(float(row.get("error_pct") or err_pct(float(computed), float(measured))), 6),
                "unit": row.get("unit"),
                "fsot_formula": row.get("fsot_formula"),
                "reference": "PDG 2024 / Zyla et al.",
                "source_corpus": "FSOT_SMILES_Lab_Dataset",
            }
        )
    return _bench_doc(
        "PDG_Particle_Properties",
        ["particle", "atomic"],
        9,
        records,
        "PDG 2024 Review of Particle Physics",
        fsot_compute_path(),
    )


def build_crc_handbook_benchmark() -> dict:
    records: list[dict] = []
    for row in _load_smiles_rows():
        if not _source_match(row, "CRC"):
            continue
        computed = row.get("computed_value")
        measured = row.get("target_value")
        if computed is None or measured is None:
            continue
        records.append(
            {
                "lab": "crc_handbook",
                "property": row.get("section"),
                "name": row.get("name"),
                "computed": float(computed),
                "measured": float(measured),
                "error_pct": round(float(row.get("error_pct") or err_pct(float(computed), float(measured))), 6),
                "unit": row.get("unit"),
                "fsot_formula": row.get("fsot_formula"),
                "reference": row.get("source"),
                "source_corpus": "FSOT_SMILES_Lab_Dataset",
            }
        )
    return _bench_doc(
        "CRC_Handbook_Properties",
        ["chemical", "material"],
        11,
        records,
        "CRC Handbook 97th ed. / NIST WebBook cross-anchors",
        fsot_compute_path(),
    )


def _load_fsot_wave_results() -> dict[str, Any]:
    path = fsot_compute_path()
    spec = importlib.util.spec_from_file_location("fsot_compute_mod", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fsot_compute_mod"] = mod
    spec.loader.exec_module(mod)
    out: dict[str, Any] = {}
    for wave_fn in ("wave8", "wave9", "wave10"):
        for result in getattr(mod, wave_fn)():
            out[result.name] = result
    return out


def build_dlmf_special_functions_benchmark() -> dict:
    wave = _load_fsot_wave_results()
    records: list[dict] = []
    for key, meta in DLMF_TARGETS.items():
        result = wave.get(key)
        if result is None:
            continue
        computed = float(result.computed)
        measured = float(meta["measured"])
        records.append(
            {
                "lab": "nist_dlmf",
                "property": "special_function_zero",
                "name": meta["name"],
                "computed": computed,
                "measured": measured,
                "error_pct": round(err_pct(computed, measured), 6),
                "unit": meta["unit"],
                "fsot_formula": result.formula_str,
                "reference": meta["reference"],
                "dlmf_section": meta["dlmf_section"],
                "source_corpus": "fsot_compute waves 8–10",
            }
        )
    return _bench_doc(
        "NIST_DLMF_Special_Functions",
        ["mathematical", "particle"],
        14,
        records,
        "NIST Digital Library of Mathematical Functions",
        fsot_compute_path(),
    )


BUILDERS = {
    "PDG_Particle_Properties": ("pdg_particle_properties_benchmark.json", build_pdg_particle_benchmark),
    "CRC_Handbook_Properties": ("crc_handbook_properties_benchmark.json", build_crc_handbook_benchmark),
    "NIST_DLMF_Special_Functions": ("nist_dlmf_special_functions_benchmark.json", build_dlmf_special_functions_benchmark),
}

REFERENCE_ANCHOR_DOMAINS = list(BUILDERS.keys())

LEAN_MAP = {
    "PDG_Particle_Properties": ("pdg_particle_properties", "particle", "particle_raw_S_positive", "PdgParticlePropertiesPriors"),
    "CRC_Handbook_Properties": ("crc_handbook_properties", "chemical", "electron_raw_S_positive", "CrcHandbookPropertiesPriors"),
    "NIST_DLMF_Special_Functions": ("nist_dlmf_special_functions", "particle", "particle_raw_S_positive", "NistDlmfSpecialFunctionsPriors"),
}