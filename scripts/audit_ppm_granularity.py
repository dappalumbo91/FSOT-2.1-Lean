#!/usr/bin/env python3
"""Score gated scalars in parts per million, against the quoted last digit.

1% = 10,000 ppm. The 0.5% green gate is 5,000 ppm. The 0.05% aspiration
is 500 ppm. A residual inside half of the last quoted digit of the stored
measured value is table-limited: the comparison has run out of printed places.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from benchmark_margin_lib import classify_record  # noqa: E402

DATA = ROOT / "data"
OUT = DATA / "ppm_granularity.json"
BANDS = (1, 10, 100, 500, 1000, 5000)


def decimal_places(value: float) -> int:
    text = format(float(value), ".16g")
    if "e" in text:
        mantissa, exponent = text.split("e")
        exp = int(exponent)
        frac = len(mantissa.split(".")[1]) if "." in mantissa else 0
        return max(0, frac - exp) if exp < 0 else 0
    if "." not in text:
        return 0
    return len(text.split(".")[1])


def half_ulp_ppm(measured: float) -> float | None:
    if measured == 0:
        return None
    places = decimal_places(measured)
    half = 0.5 * (10.0 ** (-places))
    return half / abs(measured) * 1_000_000.0


def main() -> int:
    domains = []
    all_ppm: list[float] = []
    band_hits = {b: 0 for b in BANDS}
    table_limited = 0
    outside_table = []
    n = 0
    for path in sorted(DATA.glob("*_benchmark.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        records = doc.get("material_records") or doc.get("records") or []
        if not isinstance(records, list):
            continue
        domain_ppm: list[float] = []
        worst = None
        limited = 0
        for row in records:
            if not isinstance(row, dict):
                continue
            if classify_record(row, file_name=path.name) != "scalar":
                continue
            if row.get("error_pct") is None or row.get("measured") is None:
                continue
            try:
                err = abs(float(row["error_pct"]))
                measured = float(row["measured"])
            except (TypeError, ValueError):
                continue
            ppm = err * 10_000.0
            floor = half_ulp_ppm(measured)
            inside = floor is not None and ppm <= floor
            n += 1
            all_ppm.append(ppm)
            domain_ppm.append(ppm)
            if inside:
                table_limited += 1
                limited += 1
            else:
                outside_table.append(
                    {
                        "domain": doc.get("domain") or path.stem,
                        "file": path.name,
                        "name": row.get("name"),
                        "property": row.get("property"),
                        "measured": measured,
                        "error_ppm": ppm,
                        "half_digit_ppm": floor,
                    }
                )
            for band in BANDS:
                if ppm <= band:
                    band_hits[band] += 1
            if worst is None or ppm > worst["error_ppm"]:
                worst = {
                    "name": row.get("name"),
                    "property": row.get("property"),
                    "error_ppm": ppm,
                    "measured": measured,
                    "inside_quoted_digit": inside,
                }
        if not domain_ppm:
            continue
        domains.append(
            {
                "domain": doc.get("domain") or path.stem,
                "file": path.name,
                "scalar_count": len(domain_ppm),
                "median_ppm": median(domain_ppm),
                "max_ppm": max(domain_ppm),
                "table_limited": limited,
                "within_1_ppm": sum(1 for x in domain_ppm if x <= 1),
                "within_10_ppm": sum(1 for x in domain_ppm if x <= 10),
                "within_100_ppm": sum(1 for x in domain_ppm if x <= 100),
                "within_500_ppm": sum(1 for x in domain_ppm if x <= 500),
                "worst": worst,
            }
        )
    domains.sort(key=lambda d: -d["max_ppm"])
    outside_table.sort(key=lambda r: -r["error_ppm"])
    summary = {
        "scalar_count": n,
        "ppm_per_percent": 10_000,
        "green_gate_ppm": 5_000,
        "aspiration_ppm": 500,
        "within_ppm": {str(b): band_hits[b] for b in BANDS},
        "table_limited": table_limited,
        "outside_quoted_digit": n - table_limited,
        "median_ppm": median(all_ppm) if all_ppm else None,
        "domains": domains,
        "coarsest_outside_digit": outside_table[:40],
    }
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"scalars={n} median_ppm={summary['median_ppm']}")
    print(f"table_limited={table_limited} outside_digit={n - table_limited}")
    for band in BANDS:
        print(f"  within {band} ppm: {band_hits[band]}")
    print("coarsest outside the quoted digit:")
    for row in outside_table[:12]:
        print(
            f"  {row['error_ppm']:.1f} ppm  digit {row['half_digit_ppm']:.1f}  "
            f"{row['domain']}  {row['name']}  {row['property']}"
        )
    print("ppm_granularity_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
