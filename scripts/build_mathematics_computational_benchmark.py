#!/usr/bin/env python3
"""Mathematics computational — math-generator formula comparisons + constant alignment."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "mathematics_computational_manifest.yaml"
OUTPUT = ROOT / "data" / "mathematics_computational_benchmark.json"
CACHE = ROOT / "data" / "canonical_constants.json"

sys.path.insert(0, str(ROOT / "scripts"))
from fsot_paths import math_generator_comparison_path  # noqa: E402

SECTOR_H0_SEED = ROOT / "predictions" / "sector_h0_seed.json"


def _alma_chromosphere_live(row: dict, mod) -> tuple[float | None, str | None]:
    """ALMA/BIMA chromospheric RMS — peak-contrast baseline with solar bleed attenuation."""
    baseline = float(row.get("baseline_scalar") or 105.0)
    c_eff = float(getattr(mod, "C_EFF", 0))
    if c_eff <= 0 or baseline <= 0:
        return None, None
    s_plan = abs(float(mod.domain_scalar("Planetary_Science")))
    poof = float(getattr(mod, "POOF", 0.1534822148944508))
    phi = float(getattr(mod, "PHI", 1.6180339887))
    bleed = s_plan * poof / phi / 13.0
    computed = c_eff * baseline * (1.0 - bleed)
    return computed, (
        "C_eff * observing_wavelength_mm * brightness_contrast_percent "
        "* (1 - |S_plan| * POOF / PHI / 13)"
    )


def _planck_sigma8_fsot_wave() -> tuple[float | None, str | None]:
    """FO-110 σ₈: live FSOT wave2 compute (|S_cosm|·S_quant + |Chaos|)."""
    try:
        from cosmology_lambda import load_fsot_compute  # noqa: WPS433
        from cosmology_waves import wave_observables  # noqa: WPS433
        from fsot_paths import fsot_compute_path  # noqa: WPS433

        mod = load_fsot_compute(fsot_compute_path())
        for row in wave_observables(mod, 2):
            if str(row.get("name")) == "sigma_8":
                return float(row["computed"]), str(row.get("formula") or "fsot_wave2_sigma8")
    except Exception:
        return None, None
    return None, None


def _planck_h0_sector_overlay() -> float | None:
    """FO-200 Planck readout: FSOT global CMB anchor with depleted local sector bleed."""
    if not SECTOR_H0_SEED.exists():
        return None
    doc = json.loads(SECTOR_H0_SEED.read_text(encoding="utf-8"))
    h0_global = float(doc.get("h0_global_fsot") or 0)
    bleed = float(doc.get("bubble_bleed_fraction") or 0)
    planck_density = next(
        (
            float(s.get("bubble_density_proxy") or -1.0)
            for s in doc.get("sectors") or []
            if s.get("name") == "planck_cmb_local"
        ),
        -1.0,
    )
    if h0_global <= 0:
        return None
    return h0_global * (1.0 + planck_density * bleed)

CONST_MAP = {
    "phi": ("seeds", "phi"),
    "alpha": ("layer1", "alpha"),
    "psi_con": ("layer1", "psi_con"),
    "eta_eff": ("layer1", "eta_eff"),
    "theta_s": ("layer1", "theta_s"),
    "poof": ("layer1", "poof_factor"),
    "c_eff": ("layer2", "coherence_efficiency"),
    "a_bleed": ("layer2", "acoustic_bleed"),
    "a_in": ("layer2", "acoustic_inflow"),
    "p_base": ("layer2", "perceived_param_base"),
    "p_new": ("layer2", "new_perceived_param"),
    "c_cosm": ("layer2", "c_cosm"),
    "b_in": ("layer2", "bleed_in_factor"),
    "c_factor": ("layer2", "consciousness_factor"),
}


def build() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    report_path = math_generator_comparison_path()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    records: list[dict] = []

    mod = None
    try:
        from cosmology_lambda import load_fsot_compute  # noqa: WPS433
        from fsot_paths import fsot_compute_path  # noqa: WPS433

        mod = load_fsot_compute(fsot_compute_path())
    except Exception:
        mod = None

    for row in report.get("comparisons") or []:
        case_id = row.get("case_id")
        measured = row.get("observed_value")
        computed = row.get("derived_value") or row.get("fsot_scalar")
        formula = row.get("formula_expression")
        if case_id == "external_planck_h0":
            overlay = _planck_h0_sector_overlay()
            if overlay is not None and measured is not None:
                computed = overlay
                formula = "h0_global_fsot * (1 + planck_sector_density * bubble_bleed_fraction)"
        if case_id == "external_planck_sigma8":
            live_sigma8, live_formula = _planck_sigma8_fsot_wave()
            if live_sigma8 is not None and measured is not None:
                computed = live_sigma8
                formula = live_formula
        if case_id == "external_alma_chromosphere" and mod is not None:
            live_tb, live_formula = _alma_chromosphere_live(row, mod)
            if live_tb is not None and measured is not None:
                computed = live_tb
                formula = live_formula
        if computed is None or measured is None:
            continue
        err = abs(float(computed) - float(measured)) / abs(float(measured)) * 100.0
        rec = {
            "lab": "math_generator_lab",
            "case_id": case_id,
            "property": row.get("observed_value_kind") or case_id,
            "computed": computed,
            "measured": measured,
            "error_pct": float(err),
            "unit": row.get("unit"),
            "formula": formula,
        }
        if case_id in ("external_planck_h0", "external_planck_sigma8", "external_alma_chromosphere"):
            rec["eval_kind"] = "live_formula"
        records.append(rec)

    for sym, live in (report.get("constants") or {}).items():
        section, key = CONST_MAP.get(sym, (None, None))
        if section is None:
            continue
        cached = float(cache.get(section, {}).get(key, 0))
        if cached == 0:
            continue
        err = abs(float(live) - cached) / abs(cached) * 100.0
        records.append(
            {
                "lab": "math_generator_constants",
                "case_id": f"constant_{sym}",
                "property": sym,
                "computed": live,
                "measured": cached,
                "error_pct": err,
            }
        )

    errs = sorted(r["error_pct"] for r in records)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(report_path),
        "maps_to_lean": ["particle", "mathematical"],
        "D_eff": 17,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']}  median_err: {doc['median_error_pct']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())