#!/usr/bin/env python3
"""Raw observation O–C residuals using MPC optical data + JPL Horizons.

Pipeline:
  1. Load stratified sample of raw MPC observations (external drive)
  2. For each object, query JPL Horizons geocentric RA/Dec at observation epochs
  3. Angular O–C = |obs − Horizons| in arcseconds (field-standard residual unit)

This uses **granular observations** (not literature summaries) and an industrial
ephemeris (Horizons / DE441) — the same class of tools the catalog is based on.

Storage: G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations/
Outputs:
  data/mpcorb_raw_oc_residuals.json
  predictions/reports/MPCORB_RAW_OC_RESIDUALS.md
"""

from __future__ import annotations

import json
import math
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = Path(r"G:\FSOT-PublicData\anomaly_observables\mpcorb_raw_observations")
LOCAL = ROOT / "vendor" / "mpcorb" / "raw_observations"
OUT_JSON = ROOT / "data" / "mpcorb_raw_oc_residuals.json"
OUT_MD = ROOT / "predictions" / "reports" / "MPCORB_RAW_OC_RESIDUALS.md"
CLASSICAL = ROOT / "data" / "mpcorb_classical_metrics.json"
FSOT_BENCH = ROOT / "data" / "mpcorb_fsot_benchmark.json"

HORIZONS = "https://ssd.jpl.nasa.gov/api/horizons.api"
DEG = math.pi / 180.0
ARCSEC = 3600.0


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _median(xs: list[float]) -> float | None:
    return float(statistics.median(xs)) if xs else None


def _pct(xs: list[float], p: float) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    k = (len(s) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(s[int(k)])
    return float(s[f] * (c - k) + s[c] * (k - f))


def _storage() -> Path:
    if (EXTERNAL / "sample_index.json").is_file():
        return EXTERNAL
    if (LOCAL / "sample_index.json").is_file():
        return LOCAL
    raise FileNotFoundError(
        "Run python scripts/ingest_mpcorb_raw_observations.py first"
    )


def parse_iso_to_jd(iso: str) -> float:
    iso = str(iso).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(iso)
    except ValueError:
        dt = datetime.fromisoformat(iso.split(".")[0])
    y, m = dt.year, dt.month
    d = dt.day + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0) / 24.0
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + A // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5


