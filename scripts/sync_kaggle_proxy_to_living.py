#!/usr/bin/env python3
"""Write KAGGLE_CELL_TRACKING_PROXY.json for FSOT-Living from v50 benchmark."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "kaggle_biohub_v50_competition_bridge.json"
LIVING_STATE = Path(
    r"C:\Users\damia\Desktop\living fsot\files-e5887462\state\habitat-rust\KAGGLE_CELL_TRACKING_PROXY.json"
)


def main() -> int:
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    proxy = bench["score_ladder"]["v50_fsot_pure_link_ilp_cpu"]
    out = {
        "proxy_accuracy": proxy,
        "source": f"FSOT-2.1-Lean {bench['bundle_path']} train proxy",
        "adaptive_band": 0.62,
        "competitive_defaults": bench["competitive_defaults"],
        "note": "Update proxy_accuracy after each Kaggle leaderboard feedback",
    }
    LIVING_STATE.parent.mkdir(parents=True, exist_ok=True)
    LIVING_STATE.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {LIVING_STATE} proxy={proxy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())