#!/usr/bin/env python3
"""Sync FSOT NeuroLab fsot_compute.py from canonical authority."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY = Path(r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py")
NEUROLAB_TARGET = Path(r"C:\Users\damia\Desktop\FSOT NeuroLab\fsot_compute.py")
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

    if not AUTHORITY.exists():
        raise SystemExit(f"Authority missing: {AUTHORITY}")

    auth_digest = sha256_file(AUTHORITY)
    if NEUROLAB_TARGET.exists():
        old_digest = sha256_file(NEUROLAB_TARGET)
        if old_digest == auth_digest:
            print(f"NeuroLab already canonical ({auth_digest[:16]}...)")
            return 0
        backup = NEUROLAB_TARGET.with_suffix(NEUROLAB_TARGET.suffix + BACKUP_SUFFIX)
        if not args.dry_run:
            shutil.copy2(NEUROLAB_TARGET, backup)
            print(f"Backup: {backup}")

    if args.dry_run:
        print(f"Would copy {AUTHORITY} -> {NEUROLAB_TARGET}")
        return 0

    shutil.copy2(AUTHORITY, NEUROLAB_TARGET)
    stamp = datetime.now(timezone.utc).isoformat()
    print(f"Synced NeuroLab fsot_compute.py at {stamp}")
    print(f"  sha256 = {auth_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())