#!/usr/bin/env python3
"""Small-body orbit benchmark — JPL elements vs reference semi-major / Moon period."""

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
MANIFEST = ROOT / "data" / "small_body_orbits_manifest.yaml"
CACHE = ROOT / "data" / "small_body_jpl_cache.json"
OUTPUT = ROOT / "data" / "small_body_orbits_benchmark.json"


def build(manifest_path: Path = MANIFEST, cache_path: Path = CACHE) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not cache_path.exists():
        raise FileNotFoundError(f"Run ingest_small_body_jpl.py first: {cache_path}")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    doc = json.loads(cache_path.read_text(encoding="utf-8"))
    moon_ref = float(spec["source"]["moon_reference_days"])
    pert_tol = float(spec["source"]["perturbation_tol_pct"])

    sys.path.insert(0, str(ROOT / "scripts"))
    from fsot_canonical_adapter import load_fsot_compute  # noqa: E402
    from jpl_horizons_lab import (  # noqa: E402
        MOON_SEMI_MAJOR_KM,
        SMALL_BODY_SEMI_MAJOR_AU,
        parse_physical_block,
        parse_soe_elements,
    )

    mod, authority_path = load_fsot_compute()
    S_astro = float(mod.domain_scalar("Astronomy"))
    au_km = 149597870.7

    records: list[dict] = []
    for body in doc.get("bodies") or []:
        name = body.get("name") or ""
        text = body.get("horizons_text") or ""
        phys = parse_physical_block(text)
        soe = parse_soe_elements(text)

        if name == "Moon":
            period = phys.get("period_days")
            if period is None:
                continue
            err = abs(float(period) - moon_ref) / moon_ref * 100.0
            records.append(
                {
                    "lab": "small_body_orbits_lab",
                    "property": "lunar_orbit_period",
                    "name": name,
                    "computed": round(float(period), 6),
                    "measured": moon_ref,
                    "semi_major_km": MOON_SEMI_MAJOR_KM,
                    "eccentricity": soe.get("eccentricity"),
                    "error_pct": round(err, 6),
                    "within_tol": err <= pert_tol + abs(S_astro) * 2.0,
                }
            )
            continue

        ref_au = SMALL_BODY_SEMI_MAJOR_AU.get(name)
        computed_au = soe.get("semi_major_axis_au")
        if ref_au is None or computed_au is None:
            continue
        err = abs(float(computed_au) - ref_au) / ref_au * 100.0
        ecc = soe.get("eccentricity") or 0.0
        tol = pert_tol + abs(S_astro) * 2.0 + float(ecc) * 3.0
        records.append(
            {
                "lab": "small_body_orbits_lab",
                "property": "heliocentric_semi_major_axis",
                "name": name,
                "computed_au": round(float(computed_au), 6),
                "measured_au": ref_au,
                "eccentricity": ecc,
                "semi_major_km": round(float(computed_au) * au_km, 1),
                "error_pct": round(err, 6),
                "within_tol": err <= tol,
            }
        )

    errs = [r["error_pct"] for r in records]
    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "authority_path": str(authority_path),
        "source": "JPL_Horizons_small_bodies",
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