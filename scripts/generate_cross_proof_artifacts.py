#!/usr/bin/env python3
"""Generate Coq + Isabelle artifacts from exported cross-proof obligations."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBL = ROOT / "verification" / "obligations" / "connective_spine.json"
COQ_OUT = ROOT / "verification" / "coq" / "ConnectiveSpine.v"
ISA_OUT = ROOT / "verification" / "isabelle" / "ConnectiveSpine.thy"


def _coq_lit(v: float) -> str:
    if v == 0.0:
        return "0%R"
    av = abs(v)
    if av >= 1e15 or (av < 1e-6 and av > 0):
        exp = int(math.floor(math.log10(av)))
        mant = v / (10**exp)
        return f"({mant} * 10^{exp})%R"
    return f"({v}%R)"


def _isa_lit(v: float) -> str:
    if v == 0.0:
        return "0"
    av = abs(v)
    if av >= 1e15 or (av < 1e-6 and av > 0):
        exp = int(math.floor(math.log10(av)))
        mant = v / (10**exp)
        return f"({mant} * 10^{exp})"
    return str(v)


def _unique_obligations(obligations: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for ob in obligations:
        key = f"{ob['kind']}:{ob.get('statement')}"
        if key in seen:
            continue
        seen.add(key)
        out.append(ob)
    return out


def gen_coq(obligations: list[dict]) -> str:
    lines = [
        "(* FSOT Tier 79 — connective spine cross-proof (generated). *)",
        "(* Independent of Lean proof terms — same decimal obligations. *)",
        "From Coq Require Import Reals.",
        "From Coq Require Import Psatz.",
        "Local Open Scope R_scope.",
        "",
    ]
    for ob in obligations:
        oid = ob["id"]
        if ob["kind"] == "pos":
            lit = _coq_lit(float(ob["value"]))
            lines += [f"Lemma {oid} : 0 < {lit}.", "Proof. lra. Qed.", ""]
        elif ob["kind"] == "gt_one":
            lit = _coq_lit(float(ob["value"]))
            lines += [f"Lemma {oid} : 1 < {lit}.", "Proof. lra. Qed.", ""]
        elif ob["kind"] == "lt":
            l = _coq_lit(float(ob["left_value"]))
            r = _coq_lit(float(ob["right_value"]))
            lines += [f"Lemma {oid} : {l} < {r}.", "Proof. lra. Qed.", ""]
    return "\n".join(lines) + "\n"


def gen_isabelle(obligations: list[dict]) -> str:
    lines = [
        "(* FSOT Tier 79 — connective spine cross-proof (generated). *)",
        "theory ConnectiveSpine",
        "imports Complex_Main",
        "begin",
        "",
    ]
    for ob in obligations:
        oid = ob["id"]
        if ob["kind"] == "pos":
            lit = _isa_lit(float(ob["value"]))
            lines += [f"lemma {oid}: \"0 < ({lit} :: real)\"", "  by eval", ""]
        elif ob["kind"] == "gt_one":
            lit = _isa_lit(float(ob["value"]))
            lines += [f"lemma {oid}: \"1 < ({lit} :: real)\"", "  by eval", ""]
        elif ob["kind"] == "lt":
            l = _isa_lit(float(ob["left_value"]))
            r = _isa_lit(float(ob["right_value"]))
            lines += [f"lemma {oid}: \"({l} :: real) < ({r} :: real)\"", "  by eval", ""]
    lines += ["end", ""]
    return "\n".join(lines)


def main() -> int:
    doc = json.loads(OBL.read_text(encoding="utf-8"))
    obligations = _unique_obligations(doc["obligations"])
    COQ_OUT.parent.mkdir(parents=True, exist_ok=True)
    ISA_OUT.parent.mkdir(parents=True, exist_ok=True)
    COQ_OUT.write_text(gen_coq(obligations), encoding="utf-8")
    ISA_OUT.write_text(gen_isabelle(obligations), encoding="utf-8")
    print(f"Wrote {COQ_OUT}")
    print(f"Wrote {ISA_OUT} ({len(obligations)} unique obligations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())