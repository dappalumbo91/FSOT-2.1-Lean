#!/usr/bin/env python3
"""Scan Math generator *_RULES.json corpora → formal observable registry."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "math_generator_rules_manifest.yaml"
OUTPUT = ROOT / "data" / "math_generator_rules_benchmark.json"


def _corpus_name(path: Path) -> str:
    stem = path.stem
    if stem.endswith("_RULES"):
        return stem[: -len("_RULES")]
    return stem


def _scan_corpora(mg_root: Path, dedupe_subdirs: list[str]) -> list[dict]:
    skip_dirs = {mg_root / rel for rel in dedupe_subdirs}
    corpora: list[dict] = []
    seen_names: set[str] = set()

    for path in sorted(mg_root.glob("*_RULES.json")):
        if any(skip in path.parents for skip in skip_dirs if skip.exists()):
            continue
        name = _corpus_name(path)
        if name in seen_names:
            continue
        seen_names.add(name)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"WARN: skip corrupt {path}: {exc}", file=sys.stderr)
            continue
        rules = data.get("rules") or []
        if not isinstance(rules, list):
            rules = []
        rule_ids = [r.get("id") for r in rules if isinstance(r, dict) and r.get("id")]
        corpora.append(
            {
                "corpus": name,
                "file": path.name,
                "schema_version": data.get("schema_version"),
                "knowledge_base": data.get("knowledge_base"),
                "document_source": data.get("document_source"),
                "rule_count": len(rules),
                "rule_ids_sample": rule_ids[:5],
            }
        )
    return corpora


def build_benchmark(manifest_path: Path = MANIFEST_PATH) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    spec = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    mg_root = Path(spec["source"]["math_generator_root"])
    if not mg_root.exists():
        raise FileNotFoundError(f"Math generator root missing: {mg_root}")

    dedupe = list(spec["source"].get("dedupe_subdirs") or [])
    corpora = _scan_corpora(mg_root, dedupe)
    total_rules = sum(c["rule_count"] for c in corpora)

    return {
        "benchmark_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(mg_root),
        "rule_corpus_count": len(corpora),
        "total_rule_count": total_rules,
        "observable_count": total_rules,
        "corpora": corpora,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        bench = build_benchmark(args.manifest)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(bench, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"  corpora: {bench['rule_corpus_count']}  rules: {bench['total_rule_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())