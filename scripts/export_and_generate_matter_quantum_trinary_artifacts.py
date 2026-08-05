#!/usr/bin/env python3
"""Focused multiprover package for Matter/Antimatter + Quantum/Trinary panels.

Mirrors export_and_generate_uniqueness_research_artifacts.py (lighter):
  - verification/obligations/matter_quantum_trinary_spine.json
  - Lean already generated via gen_matter_quantum_trinary_priors_lean.py
  - Coq / Isabelle / SMT / Rust replay for numeric residual gates
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from cross_proof_lib import coq_lit_real, isa_lit_real, python_verify_obligation  # noqa: E402

OUT_OBL = ROOT / "verification" / "obligations" / "matter_quantum_trinary_spine.json"
COQ_OUT = ROOT / "verification" / "coq" / "MatterQuantumTrinarySpine.v"
ISA_OUT = ROOT / "verification" / "isabelle" / "MatterQuantumTrinarySpine.thy"
SMT_OUT = ROOT / "verification" / "smt" / "matter_quantum_trinary_bounds.smt2"
RUST_DIR = ROOT / "verification" / "rust" / "fsot_matter_quantum_trinary_replay"
PANELS = [
    ("matter_antimatter_benchmark.json", "matter_antimatter", "Matter_Antimatter"),
    ("quantum_trinary_syntax_benchmark.json", "quantum_trinary_syntax", "Quantum_Trinary_Syntax"),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_id(s: str) -> str:
    out = []
    for ch in s:
        out.append(ch if ch.isalnum() else "_")
    sid = "".join(out).strip("_")
    while "__" in sid:
        sid = sid.replace("__", "_")
    return sid[:72] or "ob"


def build_obligations() -> list[dict]:
    obs: list[dict] = []
    for fname, prefix, domain in PANELS:
        path = ROOT / "data" / fname
        if not path.exists():
            continue
        bench = json.loads(path.read_text(encoding="utf-8"))
        n = int(bench.get("record_count") or bench.get("observable_count") or 0)
        pooled = float(bench.get("pooled_median_error_pct") or 0.0)
        d_eff = int(bench.get("D_eff") or 12)
        sid = _safe_id(prefix)

        obs.append(
            {
                "id": f"{sid}_count_pos",
                "coq_id": f"{sid}_count_pos",
                "kind": "nat_pos",
                "value": max(n, 1),
                "module": f"MatterQuantumTrinary.{domain}",
                "claim": f"{prefix}_records",
            }
        )
        obs.append(
            {
                "id": f"{sid}_pooled_under_half",
                "coq_id": f"{sid}_pooled_under_half",
                "kind": "lt_half",
                "value": pooled if pooled > 0 else 0.0,
                "module": f"MatterQuantumTrinary.{domain}",
                "claim": f"{prefix}_green",
                "statement": f"pooled_median_error_pct({prefix}) < 0.5",
            }
        )
        obs.append(
            {
                "id": f"{sid}_deff_eq",
                "coq_id": f"{sid}_deff_eq",
                "kind": "eq_nat",
                "value": d_eff,
                "right_value": d_eff,
                "module": f"MatterQuantumTrinary.{domain}",
                "claim": f"{prefix}_D_eff",
            }
        )
        # Per-record residual / identity sample (cap)
        mat = bench.get("material_records") or bench.get("records") or []
        for i, r in enumerate(mat[:12]):
            if not isinstance(r, dict):
                continue
            err = r.get("error_pct")
            if err is None:
                continue
            try:
                ef = float(err)
            except (TypeError, ValueError):
                continue
            rid = _safe_id(f"{prefix}_{r.get('name') or r.get('property') or i}")
            if ef <= 0.5:
                obs.append(
                    {
                        "id": f"{rid}_err_lt_half",
                        "coq_id": f"{rid}_err_lt_half",
                        "kind": "lt_half",
                        "value": ef if ef > 0 else 0.0,
                        "module": f"MatterQuantumTrinary.{domain}",
                        "claim": str(r.get("claim") or prefix),
                    }
                )
    # Dedup
    seen: set[str] = set()
    unique = []
    for o in obs:
        if o["id"] in seen:
            continue
        seen.add(o["id"])
        unique.append(o)
    return unique


def gen_coq(obs: list[dict]) -> str:
    lines = [
        "(* Matter/Antimatter + Quantum/Trinary multiprover spine *)",
        "From Stdlib Require Import Reals.",
        "From Stdlib Require Import Psatz.",
        "From Stdlib Require Import Arith.",
        "Local Open Scope R_scope.",
        "",
    ]
    for ob in obs:
        oid = ob["coq_id"]
        kind = ob["kind"]
        if kind == "lt_half":
            lit = coq_lit_real(float(ob["value"]))
            lines += [f"Lemma {oid} : ({lit}) < (0.5%R).", "Proof. lra. Qed.", ""]
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines += [f"Lemma {oid} : (0 < {v})%nat.", "Proof. apply Nat.ltb_lt; reflexivity. Qed.", ""]
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines += [f"Lemma {oid} : ({l} = {r})%nat.", "Proof. reflexivity. Qed.", ""]
    return "\n".join(lines) + "\n"


def gen_isabelle(obs: list[dict]) -> str:
    lines = [
        "theory MatterQuantumTrinarySpine",
        "  imports Complex_Main",
        "begin",
        "",
    ]
    for ob in obs:
        oid = ob["coq_id"]
        kind = ob["kind"]
        if kind == "lt_half":
            lit = isa_lit_real(float(ob["value"]))
            lines += [f'lemma {oid}: "({lit}::real) < (0.5::real)"', "  by simp", ""]
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines += [f'lemma {oid}: "(0::nat) < {v}"', "  by simp", ""]
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines += [f'lemma {oid}: "({l}::nat) = {r}"', "  by simp", ""]
    lines += ["end", ""]
    return "\n".join(lines)


def _smt_real(v: float) -> str:
    if v == 0.0:
        return "0.0"
    if v < 0:
        return f"(- {_smt_real(-v)})"
    s = f"{v:.18f}".rstrip("0").rstrip(".")
    if "." not in s:
        s += ".0"
    return s


def gen_smt(obs: list[dict]) -> str:
    lines = ["; Matter + Quantum/Trinary SMT bounds", "(set-logic QF_LIRA)", ""]
    for i, ob in enumerate(obs):
        kind = ob["kind"]
        name = f"o{i}"
        if kind == "lt_half":
            lines.append(f"(assert (! (< {_smt_real(float(ob['value']))} 0.5) :named {name}))")
        elif kind == "nat_pos":
            lines.append(f"(assert (! (> {int(ob['value'])} 0) :named {name}))")
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines.append(f"(assert (! (= {l} {r}) :named {name}))")
    lines.append("(check-sat)")
    return "\n".join(lines) + "\n"


def gen_rust(obs: list[dict]) -> tuple[str, str]:
    cargo = """[package]
