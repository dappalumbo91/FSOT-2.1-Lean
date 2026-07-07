"""FSOTB ISA registry — shared by ingest and verification."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "vendor" / "trinary_os" / "isa" / "fsotb_opcode_registry.json"


def load_opcode_registry(path: Path = DEFAULT_REGISTRY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_isa(registry: dict, oracles: dict[str, dict]) -> dict:
    opcodes = registry.get("opcodes") or []
    programs = registry.get("oracle_programs") or {}
    checks: list[dict] = []
    for key, spec in programs.items():
        oracle = oracles.get(key) or {}
        checks.append(
            {
                "program": key,
                "expected_file_size": spec.get("file_size"),
                "live_file_size": oracle.get("file_size"),
                "expected_instructions": spec.get("n_instructions"),
                "live_instructions": oracle.get("n_instructions"),
                "abi_tier": spec.get("abi_tier"),
            }
        )
    return {
        "opcode_count": len(opcodes),
        "abi_tiers": list((registry.get("abi_tiers") or {}).keys()),
        "word_width_trits": registry.get("word_width_trits"),
        "register_count": registry.get("register_count"),
        "num_task_slots": registry.get("num_task_slots"),
        "program_checks": checks,
    }