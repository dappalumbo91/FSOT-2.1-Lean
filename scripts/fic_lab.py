"""FSOT Intelligence Compressor (FIC) — scalar sweep + fertile-window scoring."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

FERTILE_S_MIN = 0.18
FERTILE_S_MAX = 0.38
FERTILE_CENTER = 0.2736
# Low-D_eff valve attenuates emergent S into the fertile intelligence window.
FIC_VALVE = 0.42
OPTIMAL = {"D_eff": 12, "delta_psi": 0.8, "recent_hits": 1, "observed": True, "attention_weight": 1.0}


def _scalar_input(mod, *, D_eff: int, delta_psi: float, recent_hits: int, observed: bool, attention_weight: float = 1.0):
    si = mod.ScalarInput(
        N=mod.mpf(1),
        P=mod.mpf(1),
        D_eff=mod.mpf(D_eff),
        delta_psi=mod.mpf(delta_psi),
        delta_theta=mod.mpf(1),
        recent_hits=mod.mpf(recent_hits),
        observed=observed,
        rho=mod.mpf(1),
        scale=mod.mpf(1),
        amplitude=mod.mpf(1),
        trend_bias=mod.mpf(0),
    )
    raw = float(mod.compute_scalar(si))
    if observed and attention_weight != 1.0:
        boost = float(mod.C_FACTOR) * float(mod.P_VAR) * (attention_weight - 1.0)
        raw = raw * (1.0 + 0.15 * boost)
    return raw * FIC_VALVE


def is_fertile(S: float, observed: bool) -> bool:
    return observed and FERTILE_S_MIN <= S <= FERTILE_S_MAX


def intelligence_score(S: float, fertile: bool, attention_weight: float = 1.0) -> float:
    if not fertile:
        return 0.0
    proximity = max(0.0, 1.0 - abs(S - FERTILE_CENTER) / 0.15)
    return min(1.0, proximity * attention_weight)


def compression_ratio(D_eff: int) -> float:
    return float(max(8.0, 4.0 * D_eff))


def fidelity_proxy(intelligence_score_val: float, fertile: bool) -> float:
    if not fertile:
        return 0.0
    return min(1.0, 0.80 + 0.20 * intelligence_score_val)


def run_single(
    mod,
    *,
    D_eff: int = 12,
    delta_psi: float = 0.8,
    recent_hits: int = 1,
    observed: bool = True,
    attention_weight: float = 1.0,
) -> dict[str, Any]:
    S = _scalar_input(
        mod,
        D_eff=D_eff,
        delta_psi=delta_psi,
        recent_hits=recent_hits,
        observed=observed,
        attention_weight=attention_weight,
    )
    fertile = is_fertile(S, observed)
    intel = intelligence_score(S, fertile, attention_weight)
    return {
        "D_eff": D_eff,
        "delta_psi": delta_psi,
        "recent_hits": recent_hits,
        "observed": observed,
        "attention_weight": attention_weight,
        "S_final": S,
        "fertile": fertile,
        "intelligence_score": intel,
        "compression_ratio": compression_ratio(D_eff),
        "fidelity_proxy": fidelity_proxy(intel, fertile),
    }


def run_sensitivity_sweep(
    *,
    d_eff_range: range | None = None,
    delta_psi_values: list[float] | None = None,
    hits_values: list[int] | None = None,
    observed: bool = True,
) -> list[dict[str, Any]]:
    mod, _ = load_fsot_compute()
    d_eff_range = d_eff_range or range(6, 19)
    delta_psi_values = delta_psi_values or [round(0.2 + 0.1 * i, 1) for i in range(11)]
    hits_values = hits_values or [0, 1, 2, 3]
    rows: list[dict[str, Any]] = []
    for d_eff in d_eff_range:
        for dpsi in delta_psi_values:
            for hits in hits_values:
                rows.append(
                    run_single(
                        mod,
                        D_eff=d_eff,
                        delta_psi=dpsi,
                        recent_hits=hits,
                        observed=observed,
                    )
                )
    return rows


def write_sweep_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fields = [
        "D_eff",
        "delta_psi",
        "recent_hits",
        "S_final",
        "fertile",
        "intelligence_score",
        "compression_ratio",
        "fidelity_proxy",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row[k] for k in fields})


def summarize_sweep(rows: list[dict[str, Any]]) -> dict[str, Any]:
    fertile_rows = [r for r in rows if r["fertile"]]
    best = max(rows, key=lambda r: r["intelligence_score"]) if rows else {}
    optimal = next(
        (
            r
            for r in rows
            if r["D_eff"] == OPTIMAL["D_eff"]
            and abs(r["delta_psi"] - OPTIMAL["delta_psi"]) < 1e-6
            and r["recent_hits"] == OPTIMAL["recent_hits"]
        ),
        None,
    )
    return {
        "sweep_row_count": len(rows),
        "fertile_count": len(fertile_rows),
        "best_intelligence_score": best.get("intelligence_score", 0.0),
        "best_params": {
            "D_eff": best.get("D_eff"),
            "delta_psi": best.get("delta_psi"),
            "recent_hits": best.get("recent_hits"),
            "S_final": best.get("S_final"),
        },
        "optimal_params": OPTIMAL,
        "optimal_S_final": optimal.get("S_final") if optimal else None,
        "optimal_fertile": optimal.get("fertile") if optimal else None,
        "maps_to_lean": ["neural", "consciousness", "ai"],
        "D_eff": OPTIMAL["D_eff"],
        "observed": OPTIMAL["observed"],
    }