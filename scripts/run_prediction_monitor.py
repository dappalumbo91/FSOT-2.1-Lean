#!/usr/bin/env python3
"""FSOT prediction monitor — track prereg locks vs near/future data drops.

Offline by default (reads repo artifacts). Optional --online probes public
endpoints (GWOSC, etc.) when network is available.

Schedule (example):
  # weekly offline:
  python scripts/run_prediction_monitor.py
  # fortnightly online:
  python scripts/run_prediction_monitor.py --online

Outputs:
  data/prediction_monitor_report.json
  data/publication/PREDICTION_MONITOR.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

REGISTRY = ROOT / "data" / "prediction_monitor_registry.yaml"
PREREG = ROOT / "data" / "preregistered_predictions_manifest.yaml"
FREEZE = ROOT / "data" / "toe_prereg_freeze.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"
CONTESTED = ROOT / "data" / "contested_observables_closure.json"
FUTURE = ROOT / "data" / "contested_future_observation_ledger.json"
OUT_JSON = ROOT / "data" / "prediction_monitor_report.json"
OUT_MD = ROOT / "data" / "publication" / "PREDICTION_MONITOR.md"

GREEN_CEILING = 0.5


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        import yaml

        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _margin_index(margin: dict) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for row in margin.get("all_domains") or []:
        dom = str(row.get("domain") or "")
        f = str(row.get("file") or "")
        if dom:
            idx[dom.lower()] = row
            idx[dom] = row
        if f:
            stem = Path(f).stem.replace("_benchmark", "")
            idx[stem.lower()] = row
            idx[f.lower()] = row
    return idx


def _find_panel(idx: dict[str, dict], hint: str | None) -> dict | None:
    if not hint:
        return None
    keys = [
        hint,
        hint.lower(),
        hint.replace("_", " "),
        hint.replace("-", "_"),
    ]
    for k in keys:
        if k in idx:
            return idx[k]
        for ik, row in idx.items():
            if hint.lower() in str(ik).lower():
                return row
    return None


def _panel_status(row: dict | None) -> dict[str, Any]:
    if not row:
        return {
            "status": "no_local_panel",
            "pooled_median_error_pct": None,
            "green_gate_pass": None,
        }
    med = row.get("official_pooled_median_error_pct")
    if med is None:
        med = row.get("pooled_median_error_pct")
    green = row.get("green_gate_pass")
    if green is None and med is not None:
        green = float(med) <= GREEN_CEILING
    st = "green_hold" if green else "gate_fail"
    if med is not None and float(med) > GREEN_CEILING * 0.7 and green:
        st = "green_watch"  # approaching ceiling
    return {
        "status": st,
        "pooled_median_error_pct": med,
        "green_gate_pass": green,
        "domain": row.get("domain"),
        "file": row.get("file"),
    }


def _probe_gwosc() -> dict[str, Any]:
    """Lightweight public GWOSC catalog count (optional online)."""
    url = "https://www.gwosc.org/eventapi/json/GWTC/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FSOT-prediction-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        events = data.get("events") or {}
        n = len(events) if isinstance(events, dict) else int(data.get("numRows") or 0)
        return {"ok": True, "event_count": n, "source": url}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as e:
        return {"ok": False, "error": str(e), "source": url}


def _probe_http_head(url: str) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "FSOT-prediction-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return {"ok": True, "status": getattr(resp, "status", None), "url": url}
    except Exception as e:
        # Some endpoints reject HEAD; try GET range
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FSOT-prediction-monitor/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return {"ok": True, "status": getattr(resp, "status", None), "url": url}
        except Exception as e2:
            return {"ok": False, "error": f"{e}; {e2}", "url": url}


def evaluate_watch(
    watch: dict,
    *,
    margin_idx: dict[str, dict],
    freeze: dict,
    contested: dict,
    online: bool,
) -> dict[str, Any]:
    check = watch.get("check") or {}
    kind = check.get("kind") or "manual_or_catalog"
    out: dict[str, Any] = {
        "id": watch.get("id"),
        "title": watch.get("title"),
        "sector": watch.get("sector"),
        "pred_ids": watch.get("pred_ids") or [],
        "fsot_lock": watch.get("fsot_lock"),
        "unit": watch.get("unit"),
        "kill_if": watch.get("kill_if"),
        "urgency": watch.get("urgency"),
        "data_drop": watch.get("data_drop") or {},
        "check_kind": kind,
        "outcome": "open_predata",
        "detail": {},
    }

    # Contested observables with same name/property
    for ob in contested.get("observables") or []:
        name = str(ob.get("name") or "")
        if any(
            str(pid).replace("PRED-", "").lower() in name.lower()
            for pid in (watch.get("pred_ids") or [])
        ) or (
            watch.get("fsot_lock") is not None
            and ob.get("measured") is not None
            and abs(float(ob.get("measured")) - float(watch["fsot_lock"]))
            / max(abs(float(watch["fsot_lock"])), 1e-12)
            < 0.05
        ):
            out["detail"]["contested_match"] = {
                "name": name,
                "fsot_error_pct": ob.get("fsot_error_pct"),
                "within_green_gate": ob.get("within_green_gate"),
                "status": ob.get("status"),
            }

    if kind == "open_science_panel":
        row = _find_panel(margin_idx, check.get("panel_hint"))
        ps = _panel_status(row)
        out["detail"]["panel"] = ps
        if ps.get("green_gate_pass") is True:
            out["outcome"] = "local_green_hold"
        elif ps.get("green_gate_pass") is False:
            out["outcome"] = "local_gate_fail"
        else:
            out["outcome"] = "open_predata"

    elif kind == "open_api" and online:
        probe = check.get("open_probe")
        if probe == "gwosc_event_count":
            g = _probe_gwosc()
            out["detail"]["online_probe"] = g
            if g.get("ok"):
                out["outcome"] = "data_available"
                out["detail"]["note"] = (
                    f"GWOSC GWTC reports {g.get('event_count')} events — "
                    "compare residual panels; do not retune freeze."
                )
            else:
                out["outcome"] = "probe_failed"
        else:
            out["outcome"] = "open_predata"

    elif kind == "literature_watch":
        out["outcome"] = "open_predata"
        out["detail"]["note"] = "Literature kill-check; no auto scrape of papers."

    else:
        # manual / catalog — optional URL liveness when online
        urls = (watch.get("data_drop") or {}).get("urls") or []
        if online and urls:
            out["detail"]["url_probes"] = [_probe_http_head(u) for u in urls[:3]]
            if any(p.get("ok") for p in out["detail"]["url_probes"]):
                out["outcome"] = "source_reachable_awaiting_release"
            else:
                out["outcome"] = "open_predata"
        else:
            out["outcome"] = "open_predata"

    # Freeze cross-link
    freeze_ids = {p.get("id") for p in (freeze.get("sector_predictions") or [])}
    out["detail"]["in_t5_freeze"] = bool(set(watch.get("pred_ids") or []) & freeze_ids)

    return out


def build_report(*, online: bool) -> dict:
    reg = _load_yaml(REGISTRY)
    prereg = _load_yaml(PREREG)
    freeze = _load_json(FREEZE)
    margin = _load_json(MARGIN)
    contested = _load_json(CONTESTED)
    future = _load_json(FUTURE)
    margin_idx = _margin_index(margin)

    watches = reg.get("watches") or []
    results = [
        evaluate_watch(w, margin_idx=margin_idx, freeze=freeze, contested=contested, online=online)
        for w in watches
    ]

    counts: dict[str, int] = {}
    for r in results:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1

    prereg_preds = prereg.get("predictions") or []
    with_future = sum(1 for p in prereg_preds if p.get("future_survey"))
    domains = sorted({p.get("domain") for p in prereg_preds if p.get("domain")})

    report = {
        "generated_at": _now(),
        "online": online,
        "authority_pin_prefix": "D1D38A",
        "registry_version": reg.get("version"),
        "schedule": reg.get("schedule"),
        "summary": {
            "watch_count": len(results),
            "outcomes": counts,
            "prereg_prediction_count": len(prereg_preds),
            "prereg_with_future_survey_tag": with_future,
            "prereg_domain_count": len(domains),
            "t5_freeze_id": freeze.get("freeze_id"),
            "t5_bundle_sha256": freeze.get("bundle_sha256"),
            "future_ledger_rows": len(future.get("future_observations") or []),
            "green_gate_pass_count": margin.get("green_gate_pass_count"),
            "green_gate_fail_count": margin.get("green_gate_fail_count"),
        },
        "watches": results,
        "high_urgency_open": [
            r["id"]
            for r in results
            if r.get("urgency") == "high"
            and r.get("outcome")
            in {
                "open_predata",
                "source_reachable_awaiting_release",
                "data_available",
            }
        ],
        "commands": {
            "offline": "python scripts/run_prediction_monitor.py",
            "online": "python scripts/run_prediction_monitor.py --online",
            "freeze": "python -c \"import sys; sys.path.insert(0,'scripts'); from build_toe_gap_closure import freeze_prereg; freeze_prereg()\"",
            "kaggle_pack": "python scripts/build_kaggle_prediction_pack.py",
        },
    }
    body = json.dumps({k: v for k, v in report.items() if k != "report_sha256"}, sort_keys=True).encode()
    report["report_sha256"] = hashlib.sha256(body).hexdigest()
    return report


def write_md(report: dict) -> None:
    s = report.get("summary") or {}
    lines = [
        "# FSOT Prediction Monitor",
        "",
        f"*Generated {report.get('generated_at')} · online={report.get('online')} · pin D1D38A*",
        "",
        "Tracks **preregistered** FSOT locks against near/future public data drops. "
        "Predicted centrals are frozen; this report only updates **outcome status**.",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Watches | {s.get('watch_count')} |",
        f"| Prereg PREDs | {s.get('prereg_prediction_count')} |",
        f"| PREDs with future_survey tag | {s.get('prereg_with_future_survey_tag')} |",
        f"| Prereg domains | {s.get('prereg_domain_count')} |",
        f"| T5 freeze | `{s.get('t5_freeze_id')}` |",
        f"| Green gate | {s.get('green_gate_pass_count')}/{int(s.get('green_gate_pass_count') or 0) + int(s.get('green_gate_fail_count') or 0)} |",
        f"| Report SHA | `{report.get('report_sha256', '')[:16]}…` |",
        "",
        "### Outcomes",
        "",
        "| Outcome | Count |",
        "|---------|------:|",
    ]
    for k, v in sorted((s.get("outcomes") or {}).items()):
        lines.append(f"| {k} | {v} |")

    lines.extend(
        [
            "",
            "## High-urgency open watches",
            "",
        ]
    )
    hu = report.get("high_urgency_open") or []
    if not hu:
        lines.append("_None (or all closed)._")
    else:
        for wid in hu:
            lines.append(f"- `{wid}`")

    lines.extend(
        [
            "",
            "## All watches",
            "",
            "| ID | Sector | Urgency | Outcome | FSOT lock | Window |",
            "|----|--------|---------|---------|-----------|--------|",
        ]
    )
    for w in report.get("watches") or []:
        dd = w.get("data_drop") or {}
        lock = w.get("fsot_lock")
        lock_s = f"`{lock}`" if lock is not None else "—"
        lines.append(
            f"| {w.get('id')} | {w.get('sector')} | {w.get('urgency')} | "
            f"**{w.get('outcome')}** | {lock_s} | {dd.get('window', '')} |"
        )

    lines.extend(
        [
            "",
            "## Schedule",
            "",
            "```text",
            (report.get("schedule") or {}).get("recommended_interval", "7d"),
            "  python scripts/run_prediction_monitor.py",
            (report.get("schedule") or {}).get("online_interval", "14d"),
            "  python scripts/run_prediction_monitor.py --online",
            "```",
            "",
            "Related: `data/prediction_monitor_registry.yaml` · `docs/PREDATA_RISK.md` · "
            "`data/toe_prereg_freeze.json` · `docs/INDEPENDENT_REPRODUCTION.md`",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="FSOT prediction monitor")
    ap.add_argument("--online", action="store_true", help="Probe public endpoints (GWOSC, URL heads)")
    ap.add_argument("--offline", action="store_true", help="Force offline (default)")
    args = ap.parse_args()
    online = bool(args.online) and not args.offline

    report = build_report(online=online)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_md(report)

    s = report["summary"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"  watches={s['watch_count']} outcomes={s['outcomes']} "
        f"preds={s['prereg_prediction_count']} future_tagged={s['prereg_with_future_survey_tag']} "
        f"online={online}"
    )
    fails = (s.get("outcomes") or {}).get("local_gate_fail", 0)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
