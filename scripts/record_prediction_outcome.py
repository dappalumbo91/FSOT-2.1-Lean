#!/usr/bin/env python3
"""Append a prediction outcome to results/ without touching predictions/.

Predictions stay frozen (SHA + registered_at). When a paper, catalog, or
API lands, record the measured result here.

Example:
  python scripts/record_prediction_outcome.py ^
    --pred-id PRED-001 --survey CCHP-TRGB-2025 ^
    --result hold --measured 70.39 --unit km/s/Mpc ^
    --source https://arxiv.org/abs/2408.06153 ^
    --notes "CCHP TRGB highest-precision central"
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "results" / "outcomes" / "prediction_outcome_log.jsonl"

VALID = {"hold", "partial", "awaiting", "theory_rebase", "kill", "local_green_hold"}


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return "unknown"


def append_outcome(row: dict[str, Any]) -> Path:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return LOG


def main() -> int:
    ap = argparse.ArgumentParser(description="Append a frozen-prediction outcome")
    ap.add_argument("--pred-id", required=True)
    ap.add_argument("--survey", required=True, help="Paper / catalog / facility label")
    ap.add_argument("--result", required=True, choices=sorted(VALID))
    ap.add_argument("--measured", default=None, help="Numeric measured central if any")
    ap.add_argument("--unit", default=None)
    ap.add_argument("--source", default=None, help="URL or citation")
    ap.add_argument("--notes", default="")
    ap.add_argument("--watch-id", default=None)
    args = ap.parse_args()

    measured: float | str | None = args.measured
    if measured is not None:
        try:
            measured = float(measured)
        except ValueError:
            pass

    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "commit_sha": _git_sha(),
        "pred_id": args.pred_id,
        "watch_id": args.watch_id,
        "survey": args.survey,
        "result": args.result,
        "measured": measured,
        "unit": args.unit,
        "source": args.source,
        "notes": args.notes,
        "authority_pin_prefix": "D1D38A",
        "predictions_untouched": True,
    }
    path = append_outcome(row)
    print(f"Appended {args.pred_id} {args.result} → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
