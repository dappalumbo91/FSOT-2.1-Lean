#!/usr/bin/env python3
"""Write a dated SHA-256 freeze of one domain mapping. Values are not changed.

  python scripts/freeze_domain.py Plasma_Physics

The new file is predictions/domain_freezes/<domain>.json. Existing preregistration
files and benchmark values are left as they are. A later evidence-tier run can
move the domain to confirmed only when a data release is dated after this freeze.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

EXTENSION = ROOT / "data" / "extension_folds_derived.json"
OUT_DIR = ROOT / "predictions" / "domain_freezes"


def _canonical(mapping: dict) -> bytes:
    return json.dumps(mapping, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _extension(name: str) -> dict | None:
    if not EXTENSION.is_file():
        return None
    folds = json.loads(EXTENSION.read_text(encoding="utf-8")).get("folds") or {}
    fold = folds.get(name)
    if not isinstance(fold, dict):
        return None
    return {
        "source": "data/extension_folds_derived.json",
        "parent_core": fold.get("parent_core"),
        "D_eff": fold.get("D_eff"),
        "look": fold.get("look"),
        "hits": fold.get("hits"),
        "observed": fold.get("observed"),
    }


def _core(name: str) -> dict | None:
    import importlib

    compute = importlib.import_module("fsot_compute")
    domain = compute.DOMAINS.get(name)
    if domain is None:
        return None
    return {
        "source": "vendor/fsot_compute.py",
        "D_eff": int(domain.D_eff),
        "look": str(domain.delta_psi),
        "hits": int(domain.hits),
        "delta_theta": str(domain.delta_theta),
        "observed": bool(domain.observed),
    }


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print("usage: python scripts/freeze_domain.py <domain>")
        return 2
    name = sys.argv[1]
    mapping = _extension(name) or _core(name)
    if mapping is None:
        print("unknown domain", name)
        return 2
    digest = hashlib.sha256(_canonical(mapping)).hexdigest()
    record = {
        "domain": name,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "mapping": mapping,
        "mapping_sha256": digest,
        "note": "Freeze of the current mapping only. No benchmark value was changed.",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.json"
    if path.exists():
        print("freeze already exists", path.relative_to(ROOT).as_posix())
        print("Leave it. A new lock needs a new file name, not an edit of this one.")
        return 2
    path.write_bytes((json.dumps(record, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    print(path.relative_to(ROOT).as_posix(), digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
