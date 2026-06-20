#!/usr/bin/env python3
"""Sync SMILES Lab and NeuroLab fsot_compute.py from canonical authority."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY = Path(r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py")
TARGETS = (
    Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\fsot_compute.py"),
    Path(r"C:\Users\damia\Desktop\FSOT NeuroLab\fsot_compute.py"),
)
BACKUP_SUFFIX = ".pre_sync_backup"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def sync_target(target: Path, auth_digest: str, dry_run: bool) -> str:
    if not target.exists():
        return f"missing: {target}"
    old = sha256_file(target)
    if old == auth_digest:
        return f"already canonical: {target.name}"
    if not dry_run:
        backup = target.with_suffix(target.suffix + BACKUP_SUFFIX)
        shutil.copy2(target, backup)
        shutil.copy2(AUTHORITY, target)
    return f"synced: {target.name} ({old[:16]}... -> {auth_digest[:16]}...)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync lab fsot_compute mirrors")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not AUTHORITY.exists():
        raise SystemExit(f"Authority missing: {AUTHORITY}")

    auth_digest = sha256_file(AUTHORITY)
    for target in TARGETS:
        print(sync_target(target, auth_digest, args.dry_run))

    if not args.dry_run:
        print(f"Mirror sync at {datetime.now(timezone.utc).isoformat()}")
        print(f"  authority sha256 = {auth_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())