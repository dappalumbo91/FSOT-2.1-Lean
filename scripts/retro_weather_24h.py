#!/usr/bin/env python3
"""Historical 24 h vs issued 48 h weather windows.

Does NOT rewrite predictions/dated_forecasts/. Public hold/kill stays.
Asks: if we had scored only the first SI day of a frozen 48 h window,
would hold/kill change? Uses NDBC realtime/stdmet (same parser as the scorer).
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from score_earth_fluid_forecasts import (  # noqa: E402
    NDBC_RT,
    NDBC_STDMET,
    _get,
    _parse_ndbc_realtime,
)

ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
OUT = ROOT / "results" / "dated_forecast_scores" / "WEATHER_24H_RETRO.json"
DOC = ROOT / "results" / "dated_forecast_scores" / "WEATHER_24H_RETRO.md"


def _stormish(rows: list[dict], expect_storm: bool) -> tuple[bool, bool]:
    saw_storm = any(
        (r.get("pres") is not None and r["pres"] < 1010.0)
        or (r.get("gst") is not None and r["gst"] >= 8.0)
        for r in rows
        if r.get("pres") is not None or r.get("gst") is not None
    )
    quiet_broken = any(
        (r.get("pres") is not None and r["pres"] < 1005.0)
        or (r.get("gst") is not None and r["gst"] >= 12.0)
        for r in rows
    )
    ok = saw_storm if expect_storm else (not quiet_broken)
    return ok, saw_storm


def _fetch_rows(bid: str, start: datetime, end: datetime) -> list[dict]:
    rows: list[dict] = []
    try:
        text = _get(f"{NDBC_RT}/{bid}.txt").decode("utf-8", errors="replace")
        rows = _parse_ndbc_realtime(text, start, end)
    except Exception:
        rows = []
    if rows:
        return rows
    month = start.strftime("%b")
    for url in (
        f"{NDBC_STDMET}/{month}/{bid}.txt",
        f"{NDBC_STDMET}/{month}/{bid.lower()}.txt",
    ):
        try:
            text = _get(url).decode("utf-8", errors="replace")
        except Exception:
            continue
        extra = _parse_ndbc_realtime(text, start, end)
        if extra:
            return extra
    return []


def main() -> int:
    rows_out: list[dict] = []
    for path in sorted(ISSUE_DIR.glob("*_issue.json")):
        if path.name.upper().startswith("LATEST"):
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        fcs = doc if isinstance(doc, list) else (doc.get("forecasts") or doc.get("rows") or [])
        if isinstance(doc, dict) and not fcs:
            fcs = doc.get("items") or []
        if isinstance(doc, dict) and "id" in doc and doc.get("kind") == "weather":
            fcs = [doc]
        for fc in fcs:
            if not isinstance(fc, dict) or fc.get("kind") != "weather":
                continue
            q = fc.get("score_query") or {}
            loc = fc.get("location") or {}
            bid = str(q.get("buoy_id") or loc.get("buoy_id") or "")
            if not bid:
                continue
            start = datetime.fromisoformat(str(fc["valid_from"]).replace("Z", "+00:00"))
            end = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)
            if end.tzinfo is None:
                end = end.replace(tzinfo=timezone.utc)
            mid = start + timedelta(hours=24)
            storm = bool(q.get("storm") or (fc.get("predicted") or {}).get("class") == "storm_sector")
            all_rows = _fetch_rows(bid, start, end)
            first = [r for r in all_rows if datetime.fromisoformat(str(r["t"]).replace("Z", "+00:00")) <= mid]
            if not all_rows:
                rows_out.append(
                    {
                        "id": fc.get("id"),
                        "buoy_id": bid,
                        "issued_hours": (end - start).total_seconds() / 3600.0,
                        "result_48h": "no_obs",
                        "result_24h": "no_obs",
                        "n_obs_48h": 0,
                        "n_obs_24h": 0,
                    }
                )
                continue
            ok48, saw48 = _stormish(all_rows, storm)
            ok24, saw24 = _stormish(first, storm) if first else (False, False)
            rows_out.append(
                {
                    "id": fc.get("id"),
                    "buoy_id": bid,
                    "expect_storm": storm,
                    "issued_hours": (end - start).total_seconds() / 3600.0,
                    "n_obs_48h": len(all_rows),
                    "n_obs_24h": len(first),
                    "saw_storm_48h": saw48,
                    "saw_storm_24h": saw24,
                    "result_48h": "hold" if ok48 else "kill",
                    "result_24h": "hold" if ok24 else "kill",
                    "same": (ok48 == ok24) if first else False,
                }
            )

    n = len(rows_out)
    n_same = sum(1 for r in rows_out if r.get("same"))
    n_obs = sum(1 for r in rows_out if r.get("n_obs_48h", 0) > 0)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "note": "Frozen 48 h issues not rewritten. 24 h is the next increment for NEW issues.",
        "n": n,
        "n_with_obs": n_obs,
        "n_24h_agrees_48h": n_same,
        "rows": rows_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Weather 24 h retrospective",
        "",
        f"*Generated {payload['generated_at']} · pin D1D38A*",
        "",
        "Issued JSON is **frozen**. This asks whether the first SI day of a 48 h",
        "window would have given the same hold/kill. New issues use 24 h.",
        "",
        f"Compared **{n_same}/{n_obs}** windows with observations (agree 24 h vs 48 h).",
        "",
        "| ID | Buoy | 48 h | 24 h | Same | n24 / n48 |",
        "|----|------|------|------|:----:|----------:|",
    ]
    for r in rows_out:
        lines.append(
            f"| `{r.get('id')}` | {r.get('buoy_id')} | {r.get('result_48h')} | "
            f"{r.get('result_24h')} | {r.get('same')} | "
            f"{r.get('n_obs_24h')}/{r.get('n_obs_48h')} |"
        )
    lines += [
        "",
        "Kill: rewriting issued JSON. Kill: retuning POOF to swallow a miss.",
        "",
        "Refresh: `python scripts/retro_weather_24h.py`",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} n={n} obs={n_obs} agree={n_same}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
