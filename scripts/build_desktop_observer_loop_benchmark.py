#!/usr/bin/env python3
"""Build Desktop_Observer_Loop_Panel benchmark from software observer replay."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "desktop_observer_loop_panel_benchmark.json"
sys.path.insert(0, str(ROOT / "scripts"))

from desktop_observer_loop_lib import replay_observed_batch  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def main() -> int:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_desktop_observer_loop.py"), "--samples", "12"],
        cwd=str(ROOT),
        check=False,
    )
    replay = replay_observed_batch()
    records = list(replay.get("records") or [])
    errs = [float(r["error_pct"]) for r in records]
    _, authority = _load_fsot()
    doc = _bench_v11(
        domain="Desktop_Observer_Loop_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "neural", "observer"],
        d_eff=14,
        authority_path=authority,
        source=["desktop_observer_loop_lib", "vendor/fsot_compute.py"],
        channel_stats=[("desktop_observer", "timing_display_proxy", errs or [0.0])],
        sota_baselines={
            "desktop_observer": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "unobserved scalar without quirk_mod replay",
            }
        },
    )
    doc["observer_policy"] = "no_mic_no_camera_esp32_deferred"
    doc["generated_at"] = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}  {doc.get('record_count')} records pooled {doc.get('pooled_median_error_pct')}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())