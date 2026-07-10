#!/usr/bin/env python3
"""Build Tier 52 astrophysical structure crosswalk benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "astrophysical_structure_crosswalk_benchmark.json"
sys.path.insert(0, str(ROOT / "scripts"))

from astrophysical_structure_lib import build_benchmark_doc  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build_benchmark_doc()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(
        f"Wrote {args.output}\n"
        f"  records={doc.get('record_count')}  pooled={doc.get('pooled_median_error_pct')}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())