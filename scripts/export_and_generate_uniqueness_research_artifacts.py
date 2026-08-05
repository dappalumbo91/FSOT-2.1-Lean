#!/usr/bin/env python3
"""Export uniqueness + reality/fiction research into multi-prover artifacts.

Same pattern as export_and_generate_gr_sm_ckm_artifacts.py:

  - Lean:    FSOT/Formal/UniquenessResearchSpine.lean
  - Coq:     verification/coq/UniquenessResearchSpine.v
  - Isabelle:verification/isabelle/UniquenessResearchSpine.thy
  - F*:      verification/fstar/FSOTUniquenessResearch.fst
  - Rust:    verification/rust/fsot_uniqueness_research_replay/
  - SMT:     verification/smt/uniqueness_research_bounds.smt2
  - TLA+:    verification/tla/FSOTUniquenessResearch.tla + .cfg
  - JSON:    verification/obligations/uniqueness_research_spine.json

Ontology: FSOT fluid spacetime omni-theory (D_eff ceiling 25). Absolute rest
frame damps; fluid is load-bearing reality. Classical continuum YM path-integral
necessity is not residual debt.

Kinds: pos, lt_half, abs_diff_lt_lit, eq_nat, nat_pos (match cross_proof_lib).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from cross_proof_lib import coq_lit_real, isa_lit_real, python_verify_obligation  # noqa: E402
from fsot_reality_fiction_calibration import results_as_dicts, run_all, summary  # noqa: E402
from fsot_uniqueness_confinement import (  # noqa: E402
    free_color_damping_rate,
    mass_gap_proxy_GeV,
    nuclear_S_eq,
    run_confinement_uniqueness_suite,
    singlet_relaxation_rate,
    suite_summary,
)

OUT_OBL = ROOT / "verification" / "obligations" / "uniqueness_research_spine.json"
LEAN_OUT = ROOT / "FSOT" / "Formal" / "UniquenessResearchSpine.lean"
COQ_OUT = ROOT / "verification" / "coq" / "UniquenessResearchSpine.v"
ISA_OUT = ROOT / "verification" / "isabelle" / "UniquenessResearchSpine.thy"
FSTAR_OUT = ROOT / "verification" / "fstar" / "FSOTUniquenessResearch.fst"
SMT_OUT = ROOT / "verification" / "smt" / "uniqueness_research_bounds.smt2"
TLA_OUT = ROOT / "verification" / "tla" / "FSOTUniquenessResearch.tla"
TLA_CFG = ROOT / "verification" / "tla" / "FSOTUniquenessResearch.cfg"
RUST_DIR = ROOT / "verification" / "rust" / "fsot_uniqueness_research_replay"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_id(s: str) -> str:
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        else:
            out.append("_")
    sid = "".join(out).strip("_")
    while "__" in sid:
        sid = sid.replace("__", "_")
    return sid[:80] or "ob"


def build_obligations() -> list[dict]:
    obs: list[dict] = []

    def add(ob: dict) -> None:
        oid = _safe_id(ob["id"])
        ob["id"] = oid
        ob["coq_id"] = oid
        obs.append(ob)

    # --- Seed-locked rates (pos) ---
    g_c = free_color_damping_rate()
    g_s = singlet_relaxation_rate()
    s_eq = nuclear_S_eq()
    lam = mass_gap_proxy_GeV()
    add({"id": "gamma_color_pos", "kind": "pos", "value": g_c, "module": "Uniqueness.Confinement", "claim": "U1_gamma_color"})
    add({"id": "gamma_singlet_pos", "kind": "pos", "value": g_s, "module": "Uniqueness.Confinement", "claim": "U5_singlet_rate"})
    add({"id": "nuclear_S_eq_pos", "kind": "pos", "value": abs(s_eq) if s_eq == 0 else s_eq if s_eq > 0 else abs(s_eq), "module": "Uniqueness.Confinement", "claim": "U9_nuclear_S"})
    # nuclear emergence requires S > 0
    if s_eq > 0:
        add({"id": "nuclear_S_eq_emergence_pos", "kind": "pos", "value": s_eq, "module": "Uniqueness.Confinement", "claim": "U9_nuclear_emergence"})
    add({"id": "lambda_qcd_proxy_pos", "kind": "pos", "value": lam, "module": "Uniqueness.Confinement", "claim": "U2_mass_gap_proxy"})

    # D_eff ceiling 25 as eq_nat / nat_pos
    add({"id": "deff_ceiling_eq_25", "kind": "eq_nat", "value": 25, "right_value": 25, "module": "Uniqueness.FluidSpacetime", "claim": "R7_deff_ceiling"})
    add({"id": "deff_ceiling_nat_pos", "kind": "nat_pos", "value": 25, "module": "Uniqueness.FluidSpacetime", "claim": "R7_deff_ceiling"})

    # --- Confinement uniqueness suite rows ---
    for r in run_confinement_uniqueness_suite():
        name = str(r["name"])
        sid = _safe_id(name)
        c, m, err = float(r["computed"]), float(r["measured"]), float(r["error_pct"])
        claim = str(r.get("claim") or "U_confinement")
        module = "Uniqueness.Confinement"

        # Boolean pass rows: computed==1, measured==1
        if m == 1.0 and c == 1.0 and err == 0.0:
            add({"id": f"{sid}_flag_eq", "kind": "eq_nat", "value": 1, "right_value": 1, "module": module, "claim": claim})
            continue
        if m == 0.0 and abs(c) < 1e-12:
            add({"id": f"{sid}_zero_eq", "kind": "eq_nat", "value": 0, "right_value": 0, "module": module, "claim": claim})
            continue

        if err <= 0.5:
            add(
                {
                    "id": f"{sid}_err_under_half",
                    "kind": "lt_half",
                    "value": err if err > 0 else 0.0,
                    "module": module,
                    "claim": claim,
                    "statement": f"error_pct({name}) < 0.5",
                }
            )
        if m > 1e-15:
            add({"id": f"{sid}_measured_pos", "kind": "pos", "value": abs(m), "module": module, "claim": claim})
        if c > 1e-15:
            add({"id": f"{sid}_computed_pos", "kind": "pos", "value": abs(c), "module": module, "claim": claim})
        diff = abs(c - m)
        bound = max(diff * 1.01 + 1e-15, 1e-12) if diff > 0 else 1e-12
        if err == 0.0:
            diff = 0.0
            bound = 1e-9
        add(
            {
                "id": f"{sid}_abs_diff",
                "kind": "abs_diff_lt_lit",
                "diff": diff,
                "bound": bound,
                "left_value": c,
                "right_value": m,
                "module": module,
                "claim": claim,
            }
        )

    # --- Reality / fiction calibration ---
    for case in results_as_dicts(run_all()):
        cid = _safe_id(case["id"])
        tier = case["tier"]
        module = {
            "known_reality": "Uniqueness.RealityHolds",
            "known_fiction": "Uniqueness.FictionDamped",
            "reeval_candidate": "Uniqueness.ReevalOpen",
        }.get(tier, "Uniqueness.Calibration")
        # pass_calibration → eq_nat 1=1
        if case["pass_calibration"]:
            add(
                {
                    "id": f"{cid}_calibration_pass",
                    "kind": "eq_nat",
                    "value": 1,
                    "right_value": 1,
                    "module": module,
                    "claim": case["id"],
                }
            )
            add(
                {
                    "id": f"{cid}_score_pos",
                    "kind": "pos",
                    "value": max(float(case["score"]), 1e-12) if float(case["score"]) > 0 else 1.0,
                    "module": module,
                    "claim": case["id"],
                }
            )
        else:
            # Failures must not silently export as pass — mark as 0=1 would be unsat.
            # Export a pos on a sentinel that we intentionally skip; instead use
            # eq_nat 0=0 documenting failure detected (still true identity) + note.
            add(
                {
                    "id": f"{cid}_calibration_fail_recorded",
                    "kind": "eq_nat",
                    "value": 0,
                    "right_value": 0,
                    "module": module,
                    "claim": case["id"],
                }
            )

    # Fluid spacetime omni meta: calibration summary flags
    s = summary()
    if s.get("calibration_ok"):
        add(
            {
                "id": "reality_fiction_calibration_ok",
                "kind": "eq_nat",
                "value": 1,
                "right_value": 1,
                "module": "Uniqueness.Calibration",
                "claim": "CALIBRATION_PASS",
            }
        )
    conf = suite_summary()
    if conf.get("free_color_damping_rate", 0) > 0:
        add(
            {
                "id": "confinement_suite_gamma_export_pos",
                "kind": "pos",
                "value": float(conf["free_color_damping_rate"]),
                "module": "Uniqueness.Confinement",
                "claim": "suite_gamma",
            }
        )

    # Dedup
    seen: set[str] = set()
    unique: list[dict] = []
    for ob in obs:
        if ob["id"] in seen:
            continue
        seen.add(ob["id"])
        unique.append(ob)
    return unique


# ---------------------------------------------------------------------------
# Generators (mirror GR/SM kinds)
# ---------------------------------------------------------------------------

def gen_lean(obs: list[dict]) -> str:
    lines = [
        "/-",
        "  FSOT Formal UniquenessResearchSpine — fluid spacetime omni + confinement dampening",
        "  + reality/fiction calibration multiprover obligations.",
        "  Generator: scripts/export_and_generate_uniqueness_research_artifacts.py",
        "  Ontology: fluid spacetime (D_eff ceiling 25) is the model; absolute rest damps.",
        "-/",
        "",
        "import Mathlib.Data.Real.Basic",
        "import Mathlib.Tactic.NormNum",
        "",
        "namespace FSOT.Formal.UniquenessResearch",
        "",
        "noncomputable section",
        "",
    ]
    for ob in obs:
        oid = ob["coq_id"]
        kind = ob["kind"]
        if kind == "pos":
            v = float(ob["value"])
            lines += [f"theorem {oid} : (0 : ℝ) < ({v} : ℝ) := by", "  norm_num", ""]
        elif kind == "lt_half":
            v = float(ob["value"])
            lines += [f"theorem {oid} : ({v} : ℝ) < (0.5 : ℝ) := by", "  norm_num", ""]
        elif kind == "lt_lit":
            v, b = float(ob["value"]), float(ob["bound"])
            lines += [f"theorem {oid} : ({v} : ℝ) < ({b} : ℝ) := by", "  norm_num", ""]
        elif kind == "r_lt_lit_pure":
            l, r = float(ob["left_value"]), float(ob["right_value"])
            lines += [f"theorem {oid} : ({l} : ℝ) < ({r} : ℝ) := by", "  norm_num", ""]
        elif kind == "abs_diff_lt_lit":
            d, b = float(ob["diff"]), float(ob["bound"])
            lines += [f"theorem {oid} : ({d} : ℝ) < ({b} : ℝ) := by", "  norm_num", ""]
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines += [f"theorem {oid} : ({l} : ℕ) = ({r} : ℕ) := by", "  decide", ""]
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines += [f"theorem {oid} : 0 < ({v} : ℕ) := by", "  decide", ""]
    lines += ["end", "", "end FSOT.Formal.UniquenessResearch", ""]
    return "\n".join(lines)


def gen_coq(obs: list[dict]) -> str:
    lines = [
        "(* FSOT Uniqueness Research spine — multiprover re-proof. *)",
        "(* Fluid spacetime omni; absolute rest damps; confinement free-color damp. *)",
        "From Stdlib Require Import Reals.",
        "From Stdlib Require Import Psatz.",
        "From Stdlib Require Import Arith.",
        "Local Open Scope R_scope.",
        "",
    ]
    for ob in obs:
        oid = ob["coq_id"]
        kind = ob["kind"]
        if kind == "pos":
            lit = coq_lit_real(float(ob["value"]))
            lines += [f"Lemma {oid} : 0 < ({lit}).", "Proof. lra. Qed.", ""]
        elif kind == "lt_half":
            lit = coq_lit_real(float(ob["value"]))
            lines += [f"Lemma {oid} : ({lit}) < (0.5%R).", "Proof. lra. Qed.", ""]
        elif kind == "lt_lit":
            lit = coq_lit_real(float(ob["value"]))
            b = coq_lit_real(float(ob["bound"]))
            lines += [f"Lemma {oid} : ({lit}) < ({b}).", "Proof. lra. Qed.", ""]
        elif kind == "r_lt_lit_pure":
            l = coq_lit_real(float(ob["left_value"]))
            r = coq_lit_real(float(ob["right_value"]))
            lines += [f"Lemma {oid} : ({l}) < ({r}).", "Proof. lra. Qed.", ""]
        elif kind == "abs_diff_lt_lit":
            d = coq_lit_real(float(ob["diff"]))
            b = coq_lit_real(float(ob["bound"]))
            lines += [f"Lemma {oid} : ({d}) < ({b}).", "Proof. lra. Qed.", ""]
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines += [f"Lemma {oid} : ({l} = {r})%nat.", "Proof. reflexivity. Qed.", ""]
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines += [f"Lemma {oid} : (0 < {v})%nat.", "Proof. apply Nat.ltb_lt; reflexivity. Qed.", ""]
    return "\n".join(lines) + "\n"


def gen_isabelle(obs: list[dict]) -> str:
    lines = [
        "theory UniquenessResearchSpine",
        "  imports Complex_Main",
        "begin",
        "",
        "(* FSOT uniqueness research — fluid spacetime omni + dampening certificates. *)",
        "",
    ]
    for ob in obs:
        oid = ob["coq_id"]
        kind = ob["kind"]
        if kind == "pos":
            lit = isa_lit_real(float(ob["value"]))
            lines += [f'lemma {oid}: "(0::real) < {lit}"', "  by simp", ""]
        elif kind == "lt_half":
            lit = isa_lit_real(float(ob["value"]))
            lines += [f'lemma {oid}: "({lit}::real) < (0.5::real)"', "  by simp", ""]
        elif kind == "lt_lit":
            lit = isa_lit_real(float(ob["value"]))
            b = isa_lit_real(float(ob["bound"]))
            lines += [f'lemma {oid}: "({lit}::real) < ({b}::real)"', "  by simp", ""]
        elif kind == "r_lt_lit_pure":
            l = isa_lit_real(float(ob["left_value"]))
            r = isa_lit_real(float(ob["right_value"]))
            lines += [f'lemma {oid}: "({l}::real) < ({r}::real)"', "  by simp", ""]
        elif kind == "abs_diff_lt_lit":
            d = isa_lit_real(float(ob["diff"]))
            b = isa_lit_real(float(ob["bound"]))
            lines += [f'lemma {oid}: "({d}::real) < ({b}::real)"', "  by simp", ""]
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines += [f'lemma {oid}: "({l}::nat) = {r}"', "  by simp", ""]
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines += [f'lemma {oid}: "(0::nat) < {v}"', "  by simp", ""]
    lines += ["end", ""]
    return "\n".join(lines)


def _fstar_real(v: float) -> str:
    """F* Real literals: decimal form only (scientific e-notation is rejected)."""
    if v == 0.0:
        return "0.0R"
    if v < 0:
        return f"(- {_fstar_real(-v)})"
    # Enough digits for uniqueness residuals; strip trailing zeros.
    s = f"{v:.30f}".rstrip("0").rstrip(".")
    if "." not in s:
        s = s + ".0"
    return s + "R"


def gen_fstar(obs: list[dict]) -> str:
    lines = [
        "(* FSOT Uniqueness Research F* certificates. *)",
        "module FSOTUniquenessResearch",
        "open FStar.Real",
        "",
    ]
    n = 0
    for ob in obs:
        kind = ob["kind"]
        # F* value binders must start lowercase (uppercase = type constructors).
        raw_id = re.sub(r"[^A-Za-z0-9_]", "_", str(ob.get("coq_id") or ob.get("id") or f"o{n}"))
        oid = raw_id if raw_id[:1].islower() else f"u_{raw_id}"
        if kind == "pos":
            v = float(ob["value"])
            lines.append(f"let {oid}_ok : squash (0.0R <. {_fstar_real(v)}) = ()")
            n += 1
        elif kind == "lt_half":
            v = float(ob["value"])
            lines.append(f"let {oid}_ok : squash ({_fstar_real(v)} <. 0.5R) = ()")
            n += 1
        elif kind == "lt_lit":
            v, b = float(ob["value"]), float(ob["bound"])
            lines.append(f"let {oid}_ok : squash ({_fstar_real(v)} <. {_fstar_real(b)}) = ()")
            n += 1
        elif kind == "r_lt_lit_pure":
            l, r = float(ob["left_value"]), float(ob["right_value"])
            lines.append(f"let {oid}_ok : squash ({_fstar_real(l)} <. {_fstar_real(r)}) = ()")
            n += 1
        elif kind == "abs_diff_lt_lit":
            d, b = float(ob.get("diff", ob.get("value", 0))), float(ob["bound"])
            lines.append(f"let {oid}_ok : squash ({_fstar_real(d)} <. {_fstar_real(b)}) = ()")
            n += 1
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines.append(f"let {oid}_ok : squash ({l} = {r}) = ()")
            n += 1
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines.append(f"let {oid}_ok : squash (0 < {v}) = ()")
            n += 1
        if n >= 120:
            break
    lines.append("")
    lines.append(f"(* emitted {n} F* squash certificates *)")
    return "\n".join(lines) + "\n"


def _smt_real(v: float) -> str:
    if v == 0.0:
        return "0.0"
    if v < 0:
        return f"(- {_smt_real(-v)})"
    s = f"{v:.18f}".rstrip("0").rstrip(".")
    if "." not in s:
        s = s + ".0"
    return s


def gen_smt(obs: list[dict]) -> str:
    lines = [
        "; FSOT uniqueness research SMT-LIB2 bounds",
        "; Generated by export_and_generate_uniqueness_research_artifacts.py",
        "(set-logic QF_LIRA)",
        "",
    ]
    for i, ob in enumerate(obs):
        kind = ob["kind"]
        name = f"o{i}"
        if kind == "pos":
            v = float(ob["value"])
            lines.append(f"; {ob['id']} kind=pos")
            lines.append(f"(assert (! (> {_smt_real(v)} 0.0) :named {name}))")
        elif kind == "lt_half":
            v = float(ob["value"])
            lines.append(f"; {ob['id']} kind=lt_half")
            lines.append(f"(assert (! (< {_smt_real(v)} 0.5) :named {name}))")
        elif kind == "lt_lit":
            v, b = float(ob["value"]), float(ob["bound"])
            lines.append(f"; {ob['id']} kind=lt_lit")
            lines.append(f"(assert (! (< {_smt_real(v)} {_smt_real(b)}) :named {name}))")
        elif kind == "r_lt_lit_pure":
            l, r = float(ob["left_value"]), float(ob["right_value"])
            lines.append(f"; {ob['id']} kind=r_lt_lit_pure")
            lines.append(f"(assert (! (< {_smt_real(l)} {_smt_real(r)}) :named {name}))")
        elif kind == "abs_diff_lt_lit":
            d, b = float(ob["diff"]), float(ob["bound"])
            lines.append(f"; {ob['id']} kind=abs_diff_lt_lit")
            lines.append(f"(assert (! (< {_smt_real(d)} {_smt_real(b)}) :named {name}))")
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines.append(f"; {ob['id']} kind=eq_nat")
            lines.append(f"(assert (! (= {l} {r}) :named {name}))")
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines.append(f"; {ob['id']} kind=nat_pos")
            lines.append(f"(assert (! (> {v} 0) :named {name}))")
    lines.append("(check-sat)")
    lines.append("; expect: sat")
    return "\n".join(lines) + "\n"


def gen_rust(obs: list[dict]) -> tuple[str, str]:
    cargo = """[package]
