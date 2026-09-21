#!/usr/bin/env python3
"""Market process product — Economics class window, not a ticker. Pin AEB2AD."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYER = ROOT / "data" / "market_process_layer.json"


def main() -> int:
    print("product=market_windows pin=AEB2AD ledger=B_correct kill=ticker_close_as_0.5pct")
    if not LAYER.is_file():
        print("missing data/market_process_layer.json — run scripts/build_market_process_layer.py")
        return 1
    d = json.loads(LAYER.read_text(encoding="utf-8"))
    print(
        f"n={d.get('n')} median={d.get('median_error_pct')}% "
        f"window_days={d.get('calendar_window_days')} valve={d.get('valve')} pin={d.get('pin')}"
    )
    print("not_claimed: next-day SPX, crash date, broker beat")
    return 0 if d.get("green_class") else 1


if __name__ == "__main__":
    raise SystemExit(main())
