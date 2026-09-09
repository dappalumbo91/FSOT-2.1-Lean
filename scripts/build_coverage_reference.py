#!/usr/bin/env python3
"""Build docs/COVERAGE_REFERENCE.md from live JSON (477 green files, 35 cores)."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "COVERAGE_REFERENCE.md"


def main() -> None:
    margin = json.loads((ROOT / "data" / "benchmark_margin_audit.json").read_text(encoding="utf-8"))
    tree = json.loads((ROOT / "data" / "domain_family_tree.json").read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    domains = [d for d in margin.get("all_domains") or [] if not d.get("excluded")]
    cores = tree.get("cores") or []
    children = tree.get("children_by_core") or {}
    bands = tree.get("bands") or []

    lines: list[str] = []
    lines.append("# Coverage reference — what the program actually solves")
    lines.append("")
    lines.append(f"*Generated {stamp} · pin D1D38A*")
    lines.append("")
    lines.append("**Refresh:** `python scripts/build_coverage_reference.py`")
    lines.append("")
    lines.append("This is the **coverage ledger**, not a second theory.")
    lines.append("Green-file count **477/477** is what Label A scores.")
    lines.append("The 35 cores are the folds. Extensions are subdomains of a fold.")
    lines.append("Do not mix this with atlas-row (~403) or scalar-record (181,477) counts —")
    lines.append("see [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md).")
    lines.append("")
    lines.append("The flagship checklist paper cites this page. It does **not** reprint 477 files.")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append("| Ledger | Live |")
    lines.append("|--------|-----:|")
    lines.append(f"| Green residual files | **{margin.get('green_gate_pass_count')}/{margin.get('benchmark_file_count')}** |")
    lines.append(f"| Fail | **{margin.get('green_gate_fail_count')}** |")
    lines.append(f"| Unique domain names in the audit | {len({d.get('domain') for d in domains})} |")
    lines.append(f"| Core folds | {tree.get('core_count')} |")
    lines.append(f"| Extension subdomains | {tree.get('extension_count')} |")
    lines.append(f"| Atlas named rows | {tree.get('atlas_rows')} |")
    lines.append("")
    lines.append("## Core folds (the 35 interfaces)")
    lines.append("")
    lines.append("| Core | D_eff | observed | Band | Child extensions |")
    lines.append("|------|------:|:--------:|------|-----------------:|")
    for c in cores:
        name = c.get("name")
        n_ch = len(children.get(name) or [])
        obs = "yes" if c.get("observed") else "dark"
        lines.append(
            f"| **{name}** | {c.get('D_eff')} | {obs} | {c.get('band','')} | {n_ch} |"
        )
    lines.append("")
    lines.append("## Bands")
    lines.append("")
    for b in bands:
        if not isinstance(b, dict):
            lines.append(f"- {b}")
            continue
        lo, hi = b.get("lo"), b.get("hi")
        title = b.get("title") or ""
        said = b.get("said") or ""
        n_cores = len(b.get("cores") or [])
        lines.append(f"- **D={lo}–{hi} — {title}** ({n_cores} cores). {said}")
    lines.append("")
    lines.append("## Green files (reviewable list)")
    lines.append("")
    lines.append("Each row is one residual panel. Pooled median ≤ 0.5% is the official gate.")
    lines.append("")
    lines.append("| File | Domain | Records | Pooled % |")
    lines.append("|------|--------|--------:|---------:|")
    for d in sorted(domains, key=lambda x: str(x.get("file") or x.get("domain") or "")):
        pooled = d.get("official_pooled_median_error_pct")
        if pooled is None:
            pooled = d.get("pooled_median_error_pct")
        try:
            pooled_s = f"{float(pooled):.6f}"
        except (TypeError, ValueError):
            pooled_s = str(pooled)
        rec = d.get("records")
        lines.append(
            f"| `{d.get('file')}` | {d.get('domain')} | {rec} | {pooled_s} |"
        )
    lines.append("")
    lines.append("Query live:")
    lines.append("")
    lines.append("```powershell")
    lines.append("python scripts/audit_all_benchmark_margins.py")
    lines.append("python scripts/query_fsot_atlas.py --stats")
    lines.append("python scripts/query_fsot_domain_navigator.py")
    lines.append("```")
    lines.append("")
    lines.append("Related: [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md) · [`APPLY.md`](APPLY.md) ·")
    lines.append("[`WHY_NOT_CLAIMED.md`](WHY_NOT_CLAIMED.md) · [`WORKED_EXAMPLES.md`](WORKED_EXAMPLES.md).")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}  files={len(domains)}")


if __name__ == "__main__":
    main()
