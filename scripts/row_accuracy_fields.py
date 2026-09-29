#!/usr/bin/env python3
"""Put the four accuracy fields on every gated scalar row.

accuracy_class, field_bar, value_computed, comparison_can_fail.
Numbers already on the row are not changed. The CODATA table is updated in
place. Every other benchmark scalar is written to
data/row_accuracy_attestation.jsonl, one row per scalar.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import classify_record  # noqa: E402

DATA = ROOT / "data"
LEDGER = DATA / "row_accuracy_attestation.jsonl"
SUMMARY = DATA / "row_accuracy_summary.json"
CODATA = DATA / "codata_full_table_open_benchmark.json"

SI_EXACT = frozenset(
    {
        "c_m_s",
        "h_J_s",
        "e_C",
        "k_J_K",
        "N_A",
        "R_J_mol_K",
        "K_J",
        "R_K",
        "F_C_mol",
        "eV_J",
    }
)
CONVENTIONAL_EXACT = frozenset({"g_n", "atm_Pa"})


def decimal_places(value: float) -> int:
    text = format(float(value), ".16g")
    if "e" in text:
        mantissa, exponent = text.split("e")
        exp = int(exponent)
        frac = len(mantissa.split(".")[1]) if "." in mantissa else 0
        return max(0, frac - exp) if exp < 0 else 0
    if "." not in text:
        return 0
    return len(text.split(".")[1])


def half_digit_ppm(measured: float) -> float | None:
    if measured == 0:
        return None
    half = 0.5 * (10.0 ** (-decimal_places(measured)))
    return half / abs(measured) * 1_000_000.0


def value_computed(row: dict) -> bool:
    if row.get("computed") is None:
        return False
    try:
        computed = float(row["computed"])
    except (TypeError, ValueError):
        return False
    try:
        measured = float(row["measured"]) if row.get("measured") is not None else None
    except (TypeError, ValueError):
        measured = None
    if computed == 0.0 and measured not in (None, 0.0):
        return False
    return True


def _uncertainty_ppm(row: dict) -> float | None:
    unc = row.get("reference_uncertainty_pct")
    if unc is None and isinstance(row.get("scientific_measurement"), dict):
        unc = row["scientific_measurement"].get("reference_uncertainty_pct")
    if unc is None:
        return None
    try:
        unc_f = float(unc)
    except (TypeError, ValueError):
        return None
    if unc_f <= 0:
        return None
    return unc_f * 10_000.0


def _bar(value: float, unit: str, rule: str) -> dict:
    return {"value": value, "unit": unit, "rule": rule}


def attest_row(row: dict, *, file_name: str = "") -> dict:
    """The four fields a row needs before it can count toward the theory bar."""
    prop = str(row.get("property") or "")
    prop_l = prop.lower()
    file_l = file_name.lower()
    existing = row.get("accuracy_class")
    math = str(row.get("math") or "")
    computed_ok = value_computed(row)

    codata_file = "codata" in file_l
    if existing in {"si_definition", "conventional_exact"} or prop in SI_EXACT or prop in CONVENTIONAL_EXACT:
        kind = "si_definition" if prop in SI_EXACT or existing == "si_definition" else "conventional_exact"
        fields = {
            "accuracy_class": kind,
            "field_bar": _bar(0, "exact", "adopted definition, not a prediction"),
            "value_computed": computed_ok,
            "comparison_can_fail": False,
        }
        return fields
    if existing == "codata_measured":
        return {
            "accuracy_class": "codata_measured",
            "field_bar": row.get("field_bar")
            or _bar(1.5e-4, "ppm", "CODATA relative uncertainty"),
            "value_computed": computed_ok,
            "comparison_can_fail": True,
        }
    if existing == "derived_from_alpha":
        return {
            "accuracy_class": "derived_from_alpha",
            "field_bar": _bar(1.5e-4, "ppm", "fixed by alpha once the SI definitions are adopted"),
            "value_computed": computed_ok,
            "comparison_can_fail": True,
        }
    if existing == "derived_exact":
        return {
            "accuracy_class": "derived_exact",
            "field_bar": _bar(0, "exact", "fixed by h, c, and k"),
            "value_computed": computed_ok,
            "comparison_can_fail": True,
        }
    if existing == "file_metadata":
        return {
            "accuracy_class": "file_metadata",
            "field_bar": _bar(0, "exact", "file count, not a physical constant"),
            "value_computed": computed_ok,
            "comparison_can_fail": False,
        }
    if existing == "uncomputed_stamp" or (codata_file and not computed_ok):
        return {
            "accuracy_class": "uncomputed_stamp",
            "field_bar": _bar(1.5e-4, "ppm", "no leaf yet; CODATA uncertainty is the bar when a leaf exists"),
            "value_computed": False,
            "comparison_can_fail": False,
        }
    if codata_file or existing in {"scale_stamp"}:
        kind = "uncomputed_stamp" if not computed_ok else "scale_stamp"
        return {
            "accuracy_class": kind,
            "field_bar": _bar(
                1.5e-4,
                "ppm",
                "CODATA relative uncertainty on alpha; other measured constants use their own",
            ),
            "value_computed": computed_ok,
            "comparison_can_fail": False,
        }
    if row.get("sigma_distance") is not None or any(
        token in file_l for token in ("h0", "shoes", "pantheon", "desi", "planck", "cmb", "bao")
    ) or "h0" in prop_l:
        kind = "cosmology_sigma"
        bar = _bar(1, "sigma", "tension against the named catalog")
    elif any(token in file_l for token in ("higgs", "muon", "pdg", "g2", "g-2")) or prop_l in {
        "m_h_gev",
        "m_w_gev",
        "m_z_gev",
    }:
        kind = "particle_sigma"
        bar = _bar(1, "sigma", "PDG total uncertainty")
    elif _uncertainty_ppm(row) is not None:
        kind = "experimental_scatter"
        bar = _bar(_uncertainty_ppm(row), "ppm", "stated experimental uncertainty")
    elif str(row.get("eval_kind") or "") == "seed_identity":
        kind = "exact_identity"
        bar = _bar(0, "exact", "identity residual")
    else:
        try:
            measured = float(row["measured"]) if row.get("measured") is not None else None
        except (TypeError, ValueError):
            measured = None
        floor = half_digit_ppm(measured) if measured not in (None, 0.0) else None
        kind = "quoted_digit"
        bar = _bar(
            floor if floor is not None else 5000.0,
            "ppm",
            "half of the last quoted digit" if floor is not None else "catalog gate, no quoted digit",
        )
    can_fail = computed_ok and math != "fsot_scaled_only"
    return {
        "accuracy_class": kind,
        "field_bar": bar,
        "value_computed": computed_ok,
        "comparison_can_fail": can_fail,
    }


def stamp_inplace(row: dict, *, file_name: str = "") -> None:
    fields = attest_row(row, file_name=file_name)
    row.update(fields)


def main() -> int:
    codata = json.loads(CODATA.read_text(encoding="utf-8"))
    for row in codata.get("material_records") or []:
        stamp_inplace(row, file_name=CODATA.name)
    CODATA.write_text(json.dumps(codata, indent=2) + "\n", encoding="utf-8")

    counts: Counter[str] = Counter()
    n = 0
    with LEDGER.open("w", encoding="utf-8") as handle:
        for path in sorted(DATA.glob("*_benchmark.json")):
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            records = doc.get("material_records") or doc.get("records") or []
            if not isinstance(records, list):
                continue
            for row in records:
                if not isinstance(row, dict):
                    continue
                if path.name != CODATA.name and classify_record(row, file_name=path.name) != "scalar":
                    continue
                if path.name == CODATA.name and row.get("property") in {
                    "pooled_median",
                    "fsot_prediction",
                }:
                    continue
                fields = attest_row(row, file_name=path.name)
                counts[fields["accuracy_class"]] += 1
                n += 1
                handle.write(
                    json.dumps(
                        {
                            "file": path.name,
                            "domain": doc.get("domain"),
                            "name": row.get("name"),
                            "property": row.get("property"),
                            **fields,
                        },
                        ensure_ascii=True,
                    )
                    + "\n"
                )
    summary = {
        "row_count": n,
        "fields": [
            "accuracy_class",
            "field_bar",
            "value_computed",
            "comparison_can_fail",
        ],
        "by_class": dict(counts),
        "ledger": str(LEDGER),
        "codata_rows_stamped_in_place": True,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"rows={n}")
    for key, count in counts.most_common():
        print(f"  {key} {count}")
    print("row_accuracy_fields_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
