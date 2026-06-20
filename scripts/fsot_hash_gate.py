#!/usr/bin/env python3
"""SHA-256 hash gate for Desktop fsot_compute.py mirrors."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY_SHA256 = (
    "D1D38A185487B452E470AC68ECE2EB45AEB1CA9CE25FC9BF9564C19633FFBE70"
)
PRE_LEDGER_ALIGN_SHA256 = (
    "EE4E02C4CD658541C019AB6F1B0649926D9319F969231E17F4987389235A83B7"
)
EXTENDED_FORK_SHA256 = (
    "DB1FAA8A40B4BDFEC98DF14869E85A891C817AD549E341090A1889399868C493"
)
STALE_SHA256 = (
    "BF668F9E3682E7834545501BE6254E5149B0D409CE02B6976B96814E07645F57"
)

KNOWN_HASHES: dict[str, str] = {
    AUTHORITY_SHA256: "canonical",
    PRE_LEDGER_ALIGN_SHA256: "stale",
    EXTENDED_FORK_SHA256: "extended_fork",
    STALE_SHA256: "stale",
}


@dataclass(frozen=True)
class MirrorEntry:
    label: str
    path: Path
    role: str


DESKTOP_MIRRORS: tuple[MirrorEntry, ...] = (
    MirrorEntry(
        "authority",
        Path(r"C:\Users\damia\Desktop\FSOT document update\fsot_compute.py"),
        "canonical",
    ),
    MirrorEntry(
        "fsot_3_0",
        Path(r"C:\Users\damia\Desktop\Fsot3.0 code\fsot_compute.py"),
        "extended_fork",
    ),
    MirrorEntry(
        "cosmology_lab",
        Path(r"C:\Users\damia\Desktop\FSOT Cosmology Lab\fsot_compute.py"),
        "extended_fork",
    ),
    MirrorEntry(
        "smiles_lab",
        Path(r"C:\Users\damia\Desktop\FSOT SMILES Lab\fsot_compute.py"),
        "canonical",
    ),
    MirrorEntry(
        "neurolab",
        Path(r"C:\Users\damia\Desktop\FSOT NeuroLab\fsot_compute.py"),
        "canonical",
    ),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def classify_hash(digest: str) -> str:
    return KNOWN_HASHES.get(digest.upper(), "unknown")


def build_hash_gate_payload(source: Path) -> dict:
    digest = sha256_file(source)
    return {
        "authority_path": str(source),
        "authority_sha256": digest,
        "expected_sha256": AUTHORITY_SHA256,
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "known_hashes": {
            "canonical": AUTHORITY_SHA256,
            "pre_ledger_align": PRE_LEDGER_ALIGN_SHA256,
            "extended_fork": EXTENDED_FORK_SHA256,
            "stale": STALE_SHA256,
        },
        "mirrors": scan_mirrors(),
    }


def scan_mirrors() -> list[dict]:
    rows: list[dict] = []
    for entry in DESKTOP_MIRRORS:
        if not entry.path.exists():
            rows.append(
                {
                    "label": entry.label,
                    "path": str(entry.path),
                    "present": False,
                    "sha256": None,
                    "class": None,
                    "expected_role": entry.role,
                    "matches_expected": None,
                }
            )
            continue
        digest = sha256_file(entry.path)
        mirror_class = classify_hash(digest)
        rows.append(
            {
                "label": entry.label,
                "path": str(entry.path),
                "present": True,
                "sha256": digest,
                "class": mirror_class,
                "expected_role": entry.role,
                "matches_expected": mirror_class == entry.role,
            }
        )
    return rows


def check_authority(source: Path) -> tuple[bool, str, list[str]]:
    issues: list[str] = []
    digest = sha256_file(source)
    if digest != AUTHORITY_SHA256:
        mirror_class = classify_hash(digest)
        issues.append(
            "hash gate: loaded engine is not canonical "
            f"({mirror_class}, sha256={digest[:16]}...)"
        )
    return len(issues) == 0, digest, issues


def check_cache_gate(cache: dict, live_digest: str) -> list[str]:
    issues: list[str] = []
    gate = cache.get("hash_gate")
    if gate is None:
        issues.append("hash gate: canonical_constants.json missing hash_gate section")
        return issues

    cached = str(gate.get("authority_sha256", "")).upper()
    expected = str(gate.get("expected_sha256", AUTHORITY_SHA256)).upper()
    if expected != AUTHORITY_SHA256:
        issues.append("hash gate: cached expected_sha256 does not match registry")
    if cached != live_digest:
        issues.append("hash gate: cache authority_sha256 drifted from live engine")
    if live_digest != AUTHORITY_SHA256:
        issues.append("hash gate: live engine digest is not canonical authority")
    return issues