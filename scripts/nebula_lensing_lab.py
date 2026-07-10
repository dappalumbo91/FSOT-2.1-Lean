"""Nebula + weak-lensing catalog helpers for bubble-bleed verification."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen


def load_seed(seed_path: Path) -> list[dict[str, Any]]:
    doc = json.loads(seed_path.read_text(encoding="utf-8"))
    return list(doc.get("nebulae") or [])


def merge_chime_nebula_overlays(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pass-through with stable schema; future MAST/SIMBAD overlays attach here."""
    return rows


def fetch_optional_chime_frb_catalog(url: str, timeout: float = 30.0) -> list[dict[str, Any]]:
    """Optional network refresh hook (not used for nebulae; shared transport)."""
    with urlopen(url, timeout=timeout) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)