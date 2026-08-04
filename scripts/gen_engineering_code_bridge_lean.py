#!/usr/bin/env python3
"""Generate Lean priors for ESP32 / coding-structure / engineering spine panels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402
from engineering_code_bridge_lib import BUILDERS, LEAN_MAP, output_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=sorted(BUILDERS.keys()), action="append")
    args = parser.parse_args()
    for domain in args.only or sorted(BUILDERS.keys()):
        bench_path = output_path(domain)
        if not bench_path.is_file():
            print(f"Skip {domain}: run build_engineering_code_bridge.py first")
            continue
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        prefix, lean_domain, sign_th, module_stem = LEAN_MAP[domain]
        text = extension_priors_lean(
            module_title=(
                f"FSOT Formal {module_stem} — engineering/code residual panel ({domain})."
            ),
            generator="scripts/gen_engineering_code_bridge_lean.py",
            prefix=prefix,
            sign_theorem=sign_th,
            lean_domain=lean_domain,
            n=int(bench.get("record_count") or 0),
            med=float(
                bench.get("pooled_median_error_pct")
                or bench.get("median_error_pct")
                or 0.0
            ),
            d_eff=int(bench.get("D_eff", 12)),
            gate_pct=0.5,
        )
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
