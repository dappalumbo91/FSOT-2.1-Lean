#!/usr/bin/env python3
"""FSOT CKM/PMNS — emerges from complex multi-sector interaction (zero free params).

Primary path: vendor/fsot_complex_interaction.py
  - Sector network (GR, EW, QCD, QED, FLAVOR_Q/L, HIGGS, ATOMIC)
  - Seed-locked κ_ij bleed couplings
  - Coupled equilibrium → emergent observables

PDG/NuFIT = comparison only.
"""

from __future__ import annotations

from typing import Any

from fsot_complex_interaction import run_complex_interaction_suite  # type: ignore


def run_ckm_pmns_suite() -> dict[str, Any]:
    return run_complex_interaction_suite()


if __name__ == "__main__":
    out = run_ckm_pmns_suite()
    print(f"n={out['record_count']} med%={out['median_error_pct']} max%={out['max_error_pct']}")
    print("method:", out["method"])
    for r in sorted(out["all_rows"], key=lambda x: -float(x["error_pct"]))[:15]:
        print(f"  {float(r['error_pct']):8.3f}%  {r['name']}")
