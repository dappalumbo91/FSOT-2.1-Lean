#!/usr/bin/env python3
"""Autopsy dated-forecast kills vs what actually happened.

Does not rewrite issued JSON. Writes results/dated_forecast_scores/KILL_AUTOPSY.md
"""
from __future__ import annotations

import json
import math
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from fsot_earth_fluid_forecast import POOF, f  # noqa: E402

ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
SCORE_DIR = ROOT / "results" / "dated_forecast_scores"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NDBC_RT = "https://www.ndbc.noaa.gov/data/realtime2"
COOPS = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
R_EARTH = 6371.0
UA = "FSOT-2.1-Lean/kill-autopsy"


def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def hav(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_EARTH * math.asin(min(1.0, math.sqrt(a)))


def load_issues() -> dict[str, dict]:
    out = {}
    for p in ISSUE_DIR.glob("*_issue.json"):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for fc in doc.get("forecasts") or []:
            out[str(fc["id"])] = fc
    return out


def load_kills() -> list[tuple[str, dict, dict]]:
    issues = load_issues()
    rows = []
    for p in sorted(SCORE_DIR.glob("*_score.json")):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for r in doc.get("rows") or []:
            if r.get("result") != "kill":
                continue
            fid = str(r.get("id") or "")
            rows.append((p.name, r, issues.get(fid) or {}))
    return rows


def usgs_near(lat: float, lon: float, start: str, end: str, mag_min: float, radius: float) -> list[dict]:
    url = (
        f"{USGS}?format=geojson&starttime={start}&endtime={end}"
        f"&minmagnitude={mag_min}&orderby=time&limit=200"
        f"&latitude={lat}&longitude={lon}&maxradiuskm={radius}"
    )
    try:
        doc = json.loads(_get(url).decode("utf-8"))
    except Exception as exc:
        return [{"error": str(exc)}]
    out = []
    for feat in doc.get("features") or []:
        props = feat.get("properties") or {}
        geom = feat.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None]
        if coords[0] is None or props.get("mag") is None:
            continue
        plat, plon = float(coords[1]), float(coords[0])
        out.append(
            {
                "id": feat.get("id"),
                "mag": float(props["mag"]),
                "place": props.get("place"),
                "km": round(hav(lat, lon, plat, plon), 1),
                "time": props.get("time"),
            }
        )
    out.sort(key=lambda x: (-float(x["mag"]), float(x["km"])))
    return out


def ndbc_extrema(bid: str, lo: datetime, hi: datetime) -> dict:
    try:
        text = _get(f"{NDBC_RT}/{bid}.txt").decode("utf-8", errors="replace")
    except Exception as exc:
        return {"error": str(exc)}
    gst, pres, n = [], [], 0
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 13:
            continue
        try:
            t = datetime(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), tzinfo=timezone.utc)
        except ValueError:
            continue
        if t < lo or t > hi:
            continue
        n += 1
        try:
            if parts[7] not in {"MM"}:
                gst.append(float(parts[7]))
        except ValueError:
            pass
        try:
            if parts[12] not in {"MM"}:
                pres.append(float(parts[12]))
        except ValueError:
            pass
    return {
        "n": n,
        "gst_max": max(gst) if gst else None,
        "pres_min": min(pres) if pres else None,
        "gst_n": len(gst),
        "pres_n": len(pres),
    }


def autopsy_eq(score: dict, fc: dict) -> dict:
    loc = fc.get("location") or {}
    pred = fc.get("predicted") or {}
    q = fc.get("score_query") or {}
    lat, lon = float(loc["lat"]), float(loc["lon"])
    start, end = str(q.get("start")), str(q.get("end"))
    r0 = float(q.get("radius_km") or 39.1)
    mag0 = float(q.get("mag_min") or 5.0)
    near39_m4 = usgs_near(lat, lon, start, end, 4.0, r0)
    if near39_m4 and "error" in near39_m4[0]:
        err = near39_m4[0]["error"]
        near39_m4, near150_m45 = [], []
    else:
        err = None
        near150_m45 = usgs_near(lat, lon, start, end, 4.5, 150.0)
        if near150_m45 and "error" in near150_m45[0]:
            near150_m45 = []
    in_kernel_m45 = [x for x in near39_m4 if float(x["mag"]) >= 4.5]
    hit_m5 = [x for x in near39_m4 if float(x["mag"]) >= mag0]
    nearest = (near150_m45[0] if near150_m45 else None)
    return {
        "kind": "earthquake",
        "id": fc.get("id"),
        "place": loc.get("name"),
        "valve": pred.get("valve_state"),
        "expect_event": pred.get("expect_event"),
        "mag_min": mag0,
        "n_recent": pred.get("n_recent"),
        "max_mag_recent": pred.get("max_mag_recent"),
        "pressure": pred.get("fsot_pressure"),
        "usgs_error": err,
        "n_m4_in_kernel": len(near39_m4),
        "n_m45_in_kernel": len(in_kernel_m45),
        "n_m5_in_kernel": len(hit_m5),
        "biggest_in_kernel": near39_m4[0] if near39_m4 else None,
        "nearest_m45_150km": nearest,
        "gap": (
            "no M>=4 in kernel"
            if not near39_m4
            else f"kernel max M={near39_m4[0]['mag']} at {near39_m4[0]['km']} km (need M>={mag0})"
        ),
    }


