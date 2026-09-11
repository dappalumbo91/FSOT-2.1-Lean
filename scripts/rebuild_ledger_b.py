#!/usr/bin/env python3
"""Rebuild Ledger B stored residuals under f=ALPHA and live domain_scalar.

Does not touch seed_identity / structural rows. Does not rewrite dated forecasts.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import STRUCTURAL_EVAL_KINDS  # noqa: E402
from fsot_api_predict_lib import fsot_correct  # noqa: E402
from fsot_precision_constants import AUDIT_EXCLUDED_BENCHMARKS  # noqa: E402

SKIP_KIND = set(STRUCTURAL_EVAL_KINDS) | {
    "seed_identity",
    "seed_closed_form",
    "seed_math_identity",
    "seed_vs_nist_codata",
    "seed_vs_open_literature",
    "live_formula",
    "formula_mass_relay",
    "complex_system_emergence",
    "dynamics_definition",
    "dynamics_identity",
    "dynamics_channel",
    "dynamics_integration",
    "dimensional_interface",
    "framework_engine_channel",
    "observer_duality",
}
SKIP_PROP = {"kp", "ap_running", "time_tag", "computed_quiet", "measured_quiet"}
RESCORABLE = {"fsot_prediction", "fsot_correction", "scaled", "", "none"}
OUT = ROOT / "data" / "ledger_b_rebuild_report.json"


def _rescore_row(row: dict, file_domain: str | None) -> bool:
    kind = str(row.get("eval_kind") or row.get("kind") or "")
    if kind in SKIP_KIND:
        return False
    if kind not in RESCORABLE and kind:
        return False
    prop = str(row.get("property") or "")
    if prop in SKIP_PROP or "kp" in prop.lower():
        return False
    measured = row.get("measured")
    if not isinstance(measured, (int, float)) or float(measured) == 0.0:
        return False
    domain = str(row.get("fsot_domain") or row.get("domain") or file_domain or "")
    if not domain:
        return False
    try:
        computed, err = fsot_correct(float(measured), domain)
    except Exception:
        return False
    row["computed"] = computed
    row["error_pct"] = err
    row["eval_kind"] = "fsot_correction"
    row["ledger"] = "B"
    return True


def main() -> int:
    files = 0
    rows = 0
    changed = 0
    failed_files: list[str] = []
    for path in sorted((ROOT / "data").glob("*_benchmark.json")):
        if path.name in AUDIT_EXCLUDED_BENCHMARKS:
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        recs = doc.get("records")
        if not isinstance(recs, list):
            continue
        files += 1
        file_domain = str(doc.get("domain") or "")
        n_ch = 0
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            rows += 1
            if _rescore_row(rec, file_domain):
                n_ch += 1
                changed += 1
        if n_ch:
            doc["ledger_b_rebuilt_at"] = datetime.now(timezone.utc).isoformat()
            path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_seen": files,
        "rows_seen": rows,
        "rows_rescored": changed,
        "failed_files": failed_files,
        "note": "Ledger B only. f=ALPHA. seed identities untouched.",
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
