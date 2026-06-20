#!/usr/bin/env python3
"""Verify Kronos FSOT metrology thesis run summary."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "kronos_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from kronos_lab import load_kronos_summary, summarize_kronos  # noqa: E402


def verify_kronos(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    kronos_root = Path(manifest["kronos_root"])
    csv_path = kronos_root / manifest["artifacts"]["run_summary"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not csv_path.exists():
        return [f"missing Kronos summary: {csv_path}"], {}

    live_rows = load_kronos_summary(csv_path)
    live = summarize_kronos(live_rows)
    stored = registry.get("kronos_lab", {})

    if not stored:
        issues.append("kronos_lab: not ingested — run ingest_kronos_lab.py")
    elif live["run_count"] != stored.get("run_count"):
        issues.append(
            f"kronos_lab: run_count={stored.get('run_count')} != live {live['run_count']}"
        )

    if live["run_count"] < ver.get("run_count_min", 100):
        issues.append(f"kronos_lab: only {live['run_count']} runs")

    best = live.get("best_fractional_error")
    if best is not None and best > ver.get("best_fractional_error_max", 1.0e-5):
        issues.append(f"kronos_lab: best_fractional_error={best:.2e} exceeds max")

    expected_unc = ver.get("record_fractional_uncertainty", 5.5e-19)
    unc = live.get("record_fractional_uncertainty")
    if unc is not None and abs(unc - expected_unc) > 1.0e-25:
        issues.append(f"kronos_lab: record_fractional_uncertainty={unc} != expected {expected_unc}")

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_kronos()
    print("=== Kronos Lab verification ===")
    for k, v in summary.items():
        if k != "issues" and k != "rows":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Kronos Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())