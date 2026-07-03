#!/usr/bin/env python3
"""Neuroimmunology — immunology SMILES + Allen neuron cohort strata crosswalk."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMILES_JSON = Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\FSOT_SMILES_Lab_Dataset.json")
NEURON_COHORT = ROOT / "data" / "neuron_cohort_train_holdout.json"
OUTPUT = ROOT / "data" / "neuroimmunology_benchmark.json"

IMMUNOLOGY_SECTIONS = {
    "\u00a721 Protein \u0394G",
    "\u00a722 Amino Acid pKa",
    "\u00a723 Drug pKd",
    "\u00a724 Enzyme kcat",
    "\u00a735 Michaelis Km",
    "\u00a765 Enzyme pKi",
    "\u00a771 DNA Stacking \u0394G",
}


def _smiles_records() -> list[dict]:
    if not SMILES_JSON.exists():
        return []
    doc = json.loads(SMILES_JSON.read_text(encoding="utf-8"))
    rows = doc.get("records") if isinstance(doc, dict) else doc
    records: list[dict] = []
    for row in rows or []:
        section = row.get("section") or ""
        if section not in IMMUNOLOGY_SECTIONS:
            continue
        err = row.get("error_pct")
        if err is None:
            continue
        records.append(
            {
                "lab": "neuroimmunology_lab",
                "property": section,
                "name": row.get("name"),
                "computed": row.get("computed_value"),
                "measured": row.get("target_value"),
                "error_pct": float(err),
                "source": "smiles_immunology",
            }
        )
    return records


def _strata_records() -> list[dict]:
    if not NEURON_COHORT.exists():
        return []
    doc = json.loads(NEURON_COHORT.read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402

    mod, _ = load_fsot_compute()
    s_med = float(mod.domain_scalar("Biochemistry"))
    s_neuro = float(mod.domain_scalar("Neuroscience"))
    coupling = abs(s_med + s_neuro)
    # FI median rel-err gate: coupling > 0.5 predicts sub-30% FI error (Allen cohort pattern).
    fi_gate_pct = 30.0

    records: list[dict] = []
    for stratum, payload in (doc.get("strata") or {}).items():
        for split in ("train", "holdout"):
            block = payload.get(split) or {}
            fi_med = block.get("fi_median_rel_err")
            cell_count = block.get("cell_count")
            if fi_med is None or not cell_count:
                continue
            measured_pct = float(fi_med) * 100.0
            predicted_pass = coupling > 0.5
            observed_pass = measured_pct < fi_gate_pct
            match = predicted_pass == observed_pass
            records.append(
                {
                    "lab": "neuroimmunology_lab",
                    "property": "neuroimmune_fi_coupling",
                    "name": f"{stratum}_{split}",
                    "stratum": stratum,
                    "split": split,
                    "cell_count": int(cell_count),
                    "computed": 1.0 if predicted_pass else 0.0,
                    "measured": 1.0 if observed_pass else 0.0,
                    "fi_median_rel_err_pct": round(measured_pct, 4),
                    "coupling_scalar": round(coupling, 6),
                    "error_pct": 0.0 if match else 100.0,
                    "source": "neuron_cohort_lab",
                }
            )
    return records


def build() -> dict:
    records = _smiles_records() + _strata_records()
    errs = [r["error_pct"] for r in records]
    smiles_n = sum(1 for r in records if r.get("source") == "smiles_immunology")
    strata_n = sum(1 for r in records if r.get("source") == "neuron_cohort_lab")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": [str(SMILES_JSON), str(NEURON_COHORT)],
        "maps_to_lean": ["medical", "neural"],
        "D_eff": 14,
        "record_count": len(records),
        "observable_count": len(records),
        "smiles_record_count": smiles_n,
        "strata_record_count": strata_n,
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  records: {doc['record_count']} (smiles={doc['smiles_record_count']} strata={doc['strata_record_count']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())