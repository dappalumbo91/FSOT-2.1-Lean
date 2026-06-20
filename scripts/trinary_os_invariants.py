"""Fsot trinary OS FSOTB oracles and derived constants — shared by ingest and verification."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = ROOT / "data" / "canonical_constants.json"


def load_oracle(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def derived_os_constants() -> dict:
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    l1 = cache["layer1"]
    l2 = cache["layer2"]
    c_eff = float(l2["coherence_efficiency"])
    p_var = float(l2["phase_variance"])
    return {
        "seeds_hash_hex": "0xc627292ec4eb3b90",
        "panel_S_hex": "0x3fee69c97260701a",
        "panel_S_f64": 0.9504134401245242,
        "k": float(l2["k"]),
        "poof": float(l1["poof_factor"]),
        "p_new": float(l2["new_perceived_param"]),
        "collapse_threshold": c_eff * p_var,
        "num_task_slots": 8,
        "trit_word_width": 27,
        "cortical_layers": 6,
    }


def load_fsotb_oracles(fsot_os_root: Path, oracle_names: dict[str, str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for key, rel in oracle_names.items():
        path = fsot_os_root / rel
        if path.exists():
            out[key] = load_oracle(path)
    return out


def summarize_trinary_os(oracles: dict[str, dict], constants: dict) -> dict:
    return {
        "oracle_count": len(oracles),
        "oracles": oracles,
        "constants": constants,
        "hello_file_size": oracles.get("hello", {}).get("file_size"),
        "call_ret_file_size": oracles.get("call_ret", {}).get("file_size"),
        "spawn_join_file_size": oracles.get("spawn_join", {}).get("file_size"),
    }