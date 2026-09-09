#!/usr/bin/env python3
"""Diagnose dated-forecast kills as missing planetary-cycle connective tanks.

The issued cell is R⊕·POOF/25 ≈ 39 km (one compactified slice). Solar, volcanic
arc, trench, and basin tanks talk at R⊕·POOF ≈ 978 km (same orifice, 25-D
denominator off). Public kill_if stays on the cell. This is results/ only.

Does not retune kernel km, POOF, or ρ. Does not rewrite issued JSON.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_earth_fluid_forecast import (  # noqa: E402
    POOF,
    R_EARTH_KM,
    cycle_km,
    f,
    haversine_km,
    kernel_km,
)
from score_earth_fluid_forecasts import _gfz_nowcast_kp_max, _ssl_ctx  # noqa: E402

ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
SCORE_DIR = ROOT / "results" / "dated_forecast_scores"
OUT_JSON = ROOT / "results" / "planetary_cycle_kill_diagnosis.json"
OUT_MD = ROOT / "docs" / "PLANETARY_CYCLE_CONNECTIVE.md"
USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query"
UA = "FSOT-2.1-Lean/planetary-cycle"


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = _ssl_ctx()
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return resp.read()


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
        coords = geom.get("coordinates") or [None, None, None]
        if coords[0] is None or props.get("mag") is None:
            continue
        plat, plon = float(coords[1]), float(coords[0])
        etype = str(props.get("type") or "earthquake")
        out.append(
            {
                "id": feat.get("id"),
                "mag": float(props["mag"]),
                "place": props.get("place"),
                "type": etype,
                "km": round(haversine_km(lat, lon, plat, plon), 1),
                "time": props.get("time"),
            }
        )
    out.sort(key=lambda x: (-float(x["mag"]), float(x["km"])))
    return out


def load_kills() -> list[tuple[dict, dict]]:
    issues: dict[str, dict] = {}
    for p in ISSUE_DIR.glob("*_issue.json"):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for fc in doc.get("forecasts") or []:
            issues[str(fc["id"])] = fc
    rows = []
    for p in sorted(SCORE_DIR.glob("*_score.json")):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for r in doc.get("rows") or []:
            if r.get("result") != "kill":
                continue
            fid = str(r.get("id") or "")
            fc = issues.get(fid) or {}
            if not fc:
                continue
            rows.append((r, fc))
    return rows


def _window(fc: dict) -> tuple[str, str]:
    q = fc.get("score_query") or {}
    start = str(q.get("start") or str(fc.get("valid_from") or "")[:10])
    end = str(q.get("end") or str(fc.get("valid_to") or "")[:10])
    return start, end


def diagnose_one(fc: dict) -> dict[str, Any] | None:
    kind = str(fc.get("kind") or "")
    loc = fc.get("location") or {}
    pred = fc.get("predicted") or {}
    valve = str(pred.get("valve_state") or "")
    if kind not in {"earthquake", "volcanic"}:
        return None
    max_recent = float(pred.get("max_mag_recent") or 0)
    loading = valve in {"loading_suction", "post_poof_aftershock"} or max_recent >= 5.5
    if kind == "earthquake" and not loading:
        return None
    if "lat" not in loc:
        return None
    lat, lon = float(loc["lat"]), float(loc["lon"])
    start, end = _window(fc)
    cell_r = kernel_km()
    cyc_r = cycle_km()
    cell = usgs_near(lat, lon, start, end, 4.0, cell_r)
    if cell and "error" in cell[0]:
        return {
            "id": fc.get("id"),
            "kind": kind,
            "place": loc.get("name"),
            "verdict": "catalog_error",
            "notes": cell[0]["error"],
        }
    cycle = usgs_near(lat, lon, start, end, 4.5, cyc_r)
    if cycle and "error" in cycle[0]:
        cycle = []
    volc_cycle = [x for x in cycle if "volcan" in str(x.get("type") or "").lower() or "volcan" in str(x.get("place") or "").lower()]
    lo = datetime.fromisoformat(str(fc["valid_from"]).replace("Z", "+00:00"))
    hi = datetime.fromisoformat(str(fc["valid_to"]).replace("Z", "+00:00"))
    if lo.tzinfo is None:
        lo = lo.replace(tzinfo=timezone.utc)
    if hi.tzinfo is None:
        hi = hi.replace(tzinfo=timezone.utc)
    kp = _gfz_nowcast_kp_max(lo, hi)
    n_cell_m45 = sum(1 for x in cell if float(x["mag"]) >= 4.5)
    n_cycle = len(cycle)
    biggest_cycle = cycle[0] if cycle else None
    solar_storm = kp is not None and kp >= 5.0
    if max_recent >= 5.5 and n_cell_m45 == 0 and n_cycle == 0:
        verdict = "already_poofed"
        why = (
            f"Recent max M={max_recent} was the POOF. Window asked for another "
            "mainshock after the orifice opened. Omori SUCTION can go quiet. "
            "Not a missing 978 km tank and not a kernel retune."
        )
    elif n_cell_m45:
        verdict = "playbook_bar"
        why = (
            f"POOF was in the cell (M≥4.5 n={n_cell_m45}) but the issued bar "
            "was M≥5. Old-rule kill. Not a missing tank."
        )
    elif n_cycle:
        verdict = "transferred_poof"
        why = (
            f"Cell quiet inside {cell_r:.0f} km. Cycle orifice R⊕·POOF={cyc_r:.0f} km "
            f"had {n_cycle} M≥4.5 (max M={biggest_cycle['mag']} at {biggest_cycle['km']} km, "
            f"{biggest_cycle.get('place')}). Load dumped in the arc/trench tank."
        )
    elif solar_storm:
        verdict = "solar_coupled"
        why = (
            f"Cell and cycle quiet. Planetary Kp_max={kp:.2f} ≥ 5 in-window. "
            "Solar tank loaded; crustal orifice did not open at this cell."
        )
    else:
        verdict = "honest_quiet"
        why = (
            f"Loading cell, no M≥4.5 inside {cyc_r:.0f} km, Kp_max="
            f"{'none' if kp is None else f'{kp:.2f}'}. SUCTION held. Not a kernel retune."
        )
    return {
        "id": fc.get("id"),
        "kind": kind,
        "place": loc.get("name"),
        "valve": valve,
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end,
        "cell_km": round(cell_r, 1),
        "cycle_km": round(cyc_r, 1),
        "n_m4_cell": len(cell),
        "n_m45_cell": n_cell_m45,
        "n_m45_cycle": n_cycle,
        "n_volcanic_cycle": len(volc_cycle),
        "biggest_cycle": biggest_cycle,
        "kp_max": kp,
        "solar_storm": solar_storm,
        "verdict": verdict,
        "why": why,
        "max_mag_recent": max_recent,
    }


def diagnose_other(fc: dict, issue_holds: dict[str, list[str]]) -> dict[str, Any] | None:
    """Weather / tide / hydro kills as tank transfers or wrong objects."""
    kind = str(fc.get("kind") or "")
    loc = fc.get("location") or {}
    pred = fc.get("predicted") or {}
    fid = str(fc.get("id") or "")
    if kind == "weather":
        storms = issue_holds.get(fid[:22], [])  # weak key; use issued_at
        issued = str(fc.get("issued_at") or "")
        storms = issue_holds.get(issued, [])
        cls = str(pred.get("class") or "")
        if "quiet" in cls and storms:
            return {
                "id": fid,
                "kind": kind,
                "place": loc.get("name"),
                "valve": pred.get("valve_state"),
                "verdict": "transferred_weather",
                "why": (
                    "Quiet-cell kill while the same issue's storm tanks held: "
                    + ", ".join(storms[:4])
                    + ". Load dumped in the loaded basin. Gap-zone quiet should not issue."
                ),
                "neighbor": storms,
            }
        return {
            "id": fid,
            "kind": kind,
            "place": loc.get("name"),
            "valve": pred.get("valve_state"),
            "verdict": "gap_zone_quiet",
            "why": "Issued quiet in the 1000–1010 hPa / 8–15 m/s gap. New issuer skips. Not a POOF retune.",
        }
    if kind == "tide":
        expect = bool(pred.get("expect_surge") or "surge" in str(pred.get("class") or ""))
        if expect:
            return {
                "id": fid,
                "kind": kind,
                "place": loc.get("name"),
                "verdict": "issue_bar",
                "why": "Surge issue bar is POOF·(1+POOF). Snapshot below issue bar. Not a POOF retune.",
            }
        return {
            "id": fid,
            "kind": kind,
            "place": loc.get("name"),
            "verdict": "honest_quiet_load",
            "why": "Harmonic cell loaded in-window. Honest quiet miss, not a POOF retune.",
        }
    if kind == "hydrology":
        site = str(loc.get("site_id") or "")
        name = str(loc.get("name") or "")
        if "06803510" in site or "06803510" in name:
            return {
                "id": fid,
                "kind": kind,
                "place": name,
                "verdict": "wrong_gage",
                "why": "06803510 is Little Salt Creek, not Missouri at Hermann (06934500). Wrong object.",
            }
        if pred.get("expect_high_flow"):
            return {
                "id": fid,
                "kind": kind,
                "place": name,
                "verdict": "fluid_released",
                "why": "Loading at issue; window mean dropped. SUCTION completed in the river tank.",
            }
        return {
            "id": fid,
            "kind": kind,
            "place": name,
            "verdict": "fluid_loaded",
            "why": "Issued quiet; window mean rose. Honest quiet miss on the river tank.",
        }
    return None


def main() -> int:
    kills = load_kills()
    issue_storm_holds: dict[str, list[str]] = {}
    for p in ISSUE_DIR.glob("*_issue.json"):
        if p.name == "LATEST.json":
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        issued = str(doc.get("issued_at") or "")
        score_p = SCORE_DIR / p.name.replace("_issue", "_score")
        holds: list[str] = []
        if score_p.is_file():
            for r in json.loads(score_p.read_text(encoding="utf-8")).get("rows") or []:
                if r.get("result") == "hold" and r.get("expect_storm"):
                    holds.append(str(r.get("buoy_id") or r.get("id")))
        issue_storm_holds[issued] = holds

    seen: set[tuple] = set()
    rows: list[dict[str, Any]] = []
    other: list[dict[str, Any]] = []
    for _score, fc in kills:
        loc = fc.get("location") or {}
        start, end = _window(fc)
        key = (
            str(fc.get("kind")),
            round(float(loc.get("lat") or 0), 2),
            round(float(loc.get("lon") or 0), 2),
            start,
            end,
        )
        if key in seen:
            continue
        diag = diagnose_one(fc)
        if diag is None:
            o = diagnose_other(fc, issue_storm_holds)
            if o is None:
                continue
            ok = ("other", o.get("id"))
            if ok in seen:
                continue
            seen.add(ok)
            other.append(o)
            continue
        seen.add(key)
        rows.append(diag)

    by_v: dict[str, int] = {}
    for r in rows + other:
        by_v[str(r["verdict"])] = by_v.get(str(r["verdict"]), 0) + 1

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "policy": [
            "do_not_rewrite_issued_json",
            "do_not_retune_kernel_or_POOF",
            "cell_is_R_earth_POOF_over_25",
            "cycle_is_R_earth_POOF",
            "recent_M55_is_the_POOF_not_a_new_loading_promise",
            "public_kill_stays_on_the_cell",
        ],
        "cell_km": kernel_km(),
        "cycle_km": cycle_km(),
        "poof": f(POOF),
        "r_earth_km": R_EARTH_KM,
        "n": len(rows),
        "n_other": len(other),
        "by_verdict": by_v,
        "rows": rows,
        "other_tanks": other,
        "kill": (
            "a new radius fitted to swallow Scotia Sea; "
            "calling transferred_poof a 0.5% central; rewriting kill_if; "
            "promising a second mainshock after a recent M≥5.5"
        ),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")

    md = [
        "# Planetary-cycle connective tanks — why isolated cells kill",
        "",
        f"*Generated {doc['generated_at']} · pin D1D38A*",
        "",
        "Earth is one 25-D compactified fluid. A dated cell is **one slice** of the",
        "crustal orifice. Solar wind, volcanic arcs, trenches, weather basins, and",
        "rivers are **other tanks of the same valve**. Scoring them as siloed",
        "catalogs misses a POOF that dumped next door.",
        "",
        "| Scale | Form | km | Job |",
        "|-------|------|---:|-----|",
        f"| Cell (issued kill_if) | \(R_\\oplus\\cdot\\mathrm{{POOF}}/25\) | **{kernel_km():.1f}** | compactified crustal orifice |",
        f"| Planetary cycle | \(R_\\oplus\\cdot\\mathrm{{POOF}}\) | **{cycle_km():.1f}** | arc / trench / basin tanks talk |",
        "| Solar | planetary Kp | global | magnetosphere tank (already issued) |",
        "",
        "Not a new coefficient. The `/25` is the compactification fold. Taking it",
        "off is looking at the planet as one tank, the same way Materials and Optics",
        "are two looks at \(D=10\).",
        "",
        "**Public scoreboard stays the cell kill.** This ledger names the neighbor",
        "POOF. Do not retune kernel km or POOF. Do not rewrite issued JSON.",
        "",
        f"**Refresh:** `python scripts/diagnose_planetary_cycle_kills.py`",
        "",
        "## Unique loading / volcanic kills",
        "",
        "| ID | Place | Cell M≥4.5 | Cycle M≥4.5 | Kp | Verdict | Why |",
        "|----|-------|-----------:|------------:|---:|---------|-----|",
    ]
    for r in rows:
        big = r.get("biggest_cycle") or {}
        cyc = (
            f"{r['n_m45_cycle']}"
            + (f" (M{big.get('mag')} @ {big.get('km')} km)" if big else "")
        )
        kp = "—" if r.get("kp_max") is None else f"{r['kp_max']:.2f}"
        md.append(
            f"| `{r['id']}` | {r.get('place')} | {r['n_m45_cell']} | {cyc} | {kp} | "
            f"**{r['verdict']}** | {r['why']} |"
        )
    md += [
        "",
        f"Crust counts: { {k: v for k, v in by_v.items() if k in ('transferred_poof','playbook_bar','already_poofed','honest_quiet','solar_coupled')} }.",
        "",
        "## Remaining other-tank kills (weather / tide / hydro)",
        "",
        "| ID | Place | Verdict | Why |",
        "|----|-------|---------|-----|",
    ]
    if not other:
        md.append("| *(none)* | | | |")
    else:
        seen_o: set[str] = set()
        for r in other:
            rid = str(r.get("id") or "")
            if rid in seen_o:
                continue
            seen_o.add(rid)
            md.append(
                f"| `{rid}` | {r.get('place')} | **{r['verdict']}** | {r['why']} |"
            )
    md += [
        "",
        f"All verdicts: {by_v}.",
        "",
        "## Verdict vocabulary",
        "",
        "| Verdict | Meaning | Next issue |",
        "|---------|---------|------------|",
        "| `transferred_poof` | Cell quiet; cycle orifice had M≥4.5 (arc/trench). | Record neighbor tank. Cell kill_if unchanged. |",
        "| `already_poofed` | Recent M≥5.5 *was* the POOF. Window asked for a second mainshock. | `valve_state` checks big event first; post-POOF is quiet hold. |",
        "| `playbook_bar` | POOF was in the cell under M≥4.5; issued bar was M≥5. | Already encoded: loading uses 4.5. |",
        "| `solar_coupled` | Crust quiet; Kp≥5. Solar tank loaded. | Keep solar as a planetary tank on every crustal issue. |",
        "| `honest_quiet` | Loading, no cycle POOF, no recent M≥5.5, Kp quiet. SUCTION held. | Not a kernel retune. |",
        "| `transferred_weather` | Quiet buoy kill; storm tanks on the same issue held. | Skip gap-zone quiet. |",
        "| `wrong_gage` | Hydro ID is a different river. | 06934500 Hermann. |",
        "| `fluid_released` | River loaded at issue; window mean dropped. | SUCTION completed. |",
        "",
        "Scotia Sea: n_recent=2, max M=6.2. That 6.2 already opened the orifice. "
        "Labeling it `loading_suction` because rate-up ran *before* the big-event "
        "check was the remaining miss. Next issues: recent M≥5.5 → `post_poof_aftershock`, "
        "expect_event false (Omori may go quiet).",
        "",
        "## What this is not",
        "",
        "- A fitted 150 km or 1000 km spring to swallow Scotia Sea.",
        "- A clock-time hypocenter.",
        "- Flipping a public cell-kill to hold.",
        "- A new \(D_{\\mathrm{eff}}\) for 'planetary science of earthquakes'.",
        "",
        "Issued EQ/volcanic forecasts now carry `cycle_radius_km` and",
        "`neighbor_kinds` on **new** issues only.",
        "",
        "Related: [`WEATHER_MONITORING_APPROACH.md`](WEATHER_MONITORING_APPROACH.md) ·",
        "[`CONCEPTS.md`](CONCEPTS.md) C1/C2/C10 ·",
        "[`../results/dated_forecast_scores/KILL_AUTOPSY.md`](../results/dated_forecast_scores/KILL_AUTOPSY.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"  n={len(rows)} other={len(other)} by_verdict={by_v} cell={kernel_km():.1f} cycle={cycle_km():.1f}")
    for r in rows:
        print(f"  {r['verdict']:20s} {r['id']}  {r.get('place')}")
    for r in other:
        print(f"  {r['verdict']:20s} {r['id']}  {r.get('place')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
