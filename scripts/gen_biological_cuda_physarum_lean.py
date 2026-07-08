#!/usr/bin/env python3
"""Generate FSOT/Formal/BiologicalCudaPhysarumPriors.lean."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
from _gen_extension_priors_lean import extension_priors_lean  # noqa: E402

MANIFEST = ROOT / "data" / "biological_cuda_physarum_manifest.yaml"
BENCH = ROOT / "data" / "biological_cuda_physarum_benchmark.json"
OUTPUT = ROOT / "FSOT" / "Formal" / "BiologicalCudaPhysarumPriors.lean"


def main() -> int:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    lean = cfg["lean"]
    text = extension_priors_lean(
        module_title="FSOT Formal BiologicalCudaPhysarumPriors — Physarum CUDA biology crosswalk.",
        generator="scripts/gen_biological_cuda_physarum_lean.py",
        prefix="biological_cuda_physarum",
        sign_theorem=lean["sign_theorem"],
        lean_domain=lean["lean_domain"],
        n=int(bench.get("record_count") or 0),
        med=float(bench.get("median_error_pct") or 0.0),
        d_eff=int(bench.get("D_eff", 22)),
    )
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())