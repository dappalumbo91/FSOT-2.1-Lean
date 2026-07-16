#!/usr/bin/env python3
"""Publish worst-domain / near-gate benchmark ledger for reviewer transparency."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "benchmark_margin_audit.json"
OUT_MD = ROOT / "data" / "publication" / "BENCHMARK_NEAR_MISS_LEDGER.md"
OUT_JSON = ROOT / "data" / "publication" / "benchmark_near_miss_ledger.json"


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    domains = [d for d in audit.get("all_domains") or [] if not d.get("excluded")]
    def _f(val: object) -> float:
        try:
            return float(val) if val is not None else 0.0
        except (TypeError, ValueError):
            return 0.0

    by_max = sorted(domains, key=lambda d: _f(d.get("max_gate_scalar_error_pct")), reverse=True)
    by_pooled = sorted(domains, key=lambda d: _f(d.get("pooled_median_error_pct")), reverse=True)
    tier_fails = [d for d in domains if d.get("tier_scalar_max_pass") is False]

    top_max = by_max[:15]
    top_pooled = by_pooled[:15]
    ts = datetime.now(timezone.utc).isoformat()

    lines = [
        "# Benchmark Near-Miss Ledger",
        "",
        f"*Generated: {ts}*",
        "",
        "Domains that pass the green gate but approach the ≤0.5% boundary — published for transparency, "
        "not hidden as post-hoc rescues.",
        "",
        f"| Gate | Value |",
        f"|------|------:|",
        f"| Green pass | {audit.get('green_gate_pass_count', '?')}/{audit.get('benchmark_file_count', '?')} |",
        f"| Worst max scalar (any domain) | {audit.get('worst_scalar_max_error_pct', '?')}% — `{audit.get('worst_scalar_domain', '')}` |",
        f"| Tier-scalar max fails | {audit.get('tier_scalar_fail_count', 0)} |",
        "",
        "## Top 15 by max single-record error (still green)",
        "",
        "| Domain | Records | Pooled median % | Max scalar % | Worst observable |",
        "|--------|--------:|----------------:|-------------:|------------------|",
    ]
    for d in top_max:
        lines.append(
            f"| {d.get('domain', '')} | {d.get('records', '')} | "
            f"{_f(d.get('pooled_median_error_pct')):.4f} | "
            f"{_f(d.get('max_gate_scalar_error_pct')):.4f} | "
            f"`{d.get('max_gate_scalar_name', '')}` / {d.get('max_gate_scalar_property', '')} |"
        )

    if tier_fails:
        lines.extend(["", "## Tier-scalar aspiration misses (extension gate unchanged)", ""])
        for d in tier_fails[:10]:
            lines.append(f"- **{d.get('domain')}**: tier_scalar_max_pass=false, pooled={d.get('pooled_median_error_pct')}%")

    lines.extend([
        "",
        "## Top 15 by pooled median (highest among green domains)",
        "",
        "| Domain | Pooled median % | Max scalar % |",
        "|--------|----------------:|-------------:|",
    ])
    for d in top_pooled:
        lines.append(
            f"| {d.get('domain', '')} | {_f(d.get('pooled_median_error_pct')):.4f} | "
            f"{_f(d.get('max_gate_scalar_error_pct')):.4f} |"
        )

    lines.extend([
        "",
        "Regenerate: `python scripts/build_benchmark_near_miss_ledger.py`",
        "",
    ])

    doc = {
        "generated_at": ts,
        "green_pass": audit.get("green_gate_pass_count"),
        "worst_scalar": {
            "domain": audit.get("worst_scalar_domain"),
            "error_pct": audit.get("worst_scalar_max_error_pct"),
        },
        "top_max_scalar": [
            {
                "domain": d.get("domain"),
                "max_scalar_error_pct": d.get("max_gate_scalar_error_pct"),
                "pooled_median_error_pct": d.get("pooled_median_error_pct"),
            }
            for d in top_max
        ],
    }
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())