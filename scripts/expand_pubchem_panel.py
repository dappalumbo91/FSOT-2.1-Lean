#!/usr/bin/env python3
"""Auto-expand PubChem CID panel via PUG REST name resolution.

Resolves preregistered seed queries and ChEMBL pharmacology drug names to CIDs,
deduplicates against existing panel files, validates live properties, and writes
vendor/public_data/pubchem/pubchem_auto_expansion.json.

Usage:
  python scripts/expand_pubchem_panel.py
  python scripts/expand_pubchem_panel.py --rebuild
  python scripts/expand_pubchem_panel.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR_PUBCHEM = ROOT / "vendor" / "public_data" / "pubchem"
SEED_MANIFEST = VENDOR_PUBCHEM / "pubchem_auto_seed_manifest.json"
AUTO_EXPANSION_PATH = VENDOR_PUBCHEM / "pubchem_auto_expansion.json"
PHARMACOLOGY_BENCH = ROOT / "data" / "pharmacology_benchmark.json"

PANEL_FILES = (
    VENDOR_PUBCHEM / "pubchem_preregistered_panel.json",
    VENDOR_PUBCHEM / "pubchem_culinary_expansion.json",
    AUTO_EXPANSION_PATH,
)

PUG_PROPERTIES = "MolecularWeight,MolecularFormula"


def _fetch_json(url: str, *, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/pubchem-expand"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_existing_cids() -> set[int]:
    seen: set[int] = set()
    for path in PANEL_FILES:
        if not path.exists():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for row in doc.get("compounds") or []:
            if row.get("cid") is not None:
                seen.add(int(row["cid"]))
    return seen


def resolve_name_to_cid(query: str) -> int | None:
    encoded = urllib.parse.quote(query, safe="")
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded}/cids/JSON"
    for attempt in range(3):
        try:
            payload = _fetch_json(url)
            cids = (payload.get("IdentifierList") or {}).get("CID") or []
            if cids:
                return int(cids[0])
            return None
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None


def validate_cids(cids: list[int]) -> set[int]:
    valid: set[int] = set()
    chunk_size = 50
    for i in range(0, len(cids), chunk_size):
        chunk = cids[i : i + chunk_size]
        cid_str = ",".join(str(c) for c in chunk)
        url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid_str}/"
            f"property/{PUG_PROPERTIES}/JSON"
        )
        payload: dict | None = None
        for attempt in range(3):
            try:
                payload = _fetch_json(url)
                break
            except Exception:
                time.sleep(0.4 * (attempt + 1))
        if payload is None:
            continue
        for props in (payload.get("PropertyTable") or {}).get("Properties") or []:
            cid = props.get("CID")
            mw = props.get("MolecularWeight")
            if cid is not None and mw is not None:
                valid.add(int(cid))
        time.sleep(0.25)
    return valid


def manifest_seeds() -> list[dict]:
    if not SEED_MANIFEST.exists():
        return []
    doc = json.loads(SEED_MANIFEST.read_text(encoding="utf-8"))
    return list(doc.get("seeds") or [])


def pharmacology_seeds() -> list[dict]:
    if not PHARMACOLOGY_BENCH.exists():
        return []
    doc = json.loads(PHARMACOLOGY_BENCH.read_text(encoding="utf-8"))
    out: list[dict] = []
    seen_names: set[str] = set()
    for row in doc.get("records") or []:
        raw = str(row.get("name") or row.get("display_name") or "").strip()
        if not raw:
            continue
        key = raw.lower()
        if key in seen_names:
            continue
        seen_names.add(key)
        slug = raw.lower().replace(" ", "_")
        out.append(
            {
                "query": raw,
                "name": slug,
                "category": "drug_pharmacology",
                "domain": "medical",
                "source": "pharmacology_benchmark",
            }
        )
    return out


def discover_compounds(*, include_pharmacology: bool = True) -> tuple[list[dict], dict]:
    existing = load_existing_cids()
    seeds = manifest_seeds()
    if include_pharmacology:
        seeds = pharmacology_seeds() + seeds

    resolved: list[dict] = []
    stats = {
        "queries_total": len(seeds),
        "resolved": 0,
        "skipped_existing": 0,
        "failed_resolve": 0,
        "failed_validate": 0,
    }

    pending: list[tuple[dict, int]] = []
    for seed in seeds:
        query = str(seed.get("query") or seed.get("name") or "").strip()
        if not query:
            continue
        cid = resolve_name_to_cid(query)
        time.sleep(0.2)
        if cid is None:
            stats["failed_resolve"] += 1
            continue
        if cid in existing:
            stats["skipped_existing"] += 1
            continue
        pending.append((seed, cid))
        existing.add(cid)

    candidate_cids = [cid for _, cid in pending]
    valid = validate_cids(candidate_cids)

    for seed, cid in pending:
        if cid not in valid:
            stats["failed_validate"] += 1
            continue
        stats["resolved"] += 1
        resolved.append(
            {
                "cid": cid,
                "name": seed.get("name") or f"cid_{cid}",
                "category": seed.get("category") or "auto_discovered",
                "domain": seed.get("domain") or "chemical",
                "query": seed.get("query"),
                "source": seed.get("source") or "pubchem_auto_seed_manifest",
            }
        )

    resolved.sort(key=lambda r: (str(r.get("domain")), str(r.get("category")), int(r["cid"])))
    return resolved, stats


def write_expansion(compounds: list[dict], stats: dict) -> None:
    doc = {
        "panel_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "description": "Automated PubChem panel expansion via PUG REST name resolution",
        "discovery_stats": stats,
        "compound_count": len(compounds),
        "compounds": [
            {
                "cid": c["cid"],
                "name": c["name"],
                "category": c["category"],
                "domain": c["domain"],
            }
            for c in compounds
        ],
    }
    AUTO_EXPANSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUTO_EXPANSION_PATH.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def run_rebuild_pipeline() -> int:
    env = os.environ.copy()
    env["FSOT_TIER68_DEEP"] = "1"
    env["FSOT_TIER38_DEEP"] = "1"
    steps = [
        [sys.executable, "scripts/ingest_tier68_live_ingest.py", "--deep", "--only", "pubchem_live"],
        [sys.executable, "scripts/ingest_tier38_public_data.py", "--deep", "--only", "pubchem"],
        [sys.executable, "scripts/build_tier38_public_data_benchmarks.py", "--only", "PubChem_Compound_Properties"],
        [sys.executable, "scripts/build_tier68_live_ingest_benchmarks.py", "--only", "PubChem_Live_Deep"],
        [sys.executable, "scripts/build_tier68_live_ingest_benchmarks.py", "--only", "Live_Ingest_Spine"],
        [sys.executable, "scripts/gen_tiers_68_70_lean.py"],
        [sys.executable, "scripts/verify_extension_domains.py"],
        [sys.executable, "scripts/audit_all_benchmark_margins.py"],
        [sys.executable, "scripts/run_cross_proof_verification.py"],
    ]
    for cmd in steps:
        print(f"\n=== {' '.join(cmd[1:])} ===")
        rc = subprocess.call(cmd, cwd=ROOT, env=env)
        if rc != 0:
            print(f"FAILED: {' '.join(cmd)}", file=sys.stderr)
            return rc
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-expand PubChem CID panel")
    parser.add_argument("--dry-run", action="store_true", help="Discover only; do not write or rebuild")
    parser.add_argument("--no-pharmacology", action="store_true", help="Skip ChEMBL pharmacology crosswalk")
    parser.add_argument("--rebuild", action="store_true", help="Run full ingest/benchmark/verify pipeline")
    args = parser.parse_args()

    compounds, stats = discover_compounds(include_pharmacology=not args.no_pharmacology)
    existing_n = len(load_existing_cids())
    print(f"Existing panel CIDs: {existing_n}")
    print(f"Discovery stats: {json.dumps(stats, indent=2)}")
    print(f"New compounds to add: {len(compounds)}")

    if args.dry_run:
        return 0

    write_expansion(compounds, stats)
    print(f"Wrote {AUTO_EXPANSION_PATH} ({len(compounds)} compounds)")
    print(f"Merged panel size: {existing_n + len(compounds)} unique CIDs")

    if args.rebuild:
        return run_rebuild_pipeline()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())