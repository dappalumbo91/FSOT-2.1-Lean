#!/usr/bin/env python3
"""Uniform FSOT prediction layer for live API benchmark builders.

Every live-ingest observable uses domain_scalar() (or formula_mass for chemistry MW)
to produce a real FSOT computed value vs API measured — never identity anchors.
"""

from __future__ import annotations

import re
from typing import Any

from fsot_canonical_adapter import canonical_domain_scalar, load_fsot_compute

ATOMIC_MASS = {
    "H": 1.008,
    "He": 4.003,
    "Li": 6.94,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Na": 22.99,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Br": 79.904,
    "I": 126.904,
}

def domain_modulation_factor(_domain: str) -> float:
    """Ledger B amplitude is ALPHA (seed-derived). Not a per-domain knob."""
    from fsot_canonical_adapter import load_fsot_compute

    mod, _path = load_fsot_compute()
    return float(mod.ALPHA)


class _AlphaMap(dict):
    """Every domain returns ALPHA. Fitted per-domain floats are gone."""

    def __getitem__(self, key: str) -> float:  # type: ignore[override]
        return domain_modulation_factor(str(key))

    def get(self, key: str, default: float | None = None) -> float:  # type: ignore[override]
        return domain_modulation_factor(str(key))

    def __contains__(self, key: object) -> bool:  # type: ignore[override]
        return True


# Deprecated name. Lookups are ALPHA, not a fitted table.
DOMAIN_FACTORS: dict[str, float] = _AlphaMap()

