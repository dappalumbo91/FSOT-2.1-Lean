#!/usr/bin/env python3
"""Orbital mechanics benchmark — Kepler third-law ratio vs unity."""

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
MANIFEST = ROOT / "data" / "orbital_mechanics_manifest.yaml"
CACHE = ROOT / "data" / "planetary_jpl_cache.json"
OUTPUT = ROOT / "data" / "orbital_mechanics_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_planetary_jpl.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    au_km = float(spec["source"]["au_km"])
    year_days = float(spec["source"]["earth_year_days"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from jpl_horizons_lab import (  # noqa: E402
        NASA_SEMI_MAJOR_AU,
        parse_physical_block,
        parse_soe_elements,
        resolve_semi_major_axis_au,
    )

    mod, authority_path = load_fsot_compute()
    S_astro = float(mod.domain_scalar("Astronomy"))

    records: list[dict] = []
    for body in doc.get("bodies") or []:
        text = body.get("horizons_text") or ""
        name = body.get("name") or ""
        phys = parse_physical_block(text)
        period_days = phys.get("period_days")
        soe = parse_soe_elements(text)
        ecc = float(soe.get("eccentricity") or 0.0)
        a_au = NASA_SEMI_MAJOR_AU.get(name) or resolve_semi_major_axis_au(name, text)
        if period_days is None or a_au is None:
            continue
        t_years = float(period_days) / year_days
        kepler_ratio = (t_years**2) / (a_au**3)
        target = 1.0
        tol_pct = 1.0 + abs(S_astro) * 0.5
        err = abs(kepler_ratio - target) / target * 100.0
        rec = {
            "lab": "orbital_mechanics_lab",
            "property": "kepler_third_law_ratio",
            "name": body.get("name"),
            "semi_major_au": round(float(a_au), 6),
            "period_years": round(t_years, 6),
            "computed": round(kepler_ratio, 6),
            "measured": target,
            "error_pct": round(err, 6),
            "within_tol": err <= tol_pct,
            "eccentricity": ecc,
        }
        if name == "Pluto" or ecc > 0.2:
            rec["eval_kind"] = "jpl_kepler"
            rec["note"] = "high_eccentricity_dwarf_kepler_closure"
        records.append(rec)

    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "JPL_Horizons_kepler",
        "record_count": len(records),
        "observable_count": len(records),
        "median_error_pct": sorted(errs)[len(errs) // 2] if errs else None,
        "D_eff": 18,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    doc = build()
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  bodies: {doc['record_count']}  median_err: {doc.get('median_error_pct')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())