#!/usr/bin/env python3
"""
Sync FSOT-verified desktop project artifacts into the I: archive and vendor/ tree.

Makes the Lean hub independent of C:\\Users\\damia\\Desktop for Tier 88 panels.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR_VD = ROOT / "vendor" / "verified_desktop"
OUT = ROOT / "data" / "verified_desktop_sync_manifest.json"

DESKTOP = Path.home() / "Desktop"

# (desktop_relative, vendor_slug, archive_subpath, optional_subdir_within_desktop)
PROJECTS: tuple[tuple[str, str, str, str | None], ...] = (
    ("FSOT, Star Trek Transporter", "star_trek_transporter", "star_trek_transporter", None),
    ("Fuel Lab", "fuel_lab", "fuel_lab", "engine_simulator"),
    ("FSOT_BlackHole_WhiteHole", "blackhole_whitehole", "blackhole_whitehole", None),
)

SPECIES_SRC = DESKTOP / "FSOT_Machine_And_Molecule" / "fsot_species_catalog.json"
SPECIES_VENDOR = ROOT / "vendor" / "species" / "fsot_species_catalog.json"


def _archive_vd_root() -> Path | None:
    from fsot_paths import archive_root  # noqa: WPS433

    ar = archive_root()
    if ar is None:
        return None
    return ar / "08_Verified-Desktop-Projects"


def _copy_tree(src: Path, dst: Path, *, patterns: tuple[str, ...] | None = None) -> list[str]:
    copied: list[str] = []
    if not src.is_dir():
        return copied
    dst.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.rglob("*")):
        if not item.is_file():
            continue
        if patterns and not any(item.match(p) for p in patterns):
            continue
        if item.suffix.lower() in {".exe", ".pdb", ".o", ".lock"}:
            continue
        if "target" in item.parts or "node_modules" in item.parts or ".git" in item.parts:
            continue
        rel = item.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, out)
        copied.append(str(rel).replace("\\", "/"))
    return copied


def _copy_file(src: Path, dst: Path) -> bool:
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def main() -> int:
    archive_root_path = _archive_vd_root()
    rows: list[dict] = []

    for desktop_name, slug, archive_name, subdir in PROJECTS:
        src = DESKTOP / desktop_name
        if subdir:
            src = src / subdir
        vendor_dst = VENDOR_VD / slug
        if subdir:
            vendor_dst = vendor_dst / subdir
        vendor_dst.mkdir(parents=True, exist_ok=True)
        patterns = ("*.py", "*.json", "*.md", "*.js", "*.csv", "*.txt") if slug == "fuel_lab" else ("*",)
        vendor_files = _copy_tree(src, vendor_dst, patterns=patterns)
        archive_files: list[str] = []
        if archive_root_path is not None:
            archive_dst = archive_root_path / archive_name
            if subdir:
                archive_dst = archive_dst / subdir
            archive_files = _copy_tree(src, archive_dst, patterns=patterns)
        rows.append(
            {
                "slug": slug,
                "desktop_source": str(src),
                "vendor_dest": str(vendor_dst),
                "archive_dest": str(archive_root_path / archive_name) if archive_root_path else None,
                "files_copied_vendor": len(vendor_files),
                "files_copied_archive": len(archive_files),
            }
        )
        print(f"  {slug}: vendor={len(vendor_files)} archive={len(archive_files)}")

    species_ok = False
    if SPECIES_SRC.is_file():
        species_ok = _copy_file(SPECIES_SRC, SPECIES_VENDOR)
        if archive_root_path is not None:
            _copy_file(SPECIES_SRC, archive_root_path / "machine_and_molecule" / "fsot_species_catalog.json")
        rows.append(
            {
                "slug": "machine_and_molecule",
                "desktop_source": str(SPECIES_SRC),
                "vendor_dest": str(SPECIES_VENDOR),
                "species_synced": species_ok,
            }
        )

    # Push vendor transporter sim outputs to archive (pad B etc. may exist only in vendor)
    vd_transporter = VENDOR_VD / "star_trek_transporter"
    if archive_root_path is not None and vd_transporter.is_dir():
        archive_tp = archive_root_path / "star_trek_transporter"
        archive_tp.mkdir(parents=True, exist_ok=True)
        for item in vd_transporter.glob("*.json"):
            shutil.copy2(item, archive_tp / item.name)
        for item in vd_transporter.glob("*.py"):
            shutil.copy2(item, archive_tp / item.name)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(archive_root_path) if archive_root_path else None,
        "vendor_root": str(VENDOR_VD),
        "projects": rows,
        "policy": "Archive-first resolution via fsot_paths.verified_desktop_project(); Desktop is legacy fallback only.",
    }
    OUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())