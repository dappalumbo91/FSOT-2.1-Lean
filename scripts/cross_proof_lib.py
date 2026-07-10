"""Shared helpers for FSOT cross-proof export, generation, and audit."""

from __future__ import annotations

import math
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "FSOT" / "Formal"
SCALAR = FORMAL / "Scalar.lean"

DEF_R = re.compile(r"def\s+(\w+)\s*:\s*ℝ\s*:=\s*\(([^)]+)\s*:\s*ℝ\)", re.M)
DEF_N = re.compile(r"def\s+(\w+)\s*:\s*ℕ\s*:=\s*(?:\((\d+)\s*:\s*ℕ\)|(\d+))", re.M)
DEF_R_SCALAR = re.compile(r"def\s+(\w+)\s*:\s*Real\s*:=\s*([0-9.eE+-]+)\s*$", re.M)

THM_POS_R = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\(0\s*:\s*ℝ\)\s*<\s*(\w+)\s*(?::=|;)", re.M
)
THM_GT1_R = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\(1\s*:\s*ℝ\)\s*<\s*(\w+)\s*(?::=|;)", re.M
)
THM_LT_R = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*<\s*(\w+)\s*:=", re.M)
THM_LT_HALF = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*<\s*\(0\.5\s*:\s*ℝ\)", re.M)
THM_NAT_POS = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*0\s*<\s*(\w+)\s*(?::=|;)", re.M
)
THM_LT_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*(?::=|;)",
    re.M,
)
THM_GT_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*(?::=|;)",
    re.M,
)
THM_NAT_GT_LIT = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*\((\d+)\s*:\s*ℕ\)\s*<\s*(\w+)", re.M)
THM_NAT_LE_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*(?:≤|<=)\s*\((\d+)\s*:\s*ℕ\)", re.M
)
THM_EQ_N = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*=\s*(\d+)\s*:=", re.M)
THM_EQ_N_SYM = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*=\s*(\w+)\s*:=", re.M)
THM_NAT_MUL_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*\*\s*(\d+)\s*=\s*(\w+)\s*:=", re.M
)
THM_NAT_SUM2_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)\s*:=", re.M
)
THM_NAT_SUM3_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)\s*:=", re.M
)

ISA_LEMMA_RE = re.compile(
    r'lemma\s+(\w+)\s*:\s*"([^"]+)"',
    re.M,
)

COQ_LEMMA_RE = re.compile(
    r"Lemma\s+(\w+)\s*:\s*(.+?)\.\s*\nProof\.\s*(.+?)\.\s*Qed\.",
    re.M,
)

_SCALAR_CACHE: dict[str, float] | None = None


def _reset_scalar_cache() -> None:
    global _SCALAR_CACHE
    _SCALAR_CACHE = None

# High-precision numeric values for symbolic FSOT constants (Bounds.lean certificates).
TRANSCENDENTAL_INTERVAL_SYMBOLS = frozenset({"pi", "e"})

COMPUTED_FSOT_CONSTANTS: dict[str, float] = {
    "psi_con": 0.6321205588287557,
    "eta_eff": 0.46694220658433506,
    "gamma_euler": 0.57721566490153286060651209008240243,
    "catalan_G": 0.91596559417721901505460351493238411,
    "phi": 1.6180339887498948482,
    "pi": 3.1415926535897932384626433832795,
    "e": 2.7182818284590452354,
    "sqrt2": 1.4142135623730951,
    "new_perceived_param": 0.30030117056875677,
}


def _parse_float_lit(s: str) -> float | None:
    try:
        return float(s.replace(" ", ""))
    except ValueError:
        return None


