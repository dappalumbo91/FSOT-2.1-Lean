#!/usr/bin/env python3
"""Generate Lean priors for Tier 39 domains."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402
from tier39_propulsion_electrical_lib import BUILDERS, TIER39_DOMAINS, TIER39_LEAN  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=TIER39_DOMAINS, action="append")
    args = parser.parse_args()
    domains = args.only or TIER39_DOMAINS
    for domain in domains:
        bench_name, _ = BUILDERS[domain]
        bench = json.loads((ROOT / "data" / bench_name).read_text(encoding="utf-8"))
        prefix, lean_domain, sign_th, module_stem = TIER39_LEAN[domain]
        text = extension_priors_lean(
            module_title=f"FSOT Formal {module_stem} — Tier 39 ({domain}).",
            generator="scripts/gen_tier39_propulsion_electrical_lean.py",
            prefix=prefix,
            sign_theorem=sign_th,
            lean_domain=lean_domain,
            n=int(bench.get("record_count") or 0),
            med=float(bench.get("median_error_pct") or 0.0),
            d_eff=int(bench.get("D_eff", 12)),
        )
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())