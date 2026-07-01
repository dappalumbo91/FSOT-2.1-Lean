#!/usr/bin/env python3
"""Compare FSOT evolution operon lengths to human mtDNA reference (NCBI NC_012920.1)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OPERONS = Path(
    r"C:\Users\damia\Desktop\fsot_evolution_\files-b7d9d6b8\fsot_evolution_sim\results\biological_mt_operons.json"
)
OUTPUT = ROOT / "data" / "evolution_operon_benchmark.json"

HUMAN_MT_OPERON_REF = {
    "MT-ND1": 956,
    "MT-ND2": 1044,
    "MT-CO1": 1542,
    "MT-CO2": 684,
    "MT-ATP8": 207,
    "MT-ATP6": 681,
    "MT-CO3": 780,
    "MT-ND3": 349,
    "MT-ND4L": 297,
    "MT-ND4": 1378,
    "MT-ND5": 1812,
    "MT-ND6": 525,
    "MT-CYTB": 1140,
}


def build_benchmark(operons_path: Path) -> dict:
    operons = json.loads(operons_path.read_text(encoding="utf-8"))
    records: list[dict] = []
    for name, ref_len in HUMAN_MT_OPERON_REF.items():
        entry = operons.get(name)
        if not entry:
            continue
        sim_len = int(entry.get("length") or 0)
        if ref_len == 0:
            continue
        err = abs(sim_len - ref_len) / ref_len * 100.0
        records.append(
            {
                "lab": "evolution_lab",
                "property": "mt_operon_length",
                "name": name,
                "computed": sim_len,
                "measured": ref_len,
                "error_pct": err,
            }
        )
    errs = [r["error_pct"] for r in records]
    return {
        "source": "NCBI_NC_012920.1",
        "operon_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "max_error_pct": max(errs) if errs else None,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build evolution operon benchmark")
    parser.add_argument("--operons", type=Path, default=DEFAULT_OPERONS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not args.operons.exists():
        print(f"FAIL: missing {args.operons}")
        return 1
    doc = build_benchmark(args.operons)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  operons: {doc['operon_count']}")
    if doc.get("median_error_pct") is not None:
        print(f"  median_error_pct: {doc['median_error_pct']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())