#!/usr/bin/env python3
"""Assemble FSOT_VERIFIED_SCOPE.yaml — public capability map for GitHub consumers."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "FSOT_VERIFIED_SCOPE.yaml"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def build_scope() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    progress = yaml.safe_load((ROOT / "data" / "fsot_verification_progress.yaml").read_text(encoding="utf-8"))
    cert = _load_json(ROOT / "data" / "certificate.json")
    sci = _load_json(ROOT / "data" / "scientific_domain_expansion_map.json")
    theory = yaml.safe_load((ROOT / "data" / "fsot_theory_crosswalk.yaml").read_text(encoding="utf-8"))
    ext = yaml.safe_load((ROOT / "data" / "extension_domains_manifest.yaml").read_text(encoding="utf-8"))

    extension_domains = []
    for dom in sci.get("extension_domains") or []:
        extension_domains.append(dom)
    for name, cfg in (ext.get("extension_domains") or {}).items():
        if any(d.get("domain") == name for d in extension_domains):
            continue
        bench = _load_json(ROOT / cfg["benchmark_data"])
        extension_domains.append(
            {
                "domain": name,
                "tier": cfg.get("tier"),
                "record_count": bench.get("record_count") or bench.get("observable_count"),
                "lean_module": cfg.get("lean_module"),
            }
        )

    lean_modules = sorted(
        {
            a.split("FSOT.Formal.")[-1]
            for t in (progress.get("tiers") or [])
            for a in (t.get("artifacts") or [])
            if "Priors" in a or a in ("CosmologyLab", "Domains", "Bounds", "Theorems")
        }
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "theory": theory.get("theory"),
        "verification_summary": progress.get("summary"),
        "current_tier": progress.get("current_position"),
        "proved_claims": cert.get("proved_claims") or progress.get("summary", {}).get("proved_claims"),
        "sorry_count": cert.get("sorry_count_formal", 0),
        "lean_build_ok": cert.get("lean_build_ok"),
        "scientific_domains_covered": sci.get("summary", {}).get("total_scientific_domains_covered"),
        "total_empirical_records": sci.get("summary", {}).get("total_empirical_records"),
        "tier_coverage": progress.get("tiers"),
        "extension_domains": extension_domains,
        "theory_crosswalk": theory.get("verified_extension_domains"),
        "lean_formal_modules": lean_modules,
        "certificate_path": "data/certificate.json",
        "reproduce": "python scripts/fsot_verification_runner.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    scope = build_scope()
    args.output.write_text(yaml.safe_dump(scope, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  domains: {scope.get('scientific_domains_covered')}  tiers: {scope['verification_summary'].get('tiers_complete')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())