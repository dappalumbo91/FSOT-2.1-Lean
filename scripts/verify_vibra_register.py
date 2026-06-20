#!/usr/bin/env python3
"""Verify VibraFSOT register experiment and FSOTLean MC alignment."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "vibra_register_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from vibra_register import load_mc_report, load_vibra_progress, summarize_vibra  # noqa: E402


def verify_vibra(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    vibra_root = Path(manifest["vibra_root"])
    lean_root = Path(manifest["fsotlean_root"])
    vibra_path = vibra_root / manifest["artifacts"]["vibra_progress"]["path"]
    mc_path = lean_root / manifest["artifacts"]["mc_report"]["path"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not vibra_path.exists():
        return [f"missing vibra progress: {vibra_path}"], {}
    if not mc_path.exists():
        return [f"missing MC report: {mc_path}"], {}

    live = summarize_vibra(load_vibra_progress(vibra_path), load_mc_report(mc_path))
    stored = registry.get("vibra_register", {})
    if not stored:
        issues.append("vibra_register: not ingested — run ingest_vibra_register.py")

    if live.get("d_eff") != ver.get("d_eff"):
        issues.append(f"vibra_register: d_eff={live.get('d_eff')} != expected {ver.get('d_eff')}")
    if (live.get("pattern_stability") or 0) < ver.get("pattern_stability_min", 0.5):
        issues.append("vibra_register: pattern_stability below minimum")
    if (live.get("vib_S_mean") or 0) <= ver.get("vib_avg_S_min", 0):
        issues.append("vibra_register: vib avg_S not positive")
    if (live.get("mc_trials") or 0) < ver.get("mc_trials_min", 1000):
        issues.append("vibra_register: MC trials below minimum")
    cp = str(ver.get("mc_checkpoint", 5))
    cp_stats_needed = ver.get("mc_prob_non_decrease_min", 0.99)
    if (live.get("mc_prob_non_decrease") or 0) < cp_stats_needed:
        issues.append(
            f"vibra_register: mc prob_non_decrease@{cp}={live.get('mc_prob_non_decrease')} < {cp_stats_needed}"
        )
    if (live.get("ai_avg_raw_S") or 0) > ver.get("ai_avg_raw_S_max", 0):
        issues.append("vibra_register: ai MC avg_raw_S should be non-positive (aligns Lean ai domain)")

    summary = {**live, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_vibra()
    print("=== VibraFSOT + FSOTLean MC verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All VibraFSOT / MC checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())