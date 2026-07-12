#!/usr/bin/env python3
"""Sync optional NeuroLab fsot_compute.py from bundled vendor authority."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_paths import fsot_compute_path, neurolab_root  # noqa: E402

BACKUP_SUFFIX = ".pre_sync_backup"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync NeuroLab fsot_compute from authority")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    authority = fsot_compute_path()
    neurolab = neurolab_root(require=False)
    if neurolab is None:
        print("NeuroLab root not configured (set FSOT_NEUROLAB_ROOT). Skipping.")
        return 0
    target = neurolab / "fsot_compute.py"

    auth_digest = sha256_file(authority)
    if target.exists():
        old_digest = sha256_file(target)
        if old_digest == auth_digest:
            print(f"NeuroLab already canonical ({auth_digest[:16]}...)")
            return 0
        backup = target.with_suffix(target.suffix + BACKUP_SUFFIX)
        if not args.dry_run:
            shutil.copy2(target, backup)
            print(f"Backup: {backup}")

    if args.dry_run:
        print(f"Would copy {authority} -> {target}")
        return 0

    shutil.copy2(authority, target)
    stamp = datetime.now(timezone.utc).isoformat()
    print(f"Synced NeuroLab fsot_compute.py at {stamp}")
    print(f"  sha256 = {auth_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())