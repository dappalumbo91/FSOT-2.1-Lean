#!/usr/bin/env python3
"""Verify Tier 96 founding-law panels are in Lean + cross-proof obligation spine."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
OBL_FORMAL = ROOT / "verification" / "obligations" / "full_formal_spine.json"
OBL_PRIORS = ROOT / "verification" / "obligations" / "full_priors_spine.json"
OUT = ROOT / "data" / "founding_laws_cross_proof_verification.json"

FOUNDING_MODULES = [
    "FoundingQuantumVacuumPanelPriors",
    "FoundingCosmicRayPanelPriors",
    "FoundingGalacticHaloRotationPanelPriors",
    "FoundingCosmicDustPanelPriors",
    "FoundingWhiteDwarfCoolingPanelPriors",
    "FoundingAtmosphericOzonePanelPriors",
    "FoundingPulsarGlitchPanelPriors",
]

FOUNDING_BUNDLES = [
    "founding_quantum_vacuum_panel_bundle",
    "founding_cosmic_ray_panel_bundle",
    "founding_galactic_halo_rotation_panel_bundle",
    "founding_cosmic_dust_panel_bundle",
    "founding_white_dwarf_cooling_panel_bundle",
    "founding_atmospheric_ozone_panel_bundle",
    "founding_pulsar_glitch_panel_bundle",
]


def _load_obligations(path: Path) -> list[dict]:
    if not path.exists():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    return doc.get("obligations") or []


def verify() -> dict:
    issues: list[str] = []
    lean_ok = True
    for mod in FOUNDING_MODULES:
        if not (FORMAL / f"{mod}.lean").exists():
            lean_ok = False
            issues.append(f"missing Lean module: {mod}.lean")

    lean_build_ok = False
    if lean_ok:
        targets = [f"FSOT.Formal.{m}" for m in FOUNDING_MODULES]
        proc = subprocess.run(
            ["lake", "build", *targets],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        lean_build_ok = proc.returncode == 0
        if not lean_build_ok:
            issues.append("Lean build failed for founding-law priors")
            issues.append((proc.stderr or proc.stdout)[-500:])

    formal_obs = _load_obligations(OBL_FORMAL)
    priors_obs = _load_obligations(OBL_PRIORS)
    formal_ids = {ob.get("id") for ob in formal_obs}
    priors_ids = {ob.get("id") for ob in priors_obs}

    bundle_hits = {bid: bid in formal_ids and bid in priors_ids for bid in FOUNDING_BUNDLES}
    for bid, hit in bundle_hits.items():
        if not hit:
            issues.append(f"bundle obligation missing from spine: {bid}")

    coq_hits = {}
    for bid in FOUNDING_BUNDLES:
        ob = next((o for o in formal_obs if o.get("id") == bid), None)
        coq_hits[bid] = bool(ob and ob.get("coq_id"))

    report = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "ok": lean_ok and lean_build_ok and all(bundle_hits.values()) and not issues,
        "lean_modules_present": lean_ok,
        "lean_build_ok": lean_build_ok,
        "bundle_obligations": bundle_hits,
        "coq_exported": coq_hits,
        "cross_proof_note": (
            "Founding-law panels export bundle conjuncts to full_formal_spine for "
            "Lean/Coq/Isabelle/Rust/F* numeric replay via run_cross_proof_verification.py"
        ),
        "issues": issues,
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    r = verify()
    print(json.dumps(r, indent=2))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())