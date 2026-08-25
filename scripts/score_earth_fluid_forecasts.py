#!/usr/bin/env python3
"""Score issued fluid-pressure forecasts against live USGS / SWPC / NDBC.

Reads predictions/dated_forecasts/*.json (not LATEST only). Writes
results/dated_forecast_scores/<issue-date>.json and appends jsonl outcomes.
Does not rewrite the frozen issue files.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_earth_fluid_forecast import haversine_km  # noqa: E402
from record_prediction_outcome import append_outcome, _git_sha  # noqa: E402

ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
OUT_DIR = ROOT / "results" / "dated_forecast_scores"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query"
SWPC_KP = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/earth-fluid-score"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _usgs_window(q: dict) -> list[dict]:
    url = (
        f"{USGS}?format=geojson&starttime={q['start']}&endtime={q['end']}"
        f"&minmagnitude={q['mag_min']}&orderby=time&limit=200"
        f"&latitude={q['lat']}&longitude={q['lon']}&maxradiuskm={q['radius_km']}"
    )
    try:
        doc = json.loads(_get(url).decode("utf-8"))
    except Exception as exc:
        return [{"error": str(exc)}]
    hits = []
    for feat in doc.get("features") or []:
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None, None]
        if coords[0] is None:
            continue
        hits.append(
            {
                "id": feat.get("id"),
                "mag": props.get("mag"),
                "place": props.get("place"),
                "lat": coords[1],
                "lon": coords[0],
                "km": haversine_km(q["lat"], q["lon"], float(coords[1]), float(coords[0])),
            }
        )
    return hits


def _swpc_kp_max(start_iso: str, end_iso: str) -> float | None:
    try:
        series = json.loads(_get(SWPC_KP).decode("utf-8"))
    except Exception:
        return None
    lo = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    hi = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    mx = None
    for row in series:
        tag = str(row.get("time_tag") or "")
        try:
            t = datetime.fromisoformat(tag.replace("Z", "+00:00"))
        except ValueError:
            continue
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        if lo <= t <= hi:
            try:
                v = float(row.get("kp_index") or 0)
            except (TypeError, ValueError):
                continue
            mx = v if mx is None else max(mx, v)
    return mx


def _score_one(fc: dict, now: datetime) -> dict | None:
    end = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    if now < end:
        return {
            "id": fc["id"],
            "result": "awaiting",
            "notes": "window still open",
        }
    kind = fc.get("kind")
    pred = fc.get("predicted") or {}
    q = fc.get("score_query") or {}
    if kind in {"earthquake", "volcanic"}:
        hits = _usgs_window(q)
        if hits and "error" in hits[0]:
            return {"id": fc["id"], "result": "awaiting", "notes": hits[0]["error"]}
        n = len(hits)
        expect = bool(pred.get("expect_event", True))
        ok = (n >= 1) if expect else (n == 0)
        return {
            "id": fc["id"],
            "result": "hold" if ok else "kill",
            "n_hits": n,
            "hits": hits[:8],
            "expect_event": expect,
        }
    if kind == "solar":
        mx = _swpc_kp_max(str(fc["valid_from"]), str(fc["valid_to"]))
        if mx is None:
            return {"id": fc["id"], "result": "awaiting", "notes": "no SWPC Kp in window"}
        expect = bool(pred.get("expect_kp_ge_5"))
        ok = (mx >= 5.0) if expect else (mx < 5.0)
        return {
            "id": fc["id"],
            "result": "hold" if ok else "kill",
            "kp_max": mx,
            "expect_kp_ge_5": expect,
        }
    if kind == "weather":
        return {
            "id": fc["id"],
            "result": "awaiting",
            "notes": "re-issue NDBC pull and compare pres/gust by buoy_id (live txt)",
        }
    return {"id": fc["id"], "result": "awaiting", "notes": "unknown kind"}


def main() -> int:
    now = datetime.now(timezone.utc)
    issues = sorted(
        p for p in ISSUE_DIR.glob("*_issue.json") if p.name != "LATEST.json"
    )
    if not issues:
        print("no issued forecasts")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for path in issues:
        doc = json.loads(path.read_text(encoding="utf-8"))
        rows = []
        for fc in doc.get("forecasts") or []:
            sc = _score_one(fc, now)
            if sc is None:
                continue
            rows.append(sc)
            if sc.get("result") in {"hold", "kill"}:
                append_outcome(
                    {
                        "ts": now.isoformat(),
                        "commit_sha": _git_sha(),
                        "pred_id": sc["id"],
                        "survey": "USGS-FDSN/SWPC-dated-fluid",
                        "result": sc["result"],
                        "measured": sc.get("n_hits", sc.get("kp_max")),
                        "notes": json.dumps({k: v for k, v in sc.items() if k != "hits"}),
                        "authority_pin_prefix": "D1D38A",
                        "predictions_untouched": True,
                    }
                )
        outp = OUT_DIR / path.name.replace("_issue", "_score")
        out_doc = {
            "scored_at": now.isoformat(),
            "issue": str(path.as_posix()),
            "rows": rows,
            "n_hold": sum(1 for r in rows if r.get("result") == "hold"),
            "n_kill": sum(1 for r in rows if r.get("result") == "kill"),
            "n_awaiting": sum(1 for r in rows if r.get("result") == "awaiting"),
        }
        outp.write_text(json.dumps(out_doc, indent=2), encoding="utf-8")
        summary.append(out_doc)
        print(
            f"{path.name}: hold={out_doc['n_hold']} kill={out_doc['n_kill']} "
            f"awaiting={out_doc['n_awaiting']}"
        )
    roll = OUT_DIR / "LATEST.json"
    roll.write_text(json.dumps({"scored_at": now.isoformat(), "issues": summary}, indent=2), encoding="utf-8")
    print(f"Wrote {roll}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
