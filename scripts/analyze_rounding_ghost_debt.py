#!/usr/bin/env python3
"""Classify aspiration scalar debt: real formula gap vs literature rounding ghost."""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBT = ROOT / "data" / "extension_scalar_precision_debt.json"
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import classify_record  # noqa: E402
from scientific_measurement_lib import (  # noqa: E402
    display_precision_decimals,
    literature_aware_error_pct,
    relative_error_pct,
)


def _load_debt_domains() -> list[str]:
    if not DEBT.exists():
        return []
    doc = json.loads(DEBT.read_text(encoding="utf-8"))
    return [row["domain"] for row in doc.get("aspiration_debt") or []]


def _bench_path(domain: str) -> Path | None:
    try:
        import yaml

        spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        domains = spec.get("extension_domains") or spec.get("domains") or {}
        if isinstance(domains, dict):
            row = domains.get(domain) or {}
            rel = row.get("benchmark_data") or row.get("benchmark")
            return ROOT / rel if rel else None
        for row in domains:
            if row.get("name") == domain:
                rel = row.get("benchmark_data") or row.get("benchmark")
                return ROOT / rel if rel else None
    except Exception:
        pass
    return None


def _max_scalar_record(records: list[dict]) -> dict | None:
    best = None
    best_err = -1.0
    for r in records:
        if classify_record(r) != "scalar":
            continue
        e = r.get("error_pct")
        if e is None:
            continue
        ef = float(e)
        if ef > best_err:
            best_err = ef
            best = r
    return best


def main() -> int:
    domains = _load_debt_domains()
    if not domains:
        print("No aspiration debt domains in extension_scalar_precision_debt.json")
        return 0

    print("Rounding ghost analysis (aspiration debt max-scalar records)")
    print("-" * 100)
    ghosts = 0
    real = 0
    crosswalk = 0

    for domain in domains:
        path = _bench_path(domain)
        if not path or not path.exists():
            print(f"{domain}: benchmark missing")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        records = doc.get("material_records") or doc.get("records") or []
        row = _max_scalar_record(records)
        if not row:
            print(f"{domain}: no scalar max record")
            continue

        comp = float(row["computed"])
        meas = float(row["measured"])
        raw = float(row.get("error_pct") or relative_error_pct(comp, meas))
        aware = literature_aware_error_pct(comp, meas, row)
        dec = display_precision_decimals(meas, row)
        delta = comp - meas

        kind = aware.get("comparison_kind") or "raw"
        eff = float(aware.get("effective_error_pct") or raw)
        is_ghost = bool(aware.get("within_display_precision")) or (
            kind == "uncertainty_band" and eff <= 0.5
        )

        # Bridge rows compare two internal catalogs — not literature observables.
        if row.get("lab") == "materials_species_bridge" or row.get("species_property"):
            kind = "catalog_crosswalk"
            is_ghost = False
            crosswalk += 1
        elif is_ghost:
            ghosts += 1
        else:
            real += 1

        flag = "GHOST" if is_ghost else ("CROSSWALK" if kind == "catalog_crosswalk" else "REAL")
        name = row.get("name") or row.get("case_id") or "?"
        prop = row.get("property") or "?"
        print(
            f"{domain[:28]:<28} {flag:<9} raw={raw:6.3f}% eff={eff:6.3f}% "
            f"Δ={delta:+.6g} meas={meas:g} ({dec}dp) {prop}:{name}"
        )

    print("-" * 100)
    print(f"domains={len(domains)}  rounding_ghosts={ghosts}  catalog_crosswalk={crosswalk}  real_gaps={real}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())