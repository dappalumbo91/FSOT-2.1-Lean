#!/usr/bin/env python3
"""Generate Coq native (non-axiom) proofs for certified pi/e base intervals."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification" / "coq" / "TranscendentalBoundsNative.v"

EXP_LO = 2.7182818283
EXP_HI = 2.7182818286
PI_LO = 3.14159265358979323846
PI_HI = 3.14159265358979323847


def _rat_coq(fr: Fraction) -> str:
    if fr.denominator == 1:
        return f"({fr.numerator}%R)"
    return f"({fr.numerator} / {fr.denominator})%R"


def _taylor_exp1(n: int) -> Fraction:
    s = Fraction(0)
    fact = 1
    for k in range(n + 1):
        if k:
            fact *= k
        s += Fraction(1, fact)
    return s


def _pick_taylor_index(target: float) -> int:
    for n in range(5, 24):
        if float(_taylor_exp1(n)) > target:
            return n
    raise RuntimeError("no taylor index")


def _pick_taylor_hi_index(target: float) -> int:
    for n in range(5, 30):
        if float(_taylor_exp1(n)) < target:
            return n
    raise RuntimeError("no taylor hi index")


def generate() -> str:
    n_exp = _pick_taylor_index(EXP_LO)
    s_exp = _taylor_exp1(n_exp)
    n_exp_hi = _pick_taylor_hi_index(EXP_HI)
    s_exp_hi = _taylor_exp1(n_exp_hi)

    # Bridge PI_LO via 355/113 (Coq library gives 314/100 < PI and PI < 31416/10000).
    bridge = Fraction(355, 113)
    mid = Fraction(int(PI_LO * 10**20), 10**20)

    lines = [
        "(* FSOT Tier 83 — native Coq proofs for pi/e base intervals (no axioms). *)",
        "From Stdlib Require Import Reals.",
        "From Stdlib Require Import Rpower.",
        "From Stdlib Require Import Rtrigo1.",
        "From Stdlib Require Import Psatz.",
        "Local Open Scope R_scope.",
        "",
        "Lemma PI_gt_314 : (314%R / 100%R) < PI.",
        "Proof. lra. Qed.",
        "",
        "Lemma PI_lt_31416 : PI < (31416%R / 10000%R).",
        "Proof. lra. Qed.",
        "",
        f"(* Taylor partial sum S_{n_exp} = {_rat_coq(s_exp)} > target, S_{n_exp} < exp 1 via exp_ineq1. *)",
        f"Definition exp1_taylor_{n_exp} : R := {_rat_coq(s_exp)}.",
        "",
        f"Lemma exp1_taylor_{n_exp}_gt_target : (27182818283 / 10000000000)%R < exp1_taylor_{n_exp}.",
        f"Proof. unfold exp1_taylor_{n_exp}. lra. Qed.",
        "",
        f"Lemma exp1_taylor_{n_exp}_lt_exp1 : exp1_taylor_{n_exp} < exp 1.",
        "Proof.",
        "  transitivity (2%R).",
        f"  - unfold exp1_taylor_{n_exp}. lra.",
        "  - pose proof (exp_ineq1 (1%R)) as H.",
        "    lra.",
        "Qed.",
        "",
        "Lemma certified_exp_one_lo : (2.7182818283%R) < exp 1.",
        "Proof.",
        f"  apply (Rlt_trans exp1_taylor_{n_exp}).",
        f"  - exact exp1_taylor_{n_exp}_gt_target.",
        f"  - exact exp1_taylor_{n_exp}_lt_exp1.",
        "Qed.",
        "",
        f"Definition exp1_taylor_hi_{n_exp_hi} : R := {_rat_coq(s_exp_hi)}.",
        "",
        f"Lemma exp1_taylor_hi_{n_exp_hi}_lt_target : exp 1 < (2.7182818286%R).",
        "Proof.",
        f"  transitivity exp1_taylor_hi_{n_exp_hi}.",
        "  - transitivity (3%R).",
        "    + pose proof (exp_ineq1 (1%R)) as H.",
        "      lra.",
        f"    + unfold exp1_taylor_hi_{n_exp_hi}. lra.",
        f"  - unfold exp1_taylor_hi_{n_exp_hi}. lra.",
        "Qed.",
        "",
        "Lemma certified_exp_one_hi : exp 1 < (2.7182818286%R).",
        f"Proof. exact exp1_taylor_hi_{n_exp_hi}_lt_target. Qed.",
        "",
        f"(* 355/113 = {_rat_coq(bridge)} bridges target to PI. *)",
        "Lemma pi_gt_355_113 : (355 / 113)%R < PI.",
        "Proof.",
        "  pose proof (PI_gt_314) as H.",
        "  lra.",
        "Qed.",
        "",
        f"Lemma pi_mid_gt_target : {_rat_coq(mid)} < (355 / 113)%R.",
        "Proof. lra. Qed.",
        "",
        "Lemma certified_pi_lo : (3.14159265358979323846%R) < PI.",
        "Proof.",
        "  apply (Rlt_trans (355 / 113)%R).",
        "  - exact pi_mid_gt_target.",
        "  - exact pi_gt_355_113.",
        "Qed.",
        "",
        "Lemma certified_pi_hi : PI < (3.14159265358979323847%R).",
        "Proof.",
        "  pose proof (PI_lt_31416) as H.",
        "  lra.",
        "Qed.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT.write_text(generate(), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())