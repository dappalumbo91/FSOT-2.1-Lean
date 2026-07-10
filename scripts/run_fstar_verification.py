#!/usr/bin/env python3
"""Tier 86 — run F* verification on FSOT scalar kernel spec."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fstar_verification_lib import run_fstar_verify  # noqa: E402

OUT = ROOT / "data" / "fstar_verification_report.json"


def main() -> int:
    result = run_fstar_verify()
    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tier": "86_fstar_verification",
        "fstar": result,
        "overall_ok": result.get("status") == "passed",
    }
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print("FSTAR VERIFICATION (Tier 86)")
    print(f"  status: {result.get('status')}")
    print(f"  overall_ok: {doc['overall_ok']}")
    print(f"Wrote {OUT}")
    return 0 if doc["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())