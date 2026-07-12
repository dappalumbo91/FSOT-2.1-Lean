#!/usr/bin/env python3
"""Sync optional lab fsot_compute.py mirrors from bundled vendor authority."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_paths import fsot_compute_path, lab_compute_sync_targets  # noqa: E402

BACKUP_SUFFIX = ".pre_sync_backup"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def sync_target(authority: Path, target: Path, auth_digest: str, dry_run: bool) -> str:
    if not target.exists():
        return f"missing: {target}"
    old = sha256_file(target)
    if old == auth_digest:
        return f"already canonical: {target.name}"
    if not dry_run:
        backup = target.with_suffix(target.suffix + BACKUP_SUFFIX)
        shutil.copy2(target, backup)
        shutil.copy2(authority, target)
    return f"synced: {target.name} ({old[:16]}... -> {auth_digest[:16]}...)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync lab fsot_compute mirrors (optional author dev)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    authority = fsot_compute_path()
    targets = lab_compute_sync_targets()
    if not targets:
        print("No lab compute targets configured (set FSOT_LAB_COMPUTE_TARGETS or lab roots).")
        return 0

    auth_digest = sha256_file(authority)
    for target in targets:
        print(sync_target(authority, target, auth_digest, args.dry_run))

    if not args.dry_run:
        print(f"Mirror sync at {datetime.now(timezone.utc).isoformat()}")
        print(f"  authority sha256 = {auth_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())