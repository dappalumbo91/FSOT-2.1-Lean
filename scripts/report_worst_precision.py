#!/usr/bin/env python3
"""Report worst continuous precision records across 35-domain labs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from domain_precision_labs import LAB_EXTRACTORS  # noqa: E402

reg = yaml.safe_load((ROOT / "data/fsot_35_domain_registry.yaml").read_text(encoding="utf-8"))
records: list[dict] = []
for domain, cfg in (reg.get("empirical_sources") or {}).items():
    for lab in cfg.get("labs") or []:
        fn = LAB_EXTRACTORS.get(lab)
        if not fn:
            continue
        summary = fn(reg)
        for r in summary.get("records") or []:
            if r.get("error_pct") is None:
                continue
            err = float(r["error_pct"])
            if err >= 100:
                continue
            records.append({**r, "domain": domain})

records.sort(key=lambda x: x["error_pct"], reverse=True)
print("TOP 25 worst continuous (35-domain rollup):")
for r in records[:25]:
    print(
        f"  {r['error_pct']:7.4f}%  {r['domain']:22} "
        f"{str(r.get('property',''))[:24]:24} {r.get('name','')}"
    )
if records:
    print(f"\nGlobal worst: {records[0]['error_pct']:.4f}% — {records[0]['domain']} / {records[0].get('name')}")