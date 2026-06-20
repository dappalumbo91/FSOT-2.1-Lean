"""FSOT weather scalar simulation — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_weather_log(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_weather(rows: list[dict]) -> dict[str, Any]:
    S_vals = [float(r["S"]) for r in rows]
    D_vals = {float(r["fsot_params"]["D_eff"]) for r in rows}
    positive = sum(1 for s in S_vals if s > 0)
    return {
        "hour_count": len(rows),
        "D_eff_values": sorted(D_vals),
        "S_min": min(S_vals) if S_vals else None,
        "S_max": max(S_vals) if S_vals else None,
        "S_mean": sum(S_vals) / len(S_vals) if S_vals else None,
        "positive_S_hours": positive,
    }