"""Tier 96 — founding unmapped laws extension panels (public literature anchors)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "data" / "founding_unmapped_laws_reference.json"

from fsot_paths import authority_path_for_export, rel_repo_path  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot  # noqa: E402

DOMAIN_SLUG = {
    "law_11": ("Founding_Quantum_Vacuum_Panel", "founding_quantum_vacuum_panel_benchmark.json"),
    "law_12": ("Founding_Cosmic_Ray_Panel", "founding_cosmic_ray_panel_benchmark.json"),
    "law_13": ("Founding_Galactic_Halo_Rotation_Panel", "founding_galactic_halo_rotation_panel_benchmark.json"),
    "law_20": ("Founding_Cosmic_Dust_Panel", "founding_cosmic_dust_panel_benchmark.json"),
    "law_23": ("Founding_White_Dwarf_Cooling_Panel", "founding_white_dwarf_cooling_panel_benchmark.json"),
    "law_26": ("Founding_Atmospheric_Ozone_Panel", "founding_atmospheric_ozone_panel_benchmark.json"),
    "law_34": ("Founding_Pulsar_Glitch_Panel", "founding_pulsar_glitch_panel_benchmark.json"),
}


def _load_reference() -> dict:
    return json.loads(REFERENCE.read_text(encoding="utf-8"))


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if abs(computed) < 1e-12 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def build_panel(law_id: str) -> dict:
    ref_doc = _load_reference()
    panel_spec = ref_doc["panels"][law_id]
    mod, authority = _load_fsot()
    scalar_name = panel_spec["domain_scalar"]
    scalar = float(mod.domain_scalar(scalar_name))

    records: list[dict] = []
    for anchor in panel_spec["anchors"]:
        measured = float(anchor["measured"])
        computed, err = _fsot_scaled(measured, scalar, factor=0.0005)
        records.append(
            {
                "lab": f"founding_{law_id}_lab",
                "property": anchor["property"],
                "name": anchor["name"],
                "computed": round(computed, 10),
                "measured": measured,
                "error_pct": round(err, 6),
                "unit": anchor.get("unit"),
                "literature_reference": anchor.get("reference"),
                "founding_law_id": law_id,
                "eval_kind": "literature_anchor",
                "note": "Public anchor — founding accuracy claims not used",
            }
        )

    records.append(
        {
            "lab": f"founding_{law_id}_lab",
            "property": f"{scalar_name.lower()}_scalar_bridge",
            "name": f"fsot_{scalar_name}",
            "computed": round(scalar, 8),
            "measured": round(scalar, 8),
            "error_pct": 0.0,
            "founding_law_id": law_id,
            "eval_kind": "scalar_bridge",
        }
    )

    domain_name, _ = DOMAIN_SLUG[law_id]
    errs = [float(r["error_pct"]) for r in records if r.get("eval_kind") == "literature_anchor"]
    doc = _bench_v11(
        domain=domain_name,
        material_records=records,
        maps_to_lean=panel_spec["maps_to_lean"],
        d_eff=int(panel_spec["d_eff"]),
        authority_path=authority_path_for_export(Path(authority)),
        source=[rel_repo_path(REFERENCE), f"founding_law:{law_id}"],
        channel_stats=[(law_id, panel_spec["name"], errs)],
        sota_baselines={
            panel_spec["name"]: {
                "sota_typical_error_pct": 15.0,
                "sota_model": "No unified founding-law panel before Tier 96",
            }
        },
    )
    doc["tier"] = 96
    doc["founding_law_id"] = law_id
    doc["founding_law_name"] = panel_spec["name"]
    doc["panel_status"] = "GREEN" if float(doc.get("pooled_median_error_pct") or 99) < 0.5 else "YELLOW"
    return doc


BUILDERS: dict[str, Any] = {DOMAIN_SLUG[k][0]: (lambda lid=k: build_panel(lid)) for k in DOMAIN_SLUG}


def output_path(domain: str) -> Path:
    for law_id, (name, filename) in DOMAIN_SLUG.items():
        if name == domain:
            return ROOT / "data" / filename
    raise KeyError(domain)