def load_scalar_constants() -> dict[str, float]:
    global _SCALAR_CACHE
    if _SCALAR_CACHE is not None:
        return _SCALAR_CACHE
    out: dict[str, float] = {}
    if SCALAR.exists():
        text = SCALAR.read_text(encoding="utf-8")
        for n, v in DEF_R_SCALAR.findall(text):
            fv = _parse_float_lit(v)
            if fv is not None:
                out[n] = fv
        for n, v in DEF_R.findall(text):
            fv = _parse_float_lit(v)
            if fv is not None:
                out[n] = fv
    for name, val in COMPUTED_FSOT_CONSTANTS.items():
        out.setdefault(name, val)
    _SCALAR_CACHE = out
    return out


def _decimal_plain(v: float) -> str:
    d = Decimal(str(v)) if "e" not in repr(v) else Decimal(repr(v))
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def coq_lit_real(v: float) -> str:
    if v == 0.0:
        return "0%R"
    av = abs(v)
    if av >= 1e15:
        exp = int(math.floor(math.log10(av)))
        mant = v / (10**exp)
        return f"({mant} * (10 ^ {exp}))%R"
    if av < 1.0 or "e" in repr(v).lower():
        return f"({_decimal_plain(v)}%R)"
    return f"({v}%R)"


def coq_lit_nat(v: int) -> str:
    return str(int(v))


def _collect_defs(text: str, global_r: dict[str, float], global_n: dict[str, int]) -> tuple[dict[str, float], dict[str, int]]:
    r_defs = dict(global_r)
    n_defs = dict(global_n)
    for n, v in DEF_R.findall(text):
        fv = _parse_float_lit(v)
        if fv is not None:
            r_defs[n] = fv
    for n, paren_v, bare_v in DEF_N.findall(text):
        n_defs[n] = int(paren_v or bare_v)
    return r_defs, n_defs


