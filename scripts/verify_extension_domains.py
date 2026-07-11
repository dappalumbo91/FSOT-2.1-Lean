#!/usr/bin/env python3
"""Verify extension domains — pooled median gate + scalar precision debt report."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
DEBT_REPORT = ROOT / "data" / "extension_scalar_precision_debt.json"

from benchmark_margin_lib import analyze_benchmark  # noqa: E402
from fsot_precision_constants import LEGACY_LOOSE_GATE_PCT, MAX_SCALAR_ERROR_PCT  # noqa: E402


def _record_count(doc: dict) -> int:
    for key in ("record_count", "observable_count", "month_count"):
        val = doc.get(key)
        if val is not None:
            return int(val)
    records = doc.get("records") or []
    if records:
        return len(records)
    nested = 0
    for val in doc.values():
        if isinstance(val, dict):
            for key in ("record_count", "observable_count", "month_count"):
                if val.get(key) is not None:
                    nested += int(val[key])
    return nested


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    ver = spec.get("verification") or {}
    min_records = int(ver.get("min_records_per_domain", 5))
    max_median = float(ver.get("max_median_error_pct", 0.5))
    aspiration_scalar = float(ver.get("aspiration_max_scalar_error_pct", MAX_SCALAR_ERROR_PCT))
    hard_scalar = float(ver.get("hard_max_scalar_error_pct", 2.0))
    tolerable_scalar = float(ver.get("tolerable_max_scalar_error_pct", LEGACY_LOOSE_GATE_PCT))
    min_classifier_acc = float(ver.get("min_classifier_accuracy_pct", 99.5))
    excluded = set(ver.get("excluded_benchmarks") or [])
    issues: list[str] = []
    aspiration_debt: list[dict] = []
    tolerable_debt: list[dict] = []

    for name, cfg in (spec.get("extension_domains") or {}).items():
        rel = cfg["benchmark_data"]
        if Path(rel).name in excluded:
            continue
        path = ROOT / rel
        if not path.exists():
            issues.append(f"{name}: missing {path}")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        n = _record_count(doc)
        margin = analyze_benchmark(doc, file_name=path.name)
        med = margin.get("official_pooled_median_error_pct")
        cls_acc = margin.get("classifier_accuracy_pct")
        max_scalar_err = margin.get("max_scalar_error_pct")
        print(
            f"  {name}: records={n} pooled={med} max_scalar={max_scalar_err} "
            f"classifier_acc={cls_acc if cls_acc is not None else 'n/a'}"
        )
        if n < min_records:
            issues.append(f"{name}: records {n} < {min_records}")
        if med is not None and float(med) > max_median:
            issues.append(f"{name}: pooled median {med} > {max_median}%")
        if max_scalar_err is not None:
            err_f = float(max_scalar_err)
            debt_row = {
                "domain": name,
                "max_scalar_error_pct": err_f,
                "property": margin.get("max_scalar_property"),
                "pooled_median_error_pct": med,
            }
            if err_f > aspiration_scalar:
                aspiration_debt.append(debt_row)
            if err_f > tolerable_scalar:
                tolerable_debt.append({**debt_row, "severity": "unacceptable"})
        if (
            margin.get("scalar_count", 0) > 0
            and max_scalar_err is not None
            and float(max_scalar_err) > hard_scalar
        ):
            issues.append(
                f"{name}: FSOT prediction max scalar {max_scalar_err}% > {hard_scalar}% "
                f"({margin.get('max_scalar_property')})"
            )
        if margin.get("classifier_count", 0) > 0 and not margin.get("classifier_pass"):
            issues.append(
                f"{name}: classifier accuracy {cls_acc}% < {min_classifier_acc}%"
            )

    debt_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "aspiration_max_scalar_error_pct": aspiration_scalar,
        "hard_max_scalar_error_pct": hard_scalar,
        "tolerable_max_scalar_error_pct": tolerable_scalar,
        "aspiration_debt_count": len(aspiration_debt),
        "unacceptable_scalar_count": len(tolerable_debt),
        "aspiration_debt": sorted(aspiration_debt, key=lambda x: -x["max_scalar_error_pct"]),
        "unacceptable_scalar_debt": sorted(tolerable_debt, key=lambda x: -x["max_scalar_error_pct"]),
        "note": (
            "Pooled median ≤0.5% is the hard pass gate. Per-record max scalar >0.5% is "
            "tracked here as precision debt — not silently ignored."
        ),
    }
    DEBT_REPORT.write_text(json.dumps(debt_doc, indent=2), encoding="utf-8")

    print("=== Extension domains verification ===")
    print(
        f"  scalar precision debt: {len(aspiration_debt)} domains > {aspiration_scalar}% "
        f"({len(tolerable_debt)} unacceptable > {tolerable_scalar}%)"
    )
    print(f"  wrote: {DEBT_REPORT}")
    if issues:
        for item in issues:
            print(f"  FAIL: {item}")
        return 1
    print("  All extension domain checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())