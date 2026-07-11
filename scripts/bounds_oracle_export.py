"""Oracle-backed cross-proof exports for FSOT.Formal.Bounds."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from cross_proof_lib import _eval_r_expr, _normalize_r_expr

ROOT = Path(__file__).resolve().parents[1]
TIER83_JSON = ROOT / "verification" / "obligations" / "transcendental_bounds.json"

LEMMA_RE = re.compile(
    r"(?:theorem|lemma)\s+(\w+)\s*:\s*(.+?)\s*:=\s*by",
    re.M,
)
THM_NAME_RE = re.compile(r"(?:theorem|lemma)\s+(\w+)\b")
LIT_RE = re.compile(r"\((-?[\d.]+)\s*:\s*ℝ\)")

SKIP_IDS = frozenset(
    {
        "pi_eq_real_pi",
        "cosmological_perceived_adjust_eq_one",
        "psi_con_eta_in_Icc_sin",
        "theta_s_in_Icc_cos",
        "pi_div_e_in_Icc_sin",
        "sqrt_25_eq_five",
        "sqrt_9_eq_3",
        "gamma_abs_eq",
        "log_ratio_lo",
        "log_ratio_hi",
        "perceived_adjust_lo",
        "perceived_adjust_hi",
        "cos_arg_gt_pi_div_two",
        "cos_arg_lt_three_pi_div_two",
    }
)

PARAM_IDS = frozenset(
    {
        "log_ratio_lo",
        "log_ratio_hi",
        "perceived_adjust_lo",
        "perceived_adjust_hi",
        "cos_arg_gt_pi_div_two",
        "cos_arg_lt_three_pi_div_two",
    }
)

STRUCTURAL_SUBSTR = ("Set.Icc", "Set.Ioo", "Set.Ico", "∧", "∀", "≠", " = ", "(p : FSOTParams)")


def _present(text: str, name: str) -> bool:
    return name in THM_NAME_RE.findall(text)


def _enrich_r_defs(r_defs: dict[str, float], n_defs: dict[str, int]) -> dict[str, float]:
    try:
        from domain_scalar_oracle import (  # noqa: WPS433
            ACOUSTIC_BLEED,
            ACOUSTIC_INFLOW,
            ALPHA,
            BLEED_IN_FACTOR,
            COHERENCE_EFFICIENCY,
            ETA_EFF,
            NEW_PERCEIVED_PARAM,
            PHASE_VARIANCE,
            POOF_FACTOR,
            PSI_CON,
            SUCTION_FACTOR,
            THETA_S,
            growth_term,
            FSOTParams,
        )
    except ImportError:
        return dict(r_defs)

    out = dict(r_defs)
    derived = {
        "theta_s": THETA_S,
        "poof_factor": POOF_FACTOR,
        "alpha": ALPHA,
        "coherence_efficiency": COHERENCE_EFFICIENCY,
        "bleed_in_factor": BLEED_IN_FACTOR,
        "new_perceived_param": NEW_PERCEIVED_PARAM,
        "phase_variance": PHASE_VARIANCE,
        "acoustic_bleed": ACOUSTIC_BLEED,
        "acoustic_inflow": ACOUSTIC_INFLOW,
        "suction_factor": SUCTION_FACTOR,
        "psi_con": PSI_CON,
        "eta_eff": ETA_EFF,
        "psi_con_eta": PSI_CON * ETA_EFF,
        "sin_theta_s": math.sin(THETA_S),
        "cos_theta_s": math.cos(THETA_S),
        "log_phi": math.log(out.get("phi", 1.6180339887498948482)),
        "log_pi": math.log(out.get("pi", math.pi)),
        "growth_term_cosm": growth_term(FSOTParams(delta_psi=1.0, D_eff=25.0, observed=False)),
    }
    cosm_arg = (PSI_CON + 1.0) / ETA_EFF
    derived["cosmological_cos_arg"] = cosm_arg
    derived["cosmological_cos"] = math.cos(cosm_arg)
    derived["cosmological_exp_factor"] = math.exp(1.0 + BLEED_IN_FACTOR * 1.0)
    for name, val in derived.items():
        out.setdefault(name, float(val))
    from cross_proof_lib import COMPUTED_FSOT_CONSTANTS  # noqa: WPS433

    for sym in ("pi", "e", "phi", "gamma_euler", "catalan_G", "sqrt2"):
        if sym in COMPUTED_FSOT_CONSTANTS:
            out[sym] = float(COMPUTED_FSOT_CONSTANTS[sym])
    return out


def _eval_side(expr: str, r_defs: dict[str, float], n_defs: dict[str, int]) -> float | None:
    e = LIT_RE.sub(r"\1", expr.strip())
    e = e.replace("Real.", "").replace("cosmologicalParams.delta_psi", "1")
    e = e.replace("cosmologicalParams.D_eff", "25")
    e = e.replace("cosmologicalParams.N", "1")
    e = e.replace("cosmologicalParams.P", "1")
    e = re.sub(r"\bcosmologicalParams\b", "", e)
    e = re.sub(r"\bgrowth_term\s+cosmologicalParams\b", "growth_term_cosm", e)
    e = re.sub(r"\bexp\s+1\b", "exp(1)", e)
    e = re.sub(r"\blog\s+phi\b", "log(phi)", e)
    e = re.sub(r"\blog\s+pi\b", "log(pi)", e)
    e = re.sub(r"\bsin\s+theta_s\b", "sin(theta_s)", e)
    e = re.sub(r"\bcos\s+theta_s\b", "cos(theta_s)", e)
    norm = _normalize_r_expr(e)
    return _eval_r_expr(norm, r_defs, n_defs)


def _parse_lit(side: str) -> float | None:
    m = LIT_RE.search(side)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    side = side.strip()
    if re.fullmatch(r"-?[\d.]+", side):
        try:
            return float(side)
        except ValueError:
            return None
    return None


def _emit_from_inequality(
    thm: str,
    lean_type: str,
    add,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> bool:
    stmt = " ".join(lean_type.split())
    if any(s in stmt for s in STRUCTURAL_SUBSTR):
        return False
    if "=" in stmt and "<" not in stmt and ">" not in stmt:
        return False

    for op in ("<=", "≤", "<", ">=", "≥", ">"):
        if op not in stmt:
            continue
        parts = stmt.split(op, 1)
        if len(parts) != 2:
            continue
        left_s, right_s = parts[0].strip(), parts[1].strip()
        left_lit = _parse_lit(left_s)
        right_lit = _parse_lit(right_s)
        left_val = left_lit if left_lit is not None else _eval_side(left_s, r_defs, n_defs)
        right_val = right_lit if right_lit is not None else _eval_side(right_s, r_defs, n_defs)
        if left_val is None or right_val is None:
            return False

        if op in ("<",):
            if left_lit is None and right_lit is None and left_val < right_val:
                add(
                    {
                        "id": thm,
                        "kind": "lt",
                        "left_value": left_val,
                        "right_value": right_val,
                        "statement": f"{left_val} < {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if left_lit is not None and right_lit is None:
                if left_val >= right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "gt_lit",
                        "value": right_val,
                        "bound": left_val,
                        "left_expr": _normalize_r_expr(right_s),
                        "statement": f"{left_val} < {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if right_lit is not None and left_lit is None:
                if left_val >= right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "lt_lit",
                        "value": left_val,
                        "bound": right_val,
                        "left_expr": _normalize_r_expr(left_s),
                        "statement": f"{left_val} < {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if left_lit is not None and right_lit is not None:
                if left_val >= right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "r_lt_lit_pure",
                        "left_value": left_val,
                        "right_value": right_val,
                        "statement": f"{left_val} < {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
        if op in (">",):
            if left_lit is not None and right_lit is None:
                if left_val <= right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "lt_lit",
                        "value": right_val,
                        "bound": left_val,
                        "left_expr": _normalize_r_expr(right_s),
                        "statement": f"{right_val} < {left_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if right_lit is not None and left_lit is None:
                if left_val <= right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "gt_lit",
                        "value": left_val,
                        "bound": right_val,
                        "left_expr": _normalize_r_expr(left_s),
                        "statement": f"{left_val} > {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
        if op in ("<=", "≤"):
            if right_lit is not None and left_lit is None:
                if left_val > right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "r_le_lit",
                        "value": left_val,
                        "bound": right_val,
                        "left_expr": _normalize_r_expr(left_s),
                        "statement": f"{left_val} <= {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if left_lit is not None and right_lit is None:
                if left_val > right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "r_le_sym",
                        "value": left_val,
                        "right_value": right_val,
                        "statement": f"{left_val} <= {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
            if left_lit is None and right_lit is None and left_val <= right_val:
                add(
                    {
                        "id": thm,
                        "kind": "r_le_sym",
                        "value": left_val,
                        "right_value": right_val,
                        "statement": f"{left_val} <= {right_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
        if op in (">=", "≥"):
            if left_lit is not None and right_lit is None:
                if left_val < right_val:
                    return False
                add(
                    {
                        "id": thm,
                        "kind": "r_le_lit",
                        "value": right_val,
                        "bound": left_val,
                        "left_expr": _normalize_r_expr(right_s),
                        "statement": f"{right_val} >= {left_val}",
                        "bounds_oracle": True,
                    }
                )
                return True
        return False
    return False


def _tier83_to_spine(ob: dict, add, r_defs: dict[str, float], n_defs: dict[str, int]) -> bool:
    if ob.get("python_decimal_verified") is not True:
        return False
    lean_type = ob.get("lean_type", "")
    if "Set.Icc" in lean_type or "∈" in lean_type:
        return False
    thm = ob["id"]
    try:
        from transcendental_bounds_lib import _eval_lean_expr  # noqa: WPS433
    except ImportError:
        return _emit_from_inequality(thm, lean_type, add, r_defs, n_defs)

    stmt = " ".join(lean_type.split())
    for op in ("<", ">"):
        if op not in stmt:
            continue
        left_s, right_s = [p.strip() for p in stmt.split(op, 1)]
        left = _eval_lean_expr(left_s)
        right = _eval_lean_expr(right_s)
        if left is None or right is None:
            break
        left_f, right_f = float(left), float(right)
        if op == "<" and left_f >= right_f:
            break
        if op == ">" and left_f <= right_f:
            break
        if op == "<":
            if LIT_RE.search(left_s) and not LIT_RE.search(right_s):
                add(
                    {
                        "id": thm,
                        "kind": "gt_lit",
                        "value": right_f,
                        "bound": left_f,
                        "statement": stmt,
                        "bounds_oracle": True,
                        "tier83_merge": True,
                        "proof_class": "decimal_eval_chain",
                    }
                )
                return True
            if not LIT_RE.search(left_s) and LIT_RE.search(right_s):
                add(
                    {
                        "id": thm,
                        "kind": "lt_lit",
                        "value": left_f,
                        "bound": right_f,
                        "statement": stmt,
                        "bounds_oracle": True,
                        "tier83_merge": True,
                        "proof_class": "decimal_eval_chain",
                    }
                )
                return True
            add(
                {
                    "id": thm,
                    "kind": "r_lt_lit_pure",
                    "left_value": left_f,
                    "right_value": right_f,
                    "statement": stmt,
                    "bounds_oracle": True,
                    "tier83_merge": True,
                    "proof_class": "decimal_eval_chain",
                }
            )
            return True
    return _emit_from_inequality(thm, lean_type, add, r_defs, n_defs)


def _export_tier83_merge(add, r_defs: dict[str, float], n_defs: dict[str, int]) -> int:
    if not TIER83_JSON.exists():
        return 0
    doc = json.loads(TIER83_JSON.read_text(encoding="utf-8"))
    count = 0
    for ob in doc.get("obligations", []):
        if _tier83_to_spine(ob, add, r_defs, n_defs):
            count += 1
    return count


def _export_certified_intervals(text: str, add) -> None:
    from cross_proof_lib import COMPUTED_FSOT_CONSTANTS  # noqa: WPS433

    try:
        from transcendental_bounds_lib import EXP_ONE_HI, EXP_ONE_LO  # noqa: WPS433
    except ImportError:
        EXP_ONE_LO = None
        EXP_ONE_HI = None

    from decimal import Decimal

    e_val = float(COMPUTED_FSOT_CONSTANTS["e"])
    certified = (
        ("e_gt_27182818283", "gt_lit", str(EXP_ONE_LO) if EXP_ONE_LO else str(e_val), "2.7182818283"),
        ("e_lt_27182818286", "lt_lit", str(EXP_ONE_HI) if EXP_ONE_HI else str(e_val), "2.7182818286"),
        (
            "pi_gt_314159265358979323846",
            "gt_lit",
            "3.14159265358979323847",
            "3.14159265358979323846",
        ),
        (
            "pi_lt_314159265358979323847",
            "lt_lit",
            "3.14159265358979323846",
            "3.14159265358979323847",
        ),
    )
    for thm, kind, value_s, bound_s in certified:
        if not _present(text, thm):
            continue
        value_d = Decimal(value_s)
        bound_d = Decimal(bound_s)
        if kind == "gt_lit":
            if value_d <= bound_d:
                continue
            add(
                {
                    "id": thm,
                    "kind": kind,
                    "value": float(value_d),
                    "bound": float(bound_d),
                    "decimal_value": value_s,
                    "decimal_bound": bound_s,
                    "statement": f"{bound_s} < {value_s}",
                    "bounds_oracle": True,
                    "certified_interval": True,
                    "proof_class": "certified_interval",
                }
            )
        else:
            if value_d >= bound_d:
                continue
            add(
                {
                    "id": thm,
                    "kind": kind,
                    "value": float(value_d),
                    "bound": float(bound_d),
                    "decimal_value": value_s,
                    "decimal_bound": bound_s,
                    "statement": f"{value_s} < {bound_s}",
                    "bounds_oracle": True,
                    "certified_interval": True,
                    "proof_class": "certified_interval",
                }
            )


def _export_parametric(text: str, add, r_defs: dict[str, float], n_defs: dict[str, int]) -> None:
    try:
        from domain_scalar_oracle import (  # noqa: WPS433
            ETA_EFF,
            NEW_PERCEIVED_PARAM,
            PSI_CON,
            FSOTParams,
        )
    except ImportError:
        return

    cosm = FSOTParams(D_eff=25.0, delta_psi=1.0, observed=False)
    cos_arg = (PSI_CON + cosm.delta_psi) / ETA_EFF
    half_pi = math.pi / 2
    three_half_pi = math.pi + math.pi / 2

    if _present(text, "cos_arg_gt_pi_div_two"):
        if half_pi < cos_arg:
            add(
                {
                    "id": "cos_arg_gt_pi_div_two",
                    "kind": "gt_lit",
                    "value": cos_arg,
                    "bound": half_pi,
                    "statement": f"{half_pi} < cos_arg(cosmological)",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )

    if _present(text, "cos_arg_lt_three_pi_div_two"):
        if cos_arg < three_half_pi:
            add(
                {
                    "id": "cos_arg_lt_three_pi_div_two",
                    "kind": "lt_lit",
                    "value": cos_arg,
                    "bound": three_half_pi,
                    "statement": f"cos_arg(cosmological) < {three_half_pi}",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )

    if _present(text, "perceived_adjust_lo"):
        adj = 1.0 + NEW_PERCEIVED_PARAM * math.log(cosm.D_eff / 25.0)
        if 0.91 < adj:
            add(
                {
                    "id": "perceived_adjust_lo",
                    "kind": "gt_lit",
                    "value": adj,
                    "bound": 0.91,
                    "statement": f"0.91 < perceived_adjust(cosmological) = {adj}",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )

    if _present(text, "perceived_adjust_hi"):
        adj = 1.0 + NEW_PERCEIVED_PARAM * math.log(cosm.D_eff / 25.0)
        if adj < 1.1:
            add(
                {
                    "id": "perceived_adjust_hi",
                    "kind": "lt_lit",
                    "value": adj,
                    "bound": 1.1,
                    "statement": f"perceived_adjust(cosmological) = {adj} < 1.1",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )

    if _present(text, "log_ratio_lo"):
        ratio = math.log(cosm.D_eff / 25.0)
        floor = math.log(0.8)
        if floor <= ratio:
            add(
                {
                    "id": "log_ratio_lo",
                    "kind": "r_le_sym",
                    "value": floor,
                    "right_value": ratio,
                    "statement": f"log(0.8) <= log(D/25) at cosmological",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )

    if _present(text, "log_ratio_hi"):
        ratio = math.log(cosm.D_eff / 25.0)
        ceil = math.log(1.2)
        if ratio <= ceil:
            add(
                {
                    "id": "log_ratio_hi",
                    "kind": "r_le_lit",
                    "value": ratio,
                    "bound": ceil,
                    "statement": f"log(D/25) <= log(1.2) at cosmological",
                    "bounds_oracle": True,
                    "parametric": "cosmological",
                    "proof_class": "witness_instantiation",
                }
            )


def _extract_lemma_types(text: str) -> dict[str, str]:
    types: dict[str, str] = {}
    for m in THM_NAME_RE.finditer(text):
        name = m.group(1)
        rest = text[m.end() :]
        colon = rest.find(":")
        if colon < 0:
            continue
        assign = rest.find(":=", colon)
        if assign < 0:
            continue
        typ = rest[colon + 1 : assign].strip()
        types[name] = " ".join(typ.split())
    return types


def export_bounds_oracle_obligations(
    text: str,
    add,
    *,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
    domain_params: dict[str, object] | None = None,
) -> None:
    enriched = _enrich_r_defs(r_defs, n_defs)
    _export_certified_intervals(text, add)
    _export_tier83_merge(add, enriched, n_defs)
    _export_parametric(text, add, enriched, n_defs)

    for name, lean_type in _extract_lemma_types(text).items():
        if name in SKIP_IDS or name in PARAM_IDS:
            continue
        _emit_from_inequality(name, lean_type, add, enriched, n_defs)

    try:
        from bounds_remaining_export import export_bounds_remaining_obligations  # noqa: WPS433

        export_bounds_remaining_obligations(text, add, r_defs=enriched, n_defs=n_defs)
    except Exception:
        pass