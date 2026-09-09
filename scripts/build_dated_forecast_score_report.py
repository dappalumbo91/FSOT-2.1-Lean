#!/usr/bin/env python3
"""Human table of dated-forecast scores. Does not rewrite issued JSON."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE_DIR = ROOT / "results" / "dated_forecast_scores"
ISSUE_DIR = ROOT / "predictions" / "dated_forecasts"
OUT_MD = SCORE_DIR / "REPORT.md"


def _kind_of(pred_id: str, issues: dict[str, dict]) -> str:
    for doc in issues.values():
        for fc in doc.get("forecasts") or []:
            if fc.get("id") == pred_id:
                return str(fc.get("kind") or "")
    if "EQ" in pred_id:
        return "earthquake"
    if "WX" in pred_id:
        return "weather"
    if "SOL" in pred_id:
        return "solar"
    if "VOLC" in pred_id:
        return "volcanic"
    if "TIDE" in pred_id:
        return "tide"
    if "HYDRO" in pred_id:
        return "hydrology"
    return "?"


def main() -> int:
    issues = {}
    for p in ISSUE_DIR.glob("*_issue.json"):
        issues[p.name] = json.loads(p.read_text(encoding="utf-8"))
    score_files = sorted(
        p for p in SCORE_DIR.glob("*_score.json") if p.name != "LATEST.json"
    )
    ts = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Dated fluid-forecast scores",
        "",
        f"*Scored rollup {ts} · pin D1D38A*",
        "",
        "Issued forecast JSON is **not** rewritten. This is `results/` only.",
        "EQ / hydro windows close **2026-09-01**. Volcanic **2026-09-08**.",
        "",
        "Refresh: `python scripts/score_earth_fluid_forecasts.py` then this script.",
        "",
    ]
    tot = {"hold": 0, "kill": 0, "awaiting": 0}
    for path in score_files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        rows = doc.get("rows") or []
        n_h = sum(1 for r in rows if r.get("result") == "hold")
        n_k = sum(1 for r in rows if r.get("result") == "kill")
        n_a = sum(1 for r in rows if r.get("result") == "awaiting")
        tot["hold"] += n_h
        tot["kill"] += n_k
        tot["awaiting"] += n_a
        lines += [
            f"## `{path.name}`",
            "",
            f"hold **{n_h}** · kill **{n_k}** · awaiting **{n_a}**",
            "",
            "| ID | Kind | Result | Detail |",
            "|----|------|--------|--------|",
        ]
        for r in rows:
            rid = str(r.get("id") or "")
            kind = _kind_of(rid, issues)
            res = str(r.get("result") or "")
            detail = r.get("notes") or ""
            if r.get("buoy_id"):
                detail = (
                    f"buoy {r.get('buoy_id')} expect_storm={r.get('expect_storm')} "
                    f"saw_storm={r.get('saw_storm')} n={r.get('n_obs')}"
                )
            if r.get("station_id"):
                detail = (
                    f"CO-OPS {r.get('station_id')} expect_surge={r.get('expect_surge')} "
                    f"max_resid={r.get('max_residual_m')} m n={r.get('n_hours')}"
                )
            if r.get("kp_max") is not None:
                detail = f"Kp_max={r.get('kp_max')} expect_ge5={r.get('expect_kp_ge_5')}"
            if r.get("site_id"):
                detail = (
                    f"NWIS {r.get('site_id')} expect_high={r.get('expect_high_flow')} "
                    f"mean={r.get('mean_cfs')} cfs"
                )
            lines.append(f"| `{rid}` | {kind} | **{res}** | {detail} |")
        lines.append("")
    lines += [
        "## Totals (all issues)",
        "",
        f"hold **{tot['hold']}** · kill **{tot['kill']}** · awaiting **{tot['awaiting']}**",
        "",
        "Tide hours are clipped to `valid_from`–`valid_to` (not the whole end calendar day).",
        "Quiet-weather kills use the issued kill_if (pres<1005 or gust≥12). Do not rewrite issues.",
        "New issues skip the 1000–1005 hPa / 12–15 m/s gap (doomed quiet) and skip lake `other` buoys.",
        "Hydro IDs on **new** issues use the 2026-09-07 NWIS map "
        "(`06934500` Missouri at Hermann). Issued JSON keeps the old IDs.",
        "",
        "## Remaining awaiting (missing catalogs, not a retune)",
        "",
        "These cells closed but the public archive was empty in-window. "
        "Do not rewrite the issue. Do not invent a residual.",
        "",
        "| ID | Catalog | Why still awaiting |",
        "|----|---------|--------------------|",
    ]
    awaiting_rows = []
    for path in score_files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for r in doc.get("rows") or []:
            if r.get("result") != "awaiting":
                continue
            awaiting_rows.append(r)
    if not awaiting_rows:
        lines.append("| *(none)* | | |")
    else:
        for r in awaiting_rows:
            lines.append(
                f"| `{r.get('id')}` | {_kind_of(str(r.get('id') or ''), issues)} | {r.get('notes') or 'catalog empty'} |"
            )
    lines += [
        "",
        "## 2026-09-01 playbook — honest loading misses (not a kernel retune)",
        "",
        "The 09-01 issue already used `expect_event` only on loading/post-POOF. "
        "Two ocean loading cells stayed quiet inside 39 km. Same grammar as Scotia Sea.",
        "",
        "| ID | Place | Valve | Result |",
        "|----|-------|-------|--------|",
        "| `FCAST-EQ-20260901T0032-05` | 32 km SSW of Honchō, Japan | loading · M≥4.5 | **kill** (no M≥4.5 in kernel) |",
        "| `FCAST-EQ-20260901T0032-08` | Kermadec Islands, New Zealand | loading · M≥4.5 | **kill** (no M≥4.5 in kernel) |",
        "| `FCAST-HYDRO-20260901T0032-01` | Potomac `01646500` (correct ID) | loading | **kill** (window mean dropped) |",
        "",
        "Do not retune kernel km, POOF, or ρ to swallow ocean-catalog sparse cells.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"  hold={tot['hold']} kill={tot['kill']} awaiting={tot['awaiting']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
