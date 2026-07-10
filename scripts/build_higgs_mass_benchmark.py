#!/usr/bin/env python3
"""Build higgs_mass benchmark — FO-213 mass + LHC measurement channels + mass ratios."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "higgs_mass_benchmark.json"
REFERENCE = ROOT / "data" / "higgs_mass_reference_observables.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cosmology_lambda import load_fsot_compute  # noqa: E402
from cosmology_waves import wave_observables  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from higgs_mass_formula_eval import evaluate_higgs_mass  # noqa: E402


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _ratio_rows(mod) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for wave_num in (3, 5):
        for row in wave_observables(mod, wave_num):
            name = str(row.get("name") or "")
            if name in ("m_H/m_W", "m_H/m_t"):
                out[name] = row
    return out


def build() -> dict:
    doc = evaluate_higgs_mass()
    computed_gev = float(doc["computed_gev"])
    computed_mev = float(doc["computed_mev"])
    rule_id = doc["rule_id"]
    formula = doc["formula"]

    ref_doc = json.loads(REFERENCE.read_text(encoding="utf-8"))
    mod = load_fsot_compute(fsot_compute_path())
    ratios = _ratio_rows(mod)

    records: list[dict] = [
        {
            "lab": "higgs_mass",
            "property": "m_H_GeV",
            "rule_id": rule_id,
            "computed": computed_gev,
            "measured": doc["measured_gev"],
            "error_pct": doc["error_pct"],
            "eval_kind": "live_formula",
            "formula": formula,
            "channel": "PDG2024_world_average",
        },
        {
            "lab": "higgs_mass",
            "property": "m_H_MeV",
            "rule_id": rule_id,
            "computed": computed_mev,
            "measured": doc["measured_gev"] * 1000.0,
            "error_pct": doc["error_pct"],
            "eval_kind": "live_formula",
            "channel": "unit_conversion",
        },
    ]

    for metric in ref_doc.get("metrics") or []:
        prop = str(metric.get("property") or "")
        measured = float(metric["measured"])
        channel = str(metric.get("channel") or metric.get("name") or "")

        if prop == "m_H_GeV":
            if channel == "PDG2024_world_average":
                continue
            err = _error_pct(computed_gev, measured)
            records.append(
                {
                    "lab": "higgs_mass",
                    "property": f"m_H_GeV_{metric['name']}",
                    "rule_id": rule_id,
                    "computed": computed_gev,
                    "measured": measured,
                    "error_pct": err,
                    "eval_kind": "measurement_channel",
                    "formula": formula,
                    "channel": channel,
                    "reference": metric.get("reference"),
                }
            )
        elif prop in ("m_H_m_W", "m_H_m_t"):
            ratio_name = "m_H/m_W" if prop == "m_H_m_W" else "m_H/m_t"
            row = ratios.get(ratio_name)
            if not row:
                continue
            records.append(
                {
                    "lab": "higgs_mass",
                    "property": prop,
                    "rule_id": ratio_name,
                    "computed": float(row["computed"]),
                    "measured": measured,
                    "error_pct": float(row["error_pct"] or _error_pct(float(row["computed"]), measured)),
                    "eval_kind": "fsot_compute_ratio",
                    "formula": row.get("formula"),
                    "channel": channel,
                    "reference": metric.get("reference"),
                    "wave": row.get("wave"),
                }
            )

    errs = sorted(float(r["error_pct"]) for r in records)
    return {
        "benchmark_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [
            "vendor/smiles/FSOT_SMILES_Lab_Dataset.json",
            "scripts/higgs_mass_formula_eval.py",
            "data/higgs_mass_reference_observables.json",
            "vendor/fsot_compute.py",
        ],
        "maps_to_lean": ["particle"],
        "rule_id": rule_id,
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": errs[len(errs) // 2] if errs else None,
        "material_records": records,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  records={doc['record_count']}  m_H={doc['records'][0]['computed']:.6f} GeV  "
        f"median_err={doc['median_error_pct']:.4f}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())