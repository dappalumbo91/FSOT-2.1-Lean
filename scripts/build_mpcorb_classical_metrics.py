#!/usr/bin/env python3
"""Classical minor-planet metrics from MPCORB (alongside FSOT residual %).

The field does **not** normally quote a catalog-wide pooled residual percent.
Standard measures are:

  1. Astrometric O–C RMS residual in **arcseconds** (stored in MPCORB as rms)
  2. Orbit quality **U** parameter (0 = best … 9 = poor; special flags D/E/F)
  3. Fractional element consistency (here: two-body Kepler Δn/n)
  4. Observation/opposition coverage (#Obs, #Opp)

This builder reports those classical metrics on the full catalog **in addition to**
the existing FSOT pooled residual % (unchanged; see build_mpcorb_fsot_benchmark.py).

Note: recomputing epoch O–C from raw observations requires observation files.
MPCORB already carries the orbit-fit RMS residual used by the MPC — that is the
catalog-native classical residual we score here.

Outputs:
  data/mpcorb_classical_metrics.json
  data/mpcorb_classical_metrics.md
  predictions/reports/MPCORB_CLASSICAL_METRICS.md  (copy for scoreboard)
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "vendor" / "mpcorb"
OUT_JSON = ROOT / "data" / "mpcorb_classical_metrics.json"
OUT_MD = ROOT / "data" / "mpcorb_classical_metrics.md"
OUT_PRED_MD = ROOT / "predictions" / "reports" / "MPCORB_CLASSICAL_METRICS.md"

# Gaussian gravitational constant → mean motion deg/day for a in AU
K_GAUSS = 0.01720209895
N_DEG_SCALE = (180.0 / math.pi) * K_GAUSS

# Literature-style survey RMS context (arcsec) — comparison bands only
SURVEY_RMS_CONTEXT_ARCSEC = {
    "panstarrs_class_well_observed": (0.12, 0.25),
    "modern_ccd_survey_typical": (0.25, 0.50),
    "mixed_survey_class": (0.50, 0.80),
    "older_photographic_class": (1.0, 3.0),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pct(xs: list[float], p: float) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    if len(s) == 1:
        return float(s[0])
    k = (len(s) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(s[int(k)])
    return float(s[f] * (c - k) + s[c] * (k - f))


def _median(xs: list[float]) -> float | None:
    return float(statistics.median(xs)) if xs else None


def _mean(xs: list[float]) -> float | None:
    return float(statistics.mean(xs)) if xs else None


def kepler_n(a: float) -> float:
    return N_DEG_SCALE / (a**1.5)


def parse_mpcorb_classical(line: str) -> dict | None:
    """Parse orbital elements + classical quality fields from one MPCORB line."""
    if len(line) < 141:
        return None
    # skip header-ish
    if line.startswith("Des") or line.startswith("-----") or line.startswith("Number"):
        return None
    try:
        a = float(line[92:103].strip())
        e = float(line[70:79].strip())
        i = float(line[59:68].strip())
        n = float(line[80:91].strip())
    except ValueError:
        return None
    if a <= 0 or n <= 0 or e < 0 or e >= 1.5:
        return None

    u_raw = line[105:106].strip() if len(line) > 105 else ""
    u_int: int | None
    u_flag: str | None = None
    if u_raw.isdigit():
        u_int = int(u_raw)
    elif u_raw in {"D", "E", "F"}:
        u_int = None
        u_flag = u_raw
    else:
        u_int = None
        u_flag = u_raw or None

    rms: float | None = None
    try:
        rs = line[137:141].strip()
        if rs:
            rms = float(rs)
    except ValueError:
        rms = None

    n_obs: int | None = None
    n_opp: int | None = None
    try:
        os_ = line[117:122].strip()
        if os_:
            n_obs = int(os_)
    except ValueError:
        pass
    try:
        op = line[123:126].strip()
        if op:
            n_opp = int(op)
    except ValueError:
        pass

    H = None
    try:
        hs = line[8:13].strip()
        if hs:
            H = float(hs)
    except ValueError:
        H = None

    flags_hex = line[161:165].strip() if len(line) >= 165 else ""
    neo = False
    if flags_hex:
        try:
            fl = int(flags_hex, 16)
            neo = bool(fl & 2048)
        except ValueError:
            pass

    q = a * (1.0 - e)
    n_kep = kepler_n(a)
    # Fractional |n_catalog - n_kepler| / n_catalog  (dimensionless)
    frac_dn = abs(n_kep - n) / max(abs(n), 1e-15)
    # Absolute residual in mean motion (deg/day)
    abs_dn = abs(n_kep - n)

    # regime
    if neo or q < 1.3:
        regime = "neo"
    elif a > 30.0:
        regime = "distant"
    elif 2.0 < a < 3.5:
        regime = "main_belt"
    elif 3.5 <= a <= 5.5:
        regime = "outer_belt"
    else:
        regime = "other"

    return {
        "des": line[0:7].strip(),
        "a": a,
        "e": e,
        "i": i,
        "n": n,
        "H": H,
        "q": q,
        "neo": neo,
        "regime": regime,
        "U": u_int,
        "U_flag": u_flag,
        "rms_arcsec": rms,
        "n_obs": n_obs,
        "n_opp": n_opp,
        "frac_dn_over_n": frac_dn,
        "abs_dn_deg_day": abs_dn,
        "kepler_error_pct": 100.0 * frac_dn,
    }


def iter_rows(path: Path, max_rows: int = 0):
    opener = gzip.open if path.suffix == ".gz" else open
    n = 0
    with opener(path, "rt", encoding="latin-1", errors="replace") as f:  # type: ignore[arg-type]
        for line in f:
            row = parse_mpcorb_classical(line)
            if not row:
                continue
            yield row
            n += 1
            if max_rows and n >= max_rows:
                break


def _stats(xs: list[float]) -> dict[str, Any]:
    if not xs:
        return {"count": 0}
    return {
        "count": len(xs),
        "min": min(xs),
        "p05": _pct(xs, 5),
        "p25": _pct(xs, 25),
        "median": _median(xs),
        "p75": _pct(xs, 75),
        "p95": _pct(xs, 95),
        "p99": _pct(xs, 99),
        "mean": _mean(xs),
        "max": max(xs),
    }


def build(max_rows: int = 0) -> dict:
    gz = RAW / "MPCORB.DAT.gz"
    dat = RAW / "MPCORB.DAT"
    src = gz if gz.exists() else dat
    if not src.exists():
        raise FileNotFoundError("Missing vendor/mpcorb/MPCORB.DAT — run ingest_mpcorb_catalog.py")

    rms_all: list[float] = []
    frac_all: list[float] = []
    abs_dn_all: list[float] = []
    u_counts: Counter[str] = Counter()
    n_obs_all: list[int] = []
    n_opp_all: list[int] = []

    by_regime: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    by_u: dict[str, list[float]] = defaultdict(list)
    by_obs_tier: dict[str, list[float]] = defaultdict(list)

    n_obj = 0
    n_with_rms = 0
    n_with_u = 0

    for row in iter_rows(src, max_rows=max_rows):
        n_obj += 1
        reg = row["regime"]
        frac_all.append(row["frac_dn_over_n"])
        abs_dn_all.append(row["abs_dn_deg_day"])
        by_regime[reg]["frac_dn"].append(row["frac_dn_over_n"])
        by_regime[reg]["kepler_pct"].append(row["kepler_error_pct"])

        if row["rms_arcsec"] is not None and row["rms_arcsec"] >= 0:
            n_with_rms += 1
            r = float(row["rms_arcsec"])
            rms_all.append(r)
            by_regime[reg]["rms_arcsec"].append(r)
            if row["U"] is not None:
                by_u[str(row["U"])].append(r)
            if row["n_obs"] is not None:
                no = row["n_obs"]
                n_obs_all.append(no)
                if no < 10:
                    tier = "obs_lt_10"
                elif no < 50:
                    tier = "obs_10_49"
                elif no < 200:
                    tier = "obs_50_199"
                elif no < 1000:
                    tier = "obs_200_999"
                else:
                    tier = "obs_ge_1000"
                by_obs_tier[tier].append(r)

        if row["U"] is not None:
            n_with_u += 1
            u_counts[str(row["U"])] += 1
        elif row["U_flag"]:
            u_counts[f"flag_{row['U_flag']}"] += 1
        else:
            u_counts["missing"] += 1

        if row["n_opp"] is not None:
            n_opp_all.append(row["n_opp"])

    # Load FSOT benchmark residual for dual-metric board (if present)
    fsot_bench = ROOT / "data" / "mpcorb_fsot_benchmark.json"
    fsot_meta: dict[str, Any] = {}
    if fsot_bench.is_file():
        try:
            fb = json.loads(fsot_bench.read_text(encoding="utf-8"))
            fsot_meta = {
                "pooled_median_error_pct": fb.get("pooled_median_error_pct")
                or fb.get("median_error_pct"),
                "record_count": fb.get("record_count"),
                "mpcorb_object_count": fb.get("mpcorb_object_count"),
                "fsot_structural_median_error_pct": fb.get("fsot_structural_median_error_pct"),
                "catalog_stats": fb.get("catalog_stats"),
                "note": (
                    "FSOT residual % is a separate metric (seed engine / channel stack). "
                    "Classical RMS arcsec is the field-standard residual unit."
                ),
            }
        except Exception:
            pass

    # How catalog RMS compares to survey-class bands (counts, not claims of superiority)
    band_counts = {}
    if rms_all:
        for name, (lo, hi) in SURVEY_RMS_CONTEXT_ARCSEC.items():
            band_counts[name] = sum(1 for r in rms_all if lo <= r < hi)
        band_counts["sub_0_12_arcsec"] = sum(1 for r in rms_all if r < 0.12)
        band_counts["ge_1_arcsec"] = sum(1 for r in rms_all if r >= 1.0)

    regime_summary = {}
    for reg, series in sorted(by_regime.items()):
        regime_summary[reg] = {
            "n_rms": len(series.get("rms_arcsec") or []),
            "rms_arcsec": _stats(series.get("rms_arcsec") or []),
            "frac_dn_over_n": _stats(series.get("frac_dn") or []),
            "kepler_error_pct": _stats(series.get("kepler_pct") or []),
        }

    obs_tier_summary = {
        tier: _stats(xs) for tier, xs in sorted(by_obs_tier.items(), key=lambda x: x[0])
    }
    u_rms_summary = {
        u: _stats(xs) for u, xs in sorted(by_u.items(), key=lambda x: (len(x[0]), x[0]))
    }

    doc = {
        "generated_at": _now(),
        "version": "1.0",
        "source_path": str(src.relative_to(ROOT)).replace("\\", "/"),
        "metric_definitions": {
            "rms_arcsec": (
                "MPCORB orbit-fit r.m.s. residual in arcseconds — classical "
                "astrometric O–C RMS stored by the MPC for each object."
            ),
            "U": (
                "MPC uncertainty parameter 0–9 (0 best). Special flags D/E/F when present."
            ),
            "frac_dn_over_n": (
                "Two-body Kepler consistency: |n_Kepler(a) − n_catalog| / n_catalog. "
                "Fractional element-level integrity check (not a free fit)."
            ),
            "kepler_error_pct": "100 × frac_dn_over_n (percent form of the same integrity check).",
            "fsot_pooled_pct": (
                "Separate metric from build_mpcorb_fsot_benchmark.py — zero-parameter "
                "FSOT channel/domain residual. Not a substitute for rms_arcsec."
            ),
            "not_included": (
                "Full epoch-by-epoch O–C re-reduction from raw observation files is "
                "not in MPCORB alone; that would require the observation archive."
            ),
        },
        "survey_rms_context_arcsec": SURVEY_RMS_CONTEXT_ARCSEC,
        "object_count": n_obj,
        "objects_with_rms": n_with_rms,
        "objects_with_U": n_with_u,
        "classical": {
            "rms_arcsec": _stats(rms_all),
            "rms_band_counts": band_counts,
            "U_distribution": dict(u_counts),
            "n_obs": _stats([float(x) for x in n_obs_all]),
            "n_opp": _stats([float(x) for x in n_opp_all]),
            "kepler_frac_dn_over_n": _stats(frac_all),
            "kepler_abs_dn_deg_day": _stats(abs_dn_all),
            "kepler_error_pct": _stats([100.0 * x for x in frac_all]),
            "by_regime": regime_summary,
            "rms_by_U": u_rms_summary,
            "rms_by_obs_tier": obs_tier_summary,
        },
        "fsot_companion_metric": fsot_meta,
        "dual_scoreboard": {
            "classical_median_rms_arcsec": _median(rms_all),
            "classical_p95_rms_arcsec": _pct(rms_all, 95) if rms_all else None,
            "classical_median_frac_dn_over_n": _median(frac_all),
            "fsot_pooled_median_error_pct": fsot_meta.get("pooled_median_error_pct"),
            "interpretation": (
                "Report both. Classical = field-standard arcsec / fractional integrity. "
                "FSOT = seed-engine catalog residual %. Different units, complementary claims."
            ),
        },
        "refresh": "python scripts/build_mpcorb_classical_metrics.py",
    }
    return doc


def write_md(doc: dict) -> None:
    cl = doc.get("classical") or {}
    rms = cl.get("rms_arcsec") or {}
    kep = cl.get("kepler_frac_dn_over_n") or {}
    kep_pct = cl.get("kepler_error_pct") or {}
    dual = doc.get("dual_scoreboard") or {}
    fsot = doc.get("fsot_companion_metric") or {}

    lines = [
        "# MPCORB classical metrics (field-standard)",
        "",
        f"*Generated {doc.get('generated_at')} · objects **{doc.get('object_count'):,}***",
        "",
        "Classical minor-planet work measures **astrometric O–C RMS in arcseconds**, "
        "orbit quality **U**, and element consistency — **not** a single pooled residual % "
        "across the whole catalog under one free-parameter-free operator.",
        "",
        "This report adds those standard metrics **on top of** the existing FSOT residual %.",
        "",
        "## Dual scoreboard",
        "",
        "| Metric | Value | Unit / meaning |",
        "|--------|------:|----------------|",
        f"| **Classical median RMS** | **{dual.get('classical_median_rms_arcsec')}** | arcsec (MPC orbit-fit O–C RMS) |",
        f"| Classical p95 RMS | {dual.get('classical_p95_rms_arcsec')} | arcsec |",
        f"| Classical median \|Δn\|/n (Kepler) | {dual.get('classical_median_frac_dn_over_n')} | fractional |",
        f"| Classical median Kepler error | {(kep_pct.get('median'))} | % of n |",
        f"| **FSOT pooled median residual** | **{dual.get('fsot_pooled_median_error_pct')}** | % (seed engine; separate metric) |",
        "",
        str(dual.get("interpretation") or ""),
        "",
        "## Classical RMS residual (arcsec)",
        "",
        f"Objects with RMS field: **{doc.get('objects_with_rms'):,}** / {doc.get('object_count'):,}",
        "",
        f"| Stat | RMS (arcsec) |",
        f"|------|-------------:|",
    ]
    for k in ("min", "p05", "p25", "median", "p75", "p95", "p99", "mean", "max"):
        if rms.get(k) is not None:
            lines.append(f"| {k} | {rms.get(k)} |")

    lines.extend(
        [
            "",
            "### Context bands (literature survey classes)",
            "",
            "Approximate modern survey RMS classes for **well-observed** objects "
            "(not a claim that every MPCORB object matches them):",
            "",
            "| Band | Arcsec | Count in catalog |",
            "|------|--------|-----------------:|",
        ]
    )
    for name, (lo, hi) in (doc.get("survey_rms_context_arcsec") or {}).items():
        c = (cl.get("rms_band_counts") or {}).get(name, 0)
        lines.append(f"| {name} ({lo}–{hi}) | {lo}–{hi} | {c} |")
    bc = cl.get("rms_band_counts") or {}
    lines.append(f"| sub-0.12 arcsec | <0.12 | {bc.get('sub_0_12_arcsec', 0)} |")
    lines.append(f"| ≥1 arcsec | ≥1 | {bc.get('ge_1_arcsec', 0)} |")

    lines.extend(
        [
            "",
            "## U (uncertainty parameter) distribution",
            "",
            "| U / flag | Count |",
            "|----------|------:|",
        ]
    )
    for u, c in sorted(
        (cl.get("U_distribution") or {}).items(),
        key=lambda x: (0, int(x[0])) if str(x[0]).isdigit() else (1, str(x[0])),
    ):
        lines.append(f"| {u} | {c} |")

    lines.extend(
        [
            "",
            "### Median RMS by U (where available)",
            "",
            "| U | n | median RMS (arcsec) | p95 |",
            "|---|--:|--------------------:|----:|",
        ]
    )
    for u, st in (cl.get("rms_by_U") or {}).items():
        if not st.get("count"):
            continue
        lines.append(
            f"| {u} | {st.get('count')} | {st.get('median')} | {st.get('p95')} |"
        )

    lines.extend(
        [
            "",
            "## RMS by observation count tier",
            "",
            "| Tier | n | median RMS | p95 |",
            "|------|--:|-----------:|----:|",
        ]
    )
    for tier, st in (cl.get("rms_by_obs_tier") or {}).items():
        lines.append(
            f"| {tier} | {st.get('count')} | {st.get('median')} | {st.get('p95')} |"
        )

    lines.extend(
        [
            "",
            "## Kepler element integrity (fractional Δn/n)",
            "",
            "Two-body check: mean motion from semi-major axis vs catalog `n`. "
            "Best objects in the literature reach fractional element precision at "
            "10⁻⁶–10⁻⁸; the full catalog has a long tail.",
            "",
            f"| Stat | \|Δn\|/n | as % |",
            f"|------|--------:|-----:|",
        ]
    )
    for k in ("median", "p95", "p99", "mean"):
        lines.append(
            f"| {k} | {kep.get(k)} | {kep_pct.get(k)} |"
        )

    lines.extend(
        [
            "",
            "## By orbital regime",
            "",
            "| Regime | n (rms) | med RMS (arcsec) | med Kepler % |",
            "|--------|--------:|-----------------:|-------------:|",
        ]
    )
    for reg, st in (cl.get("by_regime") or {}).items():
        rms_r = st.get("rms_arcsec") or {}
        kp = st.get("kepler_error_pct") or {}
        lines.append(
            f"| {reg} | {st.get('n_rms')} | {rms_r.get('median')} | {kp.get('median')} |"
        )

    lines.extend(
        [
            "",
            "## FSOT companion (unchanged metric)",
            "",
            f"- FSOT pooled median residual %: **{fsot.get('pooled_median_error_pct')}**",
            f"- FSOT structural median %: {fsot.get('fsot_structural_median_error_pct')}",
            f"- Objects (FSOT bench): {fsot.get('mpcorb_object_count')}",
            "",
            str(fsot.get("note") or ""),
            "",
            "## Metric definitions",
            "",
        ]
    )
    for k, v in (doc.get("metric_definitions") or {}).items():
        lines.append(f"- **{k}:** {v}")

    lines.extend(
        [
            "",
            "Refresh: `python scripts/build_mpcorb_classical_metrics.py`",
            "",
            "FSOT residual builder (separate): `python scripts/build_mpcorb_fsot_benchmark.py`",
            "",
        ]
    )
    text = "\n".join(lines).rstrip() + "\n"
    OUT_MD.write_text(text, encoding="utf-8")
    OUT_PRED_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRED_MD.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Classical MPCORB metrics (arcsec, U, Kepler)")
    ap.add_argument("--max-rows", type=int, default=0, help="0 = full catalog")
    args = ap.parse_args()
    print("Scanning MPCORB for classical metrics…")
    doc = build(max_rows=args.max_rows)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    dual = doc["dual_scoreboard"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_PRED_MD}")
    print(
        f"  n={doc['object_count']:,} rms_n={doc['objects_with_rms']:,} "
        f"median_rms={dual.get('classical_median_rms_arcsec')} arcsec "
        f"median_frac_dn={dual.get('classical_median_frac_dn_over_n')} "
        f"fsot_pooled%={dual.get('fsot_pooled_median_error_pct')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