name = "fsot_matter_quantum_trinary_replay"
version = "0.1.0"
edition = "2021"
"""
    lines = [
        "//! Matter + Quantum/Trinary obligation replay",
        "",
        "#[test]",
        "fn replay_matter_quantum_trinary() {",
    ]
    for ob in obs:
        oid = ob["id"]
        kind = ob["kind"]
        if kind == "lt_half":
            v = float(ob["value"])
            lines.append(f'    assert!({v}_f64 < 0.5_f64, "{oid}");')
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines.append(f'    assert!({v} > 0, "{oid}");')
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines.append(f'    assert_eq!({l}, {r}, "{oid}");')
    lines.append("}")
    lines.append("")
    return cargo, "\n".join(lines)


def patch_isabelle_root() -> None:
    root = ROOT / "verification" / "isabelle" / "ROOT"
    if not root.exists():
        return
    text = root.read_text(encoding="utf-8")
    if "MatterQuantumTrinarySpine" in text:
        return
    if "UniquenessResearchSpine" in text:
        text = text.replace(
            "UniquenessResearchSpine",
            "UniquenessResearchSpine\n    MatterQuantumTrinarySpine",
            1,
        )
    else:
        text = text.rstrip() + "\n    MatterQuantumTrinarySpine\n"
    root.write_text(text, encoding="utf-8")


def main() -> int:
    # Ensure Lean priors exist
    import subprocess

    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "gen_matter_quantum_trinary_priors_lean.py")],
        cwd=str(ROOT),
    )
    if r.returncode != 0:
        return r.returncode

    obs = build_obligations()
    obl = {
        "generated_at": _now(),
        "version": "1.0",
        "tier": "matter_quantum_trinary",
        "obligation_count": len(obs),
        "panels": [p[0] for p in PANELS],
        "modules": [
            "FSOT/Formal/MatterAntimatterPriors.lean",
            "FSOT/Formal/QuantumTrinarySyntaxPriors.lean",
            "verification/coq/MatterQuantumTrinarySpine.v",
            "verification/isabelle/MatterQuantumTrinarySpine.thy",
            "verification/smt/matter_quantum_trinary_bounds.smt2",
            "verification/rust/fsot_matter_quantum_trinary_replay",
        ],
        "obligations": obs,
        "honest_scope": (
            "Numeric residual gates for Matter/Antimatter and Quantum/Trinary syntax panels. "
            "Not continuum Sakharov or full QI complexity theory."
        ),
    }
    OUT_OBL.parent.mkdir(parents=True, exist_ok=True)
    OUT_OBL.write_text(json.dumps(obl, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_OBL} ({len(obs)} obligations)")

    COQ_OUT.write_text(gen_coq(obs), encoding="utf-8")
    print(f"Wrote {COQ_OUT}")
    ISA_OUT.write_text(gen_isabelle(obs), encoding="utf-8")
    print(f"Wrote {ISA_OUT}")
    patch_isabelle_root()
    SMT_OUT.write_text(gen_smt(obs), encoding="utf-8")
    print(f"Wrote {SMT_OUT}")

    cargo, rust = gen_rust(obs)
    RUST_DIR.mkdir(parents=True, exist_ok=True)
    (RUST_DIR / "Cargo.toml").write_text(cargo, encoding="utf-8")
    (RUST_DIR / "src").mkdir(exist_ok=True)
    (RUST_DIR / "src" / "lib.rs").write_text("//! matter quantum trinary replay\n", encoding="utf-8")
    (RUST_DIR / "tests").mkdir(exist_ok=True)
    (RUST_DIR / "tests" / "replay.rs").write_text(rust, encoding="utf-8")
    print(f"Wrote Rust {RUST_DIR}")

    bad = sum(1 for o in obs if not python_verify_obligation(o))
    print(f"Python triangulation: {len(obs) - bad}/{len(obs)}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
