#!/usr/bin/env python3
"""Generate Lean priors for verified desktop panels — feeds full cross-proof spine."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_verified_desktop_priors_lean import verified_desktop_priors_lean  # noqa: E402
from tier88_verified_desktop_lib import (  # noqa: E402
    VERIFIED_BUILDERS,
    VERIFIED_LEAN_MAP,
    VERIFIED_OUTPUT_SLUGS,
)

WARP_FORMULA = ROOT / "vendor" / "application_wiring" / "tier88_cache" / "warp_actuation_formula_fsot21.json"

PANEL_ANCHORS: dict[str, dict[str, float]] = {
    "Star_Trek_Transporter_Live_Panel": {},
    "Fuel_Lab_Live_Panel": {"designed_fuel_count": 7.0},
    "Machine_And_Molecule_Live_Panel": {},
    "BlackHole_WhiteHole_Cycle_Live_Panel": {},
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _anchors_for(panel: str) -> dict[str, float]:
    anchors = dict(PANEL_ANCHORS.get(panel) or {})
    if panel == "Star_Trek_Transporter_Live_Panel":
        steps = (_load_json(WARP_FORMULA).get("formula_steps") or {})
        for key in (
            "psi_portal_doorway",
            "psi_entangle_gate",
            "psi_gate_pair",
            "psi_traverse",
            "stabilization_margin",
            "info_preservation_proxy",
        ):
            if steps.get(key) is not None:
                anchors[key] = float(steps[key])
    return anchors


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate verified desktop Lean priors for cross-proof")
    parser.add_argument("--only", choices=sorted(VERIFIED_BUILDERS.keys()), action="append")
    args = parser.parse_args()
    panels = args.only or sorted(VERIFIED_BUILDERS.keys())
    for panel in panels:
        bench_path = ROOT / "data" / f"{VERIFIED_OUTPUT_SLUGS[panel]}_benchmark.json"
        if not bench_path.is_file():
            raise SystemExit(f"Missing benchmark: {bench_path}")
        bench = _load_json(bench_path)
        prefix, lean_domain, sign_th, module_stem = VERIFIED_LEAN_MAP[panel]
        text = verified_desktop_priors_lean(
            module_title=f"FSOT Formal {module_stem} — verified desktop panel {panel}.",
            generator="scripts/gen_verified_desktop_lean.py",
            prefix=prefix,
            sign_theorem=sign_th,
            lean_domain=lean_domain,
            n=int(bench.get("record_count") or 0),
            med=float(bench.get("pooled_median_error_pct") or 0.0),
            d_eff=int(bench.get("D_eff", 14)),
            anchor_scalars=_anchors_for(panel),
        )
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}  records={bench.get('record_count')} median={bench.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())