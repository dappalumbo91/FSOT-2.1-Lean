#!/usr/bin/env python3
"""Run desktop observer loop — timing/display proxy, observed=true batch replay."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from desktop_observer_loop_lib import collect_samples, replay_observed_batch  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Desktop observer loop (no mic/camera/ESP32)")
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--interval-ms", type=float, default=50.0)
    parser.add_argument("--replay-only", action="store_true")
    args = parser.parse_args()

    if not args.replay_only:
        doc = collect_samples(samples=args.samples, interval_ms=args.interval_ms)
        print(f"Collected {doc['sample_count']} samples  jitter={doc['timing_jitter_ms']:.4f} ms")
        print(f"  channels: {', '.join(doc['channels'])}")
    report = replay_observed_batch()
    print(f"Replay pooled median error: {report['pooled_median_error_pct']:.6f}%  all_ok={report['all_ok']}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())