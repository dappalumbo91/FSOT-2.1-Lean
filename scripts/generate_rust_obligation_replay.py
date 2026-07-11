#!/usr/bin/env python3
"""Generate Tier 84 Rust f64 obligation replay tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rust_replay_lib import RUST_DIR, write_generated_tests  # noqa: E402


def main() -> int:
    meta = write_generated_tests()
    print(f"Wrote Rust replay tests under {RUST_DIR / 'tests'}")
    print(f"  connective obligations: {meta.get('connective_count', 0)}")
    print(f"  formal obligations: {meta['formal_count']}")
    print(f"  transcendental obligations: {meta['transcendental_count']}")
    print(f"  total: {meta['total_count']}")
    print(f"  test file: {meta.get('test_file')}")
    print(f"  logical chunks: {len(meta['chunks'])}")
    for chunk in meta["chunks"]:
        label = chunk.get("chunk", chunk.get("scope"))
        print(f"    {label}: {chunk['count']} ({chunk['scope']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())