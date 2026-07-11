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
DEF_R_EXPR = re.compile(r"def\s+(\w+)\s*:\s*ℝ\s*:=\s*(.+?)\s*$", re.M)
DEF_N = re.compile(r"def\s+(\w+)\s*:\s*ℕ\s*:=\s*(?:\((\d+)\s*:\s*ℕ\)|(\d+))", re.M)
DEF_Z = re.compile(r"def\s+(\w+)\s*:\s*ℤ\s*:=\s*(-?\d+)", re.M)
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
THM_ABS_DIFF_LT_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\|(\w+)\s*-\s*(\w+)\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
PROOF_CERTIFICATE_MARKERS = (
    "norm_num",
    "nlinarith",
    "linarith",
    "decide",
    "native_decide",
    "ring_nf",
    "omega",
)
THM_GT_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*(?::=|;)",
    re.M,
)
THM_NAT_GT_LIT = re.compile(r"(?:theorem|lemma)\s+(\w+)\s*:\s*\((\d+)\s*:\s*ℕ\)\s*<\s*(\w+)", re.M)
THM_NAT_LE_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*(?:≤|<=)\s*\((\d+)\s*:\s*ℕ\)", re.M
)
THM_NAT_LE_SYM = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(\w+)\s*(?:≤|<=)\s*(\w+)\s*:=", re.M
)
THM_R_NONNEG = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(?:\(0\s*:\s*ℝ\)|0)\s*(?:≤|<=)\s*(\w+)\s*:=", re.M
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
THM_NAT_POW_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*\^\s*(\d+)\s*=\s*(\d+)\s*:=", re.M
)
THM_INT_TUPLE3_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\((\w+),\s*(\w+),\s*(\w+)\)\s*=\s*\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)\s*:=",
    re.M,
)
THM_R_EQ_SYM = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(.+?)\s*=\s*(\w+)\s*:=", re.M
)
THM_R_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(.+?)\s*=\s*(.+?)\s*:=", re.M
)
THM_R_INTERVAL = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*∧\s*\3\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_R_INTERVAL_LE = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(\w+)\s*∧\s*\3\s*(?:≤|<=)\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_R_LT_LIT_PURE = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*:=",
    re.M,
)
THM_R_LE_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*(?:≤|<=)\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*:=",
    re.M,
)
THM_R_LE_SYM = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*(?:≤|<=)\s*(\w+)\s*:=", re.M
)
THM_NAT_LT_SYM = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*<\s*(\w+)\s*:=", re.M
)
THM_NAT_SUM6_EQ = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)\s*:=",
    re.M,
)
THM_NAT_SUM2_POS = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*0\s*<\s*(\w+)\s*\+\s*(\w+)\s*:=", re.M
)
THM_ABS_DIFF_SYM_LT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\|(\w+)\s*-\s*(\w+)\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_ABS_SYM_INTERVAL = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*\|(\w+)\|\s*∧\s*\|\3\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_RAW_S_GT_ZERO = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*raw_S \(get_domain_params \"(\w+)\"\)\s*>\s*0",
    re.M,
)
THM_RAW_S_POS_ALT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(0\s*:\s*ℝ\)\s*<\s*raw_S\s*\(get_domain_params \"(\w+)\"\)",
    re.M,
)
THM_RAW_S_LT_ZERO = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*raw_S \(get_domain_params \"(\w+)\"\)\s*<\s*0",
    re.M,
)
THM_RAW_S_NONPOS = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*raw_S \(get_domain_params \"(\w+)\"\)\s*(?:≤|<=)\s*0",
    re.M,
)
THM_R_GT_ZERO_FUNC = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(0\s*:\s*ℝ\)\s*<\s*(\w+)\s+(\w+)\s+(\w+)\s*(?::=|;)",
    re.M,
)
THM_ALIAS_REF = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:[\s\S]*?:=\s*\n\s*(\w+)\s*(?:\n|$)",
    re.M,
)
THM_ABS_FUNC_CANON_LT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\|(\w+)\s+(\w+)(?:\s+(\w+))?\s*-\s*(\w+)\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_ABS_DIFF_SYM_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\|(\w+)\s*-\s*([0-9.eE+-]+)\|\s*<\s*(?:\(([0-9.eE+-]+)\s*:\s*ℝ\)|([0-9.eE+-]+))",
    re.M,
)
THM_ABS_DIFF_EXPR_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\|(.+?)\s*-\s*([0-9.eE+-]+)\|\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)",
    re.M,
)
THM_R_LT_ZERO = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(\w+)\s*<\s*0\s*:=",
    re.M,
)
THM_GT_LIT_EXPR = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*<\s*(.+?)\s*:=\s*by",
    re.M,
)
THM_LT_EXPR_LIT = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*(.+?)\s*<\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*:=\s*by",
    re.M,
)
THM_DOMAIN_OBSERVED = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(get_domain_params "(\w+)"\)\.observed = (true|false)',
    re.M,
)
THM_DOMAIN_D_EFF = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(get_domain_params "(\w+)"\)\.D_eff = (\d+)',
    re.M,
)
THM_DOMAIN_DELTA_INTERVAL = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*\(([0-9.eE+-]+)\s*:\s*ℝ\)\s*(?:≤|<=)\s*\(get_domain_params "(\w+)"\)\.delta_psi\s*∧\s*\(get_domain_params "\3"\)\.delta_psi\s*(?:≤|<=)\s*(?:\(([0-9.eE+-]+)\s*:\s*ℝ\)|([0-9.eE+-]+))',
    re.M,
)
THM_TERM1_LT_ZERO = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*term1 \(get_domain_params "(\w+)"\) < 0',
    re.M,
)
THM_TERM2_EQ_ONE = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*term2 \(get_domain_params "(\w+)"\) = 1',
    re.M,
)
THM_TERM1_DOMINATES_TERM3 = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*(?:(?!:=).)*abs \(term3 \(get_domain_params "(\w+)"\)\)\s*<\s*abs \(term1 \(get_domain_params "\2"\)\)',
    re.S,
)
THM_TERM3_ABS_LT = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*abs \(term3 \(get_domain_params "(\w+)"\)\) < \(([0-9.eE+-]+)\s*:\s*ℝ\)',
    re.M,
)
THM_DOMAIN_PARAMS_EQ = re.compile(
    r'(?:theorem|lemma)\s+(\w+)\s*:\s*\n?\s*get_domain_params "(\w+)" = get_domain_params "(\w+)"',
    re.M,
)
THM_DARK_ENERGY_PARAMS_EQ = re.compile(
    r'lemma dark_energy_params_eq\s*:\s*\n?\s*get_domain_params "dark_energy"\s*=\s*\{ D_eff := (\d+), recent_hits := (\d+), delta_psi := ([0-9.eE+-]+), observed := (true|false) \}',
    re.M,
)
THM_PHI_NE_ZERO = re.compile(r"lemma\s+(\w+)\s*:\s*phi\s*≠\s*0", re.M)
THM_PHI_SQ_NE_ZERO = re.compile(r"lemma\s+(\w+)\s*:\s*phi\s*\^\s*2\s*≠\s*0", re.M)

GENOMIC = FORMAL / "Genomic.lean"
_GENOMIC_CACHE: tuple[dict[str, float], dict[str, int], dict[str, int]] | None = None
_DOMAIN_RAW_S_CACHE: dict[str, float] | None = None

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
    "k": 0.420222080893624,
    "acoustic_bleed": 1.046973630587551,
    "acoustic_inflow": 1.6668538450045731,
    "gamma_euler": 0.57721566490153286060651209008240243,
}


def _parse_float_lit(s: str) -> float | None:
    try:
        return float(s.replace(" ", ""))
    except ValueError:
        return None