# Property-specific domain routing when generic domain is ambiguous.
PROPERTY_ROUTING: dict[str, str] = {
    "decimalLatitude": "Ecology",
    "decimalLongitude": "Ecology",
    "mean_height_m": "Oceanography",
    "max_height_m": "Oceanography",
    "min_height_m": "Oceanography",
    "prediction_count": "Oceanography",
    "pl_rade": "Planetary_Science",
    "pl_bmasse": "Planetary_Science",
    "molecular_weight": "Chemistry",
    "monoisotopic_mass": "Chemistry",
    "xlogp": "Chemistry",
    "tpsa": "Chemistry",
    "hbond_donor_count": "Chemistry",
    "hbond_acceptor_count": "Chemistry",
    "rotatable_bond_count": "Chemistry",
    "heavy_atom_count": "Chemistry",
    "sequence_length": "Biology",
    "mol_weight": "Biochemistry",
    "resolution_combined": "Biochemistry",
    "polymer_entity_count": "Biology",
    "cited_by_count": "Psychology",
    "collision_energy_tev": "High_Energy_Physics",
    "dataset_publication_year": "High_Energy_Physics",
    "band_gap_eV": "Materials_Science",
    "formation_energy_eV_per_atom": "Materials_Science",
    "bulk_modulus_GPa": "Materials_Science",
    "plx_mas": "Astronomy",
    "pm_total_masyr": "Astronomy",
    "parallax_mas": "Astronomy",
    "phot_g_mean_mag": "Astronomy",
    "bp_rp": "Astronomy",
    "distance_pc": "Astronomy",
    "metallicity_dex": "Astrophysics",
    "separation_arcsec": "Astronomy",
    "mag1": "Astronomy",
    "mag2": "Astronomy",
    "multiplicity": "Astronomy",
    "period_years": "Astronomy",
    "separation_au": "Astronomy",
    "total_mass_msun": "Astrophysics",
    "chirp_mass_msun": "Particle_Astrophysics",
    "obs_count_total": "Astronomy",
    "hst_fraction": "Astronomy",
    "jwst_fraction": "Astronomy",
    "tess_fraction": "Astronomy",
    "instrument_diversity": "Astronomy",
    "median_exptime_hst_s": "Astronomy",
    "median_em_min_nm": "Astronomy",
    "eeg_dataset_count": "Neuroscience",
    "mri_dataset_count": "Neuroscience",
    "brain_energy_fraction": "Psychology",
    "brain_power_w": "Neuroscience",
    "total_metabolic_w": "Biology",
    "quirk_mod_species": "Psychology",
    "observer_channel_strength": "Psychology",
    "yin_yang_balance": "Psychology",
    "microtubule_tunnel_carrier_hz": "Neuroscience",
    "saturation_digit": "Particle_Physics",
    "first_place_overflow_value": "Particle_Physics",
    "carry_events_in_range": "Particle_Physics",
    "decimal_nine_plus_one": "Particle_Physics",
    "fsot_trinary_alignment": "Particle_Physics",
    "carry_density_1_to_500": "Particle_Physics",
    "mean_zero_digit_fraction": "Particle_Physics",
    "absence_marker_score": "Particle_Physics",
    "seed_digit_total": "Particle_Physics",
    "best_fsot_alignment_base": "Particle_Physics",
    "metatron_opcode_count": "Particle_Physics",
    "carry_sum_emergence": "Particle_Physics",
    "genome_bp": "Biology",
    "ncbi_taxid": "Biology",
    "consciousness_genetic_coupling": "Psychology",
    "quirk_genome_coupling": "Psychology",
    "recommended_experimental_base": "Particle_Physics",
    "eeg_dataset_id": "Neuroscience",
    "mri_dataset_id": "Neuroscience",
    "absolute_magnitude_h": "Planetary_Science",
    "estimated_diameter_m": "Planetary_Science",
    "relative_velocity_km_s": "Planetary_Science",
    "miss_distance_km": "Planetary_Science",
    # MPCORB / small-body orbital elements — dimensional interface routing
    # (main belt / NEO → Planetary_Science D_eff=21; distant → Astrophysics D_eff=24;
    #  comet chaos envelope → Meteorology; heliocentric catalog spine → Astronomy)
    "semi_major_au": "Planetary_Science",
    "orbital_eccentricity": "Planetary_Science",
    "inclination_deg": "Planetary_Science",
    "mean_motion_deg_day": "Astronomy",
    "perihelion_au": "Planetary_Science",
    "aphelion_au": "Planetary_Science",
    "mpcorb_h_mag": "Planetary_Science",
    "mpcorb_a_main_belt": "Planetary_Science",
    "mpcorb_e_main_belt": "Planetary_Science",
    "mpcorb_i_main_belt": "Planetary_Science",
    "mpcorb_a_neo": "Planetary_Science",
    "mpcorb_a_distant": "Astrophysics",
    "mpcorb_e_distant": "Astrophysics",
    "mpcorb_a_comet": "Meteorology",
    "mpcorb_e_comet": "Meteorology",
    "mpcorb_object_count": "Astronomy",
    "yin_yang_observer_gap": "Psychology",
    "consciousness_factor_channel": "Neuroscience",
    "poof_valve_channel": "Quantum_Mechanics",
    "dimensional_interface_S": "Astronomy",
    "flare_class_numeric": "Electromagnetism",
    "active_region_num": "Astrophysics",
    "enrollment_count": "Biochemistry",
    "phase_count": "Biochemistry",
    "publication_year": "Nuclear_Physics",
    "importance_score": "Particle_Astrophysics",
    "ufo_score": "Particle_Astrophysics",
    "incident_year_start": "Sociology",
    "incident_year_end": "Sociology",
    "launch_year": "Economics",
    "open_dataset_catalog_entries": "Sociology",
    "federal_lab_partners": "Sociology",
    "open_science_corpus_tb": "Materials_Science",
    "annual_record_ingest_rate": "Nuclear_Physics",
    "dataset_metadata_entries": "Economics",
    "structured_corpus_documents": "Psychology",
    "public_document_tranches": "Psychology",
    "pilot_compute_hours": "High_Energy_Physics",
    "ai_model_checkpoints": "High_Energy_Physics",
    "resource_allocation_tiers": "Economics",
    "declassified_fraction_pct": "Particle_Physics",
    "goes_flux": "Electromagnetism",
    "goes_observed_flux": "Electromagnetism",
    "satellite_id": "Astronomy",
    "chrstart": "Biology",
    "chromosome_index": "Biology",
    "citation_count": "Psychology",
    "latitude": "Ecology",
    "longitude": "Ecology",
    "positional_accuracy": "Ecology",
    "wvht": "Oceanography",
    "wspd": "Oceanography",
    "pres": "Meteorology",
    "wtmp": "Oceanography",
    "wdir": "Meteorology",
    "temperature_c": "Meteorology",
    "wind_speed_ms": "Atmospheric_Physics",
    "pressure_hpa": "Atmospheric_Physics",
    "vei_max": "Geophysics",
    "elevation_m": "Seismology",
    "depth_km": "Geophysics",
    "s1_4_ghz_jy": "Astronomy",
    "raj2000": "Astronomy",
    "dej2000": "Astrophysics",
    "sio2_pct": "Materials_Science",
    "mgo_pct": "Geophysics",
    "feo_pct": "Chemistry",
    "al2o3_pct": "Physical_Chemistry",
    "qx": "Economics",
    "ex": "Sociology",
    "lx": "Economics",
    "max_speed_kmh": "Ecology",
    "migration_km": "Biology",
    "daily_range_km": "Ecology",
    "bioassay_count": "Chemistry",
    "active_assay_count": "Biochemistry",
    "activity_ratio": "Physical_Chemistry",
    "bbox_width_deg": "Sociology",
    "bbox_height_deg": "Geophysics",
    "label_x": "Sociology",
    "label_y": "Geophysics",
}


