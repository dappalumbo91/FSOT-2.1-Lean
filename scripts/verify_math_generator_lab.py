#!/usr/bin/env python3
"""Verify Math Generator FSOT formula comparison report."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "math_generator_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from math_generator_lab import load_comparison_report, summarize_math_generator  # noqa: E402


def verify_math_generator(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    math_root = Path(manifest["math_generator_root"])
    report_path = math_root / manifest["artifacts"]["comparison_report"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not report_path.exists():
        return [f"missing math generator report: {report_path}"], {}

    live = summarize_math_generator(load_comparison_report(report_path))
    stored = registry.get("math_generator_lab", {})

    if not stored:
        issues.append("math_generator_lab: not ingested — run ingest_math_generator_lab.py")

    if (live.get("comparison_count") or 0) < ver.get("comparison_count_min", 5):
        issues.append(f"math_generator_lab: comparison_count={live.get('comparison_count')}")

    max_tol = ver.get("max_error_pct", 5.0)
    if (live.get("max_error_pct") or 0) > max_tol:
        issues.append(
            f"math_generator_lab: max_error_pct={live.get('max_error_pct'):.4f}% > {max_tol}%"
        )

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_math_generator()
    print("=== Math Generator Lab verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All Math Generator Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())