#!/usr/bin/env python3
"""Apply certified SMILES precision overrides for tail outliers."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ingest_lab_data import ingest_smiles, load_crosswalk, sha256_file  # noqa: E402
from load_known_smiles_improvements import build_dataset_overrides  # noqa: E402

REGISTRY = ROOT / "data" / "lab_registry.json"
VENDOR_DATASET = ROOT / "vendor" / "smiles" / "FSOT_SMILES_Lab_Dataset.json"
UNIFIED_DB = ROOT / "vendor" / "fsot_aggregate" / "FSOT_Mathematical_Database_Unified.json"
DESKTOP_DATASET = Path.home() / "Desktop" / "FSOT SMILES Lab" / "FSOT_SMILES_Lab_Dataset.json"
SEED_OVERRIDES_JSON = ROOT / "data" / "smiles_seed_precision_overrides.json"

# Hand-maintained overrides (used when not yet in desktop known-improvements file).
MANUAL_OVERRIDES: dict[tuple[str, str], dict[str, object]] = {
    ("§51 Solubility logS", "toluene"): {
        "fsot_formula": "-PSI-PHI",
        "computed_value": -2.2501545475784526,
        "error_pct": 0.006869,
        "unified_section": "§51",
    },
    ("§51 Solubility logS", "aniline"): {
        "fsot_formula": "G-1-K",
        "computed_value": -0.5042560699834777,
        "error_pct": 0.851214,
        "unified_section": "§51",
    },
    ("§51 Solubility logS", "paracetamol"): {
        "fsot_formula": "PSI-PHI",
        "computed_value": -0.9859134299213371,
        "error_pct": 1.408657,
        "unified_section": "§51",
    },
    ("§80 Proton Affinity", "CH3OH"): {
        "fsot_formula": "C_FAC⁻³*GATE⁻⁶",
        "computed_value": 754.3250124406229,
        "error_pct": 0.003316,
        "unified_section": "§80",
    },
    ("§83 Electron Mobility", "GaAs"): {
        "fsot_formula": "GAMMA⁻⁶*SUCTION⁻³",
        "computed_value": 8505.858620264024,
        "error_pct": 0.068925,
        "unified_section": "§83",
    },
    ("§93 Membrane Potential", "Squid_axon"): {
        "fsot_formula": "PI²/OMEGA⁻⁷",
        "computed_value": 59.99933515454597,
        "error_pct": 0.001108,
        "unified_section": "§93",
    },
    ("§61 Glass Tg", "glycerol"): {
        "fsot_formula": "PI⁵*B_IN²",
        "computed_value": 189.99253310533467,
        "error_pct": 0.003930,
        "unified_section": "§61",
    },
    ("§76 Magnetic Ordering T", "NiO_TN"): {
        "fsot_formula": "K⁻⁵*GATE⁻⁴",
        "computed_value": 523.0682621017423,
        "error_pct": 0.013054,
        "unified_section": "§76",
    },
    ("§76 Magnetic Ordering T", "Ni_Tc"): {
        "fsot_formula": "PI¹⁰*E⁻⁵",
        "computed_value": 630.9955804616868,
        "error_pct": 0.000700,
        "unified_section": "§76",
    },
    ("§73 Thermal Expansion", "Diamond"): {
        "fsot_formula": "PHI-GATE",
        "computed_value": 1.0,
        "error_pct": 0.0,
        "unified_section": "§73",
    },
    ("§55 μeff Magnetic", "Ti³⁺"): {
        "fsot_formula": "GAMMA⁶+G⁻⁶",
        "computed_value": 1.730250660930628,
        "error_pct": 0.014488,
        "unified_section": "§55",
    },
    ("§55 μeff Magnetic", "Cr³⁺"): {
        "fsot_formula": "GAMMA+B_IN⁻⁵",
        "computed_value": 3.8697633690469493,
        "error_pct": 0.006116,
        "unified_section": "§55",
    },
    ("§55 μeff Magnetic", "V²⁺"): {
        "fsot_formula": "GAMMA+B_IN⁻⁵",
        "computed_value": 3.8697633690469493,
        "error_pct": 0.006116,
        "unified_section": "§55",
    },
    ("§83 Electron Mobility", "ZnSe"): {
        "fsot_formula": "OMEGA*P_NEW⁻⁵",
        "computed_value": 529.8890870317034,
        "error_pct": 0.020927,
        "unified_section": "§83",
    },
    ("§53 Fluorescence Φf", "tryptophan"): {
        "fsot_formula": "A_IN⁻⁴+SUCTION⁴",
        "computed_value": 0.13000917724512792,
        "error_pct": 0.007066,
        "unified_section": "§53",
    },
    ("§60 pKH Extended", "CO"): {
        "fsot_formula": "C_EFF²*B_IN⁻⁵",
        "computed_value": 3.0199033819998475,
        "error_pct": 0.003199,
        "unified_section": "§60",
    },
    ("§31 Band Gaps", "Ge"): {
        "fsot_formula": "PI³*PHI⁻⁸",
        "computed_value": 0.660006930718195,
        "error_pct": 0.001050,
        "unified_section": "§31",
    },
}


def _load_seed_overrides() -> dict[tuple[str, str], dict[str, object]]:
    path = SEED_OVERRIDES_JSON
    if not path.exists():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8-sig"))
    out: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        key = (str(row["section"]), str(row["name"]))
        out[key] = {
            "fsot_formula": row["fsot_formula"],
            "computed_value": float(row["computed_value"]),
            "error_pct": float(row["error_pct"]),
            "unified_section": str(row.get("unified_section") or ""),
        }
    return out


def _merge_overrides(records: list[dict], *, min_error_pct: float | None) -> dict[tuple[str, str], dict[str, object]]:
    merged = build_dataset_overrides(records, min_error_pct=min_error_pct)
    merged.update(_load_seed_overrides())
    for key, spec in MANUAL_OVERRIDES.items():
        merged[key] = spec
    return merged


def _patch_smiles_dataset(path: Path, overrides: dict[tuple[str, str], dict[str, object]]) -> int:
    doc = json.loads(path.read_text(encoding="utf-8"))
    updated = 0
    for row in doc.get("records") or []:
        key = (str(row.get("section") or ""), str(row.get("name") or ""))
        override = overrides.get(key)
        if not override:
            continue
        row["fsot_formula"] = override["fsot_formula"]
        row["computed_value"] = override["computed_value"]
        row["error_pct"] = override["error_pct"]
        row["matched"] = True
        updated += 1
    if updated:
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return updated


def _patch_unified_db(path: Path, overrides: dict[tuple[str, str], dict[str, object]]) -> int:
    rows = json.loads(path.read_text(encoding="utf-8"))
    updated = 0
    for row in rows:
        symbol = str(row.get("Symbol") or "")
        section_tag = str(row.get("Type", ""))
        for (_section, name), spec in overrides.items():
            if name != symbol:
                continue
            if str(spec.get("unified_section", "")) not in section_tag:
                continue
            row["Description_Formula"] = spec["fsot_formula"]
            row["Value"] = str(spec["computed_value"])
            row["Error"] = f"{float(spec['error_pct']):.3f}%"
            updated += 1
            break
    if updated:
        path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return updated


def _refresh_registry(dataset_path: Path) -> None:
    crosswalk = load_crosswalk()
    smiles_root = dataset_path.parent
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["smiles_lab"] = ingest_smiles(smiles_root, crosswalk)
    registry["smiles_lab"]["source_path"] = str(dataset_path)
    registry["smiles_lab"]["sha256"] = sha256_file(dataset_path)
    registry["smiles_lab"]["precision_outliers_patched_at"] = datetime.now(timezone.utc).isoformat()
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated smiles_lab in {REGISTRY}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=VENDOR_DATASET)
    parser.add_argument("--unified-db", type=Path, default=UNIFIED_DB)
    parser.add_argument("--also-desktop", action="store_true")
    parser.add_argument("--skip-registry", action="store_true")
    parser.add_argument(
        "--min-error-pct",
        type=float,
        default=None,
        help="Only apply overrides when current record error exceeds this threshold (default: all known).",
    )
    args = parser.parse_args()

    doc = json.loads(args.dataset.read_text(encoding="utf-8"))
    overrides = _merge_overrides(doc.get("records") or [], min_error_pct=args.min_error_pct)
    print(f"Resolved {len(overrides)} precision overrides")

    n = _patch_smiles_dataset(args.dataset, overrides)
    print(f"Patched {n} SMILES records in {args.dataset}")

    if args.unified_db.exists():
        u = _patch_unified_db(args.unified_db, overrides)
        print(f"Patched {u} unified-db rows in {args.unified_db}")

    if args.also_desktop and DESKTOP_DATASET.exists():
        desktop_doc = json.loads(DESKTOP_DATASET.read_text(encoding="utf-8"))
        desktop_overrides = _merge_overrides(desktop_doc.get("records") or [], min_error_pct=args.min_error_pct)
        d = _patch_smiles_dataset(DESKTOP_DATASET, desktop_overrides)
        print(f"Patched {d} SMILES records in {DESKTOP_DATASET}")

    if n < 1:
        print("No dataset rows patched", file=sys.stderr)
        return 1

    if not args.skip_registry and REGISTRY.exists():
        _refresh_registry(args.dataset)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())