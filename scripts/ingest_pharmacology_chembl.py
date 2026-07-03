#!/usr/bin/env python3
"""Fetch ChEMBL approved drugs into pharmacology cache."""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "pharmacology_chembl_manifest.yaml"
CACHE = ROOT / "data" / "pharmacology_chembl_cache.json"


def fetch_chembl(base_url: str, max_phase: int, limit: int) -> list[dict]:
    params = {"format": "json", "max_phase": max_phase, "limit": limit}
    url = base_url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/pharmacology"})
    doc = json.loads(urllib.request.urlopen(req, timeout=60).read())
    molecules: list[dict] = []
    for row in doc.get("molecules") or []:
        props = row.get("molecule_properties") or {}
        formula = props.get("molecular_formula") or props.get("full_molformula")
        if props.get("full_mwt") is None or not formula:
            continue
        molecules.append(row)
    return molecules


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    spec = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    src = spec["source"]
    molecules = fetch_chembl(src["base_url"], int(src["max_phase"]), int(src["limit"]))
    CACHE.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source_url": src["base_url"],
                "molecule_count": len(molecules),
                "molecules": molecules,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {CACHE}")
    print(f"  ChEMBL molecules: {len(molecules)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())