#!/usr/bin/env python3
"""Export a domain-scoped scientific reproduction bundle (manifest + optional file staging)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_domain_navigator_lib import bibtex_panel_entry, build_repro_bundle  # noqa: E402

DEFAULT_OUT = ROOT / "data" / "domain_repro_bundles"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export FSOT domain reproduction bundle")
    parser.add_argument("--core", help="Core domain name")
    parser.add_argument("--intent", help="Problem route intent slug")
    parser.add_argument("--panel", help="Single extension panel")
    parser.add_argument("--query", "-q", help="Keyword search to select panels")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT, help="Output root directory")
    parser.add_argument("--stage", action="store_true", help="Copy benchmark/source files into bundle dir")
    parser.add_argument("--run-verify", action="store_true", help="Run verify_extension_domains after export")
    parser.add_argument("--format", choices=("manifest", "bibtex"), default="manifest")
    args = parser.parse_args()

    if not any([args.core, args.intent, args.panel, args.query]):
        parser.error("Specify --core, --intent, --panel, or --query")

    bundle = build_repro_bundle(
        core=args.core,
        intent=args.intent,
        panel=args.panel,
        query=args.query,
    )
    bundle["exported_at"] = datetime.now(timezone.utc).isoformat()

    if args.format == "bibtex":
        entries = [bibtex_panel_entry(p["panel"], p) for p in bundle.get("panels") or []]
        print("\n\n".join(entries))
        return 0

    out_dir = args.output / bundle["bundle_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "repro_manifest.json"
    manifest_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    staged: list[str] = []
    if args.stage:
        files_dir = out_dir / "files"
        files_dir.mkdir(exist_ok=True)
        for rel in bundle.get("file_manifest") or []:
            src = (ROOT / rel).resolve()
            if not src.is_file():
                continue
            try:
                src.relative_to(ROOT.resolve())
            except ValueError:
                continue
            dest = (files_dir / rel).resolve()
            if src == dest:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            staged.append(str(dest.relative_to(out_dir)).replace("\\", "/"))
        bundle["staged_files"] = staged
        manifest_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    readme = out_dir / "REPRODUCE.txt"
    readme.write_text(
        "\n".join(
            [
                f"FSOT domain reproduction bundle: {bundle['bundle_id']}",
                f"Panels: {bundle['panel_count']}  Empirical records: {bundle['total_empirical_records']}",
                "",
                "From repository root:",
                *[f"  {cmd}" for cmd in bundle.get("reproduce_commands") or []],
                "",
                f"Manifest: {manifest_path.relative_to(ROOT)}",
                "Query tool: python scripts/query_fsot_domain_navigator.py --help",
            ]
        ),
        encoding="utf-8",
    )

    print(f"Wrote {manifest_path}")
    print(f"  panels: {bundle['panel_count']}  records: {bundle['total_empirical_records']}")
    if staged:
        print(f"  staged: {len(staged)} files")

    if args.run_verify:
        import subprocess

        rc = subprocess.call([sys.executable, str(ROOT / "scripts" / "verify_extension_domains.py")], cwd=ROOT)
        return rc

    return 0


if __name__ == "__main__":
    raise SystemExit(main())