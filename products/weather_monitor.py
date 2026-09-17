#!/usr/bin/env python3
"""Weather window product — scored NDBC cells. Not ECMWF S2S. Pin AEB2AD."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "results" / "dated_forecast_scores" / "LATEST.json"


def main() -> int:
    print("product=weather_monitor pin=AEB2AD ledger=B_correct kill=ECMWF_S2S_beat_claim")
    if not LATEST.is_file():
        print("missing results/dated_forecast_scores/LATEST.json — run score_earth_fluid_forecasts.py")
        return 1
    doc = json.loads(LATEST.read_text(encoding="utf-8"))
    rows = [r for r in (doc.get("rows") or doc.get("forecasts") or []) if r.get("kind") == "weather"]
    if not rows and isinstance(doc.get("issues"), list):
        for issue in doc["issues"]:
            for r in issue.get("rows") or []:
                if r.get("kind") == "weather":
                    rows.append(r)
    # LATEST may be a rollup with per-issue files referenced
    scores = ROOT / "results" / "dated_forecast_scores"
    if not rows:
        for p in sorted(scores.glob("*_score.json")):
            blob = json.loads(p.read_text(encoding="utf-8"))
            for r in blob.get("rows") or []:
                rid = str(r.get("id") or "")
                if r.get("kind") == "weather" or "-WX-" in rid:
                    r = dict(r)
                    r["_issue"] = p.name
                    rows.append(r)
    hold = sum(1 for r in rows if r.get("result") == "hold")
    kill = sum(1 for r in rows if r.get("result") == "kill")
    awaiting = sum(1 for r in rows if r.get("result") == "awaiting")
    print(f"weather_cells hold={hold} kill={kill} awaiting={awaiting} (missing NDBC ≠ retune)")
    print("window=24h_process  not_claimed: week-3 S2S skill")
    for r in rows[-5:]:
        print(f"  {r.get('id')} {r.get('result')} {r.get('detail') or r.get('reason') or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
