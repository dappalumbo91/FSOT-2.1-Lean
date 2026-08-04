#!/usr/bin/env python3
"""Lean priors for QCE/ELM and recent breakthrough expansion panels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
sys.path.insert(0, str(ROOT / "scripts"))

from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402
from recent_breakthrough_expansion_lib import BUILDERS, LEAN_MAP, output_path  # noqa: E402


def main() -> int:
    for domain in sorted(BUILDERS.keys()):
        bench_path = output_path(domain)
        if not bench_path.is_file():
            print(f"Skip {domain}")
            continue
        bench = json.loads(bench_path.read_text(encoding="utf-8"))
        prefix, lean_domain, sign_th, module_stem = LEAN_MAP[domain]
        text = extension_priors_lean(
            module_title=f"FSOT Formal {module_stem} — recent breakthrough expansion ({domain}).",
            generator="scripts/gen_recent_breakthrough_lean.py",
            prefix=prefix,
            sign_theorem=sign_th,
            lean_domain=lean_domain,
            n=int(bench.get("record_count") or 0),
            med=float(bench.get("pooled_median_error_pct") or bench.get("median_error_pct") or 0.0),
            d_eff=int(bench.get("D_eff", 13)),
            gate_pct=0.5,
        )
        out = FORMAL / f"{module_stem}.lean"
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