def autopsy_wx(score: dict, fc: dict) -> dict:
    loc = fc.get("location") or {}
    pred = fc.get("predicted") or {}
    bid = str((fc.get("score_query") or {}).get("buoy_id") or loc.get("buoy_id") or "")
    lo = datetime.fromisoformat(str(fc["valid_from"]).replace("Z", "+00:00"))
    hi = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
    if lo.tzinfo is None:
        lo = lo.replace(tzinfo=timezone.utc)
    if hi.tzinfo is None:
        hi = hi.replace(tzinfo=timezone.utc)
    ext = ndbc_extrema(bid, lo, hi)
    return {
        "kind": "weather",
        "id": fc.get("id"),
        "place": loc.get("name"),
        "valve": pred.get("valve_state"),
        "class": pred.get("class"),
        "pres_now": pred.get("pres_now"),
        "gst_now": pred.get("gst_now"),
        "expect_storm": (fc.get("score_query") or {}).get("storm"),
        "kill_if": fc.get("kill_if"),
        "ndbc": ext,
        "gap": (
            ext.get("error")
            or f"issued quiet at pres={pred.get('pres_now')} gst={pred.get('gst_now')}; "
            f"window min_pres={ext.get('pres_min')} max_gst={ext.get('gst_max')}"
        ),
    }


def autopsy_tide(score: dict, fc: dict) -> dict:
    pred = fc.get("predicted") or {}
    loc = fc.get("location") or {}
    thr = float(pred.get("surge_threshold_m") or f(POOF))
    now = pred.get("residual_now_m")
    mx = score.get("max_residual_m")
    expect = bool(pred.get("expect_surge"))
    if expect:
        gap = (
            f"issued surge; snapshot {now} m vs POOF {thr:.4f}; 48h max {mx} m "
            f"(short by {round(thr - float(mx), 4) if mx is not None else '?'} m)"
        )
    else:
        gap = (
            f"issued harmonic; snapshot {now} m << POOF {thr:.4f}; "
            f"48h max {mx} m crossed the bar"
        )
    return {
        "kind": "tide",
        "id": fc.get("id"),
        "place": loc.get("name"),
        "expect_surge": expect,
        "residual_now_m": now,
        "max_in_window_m": mx,
        "threshold_m": thr,
        "delta_m": None if now is None or mx is None else round(float(now) - float(mx), 4),
        "gap": gap,
    }


def autopsy_hydro(score: dict, fc: dict) -> dict:
    pred = fc.get("predicted") or {}
    loc = fc.get("location") or {}
    q = fc.get("score_query") or {}
    expect = bool(pred.get("expect_high_flow"))
    mean = score.get("mean_cfs")
    prior = pred.get("q_prior_cfs")
    recent = pred.get("q_recent_cfs")
    site = str(q.get("site_id") or loc.get("site_id") or "")
    return {
        "kind": "hydrology",
        "id": fc.get("id"),
        "place": loc.get("name"),
        "site_id": site,
        "valve": pred.get("valve_state"),
        "expect_high_flow": expect,
        "q_recent_cfs": recent,
        "q_prior_cfs": prior,
        "load_ratio": pred.get("load_ratio"),
        "mean_cfs": mean,
        "gap": (
            f"issued {'high' if expect else 'quiet'} flow on {site}; "
            f"recent={recent} prior={prior} window_mean={mean} cfs"
        ),
    }


