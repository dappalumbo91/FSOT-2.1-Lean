"""FSOT cosmology wave observable extraction — waves 4–10."""

from __future__ import annotations

from typing import Any

from cosmology_lambda import summarize_lambda


def wave_observables(mod, wave_num: int) -> list[dict[str, Any]]:
    fn = getattr(mod, f"wave{wave_num}", None)
    if fn is None:
        raise AttributeError(f"fsot_compute missing wave{wave_num}()")
    rows: list[dict[str, Any]] = []
    wave_tag = f"wave{wave_num}"
    for r in fn():
        measured = float(r.measured) if r.measured is not None else None
        computed = float(r.computed)
        error_pct = None
        if measured is not None and measured != 0:
            error_pct = abs(computed - measured) / abs(measured) * 100.0
        rows.append(
            {
                "wave": wave_tag,
                "name": r.name,
                "formula": r.formula_str,
                "computed": computed,
                "measured": measured,
                "error_pct": error_pct,
            }
        )
    return rows


def summarize_waves(rows: list[dict], wave_nums: list[int]) -> dict[str, Any]:
    base = summarize_lambda(rows)
    by_wave = {f"wave{n}_count": sum(1 for r in rows if r.get("wave") == f"wave{n}") for n in wave_nums}
    return {
        "observable_count": base["observable_count"],
        "measured_count": base["measured_count"],
        "max_error_pct": base["max_error_pct"],
        "mean_error_pct": base["mean_error_pct"],
        **by_wave,
    }