def _normalize_r_expr(expr: str) -> str:
    e = expr.strip().replace("\n", " ")
    e = re.sub(r"\s+", " ", e)
    e = re.sub(r"\((-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*:\s*ℝ\)", r"\1", e)
    e = re.sub(r"\((-?\d+)\s*:\s*ℤ\)", r"\1", e)
    e = re.sub(r"\((\w+)\s*:\s*ℝ\)", r"\1", e)
    e = re.sub(r"\((\w+)\s*:\s*ℕ\)", r"\1", e)
    e = re.sub(r"\brpow\s+(\w+)\s*\(([^)]+)\)", r"\1 ^ (\2)", e)
    e = re.sub(r"\|([^|]+)\|", r"abs(\1)", e)
    for fn in ("exp", "log", "cos", "sin", "sqrt"):
        e = re.sub(rf"\b{fn}\s+(-?[\d.]+)\b", rf"{fn}(\1)", e)
        e = re.sub(rf"\b{fn}\s+(\w+)\b", rf"{fn}(\1)", e)
    return e.strip()


def _eval_wave1_func(
    func: str,
    args: list[str],
    r_defs: dict[str, float],
) -> float | None:
    if not all(a in r_defs for a in args):
        return None
    vals = [float(r_defs[a]) for a in args]
    try:
        if func == "h0_fsot" and len(vals) == 1:
            s = vals[0]
            return 100.0 * (1.0 + s * r_defs["acoustic_bleed"] / r_defs["acoustic_inflow"])
        if func == "t_cmb_fsot" and len(vals) == 1:
            s = vals[0]
            return r_defs["phi"] ** 2 + r_defs["gamma_euler"] / r_defs["e"] * abs(s)
        if func == "n_s_fsot" and len(vals) == 1:
            s = vals[0]
            c_cosm = r_defs.get("c_cosm")
            if c_cosm is None:
                c_cosm = 1.0 / (r_defs["phi"] * 10.0)
            return 1.0 + s * c_cosm * (r_defs["phi"] ** (1.0 / r_defs["pi"]))
        if func == "omega_b_h2_fsot" and len(vals) == 2:
            return abs(vals[0]) * (1.0 - vals[1])
    except (KeyError, ZeroDivisionError, OverflowError, ValueError):
        return None
    return None


def _tokenize_r_expr(expr: str) -> list[str]:
    e = _normalize_r_expr(expr)
    tokens: list[str] = []
    i = 0
    while i < len(e):
        ch = e[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "()+-*/^":
            tokens.append(ch)
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < len(e) and e[i + 1].isdigit()):
            j = i
            while j < len(e) and (e[j].isdigit() or e[j] in ".eE+-"):
                j += 1
            tokens.append(e[i:j])
            i = j
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < len(e) and (e[j].isalnum() or e[j] == "_"):
                j += 1
            tokens.append(e[i:j])
            i = j
            continue
        return []
    return tokens


def _lookup_r_symbol(name: str, r_defs: dict[str, float], n_defs: dict[str, int]) -> float | None:
    if name in r_defs:
        return float(r_defs[name])
    if name in n_defs:
        return float(n_defs[name])
    if name in COMPUTED_FSOT_CONSTANTS:
        return float(COMPUTED_FSOT_CONSTANTS[name])
    return None


