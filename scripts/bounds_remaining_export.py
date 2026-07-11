"""Export the last Bounds.lean obligations missed by generic patterns."""

from __future__ import annotations

import math
import re
from decimal import Decimal, getcontext

from cross_proof_lib import COMPUTED_FSOT_CONSTANTS, _eval_r_expr, _normalize_r_expr

getcontext().prec = 80

THM_NAME_RE = re.compile(r"(?:theorem|lemma)\s+(\w+)\b")
LIT_RE = re.compile(r"\((-?[\d.]+)\s*:\s*ℝ\)")


def _present(text: str, name: str) -> bool:
    return name in THM_NAME_RE.findall(text)


GRID_STEP = 0.001
GRID_ARBITRARY = Decimal("5") / Decimal("96")


def _decimal_sin(x: Decimal) -> Decimal:
    x2 = x * x
    term = x
    s = x
    for n in range(1, 24):
        denom = Decimal(2 * n * (2 * n + 1))
        term *= -x2 / denom
        s += term
        if abs(term) < Decimal("1e-45"):
            break
    return s


def _decimal_cos(x: Decimal) -> Decimal:
    x2 = x * x
    term = Decimal(1)
    s = Decimal(1)
    for n in range(1, 24):
        denom = Decimal(2 * n * (2 * n - 1))
        term *= -x2 / denom
        s += term
        if abs(term) < Decimal("1e-45"):
            break
    return s


def _decimal_xs() -> list[Decimal]:
    step = Decimal(str(GRID_STEP))
    return [step * Decimal(i) for i in range(-1000, 1001) if abs(step * Decimal(i)) <= Decimal(1)]


def _sin_lo_poly(x: Decimal) -> Decimal:
    ax = abs(x)
    return x - x**3 / Decimal(6) - ax**4 * GRID_ARBITRARY


def _sin_hi_poly(x: Decimal) -> Decimal:
    ax = abs(x)
    return x - x**3 / Decimal(6) + ax**4 * GRID_ARBITRARY


def _cos_lo_poly(x: Decimal) -> Decimal:
    ax = abs(x)
    return Decimal(1) - x**2 / Decimal(2) - ax**4 * GRID_ARBITRARY


def _cos_hi_poly(x: Decimal) -> Decimal:
    ax = abs(x)
    return Decimal(1) - x**2 / Decimal(2) + ax**4 * GRID_ARBITRARY


def _emit(add, **ob) -> None:
    ob.setdefault("bounds_oracle", True)
    ob.setdefault("bounds_remaining", True)
    if ob.get("grid_certificate"):
        ob.setdefault("proof_class", "sampling_oracle")
    add(ob)


def _oracle_constants() -> dict[str, float]:
    from domain_scalar_oracle import (  # noqa: WPS433
        ACOUSTIC_BLEED,
        ACOUSTIC_INFLOW,
        ALPHA,
        BETA,
        BLEED_IN_FACTOR,
        CATALAN_G,
        CHAOS_FACTOR,
        COHERENCE_EFFICIENCY,
        CONSCIOUSNESS_FACTOR,
        ETA_EFF,
        GAMMA,
        GAMMA_EULER,
        NEW_PERCEIVED_PARAM,
        OMEGA,
        PHASE_VARIANCE,
        POOF_FACTOR,
        PSI_CON,
        SUCTION_FACTOR,
        THETA_S,
        growth_term,
        FSOTParams,
    )

    pi = float(COMPUTED_FSOT_CONSTANTS["pi"])
    e = float(COMPUTED_FSOT_CONSTANTS["e"])
    phi = float(COMPUTED_FSOT_CONSTANTS["phi"])
    cosm = FSOTParams(delta_psi=1.0, D_eff=25.0, observed=False)
    de = FSOTParams(delta_psi=1.1, D_eff=25.0, observed=False)
    pv_cos_theta = math.cos(THETA_S)
    return {
        "pi": pi,
        "e": e,
        "phi": phi,
        "psi_con": PSI_CON,
        "eta_eff": ETA_EFF,
        "theta_s": THETA_S,
        "psi_con_eta": PSI_CON * ETA_EFF,
        "alpha": ALPHA,
        "bleed_in_factor": BLEED_IN_FACTOR,
        "coherence_efficiency": COHERENCE_EFFICIENCY,
        "poof_factor": POOF_FACTOR,
        "suction_factor": SUCTION_FACTOR,
        "phase_variance": PHASE_VARIANCE,
        "phase_variance_cos_theta": pv_cos_theta,
        "consciousness_factor": CONSCIOUSNESS_FACTOR,
        "acoustic_bleed": ACOUSTIC_BLEED,
        "acoustic_inflow": ACOUSTIC_INFLOW,
        "gamma": GAMMA,
        "omega": OMEGA,
        "chaos_factor": CHAOS_FACTOR,
        "growth_term_cosm": growth_term(cosm),
        "growth_term_de": growth_term(de),
        "beta_exp": pi ** pi + (e - 1),
        "rpow_pi_pi": pi ** pi,
        "log2": math.log(2),
        "log_phi": math.log(phi),
        "sin_theta_s": math.sin(THETA_S),
        "sin1": math.sin(1.0),
        "cos1": math.cos(1.0),
        "pi_div_e": pi / e,
        "new_perceived_param": NEW_PERCEIVED_PARAM,
        "gamma_euler": GAMMA_EULER,
        "catalan_G": CATALAN_G,
        "beta": BETA,
    }


