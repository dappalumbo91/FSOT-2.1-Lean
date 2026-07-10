#!/usr/bin/env python3
"""Ingest fringe desktop traces into vendor summaries + G: cache."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fringe_desktop_ingest_lib import (  # noqa: E402
    ingest_intelligence_compressor,
    ingest_soul_simulator_manifest,
    ingest_symbolic_encoding_graph,
    ingest_vibrafsot_progress,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        choices=["soul", "fic", "vibra", "symbolic", "all"],
        default="all",
    )
    args = parser.parse_args()
    tasks = {
        "soul": ("soul_simulator", ingest_soul_simulator_manifest),
        "fic": ("intelligence_compressor", ingest_intelligence_compressor),
        "vibra": ("vibrafsot", ingest_vibrafsot_progress),
        "symbolic": ("symbolic_encoding_graph", ingest_symbolic_encoding_graph),
    }
    selected = list(tasks.keys()) if args.only == "all" else [args.only]
    failed = 0
    for key in selected:
        label, fn = tasks[key]
        result = fn()
        if not result.get("ok"):
            print(f"FAIL {label}: {result.get('error')}", file=sys.stderr)
            failed += 1
        else:
            print(f"OK {label}: {result.get('vendor_path')}")
            if result.get("cache_path"):
                print(f"  cache: {result['cache_path']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())