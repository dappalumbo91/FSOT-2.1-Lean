#!/usr/bin/env python3
"""Rank prediction watches by nearest public data-drop time.

Does NOT freeze the model. Outputs a living priority list so you can monitor
as surveys drop while development continues. Git commit timestamps remain the
legal/scientific prereg clock for anything already committed.

Outputs:
  predictions/nearest_data_drop_ranking.json
  predictions/reports/NEAREST_DATA_DROPS.md
  Optional copy to G:/FSOT-PublicData/anomaly_observables/prediction_monitor_logs/
"""

from __future__ import annotations

import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "predictions" / "nearest_data_drop_ranking.json"
OUT_MD = ROOT / "predictions" / "reports" / "NEAREST_DATA_DROPS.md"
EXTERNAL_LOG = Path(
    r"G:\FSOT-PublicData\anomaly_observables\prediction_monitor_logs"
)

# As-of research snapshot 2026-08-06. Update windows as facilities announce.
# "as_of" is today's session date for ranking.
DROPS = [
    {
        "id": "RUBIN-EDP2-COMPLETE",
        "title": "Rubin LSST Early DP2 complete (visit/diff images)",
        "window_start": "2026-10-01",
        "window_end": "2026-12-31",
        "certainty": "target_window",
        "pred_ids": ["PRED-044", "PRED-002", "PRED-S8"],
        "atlas_kinds": ["residual_hold", "sector_portfolio_hold"],
        "sectors": ["cosmology", "astro_gw"],
        "why_monitor": "Earliest Stage-IV imaging pathfinder for structure/S8-class tests.",
        "priority_note": "Closest calendar cluster after now among named survey drops.",
    },
    {
        "id": "EUCLID-DR1-FOUNDATION",
        "title": "Euclid DR1-Foundation (raw/calibrated ~1900 deg²)",
        "window_start": "2026-11-12",
        "window_end": "2026-11-12",
        "certainty": "announced_date",
        "pred_ids": ["PRED-042", "PRED-043", "PRED-002", "PRED-wa"],
        "atlas_kinds": ["multi_tool_h0", "residual_hold"],
        "sectors": ["cosmology"],
        "why_monitor": (
            "Hard date on ESA timeline (12 Nov 2026). Foundation is imaging/catalogs; "
            "full weak-lensing cosmology products follow mid-2027. Still the cleanest "
            "named calendar event for FSOT cosmology locks."
        ),
        "priority_note": "Best single hard-date cosmology drop on the public calendar.",
    },
    {
        "id": "LVK-O4-REMAINDER",
        "title": "LVK remaining O4 open data / catalog updates",
        "window_start": "2026-12-01",
        "window_end": "2026-12-31",
        "certainty": "expected_window",
        "pred_ids": ["PRED-048"],
        "atlas_kinds": ["residual_hold", "scalar_lock"],
        "sectors": ["astro_gw"],
        "why_monitor": "GWTC-5.0 already out (May 2026); remainder expected ~Dec 2026.",
    },
    {
        "id": "LVK-O5-START",
        "title": "LVK O5 observing run start",
        "window_start": "2026-08-15",
        "window_end": "2026-11-30",
        "certainty": "envisioned",
        "pred_ids": ["PRED-048"],
        "atlas_kinds": ["residual_hold"],
        "sectors": ["astro_gw"],
        "why_monitor": "Late summer/fall 2026 envisioned; live alerts before full catalogs.",
    },
    {
        "id": "EUCLID-DR1-COMPLETE",
        "title": "Euclid DR1 complete (WL / clustering science products)",
        "window_start": "2027-06-01",
        "window_end": "2027-09-30",
        "certainty": "mid_year_target",
        "pred_ids": ["PRED-042", "PRED-043", "PRED-S8", "PRED-wa"],
        "atlas_kinds": ["multi_tool_h0"],
        "sectors": ["cosmology"],
        "why_monitor": "Where S8/w_a kill criteria get their strongest posterior tests.",
    },
    {
        "id": "DESI-ROLLING",
        "title": "DESI public BAO / cosmology catalog refreshes",
        "window_start": "2026-08-06",
        "window_end": "2027-12-31",
        "certainty": "continuous",
        "pred_ids": ["PRED-046", "PRED-001", "PRED-wa"],
        "atlas_kinds": ["multi_tool_h0"],
        "sectors": ["cosmology"],
        "why_monitor": "Already dropping; check on every public cosmology paper.",
    },
    {
        "id": "JWST-LOCAL-H0-ROLLING",
        "title": "JWST / CCHP / SH0ES local ladder papers",
        "window_start": "2026-08-06",
        "window_end": "2027-12-31",
        "certainty": "continuous",
        "pred_ids": [
            "PRED-051",
            "PRED-H0-freedman_jwst",
            "PRED-H0-sh0es_jwst",
        ],
        "atlas_kinds": ["h0_sightline_host", "multi_tool_h0"],
        "sectors": ["cosmology"],
        "why_monitor": (
            "No single drop day — but every CCHP/SH0ES/JWST host paper is a per-host "
            "kill check against sightline predictions."
        ),
    },
    {
        "id": "CHIME-FRB-ROLLING",
        "title": "CHIME/FRB catalog updates",
        "window_start": "2026-08-06",
        "window_end": "2027-12-31",
        "certainty": "continuous",
        "pred_ids": ["PRED-052", "PRED-FRB-DM-excess"],
        "atlas_kinds": ["residual_hold"],
        "sectors": ["astro_gw", "cosmology"],
        "why_monitor": "DM excess class already in contested panel.",
    },
    {
        "id": "OPEN-SCIENCE-ROLLING",
        "title": "Open bio/earth/materials panel refreshes (GBIF, NCEI, PubChem…)",
        "window_start": "2026-08-06",
        "window_end": "2027-12-31",
        "certainty": "continuous",
        "pred_ids": ["PRED-054", "PRED-055"],
        "atlas_kinds": ["residual_hold", "scalar_lock", "sector_portfolio_hold"],
        "sectors": ["bio_med", "earth_climate", "materials_chem"],
        "why_monitor": (
            "Not a single press-release day — but residual/scalar locks across 400+ "
            "domains can be re-scored anytime panels rebuild."
        ),
    },
]


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def _days_until(start: str, today: date) -> int:
    s = _parse(start)
    return (s - today).days


