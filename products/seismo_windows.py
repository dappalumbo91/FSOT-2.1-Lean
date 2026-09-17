#!/usr/bin/env python3
"""Seismology window product — 39 km cells / φ^4 days. Not UTC hypocenter. Pin AEB2AD."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORES = ROOT / "results" / "dated_forecast_scores"


def main() -> int:
    print("product=seismo_windows pin=AEB2AD ledger=B_correct kill=UTC_hypocenter_as_0.5pct")
    rows = []
    for p in sorted(SCORES.glob("*_score.json")):
        blob = json.loads(p.read_text(encoding="utf-8"))
        for r in blob.get("rows") or []:
            rid = str(r.get("id") or "")
            if r.get("kind") == "earthquake" or "-EQ-" in rid:
                rows.append(r)
    hold = sum(1 for r in rows if r.get("result") == "hold")
    kill = sum(1 for r in rows if r.get("result") == "kill")
    print(f"eq_cells hold={hold} kill={kill} kernel_km≈39.1 horizon=φ^4→7d")
    print("not_claimed: M7 at 14:32:07 UTC as a 0.5% central")
    for r in rows[-6:]:
        loc = (r.get("location") or {}).get("name") if isinstance(r.get("location"), dict) else ""
        print(f"  {r.get('id')} {r.get('result')} {loc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
