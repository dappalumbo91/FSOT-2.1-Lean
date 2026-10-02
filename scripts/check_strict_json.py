#!/usr/bin/env python3
"""Reject data/*.json that is not strict JSON (bare NaN, Infinity)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _reject(token: str):
    raise ValueError(token)


def main() -> int:
    bad: list[str] = []
    checked = 0
    for path in sorted(DATA.glob("*.json")):
        checked += 1
        try:
            json.loads(path.read_text(encoding="utf-8"), parse_constant=_reject)
        except ValueError as exc:
            bad.append(f"{path.name}: {exc}")
        except json.JSONDecodeError as exc:
            bad.append(f"{path.name}: {exc}")
    print(f"strict json files={checked} rejected={len(bad)}")
    for line in bad[:30]:
        print(line)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
