#!/usr/bin/env python3
"""Score the stored SH0ES ladder on each published uncertainty.

The chain is the Cepheid-count weighted mixture already in
data/sh0es_ladder_chain_benchmark.json. Rho 5.05 is not moved.
The frozen sightline files are not rewritten.
This script only prints.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from bubble_bleed_physics import ladder_chain_h0  # noqa: E402

# Riess et al. 2022, ApJL 934, L7: 73.04 ± 1.04
SHOES = (73.04, 1.04)
# Freedman et al. 2025, ApJ 985, 203: 70.39 ± 1.22 stat ± 1.33 sys ± 0.70 SN
_FREEDMAN_PARTS = (1.22, 1.33, 0.70)
FREEDMAN = (70.39, math.sqrt(sum(x * x for x in _FREEDMAN_PARTS)))
# Cited on the ladder rows: JWST Perfect Host arXiv:2509.01667; A&A 2026 network.
PERFECT = (73.49, 0.93)
AANDA = (73.50, 0.81)


def show(name: str, value: float, central: float, bar: float) -> None:
    gap = value - central
    side = "high" if gap >= 0 else "low"
    print(f"{name}={value} gap={gap} bar={bar} sigmas={abs(gap) / bar} side={side}")


def main() -> int:
    path = ROOT / "data" / "sh0es_ladder_chain_benchmark.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    mix = ladder_chain_h0(
        doc["objects"],
        h0_global=float(doc["h0_global_fsot"]),
        bleed_frac=float(doc["bubble_bleed_fraction"]),
    )
    print(f"weight_sum={mix['weight_sum']}")
    print(f"freedman_bar={FREEDMAN[1]}")
    show("chain_vs_sh0es", mix["h0_chain"], *SHOES)
    show("anchors_vs_freedman", mix["h0_anchors_only"], *FREEDMAN)
    show("hosts_vs_perfect", mix["h0_hosts_only"], *PERFECT)
    show("hosts_vs_aanda", mix["h0_hosts_only"], *AANDA)
    by_name = {row["name"]: row for row in doc["material_records"]}
    klass = float(by_name["SH0ES_class_bin_vs_R22"]["computed"])
    show("class_bin_vs_sh0es", klass, *SHOES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
