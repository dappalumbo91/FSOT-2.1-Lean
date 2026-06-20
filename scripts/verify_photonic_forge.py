#!/usr/bin/env python3
"""Verify FSOT Photonic V2 virtual crystal VRAM payload."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "photonic_manifest.yaml"
REGISTRY_PATH = ROOT / "data" / "lab_registry.json"

sys.path.insert(0, str(ROOT / "scripts"))
from photonic_forge import (  # noqa: E402
    expected_resonance,
    load_vram_payload,
    photonic_constants,
    summarize_photonic,
)


def load_manifest() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def verify_photonic(
    manifest_path: Path = MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> tuple[list[str], dict]:
    manifest = load_manifest()
    ver = manifest.get("verification", {})
    photonic_root = Path(manifest["photonic_root"])
    payload_path = photonic_root / manifest["artifacts"]["vram_payload"]
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    issues: list[str] = []

    if not payload_path.exists():
        return [f"missing photonic payload: {payload_path}"], {}

    voxels = load_vram_payload(payload_path)
    live_summary = summarize_photonic(voxels)
    stored = registry.get("photonic_forge", {})
    consts = photonic_constants()
    tol = ver.get("resonance_tolerance", 1e-4)
    allowed_trits = set(ver.get("trinary_values", [-1, 0, 1]))

    if not stored:
        issues.append("photonic_forge: not ingested — run ingest_photonic_forge.py")
    elif live_summary["voxel_count"] != stored.get("voxel_count"):
        issues.append("photonic_forge: voxel_count drift vs registry")

    if live_summary["voxel_count"] < ver.get("voxel_count_min", 180):
        issues.append(f"photonic_forge: only {live_summary['voxel_count']} voxels")

    if set(live_summary["distinct_trinary_values"]) - allowed_trits:
        issues.append("photonic_forge: invalid trinary values in payload")

    bad_res = 0
    for v in voxels:
        t = int(v["trinary"])
        exp = expected_resonance(t, consts["poof"], consts["p_new"])
        if abs(float(v["resonance"]) - exp) > tol:
            bad_res += 1
    if bad_res:
        issues.append(f"photonic_forge: {bad_res} voxels with resonance outside FSOT POOF/P_new mapping")

    summary = {**live_summary, "issues": len(issues)}
    return issues, summary


def main() -> int:
    issues, summary = verify_photonic()
    print("=== Photonic Forge verification ===")
    for k, v in summary.items():
        if k != "issues":
            print(f"  {k}: {v}")
    if issues:
        print(f"  FAIL: {len(issues)} issue(s)")
        for item in issues[:15]:
            print(f"    - {item}")
        return 1
    print("  All Photonic Forge checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())