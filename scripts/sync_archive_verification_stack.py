#!/usr/bin/env python3
"""Sync local verification stack → I:/FSOT-Physical-Archive/09_Local-Verification-Stack."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = Path(r"I:\FSOT-Physical-Archive\09_Local-Verification-Stack")
REPORT = ROOT / "data" / "publication" / "archive_verification_sync_report.json"

COPY_FILES = [
    "data/fluidlink_local_manifest.yaml",
    "data/kronos_manifest.yaml",
    "data/desktop_observer_loop_panel_benchmark.json",
    "data/existence_simulation_gap_fill_panel_benchmark.json",
    "data/existence_simulation_refinement_panel_benchmark.json",
    "data/existence_simulation_failure_clusters_manifest.yaml",
    "data/publication/existence_refinement_report.json",
    "data/domain_coupling_simulation_benchmark.json",
    "data/publication/fluidlink_local_bundle_report.json",
    "data/publication/kronos_archive_sync_report.json",
    "data/publication/existence_simulation_report.json",
    "data/publication/independent_prediction_ledger.yaml",
    "data/publication/independent_prediction_verification_report.json",
    "data/publication/CREDIBILITY_HARDENING_AUDIT.md",
    "data/practical_pipeline_manifest.yaml",
    "docs/CONSCIOUSNESS_OBSERVER_ARCHITECTURE.md",
    "docs/PRACTICAL_PIPELINE.md",
]

COPY_DIRS = [
    "data/desktop_observer_loop",
    "data/existence_simulation",
]

COPY_SCRIPTS = [
    "scripts/existence_simulation_lib.py",
    "scripts/run_existence_simulation.py",
    "scripts/build_existence_simulation_benchmark.py",
    "scripts/build_archive_existence_bundle.py",
    "scripts/verify_independent_predictions.py",
    "scripts/existence_simulation_refinement_lib.py",
    "scripts/ring_in_existence_failures.py",
    "scripts/build_existence_refinement_benchmark.py",
    "scripts/build_fluidlink_local_bundle.py",
    "scripts/sync_kronos_to_archive.py",
    "scripts/desktop_observer_loop_lib.py",
    "scripts/run_desktop_observer_loop.py",
    "scripts/build_desktop_observer_loop_benchmark.py",
]


def _copy_file(src: Path, dest: Path) -> bool:
    if not src.is_file():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return True


def _copy_tree(src: Path, dest: Path) -> int:
    if not src.is_dir():
        return 0
    count = 0
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        count += 1
    return count


def main() -> int:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": "1.0",
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "title": "FSOT Local Verification Stack (I: archive mirror)",
        "source_repo": str(ROOT).replace("\\", "/"),
        "archive_root": str(ARCHIVE_ROOT).replace("\\", "/"),
        "policy": {
            "esp32": "deferred",
            "observer": "timing+display_proxy (no mic/camera)",
            "existence_simulation": "seed-derived synthetic gap fill + independent predictions",
        },
        "entry_commands": {
            "fluidlink_bundle": "python scripts/build_fluidlink_local_bundle.py",
            "existence_bundle": "python scripts/build_archive_existence_bundle.py",
            "existence_sim": "python scripts/run_existence_simulation.py",
        },
    }

    files_ok = 0
    files_missing: list[str] = []
    for rel in COPY_FILES:
        src = ROOT / rel
        dest = ARCHIVE_ROOT / rel
        if _copy_file(src, dest):
            files_ok += 1
        else:
            files_missing.append(rel)

    dir_counts: dict[str, int] = {}
    for rel in COPY_DIRS:
        src = ROOT / rel
        dest = ARCHIVE_ROOT / rel
        dir_counts[rel] = _copy_tree(src, dest)

    scripts_ok = 0
    for rel in COPY_SCRIPTS:
        if _copy_file(ROOT / rel, ARCHIVE_ROOT / rel):
            scripts_ok += 1

    if yaml is not None:
        (ARCHIVE_ROOT / "verification_stack_manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(ARCHIVE_ROOT),
        "files_copied": files_ok,
        "files_missing": files_missing,
        "dir_file_counts": dir_counts,
        "scripts_copied": scripts_ok,
        "all_ok": files_ok >= 6 and scripts_ok >= 5,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    _copy_file(REPORT, ARCHIVE_ROOT / "data" / "publication" / "archive_verification_sync_report.json")

    print(f"Synced verification stack → {ARCHIVE_ROOT}")
    print(f"  files: {files_ok}  dirs: {sum(dir_counts.values())}  scripts: {scripts_ok}")
    if files_missing:
        print(f"  missing (optional): {len(files_missing)}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())