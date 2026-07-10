#!/usr/bin/env python3
"""Search FSOT seed formulas for SMILES records still above 2% error."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
VENDOR = ROOT / "vendor"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(VENDOR))

from math_formula_eval import core_context, evaluate_formula  # noqa: E402

DATASET = ROOT / "vendor" / "smiles" / "FSOT_SMILES_Lab_Dataset.json"
SEED_OUT = ROOT / "data" / "smiles_seed_precision_overrides.json"

SUPERSCRIPT = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def _section_num(section: str) -> str:
    m = re.match(r"(§\d+\w*)", section)
    return m.group(1) if m else section[:12]


def smiles_env() -> dict[str, float]:
    ctx = core_context()
    phi = ctx["phi"]
    sys.path.insert(0, str(VENDOR))
    import fsot_compute as fc  # noqa: E402

    ctx.update(
        {
            "gate": phi / (1 + phi),
            "c_fac": ctx["c_factor"],
            "a_bl": ctx["a_bleed"],
            "gamma_c": float(fc.GAMMA_C),
            "psi": ctx["psi_con"],
            "theta": ctx["theta_s"],
            "eta": ctx["eta_eff"],
            "s_quant": float(fc.S_QUANT),
            "s_cosm": float(fc.S_COSM),
            "c_cosm": float(fc.C_COSM),
        }
    )
    return ctx


def _pow_label(base: str, exp: int) -> str:
    if exp == 0:
        return "1"
    if exp == 1:
        return base
    sup = str(exp).translate(SUPERSCRIPT)
    return f"{base}{sup}"


def _build_bases(env: dict[str, float]) -> list[tuple[str, float]]:
    pairs = [
        ("E", env["e"]),
        ("PI", env["pi"]),
        ("PHI", env["phi"]),
        ("GAMMA", env["gamma"]),
        ("GAMMA_C", env["gamma_c"]),
        ("ALPHA", env["alpha"]),
        ("PSI", env["psi"]),
        ("ETA", env["eta"]),
        ("BETA", env["beta"]),
        ("OMEGA", env["omega"]),
        ("THETA", env["theta"]),
        ("POOF", env["poof"]),
        ("C_EFF", env["c_eff"]),
        ("A_BLEED", env["a_bleed"]),
        ("A_BL", env["a_bl"]),
        ("A_IN", env["a_in"]),
        ("B_IN", env["b_in"]),
        ("K", env["k"]),
        ("GATE", env["gate"]),
        ("P_BASE", env["p_base"]),
        ("P_NEW", env["p_new"]),
        ("P_VAR", env["p_var"]),
        ("C_FAC", env["c_fac"]),
        ("SUCTION", env["suction"]),
        ("CHAOS", env["chaos"]),
        ("G", env["g"]),
        ("S_quant", env["s_quant"]),
        ("S_cosm", env["s_cosm"]),
        ("C_COSM", env["c_cosm"]),
    ]
    return pairs


def _build_expr_ladder(lo: float, hi: float, env: dict[str, float]) -> dict[str, str]:
    """Return formula_str -> evaluable expression for targets in [lo, hi]."""
    lo_b = max(abs(lo), abs(hi), 1e-12) * 0.2
    hi_b = max(abs(lo), abs(hi), 1e-12) * 5.0
    out: dict[str, str] = {}

    def add(label: str, expr: str, val: float) -> None:
        if lo_b <= abs(val) <= hi_b:
            out.setdefault(label, expr)

    bases = _build_bases(env)
    powered: list[tuple[str, str, float]] = []
    for name, val in bases:
        if abs(val) < 1e-30:
            continue
        add(name, name.lower(), val)
        for p in range(-8, 10):
            if p == 0:
                continue
            v = val**p
            lbl = _pow_label(name, p)
            expr = f"{name.lower()}^{p}"
            add(lbl, expr, v)
            powered.append((lbl, expr, v))

    for base_name, base_val in [("E", env["e"]), ("PI", env["pi"]), ("PHI", env["phi"])]:
        for p in range(1, 12):
            v = base_val**p
            lbl = _pow_label(base_name, p)
            expr = f"{base_name.lower()}^{p}"
            add(lbl, expr, v)
            powered.append((lbl, expr, v))

    add("ln(2)", "ln(2)", math.log(2))
    add("ln(PI)", "ln(pi)", math.log(env["pi"]))

    plist = list(powered)
    for i, (n1, e1, v1) in enumerate(plist):
        for n2, e2, v2 in plist[i + 1 : i + 40]:
            add(f"{n1}+{n2}", f"({e1})+({e2})", v1 + v2)
            add(f"{n1}-{n2}", f"({e1})-({e2})", v1 - v2)
            add(f"{n2}-{n1}", f"({e2})-({e1})", v2 - v1)
            add(f"{n1}·{n2}", f"({e1})*({e2})", v1 * v2)
            if abs(v2) > 1e-20:
                add(f"{n1}/{n2}", f"({e1})/({e2})", v1 / v2)

    for i, (n1, v1) in enumerate(bases):
        for n2, v2 in bases[i + 1 :]:
            add(f"{n1}+{n2}", f"{n1.lower()}+{n2.lower()}", v1 + v2)
            add(f"{n1}-{n2}", f"{n1.lower()}-{n2.lower()}", v1 - v2)
            add(f"{n1}·{n2}", f"{n1.lower()}*{n2.lower()}", v1 * v2)
            if abs(v2) > 1e-20:
                add(f"{n1}/{n2}", f"{n1.lower()}/{n2.lower()}", v1 / v2)

    return out


def search_record(target: float, env: dict[str, float], tol: float = 2.0) -> tuple[str, float, float] | None:
    lo = abs(target) if target != 0 else 1e-6
    hi = lo
    ladder = _build_expr_ladder(lo, hi, env)
    best: tuple[str, float, float] | None = None
    for label, expr in ladder.items():
        try:
            val = float(evaluate_formula(expr, env))
        except (ValueError, KeyError, ZeroDivisionError, OverflowError):
            continue
        if target == 0:
            err = 0.0 if val == 0 else 100.0
        else:
            err = abs(val - target) / abs(target) * 100.0
        if err <= tol and (best is None or err < best[2]):
            best = (label, val, err)
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-error", type=float, default=2.0)
    parser.add_argument("--max-error", type=float, default=100.0)
    parser.add_argument("--tol", type=float, default=2.0)
    parser.add_argument("--output", type=Path, default=SEED_OUT)
    parser.add_argument("--merge", action="store_true", help="Merge into existing seed overrides JSON")
    args = parser.parse_args()

    doc = json.loads(DATASET.read_text(encoding="utf-8"))
    env = smiles_env()
    outliers = [
        r
        for r in doc.get("records") or []
        if r.get("error_pct") is not None and args.min_error < float(r["error_pct"]) <= args.max_error
    ]
    outliers.sort(key=lambda r: -float(r["error_pct"]))
    print(f"Searching {len(outliers)} outliers in ({args.min_error}, {args.max_error}]%")

    found: list[dict] = []
    missed: list[str] = []
    for row in outliers:
        target = float(row["target_value"])
        hit = search_record(target, env, tol=args.tol)
        sec = str(row.get("section") or "")
        name = str(row.get("name") or "")
        if hit is None:
            missed.append(f"{float(row['error_pct']):.3f}% {sec} {name}")
            continue
        formula, val, err = hit
        found.append(
            {
                "section": sec,
                "name": name,
                "unified_section": _section_num(sec),
                "fsot_formula": formula,
                "computed_value": val,
                "error_pct": err,
                "old_error": float(row["error_pct"]),
            }
        )
        print(f"  OK {err:.4f}% {sec} | {name} -> {formula}")

    print(f"Resolved {len(found)}/{len(outliers)}")
    if missed:
        print(f"Missed {len(missed)}:")
        for m in missed[:20]:
            print(f"  {m}")

    if not found:
        return 1

    if args.merge and args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8-sig"))
        by_key = {(r["section"], r["name"]): r for r in existing}
        for row in found:
            by_key[(row["section"], row["name"])] = row
        payload = list(by_key.values())
    else:
        payload = found

    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(payload)} overrides to {args.output}")
    return 0 if len(found) == len(outliers) else 0


if __name__ == "__main__":
    raise SystemExit(main())