def main() -> int:
    kills = load_kills()
    autopsies = []
    for score_file, score, fc in kills:
        kind = (fc.get("kind") or "")
        if kind == "earthquake":
            a = autopsy_eq(score, fc)
        elif kind == "weather":
            a = autopsy_wx(score, fc)
        elif kind == "tide":
            a = autopsy_tide(score, fc)
        elif kind == "hydrology":
            a = autopsy_hydro(score, fc)
        elif kind == "volcanic":
            a = autopsy_eq(score, fc)
            a["kind"] = "volcanic"
            a["gap"] = (
                (a.get("gap") or "no M>=4 in 39 km cell")
                + " — check planetary cycle R⊕·POOF (~978 km) / Kp; cell kill_if unchanged"
            )
        else:
            a = {"kind": kind, "id": score.get("id"), "gap": "unhandled"}
        a["score_file"] = score_file
        autopsies.append(a)
        print(a.get("id"), a.get("kind"), a.get("gap"))

    out_json = SCORE_DIR / "KILL_AUTOPSY.json"
    out_md = SCORE_DIR / "KILL_AUTOPSY.md"
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "n_kills": len(autopsies),
        "policy": "do_not_rewrite_issued_json",
        "autopsies": autopsies,
        "solve": {
            "eq": "Do not promise M>=5 on released/steady cells. Loading cells: score elevated M>=4.5 rate vs prior half, not a guaranteed M>=5.",
            "wx_quiet": "Do not issue quiet if already pres<1005 or gst>=12. Skip lake buoys with short realtime buffers.",
            "tide": "Surge issue bar = POOF*(1+POOF). Harmonic cells can still load in 48 h — that is an honest quiet miss, not a POOF retune.",
            "hydro": "Dated-forecast gage IDs must match the named river (06803510 is Little Salt Creek, not Hermann). Do not rewrite issued JSON.",
            "planetary_cycle": (
                "Cell is R⊕·POOF/25. Neighbor tanks (solar/volcanic arc/trench/basin) "
                "talk at R⊕·POOF. Diagnose transferred_poof vs honest_quiet. "
                "Do not retune kernel km."
            ),
        },
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    by_kind: dict[str, list] = {}
    for a in autopsies:
        by_kind.setdefault(str(a.get("kind") or "?"), []).append(a)

    lines = [
        "# Kill autopsy — dated fluid windows",
        "",
        f"*Generated {payload['generated_at']} · pin D1D38A · **{len(autopsies)} kills***",
        "",
        "Issued JSON is frozen. Public scoreboard of those files stays these kills.",
        "This explains **why** each kill fired. Playbook retro of the first 12:",
        "[`RULE_RETRO.md`](RULE_RETRO.md).",
        "",
    ]
    order = ["earthquake", "weather", "tide", "hydrology", "solar", "volcanic"]
    for kind in order:
        rows = by_kind.get(kind) or []
        if not rows:
            continue
        lines += [
            f"## {kind} ({len(rows)})",
            "",
            "| ID | Issued | Gap |",
            "|----|--------|-----|",
        ]
        for a in rows:
            issued = (
                a.get("valve")
                or a.get("class")
                or ("surge" if a.get("expect_surge") else "harmonic")
            )
            lines.append(
                f"| `{a.get('id')}` | {issued} · {a.get('place')} | {a.get('gap')} |"
            )
        lines.append("")

    extra = [k for k in by_kind if k not in order]
    for kind in extra:
        for a in by_kind[kind]:
            lines.append(f"- `{a.get('id')}` ({kind}): {a.get('gap')}")

    lines += [
        "## Solve (next issues only)",
        "",
        "- **EQ:** `expect_event` only on loading / post-POOF. Released/steady hold if quiet. "
        "Loading: elevated M≥4.5, not a promised M≥5. Aug 25 duplicate issues used the old rule; "
        "do not rewrite them. Scotia Sea loading with no M≥4.5 stays an honest miss.",
        "- **Quiet weather:** do not issue if already past 1005 hPa / 12 m/s. Skip lake `other` buoys. "
        "A clean quiet (pres≥1010, gst<8) that later crosses 12 m/s is an honest 48 h miss.",
        "- **Tides:** surge *issue* bar = POOF·(1+POOF). Harmonic cells can still load in 48 h — "
        "that is an honest quiet miss, not a POOF retune.",
        "- **Hydrology:** dated-forecast gage IDs must match the named river. `06803510` is "
        "Little Salt Creek near Lincoln NE, not Missouri at Hermann (`06934500`). Issued JSON stays.",
        "- **Planetary cycle:** cell = R⊕·POOF/25 (39 km). Neighbor tanks (solar / volcanic arc / "
        "trench / basin) talk at R⊕·POOF (~978 km). Five loading kills were transferred_poof on "
        "the arc. Scotia Sea is honest_quiet. See [`../../docs/PLANETARY_CYCLE_CONNECTIVE.md`]"
        "(../../docs/PLANETARY_CYCLE_CONNECTIVE.md). Do not retune kernel km.",
        "",
        "Do not retune ρ, POOF, or kernel km to swallow these.",
        "",
        "Refresh: `python scripts/autopsy_dated_forecast_kills.py`",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
