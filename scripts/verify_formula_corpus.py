#!/usr/bin/env python3
"""Verify strict-empirical FSOT formulas: each record checked vs measured observable."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "formula_corpus_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from formula_corpus import load_strict_empirical_jsonl, summarize_formula_corpus  # noqa: E402


def verify_formula_corpus(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    ver = manifest.get("verification", {})
    corpus_path = Path(manifest["corpus_root"]) / manifest["artifacts"]["strict_empirical_jsonl"]["path"]
    issues: list[str] = []

    if not corpus_path.exists():
        return [f"missing strict_empirical corpus: {corpus_path}"], {}

    rows = load_strict_empirical_jsonl(corpus_path)
    live = summarize_formula_corpus(rows)
    live["corpus_path"] = str(corpus_path)

    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    if not registry.get("formula_corpus"):
        issues.append("formula_corpus: not ingested — run ingest_formula_corpus.py")

    checks = [
        ("records_min", "records_total"),
        ("matched_min", "matched_count"),
        ("within_target_2pct_min", "within_target_2pct"),
        ("within_tolerable_5pct_min", "within_tolerable_5pct"),
    ]
    for min_key, live_key in checks:
        floor = ver.get(min_key)
        if floor is not None and (live.get(live_key) or 0) < floor:
            issues.append(f"formula_corpus: {live_key}={live.get(live_key)} < {floor}")

    unmatched_max = ver.get("unmatched_max", 0)
    if (live.get("unmatched_count") or 0) > unmatched_max:
        issues.append(f"formula_corpus: unmatched_count={live.get('unmatched_count')}")

    return issues, {**live, "issues": len(issues)}


def main() -> int:
    issues, summary = verify_formula_corpus()
    print("=== Formula corpus verification (strict empirical) ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues:
            print(f"    - {item}")
        return 1
    print("  All formula corpus checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())