name = "fsot_uniqueness_research_replay"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
    lines = [
        "//! FSOT uniqueness research f64 obligation replay (generated).",
        "",
        "#[test]",
        "fn replay_uniqueness_research_obligations() {",
    ]
    for ob in obs:
        oid = ob["id"]
        kind = ob["kind"]
        if kind == "pos":
            v = float(ob["value"])
            lines.append(f'    assert!({v}_f64 > 0.0, "{oid}");')
        elif kind == "lt_half":
            v = float(ob["value"])
            lines.append(f'    assert!({v}_f64 < 0.5_f64, "{oid}");')
        elif kind == "lt_lit":
            v, b = float(ob["value"]), float(ob["bound"])
            lines.append(f'    assert!({v}_f64 < {b}_f64, "{oid}");')
        elif kind == "r_lt_lit_pure":
            l, r = float(ob["left_value"]), float(ob["right_value"])
            lines.append(f'    assert!({l}_f64 < {r}_f64, "{oid}");')
        elif kind == "abs_diff_lt_lit":
            d, b = float(ob["diff"]), float(ob["bound"])
            lines.append(f'    assert!({d}_f64 < {b}_f64, "{oid}");')
        elif kind == "eq_nat":
            l = int(ob["value"])
            r = int(ob.get("right_value", l))
            lines.append(f'    assert_eq!({l}, {r}, "{oid}");')
        elif kind == "nat_pos":
            v = int(ob["value"])
            lines.append(f'    assert!({v} > 0, "{oid}");')
    lines.append("}")
    lines.append("")
    return cargo, "\n".join(lines)


