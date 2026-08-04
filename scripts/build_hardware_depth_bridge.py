#!/usr/bin/env python3
"""Build cache / interconnect / C-parity / hardware-depth residual panels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hardware_depth_bridge_lib import BUILDERS, output_path  # noqa: E402


def main() -> int:
    order = [
        "FSOT_Cache_Hierarchy_Panel",
        "FSOT_Interconnect_Coherence_Panel",
        "FSOT_C_Pack_Parity_Panel",
        "FSOT_Hardware_Depth_Spine",
    ]
    # Ensure competitive refine exists for A_frac locality inputs (optional)
    refine = ROOT / "data" / "hardware_competitive_refine_report.json"
    if not refine.is_file():
        try:
            from hardware_competitive_refine_lib import run_full_refine  # noqa: WPS433

            run_full_refine()
            print("generated competitive refine for A_frac inputs")
        except Exception as e:
            print(f"note: competitive refine unavailable ({e})")

    for name in order:
        doc = BUILDERS[name]()
        out = output_path(name)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"{name}: n={doc.get('record_count')} med={doc.get('median_error_pct')} "
            f"pooled={doc.get('pooled_median_error_pct')} -> {out.name}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
