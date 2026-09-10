# Market process layer

**Pin:** D1D38A · **Fold:** Economics \(D=20\) · **Generated:** 2026-09-10T00:57:25.184327+00:00

This is the start of *price prediction* as **process time**, not as a ticker.

| Handle | Live |
|--------|------|
| Class objects | 20 public anchors (`finance_markets_reference_observables.json`) |
| Domain median err% | **0.0258%** (green if ≤ 0.5%) |
| Process window | \(d=20\): 5.483 d → **1 calendar days** |
| Valve split | POOF 0.5107 / SUCTION 0.4893 |
| Class valve | `quiet_or_class` (VIX long-run vs bar 21.916) |

Refresh: `python scripts/build_market_process_layer.py`

**Claimed:** class residuals + a dated *window* at the Economics fold.

**Not claimed yet:** next-day SPX close, a crash date, beating a broker.

**Next data (open, no key):** World Bank already in-repo; Stooq daily index
CSV can be vendored later the same way NDBC is. Do not 0.5%-gate one print.

Kill: stuffing AAPL tomorrow into the green gate.