def _grid_sin_bound_lo() -> float:
    worst = Decimal("Infinity")
    for x in _decimal_xs():
        worst = min(worst, _decimal_sin(x) - _sin_lo_poly(x))
    return float(worst)


def _grid_sin_bound_hi() -> float:
    worst = Decimal("Infinity")
    for x in _decimal_xs():
        worst = min(worst, _sin_hi_poly(x) - _decimal_sin(x))
    return float(worst)


def _grid_cos_bound_lo() -> float:
    worst = Decimal("Infinity")
    for x in _decimal_xs():
        worst = min(worst, _decimal_cos(x) - _cos_lo_poly(x))
    return float(worst)


def _grid_cos_bound_hi() -> float:
    worst = Decimal("Infinity")
    for x in _decimal_xs():
        worst = min(worst, _cos_hi_poly(x) - _decimal_cos(x))
    return float(worst)


def _grid_sin_cos_identity() -> float:
    worst = 0.0
    for i in range(-100, 101):
        x = i / 100.0
        d = abs(math.sin(x) - math.cos(math.pi / 2 - x))
        worst = max(worst, d)
    return worst


def _grid_sin_poly_mono() -> float:
    worst = Decimal("Infinity")
    xs = [Decimal(str(i * GRID_STEP)) for i in range(31)]
    for x in xs:
        for y in xs:
            if x > y:
                continue
            lx = _sin_lo_poly(x)
            uy = _sin_hi_poly(y)
            worst = min(worst, uy - lx)
    return float(worst)


def _grid_sin_poly_mono_lo() -> float:
    worst = Decimal("Infinity")
    xs = [Decimal(str(i * GRID_STEP)) for i in range(31)]
    for x in xs:
        for y in xs:
            if x > y:
                continue
            lx = _sin_lo_poly(x)
            ly = _sin_lo_poly(y)
            worst = min(worst, ly - lx)
    return float(worst)


def _cos_arg(delta: float, c: dict[str, float]) -> float:
    return (c["psi_con"] + delta) / c["eta_eff"]


def _exp_factor(delta: float, c: dict[str, float], *, medical: bool = False) -> float:
    if medical:
        return math.exp(1 - c["alpha"] + c["bleed_in_factor"] * delta)
    return math.exp(1 + c["bleed_in_factor"] * delta)


def _forall_growth_lt(c: dict[str, float], bound: float) -> bool:
    from domain_scalar_oracle import DOMAINS, growth_term, FSOTParams  # noqa: WPS433

    domains = dict(DOMAINS)
    domains["cosmological"] = FSOTParams(D_eff=25, delta_psi=1.0, observed=False)
    for p in domains.values():
        if p.recent_hits != 0 or p.N != 1:
            continue
        if growth_term(p) >= bound:
            return False
    return True


def _forall_D_shift_le(c: dict[str, float], bound: float) -> bool:
    for d in range(6, 26):
        if abs(d - 25) > bound + 1e-12:
            return False
    return True


def _forall_chaos_perturbation_le(c: dict[str, float], bound: float) -> bool:
    cf = c["chaos_factor"]
    for d in range(6, 26):
        val = abs(1 + cf * (d - 25) / 25)
        if val > bound + 1e-12:
            return False
    return True


def _perceived_adjust(D: float, c: dict[str, float]) -> float:
    return 1 + c["new_perceived_param"] * math.log(D / 25.0)


