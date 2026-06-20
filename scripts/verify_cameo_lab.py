#!/usr/bin/env python3
"""Verify Genetics CAMEO folding benchmarks and symbolic formula metadata."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "cameo_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from cameo_benchmarks import load_cameo_results, summarize_cameo  # noqa: E402


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_cameo(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    genetics_root = Path(manifest["genetics_root"])
    csv_path = genetics_root / manifest["artifacts"]["results_csv"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not csv_path.exists():
        return [f"missing CAMEO results: {csv_path}"], {}

    live_rows = load_cameo_results(csv_path)
    live_summary = summarize_cameo(live_rows, manifest.get("symbolic_formula"))
    stored = registry.get("cameo_lab", {})

    if not stored:
        issues.append("cameo_lab: not ingested — run ingest_cameo_lab.py")
    elif live_summary["benchmark_count"] != stored.get("benchmark_count"):
        issues.append(
            f"cameo_lab: benchmark_count={stored.get('benchmark_count')} != live {live_summary['benchmark_count']}"
        )

    if live_summary["benchmark_count"] < ver.get("benchmark_count_min", 100):
        issues.append(f"cameo_lab: only {live_summary['benchmark_count']} benchmarks")

    if live_summary["mean_top_l_prec"] < ver.get("top_l_prec_mean_min", 80.0):
        issues.append(
            f"cameo_lab: mean top-L prec {live_summary['mean_top_l_prec']:.2f}% < {ver.get('top_l_prec_mean_min')}%"
        )

    mae = float(manifest.get("symbolic_formula", {}).get("mae_angstrom", 8.85))
    if mae > ver.get("symbolic_mae_max", 15.0):
        issues.append(f"cameo_lab: symbolic MAE {mae} Å exceeds max")

    allowed = set(manifest.get("symbolic_formula", {}).get("constants", ["e", "pi", "phi"]))
    if not allowed.issubset({"e", "pi", "phi", "gamma"}):
        issues.append("cameo_lab: symbolic constants must be FSOT seed vocabulary")

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_cameo()
    print("=== CAMEO Lab verification ===")
    for k, v in summary.items():
        if k != "issues" and k != "rows":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:15]:
            print(f"    - {item}")
        return 1
    print("  All CAMEO Lab checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())