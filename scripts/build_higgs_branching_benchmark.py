#!/usr/bin/env python3
"""Higgs branching observables — fsot_compute wave5/8 + thesis wave8 targets."""

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
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
MANIFEST = ROOT / "data" / "higgs_branching_manifest.yaml"
OUTPUT = ROOT / "data" / "higgs_branching_benchmark.json"

from fsot_paths import fsot_compute_path, thesis_root  # noqa: E402

HIGGS_NAME_MARKERS = ("BR_H", "Higgs", "higgs", "m_H")


def _is_higgs_row(name: str) -> bool:
    n = name or ""
    return any(m in n for m in HIGGS_NAME_MARKERS)


def _thesis_higgs(thesis_root: Path, wave: int, categories: list[str]) -> list[dict]:
    path = thesis_root / f"wave{wave}_observations.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    cat_set = set(categories)
    out: list[dict] = []
    for key, row in (data.get("targets") or {}).items():
        if row.get("category") not in cat_set:
            continue
        out.append(
            {
                "source": "thesis_wave",
                "wave": wave,
                "id": key,
                "name": row.get("name") or key,
                "measured": row.get("measured"),
                "sigma_percent": row.get("sigma_percent"),
            }
        )
    return out


def build_benchmark(manifest_path: Path = MANIFEST) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    src = spec["source"]
    sys.path.insert(0, str(ROOT / "scripts"))
    from cosmology_lambda import load_fsot_compute  # noqa: E402
    from cosmology_waves import wave_observables  # noqa: E402

    mod = load_fsot_compute(fsot_compute_path())
    compute_rows: list[dict] = []
    for wave_num in (5, 8):
        for row in wave_observables(mod, wave_num):
            if _is_higgs_row(str(row.get("name", ""))):
                row = {**row, "source": "fsot_compute"}
                compute_rows.append(row)

    thesis_rows = _thesis_higgs(
        thesis_root(),
        int(src["thesis_wave"]),
        list(src["higgs_categories"]),
    )

    errs = [float(r["error_pct"]) for r in compute_rows if r.get("error_pct") is not None]
    within_5 = sum(1 for e in errs if e <= 5.0)
    median_err = sorted(errs)[len(errs) // 2] if errs else None
    records = []
    if median_err is not None:
        records.append(
            {
                "lab": "higgs_branching",
                "property": "median_error_pct",
                "computed": median_err,
                "measured": 0.5,
                "error_pct": median_err,
                "eval_kind": "aggregate_median",
            }
        )

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "compute_higgs_count": len(compute_rows),
        "thesis_higgs_count": len(thesis_rows),
        "observable_count": len(compute_rows) + len(thesis_rows),
        "median_error_pct": median_err,
        "max_error_pct": max(errs) if errs else None,
        "within_five_pct_count": within_5,
        "records": records,
        "compute_higgs_rows": compute_rows,
        "thesis_higgs_rows": thesis_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    bench = build_benchmark(args.manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(
        f"  compute: {bench['compute_higgs_count']}  thesis: {bench['thesis_higgs_count']}  "
        f"total: {bench['observable_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())