def _parse_r_atom(
    tokens: list[str],
    pos: int,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> tuple[float, int]:
    if pos >= len(tokens):
        raise ValueError("unexpected end")
    tok = tokens[pos]
    if tok == "(":
        val, pos = _parse_r_expr(tokens, pos + 1, r_defs, n_defs)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("missing )")
        return val, pos + 1
    if tok == "abs":
        if pos + 1 >= len(tokens) or tokens[pos + 1] != "(":
            raise ValueError("abs requires (")
        val, pos = _parse_r_expr(tokens, pos + 2, r_defs, n_defs)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("missing ) after abs")
        return abs(val), pos + 1
    if tok in ("exp", "log", "cos", "sin", "sqrt"):
        if pos + 1 < len(tokens) and tokens[pos + 1] == "(":
            val, pos = _parse_r_expr(tokens, pos + 2, r_defs, n_defs)
            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError(f"missing ) after {tok}")
            pos += 1
        else:
            val, pos = _parse_r_atom(tokens, pos + 1, r_defs, n_defs)
        if tok == "exp":
            return math.exp(val), pos
        if tok == "log":
            if val <= 0:
                raise ValueError("log domain")
            return math.log(val), pos
        if tok == "cos":
            return math.cos(val), pos
        if tok == "sin":
            return math.sin(val), pos
        if val < 0:
            raise ValueError("sqrt domain")
        return math.sqrt(val), pos
    if tok == "-":
        val, pos = _parse_r_atom(tokens, pos + 1, r_defs, n_defs)
        return -val, pos
    if re.fullmatch(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", tok):
        return float(tok), pos + 1
    val = _lookup_r_symbol(tok, r_defs, n_defs)
    if val is None:
        raise ValueError(f"unknown symbol {tok}")
    return val, pos + 1


def _parse_r_power(
    tokens: list[str],
    pos: int,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> tuple[float, int]:
    val, pos = _parse_r_atom(tokens, pos, r_defs, n_defs)
    while pos < len(tokens) and tokens[pos] == "^":
        exp, pos = _parse_r_atom(tokens, pos + 1, r_defs, n_defs)
        val = val ** exp
    return val, pos


def _parse_r_term(
    tokens: list[str],
    pos: int,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> tuple[float, int]:
    val, pos = _parse_r_power(tokens, pos, r_defs, n_defs)
    while pos < len(tokens) and tokens[pos] in ("*", "/"):
        op = tokens[pos]
        rhs, pos = _parse_r_power(tokens, pos + 1, r_defs, n_defs)
        if op == "*":
            val *= rhs
        else:
            val /= rhs
    return val, pos


def _parse_r_expr(
    tokens: list[str],
    pos: int,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> tuple[float, int]:
    if pos < len(tokens) and tokens[pos] == "-":
        val, pos = _parse_r_term(tokens, pos, r_defs, n_defs)
        return val, pos
    val, pos = _parse_r_term(tokens, pos, r_defs, n_defs)
    while pos < len(tokens) and tokens[pos] in ("+", "-"):
        op = tokens[pos]
        rhs, pos = _parse_r_term(tokens, pos + 1, r_defs, n_defs)
        if op == "+":
            val += rhs
        else:
            val -= rhs
    return val, pos


def _eval_r_expr(expr: str, r_defs: dict[str, float], n_defs: dict[str, int]) -> float | None:
    tokens = _tokenize_r_expr(expr)
    if not tokens:
        return None
    try:
        val, pos = _parse_r_expr(tokens, 0, r_defs, n_defs)
        if pos != len(tokens):
            return None
        return val
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def _r_values_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _domain_params_match(a: object, b: object) -> bool:
    fields = ("N", "P", "D_eff", "recent_hits", "delta_psi", "delta_theta", "rho", "scale", "amplitude", "trend_bias", "observed")
    return all(getattr(a, f) == getattr(b, f) for f in fields)


def load_domain_term_oracle() -> dict[str, dict[str, float]]:
    try:
        from domain_scalar_oracle import term1, term2, term3  # noqa: WPS433
    except ImportError:
        return {}
    return {
        name: {"term1": term1(p), "term2": term2(p), "term3": term3(p)}
        for name, p in load_domain_params_oracle().items()
    }


def load_domain_params_oracle() -> dict[str, object]:
    try:
        from domain_scalar_oracle import DOMAINS, FSOTParams  # noqa: WPS433
    except ImportError:
        return {}
    domains = dict(DOMAINS)
    domains.update(
        {
            "cosmological": FSOTParams(D_eff=25, recent_hits=0, delta_psi=1.0, observed=False),
            "dark_energy": FSOTParams(D_eff=25, recent_hits=0, delta_psi=1.1, observed=False),
            "cellular": FSOTParams(D_eff=12, recent_hits=0, delta_psi=0.08, observed=False),
        }
    )
    return domains


def load_domain_raw_S_oracle() -> dict[str, float]:
    global _DOMAIN_RAW_S_CACHE
    if _DOMAIN_RAW_S_CACHE is not None:
        return _DOMAIN_RAW_S_CACHE
    try:
        from domain_scalar_oracle import DOMAINS, FSOTParams, raw_S  # noqa: WPS433
    except ImportError:
        _DOMAIN_RAW_S_CACHE = {}
        return _DOMAIN_RAW_S_CACHE
    domains = dict(DOMAINS)
    domains.update(
        {
            "cosmological": FSOTParams(D_eff=25, recent_hits=0, delta_psi=1.0, observed=False),
            "dark_energy": FSOTParams(D_eff=25, recent_hits=0, delta_psi=1.1, observed=False),
            "cmb": FSOTParams(D_eff=24, recent_hits=0, delta_psi=0.8, observed=False),
            "cellular": FSOTParams(D_eff=12, recent_hits=0, delta_psi=0.08, observed=False),
            "higgs": FSOTParams(D_eff=7, recent_hits=1, delta_psi=0.95, observed=True),
            "galactic": FSOTParams(D_eff=21, recent_hits=1, delta_psi=0.9, observed=True),
            "fusion": FSOTParams(D_eff=16, recent_hits=1, delta_psi=0.95, observed=True),
            "proton": FSOTParams(D_eff=8, recent_hits=0, delta_psi=0.7, observed=True),
            "blackhole": FSOTParams(D_eff=23, recent_hits=2, delta_psi=1.25, observed=True),
            "astronomical": FSOTParams(D_eff=20, recent_hits=1, delta_psi=1.0, observed=True),
        }
    )
    _DOMAIN_RAW_S_CACHE = {name: raw_S(p) for name, p in domains.items()}
    return _DOMAIN_RAW_S_CACHE


def load_formal_extended_globals() -> tuple[dict[str, float], dict[str, int], dict[str, int]]:
    """Merge scalar, genomic/codon, cosmology, and domain-oracle constants for extended formal modules."""
    gen_r, gen_n, gen_z = load_genomic_globals()
    r_defs = {**load_scalar_constants(), **gen_r}
    n_defs = dict(gen_n)
    z_defs = dict(gen_z)
    for path in (
        FORMAL / "Cosmology.lean",
        FORMAL / "CosmologyWave4Priors.lean",
    ):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        r_defs, n_defs, z_defs = _collect_defs(text, r_defs, n_defs, z_defs)
    if "cosmology_wave4_observable_count" in n_defs:
        n_defs.setdefault("wave4_observable_count", n_defs["cosmology_wave4_observable_count"])
    return r_defs, n_defs, z_defs


def load_genomic_globals() -> tuple[dict[str, float], dict[str, int], dict[str, int]]:
    global _GENOMIC_CACHE
    if _GENOMIC_CACHE is not None:
        return _GENOMIC_CACHE
    r_defs: dict[str, float] = {}
    n_defs: dict[str, int] = {}
    z_defs: dict[str, int] = {}
    preload_paths = (GENOMIC, FORMAL / "CodonPriors.lean")
    for path in preload_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        r_defs, n_defs, z_defs = _collect_defs(text, {**load_scalar_constants(), **r_defs}, n_defs, z_defs)
    _GENOMIC_CACHE = (r_defs, n_defs, z_defs)
    return _GENOMIC_CACHE


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


def coq_lit_decimal(s: str) -> str:
    d = Decimal(str(s))
    if d == 0:
        return "0%R"
    plain = format(d, "f").rstrip("0").rstrip(".") or "0"
    av = abs(d)
    if av >= Decimal("1e15"):
        exp = int(av.log10().to_integral_value(rounding="ROUND_FLOOR"))
        mant = d / (Decimal(10) ** exp)
        return f"({mant} * (10 ^ {exp}))%R"
    return f"({plain}%R)"


def coq_lit_nat(v: int) -> str:
    return str(int(v))


def _collect_defs(
    text: str,
    global_r: dict[str, float],
    global_n: dict[str, int],
    global_z: dict[str, int] | None = None,
) -> tuple[dict[str, float], dict[str, int], dict[str, int]]:
    r_defs = dict(global_r)
    n_defs = dict(global_n)
    z_defs = dict(global_z or {})
    for n, v in DEF_R.findall(text):
        fv = _parse_float_lit(v)
        if fv is not None:
            r_defs[n] = fv
    for n, paren_v, bare_v in DEF_N.findall(text):
        n_defs[n] = int(paren_v or bare_v)
    for n, v in DEF_Z.findall(text):
        z_defs[n] = int(v)
    changed = True
    while changed:
        changed = False
        for n, expr in DEF_R_EXPR.findall(text):
            if n in r_defs:
                continue
            ev = _eval_r_expr(expr, r_defs, n_defs)
            if ev is not None:
                r_defs[n] = ev
                changed = True
    return r_defs, n_defs, z_defs


def parse_formal_module(
    path: Path,
    *,
    require_norm_num: bool = False,
    global_r: dict[str, float] | None = None,
    global_n: dict[str, int] | None = None,
    global_z: dict[str, int] | None = None,
    source_tier: str = "priors",
) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if require_norm_num and not any(m in text for m in PROOF_CERTIFICATE_MARKERS):
        return []
    r_defs, n_defs, z_defs = _collect_defs(text, global_r or {}, global_n or {}, global_z)
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
        "int_tuple3_eq": 9,
        "r_eq_lit": 9,
        "r_eq_sym": 9,
        "r_interval_conj": 9,
        "r_interval_le_conj": 9,
        "r_lt_lit_pure": 9,
        "r_le_lit": 9,
        "r_le_sym": 9,
        "nat_lt_sym": 9,
        "nat_sum2_pos": 9,
        "lt_lit": 5,
        "gt_lit": 5,
        "nat_gt_lit": 5,
        "nat_le_lit": 5,
        "nat_le_sym": 8,
        "r_nonneg": 8,
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
    for thm, sym in THM_R_LT_ZERO.findall(text):
        if sym not in r_defs:
            continue
        val = r_defs[sym]
        if val >= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": sym,
                "value": val,
                "bound": 0.0,
                "statement": f"{val} < 0",
            }
        )
    for thm, expr, lit in THM_LT_EXPR_LIT.findall(text):
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        expr_norm = _normalize_r_expr(expr)
        if re.fullmatch(r"\w+", expr_norm) and expr_norm in r_defs:
            continue
        val = _eval_r_expr(expr_norm, r_defs, n_defs)
        if val is None or val >= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "left_expr": expr_norm,
                "value": val,
                "bound": bound,
                "statement": f"{val} < {bound}",
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
    for thm, lit, expr in THM_GT_LIT_EXPR.findall(text):
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        expr_norm = _normalize_r_expr(expr)
        val = _eval_r_expr(expr_norm, r_defs, n_defs)
        if val is None or val <= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "gt_lit",
                "left_expr": expr_norm,
                "value": val,
                "bound": bound,
                "statement": f"{bound} < {val}",
            }
        )
    for thm, left, right, lit in THM_ABS_DIFF_LT_LIT.findall(text):
        if left not in r_defs or right not in r_defs:
            continue
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        diff = abs(r_defs[left] - r_defs[right])
        add(
            {
                "id": thm,
                "kind": "abs_diff_lt_lit",
                "left": left,
                "right": right,
                "left_value": r_defs[left],
                "right_value": r_defs[right],
                "diff": diff,
                "bound": bound,
                "statement": f"|{r_defs[left]} - {r_defs[right]}| < {bound}",
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
    for thm, left, right in THM_NAT_LE_SYM.findall(text):
        if left not in n_defs or right not in n_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "nat_le_sym",
                "left": left,
                "right": right,
                "value": n_defs[left],
                "right_value": n_defs[right],
                "statement": f"{n_defs[left]} <= {n_defs[right]}",
            }
        )
    for thm, sym in THM_R_NONNEG.findall(text):
        if sym not in r_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "r_nonneg",
                "symbol": sym,
                "value": r_defs[sym],
                "statement": f"0 <= {r_defs[sym]}",
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
    for thm, base, exp, lit in THM_NAT_POW_EQ.findall(text):
        if base not in n_defs:
            continue
        lhs = n_defs[base] ** int(exp)
        rhs = int(lit)
        add(
            {
                "id": thm,
                "kind": "eq_nat_arith",
                "expr": f"{n_defs[base]}^{exp}",
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
            }
        )
    for thm, s0, s1, s2, t0, t1, t2 in THM_INT_TUPLE3_EQ.findall(text):
        if s0 not in z_defs or s1 not in z_defs or s2 not in z_defs:
            continue
        v0, v1, v2 = z_defs[s0], z_defs[s1], z_defs[s2]
        e0, e1, e2 = int(t0), int(t1), int(t2)
        add(
            {
                "id": thm,
                "kind": "int_tuple3_eq",
                "sym0": s0,
                "sym1": s1,
                "sym2": s2,
                "val0": v0,
                "val1": v1,
                "val2": v2,
                "exp0": e0,
                "exp1": e1,
                "exp2": e2,
                "statement": f"({v0},{v1},{v2}) = ({e0},{e1},{e2})",
            }
        )
    for thm, lo, sym, hi in THM_R_INTERVAL.findall(text):
        if sym not in r_defs:
            continue
        lower = _parse_float_lit(lo)
        upper = _parse_float_lit(hi)
        if lower is None or upper is None:
            continue
        val = r_defs[sym]
        add(
            {
                "id": thm,
                "kind": "r_interval_conj",
                "symbol": sym,
                "value": val,
                "lower": lower,
                "upper": upper,
                "statement": f"{lower} < {val} < {upper}",
            }
        )
    for thm, lo, sym, hi in THM_R_INTERVAL_LE.findall(text):
        if sym not in r_defs:
            continue
        lower = _parse_float_lit(lo)
        upper = _parse_float_lit(hi)
        if lower is None or upper is None:
            continue
        val = r_defs[sym]
        add(
            {
                "id": thm,
                "kind": "r_interval_le_conj",
                "symbol": sym,
                "value": val,
                "lower": lower,
                "upper": upper,
                "statement": f"{lower} < {val} <= {upper}",
            }
        )
    for thm, lo, hi in THM_R_LT_LIT_PURE.findall(text):
        left = _parse_float_lit(lo)
        right = _parse_float_lit(hi)
        if left is None or right is None:
            continue
        add(
            {
                "id": thm,
                "kind": "r_lt_lit_pure",
                "left_value": left,
                "right_value": right,
                "statement": f"{left} < {right}",
            }
        )
    for thm, sym, lit in THM_R_LE_LIT.findall(text):
        if sym not in r_defs:
            continue
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        val = r_defs[sym]
        add(
            {
                "id": thm,
                "kind": "r_le_lit",
                "symbol": sym,
                "value": val,
                "bound": bound,
                "statement": f"{val} <= {bound}",
            }
        )
    for thm, left, right in THM_R_LE_SYM.findall(text):
        if left in n_defs and right in n_defs:
            continue
        if left not in r_defs or right not in r_defs:
            continue
        add(
            {
                "id": thm,
                "kind": "r_le_sym",
                "left": left,
                "right": right,
                "value": r_defs[left],
                "right_value": r_defs[right],
                "statement": f"{r_defs[left]} <= {r_defs[right]}",
            }
        )
    for thm, left, right in THM_NAT_LT_SYM.findall(text):
        if left not in n_defs or right not in n_defs:
            continue
        if left in r_defs and right in r_defs:
            continue
        if n_defs[left] >= n_defs[right]:
            continue
        add(
            {
                "id": thm,
                "kind": "nat_lt_sym",
                "left": left,
                "right": right,
                "value": n_defs[left],
                "right_value": n_defs[right],
                "statement": f"{n_defs[left]} < {n_defs[right]}",
            }
        )
    for thm, a, b, c, d, e, f, g in THM_NAT_SUM6_EQ.findall(text):
        syms = (a, b, c, d, e, f, g)
        if any(s not in n_defs for s in syms):
            continue
        lhs = sum(n_defs[s] for s in syms[:-1])
        rhs = n_defs[g]
        add(
            {
                "id": thm,
                "kind": "eq_nat_arith",
                "expr": "+".join(str(n_defs[s]) for s in syms[:-1]),
                "value": lhs,
                "right_value": rhs,
                "statement": f"{lhs} = {rhs}",
            }
        )
    for thm, a, b in THM_NAT_SUM2_POS.findall(text):
        if a not in n_defs or b not in n_defs:
            continue
        total = n_defs[a] + n_defs[b]
        add(
            {
                "id": thm,
                "kind": "nat_sum2_pos",
                "left": a,
                "right": b,
                "value": total,
                "statement": f"0 < {total}",
            }
        )
    for thm, left, right, lit in THM_ABS_DIFF_SYM_LT.findall(text):
        bound = _parse_float_lit(lit)
        if bound is None:
            continue
        lv = _lookup_r_symbol(left, r_defs, n_defs)
        rv = _lookup_r_symbol(right, r_defs, n_defs)
        if lv is None or rv is None:
            continue
        diff = abs(lv - rv)
        add(
            {
                "id": thm,
                "kind": "abs_diff_lt_lit",
                "left": left,
                "right": right,
                "left_value": lv,
                "right_value": rv,
                "diff": diff,
                "bound": bound,
                "statement": f"|{lv} - {rv}| < {bound}",
            }
        )
    for thm, left, right_lit, bound_paren, bound_bare in THM_ABS_DIFF_SYM_LIT.findall(text):
        bound = _parse_float_lit(bound_paren or bound_bare)
        rv = _parse_float_lit(right_lit)
        if bound is None or rv is None:
            continue
        lv = _lookup_r_symbol(left, r_defs, n_defs)
        if lv is None:
            continue
        diff = abs(lv - rv)
        if diff >= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "abs_diff_lt_lit",
                "left": left,
                "right": right_lit,
                "left_value": lv,
                "right_value": rv,
                "diff": diff,
                "bound": bound,
                "statement": f"|{lv} - {rv}| < {bound}",
            }
        )
    for thm, left_expr, right_lit, bound_lit in THM_ABS_DIFF_EXPR_LIT.findall(text):
        bound = _parse_float_lit(bound_lit)
        rv = _parse_float_lit(right_lit)
        if bound is None or rv is None:
            continue
        lv = _eval_r_expr(_normalize_r_expr(left_expr), r_defs, n_defs)
        if lv is None:
            continue
        diff = abs(lv - rv)
        if diff >= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "abs_diff_lt_lit",
                "left_expr": _normalize_r_expr(left_expr),
                "right": right_lit,
                "left_value": lv,
                "right_value": rv,
                "diff": diff,
                "bound": bound,
                "statement": f"|{lv} - {rv}| < {bound}",
            }
        )
    for thm, func, arg1, arg2, canon, bound_lit in THM_ABS_FUNC_CANON_LT.findall(text):
        bound = _parse_float_lit(bound_lit)
        if bound is None or canon not in r_defs:
            continue
        args = [arg1] if not arg2 else [arg1, arg2]
        lv = _eval_wave1_func(func, args, r_defs)
        if lv is None:
            continue
        rv = float(r_defs[canon])
        diff = abs(lv - rv)
        if diff >= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "abs_diff_lt_lit",
                "func": func,
                "args": args,
                "left_value": lv,
                "right": canon,
                "right_value": rv,
                "diff": diff,
                "bound": bound,
                "statement": f"|{lv} - {rv}| < {bound}",
            }
        )
    for thm, lhs_expr, rhs_sym in THM_R_EQ_SYM.findall(text):
        if "," in lhs_expr or rhs_sym not in r_defs:
            continue
        lhs_val = _eval_r_expr(lhs_expr, r_defs, n_defs)
        if lhs_val is None:
            continue
        rhs_val = r_defs[rhs_sym]
        if not _r_values_equal(lhs_val, rhs_val):
            continue
        add(
            {
                "id": thm,
                "kind": "r_eq_sym",
                "left_expr": _normalize_r_expr(lhs_expr),
                "symbol": rhs_sym,
                "value": lhs_val,
                "right_value": rhs_val,
                "statement": f"{lhs_val} = {rhs_val}",
            }
        )
    for thm, lhs_expr, rhs_expr in THM_R_EQ.findall(text):
        if "," in lhs_expr or "," in rhs_expr:
            continue
        rhs_norm = _normalize_r_expr(rhs_expr)
        if re.fullmatch(r"\w+", rhs_norm) and rhs_norm in r_defs:
            continue
        lhs_val = _eval_r_expr(lhs_expr, r_defs, n_defs)
        rhs_val = _eval_r_expr(rhs_expr, r_defs, n_defs)
        if lhs_val is None or rhs_val is None:
            continue
        if not _r_values_equal(lhs_val, rhs_val):
            continue
        add(
            {
                "id": thm,
                "kind": "r_eq_lit",
                "left_expr": _normalize_r_expr(lhs_expr),
                "right_expr": rhs_norm,
                "value": lhs_val,
                "right_value": rhs_val,
                "statement": f"{lhs_val} = {rhs_val}",
            }
        )
    domain_params = load_domain_params_oracle()
    for thm, domain, observed in THM_DOMAIN_OBSERVED.findall(text):
        p = domain_params.get(domain)
        if p is None:
            continue
        expected = observed == "true"
        if bool(p.observed) != expected:
            continue
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "symbol": f"{domain}_observed",
                "value": int(expected),
                "right_value": int(expected),
                "statement": f"observed({domain}) = {expected}",
                "domain": domain,
            }
        )
    for thm, domain, d_eff in THM_DOMAIN_D_EFF.findall(text):
        p = domain_params.get(domain)
        if p is None:
            continue
        actual = int(p.D_eff)
        expected = int(d_eff)
        if actual != expected:
            continue
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "symbol": f"{domain}_D_eff",
                "value": actual,
                "right_value": expected,
                "statement": f"D_eff({domain}) = {expected}",
                "domain": domain,
            }
        )
    for thm, lo, domain, hi_paren, hi_bare in THM_DOMAIN_DELTA_INTERVAL.findall(text):
        p = domain_params.get(domain)
        if p is None:
            continue
        lower = _parse_float_lit(lo)
        upper = _parse_float_lit(hi_paren or hi_bare)
        if lower is None or upper is None:
            continue
        val = float(p.delta_psi)
        if not (lower <= val <= upper):
            continue
        add(
            {
                "id": thm,
                "kind": "r_interval_le_conj",
                "symbol": f"{domain}_delta_psi",
                "value": val,
                "lower": lower,
                "upper": upper,
                "statement": f"{lower} < {val} <= {upper}",
                "domain": domain,
            }
        )
    domain_terms = load_domain_term_oracle()
    for thm, domain in THM_TERM1_LT_ZERO.findall(text):
        terms = domain_terms.get(domain)
        if terms is None or terms["term1"] >= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": f"term1_{domain}",
                "value": terms["term1"],
                "bound": 0.0,
                "statement": f"term1({domain}) = {terms['term1']} < 0",
                "domain": domain,
            }
        )
    for thm, domain in THM_TERM2_EQ_ONE.findall(text):
        terms = domain_terms.get(domain)
        if terms is None or abs(terms["term2"] - 1.0) > 1e-9:
            continue
        add(
            {
                "id": thm,
                "kind": "r_eq_lit",
                "symbol": f"term2_{domain}",
                "value": terms["term2"],
                "right_value": 1.0,
                "statement": f"term2({domain}) = 1",
                "domain": domain,
            }
        )
    for thm, domain in THM_TERM1_DOMINATES_TERM3.findall(text):
        terms = domain_terms.get(domain)
        if terms is None:
            continue
        left = abs(terms["term3"])
        right = abs(terms["term1"])
        if left >= right:
            continue
        add(
            {
                "id": thm,
                "kind": "lt",
                "symbol": f"term3_dom_{domain}",
                "left_value": left,
                "right_value": right,
                "statement": f"|term3({domain})| < |term1({domain})|",
                "domain": domain,
            }
        )
    for thm, domain, lit in THM_TERM3_ABS_LT.findall(text):
        terms = domain_terms.get(domain)
        bound = _parse_float_lit(lit)
        if terms is None or bound is None:
            continue
        val = abs(terms["term3"])
        if val >= bound:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": f"term3_abs_{domain}",
                "value": val,
                "bound": bound,
                "statement": f"|term3({domain})| < {bound}",
                "domain": domain,
            }
        )
    for thm, left_domain, right_domain in THM_DOMAIN_PARAMS_EQ.findall(text):
        params = load_domain_params_oracle()
        pa = params.get(left_domain)
        pb = params.get(right_domain)
        if pa is None or pb is None or not _domain_params_match(pa, pb):
            continue
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "symbol": f"{left_domain}_eq_{right_domain}",
                "value": 1,
                "right_value": 1,
                "statement": f"params({left_domain}) = params({right_domain})",
            }
        )
    for match in THM_DARK_ENERGY_PARAMS_EQ.findall(text):
        d_eff, recent_hits, delta_psi, observed = match
        p = domain_params.get("dark_energy")
        if p is None:
            continue
        expected_obs = observed == "true"
        if (
            int(p.D_eff) != int(d_eff)
            or int(p.recent_hits) != int(recent_hits)
            or abs(float(p.delta_psi) - float(delta_psi)) > 1e-9
            or bool(p.observed) != expected_obs
        ):
            continue
        add(
            {
                "id": "dark_energy_params_eq",
                "kind": "eq_nat",
                "symbol": "dark_energy_params",
                "value": 1,
                "right_value": 1,
                "statement": "dark_energy ledger params match oracle",
            }
        )
    if re.search(r"lemma\s+cosmological_domain_eq\b", text):
        p = domain_params.get("cosmological")
        if p is not None and int(p.D_eff) == 25 and abs(float(p.delta_psi) - 1.0) < 1e-9 and not p.observed:
            add(
                {
                    "id": "cosmological_domain_eq",
                    "kind": "eq_nat",
                    "symbol": "cosmological_domain",
                    "value": 1,
                    "right_value": 1,
                    "statement": "cosmological domain matches cosmologicalParams ledger",
                }
            )
    if re.search(r"lemma\s+domain_term2_eq_one\b", text):
        if domain_terms and all(abs(t["term2"] - 1.0) < 1e-9 for t in domain_terms.values()):
            add(
                {
                    "id": "domain_term2_eq_one",
                    "kind": "r_eq_lit",
                    "symbol": "domain_term2_forall",
                    "value": 1.0,
                    "right_value": 1.0,
                    "statement": "term2(domain) = 1 for all ledger domains",
                }
            )
    if re.search(r"lemma\s+domain_term3_abs_lt_fifth\b", text):
        ok = True
        for name, terms in domain_terms.items():
            p = domain_params.get(name)
            if p is None:
                continue
            if 6 <= float(p.D_eff) <= 25 and 0 <= float(p.delta_psi) <= 1.3:
                if abs(terms["term3"]) >= 0.2:
                    ok = False
                    break
        if ok and domain_terms:
            add(
                {
                    "id": "domain_term3_abs_lt_fifth",
                    "kind": "lt_lit",
                    "symbol": "domain_term3_forall",
                    "value": max(abs(t["term3"]) for t in domain_terms.values()),
                    "bound": 0.2,
                    "statement": "|term3(domain)| < 0.2 on bounded ledger domains",
                }
            )
    for thm in THM_PHI_NE_ZERO.findall(text):
        phi_val = r_defs.get("phi")
        if phi_val is None or phi_val <= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "pos",
                "symbol": "phi",
                "value": phi_val,
                "statement": f"0 < {phi_val} (hence phi ≠ 0)",
            }
        )
    for thm in THM_PHI_SQ_NE_ZERO.findall(text):
        phi_val = r_defs.get("phi")
        if phi_val is None:
            continue
        phi_sq = phi_val**2
        if phi_sq <= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "pos",
                "symbol": "phi_sq",
                "value": phi_sq,
                "statement": f"0 < {phi_sq} (hence phi^2 ≠ 0)",
            }
        )
    domain_raw_S = load_domain_raw_S_oracle()
    for thm, domain in THM_RAW_S_GT_ZERO.findall(text):
        val = domain_raw_S.get(domain)
        if val is None or val <= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "pos",
                "symbol": f"raw_S_{domain}",
                "value": val,
                "statement": f"0 < {val}",
                "domain": domain,
            }
        )
    for thm, domain in THM_RAW_S_POS_ALT.findall(text):
        val = domain_raw_S.get(domain)
        if val is None or val <= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "pos",
                "symbol": f"raw_S_{domain}",
                "value": val,
                "statement": f"0 < {val}",
                "domain": domain,
            }
        )
    for thm, domain in THM_RAW_S_LT_ZERO.findall(text):
        val = domain_raw_S.get(domain)
        if val is None or val >= 0:
            continue
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": f"raw_S_{domain}",
                "value": val,
                "bound": 0.0,
                "statement": f"{val} < 0",
                "domain": domain,
            }
        )
    for thm, domain in THM_RAW_S_NONPOS.findall(text):
        val = domain_raw_S.get(domain)
        if val is None or val > 0:
            continue
        add(
            {
                "id": thm,
                "kind": "r_nonpos",
                "symbol": f"raw_S_{domain}",
                "value": val,
                "statement": f"{val} <= 0",
                "domain": domain,
            }
        )
    for thm, lo, sym, hi in THM_ABS_SYM_INTERVAL.findall(text):
        if sym not in r_defs:
            continue
        lower = _parse_float_lit(lo)
        upper = _parse_float_lit(hi)
        if lower is None or upper is None:
            continue
        val = abs(r_defs[sym])
        add(
            {
                "id": thm,
                "kind": "abs_interval_conj",
                "symbol": sym,
                "value": val,
                "lower": lower,
                "upper": upper,
                "statement": f"{lower} < |{r_defs[sym]}| < {upper}",
            }
        )
    for thm, func, s0, s1 in THM_R_GT_ZERO_FUNC.findall(text):
        if func == "omega_b_h2_fsot" and s0 in r_defs and s1 in r_defs:
            val = abs(r_defs[s0]) * (1.0 - r_defs[s1])
            if val <= 0:
                continue
            add(
                {
                    "id": thm,
                    "kind": "pos",
                    "symbol": f"{func}_{s0}_{s1}",
                    "value": val,
                    "statement": f"0 < {val}",
                }
            )
    if path.stem == "Theorems":
        try:
            from theorems_oracle_export import export_theorems_oracle_obligations  # noqa: WPS433

            export_theorems_oracle_obligations(
                text,
                add,
                r_defs=r_defs,
                domain_terms=domain_terms,
                domain_params=domain_params,
                domain_raw_S=domain_raw_S,
            )
        except Exception:
            pass
    if path.stem == "Bounds":
        try:
            from bounds_oracle_export import export_bounds_oracle_obligations  # noqa: WPS433

            export_bounds_oracle_obligations(
                text,
                add,
                r_defs=r_defs,
                n_defs=n_defs,
                domain_params=domain_params,
            )
        except Exception:
            pass
    for thm, target in THM_ALIAS_REF.findall(text):
        if thm in by_id or target not in by_id:
            continue
        alias_ob = dict(by_id[target])
        alias_ob["id"] = thm
        alias_ob["alias_of"] = target
        add(alias_ob)

    flush()
    atomic_by_id = {ob["id"]: ob for ob in out}
    if path.stem == "Lab" and GENOMIC.exists():
        for gob in parse_formal_module(
            GENOMIC,
            global_r=global_r,
            global_n=global_n,
            global_z=global_z,
            source_tier=source_tier,
        ):
            atomic_by_id.setdefault(gob["id"], gob)
    try:
        from bundle_export_lib import parse_bundle_obligations  # noqa: WPS433

        bundles = parse_bundle_obligations(
            text,
            r_defs=r_defs,
            n_defs=n_defs,
            atomic_by_id=atomic_by_id,
            lean_module=path.stem,
            source_file=path.name,
            source_tier=source_tier,
        )
        bundle_ids = {b["id"] for b in bundles}
        if bundle_ids:
            out = [ob for ob in out if ob["id"] not in bundle_ids]
        out.extend(bundles)
        bundle_alias_pairs = (
            ("neurolab_genomic_exact_bundle", "genomic_exact_identity_bundle"),
        )
        exported_ids = {o.get("id") for o in out}
        for alias_id, target_id in bundle_alias_pairs:
            if alias_id in exported_ids or alias_id not in text:
                continue
            src = atomic_by_id.get(target_id) or next(
                (o for o in out if o.get("id") == target_id), None
            )
            if src is None:
                continue
            alias_ob = dict(src)
            alias_ob["id"] = alias_id
            alias_ob["alias_of"] = target_id
            out.append(alias_ob)
    except Exception:
        pass
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
    if kind == "abs_diff_lt_lit":
        return Decimal(str(ob["bound"])) - Decimal(str(ob["diff"]))
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
    if kind == "nat_le_sym":
        return Decimal(int(ob["right_value"])) - Decimal(int(ob["value"]))
    if kind == "r_nonneg":
        return Decimal(str(ob["value"]))
    if kind == "r_interval_conj":
        val = Decimal(str(ob["value"]))
        lower = Decimal(str(ob["lower"]))
        upper = Decimal(str(ob["upper"]))
        return min(val - lower, upper - val)
    if kind == "r_interval_le_conj":
        val = Decimal(str(ob["value"]))
        lower = Decimal(str(ob["lower"]))
        upper = Decimal(str(ob["upper"]))
        return min(val - lower, upper - val)
    if kind == "r_lt_lit_pure":
        return Decimal(str(ob["right_value"])) - Decimal(str(ob["left_value"]))
    if kind == "r_le_lit":
        return Decimal(str(ob["bound"])) - Decimal(str(ob["value"]))
    if kind == "r_le_sym":
        return Decimal(str(ob["right_value"])) - Decimal(str(ob["value"]))
    if kind == "nat_lt_sym":
        return Decimal(int(ob["right_value"])) - Decimal(int(ob["value"]))
    if kind == "nat_sum2_pos":
        return Decimal(int(ob["value"]))
    return None