def parse_formal_module(
    path: Path,
    *,
    require_norm_num: bool = False,
    global_r: dict[str, float] | None = None,
    global_n: dict[str, int] | None = None,
    source_tier: str = "priors",
) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if require_norm_num and "norm_num" not in text:
        return []
    r_defs, n_defs = _collect_defs(text, global_r or {}, global_n or {})
    out: list[dict] = []
    seen_ids: set[str] = set()
    kind_priority = {
        "pos": 10,
        "gt_one": 10,
        "lt_half": 10,
        "nat_pos": 10,
        "lt": 9,
        "eq_nat": 9,
        "eq_nat_arith": 9,
        "lt_lit": 5,
        "gt_lit": 5,
        "nat_gt_lit": 5,
        "nat_le_lit": 5,
    }
    by_id: dict[str, dict] = {}

    def add(ob: dict) -> None:
        sym = ob.get("symbol")
        if sym in TRANSCENDENTAL_INTERVAL_SYMBOLS and ob["kind"] in ("gt_lit", "lt_lit"):
            return
        oid = ob["id"]
        pri = kind_priority.get(ob["kind"], 0)
        if oid in by_id:
            if pri <= kind_priority.get(by_id[oid]["kind"], 0):
                return
        by_id[oid] = ob

    def flush() -> None:
        nonlocal out, seen_ids
        for oid, ob in by_id.items():
            if oid in seen_ids:
                continue
            seen_ids.add(oid)
            ob["lean_module"] = path.stem
            ob["source_file"] = path.name
            ob["source_tier"] = source_tier
            out.append(ob)

    for thm, sym in THM_POS_R.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "pos", "symbol": sym, "value": r_defs[sym], "statement": f"0 < {r_defs[sym]}"})
    for thm, sym in THM_GT1_R.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "gt_one", "symbol": sym, "value": r_defs[sym], "statement": f"1 < {r_defs[sym]}"})
    for thm, left, right in THM_LT_R.findall(text):
        if left in r_defs and right in r_defs:
            add(
                {
                    "id": thm,
                    "kind": "lt",
                    "left": left,
                    "right": right,
                    "left_value": r_defs[left],
                    "right_value": r_defs[right],
                    "statement": f"{r_defs[left]} < {r_defs[right]}",
                }
            )
    for thm, sym in THM_LT_HALF.findall(text):
        if sym in r_defs:
            add({"id": thm, "kind": "lt_half", "symbol": sym, "value": r_defs[sym], "statement": f"{r_defs[sym]} < 0.5"})
    for thm, sym in THM_NAT_POS.findall(text):
        if sym in n_defs:
            add({"id": thm, "kind": "nat_pos", "symbol": sym, "value": n_defs[sym], "statement": f"0 < {n_defs[sym]}"})
        elif sym in r_defs:
            add({"id": thm, "kind": "pos", "symbol": sym, "value": r_defs[sym], "statement": f"0 < {r_defs[sym]}"})

    for thm, sym, lit in THM_LT_LIT.findall(text):
        if sym not in r_defs:
            continue
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        if abs(bound - 0.5) < 1e-12:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": sym,
                "value": r_defs[sym],
                "bound": bound,
                "statement": f"{r_defs[sym]} < {bound}",
            }
        )
    for thm, lit, sym in THM_GT_LIT.findall(text):
        if sym not in r_defs:
            continue
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        add(
            {
                "id": thm,
                "kind": "gt_lit",
                "symbol": sym,
                "value": r_defs[sym],
                "bound": bound,
                "statement": f"{bound} < {r_defs[sym]}",
            }
        )
    for thm, lit, sym in THM_NAT_GT_LIT.findall(text):
        if sym not in n_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "nat_gt_lit",
                "symbol": sym,
                "value": n_defs[sym],
                "bound": int(lit),
                "statement": f"{lit} < {n_defs[sym]}",
            }
        )
    for thm, sym, lit in THM_NAT_LE_LIT.findall(text):
        if sym not in n_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "nat_le_lit",
                "symbol": sym,
                "value": n_defs[sym],
                "bound": int(lit),
                "statement": f"{n_defs[sym]} <= {lit}",
            }
        )
    for thm, left, lit in THM_EQ_N.findall(text):
        if left not in n_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "left": left,
                "right_value": int(lit),
                "value": n_defs[left],
                "statement": f"{n_defs[left]} = {lit}",
            }
        )
    for thm, left, right in THM_EQ_N_SYM.findall(text):
        if left not in n_defs or right not in n_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "left": left,
                "right": right,
                "value": n_defs[left],
                "right_value": n_defs[right],
                "statement": f"{n_defs[left]} = {n_defs[right]}",
            }
        )
    for thm, a, k, b in THM_NAT_MUL_EQ.findall(text):
        if a not in n_defs or b not in n_defs:
            continue
        lhs = n_defs[a] * int(k)
        rhs = n_defs[b]
        add(
            {
                "id": thm,
                "kind": "eq_nat_arith",
                "expr": f"{n_defs[a]}*{k}",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
            }
        )
    for thm, a, b, c in THM_NAT_SUM2_EQ.findall(text):
        if a not in n_defs or b not in n_defs or c not in n_defs:
            continue
        lhs = n_defs[a] + n_defs[b]
        rhs = n_defs[c]
        add(
            {
                "id": thm,
                "kind": "eq_nat_arith",
                "expr": f"{n_defs[a]}+{n_defs[b]}",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
            }
        )
    for thm, a, b, d, c in THM_NAT_SUM3_EQ.findall(text):
        if a not in n_defs or b not in n_defs or d not in n_defs or c not in n_defs:
            continue
        lhs = n_defs[a] + n_defs[b] + n_defs[d]
        rhs = n_defs[c]
        add(
            {
                "id": thm,
                "kind": "eq_nat_arith",
                "expr": f"{n_defs[a]}+{n_defs[b]}+{n_defs[d]}",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
            }
        )

    flush()
    return out


def parse_priors_module(path: Path) -> list[dict]:
    return parse_formal_module(path, require_norm_num=True, source_tier="priors")


