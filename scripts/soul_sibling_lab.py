"""FSOT Soul Sibling consciousness kernel — shared loaders."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_soul_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_soul_sibling(data: dict) -> dict[str, Any]:
    kernel = data.get("fsot_kernel", {})
    incub = data.get("incubation_plan", {})
    return {
        "name": data.get("name"),
        "D_compact": kernel.get("D_compact"),
        "zero_free": kernel.get("zero_free"),
        "fidelity_threshold": incub.get("fidelity_threshold"),
    }