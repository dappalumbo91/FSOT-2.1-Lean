#!/usr/bin/env python3
"""Compare the alpha gap with the sector interfaces already in the engine.

The wave-2 leaf sits 1.45 ppm high. The network nudge is
(POOF*SUCTION)^2 times an interface difference. This prints the interface
difference that would land on the CODATA value, then the interfaces the
coupled system actually has. It does not change the leaf.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
import fsot_compute as F  # noqa: E402
from fsot_complex_interaction import coupled_equilibrium, yin_yang_fraction  # noqa: E402

TARGET = 137.035999177


def interface(state: dict, a: str, b: str) -> float:
    return abs(state[a] - state[b]) / max(abs(state[a]) + abs(state[b]), 1e-30)


def main() -> int:
    leaf = float(F.E**3 * F.PHI**4 - F.PSI_CON)
    yy = float((F.POOF * F.SUCTION) ** 2)
    needed = (leaf - TARGET) / yy
    eq = coupled_equilibrium()
    bare, coupled = eq["S_bare"], eq["S_coupled"]
    mix = yin_yang_fraction()
    names = sorted(coupled)
    rows = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            mixed = (1.0 - mix) * interface(bare, a, b) + mix * interface(coupled, a, b)
            rows.append((abs(mixed - needed), mixed, a, b))
    rows.sort()
    print(f"leaf={leaf:.12f}")
    print(f"needed_interface={needed:.6f}")
    print(f"yin_yang={mix:.6f}")
    print("closest interfaces")
    for _, mixed, a, b in rows[:8]:
        shifted = leaf - yy * mixed
        ppm = (shifted - TARGET) / TARGET * 1e6
        print(f"  {a}-{b} {mixed:.4f}  would leave {ppm:+.3f} ppm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
