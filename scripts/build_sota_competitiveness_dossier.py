#!/usr/bin/env python3
"""Generate publishable FSOT vs SOTA competitiveness dossier (Markdown + JSON)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_REPORT = ROOT / "data" / "sota_competitiveness_report.json"
OBS_REPORT = ROOT / "data" / "sota_observable_ledger_report.json"
OUTPUT_MD = ROOT / "data" / "sota_competitiveness_dossier.md"
OUTPUT_JSON = ROOT / "data" / "sota_competitiveness_dossier.json"
EXTERNAL_ROOT = Path("G:/FSOT-Cosmology-Lab/literature")


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    domain = _load(DOMAIN_REPORT)
    obs = _load(OBS_REPORT)
    dossier = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": "FSOT Zero-Parameter Competitiveness Dossier",
        "fsot_free_parameters": domain.get("fsot_free_parameters", 0),
        "domain_summary": {
            "domains_compared": domain.get("domains_compared"),
            "domains_beats_sota": domain.get("domains_beats_sota"),
            "beats_sota_fraction": domain.get("beats_sota_fraction"),
            "average_margin_vs_sota_pct": domain.get("average_margin_vs_sota_pct"),
            "aggregate_sota_free_parameters": domain.get("aggregate_sota_free_parameters"),
        },
        "observable_summary": {
            "observable_count": obs.get("observable_count"),
            "beats_or_meets_sota_count": obs.get("beats_or_meets_sota_count"),
            "below_sota_ids": obs.get("below_sota_ids"),
        },
        "domain_table": [
            {
                "domain": r["domain"],
                "fsot_median_error_pct": r.get("fsot_median_error_pct"),
                "sota_typical_error_pct": r.get("sota_typical_median_error_pct"),
                "delta_pct": r.get("margin_vs_sota_pct"),
                "sota_free_parameters": r.get("sota_free_parameters"),
                "status": r.get("status"),
            }
            for r in domain.get("domains") or []
        ],
        "observable_table": [
            {
                "id": r["id"],
                "domain": r.get("domain"),
                "name": r.get("name"),
                "fsot_error_pct": r.get("fsot_rmse") if r.get("comparison_metric") == "rmse" else r.get("fsot_error_pct"),
                "sota_typical_error_pct": r.get("sota_rmse") if r.get("comparison_metric") == "rmse" else r.get("sota_typical_error_pct"),
                "delta_pct": r.get("margin_vs_sota_pct"),
                "sota_free_parameters": r.get("sota_free_parameters"),
                "status": r.get("status"),
                "comparison_metric": r.get("comparison_metric"),
            }
            for r in obs.get("records") or []
        ],
        "lab_comparisons": domain.get("lab_comparisons") or [],
    }
    return dossier


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def write_markdown(dossier: dict, path: Path) -> None:
    ds = dossier["domain_summary"]
    os_ = dossier["observable_summary"]
    domain_rows = [
        [
            str(r["domain"]),
            f"{r['fsot_median_error_pct']:.3f}" if r.get("fsot_median_error_pct") is not None else "—",
            f"{r['sota_typical_error_pct']:.1f}",
            f"{r['delta_pct']:.2f}" if r.get("delta_pct") is not None else "—",
            str(r.get("sota_free_parameters", 0)),
            str(r.get("status", "")),
        ]
        for r in dossier["domain_table"]
    ]
    obs_rows = [
        [
            str(r["id"]),
            f"{r['fsot_error_pct']:.3f}" if r.get("fsot_error_pct") is not None else "—",
            f"{r['sota_typical_error_pct']:.1f}" if r.get("sota_typical_error_pct") is not None else "—",
            f"{r['delta_pct']:.2f}" if r.get("delta_pct") is not None else "—",
            str(r.get("sota_free_parameters", 0)),
            str(r.get("status", "")),
        ]
        for r in dossier["observable_table"]
    ]
    body = f"""# {dossier['title']}

Generated: {dossier['generated_at']}

## Executive summary

- **FSOT free parameters:** {dossier['fsot_free_parameters']}
- **Domains beating SOTA (median):** {ds.get('domains_beats_sota')}/{ds.get('domains_compared')} ({(ds.get('beats_sota_fraction') or 0)*100:.1f}%)
- **Average margin vs SOTA:** {ds.get('average_margin_vs_sota_pct', 0):.2f} percentage points
- **Aggregate SOTA parameters replaced:** {ds.get('aggregate_sota_free_parameters')}
- **Key observables beats/meets SOTA:** {os_.get('beats_or_meets_sota_count')}/{os_.get('observable_count')}

## Per-domain comparison

{_md_table(['Domain', 'FSOT median %', 'SOTA typical %', 'Δ (pp)', 'SOTA params', 'Status'], domain_rows)}

## Per-observable comparison

{_md_table(['Observable', 'FSOT err %', 'SOTA typical %', 'Δ (pp)', 'SOTA params', 'Status'], obs_rows)}
"""
    if os_.get("below_sota_ids"):
        body += f"\n## Priority gaps\n\nBelow SOTA: {', '.join(os_['below_sota_ids'])}\n"
    path.write_text(body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SOTA competitiveness dossier")
    parser.add_argument("--output-md", type=Path, default=OUTPUT_MD)
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    args = parser.parse_args()
    dossier = build()
    args.output_json.write_text(json.dumps(dossier, indent=2), encoding="utf-8")
    write_markdown(dossier, args.output_md)
    print(f"Wrote {args.output_json}")
    print(f"Wrote {args.output_md}")
    ext = EXTERNAL_ROOT
    if ext.exists():
        ext.mkdir(parents=True, exist_ok=True)
        (ext / "sota_competitiveness_dossier.md").write_text(
            args.output_md.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (ext / "sota_competitiveness_dossier.json").write_text(
            args.output_json.read_text(encoding="utf-8"), encoding="utf-8"
        )
        ledger = ROOT / "data" / "sota_observable_ledger_report.json"
        if ledger.exists():
            (ext / "sota_observable_ledger_report.json").write_text(
                ledger.read_text(encoding="utf-8"), encoding="utf-8"
            )
        print(f"Copied to {ext}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())