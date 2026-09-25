"""Game-drive paths for public sky catalogs. Not a freeze file."""
from __future__ import annotations

import json
from pathlib import Path

GAME = Path(r"D:\FSOT_Benchmarks\anomaly_observables")
CHIME_CATALOG1 = GAME / "frb" / "chime_frb_catalog1_positions.json"
CHIME_POSITIONS = GAME / "frb" / "chime_frb_catalog2_positions.json"
ABELL_CLUSTERS = GAME / "extragalactic_structure" / "abell_clusters.json"
PANTHEON_REDSHIFTS = GAME / "pantheon_plus" / "all_redshifts_PVs.csv"
PANTHEON_DISTANCES = GAME / "pantheon_plus" / "Pantheon+SH0ES.dat"


def load_chime_positions() -> list[dict]:
    doc = json.loads(CHIME_POSITIONS.read_text(encoding="utf-8"))
    rows = []
    for row in doc.get("frbs") or []:
        if row.get("ra_deg") is None or row.get("dec_deg") is None:
            continue
        if row.get("sidelobe_flag") in (1, "1", True):
            continue
        item = dict(row)
        if item.get("dm_excess_pc") is None and item.get("dm_excess_ne2001") is not None:
            item["dm_excess_pc"] = item["dm_excess_ne2001"]
        rows.append(item)
    return rows


def load_abell_clusters() -> list[dict]:
    doc = json.loads(ABELL_CLUSTERS.read_text(encoding="utf-8"))
    return [
        row for row in (doc.get("objects") or [])
        if row.get("ra_deg") is not None and row.get("dec_deg") is not None
    ]