def build(today: date | None = None) -> dict:
    today = today or datetime.now(timezone.utc).date()
    ranked = []
    for drop in DROPS:
        days = _days_until(drop["window_start"], today)
        # continuous / already open → rank by urgency of monitoring cadence
        if drop["certainty"] == "continuous" or days < 0:
            score = 0 if drop["certainty"] == "continuous" else days
            status = "open_now" if days <= 0 or drop["certainty"] == "continuous" else "upcoming"
        else:
            score = days
            status = "upcoming"
        ranked.append(
            {
                **drop,
                "as_of": today.isoformat(),
                "days_until_window_start": days,
                "status": status,
                "rank_score": score if score >= 0 else 0,
            }
        )

    # Sort: open continuous first by monitoring value, then soonest hard dates
    certainty_tier = {
        "announced_date": 0,
        "target_window": 1,
        "expected_window": 2,
        "envisioned": 3,
        "mid_year_target": 4,
        "continuous": 5,
    }

    def sort_key(r: dict):
        # Prefer hard announced dates, then target windows, soonest first
        if r["status"] == "upcoming" or r["certainty"] != "continuous":
            return (
                certainty_tier.get(r["certainty"], 9),
                max(r["days_until_window_start"], 0),
                r["id"],
            )
        return (5, 0, r["id"])

    ranked.sort(key=sort_key)
    for i, r in enumerate(ranked, 1):
        r["rank"] = i

    nearest_hard = next(
        (
            r
            for r in ranked
            if r["certainty"] == "announced_date" and r["days_until_window_start"] >= 0
        ),
        next(
            (
                r
                for r in ranked
                if r["certainty"] in {"announced_date", "target_window"}
                and r["days_until_window_start"] >= 0
            ),
            ranked[0],
        ),
    )

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "as_of_date": today.isoformat(),
        "policy": {
            "do_not_freeze_model_while_monitoring": True,
            "prereg_clock": (
                "Git commit timestamps on GitHub are the preregistration clock for "
                "any prediction already pushed. New work can continue on main; "
                "when a survey drops, log outcome against the commit SHA that "
                "contained the prediction — do not retune that SHA's predicted values."
            ),
            "informal_prior_calls": (
                "Pre-formal X/public calls (e.g. Euclid characteristics, I3 Atlas "
                "comet morphology) are historical context. Formal scoreboard uses "
                "repo commits + this ranking only."
            ),
            "separate_predictions_repo": (
                "Recommended: keep predictions *in* the monorepo for pin/engine "
                "integrity; optionally add a thin public mirror repo that only "
                "tracks prediction JSON + outcomes. Full multiprover stays here."
            ),
        },
        "nearest_hard_calendar_drop": {
            "id": nearest_hard["id"],
            "title": nearest_hard["title"],
            "days_until_window_start": nearest_hard["days_until_window_start"],
            "window_start": nearest_hard["window_start"],
            "pred_ids": nearest_hard["pred_ids"],
            "why": nearest_hard.get("why_monitor"),
        },
        "ranked_drops": ranked,
        "monitor_commands": [
            "python scripts/rank_nearest_data_drops.py",
            "python scripts/run_prediction_monitor.py",
            "python scripts/run_prediction_monitor.py --online",
            "python scripts/build_domain_prediction_atlas.py",
        ],
    }
    return doc


