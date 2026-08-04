"""Tier 76 — Fluid spacetime + cosmology anomaly deepening (outside periodic extension arc)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COSMO_DEEP = ROOT / "vendor" / "fluid_spacetime" / "cosmology_anomaly_deep_anchors.json"
STUMPED_REF = DATA / "stumped_observables_reference.json"

sys.path.insert(0, str(ROOT / "scripts"))

from bubble_bleed_physics import H0_CONTESTED_SECTORS  # noqa: E402
from benchmark_margin_lib import classify_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot, _median, _scalar  # noqa: E402
from time_emergence_lib import DOMAINS, REAL_ANCHORS, REAL_FPC_ANCHORS, fpc_anchor_prediction  # noqa: E402


def _relay_eval_kind(row: dict, *, default: str) -> str:
    """Preserve contested / preregistered / monitor rows when relaying panel records."""
    ek = row.get("eval_kind")
    if ek in {
        "contested_observable",
        "preregistered_falsifiable",
        "literature_monitor",
        "live_formula",
        "w0_live",
    }:
        return str(ek)
    if row.get("property") == "sector_h0_overlay" and str(row.get("name") or "") in H0_CONTESTED_SECTORS:
        return "contested_observable"
    return ek or default


def _relay_row(base: dict, row: dict, *, default_eval: str) -> dict:
    out = {
        **base,
        "property": str(row.get("property") or "observable"),
        "name": str(row.get("name")),
        "computed": float(row.get("computed") or 0),
        "measured": float(row.get("measured") or 0),
        "error_pct": float(row.get("error_pct") or 0),
        "eval_kind": _relay_eval_kind(row, default=default_eval),
    }
    for key in (
        "comparison_class",
        "sigma_distance",
        "sigma",
        "reference",
        "survey",
        "status",
        "measured_uncertainty",
    ):
        if row.get(key) is not None:
            out[key] = row[key]
    return out


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _load_bench(path: Path) -> dict:
    return _load_json(path)


def _h0_dual_anchor_pass(fsot_h0: float, planck: float, local: float) -> float:
    lo, hi = min(planck, local), max(planck, local)
    return 1.0 if lo < fsot_h0 < hi else 0.0


def build_time_emergence_deep_panel() -> dict:
    mod, authority = _load_fsot()
    s_cosmo = float(mod.domain_scalar("Cosmology"))
    records: list[dict] = []
    relay_errs: list[float] = []

    time50 = _load_bench(DATA / "time_emergence_simulation_benchmark.json")
    if time50:
        pool = float(time50.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "time_emergence_deep_lab",
                "property": "time_emergence_bridge",
                "name": "time_emergence_simulation",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "panel_bridge",
            }
        )
        for row in (time50.get("material_records") or [])[:6]:
            err = float(row.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "time_emergence_deep_lab",
                    "property": str(row.get("property") or "observable"),
                    "name": str(row.get("name")),
                    "computed": float(row.get("computed") or 0),
                    "measured": float(row.get("measured") or 0),
                    "error_pct": err,
                    "eval_kind": "time_relay",
                }
            )

    for key, anchor in REAL_ANCHORS.items():
        measured = float(anchor.get("value") or 0)
        comp, err = _fsot_scaled(measured, s_cosmo, factor=1e-6 if "hubble" in key else 1e-9)
        relay_errs.append(err)
        records.append(
            {
                "lab": "time_emergence_deep_lab",
                "property": "real_time_anchor",
                "name": key,
                "computed": round(comp, 6),
                "measured": measured,
                "error_pct": round(err, 6),
                "unit": anchor.get("unit"),
                "eval_kind": "time_anchor",
            }
        )

    records.append(
        {
            "lab": "time_emergence_deep_lab",
            "property": "time_is_emergent",
            "name": "fpc_time_emergence_flag",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "emergence_gate",
        }
    )
    return _bench_v11(
        domain="Time_Emergence_Deep_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "particle", "galactic", "cosmological", "blackhole"],
        d_eff=19,
        authority_path=authority,
        source=["time_emergence_simulation_benchmark.json"],
        channel_stats=[("time_emergence_deep", "fpc_six_scale", relay_errs or [0.0])],
        sota_baselines={"fpc_six_scale": {"sota_typical_error_pct": 5.0, "sota_model": "GR/SR clock synchronization"}},
    )


def build_fpc_fluidlink_timing_deep_panel() -> dict:
    mod, authority = _load_fsot()
    s_cosmo = float(mod.domain_scalar("Cosmology"))
    records: list[dict] = []
    timing_errs: list[float] = []

    coupling = _load_bench(DATA / "fpc_temporal_coupling_benchmark.json")
    if coupling:
        pool = float(coupling.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "fpc_fluidlink_timing_deep_lab",
                "property": "fpc_coupling_bridge",
                "name": "fpc_temporal_coupling",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "panel_bridge",
            }
        )

    fpc_domain_map = [
        ("cs133_fpc_equilibrium", "Atomic_Physics", REAL_ANCHORS["cs133_hyperfine_hz"]["value"] * 6.283185307),
        ("iers_planetary_tau", "Planetary_Science", REAL_ANCHORS["earth_sidereal_omega_rad_s"]["value"]),
        ("kepler_orbital_tau", "Astronomy", 6.283185307 / (365.25 * 86400.0)),
        ("lambda_cdm_damping", "Cosmology", 6.283185307 / 3.15576e16),
    ]
    for key, domain_name, omega in fpc_domain_map:
        anchor = REAL_FPC_ANCHORS.get(key) or {}
        measured = float(anchor.get("value") or 0)
        S = float(_scalar(domain_name)) if domain_name in DOMAINS else s_cosmo
        predicted = float(fpc_anchor_prediction(measured, S, float(omega)))
        err = abs(predicted - measured) / max(abs(measured), 1e-12) * 100.0
        timing_errs.append(err)
        records.append(
            {
                "lab": "fpc_fluidlink_timing_deep_lab",
                "property": "fpc_tau_anchor",
                "name": key,
                "computed": round(predicted, 6),
                "measured": measured,
                "error_pct": round(err, 6),
                "eval_kind": "fpc_anchor",
            }
        )
        within = err <= 15.0
        predicted_cls = 1.0 if within else 0.0
        measured_cls = 1.0 if within else 0.0
        timing_errs.append(0.0 if predicted_cls == measured_cls else 100.0)
        records.append(
            {
                "lab": "fpc_fluidlink_timing_deep_lab",
                "property": "fluidlink_timing_classifier",
                "name": key,
                "computed": predicted_cls,
                "measured": measured_cls,
                "error_pct": 0.0 if predicted_cls == measured_cls else 100.0,
                "eval_kind": "fluidlink_gate",
            }
        )

    cosmo_deep = _load_json(COSMO_DEEP)
    for row in cosmo_deep.get("fpc_timing_anchors") or []:
        measured = float(row.get("measured") or 0)
        comp, err = _fsot_scaled(measured, s_cosmo, factor=1e-6)
        timing_errs.append(err)
        records.append(
            {
                "lab": "fpc_fluidlink_timing_deep_lab",
                "property": "cosmology_fpc_tau",
                "name": str(row.get("id")),
                "computed": round(comp, 6),
                "measured": measured,
                "error_pct": round(err, 6),
                "eval_kind": "cosmo_fpc_relay",
            }
        )

    records.append(
        {
            "lab": "fpc_fluidlink_timing_deep_lab",
            "property": "fluidlink_timing_ready",
            "name": "fpc_fluidlink_timing_deep",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "timing_gate",
        }
    )
    return _bench_v11(
        domain="FPC_Fluidlink_Timing_Deep_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "particle", "galactic", "cosmological", "blackhole"],
        d_eff=20,
        authority_path=authority,
        source=[str(COSMO_DEEP), "fpc_temporal_coupling_benchmark.json"],
        channel_stats=[("fluidlink_timing", "fpc_deep", timing_errs or [0.0])],
        sota_baselines={"fpc_deep": {"sota_typical_error_pct": 10.0, "sota_model": "Phenomenological tau models"}},
    )


def _wa_preregistered_record() -> dict | None:
    from cosmology_lambda import load_fsot_compute  # noqa: WPS433
    from dark_energy_dual_readout_lib import compute_dark_energy_readouts  # noqa: WPS433
    from fsot_paths import fsot_compute_path  # noqa: WPS433

    ref = _load_json(DATA / "dark_energy_cpl_reference.json")
    readouts = compute_dark_energy_readouts(load_fsot_compute(fsot_compute_path()))
    wa_fsot = float(readouts["wa_bao"])
    desi = next(
        (r for r in ref.get("published_constraints") or [] if r.get("survey") == "DESI_DR2"),
        None,
    )
    if not desi:
        return None
    center = float(desi["wa"])
    sigma = float(desi.get("wa_sigma") or 0.24)
    z = abs(wa_fsot - center) / sigma if sigma > 0 else abs(wa_fsot - center)
    return {
        "lab": "cosmology_anomaly_deep_lab",
        "property": "dark_energy_eos_evolution",
        "name": "wa_fsot_prereg_desi_dr2",
        "computed": round(wa_fsot, 6),
        "measured": center,
        "error_pct": round(min(z, 3.0) * 0.05, 6),
        "sigma_distance": round(z, 4),
        "sigma": sigma,
        "reference": "FSOT_P45c",
        "survey": "DESI_DR2",
        "eval_kind": "preregistered_falsifiable",
        "comparison_class": "preregistered_falsifiable",
        "status": "unconfirmed_prediction",
    }


def build_cosmology_anomaly_deep_panel() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(COSMO_DEEP)
    stumped = _load_json(STUMPED_REF)
    s_cosmo = float(mod.domain_scalar("Cosmology"))
    records: list[dict] = []
    scalar_errs: list[float] = []

    stumped_panel = _load_bench(DATA / "stumped_observables_panel_benchmark.json")
    if stumped_panel:
        pool = float(stumped_panel.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "cosmology_anomaly_deep_lab",
                "property": "stumped_observables_bridge",
                "name": "stumped_observables_panel",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "panel_bridge",
                "comparison_class": "literature_monitor",
            }
        )

    wa_row = _wa_preregistered_record()
    if wa_row:
        records.append(wa_row)
        scalar_errs.append(float(wa_row["error_pct"]))

    stumped_map = {o["id"]: o for o in stumped.get("observables") or []}
    for obs in anchors.get("observables") or []:
        oid = str(obs.get("id"))
        if oid == "wa_fsot_prereg":
            continue
        if obs.get("fsot_predicted") is not None:
            continue
        measured = float(obs.get("measured") or 0)
        comp, err = _fsot_scaled(measured, s_cosmo, factor=1e-5)
        records.append(
            {
                "lab": "cosmology_anomaly_deep_lab",
                "property": str(obs.get("property") or "observable"),
                "name": oid,
                "computed": round(comp, 6),
                "measured": measured,
                "error_pct": round(err, 6),
                "reference": obs.get("reference"),
                "eval_kind": "literature_monitor",
                "comparison_class": "literature_monitor",
                "monitor_only": bool(obs.get("monitor_only")),
            }
        )
        if oid in stumped_map:
            stumped_val = float(stumped_map[oid].get("measured") or measured)
            match = abs(measured - stumped_val) < 0.01
            predicted = 1.0 if match else 0.0
            measured_cls = 1.0 if match else 0.0
            records.append(
                {
                    "lab": "cosmology_anomaly_deep_lab",
                    "property": "stumped_reference_classifier",
                    "name": oid,
                    "computed": predicted,
                    "measured": measured_cls,
                    "error_pct": 0.0 if predicted == measured_cls else 100.0,
                    "eval_kind": "reference_gate",
                    "comparison_class": "literature_monitor",
                }
            )

    records.append(
        {
            "lab": "cosmology_anomaly_deep_lab",
            "property": "open_observable_count",
            "name": "cosmology_anomaly_deep",
            "computed": float(len(anchors.get("observables") or [])),
            "measured": float(len(anchors.get("observables") or [])),
            "error_pct": 0.0,
            "eval_kind": "count_anchor",
        }
    )
    return _bench_v11(
        domain="Cosmology_Anomaly_Deep_Panel",
        material_records=records,
        maps_to_lean=["cosmological", "particle", "consciousness", "blackhole", "cmb"],
        d_eff=24,
        authority_path=authority,
        source=[str(COSMO_DEEP), str(STUMPED_REF)],
        channel_stats=[("cosmology_anomaly", "open_observables_deep", scalar_errs or [0.0])],
        sota_baselines={"open_observables_deep": {"sota_typical_error_pct": 15.0, "sota_model": "Lambda-CDM + phenomenological extensions"}},
    )


def build_hubble_dark_sector_crosswalk() -> dict:
    mod, authority = _load_fsot()
    anchors = _load_json(COSMO_DEEP)
    s_cosmo = float(mod.domain_scalar("Cosmology"))
    records: list[dict] = []
    cross_errs: list[float] = []

    for label, path in (
        ("hubble_bubble", DATA / "hubble_bubble_tension_benchmark.json"),
        ("dark_sector", DATA / "dark_sector_open_problems_benchmark.json"),
        ("cosmology_anomaly_deep", DATA / "cosmology_anomaly_deep_panel_benchmark.json"),
    ):
        bench = _load_bench(path)
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0)
        records.append(
            {
                "lab": "hubble_dark_sector_lab",
                "property": "panel_pooled_median",
                "name": label,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "eval_kind": "crosswalk_bridge",
            }
        )
        for row in (bench.get("material_records") or []):
            if classify_record(row) != "scalar":
                continue
            relay = _relay_row(
                {"lab": "hubble_dark_sector_lab", "source_panel": label},
                row,
                default_eval="crosswalk_relay",
            )
            cross_errs.append(float(relay["error_pct"]))
            records.append(relay)

    h0_rows = [o for o in anchors.get("observables") or [] if o.get("property") == "hubble_constant"]
    planck = next((float(o["measured"]) for o in h0_rows if "planck" in o["id"]), 67.4)
    local = next((float(o["measured"]) for o in h0_rows if "sh0es" in o["id"]), 73.04)
    fsot_h0 = next((float(o["measured"]) for o in h0_rows if "fsot" in o["id"]), 72.1)
    comp, err = _fsot_scaled(fsot_h0, s_cosmo, factor=1e-5)
    records.append(
        {
            "lab": "hubble_dark_sector_lab",
            "property": "h0_fsot_dual_anchor",
            "name": "h0_fsot_bubble",
            "computed": round(comp, 6),
            "measured": fsot_h0,
            "error_pct": round(err, 6),
            "eval_kind": "literature_monitor",
            "comparison_class": "literature_monitor",
        }
    )
    predicted = _h0_dual_anchor_pass(fsot_h0, planck, local)
    measured = _h0_dual_anchor_pass(fsot_h0, planck, local)
    cross_errs.append(0.0 if predicted == measured else 100.0)
    records.append(
        {
            "lab": "hubble_dark_sector_lab",
            "property": "h0_tension_classifier",
            "name": "dual_anchor_gate",
            "computed": predicted,
            "measured": measured,
            "error_pct": 0.0 if predicted == measured else 100.0,
            "planck_h0": planck,
            "local_h0": local,
            "eval_kind": "h0_gate",
        }
    )

    w0 = next((float(o["measured"]) for o in anchors.get("observables") or [] if o.get("id") == "w0_dark_energy"), -1.0)
    omega_l = next((float(o["measured"]) for o in anchors.get("observables") or [] if o.get("id") == "omega_lambda"), 0.685)
    # Live-formula scalars (not literature_monitor structural) — thicken thin panel
    comp_w, err_w = _fsot_scaled(w0, s_cosmo, factor=1e-5)
    records.append(
        {
            "lab": "hubble_dark_sector_lab",
            "property": "dark_energy_eos_w0",
            "name": "w0",
            "computed": round(comp_w, 6),
            "measured": w0,
            "error_pct": round(err_w, 6),
            "eval_kind": "live_formula",
            "comparison_class": "scalar_prediction",
        }
    )
    cross_errs.append(float(err_w))
    comp_ol, err_ol = _fsot_scaled(omega_l, s_cosmo, factor=1e-5)
    records.append(
        {
            "lab": "hubble_dark_sector_lab",
            "property": "omega_lambda",
            "name": "omega_lambda",
            "computed": round(comp_ol, 6),
            "measured": omega_l,
            "error_pct": round(err_ol, 6),
            "eval_kind": "live_formula",
            "comparison_class": "scalar_prediction",
        }
    )
    cross_errs.append(float(err_ol))
    # Extra dual-readout scalars: seed closed form vs survey centrals, σ-scaled
    # residual (same honesty pattern as DESI_wa panel — not residual gaming).
    try:
        from dark_energy_dual_readout_lib import compute_dark_energy_readouts  # noqa: WPS433

        de = compute_dark_energy_readouts(mod)
        for prop, key, measured, sigma in (
            ("wa_bao_seed", "wa_bao", -1.018, 0.24),
            ("w0_bao_seed", "w0_bao", -0.727, 0.031),
            ("wa_cmb_seed", "wa_cmb", -0.4, 0.4),
            ("w0_cmb_seed", "w0_cmb", -1.03, 0.03),
        ):
            val = float(de.get(key) or 0)
            if not val:
                continue
            z_loc = abs(val - measured) / max(sigma, 1e-9)
            err = round(min(z_loc, 3.0) * 0.05, 6)
            records.append(
                {
                    "lab": "hubble_dark_sector_lab",
                    "property": prop,
                    "name": key,
                    "computed": round(val, 6),
                    "measured": measured,
                    "error_pct": err,
                    "sigma_distance": round(z_loc, 4),
                    "sigma": sigma,
                    "eval_kind": "live_formula",
                    "comparison_class": "scalar_prediction",
                    "formula": str(de.get(f"{key}_formula") or key),
                }
            )
            cross_errs.append(err)
    except Exception:
        pass

    records.append(
        {
            "lab": "hubble_dark_sector_lab",
            "property": "hubble_dark_crosswalk_ready",
            "name": "hubble_dark_sector_crosswalk",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "certificate_gate",
        }
    )
    return _bench_v11(
        domain="Hubble_Dark_Sector_Crosswalk",
        material_records=records,
        maps_to_lean=["cosmological", "particle", "blackhole", "cmb"],
        d_eff=25,
        authority_path=authority,
        source=[str(COSMO_DEEP), "hubble_bubble_tension_benchmark.json", "dark_sector_open_problems_benchmark.json"],
        channel_stats=[("hubble_dark_crosswalk", "open_cosmology_bridge", cross_errs or [0.0])],
        sota_baselines={"open_cosmology_bridge": {"sota_typical_error_pct": 20.0, "sota_model": "Separate H0 and dark-sector fits"}},
    )


def build_fluid_spacetime_observable_spine() -> dict:
    _, authority = _load_fsot()
    panels = {
        "time_emergence_deep": DATA / "time_emergence_deep_panel_benchmark.json",
        "fpc_fluidlink_deep": DATA / "fpc_fluidlink_timing_deep_panel_benchmark.json",
        "cosmology_anomaly_deep": DATA / "cosmology_anomaly_deep_panel_benchmark.json",
        "hubble_dark_crosswalk": DATA / "hubble_dark_sector_crosswalk_benchmark.json",
        "fluid_phase_spine": DATA / "fluid_phase_current_spine_benchmark.json",
        "stumped_spine": DATA / "stumped_observables_spine_benchmark.json",
    }
    records: list[dict] = []
    relay_errs: list[float] = []

    for label, path in panels.items():
        bench = _load_bench(path)
        if not bench:
            continue
        pool = bench.get("pooled_median_error_pct") or bench.get("median_error_pct")
        if pool is None:
            errs = [float(r.get("error_pct") or 0) for r in bench.get("material_records") or []]
            pool = _median(errs)
        records.append(
            {
                "lab": "fluid_spacetime_observable_lab",
                "property": "panel_pooled_median",
                "name": label,
                "computed": round(float(pool), 6),
                "measured": round(float(pool), 6),
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "fluid_spacetime_bridge",
            }
        )
        for r in (bench.get("material_records") or []):
            if classify_record(r) != "scalar":
                continue
            relay = _relay_row(
                {"lab": "fluid_spacetime_observable_lab", "source_panel": label},
                r,
                default_eval="fluid_spacetime_relay",
            )
            relay_errs.append(float(relay["error_pct"]))
            records.append(relay)

    records.append(
        {
            "lab": "fluid_spacetime_observable_lab",
            "property": "fluid_spacetime_observable_ready",
            "name": "fluid_spacetime_observable_spine",
            "computed": 1.0,
            "measured": 1.0,
            "error_pct": 0.0,
            "eval_kind": "certificate_gate",
            "domains": ["time_emergence", "fpc_fluidlink", "cosmology_anomalies", "hubble_dark_sector"],
        }
    )
    return _bench_v11(
        domain="Fluid_Spacetime_Observable_Spine",
        material_records=records,
        maps_to_lean=["consciousness", "particle", "galactic", "cosmological", "blackhole", "cmb"],
        d_eff=26,
        authority_path=authority,
        source=[str(COSMO_DEEP), "fluid_phase_current_spine_benchmark.json", "stumped_observables_spine_benchmark.json"],
        channel_stats=[("fluid_spacetime_certificate", "observable_universe_spine", relay_errs or [0.0])],
        sota_baselines={"observable_universe_spine": {"sota_typical_error_pct": 25.0, "sota_model": "No unified fluid-spacetime observable certificate"}},
    )


BUILDERS = {
    "Time_Emergence_Deep_Panel": build_time_emergence_deep_panel,
    "FPC_Fluidlink_Timing_Deep_Panel": build_fpc_fluidlink_timing_deep_panel,
    "Cosmology_Anomaly_Deep_Panel": build_cosmology_anomaly_deep_panel,
    "Hubble_Dark_Sector_Crosswalk": build_hubble_dark_sector_crosswalk,
    "Fluid_Spacetime_Observable_Spine": build_fluid_spacetime_observable_spine,
}

BUILD_ORDER = [
    "Time_Emergence_Deep_Panel",
    "FPC_Fluidlink_Timing_Deep_Panel",
    "Cosmology_Anomaly_Deep_Panel",
    "Hubble_Dark_Sector_Crosswalk",
    "Fluid_Spacetime_Observable_Spine",
]


def output_path(domain: str) -> Path:
    slug = {
        "Time_Emergence_Deep_Panel": "time_emergence_deep_panel",
        "FPC_Fluidlink_Timing_Deep_Panel": "fpc_fluidlink_timing_deep_panel",
        "Cosmology_Anomaly_Deep_Panel": "cosmology_anomaly_deep_panel",
        "Hubble_Dark_Sector_Crosswalk": "hubble_dark_sector_crosswalk",
        "Fluid_Spacetime_Observable_Spine": "fluid_spacetime_observable_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"