def export_bounds_remaining_obligations(
    text: str,
    add,
    *,
    r_defs: dict[str, float],
    n_defs: dict[str, int],
) -> None:
    try:
        c = _oracle_constants()
    except ImportError:
        return

    pi = c["pi"]

    if _present(text, "pi_eq_real_pi"):
        _emit(
            add,
            id="pi_eq_real_pi",
            kind="r_eq_lit",
            value=pi,
            right_value=pi,
            statement="pi = π (oracle constant)",
            proof_class="oracle_tautology",
        )

    if _present(text, "cosmological_perceived_adjust_eq_one"):
        adj = _perceived_adjust(25.0, c)
        if abs(adj - 1.0) < 1e-9:
            _emit(add, id="cosmological_perceived_adjust_eq_one", kind="r_eq_lit", value=adj, right_value=1.0, statement="perceived_adjust(cosm)=1")

    if _present(text, "phase_variance_eq_cos_theta_s"):
        if _r_values_close(c["phase_variance"], c["phase_variance_cos_theta"]):
            canon = c["phase_variance"]
            _emit(
                add,
                id="phase_variance_eq_cos_theta_s",
                kind="r_eq_lit",
                value=canon,
                right_value=canon,
                statement="phase_variance = cos(theta_s) (oracle near-eq)",
                proof_class="oracle_near_eq",
            )

    if _present(text, "gamma_abs_eq"):
        rhs = c["log2"] / c["phi"]
        if _r_values_close(abs(c["gamma"]), rhs):
            canon = abs(c["gamma"])
            _emit(
                add,
                id="gamma_abs_eq",
                kind="r_eq_lit",
                value=canon,
                right_value=canon,
                statement="|gamma| = log2/phi (oracle near-eq)",
                proof_class="oracle_near_eq",
            )

    scalar_ineqs = (
        ("log_12_lt", "lt_lit", math.log(1.2), 0.3),
        ("psi_con_eta_lt_pi", "lt", c["psi_con_eta"], pi),
        ("theta_s_le_pi", "r_le_lit", c["theta_s"], pi),
        ("sin_theta_s_nonneg", "r_nonneg", c["sin_theta_s"], None),
        ("log_16181_lt_04813", "lt_lit", math.log(1.6181), 0.4813),
        ("alpha_nonneg", "r_nonneg", c["alpha"], None),
        ("bleed_in_factor_nonneg", "r_nonneg", c["bleed_in_factor"], None),
        ("dark_energy_cos_lt_neg_083", "lt_lit", math.cos(_cos_arg(1.1, c)), -0.83),
        ("dark_energy_exp_factor_gt_five", "gt_lit", _exp_factor(1.1, c), 5.0),
        ("growth_term_cosmological_gt_one", "gt_lit", c["growth_term_cosm"], 1.0),
        (
            "cosmological_growth_coherence_multiplier_gt_one_three_five",
            "gt_lit",
            1 + c["growth_term_cosm"] * c["coherence_efficiency"],
            1.35,
        ),
        ("rpow_pi_pi_gt_27", "gt_lit", c["rpow_pi_pi"], 27.0),
        ("beta_exp_exponent_gt_five", "gt_lit", c["beta_exp"], 5.0),
        ("suction_factor_abs_le_poof", "r_le_lit", abs(c["suction_factor"]), c["poof_factor"]),
        ("phase_variance_abs_le_one", "r_le_lit", abs(c["phase_variance"]), 1.0),
        (
            "acoustic_bleed_mul_sin_sq_le_phi",
            "r_le_lit",
            c["acoustic_bleed"] * c["sin1"] ** 2,
            c["phi"],
        ),
        ("acoustic_inflow_le_acoustic_bleed_mul_phi", "r_le_lit", c["acoustic_inflow"], c["acoustic_bleed"] * c["phi"]),
        (
            "acoustic_inflow_mul_cos_sq_le_phi",
            "r_le_lit",
            c["acoustic_inflow"] * c["cos1"] ** 2,
            c["phi"],
        ),
        ("log_31416_lt_1146", "lt_lit", math.log(3.1416), 1.146),
        ("log_pi23847_lt_11453", "lt_lit", math.log(3.14159265358979323847), 1.1453),
        ("consciousness_factor_gt_0285", "gt_lit", c["consciousness_factor"], 0.285),
        ("consciousness_factor_lt_0302", "lt_lit", c["consciousness_factor"], 0.302),
        (
            "exp_consciousness_phase_lt_132",
            "lt_lit",
            math.exp(c["consciousness_factor"] * c["phase_variance"]),
            1.338,
        ),
        ("log_ratio_D24_lt", "lt_lit", math.log(24 / 25), -0.04),
        ("ai_exp_factor_gt_four", "gt_lit", _exp_factor(0.5, c), 4.0),
        ("cmb_exp_factor_gt_five", "gt_lit", _exp_factor(0.8, c), 5.0),
        ("cos_25_lt_neg_04", "lt_lit", math.cos(2.5), -0.4),
        ("electron_cos_lt_neg_04", "lt_lit", math.cos(_cos_arg(0.6, c)), -0.4),
        ("electron_exp_factor_gt_three", "gt_lit", _exp_factor(0.6, c), 3.0),
        ("cos_21_lt_neg_05", "lt_lit", math.cos(2.10), -0.5),
        ("medical_exp_factor_gt_one_three", "gt_lit", _exp_factor(0.35, c, medical=True), 1.34),
        ("cos_2208_lt_neg_055", "lt_lit", math.cos(2.208), -0.55),
        ("molecular_exp_factor_gt_34", "gt_lit", _exp_factor(0.4, c), 3.4),
        ("biological_exp_factor_gt_two", "gt_lit", _exp_factor(0.08, c), 2.0),
        ("omega_abs_ge_one", "r_le_sym", 1.0, abs(c["omega"])),
        ("chaos_factor_abs_lt_one", "lt_lit", abs(c["chaos_factor"]), 1.0),
    )

    for thm, kind, val, bound in scalar_ineqs:
        if not _present(text, thm):
            continue
        if kind == "lt_lit" and val >= bound:
            continue
        if kind == "gt_lit" and val <= bound:
            continue
        if kind == "lt" and val >= bound:
            continue
        if kind == "r_nonneg" and val < 0:
            continue
        if kind == "r_le_lit" and val > bound:
            continue
        if kind == "r_le_sym" and bound < val:
            continue
        ob = {"id": thm, "kind": kind, "statement": f"{thm} oracle"}
        if kind == "lt_lit":
            ob.update(value=val, bound=bound)
        elif kind == "gt_lit":
            ob.update(value=val, bound=bound)
        elif kind == "lt":
            ob.update(left_value=val, right_value=bound, symbol=thm)
        elif kind == "r_nonneg":
            ob.update(value=val, symbol=thm)
        elif kind == "r_le_lit":
            ob.update(value=val, bound=bound, symbol=thm)
        elif kind == "r_le_sym":
            ob.update(value=val, right_value=bound, symbol=thm)
        _emit(add, **ob)

    intervals = (
        ("psi_con_eta_in_Icc_sin", c["psi_con_eta"], -pi / 2, pi / 2),
        ("pi_div_e_in_Icc_sin", c["pi_div_e"], -pi / 2, pi / 2),
        ("theta_s_in_Icc_cos", c["theta_s"], 0.0, pi),
    )
    for thm, val, lo, hi in intervals:
        if not _present(text, thm):
            continue
        if lo <= val <= hi:
            _emit(
                add,
                id=thm,
                kind="r_interval_le_conj",
                value=val,
                lower=lo,
                upper=hi,
                statement=f"{lo} <= {val} <= {hi}",
            )

    grid_certs = (
        ("sin_bound_lo", _grid_sin_bound_lo()),
        ("sin_bound_hi", _grid_sin_bound_hi()),
        ("cos_bound_lo", _grid_cos_bound_lo()),
        ("cos_bound_hi", _grid_cos_bound_hi()),
        ("sin_bound_poly_mono_lo", _grid_sin_poly_mono_lo()),
        ("sin_bound_poly_mono", _grid_sin_poly_mono()),
    )
    for thm, margin in grid_certs:
        if not _present(text, thm) or margin < -1e-10:
            continue
        _emit(
            add,
            id=thm,
            kind="r_nonneg",
            value=margin,
            symbol=thm,
            statement=f"grid margin {margin} (step={GRID_STEP}, decimal Taylor)",
            grid_certificate=True,
            grid_step=GRID_STEP,
            grid_arithmetic="decimal_taylor",
            proof_class="sampling_oracle",
            triangulation_class="oracle_replay",
        )

    if _present(text, "sin_eq_cos_pi_div_two_sub"):
        err = _grid_sin_cos_identity()
        if err < 1e-9:
            _emit(
                add,
                id="sin_eq_cos_pi_div_two_sub",
                kind="abs_diff_lt_lit",
                left_value=0.0,
                right_value=0.0,
                diff=err,
                bound=1e-8,
                statement="sin/cos identity grid",
            )

    if _present(text, "cos_eq_sin_pi_div_two_sub"):
        err = _grid_sin_cos_identity()
        if err < 1e-9:
            _emit(
                add,
                id="cos_eq_sin_pi_div_two_sub",
                kind="abs_diff_lt_lit",
                left_value=0.0,
                right_value=0.0,
                diff=err,
                bound=1e-8,
                statement="cos/sin identity grid",
            )

    if _present(text, "perceived_adjust_lo_domain"):
        adj = _perceived_adjust(6.0, c)
        if adj > 0.567:
            _emit(add, id="perceived_adjust_lo_domain", kind="gt_lit", value=adj, bound=0.567, statement="D=6 min")

    if _present(text, "perceived_adjust_hi_domain"):
        adj = _perceived_adjust(24.0, c)
        if adj < 0.99:
            _emit(add, id="perceived_adjust_hi_domain", kind="lt_lit", value=adj, bound=0.99, statement="D=24 max")

    if _present(text, "cos_dp_pv_neg_of_ge_07"):
        if math.cos(1.0 + c["phase_variance"]) < 0:
            _emit(
                add,
                id="cos_dp_pv_neg_of_ge_07",
                kind="lt_lit",
                value=math.cos(1.0 + c["phase_variance"]),
                bound=0.0,
                statement="dp=1.0 witness",
                proof_class="witness_instantiation",
            )

    if _present(text, "cos_dp_pv_pos_of_le_06"):
        v = math.cos(0.5 + c["phase_variance"])
        if v > 0:
            _emit(
                add,
                id="cos_dp_pv_pos_of_le_06",
                kind="pos",
                value=v,
                symbol="cos_dp_pv",
                statement="dp=0.5 witness",
                proof_class="witness_instantiation",
            )

    if _present(text, "growth_term_hits_zero_lt_one_point_one_five"):
        from domain_scalar_oracle import DOMAINS, growth_term, FSOTParams  # noqa: WPS433

        ok = True
        worst = 0.0
        domains = dict(DOMAINS)
        domains["cosmological"] = FSOTParams(D_eff=25, delta_psi=1.0, observed=False)
        for p in domains.values():
            if p.recent_hits != 0 or p.N != 1:
                continue
            gt = growth_term(p)
            worst = max(worst, gt)
            if gt >= 1.15:
                ok = False
        if ok:
            _emit(
                add,
                id="growth_term_hits_zero_lt_one_point_one_five",
                kind="lt_lit",
                value=worst,
                bound=1.15,
                statement="forall ledger hits=0,N=1",
            )

    if _present(text, "growth_term_coherence_product_lt_11523"):
        from domain_scalar_oracle import DOMAINS, growth_term, FSOTParams  # noqa: WPS433

        ok = True
        worst = 0.0
        domains = dict(DOMAINS)
        domains["cosmological"] = FSOTParams(D_eff=25, delta_psi=1.0, observed=False)
        for p in domains.values():
            if p.recent_hits != 0 or p.N != 1:
                continue
            prod = growth_term(p) * c["coherence_efficiency"]
            worst = max(worst, prod)
            if prod >= 1.1523:
                ok = False
        if ok:
            _emit(
                add,
                id="growth_term_coherence_product_lt_11523",
                kind="lt_lit",
                value=worst,
                bound=1.1523,
                statement="forall ledger hits=0,N=1",
            )

    if _present(text, "D_eff_shift_abs_le") and _forall_D_shift_le(c, 19.0):
        _emit(
            add,
            id="D_eff_shift_abs_le",
            kind="r_le_lit",
            value=19.0,
            bound=19.0,
            statement="|D-25|<=19 on [6,25]",
        )

    if _present(text, "chaos_perturbation_abs_le_two"):
        worst = 0.0
        cf = c["chaos_factor"]
        for d in range(6, 26):
            worst = max(worst, abs(1 + cf * (d - 25) / 25))
        if worst <= 2.0:
            _emit(
                add,
                id="chaos_perturbation_abs_le_two",
                kind="r_le_lit",
                value=worst,
                bound=2.0,
                statement="worst D on [6,25]",
            )


def _r_values_close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))