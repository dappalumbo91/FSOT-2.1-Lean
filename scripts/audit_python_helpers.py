#!/usr/bin/env python3
"""Audit helper scripts for hardcoded author paths and missing fsot_paths usage."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REPORT = ROOT / "data" / "python_helpers_audit.json"

HARDCODED_PATTERNS = (
    re.compile(r"C:\\Users\\damia", re.I),
    re.compile(r"C:/Users/damia", re.I),
    re.compile(r"Desktop/Knowledge base", re.I),
    re.compile(r"Desktop\\Knowledge base", re.I),
    re.compile(r"fsot code language", re.I),
)

ALLOWLIST = {
    "audit_python_helpers.py",
    "build_desktop_project_crosswalk.py",
    "build_fsot_20_domain_crosswalk.py",
    "build_fsot_systems_registry.py",
    "build_warp_bh_wh_portal_benchmark.py",
    "gen_warp_bh_wh_portal_lean.py",
    "fetch_weather_observed_benchmark.py",
    "fringe_desktop_ingest_lib.py",
    "fsot_hash_gate.py",
    "fsot_paths.py",
    "living_fsot_lib.py",
    "parse_neurolab_translations.py",
    "run_cross_proof_verification.py",
}


def audit_scripts() -> dict:
    findings: list[dict] = []
    for path in sorted(SCRIPTS.glob("*.py")):
        if path.name in ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = []
        for idx, line in enumerate(text.splitlines(), start=1):
            if "fsot_paths" in line and "import" in line:
                continue
            for pattern in HARDCODED_PATTERNS:
                if pattern.search(line):
                    hits.append({"line": idx, "text": line.strip()[:160]})
                    break
        if hits:
            uses_fsot_paths = "fsot_paths" in text
            findings.append(
                {
                    "script": path.name,
                    "hardcoded_hits": len(hits),
                    "uses_fsot_paths": uses_fsot_paths,
                    "samples": hits[:5],
                }
            )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scripts_scanned": len(list(SCRIPTS.glob("*.py"))),
        "scripts_with_hardcoded_paths": len(findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()
    doc = audit_scripts()
    args.report.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.report}")
    print(f"  scanned={doc['scripts_scanned']} hardcoded={doc['scripts_with_hardcoded_paths']}")
    for row in doc["findings"][:10]:
        print(f"  {row['script']}: {row['hardcoded_hits']} hit(s) fsot_paths={row['uses_fsot_paths']}")
    if args.fail_on_findings and doc["scripts_with_hardcoded_paths"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())