def write_md(doc: dict) -> None:
    nh = doc.get("nearest_hard_calendar_drop") or {}
    lines = [
        "# Nearest data drops (monitor priority)",
        "",
        f"*As of {doc.get('as_of_date')} · generated {doc.get('generated_at')}*",
        "",
        "## Closest hard calendar event",
        "",
        f"**{nh.get('title')}**  ",
        f"ID: `{nh.get('id')}` · window start **{nh.get('window_start')}** · "
        f"**{nh.get('days_until_window_start')} days** from as-of date  ",
        f"Linked PREDs: {', '.join(f'`{p}`' for p in (nh.get('pred_ids') or []))}  ",
        "",
        str(nh.get("why") or ""),
        "",
        "## Policy (WIP model — do not freeze development)",
        "",
        str((doc.get("policy") or {}).get("do_not_freeze_model_while_monitoring")),
        "",
        str((doc.get("policy") or {}).get("prereg_clock") or ""),
        "",
        str((doc.get("policy") or {}).get("separate_predictions_repo") or ""),
        "",
        "## Full ranking",
        "",
        "| Rank | Drop | Window start | Days | Certainty | Status |",
        "|-----:|------|--------------|-----:|-----------|--------|",
    ]
    for r in doc.get("ranked_drops") or []:
        lines.append(
            f"| {r['rank']} | {r['title']} | {r['window_start']} | "
            f"{r['days_until_window_start']} | {r['certainty']} | {r['status']} |"
        )
    lines.extend(
        [
            "",
            "Refresh: `python scripts/rank_nearest_data_drops.py`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    doc = build()
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    write_md(doc)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    nh = doc["nearest_hard_calendar_drop"]
    print(
        f"  NEAREST HARD: {nh['id']} in {nh['days_until_window_start']} days "
        f"({nh['window_start']})"
    )
    # Mirror log to external drive if present
    if EXTERNAL_LOG.parent.is_dir():
        EXTERNAL_LOG.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = EXTERNAL_LOG / f"nearest_data_drops_{stamp}.json"
        shutil.copy2(OUT_JSON, dest)
        shutil.copy2(OUT_JSON, EXTERNAL_LOG / "nearest_data_drops_latest.json")
        print(f"  mirrored to {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
