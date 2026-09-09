#!/usr/bin/env python3
"""Re-score already-locked catalog-class PREDs against in-repo panels.

This is a hold-on-refresh of dumps we already ingest. It does not invent a
dated window and it does not 0.5%-gate a 10-row seed.

Kill: pooled median > 0.5%, or treating a missing live dump as a new ε.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_JSON = ROOT / "results" / "catalog_class_refresh.json"
OUT_MD = ROOT / "predictions" / "reports" / "CATALOG_CLASS_REFRESH.md"
GATE = 0.5

PANELS = [
    ("PRED-066", "Exoplanet_System_Architecture", "exoplanet_system_architecture_benchmark.json"),
    ("PRED-048", "GWTC_Catalog_Open", "gwtc_catalog_open_benchmark.json"),
    ("PRED-067", "Compact_Object_Binary_Events", "compact_object_binary_events_benchmark.json"),
    ("PRED-082", "Gaia_Astrometry_Panel_Deep", "gaia_astrometry_panel_deep_benchmark.json"),
    ("PRED-068", "GBIF_Species_Occurrence", "gbif_species_occurrence_benchmark.json"),
    ("PRED-069", "Epidemiology_Panel", "epidemiology_panel_benchmark.json"),
    ("PRED-080", "Grace_Cryosphere", "grace_cryosphere_benchmark.json"),
    ("PRED-081", "Agriculture_Agroecology", "agriculture_agroecology_gap_fill_benchmark.json"),
    ("PRED-083", "Paleoclimate_Panel", "paleoclimate_panel_benchmark.json"),
    ("PRED-079", "MPCORB_Minor_Planet_Catalog", "mpcorb_fsot_benchmark.json"),
    ("PRED-CAT-GAIA-DR3", "Gaia_DR3_Source_Sample_Open", "gaia_dr3_source_sample_open_benchmark.json"),
    ("PRED-CAT-PUBCHEM", "PubChem_Depth_Open", "pubchem_depth_open_benchmark.json"),
]


def _pooled(doc: dict[str, Any]) -> float | None:
    for key in ("pooled_median_error_pct", "headline_median_error_pct", "median_error_pct"):
        if doc.get(key) is not None:
            try:
                return float(doc[key])
            except (TypeError, ValueError):
                continue
    return None


def build() -> dict[str, Any]:
    rows = []
    for pred, domain, fname in PANELS:
        path = DATA / fname
        if not path.is_file():
            # try common alternates
            alts = list(DATA.glob(fname.replace(".json", "*.json")))[:1]
            path = alts[0] if alts else path
        if not path.is_file():
            rows.append(
                {
                    "pred": pred,
                    "domain": domain,
                    "file": fname,
                    "present": False,
                    "verdict": "missing_panel",
                }
            )
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        pooled = _pooled(doc)
        n = int(doc.get("record_count") or doc.get("scalar_record_count") or 0)
        hold = pooled is not None and pooled <= GATE
        rows.append(
            {
                "pred": pred,
                "domain": domain,
                "file": path.name,
                "present": True,
                "record_count": n,
                "pooled_median_error_pct": pooled,
                "verdict": "hold" if hold else ("kill" if pooled is not None else "no_pooled"),
            }
        )
    holds = sum(1 for r in rows if r.get("verdict") == "hold")
    kills = sum(1 for r in rows if r.get("verdict") == "kill")
    missing = sum(1 for r in rows if r.get("verdict") == "missing_panel")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "gate_pct": GATE,
        "n": len(rows),
        "hold": holds,
        "kill": kills,
        "missing": missing,
        "rows": rows,
        "kill_note": "pooled > 0.5%; a per-object fitted ε; stuffing a missing dump",
    }


def _md(doc: dict[str, Any]) -> str:
    lines = [
        "# Catalog-class refresh (in-repo dumps)",
        "",
        f"*Generated {doc['generated_at']} · pin D1D38A*",
        "",
        "Green residual catalogs are **not** automatically new predictions.",
        "This re-reads the locked panels and scores the class hold (≤ 0.5%).",
        "Live NASA/Gaia/GWTC bytes that are not in-repo stay a future dump.",
        "",
        f"Hold **{doc['hold']}** · kill **{doc['kill']}** · missing **{doc['missing']}**.",
        "",
        "| PRED | Domain | n | pooled % | Verdict |",
        "|------|--------|--:|---------:|---------|",
    ]
    for r in doc["rows"]:
        n = r.get("record_count") if r.get("present") else "—"
        p = r.get("pooled_median_error_pct")
        pct = f"{p:.4f}" if isinstance(p, float) else "—"
        lines.append(
            f"| `{r['pred']}` | {r['domain']} | {n} | {pct} | **{r['verdict']}** |"
        )
    lines += [
        "",
        "Kill for this page: treating it as a request for free parameters.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    doc = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.write_text(_md(doc), encoding="utf-8")
    print(
        f"catalog-class refresh hold={doc['hold']} kill={doc['kill']} "
        f"missing={doc['missing']} → {OUT_JSON.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
