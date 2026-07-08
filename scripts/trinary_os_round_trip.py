"""Portable FSOTB round-trip smoke checks from vendor ISA + fixtures."""

from __future__ import annotations

from pathlib import Path

from trinary_os_invariants import derived_os_constants, load_oracle
from trinary_os_isa import load_opcode_registry


def _parse_fsa_mnemonics(path: Path) -> list[str]:
    mnemonics: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(";", 1)[0].strip()
        if not line or line.startswith("."):
            continue
        if line.endswith(":"):
            continue
        token = line.split()[0].upper()
        if token:
            mnemonics.append(token)
    return mnemonics


def _count_fixture_instructions(path: Path) -> int:
    return len(_parse_fsa_mnemonics(path))


def _round_trip_identical(pass1: Path, pass2: Path) -> bool:
    if not pass1.exists() or not pass2.exists():
        return False
    return pass1.read_bytes() == pass2.read_bytes()


def summarize_round_trip(
    os_root: Path,
    isa_path: Path,
    *,
    fixture_names: dict[str, str] | None = None,
) -> dict:
    registry = load_opcode_registry(isa_path)
    programs = registry.get("oracle_programs") or {}
    constants = derived_os_constants()
    fixture_names = fixture_names or {
        "hello": "fixtures/hello.fsa",
        "call_ret": "fixtures/call_ret.fsa",
        "spawn_join": "fixtures/spawn_join.fsa",
    }
    mnemonic_set = {str(op.get("mnemonic", "")).upper() for op in registry.get("opcodes") or []}
    checks: list[dict] = []

    for key, spec in programs.items():
        oracle_path = os_root / "target" / f"{key}.fsotb.oracle.json"
        blob_path = os_root / "target" / f"{key}.fsotb"
        fixture_rel = fixture_names.get(key)
        fixture_path = os_root / fixture_rel if fixture_rel else None
        round_pass1 = os_root / "round_trip" / f"{key}.fsa.pass1.fsotb"
        round_pass2 = os_root / "round_trip" / f"{key}.fsa.pass2.fsotb"
        oracle = load_oracle(oracle_path) if oracle_path.exists() else {}
        checks.append(
            {
                "program": key,
                "abi_tier": spec.get("abi_tier"),
                "expected_file_size": spec.get("file_size"),
                "live_file_size": oracle.get("file_size"),
                "blob_file_size": blob_path.stat().st_size if blob_path.exists() else None,
                "expected_instructions": spec.get("n_instructions"),
                "live_instructions": oracle.get("n_instructions"),
                "fixture_instruction_lines": _count_fixture_instructions(fixture_path)
                if fixture_path and fixture_path.exists()
                else None,
                "round_trip_identical": _round_trip_identical(round_pass1, round_pass2),
                "panel_S_hex": oracle.get("panel_S_hex"),
                "seeds_hash_hex": oracle.get("seeds_hash_hex"),
                "fixture_mnemonics": _parse_fsa_mnemonics(fixture_path)
                if fixture_path and fixture_path.exists()
                else [],
                "mnemonic_registry_coverage": all(m in mnemonic_set for m in _parse_fsa_mnemonics(fixture_path))
                if fixture_path and fixture_path.exists()
                else False,
            }
        )

    return {
        "opcode_count": len(registry.get("opcodes") or []),
        "constants": constants,
        "program_checks": checks,
    }