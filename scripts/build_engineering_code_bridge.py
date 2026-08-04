#!/usr/bin/env python3
"""Build ESP32 engineering + coding structure verifier + hardware/code spine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from engineering_code_bridge_lib import BUILDERS, output_path  # noqa: E402


def main() -> int:
    # Ensure circuit catalog cache is warm
    from circuit_component_emergence_lib import (  # noqa: WPS433
        ingest_industry_catalog,
        build_circuit_component_emergence_panel,
        build_schematic_netlist_intrinsic_panel,
        build_tier_96_circuit_spine,
        output_path as circuit_out,
    )

    ingest_industry_catalog()
    for name, builder in (
        ("Circuit_Component_Emergence_Panel", build_circuit_component_emergence_panel),
        ("Schematic_Netlist_Intrinsic_Panel", build_schematic_netlist_intrinsic_panel),
        ("Tier_96_Circuit_Spine", build_tier_96_circuit_spine),
    ):
        doc = builder()
        circuit_out(name).write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{name}: n={doc.get('record_count')} med={doc.get('median_error_pct')}")

    for name, builder in BUILDERS.items():
        doc = builder()
        out = output_path(name)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(f"{name}: n={doc.get('record_count')} med={doc.get('median_error_pct')} -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