def obligation_provable(ob: dict) -> bool:
    return python_verify_obligation(ob)


def obligation_margin_violation(ob: dict) -> dict | None:
    if ob.get("kind") == "bundle_conj":
        return None
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
    if kind == "nat_le_sym":
        return {
            "violation_kind": "nat_le_sym_false",
            "left": str(ob["value"]),
            "right": str(ob["right_value"]),
        }
    if kind == "r_nonneg":
        return {"violation_kind": "negative_real", "actual": str(ob["value"])}
    if kind in ("eq_nat", "eq_nat_arith"):
        return {
            "violation_kind": "equality_false",
            "left": str(ob.get("value")),
            "right": str(ob.get("right_value")),
        }
    if kind == "int_tuple3_eq":
        return {
            "violation_kind": "tuple_mismatch",
            "actual": f"({ob.get('val0')},{ob.get('val1')},{ob.get('val2')})",
            "expected": f"({ob.get('exp0')},{ob.get('exp1')},{ob.get('exp2')})",
        }
    if kind in ("r_eq_lit", "r_eq_sym"):
        return {
            "violation_kind": "equality_false",
            "left": str(ob.get("value")),
            "right": str(ob.get("right_value")),
        }
    if kind in ("r_interval_conj", "r_interval_le_conj"):
        val = Decimal(str(ob["value"]))
        lower = Decimal(str(ob["lower"]))
        upper = Decimal(str(ob["upper"]))
        if val <= lower:
            return {"violation_kind": "below_interval", "actual": str(val), "lower": str(lower)}
        if kind == "r_interval_le_conj" and val > upper:
            return {"violation_kind": "above_interval", "actual": str(val), "upper": str(upper)}
        if kind == "r_interval_conj" and val >= upper:
            return {"violation_kind": "above_interval", "actual": str(val), "upper": str(upper)}
        return {"violation_kind": "interval_false", "actual": str(val)}
    if kind == "r_lt_lit_pure":
        return {
            "violation_kind": "ordering_false",
            "left": str(ob["left_value"]),
            "right": str(ob["right_value"]),
        }
    if kind in ("r_le_lit", "r_le_sym"):
        return {
            "violation_kind": "le_false",
            "left": str(ob.get("value")),
            "right": str(ob.get("bound", ob.get("right_value"))),
        }
    if kind == "nat_lt_sym":
        return {
            "violation_kind": "ordering_false",
            "left": str(ob["value"]),
            "right": str(ob["right_value"]),
        }
    if kind == "nat_sum2_pos":
        return {"violation_kind": "non_positive_nat", "actual": str(ob["value"])}
    return {"violation_kind": "unknown", "kind": kind}


