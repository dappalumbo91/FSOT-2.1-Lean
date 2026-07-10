#!/usr/bin/env python3
"""Ingest FRB repeater catalog into cache."""

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
MANIFEST = ROOT / "data" / "cosmology_bubble_bleed_manifest.yaml"
sys.path.insert(0, str(ROOT / "scripts"))
from frb_catalog_lab import (  # noqa: E402
    fetch_chime_catalog_with_fallback,
    load_literature_seed,
    load_seed,
    merge_catalog_rows,
)


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    seed_path = ROOT / src["frb_seed"]
    cache_path = ROOT / src["frb_cache"]
    rows = load_seed(seed_path)
    lit_path = ROOT / src.get("frb_literature_seed", "data/frb_literature_seed.json")
    literature = load_literature_seed(lit_path)
    if literature:
        rows = merge_catalog_rows(rows, literature)
    source_note = str(seed_path)
    if literature:
        source_note = f"{source_note}+literature"
    fetch_errors: list[str] = []
    if src.get("fetch_chime"):
        urls = [u for u in (src.get("chime_catalog_url"), src.get("chime_catalog_mirror")) if u]
        live, live_source, fetch_errors = fetch_chime_catalog_with_fallback(urls)
        if live:
            rows = merge_catalog_rows(rows, live)
            source_note = f"{source_note}+{live_source}"
            print(f"  CHIME live merge: +{len(live)} sources into {len(rows)} FRBs", file=sys.stderr)
        for err in fetch_errors:
            print(f"CHIME fetch skipped ({err})", file=sys.stderr)
    cache_path.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": source_note,
                "frb_count": len(rows),
                "fetch_errors": fetch_errors,
                "frbs": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {cache_path}")
    print(f"  FRBs: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())