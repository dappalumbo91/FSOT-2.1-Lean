#!/usr/bin/env python3
"""Living contested-sector watch document from prereg + closure artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTESTED = ROOT / "data" / "contested_observables_closure.json"
PREREG = ROOT / "predictions" / "preregistered_predictions_manifest.yaml"
OUT = ROOT / "predictions" / "reports" / "CONTESTED_SECTOR_WATCH.md"


def main() -> int:
    import yaml

    contested = json.loads(CONTESTED.read_text(encoding="utf-8")) if CONTESTED.is_file() else {}
    prereg = yaml.safe_load(PREREG.read_text(encoding="utf-8")) if PREREG.is_file() else {}
    cosmology_preds = [
        p for p in prereg.get("predictions") or []
        if p.get("domain") == "Cosmology" or "H0" in (p.get("name") or "") or "S8" in (p.get("name") or "")
    ]
    panel = contested.get("panel_summary") or {}
    ts = datetime.now(timezone.utc).isoformat()

    lines = [
        "# Contested Sector Watch",
        "",
        f"*Living monitor · {ts}*",
        "",
        contested.get("reframe", ""),
        "",
        f"| Metric | Value |",
        f"|--------|------:|",
        f"| Observables monitored | {panel.get('observable_count', 13)} |",
        f"| FSOT pooled median | {panel.get('pooled_median_error_pct', '?')}% |",
        f"| ΛCDM/SM typical baseline | {panel.get('current_model_baseline_pct', 15)}% |",
        f"| Beats baseline count | {panel.get('beats_baseline_count', '?')} |",
        "",
        "## Active observables",
        "",
        "| Observable | FSOT err % | Reference | Status |",
        "|------------|----------:|-----------|--------|",
    ]
    for ob in contested.get("observables") or []:
        lines.append(
            f"| {ob.get('name', '')} | {ob.get('fsot_error_pct', '')} | "
            f"{ob.get('reference', '')} | {ob.get('status', '')} |"
        )

    lines.extend(["", "## Preregistered cosmology locks", ""])
    for p in cosmology_preds[:8]:
        lines.append(
            f"- **{p.get('id')}** `{p.get('name')}` — FSOT {p.get('fsot_predicted')} {p.get('unit', '')} "
            f"vs {p.get('sota_label')} {p.get('sota_baseline')}; discriminant: {p.get('discriminant')}"
        )

    lines.extend([
        "",
        "## Future-observation ledger",
        "",
        "Pre-data differentiators (surveys not yet closed): "
        "`predictions/contested_future_observation_ledger.json` · "
        "`predictions/reports/CONTESTED_FUTURE_OBSERVATION_LEDGER.md`",
        "",
        "Discipline: [`docs/PREDATA_RISK.md`](../../docs/PREDATA_RISK.md) · freeze: `predictions/toe_prereg_freeze.json`",
        "",
        "Refresh: `python scripts/build_contested_observables_closure.py && "
        "python scripts/build_contested_sector_watch.py && "
        "python scripts/build_contested_future_observation_ledger.py`",
        "",
        "External authorities to monitor: Planck Collaboration (2018); Riess et al. (2024); DES Y3 σ₈; BBN lithium gap; DESI/Euclid/CMB-S4 class releases.",
        "",
    ])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())