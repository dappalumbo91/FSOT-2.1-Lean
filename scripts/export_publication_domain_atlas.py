#!/usr/bin/env python3
"""Export full FSOT domain atlas for monograph Appendix A (403 domains)."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "data" / "scientific_domain_expansion_map.yaml"
OUT_DIR = ROOT / "data" / "publication"


def _load_map() -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML required") from exc
    return yaml.safe_load(MAP.read_text(encoding="utf-8"))


def _rows(doc: dict) -> list[dict]:
    rows: list[dict] = []
    for kind, key in (("core", "neurolab_domains"), ("extension", "extension_domains")):
        for item in doc.get(key) or []:
            rows.append(
                {
                    "kind": kind,
                    "domain": item.get("domain"),
                    "lean_domain": item.get("lean_domain") or "",
                    "lean_module": item.get("lean_module") or "",
                    "tier": item.get("tier") or "",
                    "record_count": int(item.get("record_count") or item.get("empirical_records") or 0),
                    "median_error_pct": float(item.get("median_error_pct") or 0.0),
                    "coverage_tier": item.get("coverage_tier") or "",
                    "precision_status": item.get("precision_status") or "",
                    "labs": ";".join(item.get("labs") or []),
                }
            )
    rows.sort(key=lambda r: (r["kind"], r["domain"] or ""))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Export FSOT publication domain atlas")
    parser.add_argument("--format", choices=("all", "csv", "json", "latex"), default="all")
    args = parser.parse_args()

    doc = _load_map()
    rows = _rows(doc)
    summary = doc.get("summary") or {}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    atlas = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": str(MAP.relative_to(ROOT)),
        "summary": summary,
        "domain_count": len(rows),
        "core_count": sum(1 for r in rows if r["kind"] == "core"),
        "extension_count": sum(1 for r in rows if r["kind"] == "extension"),
        "total_empirical_records": int(summary.get("total_empirical_records") or 0),
        "domains": rows,
    }

    if args.format in ("all", "json"):
        out_json = OUT_DIR / "domain_atlas.json"
        out_json.write_text(json.dumps(atlas, indent=2), encoding="utf-8")
        print(f"Wrote {out_json}  domains={len(rows)}")

    if args.format in ("all", "csv"):
        out_csv = OUT_DIR / "domain_atlas.csv"
        with out_csv.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [])
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {out_csv}")

    if args.format in ("all", "latex"):
        lines = [
            "% FSOT Domain Atlas — auto-generated for monograph Appendix A",
            "\\begin{longtable}{llrrrl}",
            "\\toprule",
            "Kind & Domain & Records & Median err\\% & Tier & Lean \\\\",
            "\\midrule",
        ]
        for r in rows[:500]:
            dom = str(r["domain"]).replace("_", "\\_")
            lean = (r["lean_module"] or r["lean_domain"] or "").replace("_", "\\_")
            lines.append(
                f"{r['kind']} & {dom} & {r['record_count']} & {r['median_error_pct']:.6f} & "
                f"{r['coverage_tier']} & {lean} \\\\"
            )
        lines.extend(["\\bottomrule", "\\end{longtable}"])
        out_tex = OUT_DIR / "domain_atlas.tex"
        out_tex.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {out_tex}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())