#!/usr/bin/env python3
"""Recompute the 22 frozen per-host H0 values from the frozen file's own inputs.

The freeze pin on that file is D1D38A. Commit 43d1fe4 is not an object in this
clone; the prereg hash of predictions/h0_sightline_predictions.json is the pin
for the bytes that are here. This script does not write that file.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "predictions" / "h0_sightline_predictions.json"


def main() -> int:
    doc = json.loads(FROZEN.read_text(encoding="utf-8"))
    h0 = float(doc["h0_global_fsot"])
    bleed = float(doc["bubble_bleed_fraction"])
    hosts = doc["hosts"]
    worst = 0.0
    for row in hosts:
        got = h0 * (1.0 + float(row["bubble_density_model"]) * bleed)
        worst = max(worst, abs(got - float(row["fsot_predicted_h0"])))
    commit = subprocess.run(
        ["git", "cat-file", "-t", "43d1fe4"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(f"pin_in_file={doc.get('authority_pin_prefix')} hosts={len(hosts)} max_abs_diff={worst:.3e}")
    print(f"commit_43d1fe4={'present' if commit.returncode == 0 else 'not_in_this_clone'}")
    if len(hosts) != 22 or worst > 5e-4:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
