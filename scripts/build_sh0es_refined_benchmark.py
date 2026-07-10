#!/usr/bin/env python3
"""SH0ES per-host H0 refinement — Pantheon+SH0ES Cepheid hosts × bubble-density overlay."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "sh0es_refined_benchmark.json"
HOST_COORDS = ROOT / "data" / "sh0es_host_coordinates.json"
SH0ES_PARSED = Path(r"G:\FSOT-PublicData\anomaly_observables\sh0es\sh0es_hosts_parsed.json")
HOST_ALIASES = {
    "N1015": "NGC1015",
    "N1309": "NGC1309",
    "N1365": "NGC1365",
    "N1448": "NGC1448",
    "N2442": "NGC2442",
    "N3021": "NGC3021",
    "N3370": "NGC3370",
    "N3447": "NGC3447",
    "N3972": "NGC3972",
    "N3982": "NGC3982",
    "N4038": "NGC4038",
    "N4258": "NGC4258",
    "N4424": "NGC4424",
    "N4536": "NGC4536",
    "N4639": "NGC4639",
    "N5584": "NGC5584",
    "N5917": "NGC5917",
    "N7250": "NGC7250",
    "U9391": "UGC9391",
}
SECTOR_SEED = ROOT / "data" / "sector_h0_seed.json"

sys.path.insert(0, str(ROOT / "scripts"))
from bubble_bleed_physics import bubble_density_for_sector, sky_sector  # noqa: E402
from build_cosmology_bubble_bleed_benchmark import _h0_sector_records  # noqa: E402
from cosmology_anomalies_physics import load_auxiliary  # noqa: E402
from cosmology_lambda import H0_CANONICAL, load_fsot_compute  # noqa: E402
from fsot_paths import fsot_compute_path  # noqa: E402
from tier_gap_fill_lib import _bench_v11  # noqa: E402


def _error_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def _canonical_host(name: str) -> str:
    return HOST_ALIASES.get(name, name)


def _host_coords() -> dict[str, float]:
    out: dict[str, float] = {}
    if HOST_COORDS.exists():
        for row in json.loads(HOST_COORDS.read_text(encoding="utf-8")).get("hosts") or []:
            out[str(row["name"])] = float(row["ra_deg"])
    if SH0ES_PARSED.exists():
        for row in json.loads(SH0ES_PARSED.read_text(encoding="utf-8")):
            canonical = str(row.get("canonical_name") or _canonical_host(str(row["host"])))
            ra = float(row["ra_deg_mean"])
            out.setdefault(canonical, ra)
            out.setdefault(str(row["host"]), ra)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    sectors_doc = json.loads(SECTOR_SEED.read_text(encoding="utf-8"))
    bleed_frac = float(sectors_doc.get("bubble_bleed_fraction") or 0.015431)
    h0_global = float(sectors_doc.get("h0_global_fsot") or H0_CANONICAL)
    sh0es_measured = float(
        next(
            s["measured_h0"]
            for s in sectors_doc["sectors"]
            if s["name"] == "sh0es_jwst"
        )
    )

    sectors_doc_aux, nebulae, frbs = load_auxiliary()
    if not sectors_doc_aux:
        sectors_doc_aux = sectors_doc

    ra_map = _host_coords()
    parsed_hosts = {}
    if SH0ES_PARSED.exists():
        for row in json.loads(SH0ES_PARSED.read_text(encoding="utf-8")):
            count = int(row.get("cepheid_count") or 1)
            for key in (
                str(row.get("canonical_name") or ""),
                _canonical_host(str(row["host"])),
                str(row["host"]),
            ):
                if key:
                    parsed_hosts[key] = max(parsed_hosts.get(key, 0), count)

    host_computed: list[float] = []
    host_details: list[dict] = []
    for host, ra in sorted(ra_map.items()):
        density_sky = bubble_density_for_sector(nebulae, frbs, sky_sector(ra))
        computed = h0_global * (1.0 + density_sky * bleed_frac)
        host_computed.append(computed)
        host_details.append(
            {
                "host": host,
                "computed_h0": round(computed, 6),
                "ra_deg": round(ra, 4),
                "bubble_density_sky": round(density_sky, 4),
                "cepheid_count": parsed_hosts.get(host, 0),
            }
        )

    weights = [max(parsed_hosts.get(h, 1), 1) for h in ra_map]
    weighted_mean = sum(c * w for c, w in zip(host_computed, weights)) / sum(weights)
    median_computed = sorted(host_computed)[len(host_computed) // 2]

    records: list[dict] = [
        {
            "lab": "sh0es_refined_lab",
            "property": "host_h0_weighted_mean",
            "name": "SH0ES_cepheid_hosts_weighted",
            "computed": round(weighted_mean, 6),
            "measured": sh0es_measured,
            "error_pct": round(_error_pct(weighted_mean, sh0es_measured), 6),
            "host_count": len(ra_map),
            "method": "bubble_bleed_weighted_by_cepheid_count",
        },
        {
            "lab": "sh0es_refined_lab",
            "property": "host_h0_median",
            "name": "SH0ES_cepheid_hosts_median",
            "computed": round(median_computed, 6),
            "measured": sh0es_measured,
            "error_pct": round(_error_pct(median_computed, sh0es_measured), 6),
            "host_count": len(ra_map),
            "method": "bubble_bleed_median_sightline",
        },
    ]

    sector_recs = _h0_sector_records(sectors_doc_aux, nebulae, frbs)
    for row in sector_recs:
        if row.get("name") == "sh0es_jwst":
            continue
        records.append(
            {
                **row,
                "lab": "sh0es_refined_lab",
                "property": f"sector_h0_{row.get('name')}",
            }
        )

    errs = [float(r["error_pct"]) for r in records]
    doc = _bench_v11(
        domain="SH0ES_Refined",
        material_records=records,
        maps_to_lean=["cosmological", "blackhole", "cmb"],
        d_eff=25,
        authority_path=str(fsot_compute_path()),
        source=[
            "G:/FSOT-PublicData/anomaly_observables/sh0es",
            "data/sh0es_host_coordinates.json",
            "data/sector_h0_seed.json",
        ],
        channel_stats=[("sh0es", "per_host_h0_panel", errs)],
        sota_baselines={
            "per_host_h0_panel": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "Single H0 ignores sightline bubble structure",
            }
        },
    )
    doc["tier"] = 51
    doc["host_count"] = len(ra_map)
    doc["host_details"] = host_details
    doc["h0_global_fsot"] = h0_global
    doc["sh0es_measured_h0"] = sh0es_measured
    doc["sh0es_status"] = "GREEN" if (doc.get("pooled_median_error_pct") or 99) < 0.5 else "YELLOW"
    args.output.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  hosts={doc['host_count']}  pooled={doc['pooled_median_error_pct']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())