def make_unique_coq_ids(obligations: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for ob in obligations:
        base = ob["id"]
        coq_id = base
        if coq_id in seen:
            coq_id = f"{ob['lean_module']}_{base}"
        n = 2
        while coq_id in seen:
            coq_id = f"{ob['lean_module']}_{base}_{n}"
            n += 1
        seen.add(coq_id)
        ob = dict(ob)
        ob["coq_id"] = coq_id
        out.append(ob)
    return out


def obligation_margin(ob: dict) -> Decimal | None:
    kind = ob["kind"]
    if kind == "pos":
        return Decimal(str(ob["value"]))
    if kind == "gt_one":
        return Decimal(str(ob["value"])) - Decimal(1)
    if kind == "lt_half":
        return Decimal("0.5") - Decimal(str(ob["value"]))
    if kind == "lt_lit":
        return Decimal(str(ob["bound"])) - Decimal(str(ob["value"]))
    if kind == "gt_lit":
        return Decimal(str(ob["value"])) - Decimal(str(ob["bound"]))
    if kind == "lt":
        return Decimal(str(ob["right_value"])) - Decimal(str(ob["left_value"]))
    if kind == "nat_pos":
        return Decimal(int(ob["value"]))
    if kind == "nat_gt_lit":
        return Decimal(int(ob["value"])) - Decimal(int(ob["bound"]))
    if kind == "nat_le_lit":
        return Decimal(int(ob["bound"])) - Decimal(int(ob["value"]))
    return None


def obligation_provable(ob: dict) -> bool:
    return python_verify_obligation(ob)


def obligation_margin_violation(ob: dict) -> dict | None:
    if obligation_provable(ob):
        return None
    kind = ob["kind"]
    if kind in ("lt_half", "lt_lit"):
        val = Decimal(str(ob["value"]))
        bound = Decimal(str(ob.get("bound", "0.5")))
        return {
            "violation_kind": "exceeds_bound",
            "bound": str(bound),
            "actual": str(val),
            "overrun": str(val - bound),
            "margin_to_bound": str(bound - val),
        }
    if kind == "pos":
        return {"violation_kind": "non_positive", "actual": str(ob["value"])}
    if kind == "gt_one":
        val = Decimal(str(ob["value"]))
        return {"violation_kind": "not_gt_one", "actual": str(val), "shortfall": str(Decimal(1) - val)}
    if kind == "gt_lit":
        val = Decimal(str(ob["value"]))
        bound = Decimal(str(ob["bound"]))
        return {"violation_kind": "below_literal_bound", "bound": str(bound), "actual": str(val)}
    if kind == "lt":
        return {
            "violation_kind": "ordering_false",
            "left": str(ob["left_value"]),
            "right": str(ob["right_value"]),
        }
    if kind in ("nat_pos", "nat_gt_lit"):
        return {"violation_kind": "non_positive_nat", "actual": str(ob["value"])}
    if kind == "nat_le_lit":
        return {"violation_kind": "nat_le_false", "actual": str(ob["value"]), "bound": str(ob["bound"])}
    if kind in ("eq_nat", "eq_nat_arith"):
        return {
            "violation_kind": "equality_false",
            "left": str(ob.get("value")),
            "right": str(ob.get("right_value")),
        }
    return {"violation_kind": "unknown", "kind": kind}


def python_verify_obligation(ob: dict) -> bool:
    kind = ob["kind"]
    if kind == "pos":
        return Decimal(str(ob["value"])) > 0
    if kind == "gt_one":
        return Decimal(str(ob["value"])) > 1
    if kind == "lt":
        return Decimal(str(ob["left_value"])) < Decimal(str(ob["right_value"]))
    if kind == "lt_half":
        return Decimal(str(ob["value"])) < Decimal("0.5")
    if kind == "lt_lit":
        return Decimal(str(ob["value"])) < Decimal(str(ob["bound"]))
    if kind == "gt_lit":
        return Decimal(str(ob["value"])) > Decimal(str(ob["bound"]))
    if kind == "nat_pos":
        return int(ob["value"]) > 0
    if kind == "nat_gt_lit":
        return int(ob["value"]) > int(ob["bound"])
    if kind == "nat_le_lit":
        return int(ob["value"]) <= int(ob["bound"])
    if kind in ("eq_nat", "eq_nat_arith"):
        return int(ob["value"]) == int(ob["right_value"])
    return False


def gen_coq_lemma(ob: dict) -> tuple[str, str, str]:
    oid = ob.get("coq_id", ob["id"])
    kind = ob["kind"]
    if kind == "pos":
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"0 < {lit}", "lra"
    if kind == "gt_one":
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"1 < {lit}", "lra"
    if kind == "lt":
        l = coq_lit_real(float(ob["left_value"]))
        r = coq_lit_real(float(ob["right_value"]))
        return oid, f"{l} < {r}", "lra"
    if kind == "lt_half":
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lit} < (0.5%R)", "lra"
    if kind == "lt_lit":
        lit = coq_lit_real(float(ob["value"]))
        b = coq_lit_real(float(ob["bound"]))
        return oid, f"{lit} < {b}", "lra"
    if kind == "gt_lit":
        b = coq_lit_real(float(ob["bound"]))
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{b} < {lit}", "lra"
    if kind == "nat_pos":
        lit = coq_lit_nat(int(ob["value"]))
        return oid, f"(0 < {lit})%nat", "apply Nat.ltb_lt; reflexivity"
    if kind == "nat_gt_lit":
        lit = coq_lit_nat(int(ob["value"]))
        b = coq_lit_nat(int(ob["bound"]))
        return oid, f"({b} < {lit})%nat", "apply Nat.ltb_lt; reflexivity"
    if kind == "nat_le_lit":
        lit = coq_lit_nat(int(ob["value"]))
        b = coq_lit_nat(int(ob["bound"]))
        return oid, f"({lit} <= {b})%nat", "apply Nat.leb_le; reflexivity"
    if kind in ("eq_nat", "eq_nat_arith"):
        l = coq_lit_nat(int(ob["value"]))
        r = coq_lit_nat(int(ob["right_value"]))
        return oid, f"({l} = {r})%nat", "reflexivity"
    raise ValueError(f"unsupported obligation kind: {kind}")