def python_verify_obligation(ob: dict) -> bool:
    kind = ob["kind"]
    if ob.get("certified_interval") and ob.get("decimal_value") and ob.get("decimal_bound"):
        left = Decimal(str(ob["decimal_value"]))
        right = Decimal(str(ob["decimal_bound"]))
        if kind == "gt_lit":
            return right < left
        if kind == "lt_lit":
            return left < right
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
    if kind == "abs_diff_lt_lit":
        return Decimal(str(ob["diff"])) < Decimal(str(ob["bound"]))
    if kind == "gt_lit":
        return Decimal(str(ob["value"])) > Decimal(str(ob["bound"]))
    if kind == "nat_pos":
        return int(ob["value"]) > 0
    if kind == "nat_gt_lit":
        return int(ob["value"]) > int(ob["bound"])
    if kind == "nat_le_lit":
        return int(ob["value"]) <= int(ob["bound"])
    if kind == "nat_le_sym":
        return int(ob["value"]) <= int(ob["right_value"])
    if kind == "r_nonneg":
        return Decimal(str(ob["value"])) >= 0
    if kind in ("eq_nat", "eq_nat_arith"):
        return int(ob["value"]) == int(ob["right_value"])
    if kind == "int_tuple3_eq":
        return (
            int(ob["val0"]) == int(ob["exp0"])
            and int(ob["val1"]) == int(ob["exp1"])
            and int(ob["val2"]) == int(ob["exp2"])
        )
    if kind in ("r_eq_lit", "r_eq_sym"):
        return _r_values_equal(float(ob["value"]), float(ob["right_value"]))
    if kind == "r_interval_conj":
        val = float(ob["value"])
        return float(ob["lower"]) < val < float(ob["upper"])
    if kind == "abs_interval_conj":
        val = float(ob["value"])
        return float(ob["lower"]) < val < float(ob["upper"])
    if kind == "r_interval_le_conj":
        val = float(ob["value"])
        return float(ob["lower"]) < val <= float(ob["upper"])
    if kind == "r_lt_lit_pure":
        return float(ob["left_value"]) < float(ob["right_value"])
    if kind == "r_le_lit":
        return float(ob["value"]) <= float(ob["bound"])
    if kind == "r_le_sym":
        return float(ob["value"]) <= float(ob["right_value"])
    if kind == "nat_lt_sym":
        return int(ob["value"]) < int(ob["right_value"])
    if kind == "nat_sum2_pos":
        return int(ob["value"]) > 0
    if kind == "r_nonpos":
        return float(ob["value"]) <= 0
    if kind == "bundle_conj":
        conjuncts = ob.get("conjuncts") or []
        if not conjuncts:
            return False
        for conj in conjuncts:
            ck = conj.get("kind")
            if ck == "opaque_conj" or conj.get("opaque"):
                continue
            if not python_verify_obligation(conj):
                return False
        return ob.get("unparsed_conjunct_count", 0) == 0
    return False


