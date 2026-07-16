#!/usr/bin/env python3
"""Copy Kronos from Desktop → I:/FSOT-Physical-Archive/06_Kronos-FluidLink (internal verification)."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "kronos_manifest.yaml"
FLUIDLINK_MANIFEST = ROOT / "data" / "fluidlink_local_manifest.yaml"
REPORT = ROOT / "data" / "publication" / "kronos_archive_sync_report.json"

DESKTOP_SRC = Path(r"C:\Users\damia\Desktop\Kronos")
ARCHIVE_ROOT = Path(r"I:\FSOT-Physical-Archive\06_Kronos-FluidLink")
ARCHIVE_DEST = ARCHIVE_ROOT / "Kronos"

SKIP_DIRS = {"__pycache__", ".git", "node_modules"}
SKIP_SUFFIX = {".exe", ".pdb"}


def _load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _should_skip(path: Path) -> bool:
    if path.name in SKIP_DIRS:
        return True
    if path.suffix.lower() in SKIP_SUFFIX and path.name not in {"go.exe"}:
        return True
    return False


def sync_tree(src: Path, dest: Path) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    copied = 0
    skipped = 0
    for item in src.rglob("*"):
        if _should_skip(item):
            skipped += 1
            continue
        rel = item.relative_to(src)
        if any(part in SKIP_DIRS for part in rel.parts):
            skipped += 1
            continue
        target = dest / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied += 1
    return {"files_copied": copied, "paths_skipped": skipped, "source": str(src), "dest": str(dest)}


def main() -> int:
    src = DESKTOP_SRC if DESKTOP_SRC.is_dir() else ARCHIVE_DEST
    if not src.is_dir():
        print(f"Kronos source not found: {DESKTOP_SRC}")
        return 1

    stats = sync_tree(DESKTOP_SRC, ARCHIVE_DEST) if DESKTOP_SRC.is_dir() else {"already_present": True}

    # Update kronos_manifest to prefer archive path
    doc = _load_yaml(MANIFEST)
    doc["kronos_root"] = str(ARCHIVE_DEST).replace("\\", "/")
    doc["kronos_root_fallback"] = str(DESKTOP_SRC).replace("\\", "/")
    doc["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    import yaml

    MANIFEST.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")

    fluidlink = {
        "version": "1.0",
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "title": "FluidLink local timing mesh (archive-internal)",
        "kronos_root": doc["kronos_root"],
        "fluidlink_hub_panel": "FPC_Temporal_Coupling",
        "tier": 50,
        "policy": "local_private_no_cloud",
        "commands": {
            "sync": "python scripts/sync_kronos_to_archive.py",
            "ingest": "python scripts/ingest_kronos_lab.py",
            "tier50": "python scripts/build_tier_o_time_emergence_benchmarks.py",
            "bundle": "python scripts/build_fluidlink_local_bundle.py",
        },
        "simulation_note": "Ground-up existence simulation scaffold — FPC timing edges + Kronos metrology feed Tier 50 spine.",
    }
    FLUIDLINK_MANIFEST.write_text(yaml.safe_dump(fluidlink, sort_keys=False, allow_unicode=True), encoding="utf-8")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sync": stats,
        "kronos_root": doc["kronos_root"],
        "archive_folder": str(ARCHIVE_ROOT),
        "all_ok": ARCHIVE_DEST.is_dir() and (ARCHIVE_DEST / "thesis_kronos_run_summary.csv").is_file(),
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Synced Kronos → {ARCHIVE_DEST}")
    print(f"  files: {stats.get('files_copied', '?')}  summary_csv: {report['all_ok']}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())