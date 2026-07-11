"""Portable math-formula evaluation aligned with fsot-read-write fsot-core."""

from __future__ import annotations

import csv
import json
import math
import re
import subprocess
from collections.abc import Mapping
from pathlib import Path


def core_context() -> dict[str, float]:
    """Mirror fsot-core model::core_context()."""
    pi = math.pi
    e = math.e
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    gamma = 0.5772156649015329
    g_cat = 0.915965594177219

    alpha = math.log(pi) / (e * phi**13)
    psi_con = 1.0 - math.exp(-1.0)
    eta_eff = 1.0 / (pi - 1.0)
    beta = 1.0 / math.exp(pi**pi + (e - 1.0))
    gamma_c = -(math.log(2.0)) / phi
    omega = math.sin(pi / e) * math.sqrt(2.0)
    theta_s = math.sin(psi_con * eta_eff)
    poof = math.exp((-(math.log(pi)) / e) / (eta_eff * math.log(phi)))

    c_eff = (1.0 - poof * math.sin(theta_s)) * (1.0 + 0.01 * g_cat / (pi * phi))
    a_bleed = math.sin(pi / e) * phi / math.sqrt(2.0)
    p_var = -math.cos(theta_s + pi)
    b_in = c_eff * (1.0 - math.sin(theta_s) / phi)
    a_in = a_bleed * (1.0 + math.cos(theta_s) / phi)
    suction = poof * (-math.cos(theta_s - pi))
    chaos = gamma_c / omega
    p_base = gamma / e
    p_new = p_base * math.sqrt(2.0)
    c_factor = c_eff * p_new
    k = phi * (gamma / e) * math.sqrt(2.0) / math.log(pi) * 0.99
    c_cosm = 1.0 / (phi * 10.0)
    gate = phi / (1.0 + phi)

    values = {
        "pi": pi,
        "e": e,
        "phi": phi,
        "gamma": gamma,
        "g_cat": g_cat,
        "alpha": alpha,
        "psi_con": psi_con,
        "eta_eff": eta_eff,
        "beta": beta,
        "gamma_c": gamma_c,
        "omega": omega,
        "theta_s": theta_s,
        "poof": poof,
        "c_eff": c_eff,
        "a_bleed": a_bleed,
        "p_var": p_var,
        "b_in": b_in,
        "a_in": a_in,
        "suction": suction,
        "chaos": chaos,
        "p_base": p_base,
        "p_new": p_new,
        "c_factor": c_factor,
        "k": k,
        "c_cosm": c_cosm,
        "g": g_cat,
        "pnew": p_new,
        "pbase": p_base,
        "p_base": p_base,
        "p_new": p_new,
        "c_eff": c_eff,
        "thetas": theta_s,
        "theta_s": theta_s,
        "psicon": psi_con,
        "psi_con": psi_con,
        "ceff": c_eff,
        "ableed": a_bleed,
        "ain": a_in,
        "mathcal_c": c_cosm,
        "eta_eff": eta_eff,
        "theta": theta_s,
        "thetas": theta_s,
        "psi": psi_con,
        "eta": eta_eff,
        "omega": omega,
        "a_bleed": a_bleed,
        "a_in": a_in,
        "b_in": b_in,
        "p_new": p_new,
        "p_var": p_var,
        "suction": suction,
        "chaos": chaos,
        "c_factor": c_factor,
        "c_cosm": c_cosm,
        "g_cat": g_cat,
        "catalan": g_cat,
        "c": g_cat,
        "big_g": g_cat,
        "gate": gate,
        "omega": omega,
        "gamma": gamma,
        "pnew": p_new,
        "pbase": p_base,
        "b_in": b_in,
        "poof": poof,
    }
    return values


_GREEK_TO_LATIN = {
    "Ω": "omega",
    "Ψ": "psi",
    "Θ": "theta",
    "Η": "eta",
    "Γ": "gamma",
    "Φ": "phi",
    "Π": "pi",
    "Α": "alpha",
    "α": "alpha",
    "β": "beta",
    "ω": "omega",
    "ψ": "psi",
    "θ": "theta",
    "η": "eta",
    "γ": "gamma",
    "φ": "phi",
    "π": "pi",
}


