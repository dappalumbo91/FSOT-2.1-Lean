#!/usr/bin/env python3
"""Ingest BlackHole thermo thesis observable table."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "blackhole_thesis_manifest.yaml"
REGISTRY = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from blackhole_thesis_lab import parse_thesis_table, summarize_blackhole  # noqa: E402


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    md = Path(manifest["thesis_root"]) / manifest["artifacts"]["thesis_md"]["path"]
    rows = parse_thesis_table(md)
    summary = summarize_blackhole(rows)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    registry["blackhole_thesis"] = {
        **summary,
        "observables": rows,
        "source_md": str(md),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Updated {REGISTRY}")
    print(f"  observables: {summary['observable_count']}  max_err: {summary['max_error_pct']:.4f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())