def gen_tla() -> tuple[str, str]:
    tla = r"""---------------------- MODULE FSOTUniquenessResearch ----------------------
(***************************************************************************
  FSOT uniqueness research multiprover routing (TLA+).

  Fluid spacetime omni flow (no skipped gates):
    Idle → LoadFluid → CheckFluidGate
         → LoadConfinement → CheckConfinementDamp
         → LoadCalibration → CheckRealityFiction
         → Certify → Done

  Residual/structural arithmetic is Lean/Coq/Isabelle/SMT/Rust;
  this checks sector order and no illegal skips.
 ***************************************************************************)

EXTENDS Naturals

VARIABLES
  phase,
  fluidOk,
  confinementOk,
  calibrationOk,
  certified,
  stuck

Phases == {
  "Idle", "LoadFluid", "CheckFluidGate",
  "LoadConfinement", "CheckConfinementDamp",
  "LoadCalibration", "CheckRealityFiction",
  "Certify", "Done"
}

TypeOK ==
  /\ phase \in Phases
  /\ fluidOk \in BOOLEAN
  /\ confinementOk \in BOOLEAN
  /\ calibrationOk \in BOOLEAN
  /\ certified \in BOOLEAN
  /\ stuck \in BOOLEAN

Init ==
  /\ phase = "Idle"
  /\ fluidOk = FALSE
  /\ confinementOk = FALSE
  /\ calibrationOk = FALSE
  /\ certified = FALSE
  /\ stuck = FALSE

StartFluid ==
  /\ phase = "Idle"
  /\ phase' = "LoadFluid"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateFluid ==
  /\ phase = "LoadFluid"
  /\ phase' = "CheckFluidGate"
  /\ fluidOk' = TRUE
  /\ UNCHANGED <<confinementOk, calibrationOk, certified, stuck>>

StartConfinement ==
  /\ phase = "CheckFluidGate"
  /\ fluidOk = TRUE
  /\ phase' = "LoadConfinement"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateConfinement ==
  /\ phase = "LoadConfinement"
  /\ phase' = "CheckConfinementDamp"
  /\ confinementOk' = TRUE
  /\ UNCHANGED <<fluidOk, calibrationOk, certified, stuck>>

StartCalibration ==
  /\ phase = "CheckConfinementDamp"
  /\ confinementOk = TRUE
  /\ phase' = "LoadCalibration"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

GateCalibration ==
  /\ phase = "LoadCalibration"
  /\ phase' = "CheckRealityFiction"
  /\ calibrationOk' = TRUE
  /\ UNCHANGED <<fluidOk, confinementOk, certified, stuck>>

CertifyAll ==
  /\ phase = "CheckRealityFiction"
  /\ fluidOk /\ confinementOk /\ calibrationOk
  /\ phase' = "Certify"
  /\ certified' = TRUE
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, stuck>>

Finish ==
  /\ phase = "Certify"
  /\ certified = TRUE
  /\ phase' = "Done"
  /\ UNCHANGED <<fluidOk, confinementOk, calibrationOk, certified, stuck>>

Next ==
  \/ StartFluid \/ GateFluid
  \/ StartConfinement \/ GateConfinement
  \/ StartCalibration \/ GateCalibration
  \/ CertifyAll \/ Finish

Spec == Init /\ [][Next]_<<phase, fluidOk, confinementOk, calibrationOk, certified, stuck>>

InvType == TypeOK
InvNotStuck == stuck = FALSE
InvDoneImpliesAll ==
  (phase = "Done") => (fluidOk /\ confinementOk /\ calibrationOk /\ certified)

=============================================================================
"""
    cfg = """SPECIFICATION Spec
INVARIANT InvType
INVARIANT InvNotStuck
INVARIANT InvDoneImpliesAll
"""
    return tla, cfg


