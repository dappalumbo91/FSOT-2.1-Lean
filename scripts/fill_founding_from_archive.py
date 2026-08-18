#!/usr/bin/env python3
"""Add on-topic public literature the founding archive was pointing at.

Does not import FSUFT 4.2 / 8.7 chat-era numbers (71.98, invented %).
Uses the same published families already in founding_unmapped_laws_reference.json
plus the archive's named catalogs (Planck, IceCube/Auger, SPARC, Draine,
Fontaine, OMI/WMO, Espinoza).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from founding_unmapped_laws_lib import BUILDERS, DOMAIN_SLUG, REFERENCE, output_path  # noqa: E402
from c_thin_depth_lib import _tier  # noqa: E402

EXTRA = {
    "law_11": [
        ("casimir_pressure_0p5um", "casimir_pressure_pa", 2.08, "Pa", "Bordag+ Phys.Rep. 353 (2001) 1/d^4 at 0.5 um"),
        ("casimir_pressure_0p7um", "casimir_pressure_pa", 0.541, "Pa", "Bordag+ Phys.Rep. 353 (2001) 1/d^4 at 0.7 um"),
        ("casimir_pressure_2um", "casimir_pressure_pa", 0.008125, "Pa", "Bordag+ Phys.Rep. 353 (2001) 1/d^4 at 2 um"),
        ("casimir_pressure_3um", "casimir_pressure_pa", 0.001605, "Pa", "Bordag+ Phys.Rep. 353 (2001) 1/d^4 at 3 um"),
        ("casimir_energy_density_0p5um", "zero_point_energy", 0.0208, "J/m^3", "Bordag+ 2001 energy density at 0.5 um"),
        ("casimir_energy_density_2um", "zero_point_energy", 8.125e-5, "J/m^3", "Bordag+ 2001 energy density at 2 um"),
        ("decca_force_0p16um_pN", "casimir_force_pN", 320.0, "pN", "Decca et al. PRL 2007 162 nm class"),
        ("mohideen_sphere_plate_pN", "casimir_force_pN", 50.0, "pN", "Mohideen & Roy PRL 81, 4549 (1998)"),
        ("bressi_parallel_plates_pN", "casimir_force_pN", 3.0, "pN", "Bressi et al. PRL 88, 041804 (2002)"),
        ("planck_rho_vac_kg_m3", "vacuum_energy_density", 5.96e-27, "kg/m^3", "Planck 2018 cosmological-constant density"),
        ("codata_hbar", "reduced_planck", 1.054571817e-34, "J s", "CODATA 2018 hbar"),
        ("fine_structure_alpha", "vacuum_coupling", 0.0072973525693, "dimensionless", "CODATA 2018 fine-structure constant"),
        ("compton_electron_pm", "electron_compton_pm", 2.42631023867, "pm", "CODATA 2018 electron Compton wavelength"),
        ("rydberg_hz", "rydberg_frequency", 3.2898419602508e15, "Hz", "CODATA 2018 Rydberg"),
        ("vacuum_impedance_ohm", "z0_ohm", 376.730313461, "ohm", "CODATA 2018 vacuum impedance"),
    ],
    "law_12": [
        ("auger_gzk_cutoff_eV", "uhecr_cutoff_eV", 5.0e19, "eV", "Pierre Auger GZK-like cutoff"),
        ("knee_energy_eV", "cosmic_ray_knee_eV", 3.0e15, "eV", "CR all-particle knee"),
        ("ankle_energy_eV", "cosmic_ray_ankle_eV", 5.0e18, "eV", "CR ankle"),
        ("auger_dipole_8EeV", "cosmic_ray_anisotropy_amplitude", 0.065, "fraction", "Auger Science 2017 dipole E>8 EeV"),
        ("icecube_flavor_ratio", "neutrino_flavor_ratio", 1.0, "dimensionless", "IceCube cosmic flavor ~1:1:1"),
        ("fermi_gc_excess_GeV", "gamma_ray_excess_GeV", 2.0, "GeV", "Fermi-LAT Galactic-centre GeV excess"),
        ("hawc_index_10TeV", "cosmic_ray_spectral_index", 2.63, "dimensionless", "HAWC high-energy spectral index class"),
        ("auger_heavy_fraction_1e18", "uhecr_heavy_fraction", 0.30, "fraction", "Auger composition ~30% heavy at 1e18 eV"),
        ("icecube_100TeV_index", "cosmic_ray_spectral_index", 2.37, "dimensionless", "IceCube 100 TeV class index"),
        ("dipole_phase_auger_deg", "cosmic_ray_anisotropy_phase", 100.0, "deg", "Auger dipole RA class"),
        ("tropospheric_muon_index", "cosmic_ray_spectral_index", 2.7, "dimensionless", "Sea-level muon spectrum index"),
        ("pamela_positron_GeV", "positron_fraction_energy_GeV", 20.0, "GeV", "PAMELA/AMS positron-rise energy class"),
        ("hess_knee_pev", "cosmic_ray_knee_PeV", 1.0, "PeV", "H.E.S.S. knee-region class"),
        ("kascade_index", "cosmic_ray_spectral_index", 2.7, "dimensionless", "KASCADE knee-region index"),
        ("ta_cutoff_eV", "uhecr_cutoff_eV", 6.0e19, "eV", "Telescope Array cutoff class"),
    ],
    "law_13": [
        ("ngc2403_v_flat", "halo_rotation_velocity", 131.0, "km/s", "SPARC NGC 2403"),
        ("ngc2841_v_flat", "halo_rotation_velocity", 284.0, "km/s", "SPARC NGC 2841"),
        ("m31_v_flat", "galaxy_rotation_curve", 250.0, "km/s", "Andromeda rotation"),
        ("reid2014_mw", "halo_rotation_velocity", 240.0, "km/s", "Reid+ 2014 Milky Way"),
        ("sofue_mw", "galaxy_rotation_curve", 238.0, "km/s", "Sofue Milky Way compilation"),
        ("ugc2885_v_flat", "halo_rotation_velocity", 298.0, "km/s", "SPARC UGC 2885"),
        ("ngc7331_v_flat", "galaxy_rotation_curve", 250.0, "km/s", "SPARC NGC 7331"),
        ("things_typical", "halo_rotation_velocity", 200.0, "km/s", "THINGS typical flat rotation"),
        ("mond_a0", "mond_acceleration", 1.2e-10, "m/s^2", "MOND a0 Milgrom"),
        ("ngc6503_v_flat", "galaxy_rotation_curve", 116.0, "km/s", "SPARC NGC 6503"),
        ("ddo154_alt", "halo_rotation_velocity", 47.0, "km/s", "SPARC DDO 154"),
        ("ngc55_v_flat", "galaxy_rotation_curve", 86.0, "km/s", "SPARC NGC 55"),
        ("ic2574_v_flat", "halo_rotation_velocity", 66.0, "km/s", "SPARC IC 2574"),
        ("ngc925_v_flat", "galaxy_rotation_curve", 113.0, "km/s", "SPARC NGC 925"),
        ("lsbs_typical", "halo_rotation_velocity", 80.0, "km/s", "SPARC LSB typical"),
    ],
    "law_20": [
        ("mw_R_V", "extinction_R_V", 3.1, "dimensionless", "Cardelli+ 1989 MW R_V"),
        ("A_V_over_N_H", "dust_extinction_per_H", 5.3e-22, "mag cm2", "Bohlin / Draine A_V/N_H"),
        ("pah_mass_fraction", "dust_pah_fraction", 0.046, "fraction", "Draine & Li 2007 PAH fraction"),
        ("lmc_dust_to_gas", "dust_density_anomaly", 0.0025, "dimensionless", "LMC dust-to-gas"),
        ("smc_dust_to_gas", "dust_density_anomaly", 0.0008, "dimensionless", "SMC dust-to-gas"),
        ("dust_albedo", "dust_albedo", 0.6, "dimensionless", "Draine ISM albedo"),
        ("extinction_beta", "dust_extinction_beta", 1.7, "dimensionless", "FIR extinction beta"),
        ("graphite_peak_um", "dust_grain_radius_um", 0.01, "um", "Weingartner & Draine graphite peak"),
        ("a_min_angstrom", "dust_grain_size", 0.00035, "um", "Weingartner & Draine a_min"),
        ("av_per_kpc", "extinction_mag_per_kpc", 1.0, "mag/kpc", "MW midplane A_V class"),
        ("mrn_power", "dust_size_index", 3.5, "dimensionless", "MRN n(a) ~ a^{-3.5}"),
        ("zodiacal_um", "dust_grain_radius_um", 10.0, "um", "Zodiacal / SPHEREx-class grain"),
        ("silicate_feature_um", "dust_feature_um", 9.7, "um", "Silicate 9.7 um feature"),
        ("carbon_feature_um", "dust_feature_um", 3.3, "um", "PAH 3.3 um feature"),
        ("submm_opacity", "dust_opacity_index", 2.0, "dimensionless", "Submm dust opacity index class"),
    ],
    "law_23": [
        ("wd_typical_mass", "white_dwarf_mass_msun", 0.6, "M_sun", "Sloan / Gaia WD mass peak"),
        ("wd_typical_radius", "white_dwarf_radius_rsun", 0.012, "R_sun", "0.6 Msun WD radius"),
        ("wd_log_g", "white_dwarf_log_g", 8.0, "cgs", "Typical DA log g"),
        ("wd_crystallization_k", "white_dwarf_temperature", 4000.0, "K", "Fontaine crystallization sequence"),
        ("gaia_wd_peak_k", "white_dwarf_temperature", 10000.0, "K", "Gaia WD locus peak"),
        ("wd_1gyr_luminosity", "white_dwarf_luminosity", 0.001, "L_sun", "Fontaine 1 Gyr cooling"),
        ("da_fraction", "white_dwarf_da_fraction", 0.80, "fraction", "DA spectral fraction"),
        ("wd_teff_median", "white_dwarf_temperature", 12000.0, "K", "Sloan WD Teff median class"),
        ("sirius_b_teff", "white_dwarf_temperature", 25000.0, "K", "Sirius B Teff"),
        ("wd_1145_period_hr", "wd_transit_period_hr", 4.5, "hr", "WD 1145+017 disintegrating period class"),
        ("mestel_index", "white_dwarf_cooling_index", 1.4, "dimensionless", "Mestel L ~ t^{-7/5}"),
        ("wd_age_4kK_gyr", "white_dwarf_cooling_time", 10.0, "Gyr", "Fontaine cool DA age class"),
        ("wd_0p9msun", "white_dwarf_mass_msun", 0.9, "M_sun", "High-mass WD peak"),
        ("wd_0p5msun", "white_dwarf_mass_msun", 0.5, "M_sun", "Low-mass He WD class"),
        ("wd_hot_dq_k", "white_dwarf_temperature", 18000.0, "K", "Hot DQ / Sloan hot branch"),
    ],
    "law_26": [
        ("dobson_hole_threshold_du", "ozone_column_du", 220.0, "DU", "WMO ozone-hole threshold"),
        ("midlatitude_column_du", "ozone_column_du", 350.0, "DU", "OMI mid-latitude climatology"),
        ("equatorial_column_du", "ozone_column_du", 260.0, "DU", "OMI equatorial climatology"),
        ("arctic_min_du", "ozone_anomaly_du", 200.0, "DU", "WMO Arctic ozone minimum class"),
        ("tropospheric_mean_ppbv", "atmospheric_ozone", 30.0, "ppbv", "NOAA tropospheric ozone class"),
        ("strat_peak_8ppmv", "atmospheric_ozone_concentration", 8.0, "ppmv", "US Standard Atmosphere strat peak"),
        ("hole_1985_min_du", "ozone_anomaly_du", 120.0, "DU", "WMO 1980s hole minimum class"),
        ("hole_2015_min_du", "ozone_anomaly_du", 110.0, "DU", "WMO 2015 hole minimum class"),
        ("montreal_cfc_index", "cfc_equivalent", 1.0, "relative", "Montreal Protocol CFC baseline"),
        ("omi_global_2020_du", "ozone_column_du", 290.0, "DU", "OMI/OMPS 2020s global mean class"),
        ("antarctic_spring_du", "ozone_column_du", 150.0, "DU", "WMO Antarctic spring mean class"),
        ("trop_ozone_40ppbv", "atmospheric_ozone", 40.0, "ppbv", "NOAA ozonesonde mid-trop class"),
        ("uv_index_clear", "uv_index", 10.0, "index", "WHO clear-sky UV index class"),
        ("total_o3_preindustrial", "ozone_column_du", 300.0, "DU", "Pre-industrial total-column class"),
        ("omi_nh_spring_du", "ozone_column_du", 380.0, "DU", "OMI northern-hemisphere spring class"),
    ],
    "law_34": [
        ("vela_dnu_over_nu", "pulsar_glitch_spin_up", 2.34e-6, "fraction", "Espinoza+ Vela typical large glitch"),
        ("crab_dnu_over_nu", "pulsar_glitch_spin_up", 4.0e-8, "fraction", "Crab typical glitch size"),
        ("typical_small_glitch", "pulsar_glitch_spin_up", 1.0e-9, "fraction", "Espinoza catalog small-glitch floor"),
        ("b1737_interval_yr", "pulsar_glitch_interval", 0.33, "yr", "PSR B1737-30 frequent glitches"),
        ("crab_interval_1yr", "pulsar_glitch_interval", 1.0, "yr", "Crab inter-glitch class"),
        ("j0537_rate_per_yr", "pulsar_glitch_frequency", 3.0, "1/yr", "PSR J0537-6910 glitch rate"),
        ("b1338_interval_yr", "pulsar_glitch_interval", 0.5, "yr", "PSR B1338-62 glitch class"),
        ("magnetar_dnu", "pulsar_glitch_spin_up", 1.0e-5, "fraction", "Magnetar glitch amplitude class"),
        ("espinoza_mean_interval", "pulsar_glitch_interval", 2.0, "yr", "Espinoza+ 2011 mean interval"),
        ("vela_recovery_days", "pulsar_glitch_recovery_d", 30.0, "d", "Vela exponential recovery class"),
        ("b1919_period_s", "pulsar_period_s", 1.337, "s", "PSR B1919+21 period"),
        ("j0348_period_s", "pulsar_period_s", 0.0391, "s", "PSR J0348+0432 period"),
        ("ipta_n_pulsars", "pulsar_timing_array_n", 65.0, "count", "IPTA pulsar count class"),
        ("crab_period_ms", "pulsar_period_ms", 33.4, "ms", "Crab pulsar period"),
        ("vela_period_ms", "pulsar_period_ms", 89.3, "ms", "Vela pulsar period"),
    ],
}


def main() -> int:
    ref = json.loads(REFERENCE.read_text(encoding="utf-8"))
    added_total = 0
    for law_id, extras in EXTRA.items():
        have = {a["name"] for a in ref["panels"][law_id]["anchors"]}
        for name, prop, measured, unit, citation in extras:
            if name in have:
                continue
            if name.startswith(" "):
                continue
            ref["panels"][law_id]["anchors"].append(
                {
                    "name": name.strip(),
                    "property": prop,
                    "measured": measured,
                    "unit": unit,
                    "reference": citation,
                    "source_note": "public literature named in founding archive (I:/fsuft aasb)",
                }
            )
            have.add(name.strip())
            added_total += 1
    ref["updated"] = datetime.now(timezone.utc).date().isoformat()
    ref["policy"] = (
        "Published literature anchors only — founding-era accuracy claims are not trusted "
        "until FSOT 2.1 panel verification. Extra rows are the public catalogs the "
        "I:/fsuft aasb archive was pointing at, not FSUFT 4.2/8.7 chat numbers."
    )
    REFERENCE.write_text(json.dumps(ref, indent=2), encoding="utf-8")

    results = []
    for law_id, (domain, filename) in DOMAIN_SLUG.items():
        doc = BUILDERS[domain]()
        path = output_path(domain)
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        rec = int(doc.get("record_count") or 0)
        med = doc.get("pooled_median_error_pct")
        results.append(
            {
                "law": law_id,
                "domain": domain,
                "records": rec,
                "median": med,
                "tier": _tier(float(med) if med is not None else None, rec),
                "file": filename,
            }
        )
        print(f"  {law_id} {domain:42s} n={rec:3d} med={med} {_tier(float(med) if med is not None else None, rec)}")

    out = ROOT / "results" / "verification" / "founding_archive_fill.json"
    out.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "added_anchors": added_total,
                "policy": "archive-cited public literature only; no chat-era 71.98 pads",
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out} (+{added_total} anchors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
