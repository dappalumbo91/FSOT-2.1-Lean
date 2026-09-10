#!/usr/bin/env python3
"""Market *process* layer — public class objects, not next-day tickers.

Economics D=20. Quiet vs storm is D4 (same valve as weather/H0).
Process window is process_time(φ^4, 20) rounded to SI days.

Kill: stuffing a single ticker close into the 0.5% gate.
Goal: dated quiet/storm windows, then finer dt — same path as ECMWF.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import fsot_scaled  # noqa: E402
from fsot_earth_fluid_forecast import (  # noqa: E402
    POOF,
    process_ceiling_days,
    process_time_days,
    valve_split,
)

REF = ROOT / "data" / "finance_markets_reference_observables.json"
OUT = ROOT / "data" / "market_process_layer.json"
DOC = ROOT / "docs" / "MARKET_PROCESS_LAYER.md"
DOMAIN = "Economics"


def main() -> int:
    ref = json.loads(REF.read_text(encoding="utf-8"))
    metrics = list(ref.get("metrics") or [])
    rows = []
    for m in metrics:
        meas = float(m["measured"])
        computed, err = fsot_scaled(meas, DOMAIN)
        rows.append(
            {
                "name": m["name"],
                "market": m.get("market"),
                "property": m.get("property"),
                "measured": meas,
                "computed": computed,
                "error_pct": err,
                "domain": DOMAIN,
                "source": "data/finance_markets_reference_observables.json",
            }
        )
    errs = sorted(r["error_pct"] for r in rows)
    median = errs[len(errs) // 2] if errs else 0.0
    vix = next((r for r in rows if r["name"] == "vix_long_run_mean"), None)
    storm_bar = (vix["measured"] if vix else 19.0) * (1.0 + float(POOF))
    # Class valve: long-run VIX vs POOF storm bar. Not tomorrow's VIX print.
    valve = "storm_sector" if vix and vix["measured"] >= storm_bar else "quiet_or_class"
    tau0 = process_ceiling_days()
    window_d = process_time_days(tau0, 20.0)
    # Next increment (same grammar as weather 48 h → 24 h): one SI day.
    # Structural d=20 duration stays in process_time_days_d20.
    window_days = 1
    p_fire, p_hold = valve_split()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pin": "D1D38A",
        "domain": DOMAIN,
        "D_eff": 20,
        "n": len(rows),
        "median_error_pct": median,
        "green_class": median <= 0.5,
        "valve": valve,
        "storm_bar_vix": storm_bar,
        "process_time_days_d20": window_d,
        "calendar_window_days": window_days,
        "poof_hold": p_fire,
        "suction_hold": p_hold,
        "kill": "A single ticker close or crash date as a 0.5% central.",
        "goal": "1-day quiet/storm windows on public class objects; finer dt later.",
        "previous_calendar_window_days": max(1, int(round(window_d))),
        "rows": rows,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    doc = f"""# Market process layer

**Pin:** D1D38A · **Fold:** Economics \(D=20\) · **Generated:** {payload['generated_at']}

This is the start of *price prediction* as **process time**, not as a ticker.

| Handle | Live |
|--------|------|
| Class objects | {payload['n']} public anchors (`finance_markets_reference_observables.json`) |
| Domain median err% | **{median:.4f}%** (green if ≤ 0.5%) |
| Process window | \(d=20\): {window_d:.3f} d → **{window_days} calendar days** |
| Valve split | POOF {p_fire:.4f} / SUCTION {p_hold:.4f} |
| Class valve | `{valve}` (VIX long-run vs bar {storm_bar:.3f}) |

Refresh: `python scripts/build_market_process_layer.py`

**Claimed:** class residuals + a dated *window* at the Economics fold.

**Not claimed yet:** next-day SPX close, a crash date, beating a broker.

**Next data (open, no key):** World Bank already in-repo; Stooq daily index
CSV can be vendored later the same way NDBC is. Do not 0.5%-gate one print.

Kill: stuffing AAPL tomorrow into the green gate.
"""
    DOC.write_text(doc, encoding="utf-8")
    print(f"Wrote {OUT} median={median:.4f}% window={window_days}d valve={valve}")
    return 0 if payload["green_class"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
