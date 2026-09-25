#!/usr/bin/env python3
"""Log SIMBAD vs live catalog vs frozen host coordinates. Does not edit the freeze."""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "data" / "sh0es_host_coordinates.json"
FROZEN = ROOT / "predictions" / "h0_sightline_predictions.json"
OUT = ROOT / "results" / "host_coordinate_audit.json"

# SIMBAD ICRS J2000, 2026-09-24.
SIMBAD = {
    "NGC7250": (334.574067, 40.562406),
    "NGC5917": (230.377292, -7.377089),
    "UGC9391": (218.653871, 59.338261),
    "NGC2442": (114.099045, -69.530833),
    "NGC1309": (50.527308, -15.399942),
    "NGC1559": (64.398963, -62.783681),
}


def _sep(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    r1, d1, r2, d2 = (math.radians(x) for x in (ra1, dec1, ra2, dec2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def _sector(ra: float) -> str:
    x = ra % 360.0
    if x < 60:
        return "sector_0_planck_depleted"
    if x < 120:
        return "sector_1_local_low"
    if x < 180:
        return "sector_2_carnegie"
    if x < 240:
        return "sector_3_fsot_document"
    if x < 300:
        return "sector_4_freedman"
    return "sector_5_sh0es_inflated"


def main() -> int:
    live = {h["name"]: h for h in json.loads(LIVE.read_text(encoding="utf-8"))["hosts"]}
    frozen_doc = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen = {h["host"]: h for h in frozen_doc["hosts"]}
    rows = []
    for name, (ra, dec) in SIMBAD.items():
        lv = live[name]
        fr = frozen.get(name)
        item = {
            "host": name,
            "simbad_ra_deg": ra,
            "simbad_dec_deg": dec,
            "live_ra_deg": lv["ra_deg"],
            "live_dec_deg": lv["dec_deg"],
            "live_offset_deg": round(_sep(lv["ra_deg"], lv["dec_deg"], ra, dec), 3),
            "live_sector": _sector(float(lv["ra_deg"])),
        }
        if fr:
            item["frozen_ra_deg"] = fr["ra_deg"]
            item["frozen_dec_deg"] = fr["dec_deg"]
            item["frozen_offset_deg"] = round(_sep(fr["ra_deg"], fr["dec_deg"], ra, dec), 3)
            item["frozen_sector"] = fr["sky_sector"]
            item["frozen_h0"] = fr["fsot_predicted_h0"]
            item["frozen_left_unchanged"] = True
        rows.append(item)
    ugc = next(r for r in rows if r["host"] == "UGC9391")
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "SIMBAD ICRS",
        "frozen_file": "predictions/h0_sightline_predictions.json",
        "frozen_rewritten": False,
        "rows": rows,
        "ugc9391_sector_note": (
            "Live RA moves UGC9391 from sector 2 to sector 3. On the frozen "
            "sky-density map that sector reads 73.497 instead of the frozen "
            f"{ugc.get('frozen_h0')}. The frozen value was not rewritten."
        ),
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    for r in rows:
        print(
            f"  {r['host']} live_off={r['live_offset_deg']} "
            f"frozen_off={r.get('frozen_offset_deg')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
