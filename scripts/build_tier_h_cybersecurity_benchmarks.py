#!/usr/bin/env python3
"""Build Tier H (43) cybersecurity engineering benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tier_h_cybersecurity_lib import BUILDERS, output_path  # noqa: E402

BASE_ORDER = [
    "Cryptography_Technology",
    "Network_Internet_Protocols",
    "Secure_Software_Engineering",
]
DEPTH_ORDER = ["Malware_Threat_Intelligence", "Code_Genome_Structure"]
BUILD_ORDER = BASE_ORDER + DEPTH_ORDER + ["Zero_Day_Risk_Evaluator"]


def _write(domain: str) -> None:
    doc = BUILDERS[domain]()
    out = output_path(domain)
    out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    med = doc.get("pooled_median_error_pct")
    extra = ""
    if domain == "Zero_Day_Risk_Evaluator":
        extra = f" risk_tier={doc.get('risk_tier')} holes={doc.get('detected_hole_count')}"
    print(f"{domain}: {doc.get('record_count')} records, pooled median {med}%{extra} -> {out.name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()

    if args.only:
        if "Zero_Day_Risk_Evaluator" in args.only:
            for d in BUILD_ORDER:
                if d == "Zero_Day_Risk_Evaluator":
                    break
                if d not in args.only and d not in DEPTH_ORDER:
                    _write(d)
        for domain in args.only:
            _write(domain)
        return 0

    for domain in BASE_ORDER:
        _write(domain)
    print("Skipping depth domains — run scripts/build_tier_h_depth_benchmarks.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())