def gen_coq_chunk(
    obligations: list[dict],
    chunk_idx: int,
    chunk_total: int,
    spine_name: str = "FullFormalSpine",
) -> str:
    lines = [
        f"(* FSOT Tier 80 — {spine_name} chunk {chunk_idx + 1}/{chunk_total} (generated). *)",
        "(* Independent of Lean proof terms — same decimal obligations. *)",
        "From Stdlib Require Import Reals.",
        "From Stdlib Require Import Psatz.",
        "From Stdlib Require Import Lia.",
        "From Stdlib Require Import Arith.",
        "Local Open Scope R_scope.",
        "",
    ]
    for ob in obligations:
        oid, stmt, tac = gen_coq_lemma(ob)
        lines += [f"Lemma {oid} : {stmt}.", f"Proof. {tac}. Qed.", ""]
    return "\n".join(lines) + "\n"


def isa_lit_real(v: float) -> str:
    if v == 0.0:
        return "0"
    av = abs(v)
    if av < 1e-3 or "e" in f"{v:.12g}".lower():
        digits = max(6, int(-math.floor(math.log10(av))) + 6) if av > 0 else 6
        return f"{v:.{digits}f}".rstrip("0").rstrip(".") or "0"
    if av >= 1e15:
        exp = int(math.floor(math.log10(av)))
        mant = v / (10**exp)
        return f"({mant} * 10 ^ ({exp} :: real))"
    plain = _decimal_plain(v)
    return plain if "." in plain else f"{plain}.0"


def isa_lit_nat(v: int) -> str:
    return str(int(v))