def ang_sep_arcsec(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    r1, d1, r2, d2 = ra1 * DEG, dec1 * DEG, ra2 * DEG, dec2 * DEG
    cos_c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    cos_c = max(-1.0, min(1.0, cos_c))
    return math.acos(cos_c) / DEG * ARCSEC


def horizons_radec_batch(command: str, jd_list: list[float]) -> dict[float, tuple[float, float]]:
    """Return map jd → (ra_deg, dec_deg) from Horizons OBSERVER table."""
    if not jd_list:
        return {}
    # Horizons TLIST: space-separated JDs
    tlist = " ".join(f"{jd:.6f}" for jd in jd_list)
    params = {
        "format": "json",
        "COMMAND": f"'{command};'" if not str(command).endswith(";") else f"'{command}'",
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "'500@399'",
        "TLIST": tlist,
        "QUANTITIES": "1",
        "ANG_FORMAT": "DEG",
        "CAL_FORMAT": "JD",
    }
    # COMMAND format: '1;' for numbered minor planets
    params["COMMAND"] = f"{command};" if str(command).replace(".", "").isdigit() else command

    url = HORIZONS + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/raw-oc"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(str(payload.get("error"))[:200])
    text = payload.get("result") or ""
    i0 = text.find("$$SOE")
    i1 = text.find("$$EOE")
    if i0 < 0 or i1 < 0:
        raise RuntimeError("Horizons table missing SOE/EOE")
    body = text[i0 + 5 : i1].strip()
    out: dict[float, tuple[float, float]] = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("*"):
            continue
        parts = line.split()
        # CAL_FORMAT=JD → JD RA DEC
        if len(parts) < 3:
            continue
        try:
            jd = float(parts[0])
            ra = float(parts[1])
            dec = float(parts[2])
            out[jd] = (ra, dec)
        except ValueError:
            continue
    return out


def subsample(obs: list[dict], max_n: int) -> list[dict]:
    if len(obs) <= max_n:
        return obs
    # prefer post-2000 CCD-era
    modern = [o for o in obs if str(o.get("obstime", "")).startswith(("20", "19"))]
    pool = modern if len(modern) >= max_n // 2 else obs
    step = len(pool) / max_n
    return [pool[int(i * step)] for i in range(max_n)]


def process_object(
    path: Path,
    *,
    max_obs: int = 40,
    sleep_s: float = 0.5,
) -> dict[str, Any] | None:
    data = json.loads(path.read_text(encoding="utf-8"))
    orbit = data.get("orbit") or {}
    obs = data.get("observations") or []
    desig = str(orbit.get("api_desig") or orbit.get("des_packed") or path.stem)
    optical = [
        o
        for o in obs
        if o.get("ra_deg") is not None and o.get("dec_deg") is not None and o.get("obstime")
    ]
    optical = subsample(optical, max_obs)
    if len(optical) < 3:
        return None

    # Build JD list and obs map
    items = []
    for o in optical:
        try:
            jd = parse_iso_to_jd(str(o["obstime"]))
            items.append((jd, float(o["ra_deg"]), float(o["dec_deg"]), str(o["obstime"])))
        except Exception:
            continue
    if len(items) < 3:
        return None

    # Horizons command: numbered minor planets by number
    cmd = desig
    jds = [it[0] for it in items]
    try:
        # batch in chunks of 25 (Horizons URL length)
        pred: dict[float, tuple[float, float]] = {}
        chunk = 25
        for i in range(0, len(jds), chunk):
            part = jds[i : i + chunk]
            pred.update(horizons_radec_batch(cmd, part))
            time.sleep(sleep_s)
    except Exception as e:
        return {
            "desig": desig,
            "error": str(e)[:180],
            "regime": orbit.get("regime"),
            "U": orbit.get("U"),
            "rms_catalog_arcsec": orbit.get("rms_catalog_arcsec"),
        }

    residuals = []
    for jd, ra_o, dec_o, _t in items:
        # match nearest predicted JD (float key)
        if not pred:
            break
        best_jd = min(pred.keys(), key=lambda k: abs(k - jd))
        if abs(best_jd - jd) > 0.02:  # > ~30 min mismatch
            continue
        pra, pdec = pred[best_jd]
        sep = ang_sep_arcsec(ra_o, dec_o, pra, pdec)
        if math.isfinite(sep) and sep < 3600:  # < 1 deg sanity
            residuals.append(sep)

    if not residuals:
        return {
            "desig": desig,
            "error": "no_matched_residuals",
            "regime": orbit.get("regime"),
            "U": orbit.get("U"),
            "rms_catalog_arcsec": orbit.get("rms_catalog_arcsec"),
            "n_horizons": len(pred),
        }

    return {
        "desig": desig,
        "regime": orbit.get("regime"),
        "U": orbit.get("U"),
        "rms_catalog_arcsec": orbit.get("rms_catalog_arcsec"),
        "n_obs_used": len(residuals),
        "n_obs_available": len(obs),
        "raw_oc_median_arcsec": _median(residuals),
        "raw_oc_mean_arcsec": float(statistics.mean(residuals)),
        "raw_oc_p95_arcsec": _pct(residuals, 95),
        "raw_oc_rms_arcsec": math.sqrt(sum(r * r for r in residuals) / len(residuals)),
        "ephemeris": "JPL_Horizons_OBSERVER_geocentric",
        "observations_source": "MPC_Observations_API_ADES",
    }


def build(max_obs: int = 40) -> dict:
    store = _storage()
    index = json.loads((store / "sample_index.json").read_text(encoding="utf-8"))
    objects_dir = store / "objects"

    per_object = []
    errors = []
    for entry in index.get("objects") or []:
        if not entry.get("fetch_ok"):
            continue
        desig = str(entry.get("api_desig"))
        path = objects_dir / f"{desig}.json"
        if not path.is_file():
            alt = entry.get("path")
            path = Path(alt) if alt else path
        if not path.is_file():
            continue
        print(f"O–C {desig}…", end=" ", flush=True)
        rec = process_object(path, max_obs=max_obs)
        if rec and rec.get("raw_oc_median_arcsec") is not None:
            print(f"med={rec['raw_oc_median_arcsec']:.3f}\" n={rec['n_obs_used']}")
            per_object.append(rec)
        else:
            err = (rec or {}).get("error") or "failed"
            print(f"skip ({err})")
            if rec:
                errors.append(rec)

    all_med = [r["raw_oc_median_arcsec"] for r in per_object]
    all_rms = [r["raw_oc_rms_arcsec"] for r in per_object]
    cat_rms = [r["rms_catalog_arcsec"] for r in per_object if r.get("rms_catalog_arcsec") is not None]

    classical = {}
    if CLASSICAL.is_file():
        try:
            classical = json.loads(CLASSICAL.read_text(encoding="utf-8")).get("dual_scoreboard") or {}
        except Exception:
            pass
    fsot_pct = None
    if FSOT_BENCH.is_file():
        try:
            fb = json.loads(FSOT_BENCH.read_text(encoding="utf-8"))
            fsot_pct = fb.get("pooled_median_error_pct") or fb.get("median_error_pct")
        except Exception:
            pass

    by_regime: dict[str, list[float]] = {}
    for r in per_object:
        by_regime.setdefault(str(r.get("regime")), []).append(r["raw_oc_median_arcsec"])

    doc = {
        "generated_at": _now(),
        "version": "2.0",
        "storage_root": str(store).replace("\\", "/"),
        "ephemeris": "JPL Horizons geocentric OBSERVER (DE441-class)",
        "observations": "MPC Observations API ADES (optical RA/Dec)",
        "honesty": {
            "what_this_is": (
                "O–C in arcseconds between raw MPC optical observations we download "
                "and JPL Horizons predicted positions at those epochs — granular data, "
                "not a literature summary table."
            ),
            "what_this_is_not": (
                "Not a re-fit of orbits. Catalog rms remains the MPC's own orbit-fit "
                "residual; Horizons O–C is an independent industrial ephemeris check."
            ),
            "granular_data": True,
            "literature_only": False,
        },
        "sample": {
            "objects_in_index": index.get("sample_size"),
            "objects_with_oc": len(per_object),
            "objects_failed": len(errors),
            "max_obs_per_object": max_obs,
        },
        "raw_oc_summary_arcsec": {
            "median_of_object_medians": _median(all_med),
            "p95_of_object_medians": _pct(all_med, 95) if all_med else None,
            "median_of_object_rms": _median(all_rms),
            "n_objects": len(all_med),
        },
        "catalog_rms_on_same_sample_arcsec": {
            "median": _median(cat_rms),
            "p95": _pct(cat_rms, 95) if cat_rms else None,
            "n": len(cat_rms),
        },
        "by_regime_median_oc_arcsec": {
            reg: _median(xs) for reg, xs in sorted(by_regime.items())
        },
        "triple_scoreboard": {
            "raw_obs_horizons_median_oc_arcsec": _median(all_med),
            "catalog_median_rms_arcsec": classical.get("classical_median_rms_arcsec")
            or _median(cat_rms),
            "fsot_pooled_median_error_pct": fsot_pct,
            "note": (
                "Three layers on real data: (1) raw MPC obs vs Horizons O–C arcsec, "
                "(2) MPCORB catalog rms field arcsec, (3) FSOT seed residual %."
            ),
        },
        "objects": per_object,
        "failures": errors[:20],
        "refresh": [
            "python scripts/ingest_mpcorb_raw_observations.py",
            "python scripts/build_mpcorb_raw_oc_residuals.py",
        ],
    }
    return doc


def write_md(doc: dict) -> None:
    ts = doc.get("triple_scoreboard") or {}
    raw = doc.get("raw_oc_summary_arcsec") or {}
    cat = doc.get("catalog_rms_on_same_sample_arcsec") or {}
    lines = [
        "# MPCORB raw observation O–C (MPC + JPL Horizons)",
        "",
        f"*Generated {doc.get('generated_at')}*",
        "",
        str((doc.get("honesty") or {}).get("what_this_is") or ""),
        "",
        f"**Ephemeris:** {doc.get('ephemeris')}  ",
        f"**Observations:** {doc.get('observations')}  ",
        f"**Store:** `{doc.get('storage_root')}`",
        "",
        str((doc.get("honesty") or {}).get("what_this_is_not") or ""),
        "",
        "## Triple scoreboard (granular data)",
        "",
        "| Layer | Value | Unit |",
        "|-------|------:|------|",
        f"| **Raw obs vs Horizons O–C (median)** | **{ts.get('raw_obs_horizons_median_oc_arcsec')}** | arcsec |",
        f"| Catalog RMS on same sample | {cat.get('median')} | arcsec |",
        f"| Catalog RMS full MPCORB median | {ts.get('catalog_median_rms_arcsec')} | arcsec |",
        f"| FSOT pooled residual | {ts.get('fsot_pooled_median_error_pct')} | % |",
        "",
        str(ts.get("note") or ""),
        "",
        f"Objects scored: **{(doc.get('sample') or {}).get('objects_with_oc')}** "
        f"(up to {(doc.get('sample') or {}).get('max_obs_per_object')} obs each)",
        "",
        f"| Raw O–C summary | arcsec |",
        f"|-----------------|-------:|",
        f"| median of object medians | {raw.get('median_of_object_medians')} |",
        f"| p95 of object medians | {raw.get('p95_of_object_medians')} |",
        f"| median of object RMS | {raw.get('median_of_object_rms')} |",
        "",
        "## By regime",
        "",
        "| Regime | median O–C (arcsec) |",
        "|--------|--------------------:|",
    ]
    for reg, v in (doc.get("by_regime_median_oc_arcsec") or {}).items():
        lines.append(f"| {reg} | {v} |")

    lines.extend(
        [
            "",
            "## Per-object",
            "",
            "| Desig | Regime | U | Catalog RMS | Horizons O–C med | O–C RMS | n |",
            "|------:|--------|--:|------------:|-----------------:|--------:|--:|",
        ]
    )
    for o in sorted(
        doc.get("objects") or [],
        key=lambda x: (x.get("raw_oc_median_arcsec") or 0),
    ):
        lines.append(
            f"| {o.get('desig')} | {o.get('regime')} | {o.get('U')} | "
            f"{o.get('rms_catalog_arcsec')} | {o.get('raw_oc_median_arcsec'):.4f} | "
            f"{o.get('raw_oc_rms_arcsec'):.4f} | {o.get('n_obs_used')} |"
        )

    lines.extend(
        [
            "",
            "```powershell",
            "python scripts/ingest_mpcorb_raw_observations.py --max-objects 48",
            "python scripts/build_mpcorb_raw_oc_residuals.py",
            "python scripts/build_mpcorb_classical_metrics.py",
            "```",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    print("Computing raw O–C via Horizons + MPC observations…")
    doc = build(max_obs=40)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    ts = doc["triple_scoreboard"]
    print(
        f"  objects={doc['sample']['objects_with_oc']} "
        f"raw_oc={ts.get('raw_obs_horizons_median_oc_arcsec')} arcsec "
        f"catalog_rms={ts.get('catalog_median_rms_arcsec')} "
        f"fsot%={ts.get('fsot_pooled_median_error_pct')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
