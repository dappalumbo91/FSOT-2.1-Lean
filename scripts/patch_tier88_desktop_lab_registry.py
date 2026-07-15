#!/usr/bin/env python3
"""Patch lab_registry.json with Tier 88 desktop wiring lab entries."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "lab_registry.json"
sys.path.insert(0, str(ROOT / "scripts"))

from tier88_desktop_extended_lib import DESKTOP_LAB_KEYS, patch_lab_registry  # noqa: E402
from tier88_verified_desktop_lib import VERIFIED_DESKTOP_LAB_KEYS  # noqa: E402


def _base_lab_entry(theme: str, lab_key: str) -> dict:
    return {
        "present": True,
        "wire_status": "tier88_live_panel",
        "desktop_theme": theme,
        "source_root": "vendor/application_wiring/tier88_cache",
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    all_keys = {**DESKTOP_LAB_KEYS, **VERIFIED_DESKTOP_LAB_KEYS}
    for theme, lab_key in all_keys.items():
        entry = registry.get(lab_key, {})
        if not isinstance(entry, dict):
            entry = {}
        entry.update(_base_lab_entry(theme, lab_key))
        registry[lab_key] = entry
    registry = patch_lab_registry(registry)
    registry["registry_version"] = registry.get("registry_version", "1.0")
    registry["tier88_desktop_patch_at"] = datetime.now(timezone.utc).isoformat()
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Patched {len(all_keys)} tier88 desktop labs into {REGISTRY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())