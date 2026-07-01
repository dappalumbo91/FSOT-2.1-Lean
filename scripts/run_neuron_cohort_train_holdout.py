#!/usr/bin/env python3
"""Allen neuron cohort deterministic train/holdout split + regression gates."""

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
MANIFEST = ROOT / "data" / "neuron_cohort_train_holdout_manifest.yaml"
COHORT_MANIFEST = ROOT / "data" / "neuron_cohort_manifest.yaml"
OUTPUT = ROOT / "data" / "neuron_cohort_train_holdout.json"

sys.path.insert(0, str(ROOT / "scripts"))
from run_neuron_cohort_eval import (  # noqa: E402
    MANIFEST_PATH,
    eval_allen_fi_cohort,
    _infer_stratum,
)


def _split_label(specimen_id: int | None, hero_id: int, train_pct: int) -> str:
    if specimen_id is None:
        return "excluded"
    if hero_id and int(specimen_id) == hero_id:
        return "hero_excluded"
    bucket = (int(specimen_id) * 2654435761) % 1000
    return "train" if bucket < train_pct * 10 else "holdout"


def build_report(cells: list[dict], cohort_manifest: dict, spec: dict) -> dict:
    hero_id = int(cohort_manifest.get("strata", {}).get("hero_specimen_id") or 0)
    offset_pa = float(cohort_manifest["fi_proxy"]["stim_offset_pa"])
    train_pct = int(spec.get("split", {}).get("train_percent", 80))
    strata_cfg = cohort_manifest.get("strata", {}).get("classes") or []
    gates = spec.get("gates") or {}

    buckets: dict[str, list[dict]] = {"train": [], "holdout": []}
    for cell in cells:
        label = _split_label(cell.get("specimen__id"), hero_id, train_pct)
        if label in buckets:
            buckets[label].append(cell)

    overall = {}
    for label, subset in buckets.items():
        overall[label] = eval_allen_fi_cohort(subset, offset_pa)

    strata_out: dict[str, dict] = {}
    for sspec in strata_cfg:
        sid = sspec["id"]
        strata_out[sid] = {}
        for label in ("train", "holdout"):
            stratum_cells = [
                c
                for c in buckets[label]
                if _infer_stratum(c, strata_cfg) == sid
            ]
            strata_out[sid][label] = {
                "catalog_cells": len(stratum_cells),
                **eval_allen_fi_cohort(stratum_cells, offset_pa),
            }

    hold = overall.get("holdout") or {}
    hold_med = float(hold.get("fi_median_rel_err") or 1.0)
    hold_r = float(hold.get("fi_pearson_r") or 0.0)
    hold_n = int(hold.get("cell_count") or 0)

    gates_ok = (
        hold_n >= int(gates.get("holdout_min_cells", 400))
        and hold_med <= float(gates.get("holdout_fi_median_rel_err_max", 0.30))
        and hold_r >= float(gates.get("holdout_fi_pearson_r_min", 0.55))
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "split_method": "deterministic_specimen_hash",
        "train_percent": train_pct,
        "hero_specimen_excluded": hero_id,
        "train": overall.get("train"),
        "holdout": overall.get("holdout"),
        "strata": strata_out,
        "gates": {
            **gates,
            "all_pass": gates_ok,
            "holdout_median_rel_err": hold_med,
            "holdout_pearson_r": hold_r,
            "holdout_cell_count": hold_n,
        },
    }


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser(description="Neuron cohort train/holdout evaluation")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--cohort-manifest", type=Path, default=COHORT_MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    cohort_spec = yaml.safe_load(args.cohort_manifest.read_text(encoding="utf-8"))
    cohort_root = Path(cohort_spec["neuron_cohort_root"])
    cells_path = cohort_root / cohort_spec["artifacts"]["cells_json"]
    cells = json.loads(cells_path.read_text(encoding="utf-8"))

    doc = build_report(cells, cohort_spec, spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    tr = doc.get("train") or {}
    ho = doc.get("holdout") or {}
    print(f"  train: n={tr.get('cell_count')} median={tr.get('fi_median_rel_err', 0):.4f}")
    print(f"  holdout: n={ho.get('cell_count')} median={ho.get('fi_median_rel_err', 0):.4f}")
    print(f"  gates_pass: {doc.get('gates', {}).get('all_pass')}")
    return 0 if doc.get("gates", {}).get("all_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())