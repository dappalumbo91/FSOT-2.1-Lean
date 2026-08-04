#!/usr/bin/env python3
"""Build QCE/ELM + recent breakthrough residual panels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from recent_breakthrough_expansion_lib import BUILDERS, output_path  # noqa: E402


def main() -> int:
    order = [
        "QCE_ELM_Fusion_Edge_Panel",
        "Recent_Breakthroughs_Expansion_Panel",
        "Breakthrough_Fusion_Spine",
    ]
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
