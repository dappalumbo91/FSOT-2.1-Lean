"""FSOT dark-energy dual readout — CMB vs BAO sector derivations (zero free parameters)."""

from __future__ import annotations

from typing import Any

# Survey → which intrinsic readout lane applies (CMB-primary vs BAO-primary).
CMB_PRIMARY_SURVEYS = frozenset({"Planck2018", "PantheonPlus", "DESI_2024_BAO_preview"})
BAO_PRIMARY_SURVEYS = frozenset({"DESI_DR2"})
BLENDED_SURVEYS = frozenset({"DES_Y3"})


def compute_dark_energy_readouts(mod) -> dict[str, Any]:
    """
    Derive w0/wa from fsot_compute constants — no fitted knobs.

    CMB lane (Planck-class): w0 = −P_new·π/G, wa = −γeφ/π
    BAO lane (DESI DR2-class): w0 bleeds (1−G/π); wa couples BAO w0 via G/π
    """
    from fsot_compute import GAMMA, G_CAT, P_NEW, PI, E, PHI  # noqa: WPS433

    w0_cmb = float(-P_NEW * PI / G_CAT)
    wa_cmb = float(-GAMMA * E * PHI / PI)
    g_over_pi = float(G_CAT / PI)
    bao_bleed = float(1 - G_CAT / PI)
    w0_bao = w0_cmb * bao_bleed
    wa_bao = wa_cmb + w0_bao * g_over_pi

    return {
        "w0_cmb": w0_cmb,
        "w0_cmb_formula": "−P_new·π/G",
        "wa_cmb": wa_cmb,
        "wa_cmb_formula": "−γ·e·φ/π",
        "w0_bao": w0_bao,
        "w0_bao_formula": "w0_cmb·(1 − G/π)",
        "wa_bao": wa_bao,
        "wa_bao_formula": "wa_cmb + w0_bao·(G/π)",
        "bao_bleed_factor": bao_bleed,
        "g_over_pi": g_over_pi,
        "mechanism": "CMB sound-horizon vs BAO acoustic-scale readout (Catalan/π bleed)",
    }


def readout_lane_for_survey(survey: str) -> str:
    if survey in BAO_PRIMARY_SURVEYS:
        return "bao"
    if survey in CMB_PRIMARY_SURVEYS:
        return "cmb"
    if survey in BLENDED_SURVEYS:
        return "blended"
    return "cmb"


def fsot_w0_wa_for_survey(readouts: dict[str, Any], survey: str) -> tuple[float, float, str, str]:
    lane = readout_lane_for_survey(survey)
    if lane == "bao":
        return (
            readouts["w0_bao"],
            readouts["wa_bao"],
            readouts["w0_bao_formula"],
            readouts["wa_bao_formula"],
        )
    if lane == "blended":
        # Intrinsic midpoint — DESI-class surveys between CMB and BAO anchors
        w0 = 0.5 * (readouts["w0_cmb"] + readouts["w0_bao"])
        wa = 0.5 * (readouts["wa_cmb"] + readouts["wa_bao"])
        return w0, wa, "mean(CMB,BAO) w0", "mean(CMB,BAO) wa"
    return (
        readouts["w0_cmb"],
        readouts["wa_cmb"],
        readouts["w0_cmb_formula"],
        readouts["wa_cmb_formula"],
    )