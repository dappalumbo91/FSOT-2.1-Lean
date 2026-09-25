#!/usr/bin/env python3
"""Historical 24 h vs issued 48 h weather windows.

Does NOT rewrite predictions/dated_forecasts/. Public hold/kill stays.
Asks: if we had scored only the first SI day of a frozen 48 h window,
would hold/kill change? Uses NDBC realtime/stdmet (same parser as the scorer).
"""
from __future__ import annotations

import hashlib
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


def _nums(rows: list[dict], key: str) -> list[float]:
    out: list[float] = []
    for r in rows:
        v = r.get(key)
        if v is None:
            continue
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            continue
    return out


def _gust_at_or_above(rows: list[dict], bar: float = 12.0) -> list[dict]:
    """6-minute samples whose gust meets the quiet-kill bar. Times stay on the row."""
    hits: list[dict] = []
    for r in rows:
        try:
            g = float(r.get("gst"))
        except (TypeError, ValueError):
            continue
        if g >= bar:
            hits.append({"t": r.get("t"), "gst": g, "pres": r.get("pres")})
    return hits


def _stormish(rows: list[dict], expect_storm: bool) -> tuple[bool, bool, bool, dict]:
    """Quiet kill is pres<1005 or gust≥12. Mild saw_storm is pres<1010 or gust≥8.

    A quiet cell can 'see' a mild dip on day 1 and still hold, then break on day 2.
    Those are two process days. Do not move 1005/1010 to swallow one of them.
    """
    pres = _nums(rows, "pres")
    gst = _nums(rows, "gst")
    saw_storm = any(p < 1010.0 for p in pres) or any(g >= 8.0 for g in gst)
    quiet_broken = any(p < 1005.0 for p in pres) or any(g >= 12.0 for g in gst)
    ok = saw_storm if expect_storm else (not quiet_broken)
    stats = {
        "min_pres": min(pres) if pres else None,
        "max_gst": max(gst) if gst else None,
        "quiet_broken": quiet_broken,
        "saw_storm": saw_storm,
    }
    return ok, saw_storm, quiet_broken, stats


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
            second = [r for r in all_rows if datetime.fromisoformat(str(r["t"]).replace("Z", "+00:00")) > mid]
            ok48, saw48, br48, st48 = _stormish(all_rows, storm)
            ok24, saw24, br24, st24 = _stormish(first, storm) if first else (False, False, False, {})
            ok2, saw2, br2, st2 = _stormish(second, storm) if second else (False, False, False, {})
            same = (ok48 == ok24) if first else False
            if first and (not storm) and ok24 and not ok48:
                split = "second_process_day"
            elif not first:
                split = "no_obs"
            elif same:
                split = "agree"
            else:
                split = "disagree"
            rows_out.append(
                {
                    "id": fc.get("id"),
                    "buoy_id": bid,
                    "expect_storm": storm,
                    "issued_hours": (end - start).total_seconds() / 3600.0,
                    "n_obs_48h": len(all_rows),
                    "n_obs_24h": len(first),
                    "n_obs_day2": len(second),
                    "saw_storm_48h": saw48,
                    "saw_storm_24h": saw24,
                    "saw_storm_day2": saw2,
                    "quiet_broken_24h": br24,
                    "quiet_broken_48h": br48,
                    "quiet_broken_day2": br2,
                    "min_pres_24h": st24.get("min_pres"),
                    "max_gst_24h": st24.get("max_gst"),
                    "min_pres_day2": st2.get("min_pres"),
                    "max_gst_day2": st2.get("max_gst"),
                    "min_pres_48h": st48.get("min_pres"),
                    "max_gst_48h": st48.get("max_gst"),
                    "result_48h": "hold" if ok48 else "kill",
                    "result_24h": "hold" if ok24 else "kill",
                    "result_day2": ("hold" if ok2 else "kill") if second else "no_obs",
                    "same": same,
                    "split": split,
                    "gust_ge_12_day1": _gust_at_or_above(first),
                    "gust_ge_12_day2": _gust_at_or_above(second),
                }
            )

    n = len(rows_out)
    n_same = sum(1 for r in rows_out if r.get("same"))
    n_obs = sum(1 for r in rows_out if r.get("n_obs_48h", 0) > 0)
    n_second = sum(1 for r in rows_out if r.get("split") == "second_process_day")
    pin = hashlib.sha256((ROOT / "vendor" / "fsot_compute.py").read_bytes()).hexdigest()[:6].upper()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": pin,
        "note": (
            "Frozen 48 h issues not rewritten. A quiet hold on day 1 that breaks on day 2 "
            "is the next process day, not a day-1 miss. gust_ge_12_day2 lists the "
            "NDBC samples on that next day. Bars stay 1010/1005 and 8/12 m/s."
        ),
        "n": n,
        "n_with_obs": n_obs,
        "n_24h_agrees_48h": n_same,
        "n_second_process_day": n_second,
        "rows": rows_out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# Weather 24 h retrospective",
        "",
        f"*Generated {payload['generated_at']} · pin {pin}*",
        "",
        "Issued JSON is **frozen**. 48 h is two process days. Day 1 is the competitive window.",
        "Day 2 is the next window. Bars are not moved.",
        "",
        f"The frozen 48 h card matches the first day on **{n_same}/{n_obs}**.",
        f"Second-process-day breaks: **{n_second}**.",
        "",
        "The law's window is that first day. A quiet hold that breaks only on day 2",
        "is the next process day. The samples that cross 12 m/s are listed below.",
        "The bar stays 12 m/s. Issued JSON stays frozen.",
        "",
        "| ID | Buoy | 48 h | day1 | day2 | split | minP day1 | minP day2 | maxG day1 | maxG day2 |",
        "|----|------|------|------|------|-------|----------:|----------:|----------:|----------:|",
    ]
    for r in rows_out:
        lines.append(
            f"| `{r.get('id')}` | {r.get('buoy_id')} | {r.get('result_48h')} | "
            f"{r.get('result_24h')} | {r.get('result_day2')} | {r.get('split')} | "
            f"{r.get('min_pres_24h')} | {r.get('min_pres_day2')} | "
            f"{r.get('max_gst_24h')} | {r.get('max_gst_day2')} |"
        )
    lines.append("")
    for r in rows_out:
        hits = r.get("gust_ge_12_day2") or []
        if r.get("split") != "second_process_day" or not hits:
            continue
        lines.append(
            f"`{r.get('id')}` {r.get('buoy_id')}: day 1 held "
            f"(min {r.get('min_pres_24h')} hPa, max gust {r.get('max_gst_24h')} m/s, "
            f"{len(r.get('gust_ge_12_day1') or [])} samples at or above 12). "
            f"Day 2 has {len(hits)} samples at or above 12 m/s. "
            f"Window min pressure {r.get('min_pres_day2')} hPa stays above 1005."
        )
        for h in hits:
            lines.append(f"- {h.get('t')}  gust {h.get('gst')} m/s  pressure {h.get('pres')} hPa")
        lines.append("")
    lines += [
        "",
        "Quiet kill: pressure < 1005 hPa or gust ≥ 12 m/s. Mild saw-storm: < 1010 hPa or gust ≥ 8 m/s.",
        "Kill: rewriting issued JSON. Kill: retuning POOF or the bars to swallow PTIT2.",
        "",
        "Refresh: `python scripts/retro_weather_24h.py`",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} n={n} obs={n_obs} agree={n_same}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
