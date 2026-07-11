#!/usr/bin/env python3
"""Rebuild all extension-domain benchmarks from manifest build scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "extension_domains_manifest.yaml"


def main() -> int:
    if yaml is None:
        print("FAIL: PyYAML required", file=sys.stderr)
        return 1
    spec = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    scripts: list[str] = []
    for _name, cfg in (spec.get("extension_domains") or {}).items():
        for key in ("build_script", "benchmark_script"):
            rel = cfg.get(key)
            if rel and rel not in scripts:
                scripts.append(rel)

    failed: list[str] = []
    print(f"=== Rebuilding {len(scripts)} extension benchmark scripts ===")
    for rel in sorted(scripts):
        path = ROOT / rel
        if not path.exists():
            print(f"  SKIP missing: {rel}")
            continue
        proc = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            failed.append(rel)
            print(f"  FAIL {rel}")
            if proc.stderr.strip():
                print(f"    {proc.stderr.strip()[:300]}")
        else:
            tail = (proc.stdout.strip() or proc.stderr.strip()).splitlines()
            print(f"  OK   {rel}" + (f" — {tail[-1]}" if tail else ""))

    if failed:
        print(f"FAIL: {len(failed)} build script(s) failed")
        return 1
    print("All extension benchmarks rebuilt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())