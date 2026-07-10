#!/usr/bin/env python3
"""Ingest nebula + weak-lensing catalog into cache."""

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
from nebula_lensing_lab import load_seed, merge_chime_nebula_overlays  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    seed_path = ROOT / src["nebula_seed"]
    cache_path = ROOT / src["nebula_cache"]
    rows = merge_chime_nebula_overlays(load_seed(seed_path))
    cache_path.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": str(seed_path),
                "nebula_count": len(rows),
                "nebulae": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {cache_path}")
    print(f"  nebulae: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())