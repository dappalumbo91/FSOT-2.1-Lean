#!/usr/bin/env python3
"""Catalog-native prediction layer from open panels already in the monorepo.

Does NOT change the global framework residual gate (≤0.5%).
Registers Tier A/C style locks with catalog-specific kill notes.

Sources (green panels):
  MPCORB, Gaia DR3 sample, DESI public depth, GWTC open, PubChem properties

Outputs:
  predictions/catalog_prediction_layer.json
  predictions/reports/CATALOG_PREDICTION_LAYER.md
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PRED = ROOT / "predictions"
OUT_JSON = PRED / "catalog_prediction_layer.json"
OUT_MD = PRED / "reports" / "CATALOG_PREDICTION_LAYER.md"

# Global framework gate — never overridden here
FRAMEWORK_GATE_PCT = 0.5

CATALOGS = [
    {
        "id": "CAT-MPCORB",
        "domain": "MPCORB_Minor_Planet_Catalog",
        "file": "mpcorb_fsot_benchmark.json",
        "tier": "C",
        "sector": "astro_gw",
        "future_survey": "MPC / IAU minor-planet catalog refreshes",
        "note": (
            "FSOT residual hold under channel stack. Classical field metrics "
            "(RMS arcsec, U, Kepler Δn/n) live in data/mpcorb_classical_metrics.json "
            "— dual scoreboard; not the same unit as residual %."
        ),
        "classical_metrics": "data/mpcorb_classical_metrics.json",
    },
    {
        "id": "CAT-GAIA-DR3",
        "domain": "Gaia_DR3_Source_Sample_Open",
        "file": "gaia_dr3_source_sample_open_benchmark.json",
        "tier": "A",
        "sector": "astro_gw",
        "future_survey": "Gaia DR4 / DR3 reprocess public samples",
        "note": "Astrometric open sample residual lock (distance-ladder adjacent).",
    },
    {
        "id": "CAT-DESI-PUBLIC",
        "domain": "DESI_Public_Depth_Open",
        "file": "desi_public_depth_open_benchmark.json",
        "tier": "A",
        "sector": "cosmology",
        "future_survey": "DESI public BAO / spectroscopy catalog refreshes",
        "note": "Public DESI depth residual lock — companion to w_a / H0 bridge PREDs.",
    },
    {
        "id": "CAT-DESI-EDR-FITS",
        "domain": "DESI_EDR_FITS_Residual",
        "file": "desi_edr_fits_residual_benchmark.json",
        "tier": "A",
        "sector": "cosmology",
        "future_survey": "DESI EDR/DR table residual refreshes",
        "note": "Large EDR residual surface (~97k class) — catalog kill, not free ε.",
    },
    {
        "id": "CAT-GWTC",
        "domain": "GWTC_Catalog_Open",
        "file": "gwtc_catalog_open_benchmark.json",
        "tier": "A",
        "sector": "astro_gw",
        "future_survey": "GWOSC / GWTC catalog updates (O4 remainder, O5)",
        "note": "Gravitational-wave transient catalog residual lock.",
    },
    {
        "id": "CAT-PUBCHEM",
        "domain": "PubChem_Compound_Properties",
        "file": "pubchem_compound_properties_benchmark.json",
        "tier": "C",
        "sector": "materials_chem",
        "future_survey": "PubChem compound property dumps",
        "note": "Molecular property class lock (open chemistry).",
    },
    {
        "id": "CAT-EXO",
        "domain": "Exoplanet_Archive_Depth_Open",
        "file": "exoplanet_archive_depth_open_benchmark.json",
        "tier": "A",
        "sector": "astro_gw",
        "future_survey": "NASA Exoplanet Archive continuous updates",
        "note": "Exoplanet architecture / property residual lock.",
    },
    {
        "id": "CAT-CLIMATE",
        "domain": "climate_observed",
        "file": "climate_observed_benchmark.json",
        "tier": "C",
        "sector": "earth_climate",
        "future_survey": "NOAA NCEI / open climate station refreshes",
        "note": "Observed climate residual hold under continuous open data.",
    },
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _panel_stats(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"present": False}
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"present": False, "error": str(e)}
    recs = d.get("records") or d.get("material_records") or []
    med = d.get("pooled_median_error_pct")
    if med is None:
        med = d.get("median_error_pct")
    # top scalar locks (continuous)
    locks = []
    if isinstance(recs, list):
        for r in recs:
            if not isinstance(r, dict):
                continue
            try:
                c = float(r.get("computed"))
                m = float(r.get("measured"))
                e = r.get("error_pct")
                e = float(e) if e is not None else abs(c - m) / max(abs(m), 1e-12) * 100.0
            except (TypeError, ValueError):
                continue
            if m == 0 and c == 0:
                continue
            if e > FRAMEWORK_GATE_PCT:
                continue
            name = r.get("name") or r.get("property") or "observable"
            if str(name) in {"all_channels", "fsot_prediction"} and m == 0:
                # depth panels often encode residual as computed vs 0
                locks.append(
                    {
                        "name": str(name),
                        "kind": "residual_encoded",
                        "fsot_predicted": c,
                        "panel_measured": m,
                        "error_pct_at_registration": e,
                    }
                )
                continue
            if abs(m) <= 1.0 and abs(c) <= 1.0 and m in (0.0, 1.0) and c in (0.0, 1.0):
                continue
            locks.append(
                {
                    "name": str(name),
                    "property": r.get("property"),
                    "kind": "scalar",
                    "fsot_predicted": c,
                    "panel_measured": m,
                    "error_pct_at_registration": e,
                    "unit": r.get("unit"),
                }
            )
        locks.sort(key=lambda x: x["error_pct_at_registration"])
    return {
        "present": True,
        "record_count": int(d.get("record_count") or len(recs) or 0),
        "pooled_median_error_pct": med,
        "green_under_framework": (
            med is not None and float(med) <= FRAMEWORK_GATE_PCT
        ),
        "top_scalar_locks": locks[:8],
    }


def build() -> dict:
    predictions = []
    catalogs_out = []
    for cat in CATALOGS:
        path = DATA / cat["file"]
        stats = _panel_stats(path)
        med = stats.get("pooled_median_error_pct")
        try:
            med_f = float(med) if med is not None else None
        except (TypeError, ValueError):
            med_f = None

        residual_id = f"PRED-{cat['id']}-RESIDUAL"
        residual = {
            "id": residual_id,
            "tier": cat["tier"],
            "kind": "catalog_residual_hold",
            "domain": cat["domain"],
            "sector": cat["sector"],
            "catalog_id": cat["id"],
            "benchmark_file": cat["file"],
            "fsot_predicted": med_f if med_f is not None else 0.0,
            "unit": "pooled_median_error_pct_watch",
            "framework_gate_pct": FRAMEWORK_GATE_PCT,
            "kill": f"{cat['id']}_pooled_median_exceeds_{FRAMEWORK_GATE_PCT}_pct_on_catalog_refresh",
            "future_survey": cat["future_survey"],
            "note": cat["note"],
            "record_count": stats.get("record_count"),
            "registered_at": "2026-08-06",
            "status": "registered" if stats.get("present") else "missing_panel",
        }
        predictions.append(residual)

        for i, lock in enumerate(stats.get("top_scalar_locks") or []):
            if lock.get("kind") == "residual_encoded":
                continue
            sid = f"PRED-{cat['id']}-S{i+1:02d}"
            predictions.append(
                {
                    "id": sid,
                    "tier": cat["tier"],
                    "kind": "catalog_scalar_lock",
                    "domain": cat["domain"],
                    "sector": cat["sector"],
                    "catalog_id": cat["id"],
                    "observable": lock.get("name"),
                    "fsot_predicted": lock.get("fsot_predicted"),
                    "panel_measured_at_registration": lock.get("panel_measured"),
                    "error_pct_at_registration": lock.get("error_pct_at_registration"),
                    "unit": lock.get("unit"),
                    "framework_gate_pct": FRAMEWORK_GATE_PCT,
                    "kill": (
                        f"{cat['id']}_{lock.get('name')}_outside_"
                        f"{FRAMEWORK_GATE_PCT}pct_of_fsot_on_refresh"
                    ),
                    "future_survey": cat["future_survey"],
                    "registered_at": "2026-08-06",
                }
            )

        catalogs_out.append(
            {
                **cat,
                "stats": {
                    "record_count": stats.get("record_count"),
                    "pooled_median_error_pct": med_f,
                    "green_under_framework": stats.get("green_under_framework"),
                    "present": stats.get("present"),
                },
                "residual_pred_id": residual_id,
            }
        )

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "authority_pin_prefix": "D1D38A",
        "framework_gate_pct": FRAMEWORK_GATE_PCT,
        "framework_gate_note": (
            "Global residual framework gate remains ≤0.5%. This layer does not "
            "replace or relax that gate. Domain-specific tighter kills (e.g. Higgs) "
            "are a separate follow-on program — see predictions/HIGGS_TIGHTEN_PLAN.md."
        ),
        "purpose": (
            "Catalog-native predictions from open panels already residual-gated in "
            "the monorepo (MPCORB, Gaia, DESI, GWTC, PubChem, exoplanets, climate)."
        ),
        "catalog_count": len(catalogs_out),
        "prediction_count": len(predictions),
        "catalogs": catalogs_out,
        "predictions": predictions,
        "refresh": "python scripts/build_catalog_prediction_layer.py",
    }
    raw = json.dumps(
        {k: v for k, v in doc.items() if k not in {"bundle_sha256", "predictions"}},
        sort_keys=True,
    ).encode()
    ids = json.dumps([p["id"] for p in predictions], sort_keys=True).encode()
    doc["bundle_sha256"] = hashlib.sha256(raw + ids).hexdigest()
    return doc


def write_md(doc: dict) -> None:
    lines = [
        "# Catalog prediction layer",
        "",
        f"*Generated {doc.get('generated_at')} · pin D1D38A*",
        "",
        str(doc.get("purpose") or ""),
        "",
        f"**Framework gate (unchanged):** ≤ **{doc.get('framework_gate_pct')}%** pooled residual.",
        "",
        str(doc.get("framework_gate_note") or ""),
        "",
        f"Catalogs: **{doc.get('catalog_count')}** · Predictions: **{doc.get('prediction_count')}**",
        "",
        "| Catalog | Tier | Records | Pooled % | Residual PRED | Survey |",
        "|---------|------|--------:|---------:|---------------|--------|",
    ]
    for c in doc.get("catalogs") or []:
        st = c.get("stats") or {}
        lines.append(
            f"| {c.get('id')} | {c.get('tier')} | {st.get('record_count')} | "
            f"{st.get('pooled_median_error_pct')} | `{c.get('residual_pred_id')}` | "
            f"{c.get('future_survey')} |"
        )
    lines.extend(
        [
            "",
            "## Sample scalar locks",
            "",
            "| ID | Domain | Observable | FSOT | Err % |",
            "|----|--------|------------|-----:|------:|",
        ]
    )
    for p in (doc.get("predictions") or [])[:40]:
        if p.get("kind") != "catalog_scalar_lock":
            continue
        lines.append(
            f"| `{p.get('id')}` | {p.get('domain')} | {p.get('observable')} | "
            f"{p.get('fsot_predicted')} | {p.get('error_pct_at_registration')} |"
        )
    lines.extend(
        [
            "",
            "Refresh: `python scripts/build_catalog_prediction_layer.py`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    PRED.mkdir(parents=True, exist_ok=True)
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"  catalogs={doc['catalog_count']} preds={doc['prediction_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
