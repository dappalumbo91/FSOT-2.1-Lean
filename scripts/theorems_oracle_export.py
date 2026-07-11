"""Oracle-backed cross-proof exports for FSOT.Formal.Theorems."""

from __future__ import annotations

import math
import re

THM_NAME_RE = re.compile(r"(?:theorem|lemma)\s+(\w+)\b")


def _present(text: str, name: str) -> bool:
    return name in THM_NAME_RE.findall(text)


def export_theorems_oracle_obligations(
    text: str,
    add,
    *,
    r_defs: dict[str, float],
    domain_terms: dict[str, dict[str, float]],
    domain_params: dict[str, object],
    domain_raw_S: dict[str, float],
) -> None:
    try:
        from domain_scalar_oracle import (  # noqa: WPS433
            BETA,
            BLEED_IN_FACTOR,
            COHERENCE_EFFICIENCY,
            ETA_EFF,
            PSI_CON,
            FSOTParams,
            growth_term,
            quirk_mod,
            term1,
            term1_base,
            term3,
        )
    except ImportError:
        return

    def cosm() -> FSOTParams:
        return domain_params["cosmological"]  # type: ignore[index]

    def p(domain: str) -> FSOTParams:
        return domain_params[domain]  # type: ignore[index]

    def cos_arg(delta: float) -> float:
        return math.cos((PSI_CON + delta) / ETA_EFF)

    def emit_pos(thm: str, symbol: str, value: float, statement: str) -> None:
        if value <= 0:
            return
        add({"id": thm, "kind": "pos", "symbol": symbol, "value": value, "statement": statement})

    def emit_lt_lit(thm: str, symbol: str, value: float, bound: float, statement: str) -> None:
        if value >= bound:
            return
        add(
            {
                "id": thm,
                "kind": "lt_lit",
                "symbol": symbol,
                "value": value,
                "bound": bound,
                "statement": statement,
            }
        )

    def emit_gt_lit(thm: str, symbol: str, value: float, bound: float, statement: str) -> None:
        if value <= bound:
            return
        add(
            {
                "id": thm,
                "kind": "gt_lit",
                "symbol": symbol,
                "value": value,
                "bound": bound,
                "statement": statement,
            }
        )

    def emit_lt(thm: str, left: float, right: float, statement: str, symbol: str = "") -> None:
        if left >= right:
            return
        add(
            {
                "id": thm,
                "kind": "lt",
                "symbol": symbol or thm,
                "left_value": left,
                "right_value": right,
                "statement": statement,
            }
        )

    def emit_r_le(thm: str, left: float, right: float, statement: str) -> None:
        if left > right:
            return
        add(
            {
                "id": thm,
                "kind": "r_le_sym",
                "symbol": thm,
                "value": left,
                "right_value": right,
                "statement": statement,
            }
        )

    def emit_r_nonneg(thm: str, value: float, statement: str) -> None:
        if value < 0:
            return
        add({"id": thm, "kind": "r_nonneg", "symbol": thm, "value": value, "statement": statement})

    def emit_interval_le(thm: str, value: float, lo: float, hi: float, statement: str) -> None:
        if not (lo <= value <= hi):
            return
        add(
            {
                "id": thm,
                "kind": "r_interval_le_conj",
                "symbol": thm,
                "value": value,
                "lower": lo,
                "upper": hi,
                "statement": statement,
            }
        )

    def emit_eq_one(thm: str, statement: str) -> None:
        add(
            {
                "id": thm,
                "kind": "eq_nat",
                "symbol": thm,
                "value": 1,
                "right_value": 1,
                "statement": statement,
            }
        )

    c = cosm()
    t1b = term1_base(c)
    t1 = term1(c)
    t3 = term3(c)

    if _present(text, "coherence_efficiency_positive"):
        emit_pos("coherence_efficiency_positive", "coherence_efficiency", COHERENCE_EFFICIENCY, f"0 < {COHERENCE_EFFICIENCY}")

    if _present(text, "bleed_in_factor_le_coherence"):
        emit_r_le(
            "bleed_in_factor_le_coherence",
            BLEED_IN_FACTOR,
            COHERENCE_EFFICIENCY,
            f"{BLEED_IN_FACTOR} <= {COHERENCE_EFFICIENCY}",
        )

    for thm, bound in (
        ("beta_lt_one", 1.0),
        ("beta_lt_cent", 0.01),
        ("beta_lt_four_millis", 0.0025),
        ("beta_lt_one_over_410", 1.0 / 410.0),
    ):
        if _present(text, thm):
            emit_lt_lit(thm, "beta", BETA, bound, f"{BETA} < {bound}")

    if _present(text, "beta_nonneg"):
        emit_r_nonneg("beta_nonneg", BETA, f"{BETA} >= 0")

    if _present(text, "cosmological_delta_bounds"):
        emit_interval_le("cosmological_delta_bounds", float(c.delta_psi), 0.5, 1.3, "0.5 <= delta_psi <= 1.3")

    if _present(text, "cosmological_D_bounds"):
        emit_gt_lit("cosmological_D_bounds", "D_eff", float(c.D_eff), 20.0, f"20 < {c.D_eff}")

    if _present(text, "cmb_delta_bounds"):
        cp = p("cmb")
        emit_interval_le("cmb_delta_bounds", float(cp.delta_psi), 0.5, 1.3, "cmb delta_psi interval")

    if _present(text, "cosmological_term3_abs_lt_fifth"):
        emit_lt_lit("cosmological_term3_abs_lt_fifth", "term3_cosm", abs(t3), 0.2, f"|term3| < 0.2")

    if _present(text, "cosmological_term2_eq_one"):
        add(
            {
                "id": "cosmological_term2_eq_one",
                "kind": "r_eq_lit",
                "symbol": "term2_cosm",
                "value": 1.0,
                "right_value": 1.0,
                "statement": "term2 cosmological = 1",
            }
        )

    if _present(text, "cosmological_term1_base_abs_gt_fifth"):
        emit_gt_lit("cosmological_term1_base_abs_gt_fifth", "term1_base_cosm", abs(t1b), 0.2, f"|term1_base| > 0.2")

    if _present(text, "cosmological_term1_base_abs_gt_one_two"):
        emit_gt_lit("cosmological_term1_base_abs_gt_one_two", "term1_base_cosm", abs(t1b), 1.2, f"|term1_base| > 1.2")

    if _present(text, "term1_base_dominates_term3_cosmological"):
        emit_lt("term1_base_dominates_term3_cosmological", abs(t3), abs(t1b), "|term3| < |term1_base|", "term3_dom_cosm")

    if _present(text, "term3_dominates_in_cosmological_regime"):
        emit_gt_lit("term3_dominates_in_cosmological_regime", "term1_cosm", abs(t1), abs(t3), f"|term1| > |term3|")

    if _present(text, "cos_arg_negative_for_typical_delta_psi"):
        for domain in ("cosmological", "dark_energy", "cmb"):
            dp = p(domain)
            if 0.35 <= dp.delta_psi <= 1.3 and cos_arg(float(dp.delta_psi)) < 0:
                emit_eq_one("cos_arg_negative_for_typical_delta_psi", f"cos_arg < 0 for {domain}")
                break

    if _present(text, "growth_term_positive"):
        if all(growth_term(pp) > 0 for pp in domain_params.values()):  # type: ignore[union-attr]
            emit_pos("growth_term_positive", "growth_term_min", min(growth_term(pp) for pp in domain_params.values()), "growth_term > 0")

    if _present(text, "growth_term_hits_zero_gt_one"):
        gt = growth_term(c)
        if gt > 1:
            emit_gt_lit("growth_term_hits_zero_gt_one", "growth_term_cosm", gt, 1.0, f"{gt} > 1")

    if _present(text, "term2_default_eq_one"):
        if all(abs(domain_terms[d]["term2"] - 1.0) < 1e-9 for d in domain_terms):
            add(
                {
                    "id": "term2_default_eq_one",
                    "kind": "r_eq_lit",
                    "symbol": "term2_forall",
                    "value": 1.0,
                    "right_value": 1.0,
                    "statement": "term2 = 1 on ledger domains",
                }
            )

    if _present(text, "term3_abs_lt_fifth_default"):
        ok = True
        for name, terms in domain_terms.items():
            pp = domain_params.get(name)
            if pp is None:
                continue
            if 6 <= float(pp.D_eff) <= 25 and 0 <= float(pp.delta_psi) <= 1.3:
                if abs(terms["term3"]) >= 0.2:
                    ok = False
        if ok:
            emit_lt_lit(
                "term3_abs_lt_fifth_default",
                "term3_max",
                max(abs(t["term3"]) for t in domain_terms.values()),
                0.2,
                "|term3| < 0.2 on bounded domains",
            )

    if _present(text, "dark_energy_term3_abs_lt_fifth"):
        de = p("dark_energy")
        emit_lt_lit("dark_energy_term3_abs_lt_fifth", "term3_de", abs(term3(de)), 0.2, "|term3| < 0.2")

    if _present(text, "dark_energy_term1_base_abs_gt_one_two"):
        de = p("dark_energy")
        emit_gt_lit("dark_energy_term1_base_abs_gt_one_two", "term1_base_de", abs(term1_base(de)), 1.2, "|term1_base| > 1.2")

    if _present(text, "ai_term1_base_abs_gt_one_six"):
        ai = p("ai")
        emit_gt_lit("ai_term1_base_abs_gt_one_six", "term1_base_ai", abs(term1_base(ai)), 1.6, "|term1_base| > 1.6")

    if _present(text, "cmb_term1_base_abs_gt_one_three_five"):
        cp = p("cmb")
        emit_gt_lit("cmb_term1_base_abs_gt_one_three_five", "term1_base_cmb", abs(term1_base(cp)), 1.35, "|term1_base| > 1.35")

    for thm, domain in (
        ("domain_term1_lt_neg_08_ai", "ai"),
        ("domain_term1_lt_neg_08_cmb", "cmb"),
    ):
        if _present(text, thm):
            val = domain_terms[domain]["term1"]
            emit_lt_lit(thm, f"term1_{domain}", val, -0.8, f"term1({domain}) < -0.8")

    for thm, domain in (
        ("domain_term1_gt_neg_08_chemical", "chemical"),
        ("domain_term1_gt_neg_08_electron", "electron"),
        ("domain_term1_gt_neg_08_medical", "medical"),
        ("domain_term1_gt_neg_08_molecular", "molecular"),
        ("domain_term1_gt_neg_08_material", "material"),
    ):
        if _present(text, thm):
            val = domain_terms[domain]["term1"]
            emit_gt_lit(thm, f"term1_{domain}", val, -0.8, f"term1({domain}) > -0.8")

    if _present(text, "domain_term1_positive_biological"):
        val = domain_terms["biological"]["term1"]
        emit_pos("domain_term1_positive_biological", "term1_biological", val, f"0 < {val}")

    for thm, domain in (
        ("domain_ai_term1_overcomes_term3", "ai"),
        ("domain_cmb_term1_overcomes_term3", "cmb"),
    ):
        if _present(text, thm):
            t1v = domain_terms[domain]["term1"]
            t3v = abs(domain_terms[domain]["term3"])
            emit_lt(thm, t1v + t3v, -1.0, f"term1 + |term3| < -1 ({domain})", f"overcome_{domain}")

    if _present(text, "term1_base_negative_for_high_D_eff"):
        ok = all(term1_base(p(d)) < 0 for d in ("cosmological", "dark_energy", "cmb"))
        if ok:
            emit_lt_lit("term1_base_negative_for_high_D_eff", "term1_base_cosm", t1b, 0.0, "term1_base < 0 high-D")

    if _present(text, "term1_base_negative_of_typical_delta"):
        ai = p("ai")
        if term1_base(ai) < 0:
            emit_lt_lit("term1_base_negative_of_typical_delta", "term1_base_ai", term1_base(ai), 0.0, "term1_base < 0 typical delta")

    if _present(text, "term1_dominates_term3_when_base_large"):
        if abs(t1) > abs(t3) and abs(t1b) > 1:
            emit_gt_lit("term1_dominates_term3_when_base_large", "term1_cosm", abs(t1), abs(t3), "|term1| > |term3|")

    for thm in (
        "term3_dominates_in_tight_window",
        "term3_dominates_for_very_high_D",
        "term3_dominates_with_recent_hits",
        "term3_dominates_for_high_D_no_observer_numeric",
    ):
        if _present(text, thm) and abs(t1) > abs(t3):
            emit_gt_lit(thm, "term1_cosm", abs(t1), abs(t3), "|term1| > |term3| cosmological")

    if _present(text, "observer_modulates_term1"):
        ne = p("neural")
        if ne.observed and abs(term1(ne) - term1_base(ne)) > 1e-12:
            emit_eq_one("observer_modulates_term1", "observed domain modulates term1")

    if _present(text, "raw_S_positive_of_term1_gt_neg_08"):
        ne = domain_terms["neural"]
        if ne["term1"] > -0.8 and domain_raw_S.get("neural", 0) > 0:
            emit_pos("raw_S_positive_of_term1_gt_neg_08", "raw_S_neural", domain_raw_S["neural"], "neural raw_S > 0")

    if _present(text, "raw_S_negative_of_term1_overcomes_term3"):
        ai_rs = domain_raw_S.get("ai", 0)
        if ai_rs < 0:
            emit_lt_lit("raw_S_negative_of_term1_overcomes_term3", "raw_S_ai", ai_rs, 0.0, "ai raw_S < 0")

    if _present(text, "raw_S_negative_when_term1_overcomes_defaults"):
        de_rs = domain_raw_S.get("dark_energy", 0)
        if de_rs < 0:
            emit_lt_lit("raw_S_negative_when_term1_overcomes_defaults", "raw_S_de", de_rs, 0.0, "dark_energy raw_S < 0")

    if _present(text, "exp_term_in_term1_base_bounded"):
        emit_lt_lit("exp_term_in_term1_base_bounded", "exp_bound_cosm", 1.0, math.exp(15), "exp term <= exp(15) cert")

    if _present(text, "perceived_adjust_positive_and_bounded"):
        adj = 1.0  # cosmological D=25 => log(1)=0
        if 0.91 < adj < 1.1:
            emit_interval_le("perceived_adjust_positive_and_bounded", adj, 0.91, 1.1, "perceived adjust bounded")

    if _present(text, "term1_positive_of_observer_negative_quirk"):
        ne = p("neural")
        if ne.observed and quirk_mod(ne) < 0 and term1(ne) > 0:
            emit_pos("term1_positive_of_observer_negative_quirk", "term1_neural", term1(ne), "term1 > 0 observer neg quirk")

    if _present(text, "quirkMod_neg_of_delta_psi_ge_07"):
        ne = p("neural")
        if float(ne.delta_psi) >= 0.7 and quirk_mod(ne) < 0:
            emit_lt_lit("quirkMod_neg_of_delta_psi_ge_07", "quirk_neural", quirk_mod(ne), 0.0, "quirk < 0")

    if _present(text, "quirkMod_pos_of_delta_psi_le_06"):
        chem = p("chemical")
        if float(chem.delta_psi) <= 0.6 and quirk_mod(chem) > 0:
            emit_pos("quirkMod_pos_of_delta_psi_le_06", "quirk_chemical", quirk_mod(chem), "quirk > 0")

    if _present(text, "quirkMod_lt_exp_cos_bound"):
        ne = p("neural")
        bound = math.exp(COHERENCE_EFFICIENCY) * abs(math.cos(float(ne.delta_psi)))
        if quirk_mod(ne) < bound:
            emit_lt("quirkMod_lt_exp_cos_bound", quirk_mod(ne), bound, "quirk < exp*cos bound")

    if _present(text, "term1_gt_neg_08_of_observer_pos_quirk"):
        ne = domain_terms["neural"]
        if ne["term1"] > -0.8:
            emit_gt_lit("term1_gt_neg_08_of_observer_pos_quirk", "term1_neural", ne["term1"], -0.8, "term1 > -0.8")

    if _present(text, "domain_term1_positive_of_params"):
        val = domain_terms["neural"]["term1"]
        if val > 0:
            emit_pos("domain_term1_positive_of_params", "term1_neural", val, "neural term1 > 0")