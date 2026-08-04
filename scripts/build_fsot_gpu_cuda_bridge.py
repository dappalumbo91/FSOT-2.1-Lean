#!/usr/bin/env python3
"""Build FSOT-GPU CUDA competitive + parity/verify residual panels into data/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_gpu_cuda_bridge_lib import BUILDERS, output_path, resolve_fsot_gpu_root  # noqa: E402


def main() -> int:
    root = resolve_fsot_gpu_root()
    print(f"FSOT-GPU root: {root or 'MISSING'}")
    # Competitive + parity first (spine depends on their on-disk benches)
    order = [
        "FSOT_GPU_CUDA_Competitive_Panel",
        "FSOT_GPU_Parity_Verify_Panel",
        "FSOT_GPU_Engineering_Spine",
    ]
    for name in order:
        builder = BUILDERS[name]
        doc = builder()
        out = output_path(name)
        out.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        print(
            f"{name}: n={doc.get('record_count')} "
            f"med={doc.get('median_error_pct')} "
            f"pooled={doc.get('pooled_median_error_pct')} -> {out.name}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
