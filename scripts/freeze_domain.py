#!/usr/bin/env python3
"""Write a dated SHA-256 freeze. Values are not changed.

  python scripts/freeze_domain.py Plasma_Physics
  python scripts/freeze_domain.py --mapping
  python scripts/freeze_domain.py --ledger-a

A domain freeze is predictions/domain_freezes/<domain>.json.
--mapping writes predictions/domain_freezes/AEB2AD_mapping.json for every
current core and extension mapping, hashed with the live authority pin.
--ledger-a writes predictions/LEDGER_A_FREEZE_SHA256.json, the hash of
predictions/LEDGER_A_FREEZE.yaml. That yaml is not edited.
Existing preregistration files and benchmark values are left as they are.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))

EXTENSION = ROOT / "data" / "extension_folds_derived.json"
OUT_DIR = ROOT / "predictions" / "domain_freezes"
LEDGER_A = ROOT / "predictions" / "LEDGER_A_FREEZE.yaml"
AUTHORITY = ROOT / "vendor" / "fsot_compute.py"


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


def _write_new(path: Path, record: dict) -> int:
    if path.exists():
        print("freeze already exists", path.relative_to(ROOT).as_posix())
        print("Leave it. A new lock needs a new file name, not an edit of this one.")
        return 2
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(record, indent=2, allow_nan=False) + "\n").encode("utf-8"))
    return 0


def _authority_pin() -> tuple[str, str]:
    digest = hashlib.sha256(AUTHORITY.read_bytes()).hexdigest()
    return digest[:6].upper(), digest


def _all_domains() -> dict[str, dict]:
    import importlib

    compute = importlib.import_module("fsot_compute")
    names = list(compute.DOMAINS)
    if EXTENSION.is_file():
        folds = json.loads(EXTENSION.read_text(encoding="utf-8")).get("folds") or {}
        for name in folds:
            if name not in names:
                names.append(name)
    out: dict[str, dict] = {}
    for name in names:
        mapping = _extension(name) or _core(name)
        if mapping is not None:
            out[name] = mapping
    return out


def _freeze_mapping() -> int:
    pin, authority_sha = _authority_pin()
    domains = _all_domains()
    payload = {
        "authority_sha256": authority_sha,
        "domains": domains,
        "pin_prefix": pin,
    }
    digest = hashlib.sha256(_canonical(payload)).hexdigest()
    record = {
        "freeze_id": "AEB2AD-MAPPING",
        "pin_prefix": pin,
        "authority_file": "vendor/fsot_compute.py",
        "authority_sha256": authority_sha,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "domain_count": len(domains),
        "domains": domains,
        "mapping_sha256": digest,
        "note": (
            "Freeze of the current domain mapping at the live authority pin. "
            "No benchmark value was changed. predictions/toe_prereg_freeze.json "
            "stays the D1D38A preregistration and was not edited."
        ),
    }
    path = OUT_DIR / "AEB2AD_mapping.json"
    status = _write_new(path, record)
    if status == 0:
        print(path.relative_to(ROOT).as_posix(), digest, "domains", len(domains), "pin", pin)
    return status


def _freeze_ledger_a() -> int:
    raw = LEDGER_A.read_bytes()
    text = raw.decode("utf-8")
    pin_match = re.search(r"(?m)^pin:\s*(\S+)\s*$", text)
    generated = re.search(r"generated_at:\s*(\S+)", text)
    record = {
        "source": "predictions/LEDGER_A_FREEZE.yaml",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "hashed_at": datetime.now(timezone.utc).isoformat(),
        "header_pin": pin_match.group(1) if pin_match else None,
        "source_generated_at_comment": generated.group(1) if generated else None,
        "note": (
            "SHA-256 of predictions/LEDGER_A_FREEZE.yaml as stored, including "
            "line endings. The yaml was not modified. hashed_at is the day this "
            "hash was recorded. It is not the yaml comment date."
        ),
    }
    path = ROOT / "predictions" / "LEDGER_A_FREEZE_SHA256.json"
    status = _write_new(path, record)
    if status == 0:
        print(path.relative_to(ROOT).as_posix(), record["sha256"])
    return status


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--mapping":
        return _freeze_mapping()
    if len(sys.argv) == 2 and sys.argv[1] == "--ledger-a":
        return _freeze_ledger_a()
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print("usage: python scripts/freeze_domain.py <domain>|--mapping|--ledger-a")
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
    path = OUT_DIR / f"{name}.json"
    status = _write_new(path, record)
    if status == 0:
        print(path.relative_to(ROOT).as_posix(), digest)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
