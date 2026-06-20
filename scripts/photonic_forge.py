"""FSOT Photonic V2 virtual crystal payload — shared by ingest and verification."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "canonical_constants.json"


def expected_resonance(trinary: int, poof: float, p_new: float) -> float:
    if trinary == -1:
        return -poof
    if trinary == 0:
        return 0.0
    if trinary == 1:
        return p_new
    raise ValueError(f"invalid trinary: {trinary}")


def load_vram_payload(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def photonic_constants() -> dict[str, float]:
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    l1 = cache["layer1"]
    l2 = cache["layer2"]
    return {
        "poof": float(l1["poof_factor"]),
        "p_new": float(l2["new_perceived_param"]),
    }


def summarize_photonic(voxels: list[dict]) -> dict:
    trinary_counts = {-1: 0, 0: 0, 1: 0}
    for v in voxels:
        t = int(v["trinary"])
        trinary_counts[t] = trinary_counts.get(t, 0) + 1
    return {
        "voxel_count": len(voxels),
        "trinary_counts": trinary_counts,
        "distinct_trinary_values": sorted(trinary_counts.keys()),
    }