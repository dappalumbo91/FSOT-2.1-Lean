#!/usr/bin/env python3
"""Reproduce verification for one extension panel — ingest, build, verify."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"
sys.path.insert(0, str(ROOT / "scripts"))

from benchmark_margin_lib import analyze_benchmark  # noqa: E402
from fsot_domain_navigator_lib import enrich_panel  # noqa: E402


def _run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def verify_one(panel: str, cfg: dict) -> dict:
    bench_rel = cfg.get("benchmark_data")
    if not bench_rel:
        raise SystemExit(f"{panel}: no benchmark_data in manifest")
    path = ROOT / bench_rel
    if not path.exists():
        raise SystemExit(f"{panel}: missing {path}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    margin = analyze_benchmark(doc, file_name=path.name)
    return {
        "panel": panel,
        "record_count": doc.get("record_count") or doc.get("observable_count"),
        "pooled_median_error_pct": margin.get("official_pooled_median_error_pct"),
        "max_scalar_error_pct": margin.get("max_scalar_error_pct"),
        "classifier_accuracy_pct": margin.get("classifier_accuracy_pct"),
        "ok": margin.get("official_pooled_median_error_pct") is not None
        and float(margin.get("official_pooled_median_error_pct") or 99) <= 0.5,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Reproduce one FSOT extension panel")
    parser.add_argument("--panel", required=True, help="Extension panel name")
    parser.add_argument("--skip-ingest", action="store_true")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--deep", action="store_true", help="Pass --deep to ingest scripts")
    args = parser.parse_args()

    if yaml is None:
        raise SystemExit("PyYAML required")
    ext = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")).get("extension_domains") or {}
    if args.panel not in ext:
        raise SystemExit(f"Unknown panel: {args.panel}")
    cfg = ext[args.panel]
    py = sys.executable

    if cfg.get("ingest_script") and not args.skip_ingest:
        cmd = [py, str(ROOT / cfg["ingest_script"])]
        if args.deep:
            cmd.append("--deep")
        if _run(cmd) != 0:
            return 1

    build = cfg.get("build_script") or cfg.get("benchmark_script")
    if build and not args.skip_build:
        cmd = [py, str(ROOT / build), "--skip-ingest"]
        if _run(cmd) != 0:
            return 1

    result = verify_one(args.panel, cfg)
    detail = enrich_panel(args.panel, cfg)
    print(json.dumps({"verify": result, "scientific": detail.get("scientific")}, indent=2))
    print(f"\n{args.panel}: {'OK' if result['ok'] else 'FAILED'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())