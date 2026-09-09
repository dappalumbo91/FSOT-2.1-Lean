#!/usr/bin/env python3
"""Smoke: new dated forecasts carry fold + potentials. Does not write issues.

Kill: rewriting predictions/dated_forecasts/. Retuning kernel km.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_earth_fluid_forecast import (  # noqa: E402
    earthquake_forecasts,
    kernel_km,
)


def _events() -> list[dict]:
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    day = 86400 * 1000
    # Cluster of M4.6 with no M≥5.5 → loading_suction
    return [
        {"lat": -8.5, "lon": 121.4, "mag": 4.8, "time": now_ms - 2 * day, "place": "smoke cell A"},
        {"lat": -8.51, "lon": 121.41, "mag": 4.6, "time": now_ms - 3 * day, "place": "smoke cell A"},
        {"lat": -8.52, "lon": 121.42, "mag": 4.7, "time": now_ms - 4 * day, "place": "smoke cell A"},
        # Separate post-POOF cell
        {"lat": 52.2, "lon": -169.4, "mag": 6.1, "time": now_ms - 1 * day, "place": "smoke cell B"},
        {"lat": 52.21, "lon": -169.41, "mag": 5.0, "time": now_ms - 2 * day, "place": "smoke cell B"},
    ]


def main() -> int:
    issued = datetime.now(timezone.utc)
    fcs = earthquake_forecasts(_events(), issued=issued)
    if not fcs:
        print("FAIL: no forecasts from smoke events", file=sys.stderr)
        return 1
    k = kernel_km()
    for fc in fcs:
        pred = fc.get("predicted") or {}
        kill = str(fc.get("kill_if") or "")
        pots = pred.get("potentials") or []
        w = sum(float(p.get("weight") or 0) for p in pots)
        if not pots:
            print(f"FAIL {fc['id']}: missing potentials", file=sys.stderr)
            return 1
        if abs(w - 1.0) > 1e-5:
            print(f"FAIL {fc['id']}: weights sum {w}", file=sys.stderr)
            return 1
        if pred.get("fold_valve_d") != 25:
            print(f"FAIL {fc['id']}: fold_valve_d {pred.get('fold_valve_d')}", file=sys.stderr)
            return 1
        if "cycle_radius_km" not in pred:
            print(f"FAIL {fc['id']}: missing cycle_radius_km", file=sys.stderr)
            return 1
        loc_r = float((fc.get("location") or {}).get("radius_km") or 0)
        if abs(loc_r - round(k, 1)) > 0.2:
            print(f"FAIL {fc['id']}: kill radius {loc_r} vs kernel {k}", file=sys.stderr)
            return 1
        if "39" not in kill and "40" not in kill:
            # kernel is 39.1 → kill_if still names the cell
            if f"{k:.0f}" not in kill:
                print(f"FAIL {fc['id']}: kill_if lost cell scale: {kill}", file=sys.stderr)
                return 1
        ids = {str(p.get("id")) for p in pots}
        state = str(pred.get("valve_state") or "")
        if state == "loading_suction" and "cell_poof" not in ids:
            print(f"FAIL {fc['id']}: loading missing cell_poof", file=sys.stderr)
            return 1
        if state == "post_poof_aftershock" and "quiet_hold" not in ids:
            print(f"FAIL {fc['id']}: post_poof missing quiet_hold", file=sys.stderr)
            return 1
        print(
            f"ok {fc['id']} valve={state} n_pot={len(pots)} "
            f"fold_score={pred.get('fold_score_d')} kill_cell=yes"
        )
    print(f"smoke n={len(fcs)} kernel={k:.1f}  (no issue JSON written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