def normalize_formula(text: str) -> str:
    out = text
    for src, dst in _GREEK_TO_LATIN.items():
        out = out.replace(src, dst)
    out = (
        out.replace("**", "^")
        .replace("·", "*")
        .replace("•", "*")
        .replace("×", "*")
        .replace("−", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("⁄", "/")
        .replace("→", "->")
        .lower()
    )
    out = re.sub(r"\(\s*rad\s*->\s*°\s*\)", " * 180 / pi ", out)
    out = re.sub(r"\(\s*rad\s*->\s*deg\s*\)", " * 180 / pi ", out)
    out = re.sub(r"√\s*([a-z0-9_()]+)", r"sqrt(\1)", out)
    out = re.sub(r"\s+", "", out)
    out = re.sub(r"\btheta_s\b", "theta_s", out)
    out = re.sub(r"\btheta\b(?!_)", "theta_s", out)
    out = re.sub(r"\bg\b(?![_a-z])", "g_cat", out)
    out = re.sub(r"\bc\b(?![_a-z])", "g_cat", out)
    return out


class _FormulaParser:
    def __init__(self, tokens: list[str], env: Mapping[str, float]) -> None:
        self.tokens = tokens
        self.index = 0
        self.env = env

    def parse(self) -> float:
        value = self._parse_expr()
        if self.index < len(self.tokens):
            raise ValueError(f"unexpected trailing tokens: {self.tokens[self.index:]}")
        return value

    def _peek(self) -> str | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def _consume(self, expected: str | None = None) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("unexpected end of formula")
        if expected is not None and token != expected:
            raise ValueError(f"expected {expected}, got {token}")
        self.index += 1
        return token

    def _parse_expr(self) -> float:
        value = self._parse_term()
        while True:
            token = self._peek()
            if token == "+":
                self._consume("+")
                value += self._parse_term()
            elif token == "-":
                self._consume("-")
                value -= self._parse_term()
            else:
                break
        return value

    def _parse_term(self) -> float:
        value = self._parse_power()
        while True:
            token = self._peek()
            if token == "*":
                self._consume("*")
                value *= self._parse_power()
            elif token == "/":
                self._consume("/")
                value /= self._parse_power()
            else:
                break
        return value

    def _parse_power(self) -> float:
        return self._parse_unary()

    def _parse_unary(self) -> float:
        token = self._peek()
        if token == "-":
            self._consume("-")
            # -pi^2 means -(pi^2), not (-pi)^2
            return -self._parse_power_body()
        if token == "+":
            self._consume("+")
            return self._parse_power_body()
        return self._parse_power_body()

    def _parse_power_body(self) -> float:
        value = self._parse_atom()
        if self._peek() == "^":
            self._consume("^")
            value = value ** self._parse_power_body()
        return value

    def _parse_atom(self) -> float:
        token = self._peek()
        if token is None:
            raise ValueError("unexpected end of formula")
        if token == "(":
            self._consume("(")
            value = self._parse_expr()
            self._consume(")")
            return value
        if re.fullmatch(r"[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?", token):
            self._consume()
            return float(token)
        if re.fullmatch(r"[a-z_][a-z0-9_]*", token):
            name = self._consume()
            if self._peek() == "(":
                return self._parse_call(name)
            if name not in self.env:
                raise KeyError(f"unknown identifier: {name}")
            return float(self.env[name])
        raise ValueError(f"unsupported token: {token}")

    def _parse_call(self, name: str) -> float:
        self._consume("(")
        args = [self._parse_expr()]
        while self._peek() == ",":
            self._consume(",")
            args.append(self._parse_expr())
        self._consume(")")
        if name == "ln":
            return math.log(args[0])
        if name == "sqrt":
            return math.sqrt(args[0])
        if name == "abs":
            return abs(args[0])
        if name == "sin":
            return math.sin(args[0])
        if name == "cos":
            return math.cos(args[0])
        if name == "exp":
            return math.exp(args[0])
        if name == "arccos":
            return math.acos(args[0])
        if name == "acos":
            return math.acos(args[0])
        if name == "arcsin":
            return math.asin(args[0])
        if name == "asin":
            return math.asin(args[0])
        raise ValueError(f"unsupported function: {name}")


def _tokenize(text: str) -> list[str]:
    pattern = re.compile(
        r"[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?"
        r"|[a-z_][a-z0-9_]*"
        r"|[()+\-*/^,]"
    )
    return pattern.findall(text)


def _insert_implicit_multiplication(tokens: list[str]) -> list[str]:
    out: list[str] = []
    prev: str | None = None
    for token in tokens:
        if prev is not None and _ends_expr(prev) and _starts_expr(token) and not (
            prev.isidentifier() and token == "("
        ):
            out.append("*")
        out.append(token)
        prev = token
    return out


def _ends_expr(token: str) -> bool:
    return bool(re.fullmatch(r"[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?|[a-z_][a-z0-9_]*", token)) or token == ")"


def _starts_expr(token: str) -> bool:
    return bool(re.fullmatch(r"[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?|[a-z_][a-z0-9_]*", token)) or token == "("


def _canonicalize_fsot_v4_formula(normalized: str) -> str:
    """Align portable eval with fsot_numeric_eval_v4 SMILES electrode conventions."""
    compact = normalized.replace(" ", "")
    if compact == "theta-phi":
        return "phi-theta"
    return normalized


def evaluate_formula(formula: str, env: Mapping[str, float]) -> float:
    normalized = _canonicalize_fsot_v4_formula(normalize_formula(formula))
    tokens = _insert_implicit_multiplication(_tokenize(normalized))
    return _FormulaParser(tokens, env).parse()


def load_csv_dataset(path: Path) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for record in reader:
            row: dict[str, float | str] = {}
            for key, value in record.items():
                if value is None or value == "":
                    continue
                try:
                    row[key] = float(value)
                except ValueError:
                    row[key] = value
            rows.append(row)
    return rows


def _sip_hash13(data: bytes, k0: int = 0, k1: int = 0) -> int:
    """Rust DefaultHasher (SipHasher13) compatible digest for stable_row_key."""

    def rotl(x: int, b: int) -> int:
        return ((x << b) | (x >> (64 - b))) & 0xFFFFFFFFFFFFFFFF

    def u64(x: int) -> int:
        return x & 0xFFFFFFFFFFFFFFFF

    v0, v1, v2, v3 = u64(k0 ^ 0x736F6D6570736575), u64(k1 ^ 0x646F72616E646F6D), u64(k0 ^ 0x6C7967656E657261), u64(k1 ^ 0x7465646279746573)
    msg = bytearray(data)
    msg.extend(b"\x00" * ((8 - (len(msg) % 8)) % 8))
    for i in range(0, len(msg), 8):
        m = int.from_bytes(msg[i : i + 8], "little")
        v3 ^= m
        for _ in range(7):
            v0, v1, v2, v3 = u64(v0 + v1), u64(v1 ^ rotl(v2, 13)), u64(v2 + v3), u64(v3 ^ rotl(v0, 16))
            v0, v1, v2, v3 = u64(v0 + v1), u64(v1 ^ rotl(v2, 17)), u64(v2 + v3), u64(v3 ^ rotl(v0, 32))
        v0 ^= m
    v2 ^= 0xFF
    for _ in range(3):
        v0, v1, v2, v3 = u64(v0 + v1), u64(v1 ^ rotl(v2, 13)), u64(v2 + v3), u64(v3 ^ rotl(v0, 16))
        v0, v1, v2, v3 = u64(v0 + v1), u64(v1 ^ rotl(v2, 17)), u64(v2 + v3), u64(v3 ^ rotl(v0, 32))
    return v0 ^ v1 ^ v2 ^ v3


def _hash_u64(value: int) -> bytes:
    return int(value).to_bytes(8, "little", signed=False)


def _hash_str(text: str) -> bytes:
    return text.encode("utf-8")


def stable_row_key(index: int, row: Mapping[str, object], split_seed: int) -> int:
    serialized = json.dumps(dict(sorted(row.items())), separators=(",", ":"), ensure_ascii=True)
    data = _hash_u64(split_seed) + _hash_u64(index) + _hash_str(serialized)
    return _sip_hash13(data)


def split_dataset_rows(
    rows: list[dict[str, float | str]],
    train_fraction: float,
    split_seed: int,
    shuffle_rows: bool,
) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    if len(rows) < 2:
        raise ValueError("dataset split requires at least 2 rows")
    bounded = max(0.5, min(0.95, train_fraction))
    indexed = list(enumerate(rows))
    if shuffle_rows:
        indexed.sort(key=lambda item: stable_row_key(item[0], item[1], split_seed))
    train_count = round(len(indexed) * bounded)
    train_count = max(1, min(len(indexed) - 1, train_count))
    train = [row for _, row in indexed[:train_count]]
    test = [row for _, row in indexed[train_count:]]
    return train, test


def compute_metrics(actuals: list[float], predictions: list[float]) -> dict[str, float]:
    mean_actual = sum(actuals) / len(actuals)
    ss_res = sum((a - p) ** 2 for a, p in zip(actuals, predictions))
    ss_tot = sum((a - mean_actual) ** 2 for a in actuals)
    mae = sum(abs(a - p) for a, p in zip(actuals, predictions)) / len(actuals)
    rmse = math.sqrt(ss_res / len(actuals))
    r2 = 1.0 if ss_tot <= 1e-15 else 1.0 - ss_res / ss_tot
    return {"r2": r2, "mae": mae, "rmse": rmse}


def evaluate_dataset_formula(
    rows: list[dict[str, float | str]],
    target_column: str,
    formula: str,
    context: Mapping[str, float] | None = None,
) -> dict[str, float]:
    ctx = dict(context or core_context())
    actuals: list[float] = []
    predictions: list[float] = []
    for row in rows:
        target = row.get(target_column)
        if not isinstance(target, (int, float)):
            continue
        env = dict(ctx)
        for key, value in row.items():
            if isinstance(value, (int, float)):
                env[key.lower()] = float(value)
        pred = evaluate_formula(formula, env)
        actuals.append(float(target))
        predictions.append(pred)
    if not actuals:
        raise ValueError(f"no numeric rows for target {target_column}")
    return compute_metrics(actuals, predictions)


def evaluate_dataset_formula_split(
    rows: list[dict[str, float | str]],
    target_column: str,
    formula: str,
    train_fraction: float,
    split_seed: int,
    shuffle_rows: bool,
    context: Mapping[str, float] | None = None,
) -> dict[str, object]:
    train_rows, test_rows = split_dataset_rows(rows, train_fraction, split_seed, shuffle_rows)
    ctx = context or core_context()
    train_metrics = evaluate_dataset_formula(train_rows, target_column, formula, ctx)
    test_metrics = evaluate_dataset_formula(test_rows, target_column, formula, ctx)
    return {
        "train_row_count": len(train_rows),
        "test_row_count": len(test_rows),
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
    }


def review_with_fsot_read(
    fsot_read: Path,
    dataset_path: Path,
    target_column: str,
    formula: str,
    train_fraction: float | None,
    split_seed: int,
    shuffle_rows: bool,
) -> dict | None:
    if not fsot_read.exists():
        return None
    cmd = [
        str(fsot_read),
        "--json",
        "review-formula",
        "--input",
        str(dataset_path),
        "--target",
        target_column,
        "--formula",
        formula,
        "--split-seed",
        str(split_seed),
    ]
    if train_fraction is not None:
        cmd.extend(["--train-fraction", str(train_fraction)])
    if not shuffle_rows:
        cmd.append("--shuffle-rows=false")
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return None
    return json.loads(proc.stdout)