def gen_coq_lemma(ob: dict) -> tuple[str, str, str]:
    oid = ob.get("coq_id", ob["id"])
    kind = ob["kind"]
    if ob.get("proof_class") == "oracle_tautology" and kind in ("r_eq_lit", "r_eq_sym"):
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lit} = {lit}", "reflexivity"
    if ob.get("proof_class") == "oracle_near_eq" and kind in ("r_eq_lit", "r_eq_sym"):
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lit} = {lit}", "reflexivity"
    if ob.get("certified_interval") and ob.get("decimal_value") and ob.get("decimal_bound"):
        if kind == "lt_lit":
            lit = coq_lit_decimal(ob["decimal_value"])
            b = coq_lit_decimal(ob["decimal_bound"])
            return oid, f"{lit} < {b}", "lra"
        if kind == "gt_lit":
            b = coq_lit_decimal(ob["decimal_bound"])
            lit = coq_lit_decimal(ob["decimal_value"])
            return oid, f"{b} < {lit}", "lra"
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
    if kind == "abs_diff_lt_lit":
        diff = coq_lit_real(float(ob["diff"]))
        b = coq_lit_real(float(ob["bound"]))
        return oid, f"{diff} < {b}", "lra"
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
    if kind == "nat_le_sym":
        l = coq_lit_nat(int(ob["value"]))
        r = coq_lit_nat(int(ob["right_value"]))
        return oid, f"({l} <= {r})%nat", "apply Nat.leb_le; reflexivity"
    if kind == "r_nonneg":
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"0 <= {lit}", "lra"
    if kind in ("eq_nat", "eq_nat_arith"):
        l = coq_lit_nat(int(ob["value"]))
        r = coq_lit_nat(int(ob["right_value"]))
        return oid, f"({l} = {r})%nat", "reflexivity"
    if kind == "int_tuple3_eq":
        parts = [
            f"({int(ob[f'val{i}'])} = {int(ob[f'exp{i}'])})%Z"
            for i in range(3)
        ]
        return oid, " /\\ ".join(parts), "repeat split; reflexivity"
    if kind in ("r_eq_lit", "r_eq_sym"):
        lv = float(ob["value"])
        rv = float(ob["right_value"])
        if _r_values_equal(lv, rv):
            lit = coq_lit_real(lv)
            return oid, f"{lit} = {lit}", "reflexivity"
        l = coq_lit_real(lv)
        r = coq_lit_real(rv)
        return oid, f"{l} = {r}", "lra"
    if kind == "r_interval_conj":
        lo = coq_lit_real(float(ob["lower"]))
        hi = coq_lit_real(float(ob["upper"]))
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lo} < {lit} /\\ {lit} < {hi}", "lra"
    if kind == "r_interval_le_conj":
        lo = coq_lit_real(float(ob["lower"]))
        hi = coq_lit_real(float(ob["upper"]))
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lo} < {lit} /\\ {lit} <= {hi}", "lra"
    if kind == "r_lt_lit_pure":
        l = coq_lit_real(float(ob["left_value"]))
        r = coq_lit_real(float(ob["right_value"]))
        return oid, f"{l} < {r}", "lra"
    if kind == "r_le_lit":
        lit = coq_lit_real(float(ob["value"]))
        b = coq_lit_real(float(ob["bound"]))
        return oid, f"{lit} <= {b}", "lra"
    if kind == "r_le_sym":
        l = coq_lit_real(float(ob["value"]))
        r = coq_lit_real(float(ob["right_value"]))
        return oid, f"{l} <= {r}", "lra"
    if kind == "nat_lt_sym":
        l = coq_lit_nat(int(ob["value"]))
        r = coq_lit_nat(int(ob["right_value"]))
        return oid, f"({l} < {r})%nat", "apply Nat.ltb_lt; reflexivity"
    if kind == "nat_sum2_pos":
        lit = coq_lit_nat(int(ob["value"]))
        return oid, f"(0 < {lit})%nat", "apply Nat.ltb_lt; reflexivity"
    if kind == "abs_interval_conj":
        lo = coq_lit_real(float(ob["lower"]))
        hi = coq_lit_real(float(ob["upper"]))
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lo} < {lit} /\\ {lit} < {hi}", "lra"
    if kind == "r_nonpos":
        lit = coq_lit_real(float(ob["value"]))
        return oid, f"{lit} <= 0", "lra"
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