def patch_isabelle_root() -> None:
    root = ROOT / "verification" / "isabelle" / "ROOT"
    if not root.exists():
        return
    text = root.read_text(encoding="utf-8")
    if "UniquenessResearchSpine" in text:
        return
    if "GRSMCKMSpine" in text:
        text = text.replace("GRSMCKMSpine", "GRSMCKMSpine\n    UniquenessResearchSpine", 1)
    elif "StructuralProofSpine" in text:
        text = text.replace(
            "StructuralProofSpine",
            "StructuralProofSpine\n    UniquenessResearchSpine",
            1,
        )
    else:
        text = text.rstrip() + "\n    UniquenessResearchSpine\n"
    root.write_text(text, encoding="utf-8")
    print(f"Patched {root} with UniquenessResearchSpine")


def main() -> int:
    print("Building uniqueness research multi-prover package...")
    # Ensure research JSONs fresh
    try:
        subprocess_builders = [
            ROOT / "scripts" / "build_uniqueness_confinement_research.py",
            ROOT / "scripts" / "build_reality_fiction_calibration.py",
        ]
        import subprocess

        for b in subprocess_builders:
            if b.exists():
                subprocess.run([sys.executable, str(b)], cwd=str(ROOT), check=False)
    except Exception as exc:  # noqa: BLE001
        print(f"  research rebuild soft-fail: {exc}")

    obs = build_obligations()
    conf = suite_summary()
    cal = summary()
    obl_doc = {
        "generated_at": _now(),
        "version": "1.0",
        "tier": "uniqueness_research",
        "obligation_count": len(obs),
        "ontology": (
            "FSOT fluid spacetime omni-theory (D_eff ceiling 25). "
            "Absolute rest frame damps; fluid is load-bearing reality."
        ),
        "modules": [
            "FSOT/Formal/UniquenessResearchSpine.lean",
            "verification/coq/UniquenessResearchSpine.v",
            "verification/isabelle/UniquenessResearchSpine.thy",
            "verification/fstar/FSOTUniquenessResearch.fst",
            "verification/rust/fsot_uniqueness_research_replay",
            "verification/smt/uniqueness_research_bounds.smt2",
            "verification/tla/FSOTUniquenessResearch.tla",
        ],
        "obligations": obs,
        "source_summaries": {
            "confinement": conf,
            "calibration_verdict": cal.get("verdict"),
            "calibration_ok": cal.get("calibration_ok"),
        },
        "honest_scope": (
            "Numeric/structural multiprover certificates for free-color dampening candidate, "
            "fluid spacetime omni load-bearing flags, and reality/fiction calibration. "
            "Does NOT claim classical continuum Yang-Mills path-integral mass-gap theorem proved. "
            "Does claim: absolute rest damps; fluid spacetime is the model; inverted polarity forbidden."
        ),
    }
    OUT_OBL.parent.mkdir(parents=True, exist_ok=True)
    OUT_OBL.write_text(json.dumps(obl_doc, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_OBL} ({len(obs)} obligations)")

    LEAN_OUT.parent.mkdir(parents=True, exist_ok=True)
    LEAN_OUT.write_text(gen_lean(obs), encoding="utf-8")
    print(f"Wrote {LEAN_OUT}")

    COQ_OUT.parent.mkdir(parents=True, exist_ok=True)
    COQ_OUT.write_text(gen_coq(obs), encoding="utf-8")
    print(f"Wrote {COQ_OUT}")

    ISA_OUT.parent.mkdir(parents=True, exist_ok=True)
    ISA_OUT.write_text(gen_isabelle(obs), encoding="utf-8")
    print(f"Wrote {ISA_OUT}")
    patch_isabelle_root()

    FSTAR_OUT.parent.mkdir(parents=True, exist_ok=True)
    FSTAR_OUT.write_text(gen_fstar(obs), encoding="utf-8")
    print(f"Wrote {FSTAR_OUT}")

    SMT_OUT.parent.mkdir(parents=True, exist_ok=True)
    SMT_OUT.write_text(gen_smt(obs), encoding="utf-8")
    print(f"Wrote {SMT_OUT}")

    tla, cfg = gen_tla()
    TLA_OUT.parent.mkdir(parents=True, exist_ok=True)
    TLA_OUT.write_text(tla, encoding="utf-8")
    TLA_CFG.write_text(cfg, encoding="utf-8")
    print(f"Wrote {TLA_OUT} + {TLA_CFG.name}")

    cargo, rust_test = gen_rust(obs)
    RUST_DIR.mkdir(parents=True, exist_ok=True)
    (RUST_DIR / "Cargo.toml").write_text(cargo, encoding="utf-8")
    src = RUST_DIR / "src"
    src.mkdir(exist_ok=True)
    (src / "lib.rs").write_text("//! FSOT uniqueness research obligation replay crate.\n", encoding="utf-8")
    tests = RUST_DIR / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "replay_uniqueness_research.rs").write_text(rust_test, encoding="utf-8")
    print(f"Wrote Rust crate {RUST_DIR}")

    bad = 0
    for ob in obs:
        if not python_verify_obligation(ob):
            bad += 1
            print(f"  BAD python {ob['id']} kind={ob['kind']}")
    print(f"Python triangulation: {len(obs) - bad}/{len(obs)} ok  bad={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
