#!/usr/bin/env python3
"""Apply the refined dated-forecast playbook to frozen kills.

Does **not** rewrite issued JSON or restuff the public scoreboard. The 12
kills stay kills on the files that were issued. This is a playbook test:
would the loading M≥4.5 / quiet-hold / tide-headroom rules have converted
those misses, and which one still kills?

Input: results/dated_forecast_scores/KILL_AUTOPSY.json
Output: results/dated_forecast_scores/RULE_RETRO.json + RULE_RETRO.md
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
from fsot_earth_fluid_forecast import (  # noqa: E402
    POOF,
    f,
    surge_class_m,
    surge_issue_m,
)

SCORE_DIR = ROOT / "results" / "dated_forecast_scores"
PIN = "D1D38A"
LOADING = {"loading_suction", "post_poof_aftershock"}


def _eq(row: dict) -> dict:
    valve = str(row.get("valve") or "")
    new_expect = valve in LOADING
    new_mag = 4.5 if new_expect else 5.0
    n45 = int(row.get("n_m45_in_kernel") or 0)
    n5 = int(row.get("n_m5_in_kernel") or 0)
    biggest = row.get("biggest_in_kernel")
    if new_expect:
        converted = "hold" if n45 >= 1 else "kill"
        reason = (
            f"loading → expect M≥4.5; kernel had "
            f"{(biggest or {}).get('mag', 'none')}"
            if biggest
            else "loading → expect M≥4.5; no M≥4.5 in kernel"
        )
    else:
        converted = "kill" if n5 >= 1 else "hold"
        reason = (
            "released/steady → quiet hold (kill only if M≥5 shows); "
            f"n_M5={n5}"
        )
    return {
        "id": row.get("id"),
        "kind": "earthquake",
        "place": row.get("place"),
        "issued_expect": True,
        "issued_mag_min": row.get("mag_min"),
        "valve": valve,
        "new_expect": new_expect,
        "new_mag_min": new_mag,
        "converted": converted,
        "reason": reason,
        "biggest_in_kernel": biggest,
        "would_issue": True,
    }


def _wx(row: dict) -> dict:
    pres = float(row.get("pres_now") or 0)
    gst = float(row.get("gst_now") or 0)
    storm = pres < 1000.0 or gst >= 15.0
    quiet_clean = pres >= 1010.0 and gst < 8.0
    if storm:
        converted = "would_issue_storm"
        reason = "at-issue state is now a storm cell (pres<1000 or gst≥15)"
        would_issue = True
    elif quiet_clean:
        converted = "hold"
        reason = "at-issue state is clean quiet (pres≥1010 and gst<8)"
        would_issue = True
    else:
        converted = "would_not_issue"
        reason = (
            f"gap-zone quiet (pres={pres:.1f} hPa, gst={gst:.1f} m/s); "
            "new issuer skips 1000–1010 / 8–15"
        )
        would_issue = False
    return {
        "id": row.get("id"),
        "kind": "weather",
        "place": row.get("place"),
        "pres_now": pres,
        "gst_now": gst,
        "issued_expect_storm": False,
        "converted": converted,
        "reason": reason,
        "would_issue": would_issue,
    }


def _tide(row: dict) -> dict:
    resid = float(row.get("residual_now_m") or 0)
    window_max = float(row.get("max_in_window_m") or 0)
    score_thr = surge_class_m()
    issue_thr = surge_issue_m()
    if resid >= issue_thr:
        converted = "hold" if window_max >= score_thr else "kill"
        reason = (
            f"snapshot {resid:.3f} m ≥ issue bar {issue_thr:.3f} m; "
            f"window max {window_max:.3f} vs score bar {score_thr:.3f}"
        )
        would_issue = True
    else:
        converted = "would_not_issue"
        reason = (
            f"snapshot {resid:.3f} m < issue bar POOF·(1+POOF)={issue_thr:.3f} m "
            f"(score bar still POOF={score_thr:.3f} m)"
        )
        would_issue = False
    return {
        "id": row.get("id"),
        "kind": "tide",
        "place": row.get("place"),
        "residual_now_m": resid,
        "max_in_window_m": window_max,
        "score_threshold_m": score_thr,
        "issue_threshold_m": issue_thr,
        "issued_expect_surge": True,
        "converted": converted,
        "reason": reason,
        "would_issue": would_issue,
    }


def main() -> int:
    src = SCORE_DIR / "KILL_AUTOPSY.json"
    if not src.is_file():
        print("missing KILL_AUTOPSY.json — run autopsy_dated_forecast_kills.py first")
        return 1
    doc = json.loads(src.read_text(encoding="utf-8"))
    rows = []
    for a in doc.get("autopsies") or []:
        kind = str(a.get("kind") or "")
        if kind == "earthquake":
            rows.append(_eq(a))
        elif kind == "weather":
            rows.append(_wx(a))
        elif kind == "tide":
            rows.append(_tide(a))
        else:
            rows.append(
                {
                    "id": a.get("id"),
                    "kind": kind,
                    "converted": "skipped",
                    "reason": "unknown kind",
                }
            )

    counts: dict[str, int] = {}
    for r in rows:
        counts[str(r.get("converted"))] = counts.get(str(r.get("converted")), 0) + 1

    remaining_kills = [r for r in rows if r.get("converted") == "kill"]
    converted_holds = [r for r in rows if r.get("converted") == "hold"]
    skipped_issue = [r for r in rows if r.get("converted") == "would_not_issue"]

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": PIN,
        "policy": [
            "do_not_rewrite_issued_json",
            "do_not_restuff_public_scoreboard",
            "playbook_test_only",
        ],
        "poof": f(POOF),
        "surge_score_m": surge_class_m(),
        "surge_issue_m": surge_issue_m(),
        "n_input_kills": len(rows),
        "counts": counts,
        "n_converted_hold": len(converted_holds),
        "n_still_kill": len(remaining_kills),
        "n_would_not_issue": len(skipped_issue),
        "rows": rows,
        "still_kill": remaining_kills,
        "note": (
            "Frozen issue scores stay kill. This file asks: under the playbook "
            "encoded after the autopsy (loading M≥4.5 / released-steady quiet / "
            "quiet only if pres≥1010 and gst<8 / surge issue bar POOF·(1+POOF)), "
            "which of those 12 would still be a miss?"
        ),
    }
    SCORE_DIR.mkdir(parents=True, exist_ok=True)
    (SCORE_DIR / "RULE_RETRO.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    lines = [
        "# Playbook retrospective — 12 frozen kills under the refined rule",
        "",
        f"*Generated {out['generated_at']} · pin {PIN}*",
        "",
        "Issued JSON is **still frozen**. Public scoreboard of those files stays",
        f"**{len(rows)} kills**. This is not a restuff. It asks whether the",
        "playbook encoded after the autopsy would have issued a different call.",
        "",
        f"POOF = {f(POOF):.4f} m · score bar = POOF · issue bar = POOF·(1+POOF) = "
        f"**{surge_issue_m():.4f} m**.",
        "",
        f"Converted to hold **{len(converted_holds)}** · still kill **{len(remaining_kills)}** · "
        f"would not issue **{len(skipped_issue)}**.",
        "",
        "## Earthquakes",
        "",
        "| ID | Place | Valve | New call | Converted | Why |",
        "|----|-------|-------|----------|-----------|-----|",
    ]
    for r in rows:
        if r.get("kind") != "earthquake":
            continue
        call = (
            f"M≥{r['new_mag_min']} expect={r['new_expect']}"
        )
        lines.append(
            f"| `{r['id']}` | {r.get('place')} | **{r.get('valve')}** | {call} | "
            f"**{r.get('converted')}** | {r.get('reason')} |"
        )

    lines += [
        "",
        "## Weather quiet",
        "",
        "| ID | Buoy | At issue | Converted | Why |",
        "|----|------|----------|-----------|-----|",
    ]
    for r in rows:
        if r.get("kind") != "weather":
            continue
        lines.append(
            f"| `{r['id']}` | {r.get('place')} | "
            f"{r.get('pres_now'):.1f} hPa / {r.get('gst_now'):.1f} m/s | "
            f"**{r.get('converted')}** | {r.get('reason')} |"
        )

    lines += [
        "",
        "## Tide",
        "",
        "| ID | Station | Snapshot | Window max | Converted | Why |",
        "|----|---------|---------:|-----------:|-----------|-----|",
    ]
    for r in rows:
        if r.get("kind") != "tide":
            continue
        lines.append(
            f"| `{r['id']}` | {r.get('place')} | {r.get('residual_now_m'):.3f} m | "
            f"{r.get('max_in_window_m'):.3f} m | **{r.get('converted')}** | "
            f"{r.get('reason')} |"
        )

    lines += [
        "",
        "## What still kills",
        "",
    ]
    if remaining_kills:
        for r in remaining_kills:
            lines.append(
                f"- `{r['id']}` ({r.get('place')}): {r.get('reason')}"
            )
        lines.append("")
        lines.append(
            "Scotia Sea is the remaining EQ miss: a loading cell with no M≥4.5 "
            "inside 39 km. Ocean catalog is sparse; do not retune kernel km or ρ "
            "to swallow it. Next issues keep the same kernel; a loading ocean "
            "cell that stays quiet is an honest kill."
        )
    else:
        lines.append("None of the 12 would still kill under the refined playbook.")

    lines += [
        "",
        "## What we will not do",
        "",
        "- Rewrite issued JSON.",
        "- Change the public hold/kill counts on frozen files.",
        "- Retune ρ, POOF, or kernel km to swallow Scotia Sea.",
        "",
        "Refresh: `python scripts/retro_dated_forecast_rule.py`",
        "",
        "Related: [`KILL_AUTOPSY.md`](KILL_AUTOPSY.md) · "
        "[`../../docs/WEATHER_MONITORING_APPROACH.md`](../../docs/WEATHER_MONITORING_APPROACH.md)",
        "",
    ]
    (SCORE_DIR / "RULE_RETRO.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        f"retro n={len(rows)} hold={len(converted_holds)} "
        f"still_kill={len(remaining_kills)} would_not_issue={len(skipped_issue)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