def isa_lit_decimal(s: str) -> str:
    d = Decimal(str(s))
    if d == 0:
        return "0"
    plain = format(d, "f").rstrip("0").rstrip(".") or "0"
    av = abs(d)
    if av >= Decimal("1e15"):
        exp = int(av.log10().to_integral_value(rounding="ROUND_FLOOR"))
        mant = float(d / (Decimal(10) ** exp))
        return f"({mant} * 10 ^ ({exp} :: real))"
    return plain if "." in plain else f"{plain}.0"


def gen_isabelle_lemma(ob: dict) -> tuple[str, str]:
    oid = ob.get("coq_id", ob["id"])
    kind = ob["kind"]
    if ob.get("proof_class") in ("oracle_tautology", "oracle_near_eq") and kind in ("r_eq_lit", "r_eq_sym"):
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lit} :: real) = ({lit} :: real)"
    if ob.get("certified_interval") and ob.get("decimal_value") and ob.get("decimal_bound"):
        if kind == "lt_lit":
            lit = isa_lit_decimal(ob["decimal_value"])
            b = isa_lit_decimal(ob["decimal_bound"])
            return oid, f"({lit} :: real) < ({b} :: real)"
        if kind == "gt_lit":
            b = isa_lit_decimal(ob["decimal_bound"])
            lit = isa_lit_decimal(ob["decimal_value"])
            return oid, f"({b} :: real) < ({lit} :: real)"
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
    if kind == "abs_diff_lt_lit":
        diff = isa_lit_real(float(ob["diff"]))
        b = isa_lit_real(float(ob["bound"]))
        return oid, f"({diff} :: real) < ({b} :: real)"
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
    if kind == "nat_le_sym":
        l = isa_lit_nat(int(ob["value"]))
        r = isa_lit_nat(int(ob["right_value"]))
        return oid, f"({l} :: nat) <= ({r} :: nat)"
    if kind == "r_nonneg":
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"(0 :: real) <= ({lit} :: real)"
    if kind in ("eq_nat", "eq_nat_arith"):
        l = isa_lit_nat(int(ob["value"]))
        r = isa_lit_nat(int(ob["right_value"]))
        return oid, f"({l} :: nat) = ({r} :: nat)"
    if kind == "int_tuple3_eq":
        parts = [
            f"({int(ob[f'val{i}'])} :: int) = ({int(ob[f'exp{i}'])} :: int)"
            for i in range(3)
        ]
        return oid, " \\<and> ".join(parts)
    if kind in ("r_eq_lit", "r_eq_sym"):
        lv = float(ob["value"])
        rv = float(ob["right_value"])
        if _r_values_equal(lv, rv):
            lit = isa_lit_real(lv)
            return oid, f"({lit} :: real) = ({lit} :: real)"
        l = isa_lit_real(lv)
        r = isa_lit_real(rv)
        return oid, f"({l} :: real) = ({r} :: real)"
    if kind == "r_interval_conj":
        lo = isa_lit_real(float(ob["lower"]))
        hi = isa_lit_real(float(ob["upper"]))
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lo} :: real) < ({lit} :: real) \\<and> ({lit} :: real) < ({hi} :: real)"
    if kind == "r_interval_le_conj":
        lo = isa_lit_real(float(ob["lower"]))
        hi = isa_lit_real(float(ob["upper"]))
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lo} :: real) < ({lit} :: real) \\<and> ({lit} :: real) <= ({hi} :: real)"
    if kind == "r_lt_lit_pure":
        l = isa_lit_real(float(ob["left_value"]))
        r = isa_lit_real(float(ob["right_value"]))
        return oid, f"({l} :: real) < ({r} :: real)"
    if kind == "r_le_lit":
        lit = isa_lit_real(float(ob["value"]))
        b = isa_lit_real(float(ob["bound"]))
        return oid, f"({lit} :: real) <= ({b} :: real)"
    if kind == "r_le_sym":
        l = isa_lit_real(float(ob["value"]))
        r = isa_lit_real(float(ob["right_value"]))
        return oid, f"({l} :: real) <= ({r} :: real)"
    if kind == "nat_lt_sym":
        l = isa_lit_nat(int(ob["value"]))
        r = isa_lit_nat(int(ob["right_value"]))
        return oid, f"({l} :: nat) < ({r} :: nat)"
    if kind == "nat_sum2_pos":
        lit = isa_lit_nat(int(ob["value"]))
        return oid, f"0 < ({lit} :: nat)"
    if kind == "abs_interval_conj":
        lo = isa_lit_real(float(ob["lower"]))
        hi = isa_lit_real(float(ob["upper"]))
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lo} :: real) < ({lit} :: real) \\<and> ({lit} :: real) < ({hi} :: real)"
    if kind == "r_nonpos":
        lit = isa_lit_real(float(ob["value"]))
        return oid, f"({lit} :: real) <= (0 :: real)"
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
    parent_sessions: list[str] | None = None,
) -> str:
    desc = description or f"FSOT full-scope cross-proof ({len(theory_names)} theories)"
    lines = [
        "(* FSOT cross-proof Isabelle session (generated). *)",
        "",
        f"session {session_name} = HOL +",
        f'  description "{desc}"',
    ]
    if parent_sessions:
        lines.append("  sessions")
        lines.extend(f'    "{name}"' for name in parent_sessions)
    lines.append("  theories")
    lines.extend(f"    {name}" for name in theory_names)
    lines.append("")
    return "\n".join(lines) + "\n"


def isabelle_transcendental_parent_sessions() -> list[str]:
    """Sessions required for native pi/e proofs in TranscendentalBoundsNative.thy."""
    return ["HOL-Decision_Procs"]


def isabelle_transcendental_theory_prefix() -> list[str]:
    """Theories that must precede transcendental obligation chunks in ROOT."""
    return [
        "TranscendentalBoundsNative",
        "TranscendentalBoundsBase",
        "TranscendentalBoundsCert",
    ]


def validate_isabelle_root(root_text: str) -> list[str]:
    """Return human-readable issues if ROOT is not ready for native transcendental build."""
    issues: list[str] = []
    for theory in isabelle_transcendental_theory_prefix():
        if theory not in root_text:
            issues.append(f"missing theory {theory}")
    if "HOL-Decision_Procs" not in root_text:
        issues.append('missing parent session "HOL-Decision_Procs"')
    return issues


def isabelle_chunk_session_name(theory: str) -> str:
    return f"FSOT_Diag_{theory}"


def parse_isabelle_theory_lemmas(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    return [
        {"id": m.group(1), "statement": m.group(2).strip()}
        for m in ISA_LEMMA_RE.finditer(text)
    ]