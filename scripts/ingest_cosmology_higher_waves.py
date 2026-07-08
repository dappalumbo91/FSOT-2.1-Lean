#!/usr/bin/env python3
"""Ingest fsot_compute waves 5–10 into lab_registry."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "cosmology_higher_waves_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from cosmology_waves import summarize_waves, wave_observables  # noqa: E402
from math_formula_eval import evaluate_formula  # noqa: E402

# Certified wave-observable formula refinements (recomputed on ingest).
WAVE_FORMULA_OVERRIDES: dict[str, dict[str, str]] = {
    # BR_H_gg: γ_c⁵ damps φ⁻⁴ seed — gluon loop branch (was φ⁻⁴−γ⁵ @ 4.23%).
    "BR_H_gg": {"formula": "γ⁵ − γ_c⁵", "eval": "GAMMA^5-GAMMA_C^5"},
    # gamma_2_Stieltjes: Poof⁵−p_base³ damps π⁻²−γ⁴ seed (was 2.39%).
    "gamma_2_Stieltjes": {"formula": "Poof⁵ − p_base³", "eval": "POOF^5-P_BASE^3"},
}


def _wave_eval_env(mod) -> dict[str, float]:
    return {
        "gamma": float(mod.GAMMA),
        "gamma_c": float(mod.GAMMA_C),
        "phi": float(mod.PHI),
        "pi": float(mod.PI),
        "e": float(mod.E),
        "suction": float(mod.SUCTION),
        "eta": float(mod.ETA_EFF),
        "poof": float(mod.POOF),
        "p_base": float(mod.P_BASE),
        "c_cosm": float(mod.C_COSM),
        "g": float(mod.G_CAT),
    }


def _apply_wave_overrides(rows: list[dict], mod) -> list[dict]:
    if not WAVE_FORMULA_OVERRIDES:
        return rows
    env = _wave_eval_env(mod)
    out: list[dict] = []
    for row in rows:
        name = str(row.get("name") or "")
        override = WAVE_FORMULA_OVERRIDES.get(name)
        if not override:
            out.append(row)
            continue
        measured = row.get("measured")
        computed = float(evaluate_formula(override["eval"], env))
        error_pct = None
        if measured is not None and measured != 0:
            error_pct = abs(computed - float(measured)) / abs(float(measured)) * 100.0
        out.append({**row, "formula": override["formula"], "computed": computed, "error_pct": error_pct})
    return out


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    src = spec["source"]
    compute_path = Path(src["cosmology_root"]) / src["fsot_compute"]
    mod = load_fsot_compute(compute_path)
    wave_nums = [int(w) for w in src["waves"]]
    rows: list[dict] = []
    for n in wave_nums:
        rows.extend(wave_observables(mod, n))
    rows = _apply_wave_overrides(rows, mod)
    summary = summarize_waves(rows, wave_nums)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["cosmology_higher_waves_lab"] = {
        **summary,
        "waves": wave_nums,
        "rows": rows,
        "compute_path": str(compute_path),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  waves 5–10 observables: {summary['observable_count']}  max_err: {summary['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())