def gen_isabelle_lemma(ob: dict) -> tuple[str, str]:
    oid = ob.get("coq_id", ob["id"])
    kind = ob["kind"]
    if kind == "pos":
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"0 < ({lit} :: real)"
    if kind == "gt_one":
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"1 < ({lit} :: real)"
    if kind == "lt":
        l = isa_lit_real(float(ob["left_value"]))
        r = isa_lit_real(float(ob["right_value"]))
        return oid, f"({l} :: real) < ({r} :: real)"
    if kind == "lt_half":
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lit} :: real) < (0.5 :: real)"
    if kind == "lt_lit":
        lit = isa_lit_real(float(ob["value"]))
        b = isa_lit_real(float(ob["bound"]))
        return oid, f"({lit} :: real) < ({b} :: real)"
    if kind == "gt_lit":
        b = isa_lit_real(float(ob["bound"]))
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({b} :: real) < ({lit} :: real)"
    if kind == "nat_pos":
        lit = isa_lit_nat(int(ob["value"]))
        return oid, f"0 < ({lit} :: nat)"
    if kind == "nat_gt_lit":
        lit = isa_lit_nat(int(ob["value"]))
        b = isa_lit_nat(int(ob["bound"]))
        return oid, f"({b} :: nat) < ({lit} :: nat)"
    if kind == "nat_le_lit":
        lit = isa_lit_nat(int(ob["value"]))
        b = isa_lit_nat(int(ob["bound"]))
        return oid, f"({lit} :: nat) <= ({b} :: nat)"
    if kind in ("eq_nat", "eq_nat_arith"):
        l = isa_lit_nat(int(ob["value"]))
        r = isa_lit_nat(int(ob["right_value"]))
        return oid, f"({l} :: nat) = ({r} :: nat)"
    raise ValueError(f"unsupported obligation kind: {kind}")


def gen_isabelle_chunk(
    obligations: list[dict],
    chunk_idx: int,
    chunk_total: int,
    *,
    theory_name: str | None = None,
    spine_name: str = "FullFormalSpine",
) -> str:
    theory = theory_name or f"{spine_name}_{chunk_idx:02d}"
    lines = [
        f"(* FSOT Tier 81 — {spine_name} chunk {chunk_idx + 1}/{chunk_total} (generated). *)",
        f"theory {theory}",
        "imports Complex_Main",
        "begin",
        "",
    ]
    for ob in obligations:
        oid, stmt = gen_isabelle_lemma(ob)
        lines += [f"lemma {oid}: \"{stmt}\"", "  by eval", ""]
    lines += ["end", ""]
    return "\n".join(lines)


def gen_isabelle_connective(obligations: list[dict]) -> str:
    seen: set[str] = set()
    unique: list[dict] = []
    for ob in obligations:
        key = f"{ob['kind']}:{ob.get('statement')}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(ob)
    lines = [
        "(* FSOT Tier 79 — connective spine cross-proof (generated). *)",
        "theory ConnectiveSpine",
        "imports Complex_Main",
        "begin",
        "",
    ]
    for ob in unique:
        oid, stmt = gen_isabelle_lemma(ob)
        lines += [f"lemma {oid}: \"{stmt}\"", "  by eval", ""]
    lines += ["end", ""]
    return "\n".join(lines)


def gen_isabelle_root(
    theory_names: list[str],
    *,
    session_name: str = "FSOT_CrossProof",
    description: str | None = None,
) -> str:
    desc = description or f"FSOT full-scope cross-proof ({len(theory_names)} theories)"
    lines = [
        "(* FSOT cross-proof Isabelle session (generated). *)",
        "",
        f"session {session_name} = HOL +",
        f'  description "{desc}"',
        "  theories",
    ]
    lines.extend(f"    {name}" for name in theory_names)
    lines.append("")
    return "\n".join(lines) + "\n"


def isabelle_chunk_session_name(theory: str) -> str:
    return f"FSOT_Diag_{theory}"


def parse_isabelle_theory_lemmas(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    return [
        {"id": m.group(1), "statement": m.group(2).strip()}
        for m in ISA_LEMMA_RE.finditer(text)
    ]