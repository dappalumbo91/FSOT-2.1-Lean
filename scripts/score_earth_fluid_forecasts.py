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
SWPC_KP_1M = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
SWPC_KP_OBS = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
SWPC_KP_FCST = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
GFZ_KP = "https://kp.gfz.de/app/json/"
NDBC_RT = "https://www.ndbc.noaa.gov/data/realtime2"
NDBC_STDMET = "https://www.ndbc.noaa.gov/data/stdmet"
COOPS = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"


def _ssl_ctx():
    try:
        import certifi
        import ssl

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/earth-fluid-score"})
    ctx = _ssl_ctx()
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
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


def _parse_kp_time(tag: str) -> datetime | None:
    tag = str(tag or "").replace("Z", "+00:00")
    try:
        t = datetime.fromisoformat(tag)
    except ValueError:
        try:
            t = datetime.strptime(tag[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t


def _kp_from_rows(rows: list, lo: datetime, hi: datetime) -> float | None:
    mx = None
    for row in rows:
        if not isinstance(row, dict):
            continue
        tag = row.get("time_tag") or row.get("datetime") or row.get("time") or ""
        t = _parse_kp_time(str(tag))
        if t is None or t < lo or t > hi:
            continue
        raw = row.get("kp_index")
        if raw is None:
            raw = row.get("Kp")
        if raw is None:
            raw = row.get("kp")
        try:
            v = float(raw)
        except (TypeError, ValueError):
            continue
        mx = v if mx is None else max(mx, v)
    return mx


def _swpc_kp_max(start_iso: str, end_iso: str) -> float | None:
    """1-minute SWPC rolls off; fall back to 3-hour SWPC then GFZ for closed windows."""
    lo = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    hi = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    if lo.tzinfo is None:
        lo = lo.replace(tzinfo=timezone.utc)
    if hi.tzinfo is None:
        hi = hi.replace(tzinfo=timezone.utc)
    urls = [
        SWPC_KP_1M,
        SWPC_KP_OBS,
        SWPC_KP_FCST,
    ]
    for url in urls:
        try:
            raw = json.loads(_get(url).decode("utf-8"))
        except Exception:
            continue
        if isinstance(raw, dict):
            rows = raw.get("data") or raw.get("kp") or raw.get("records") or []
            if isinstance(rows, dict):
                rows = [rows]
        else:
            rows = raw
        if not isinstance(rows, list):
            continue
        mx = _kp_from_rows(rows, lo, hi)
        if mx is not None:
            return mx
    mx = _gfz_kp_max(lo, hi)
    if mx is not None:
        return mx
    return _gfz_nowcast_kp_max(lo, hi)


def _gfz_nowcast_kp_max(lo: datetime, hi: datetime) -> float | None:
    """GFZ 30-day nowcast ASCII (one line per 3-hour Kp)."""
    urls = (
        "https://kp.gfz.de/app/files/Kp_ap_nowcast.txt",
        "https://kp.gfz-potsdam.de/app/files/Kp_ap_nowcast.txt",
    )
    text = ""
    for url in urls:
        try:
            text = _get(url).decode("utf-8", errors="replace")
            break
        except Exception:
            continue
    if not text:
        return None
    mx = None
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 8:
            continue
        try:
            t = datetime(
                int(parts[0]), int(parts[1]), int(parts[2]),
                int(float(parts[3])), tzinfo=timezone.utc,
            )
            v = float(parts[7])
        except (TypeError, ValueError, IndexError):
            continue
        if v < 0 or t < lo or t > hi:
            continue
        mx = v if mx is None else max(mx, v)
    return mx


def _gfz_kp_max(lo: datetime, hi: datetime) -> float | None:
    """GFZ Potsdam Kp archive — SWPC 1-minute rolls off closed windows."""
    url = (
        f"{GFZ_KP}?start={lo.strftime('%Y-%m-%dT%H:%M:%SZ')}"
        f"&end={hi.strftime('%Y-%m-%dT%H:%M:%SZ')}&index=Kp"
    )
    try:
        raw = json.loads(_get(url).decode("utf-8"))
    except Exception:
        return None
    mx = None
    if isinstance(raw, dict) and isinstance(raw.get("datetime"), list):
        times = raw.get("datetime") or []
        vals = raw.get("Kp") or raw.get("kp") or []
        for tag, val in zip(times, vals):
            t = _parse_kp_time(str(tag))
            if t is None or t < lo or t > hi:
                continue
            try:
                v = float(val)
            except (TypeError, ValueError):
                continue
            mx = v if mx is None else max(mx, v)
        return mx
    if isinstance(raw, list):
        return _kp_from_rows(raw, lo, hi)
    return None


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
        return _score_weather(fc)
    if kind == "tide":
        return _score_tide(fc)
    if kind == "hydrology":
        return _score_hydrology(fc)
    return {"id": fc["id"], "result": "awaiting", "notes": "unknown kind"}


def _parse_ndbc_realtime(text: str, start: datetime, end: datetime) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 13:
            continue
        try:
            t = datetime(
                int(parts[0]), int(parts[1]), int(parts[2]),
                int(parts[3]), int(parts[4]), tzinfo=timezone.utc,
            )
        except ValueError:
            continue
        if t < start or t > end:
            continue
        def _f(i: int, bad: set[str]) -> float | None:
            if i >= len(parts) or parts[i] in bad:
                return None
            try:
                return float(parts[i])
            except ValueError:
                return None
        rows.append({"t": t.isoformat(), "wspd": _f(6, {"MM"}), "gst": _f(7, {"MM"}), "pres": _f(12, {"MM"})})
    return rows


def _score_weather(fc: dict) -> dict:
    q = fc.get("score_query") or {}
    bid = str(q.get("buoy_id") or "")
    storm = bool(q.get("storm"))
    start = datetime.fromisoformat(str(fc["valid_from"]).replace("Z", "+00:00"))
    end = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    rows: list[dict] = []
    notes = ""
    try:
        text = _get(f"{NDBC_RT}/{bid}.txt").decode("utf-8", errors="replace")
        rows = _parse_ndbc_realtime(text, start, end)
    except Exception as exc:
        notes = f"ndbc {bid}: {exc}"
    if not rows:
        # stdmet monthly files keep a longer archive than realtime2.
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
                rows = extra
                break
    if not rows:
        return {
            "id": fc["id"],
            "result": "awaiting",
            "notes": notes or f"no NDBC realtime/stdmet in window for {bid}",
        }
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
    ok = saw_storm if storm else (not quiet_broken)
    return {
        "id": fc["id"],
        "result": "hold" if ok else "kill",
        "n_obs": len(rows),
        "saw_storm": saw_storm,
        "expect_storm": storm,
        "buoy_id": bid,
    }


def _coops(station: str, product: str, start: str, end: str) -> list[dict]:
    url = (
        f"{COOPS}?product={product}&application=FSOT-2.1-Lean"
        f"&station={station}&begin_date={start}&end_date={end}"
        f"&datum=MLLW&time_zone=gmt&units=metric&format=json"
    )
    if product == "predictions":
        url += "&interval=h"
    try:
        doc = json.loads(_get(url).decode("utf-8"))
    except Exception:
        return []
    return list(doc.get("data") or doc.get("predictions") or [])


def _parse_coops_t(tag: str) -> datetime | None:
    try:
        t = datetime.strptime(str(tag), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return t


def _score_tide(fc: dict) -> dict:
    q = fc.get("score_query") or {}
    sid = str(q.get("station_id") or "")
    thr = float(q.get("surge_threshold_m") or 0.1535)
    expect = bool(q.get("expect_surge"))
    lo = datetime.fromisoformat(str(fc["valid_from"]).replace("Z", "+00:00"))
    hi = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
    if lo.tzinfo is None:
        lo = lo.replace(tzinfo=timezone.utc)
    if hi.tzinfo is None:
        hi = hi.replace(tzinfo=timezone.utc)
    start = lo.strftime("%Y%m%d")
    end = hi.strftime("%Y%m%d")
    obs = _coops(sid, "water_level", start, end)
    pred = _coops(sid, "predictions", start, end)
    if not obs or not pred:
        return {"id": fc["id"], "result": "awaiting", "notes": f"CO-OPS {sid} missing obs/pred"}
    pmap = {str(r.get("t")): r for r in pred}
    residuals = []
    for row in obs:
        t = _parse_coops_t(str(row.get("t") or ""))
        if t is None or t < lo or t > hi:
            continue
        pr = pmap.get(str(row.get("t")))
        if not pr:
            continue
        try:
            residuals.append(float(row["v"]) - float(pr["v"]))
        except (TypeError, ValueError, KeyError):
            continue
    if not residuals:
        return {"id": fc["id"], "result": "awaiting", "notes": f"CO-OPS {sid} no overlapping hours in valid window"}
    mx = max(residuals)
    ok = (mx >= thr) if expect else (mx < thr)
    return {
        "id": fc["id"],
        "result": "hold" if ok else "kill",
        "max_residual_m": round(mx, 4),
        "n_hours": len(residuals),
        "expect_surge": expect,
        "station_id": sid,
        "window_clipped": True,
    }


def _score_hydrology(fc: dict) -> dict:
    q = fc.get("score_query") or {}
    sid = str(q.get("site_id") or "")
    expect = bool(q.get("expect_high_flow"))
    q_prior = float(q.get("q_prior_cfs") or 0)
    bar = float(q.get("load_bar") or 1.1535)
    start = str(q.get("start") or fc["valid_from"][:10])
    end = str(q.get("end") or fc["valid_to"][:10])
    url = (
        f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={sid}"
        f"&parameterCd=00060&startDT={start}&endDT={end}"
    )
    try:
        doc = json.loads(_get(url).decode("utf-8"))
    except Exception as exc:
        return {"id": fc["id"], "result": "awaiting", "notes": f"nwis {sid}: {exc}"}
    series = ((doc.get("value") or {}).get("timeSeries")) or []
    qs: list[float] = []
    for ts in series:
        for item in (ts.get("values") or [{}])[0].get("value") or []:
            raw = item.get("value")
            if raw in (None, "", "-999999"):
                continue
            try:
                v = float(raw)
            except (TypeError, ValueError):
                continue
            if v >= 0:
                qs.append(v)
    if not qs:
        return {"id": fc["id"], "result": "awaiting", "notes": f"nwis {sid} no discharge in window"}
    mean_q = sum(qs) / len(qs)
    if expect:
        ok = mean_q >= q_prior
    else:
        ok = mean_q < q_prior * bar
    return {
        "id": fc["id"],
        "result": "hold" if ok else "kill",
        "mean_cfs": round(mean_q, 2),
        "n_obs": len(qs),
        "expect_high_flow": expect,
        "site_id": sid,
    }


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
        prev_path = OUT_DIR / path.name.replace("_issue", "_score")
        prev_by_id: dict[str, dict] = {}
        if prev_path.is_file():
            try:
                for r in json.loads(prev_path.read_text(encoding="utf-8")).get("rows") or []:
                    if r.get("id") and r.get("result") in {"hold", "kill"}:
                        prev_by_id[str(r["id"])] = r
            except Exception:
                prev_by_id = {}
        rows = []
        for fc in doc.get("forecasts") or []:
            sc = _score_one(fc, now)
            if sc is None:
                continue
            # Catalogs roll off. A prior hold/kill is the public scoreboard;
            # do not regress it to awaiting on a missing fetch.
            prev = prev_by_id.get(str(sc.get("id") or ""))
            if prev and sc.get("result") == "awaiting":
                sc = dict(prev)
                sc["notes"] = (
                    str(sc.get("notes") or "")
                    + " kept prior hold/kill; later catalog fetch empty"
                ).strip()
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