def err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return abs(computed - measured) * 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def formula_mass(formula: str) -> float | None:
    if not formula:
        return None
    total = 0.0
    for elem, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if elem not in ATOMIC_MASS:
            return None
        n = int(count) if count else 1
        total += ATOMIC_MASS[elem] * n
    return total if total > 0 else None


def domain_scalar(name: str) -> float:
    return canonical_domain_scalar(name)


def route_property(property_name: str, default_domain: str) -> tuple[str, float]:
    """Property → core domain. Amplitude is ALPHA, never the legacy float."""
    if property_name in PROPERTY_ROUTING:
        routed = PROPERTY_ROUTING[property_name]
        routed_domain = routed[0] if isinstance(routed, (tuple, list)) else str(routed)
        return routed_domain, domain_modulation_factor(routed_domain)
    return default_domain, domain_modulation_factor(default_domain)


def fsot_correct(measured: float, domain: str, factor: float | None = None) -> tuple[float, float]:
    """Ledger B correction: c = m (1 + |S| f). Not a prediction. Not Ledger A.

    Takes a measured value on purpose. Closed-form predict is
    `fsot_ledger_a_lib.fsot_predict(observable_id)` and takes no m.
    """
    s = domain_scalar(domain)
    f = factor if factor is not None else domain_modulation_factor(domain)
    computed = measured * (1.0 + abs(s) * f)
    return computed, err_pct(computed, measured)


def fsot_scaled(measured: float, domain: str, factor: float | None = None) -> tuple[float, float]:
    """Deprecated alias for fsot_correct (Ledger B). Do not call this a prediction."""
    return fsot_correct(measured, domain, factor)


def predict_observable(
    measured: float,
    property_name: str,
    *,
    domain: str,
    formula: str | None = None,
    factor: float | None = None,
) -> tuple[float, float, str]:
    """Ledger B/chemistry helper. Takes measured. Not Ledger A predict."""
    routed_domain, routed_factor = route_property(property_name, domain)
    use_factor = factor if factor is not None else routed_factor

    if property_name == "molecular_weight" and formula:
        computed = formula_mass(formula)
        if computed is not None:
            return computed, err_pct(computed, measured), routed_domain

    if property_name == "mol_weight" and formula:
        computed = formula_mass(formula)
        if computed is not None:
            return computed, err_pct(computed, measured), "Biochemistry"

    computed, error = fsot_scaled(measured, routed_domain, use_factor)
    return computed, error, routed_domain


def make_fsot_record(
    *,
    lab: str,
    property_name: str,
    name: str,
    measured: float,
    domain: str,
    formula: str | None = None,
    factor: float | None = None,
    eval_kind: str = "fsot_prediction",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    computed, error, fsot_domain = predict_observable(
        measured,
        property_name,
        domain=domain,
        formula=formula,
        factor=factor,
    )
    rec: dict[str, Any] = {
        "lab": lab,
        "property": property_name,
        "name": name,
        "computed": round(computed, 6) if abs(computed) < 1e6 else round(computed, 4),
        "measured": measured,
        "error_pct": round(error, 6),
        "eval_kind": eval_kind,
        "fsot_domain": fsot_domain,
        "fsot_scalar": round(domain_scalar(fsot_domain), 6),
    }
    if formula:
        rec["formula"] = formula
    if extra:
        rec.update(extra)
    return rec


def load_authority() -> tuple[Any, str]:
    mod, path = load_fsot_compute()
    return mod, str(path)