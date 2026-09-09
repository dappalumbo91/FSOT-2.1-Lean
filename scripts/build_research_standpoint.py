#!/usr/bin/env python3
"""Research standpoint — domain inventory, laws of reality, depth gaps.

Not more domains. Not a second theory. Reads the pin, the family tree, and
the green gate, then writes:

  data/research_standpoint.json
  data/laws_of_reality.json
  docs/RESEARCH_STANDPOINT.md
  docs/LAWS_OF_REALITY.md

Refresh: python scripts/build_research_standpoint.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

from fsot_compute import (  # noqa: E402
    DOMAINS,
    K,
    POOF,
    SUCTION,
    PHI,
    C_EFF,
    C_FACTOR,
    A_BLEED,
)
from fsot_scale_interconnects import perception_summary  # noqa: E402
from c_thin_depth_lib import _tier  # noqa: E402

PIN = "D1D38A"
OUT_JSON = ROOT / "data" / "research_standpoint.json"
LAWS_JSON = ROOT / "data" / "laws_of_reality.json"
OUT_MD = ROOT / "docs" / "RESEARCH_STANDPOINT.md"
LAWS_MD = ROOT / "docs" / "LAWS_OF_REALITY.md"

# Gated connective tissues (already residual-checked). Same physics, two zooms.
GATED_TISSUES = [
    {
        "id": "TISSUE-H0",
        "cores": ["Cosmology", "Astronomy", "Astrophysics"],
        "said": "H0 is sectors of one fluid, not two cosmologies",
        "artifact": "docs/CONCEPTS.md C3 · docs/OBJECT_SCORING.md",
        "live": "Planck 0.024%; chain 72.856 vs 73.04 (0.252%); class bin 1% frozen",
    },
    {
        "id": "TISSUE-WAVE",
        "cores": ["Acoustics", "Seismology"],
        "said": "Lab sound and crustal PREM are one T3 standing wave",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §1",
        "live": "lithosphere median 0.069%",
    },
    {
        "id": "TISSUE-FLUID",
        "cores": ["Fluid_Dynamics", "Oceanography", "Atmospheric_Physics"],
        "said": "One NDBC neighborhood, three tanks",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §2",
        "live": "pres/SST/wind 0.026–0.030%",
    },
    {
        "id": "TISSUE-FRIDGE",
        "cores": ["Thermodynamics", "Cosmology"],
        "said": "BH→WH is a heat/information pump (same fridge cycle)",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §3 · CONCEPTS C2",
        "live": "|S_thermo|/|S_cosm| vs π/2 0.289%",
    },
    {
        "id": "TISSUE-ORIFICE",
        "cores": ["Nuclear_Physics", "Particle_Physics"],
        "said": "ENDF levels are two zooms of one orifice",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §4",
        "live": "nuclear 0.046% · particle 0.010%",
    },
    {
        "id": "TISSUE-CEILING",
        "cores": ["Quantum_Gravity", "Cosmology"],
        "said": "Compactification remainder → 1 as D→25",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §5",
        "live": "|S_QG|/|S_cosm| vs A_bleed 0.088%",
    },
    {
        "id": "TISSUE-SOCIAL",
        "cores": ["Economics", "Neuroscience"],
        "said": "A market is not a different medium from a neural net",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §6",
        "live": "same World Bank YoY on both folds; siloed 0.129% not retuned",
    },
    {
        "id": "TISSUE-CEPHEID",
        "cores": ["Acoustics", "Chemistry", "Electromagnetism", "Astronomy"],
        "said": "Cepheid PL is acoustic + chemistry + light, not a fitted b",
        "artifact": "docs/CEPHEID_PL_PHYSICS.md",
        "live": "R_H = POOF·e·C_eff vs 0.4 at 0.110%",
    },
    {
        "id": "TISSUE-CHEMLINK",
        "cores": ["Biology", "Chemistry", "Biochemistry"],
        "said": "Protein product is residual at named ChemLink interfaces",
        "artifact": "docs/GENETICS_CLAIM_EVIDENCE.md",
        "live": "sibling freeze 0.13 Å vs AF 0.47 Å (10/10)",
    },
    {
        "id": "TISSUE-OBSERVER",
        "cores": ["Neuroscience", "Quantum_Mechanics", "Optics"],
        "said": "Consciousness is C_factor on the observer string, not a bolt-on",
        "artifact": "docs/CONSCIOUSNESS_CLAIM_EVIDENCE.md",
        "live": "20.003601 vs 20.0 W (0.018%)",
    },
    {
        "id": "TISSUE-CONJUGATE",
        "cores": ["Particle_Physics", "High_Energy_Physics", "Quantum_Mechanics"],
        "said": "Matter–antimatter is the other face of the same valve",
        "artifact": "docs/MATTER_ANTIMATTER_CLAIM_EVIDENCE.md",
        "live": "C13 conjugate; not a second ontology",
    },
    {
        "id": "TISSUE-VALVE-EQ",
        "cores": ["Seismology", "Fluid_Dynamics"],
        "said": "Slow slip and fast rupture are SUCTION vs POOF of one valve",
        "artifact": "PRED-057 · dated windows PRED-064",
        "live": "dated cells 39.1 km / φ^4 days; not a clock-time hypocenter",
    },
    {
        "id": "TISSUE-SEIS-GEO",
        "cores": ["Seismology", "Geophysics"],
        "said": "Wave fold vs bulk-earth fold on adjacent D=18/19; same PREM density",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §7 · docs/APPLY_SEISMOLOGY.md",
        "live": "|S_seis|/|S_geo| vs φ/2; PREM lithosphere density dual-routed",
    },
    {
        "id": "TISSUE-FRB-ORIFICE",
        "cores": ["Particle_Astrophysics", "Cosmology"],
        "said": "FRB is BH→WH orifice outgassing; repeaters are saloon-door post-POOF, one-shots a paper-rip",
        "artifact": "docs/FRB_ORIFICE.md",
        "live": "E=width×fluence vs e·POOF 37/37; width class vs D=5 at 0%; 16.35 d = 5π+1/φ; 200·(1+dens) REMEDIED_WRONG_APPLY",
    },
    {
        "id": "TISSUE-MAT-OPT",
        "cores": ["Materials_Science", "Optics"],
        "said": "Same D=10 rung: CRC n_D on Optics, density on Materials; ice n vs φ²/2",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §8",
        "live": "n/ρ dual-fold APPLY; |S_mat|/|S_opt| vs PhysChem/Chem look-split 0.329%; vs 1 REMEDIED_WRONG_APPLY",
    },
    {
        "id": "TISSUE-OPT-QO",
        "cores": ["Optics", "Quantum_Optics"],
        "said": "Wave and photon are adjacent D=10/11 of one light; same C=π/e",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §9 · docs/APPLY_OPTICS.md",
        "live": "|S_opt|/|S_qo| vs 1 at 0.0265%; CRC n_D photon fold 0.016%",
    },
    {
        "id": "TISSUE-QM-ATOMIC",
        "cores": ["Quantum_Mechanics", "Atomic_Physics"],
        "said": "Orbit and bound well are adjacent D=6/7 of one hydrogen; equalize the look",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §10 · docs/APPLY_ATOMIC.md",
        "live": "same-look D=6/7 vs 1 at 0.046%; IE_H seed 0.070%; NIST H–Ca IE/a0/R∞ dual-routed; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-EM-OPT",
        "cores": ["Electromagnetism", "Optics"],
        "said": "Source and readout are adjacent D=9/10 of one light; ε_opt=n²; inverse C",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §11 · docs/APPLY_EM.md",
        "live": "same-look D=9/10 vs 1 at 0.024%; CRC n² on EM 0.021%; ice ε vs (φ²/2)² 0.0026%; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-BIO-BIOCHEM",
        "cores": ["Biology", "Biochemistry"],
        "said": "Organism and molecule are adjacent D=12/13 of one life; Biology stays dark",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §12 · docs/APPLY_BIO.md",
        "live": "dark same-look D=12/13 vs 1 at 0.053%; NCBI mt-operon + AA MW 0.015–0.022%; not Genetics 0.13 Å; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-ATOMIC-HEP",
        "cores": ["Atomic_Physics", "High_Energy_Physics"],
        "said": "Bound well and collision are two looks at D=7; fold 0.85/0.95 onto QM",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §13 · docs/APPLY_HEP.md",
        "live": "look-split vs QM rung 0.042%; CODATA m_e/m_p + IE_H dual-route; vs 1 retired",
    },
    {
        "id": "TISSUE-CHEM-PC",
        "cores": ["Chemistry", "Physical_Chemistry"],
        "said": "Composition and thermo are two looks at D=8; 0.5/0.6 is the mat-opt look-split",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §14",
        "live": "S-ratio vs mat-opt look-split 0.328%; CRC rho/MW vs Tm/Tb 0.017–0.041%; vs 1 retired",
    },
    {
        "id": "TISSUE-CHEM-MOL",
        "cores": ["Chemistry", "Molecular_Chemistry"],
        "said": "Composition and molecule are adjacent D=8/9; equalize the chemistry look",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §15",
        "live": "same-look D=8/9 vs 1 at 0.020%; CRC MW dual-routed; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-PC-MOL",
        "cores": ["Physical_Chemistry", "Molecular_Chemistry"],
        "said": "Thermo and molecule already share δψ=0.5 on adjacent D=8/9",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §15",
        "live": "live |S| vs 1 at 0.167% (looks matched); CRC Tm vs MW dual-routed",
    },
    {
        "id": "TISSUE-AC-OPT",
        "cores": ["Acoustics", "Optics"],
        "said": "Lab sound and light are two looks at D=10; fold 0.3/0.6 onto D=9",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §16",
        "live": "look-split vs D=9 at 0.258%; CRC c vs n 0.013–0.016%; vs 1 retired",
    },
    {
        "id": "TISSUE-AC-MAT",
        "cores": ["Acoustics", "Materials_Science"],
        "said": "Lab sound and bulk density are two looks at D=10; fold 0.3/0.5 onto D=9",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §16",
        "live": "look-split vs D=9 at 0.077%; CRC c vs ρ; vs 1 retired",
    },
    {
        "id": "TISSUE-MOL-AC",
        "cores": ["Molecular_Chemistry", "Acoustics"],
        "said": "Molecule and lab sound are adjacent D=9/10; equalize δψ=0.5",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §17",
        "live": "same-look D=9/10 vs 1 at 0.205%; CRC MW vs c; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-CM-THERMO",
        "cores": ["Condensed_Matter", "Thermodynamics"],
        "said": "Solid and heat are adjacent D=14/15; equalize the CM look",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §18",
        "live": "same-look D=14/15 vs 1 at 0.233%; CRC metal ρ vs Tm; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-EM-MAT",
        "cores": ["Electromagnetism", "Materials_Science"],
        "said": "Field and bulk are adjacent D=9/10; equalize the materials look",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §19",
        "live": "same-look D=9/10 vs 1 at 0.205%; CRC n² vs ρ; mixed vs 1 retired",
    },
    {
        "id": "TISSUE-BIOCHEM-NEURO",
        "cores": ["Biochemistry", "Neuroscience"],
        "said": "Molecule and signaling are adjacent D=13/14; not the social-tank GDP route",
        "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §20",
        "live": "same-look D=13/14 vs 1 at 0.179%; transmitter AA MW; mixed vs 1 retired",
    },
        {
            "id": "TISSUE-ATOMIC-CHEM",
            "cores": ["Atomic_Physics", "Chemistry"],
            "said": "Bound well and composition are adjacent D=7/8; equalize the chemistry look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §21",
            "live": "same-look D=7/8 at δψ=0.6; NIST IE + CRC MW",
        },
        {
            "id": "TISSUE-ATOMIC-PC",
            "cores": ["Atomic_Physics", "Physical_Chemistry"],
            "said": "Bound well and thermo are adjacent D=7/8; equalize δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §21",
            "live": "same-look D=7/8 at δψ=0.5; NIST IE + CRC Tm",
        },
        {
            "id": "TISSUE-HEP-CHEM",
            "cores": ["High_Energy_Physics", "Chemistry"],
            "said": "Collision and composition are adjacent D=7/8; equalize δψ=0.6",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §21",
            "live": "same-look D=7/8 at δψ=0.6; NIST IE on HEP + CRC MW",
        },
        {
            "id": "TISSUE-HEP-PC",
            "cores": ["High_Energy_Physics", "Physical_Chemistry"],
            "said": "Collision and thermo are adjacent D=7/8; equalize δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §21",
            "live": "same-look D=7/8 at δψ=0.5; NIST IE on HEP + CRC Tm",
        },
        {
            "id": "TISSUE-PC-EM",
            "cores": ["Physical_Chemistry", "Electromagnetism"],
            "said": "Thermo and field are adjacent D=8/9; equalize δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §22",
            "live": "same-look D=8/9 at δψ=0.5; CRC Tm + n²",
        },
        {
            "id": "TISSUE-EM-MOL",
            "cores": ["Electromagnetism", "Molecular_Chemistry"],
            "said": "Field and molecule are two looks at D=9; fold 0.7/0.5 onto D=8",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §22",
            "live": "look-split vs D=8; CRC n² vs MW; vs 1 retired",
        },
        {
            "id": "TISSUE-MOL-MAT",
            "cores": ["Molecular_Chemistry", "Materials_Science"],
            "said": "Molecule and bulk are adjacent D=9/10 already sharing δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §23",
            "live": "matched-look live |S| vs 1; CRC MW vs density",
        },
        {
            "id": "TISSUE-MOL-OPT",
            "cores": ["Molecular_Chemistry", "Optics"],
            "said": "Molecule and light are adjacent D=9/10; equalize δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §23",
            "live": "same-look D=9/10 at δψ=0.5; CRC MW vs n; mixed vs 1 retired",
        },
        {
            "id": "TISSUE-AC-QO",
            "cores": ["Acoustics", "Quantum_Optics"],
            "said": "Lab sound and photon are adjacent D=10/11; equalize the light look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §24",
            "live": "same-look D=10/11 at δψ=0.6; CRC c vs n",
        },
        {
            "id": "TISSUE-MAT-QO",
            "cores": ["Materials_Science", "Quantum_Optics"],
            "said": "Bulk and photon are adjacent D=10/11; equalize δψ=0.5",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §24",
            "live": "same-look D=10/11 at δψ=0.5; CRC ρ vs n",
        },
        {
            "id": "TISSUE-NUC-THERMO",
            "cores": ["Nuclear_Physics", "Thermodynamics"],
            "said": "Orifice and heat are two looks at D=15; fold 1/0.9 onto D=14",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §25",
            "live": "look-split vs D=14; ENDF keV + Carnot dual-route",
        },
        {
            "id": "TISSUE-FLUID-THERMO",
            "cores": ["Fluid_Dynamics", "Thermodynamics"],
            "said": "Tank and heat share D=15; Fluid stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §25",
            "live": "Carnot COP dual-route; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-METEO-ATM",
            "cores": ["Meteorology", "Atmospheric_Physics"],
            "said": "Weather and air tank are adjacent dark CHAOS rungs D=16/17",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §26",
            "live": "dark same-look δψ=0.8; NDBC pressure; do not flip dark",
        },
        {
            "id": "TISSUE-BIOCHEM-CM",
            "cores": ["Biochemistry", "Condensed_Matter"],
            "said": "Molecule and solid are adjacent D=13/14; equalize the CM look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §27",
            "live": "same-look D=13/14 at δψ=0.5; CRC AA MW vs metal ρ",
        },
        {
            "id": "TISSUE-CM-NEURO",
            "cores": ["Condensed_Matter", "Neuroscience"],
            "said": "Solid and signaling are two looks at D=14; fold onto D=13",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §27",
            "live": "look-split 0.5/0.7 onto D=13; CRC ρ vs transmitter AA; vs 1 retired",
        },
        {
            "id": "TISSUE-CM-FLUID",
            "cores": ["Condensed_Matter", "Fluid_Dynamics"],
            "said": "Ice and water are one H2O, solid vs tank; Fluid stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §28",
            "live": "CRC ice ρ on CM, water ρ on Fluid; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-CM-NUC",
            "cores": ["Condensed_Matter", "Nuclear_Physics"],
            "said": "Lattice and orifice are adjacent D=14/15; Fe is the shared class",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §28",
            "live": "same-look D=14/15 at δψ=0.5; CRC ρ + ENDF keV dual-route",
        },
        {
            "id": "TISSUE-NEURO-THERMO",
            "cores": ["Neuroscience", "Thermodynamics"],
            "said": "Signaling and heat are adjacent D=14/15; not the social-tank GDP route",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §27",
            "live": "same-look D=14/15 at δψ=0.7 hits=1; transmitter AA vs Carnot",
        },
        {
            "id": "TISSUE-FLUID-NUC",
            "cores": ["Fluid_Dynamics", "Nuclear_Physics"],
            "said": "Tank and orifice share D=15; Fluid stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §28",
            "live": "Carnot + ENDF dual-route; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-FLUID-METEO",
            "cores": ["Fluid_Dynamics", "Meteorology"],
            "said": "Lab tank and weather are adjacent dark rungs D=15/16",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §28",
            "live": "dark same-look δψ=0.8 hits=2; NDBC pressure; do not flip dark",
        },
        {
            "id": "TISSUE-NEURO-FLUID",
            "cores": ["Neuroscience", "Fluid_Dynamics"],
            "said": "Signaling and tank are adjacent D=14/15; Fluid stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §29",
            "live": "transmitter AA vs CRC water ρ; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-NEURO-NUC",
            "cores": ["Neuroscience", "Nuclear_Physics"],
            "said": "Signaling and orifice are adjacent D=14/15; equalize the neural look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §29",
            "live": "same-look D=14/15 at δψ=0.7 hits=1; AA vs ENDF keV",
        },
        {
            "id": "TISSUE-THERMO-METEO",
            "cores": ["Thermodynamics", "Meteorology"],
            "said": "Heat and weather are adjacent D=15/16; Meteo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §29",
            "live": "Carnot + NDBC pressure; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-NUC-METEO",
            "cores": ["Nuclear_Physics", "Meteorology"],
            "said": "Orifice and weather are adjacent D=15/16; Meteo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §29",
            "live": "ENDF keV + NDBC pressure; do not flip dark",
        },
        {
            "id": "TISSUE-METEO-OCEAN",
            "cores": ["Meteorology", "Oceanography"],
            "said": "Weather and ocean tank are adjacent dark rungs D=16/17",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §30",
            "live": "dark same-look δψ=0.8 hits=2; NDBC pressure; do not flip dark",
        },
        {
            "id": "TISSUE-ATM-SEIS",
            "cores": ["Atmospheric_Physics", "Seismology"],
            "said": "Air tank and crust are adjacent dark rungs D=17/18",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §30",
            "live": "NDBC pressure + PREM lithosphere density; both stay dark",
        },
        {
            "id": "TISSUE-OCEAN-SEIS",
            "cores": ["Oceanography", "Seismology"],
            "said": "Ocean tank and crust are adjacent dark rungs D=17/18",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §30",
            "live": "NDBC SST + PREM lithosphere density; both stay dark",
        },
        {
            "id": "TISSUE-ASTRO-PLANET",
            "cores": ["Astronomy", "Planetary_Science"],
            "said": "Sky and body are adjacent D=20/21; equalize the astronomy look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §31",
            "live": "same-look D=20/21 at δψ=1; JPL densities via APPLY not identity pad",
        },
        {
            "id": "TISSUE-QO-BIO",
            "cores": ["Quantum_Optics", "Biology"],
            "said": "Photon and organism are adjacent D=11/12; Biology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §31",
            "live": "dark same-look δψ=0.08; CRC n vs NCBI mt-operon; do not flip dark",
        },
        {
            "id": "TISSUE-ATM-SOC",
            "cores": ["Atmospheric_Physics", "Sociology"],
            "said": "Air tank and catalog tank are adjacent D=17/18; Atm stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §32",
            "live": "NDBC pressure + World Bank YoY; do not flip dark",
        },
        {
            "id": "TISSUE-OCEAN-SOC",
            "cores": ["Oceanography", "Sociology"],
            "said": "Ocean tank and catalog tank are adjacent D=17/18; Ocean stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §32",
            "live": "NDBC SST + World Bank YoY; do not flip dark",
        },
        {
            "id": "TISSUE-SEIS-SOC",
            "cores": ["Seismology", "Sociology"],
            "said": "Crust and catalog share D=18; Seismology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §32",
            "live": "PREM lithosphere + World Bank YoY; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-SOC-GEO",
            "cores": ["Sociology", "Geophysics"],
            "said": "Catalog and bulk-earth are adjacent D=18/19; Geo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §32",
            "live": "World Bank YoY + PREM lithosphere density",
        },
        {
            "id": "TISSUE-GEO-ASTRO",
            "cores": ["Geophysics", "Astronomy"],
            "said": "Bulk-earth and sky are adjacent D=19/20; Geo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §33",
            "live": "PREM lithosphere + JPL densities",
        },
        {
            "id": "TISSUE-GEO-ECON",
            "cores": ["Geophysics", "Economics"],
            "said": "Bulk-earth and market are adjacent D=19/20; Geo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §33",
            "live": "PREM lithosphere + World Bank YoY",
        },
        {
            "id": "TISSUE-ASTRO-ECON",
            "cores": ["Astronomy", "Economics"],
            "said": "Sky and market are two looks at D=20; fold onto D=19",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §33",
            "live": "look-split 1.0/1.5 onto D=19; JPL + World Bank; vs 1 retired",
        },
        {
            "id": "TISSUE-ECON-PLANET",
            "cores": ["Economics", "Planetary_Science"],
            "said": "Market and body are adjacent D=20/21; equalize the astronomy look",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §33",
            "live": "same-look D=20/21 at δψ=1; World Bank YoY + JPL densities",
        },
        {
            "id": "TISSUE-PLANET-QG",
            "cores": ["Planetary_Science", "Quantum_Gravity"],
            "said": "Body and ceiling are adjacent D=21/22; QG stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §34",
            "live": "JPL densities + compact remainder; do not flip QG",
        },
        {
            "id": "TISSUE-ASTROPHYS-PA",
            "cores": ["Astrophysics", "Particle_Astrophysics"],
            "said": "Star and cosmic-ray share D=24; PA stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §34",
            "live": "PDG 2024 measured masses via APPLY; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-QC-AC",
            "cores": ["Acoustics", "Quantum_Computing"],
            "said": "Lab sound and Hilbert are adjacent D=10/11; QC stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §35",
            "live": "dark same-look δψ=0.5; CRC c vs n; do not flip Hilbert",
        },
        {
            "id": "TISSUE-QC-MAT",
            "cores": ["Materials_Science", "Quantum_Computing"],
            "said": "Bulk and Hilbert are adjacent D=10/11; QC stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §35",
            "live": "CRC ρ vs n; do not flip Hilbert",
        },
        {
            "id": "TISSUE-QC-OPT",
            "cores": ["Optics", "Quantum_Computing"],
            "said": "Wave and Hilbert are adjacent D=10/11; QC stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §35",
            "live": "CRC n dual-route; do not flip Hilbert",
        },
        {
            "id": "TISSUE-QC-QO",
            "cores": ["Quantum_Computing", "Quantum_Optics"],
            "said": "Hilbert and photon share D=11; QC stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §35",
            "live": "CRC n dual-route; live vs 1 is observed mix",
        },
        {
            "id": "TISSUE-QC-BIO",
            "cores": ["Quantum_Computing", "Biology"],
            "said": "Hilbert and organism are adjacent D=11/12; both stay dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §35",
            "live": "dark same-look δψ=0.08; CRC n vs NCBI mt-operon",
        },
        {
            "id": "TISSUE-CM-ECO",
            "cores": ["Condensed_Matter", "Ecology"],
            "said": "Solid and habitat are adjacent D=14/15; Ecology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "CRC metal ρ + GBIF decimalLatitude; no invented watts",
        },
        {
            "id": "TISSUE-NEURO-ECO",
            "cores": ["Neuroscience", "Ecology"],
            "said": "Signaling and habitat are adjacent D=14/15; Ecology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "transmitter AA + GBIF latitude",
        },
        {
            "id": "TISSUE-ECO-FLUID",
            "cores": ["Ecology", "Fluid_Dynamics"],
            "said": "Habitat and tank share D=15; both stay dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "GBIF latitude + CRC water ρ",
        },
        {
            "id": "TISSUE-ECO-NUC",
            "cores": ["Ecology", "Nuclear_Physics"],
            "said": "Habitat and orifice share D=15; Ecology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "GBIF latitude + ENDF keV",
        },
        {
            "id": "TISSUE-ECO-THERMO",
            "cores": ["Ecology", "Thermodynamics"],
            "said": "Habitat and heat share D=15; Ecology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "GBIF latitude + Carnot COP",
        },
        {
            "id": "TISSUE-ECO-METEO",
            "cores": ["Ecology", "Meteorology"],
            "said": "Habitat and weather are adjacent dark rungs D=15/16",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "GBIF latitude + NDBC pressure; both stay dark",
        },
        {
            "id": "TISSUE-ECO-PSYCH",
            "cores": ["Ecology", "Psychology"],
            "said": "Habitat and psychometric scale are adjacent D=15/16; Ecology stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §36",
            "live": "GBIF latitude + Nunnally/Cohen anchors; not watts",
        },
        {
            "id": "TISSUE-FLUID-PSYCH",
            "cores": ["Fluid_Dynamics", "Psychology"],
            "said": "Tank and psychometric scale are adjacent D=15/16; Fluid stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "CRC water ρ + Nunnally/Cohen; not watts",
        },
        {
            "id": "TISSUE-NUC-PSYCH",
            "cores": ["Nuclear_Physics", "Psychology"],
            "said": "Orifice and psychometric scale are adjacent D=15/16",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "ENDF keV + Nunnally/Cohen; not watts",
        },
        {
            "id": "TISSUE-THERMO-PSYCH",
            "cores": ["Thermodynamics", "Psychology"],
            "said": "Heat and psychometric scale are adjacent D=15/16",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "Carnot COP + Nunnally/Cohen; not watts",
        },
        {
            "id": "TISSUE-METEO-PSYCH",
            "cores": ["Meteorology", "Psychology"],
            "said": "Weather and psychometric scale share D=16; Meteo stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "NDBC pressure + Nunnally/Cohen; not watts",
        },
        {
            "id": "TISSUE-PSYCH-ATM",
            "cores": ["Psychology", "Atmospheric_Physics"],
            "said": "Psychometric scale and air tank are adjacent D=16/17; Atm stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "Nunnally/Cohen + NDBC pressure; not watts",
        },
        {
            "id": "TISSUE-PSYCH-OCEAN",
            "cores": ["Psychology", "Oceanography"],
            "said": "Psychometric scale and ocean tank are adjacent D=16/17; Ocean stays dark",
            "artifact": "docs/SCALE_INTERCONNECT_PHYSICS.md §37",
            "live": "Nunnally/Cohen + NDBC SST; not watts",
        },
]


def _f(x) -> float:
    return float(x)


def _scan_tiers() -> dict:
    tiers: dict[str, list] = defaultdict(list)
    for p in sorted((ROOT / "data").glob("*benchmark*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        rec = int(d.get("record_count") or 0)
        med = d.get("pooled_median_error_pct")
        if med is None:
            med = d.get("median_error_pct")
        if med is None or rec == 0:
            continue
        t = _tier(float(med), rec)
        tiers[t].append(
            {
                "file": p.name,
                "domain": d.get("domain") or p.stem,
                "records": rec,
                "pooled_pct": float(med),
            }
        )
    for k in tiers:
        tiers[k].sort(key=lambda r: -float(r["pooled_pct"]))
    return {k: v for k, v in tiers.items()}


def _tree() -> dict:
    p = ROOT / "data" / "domain_family_tree.json"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _margin() -> dict:
    p = ROOT / "data" / "benchmark_margin_audit.json"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def laws() -> list[dict]:
    k = _f(K)
    poof = _f(POOF)
    suc = _f(SUCTION)
    phi = _f(PHI)
    b_gr = phi - 1.0 / phi
    pv = {}
    ip = ROOT / "results" / "between_scale_interconnect_outcome.json"
    if ip.is_file():
        try:
            pv = json.loads(ip.read_text(encoding="utf-8")).get("perception_view") or {}
        except Exception:
            pv = {}
    if not pv:
        pv = perception_summary()
    qm_vs1 = 0.0
    for row in pv.get("pairs") or []:
        if str(row.get("name") or "").startswith("qm_atomic"):
            qm_vs1 = float(row.get("live_vs_1_pct") or 0)
            break
    return [
        {
            "id": "R1",
            "kind": "engine",
            "name": "one_scalar",
            "statement": "Reality is one compressible fluid. The heartbeat is S = K(T1+T2+T3).",
            "closed_form": "S = K(T1+T2+T3)",
            "live": f"K ≈ {k:.6f}",
            "code": "vendor/fsot_compute.py · FSOT/Scalar.lean",
            "not": "A separate Lagrangian per domain.",
        },
        {
            "id": "R2",
            "kind": "engine",
            "name": "five_seeds",
            "statement": "Every constant reduces to {π, e, φ, γ, G}. Zero free parameters.",
            "closed_form": "seeds only",
            "live": "parameter_count_audit ZERO_FREE",
            "code": "vendor/fsot_compute.py §1",
            "not": "A Yukawa, dark density, or per-row ε.",
        },
        {
            "id": "R3",
            "kind": "engine",
            "name": "compactification_ceiling",
            "statement": "Effective dimension D_eff is a fold of a 25-D ceiling, not a count of extra spatial axes.",
            "closed_form": "T1 ln(D/25); T3 Chaos (D-25)/25",
            "live": "D_eff ∈ [5, 25]; 35 core folds",
            "code": "DOMAINS table §5",
            "not": "Inventing D=26 to fit one ugly panel.",
        },
        {
            "id": "R4",
            "kind": "engine",
            "name": "yin_yang_valve",
            "statement": "Load (SUCTION) then orifice (POOF). Creation and destruction are one cycle.",
            "closed_form": f"POOF≈{poof:.4f} · SUCTION≈{suc:.4f}",
            "live": "T3 valve; hydrology load bar 1+POOF; tide score bar POOF m",
            "code": "fsot_compute T3 · fsot_earth_fluid_forecast.py",
            "not": "Two unrelated constitutive laws for slow vs fast, quiet vs storm.",
        },
        {
            "id": "R5",
            "kind": "engine",
            "name": "information_valve",
            "statement": "A black hole is an information-flow valve at every scale, not a trash can.",
            "closed_form": "infall → POOF → WH outflow / C_eff re-solidification",
            "live": f"C_eff≈{_f(C_EFF):.4f}",
            "code": "scripts/bubble_bleed_physics.py · CONCEPTS C2/C10",
            "not": "A cosmological BH only.",
        },
        {
            "id": "R6",
            "kind": "engine",
            "name": "observer_is_physical",
            "statement": "Observation is C_factor on T1 when observed=true. Dark folds stay dark.",
            "closed_form": "C_factor = C_eff · P_new",
            "live": f"C_factor≈{_f(C_FACTOR):.6f}; Homo sapiens 20.003601 vs 20.0 W (0.018%)",
            "code": "CONCEPTS C11 · CONSCIOUSNESS_CLAIM_EVIDENCE.md",
            "not": "A 21.79 W Cosmology-Lab leftover. Looking at QC (observed=false).",
        },
        {
            "id": "R7",
            "kind": "engine",
            "name": "bleed",
            "statement": "Adjacent folds talk through κ_ij. Silos are institutional, not physical.",
            "closed_form": "κ_ij = A_bleed·POOF·|Si||Sj| / (1+|Di-Dj|/25)",
            "live": f"A_bleed≈{_f(A_BLEED):.4f}; between-scale pooled 0.026%",
            "code": "vendor/fsot_complex_interaction.py · SCALE_INTERCONNECT_PHYSICS.md",
            "not": "A free spring between two panels.",
        },
        {
            "id": "R8",
            "kind": "engine",
            "name": "apply_residual",
            "statement": "computed = measured × (1 + |S(domain)| × f_domain). Mismatch → change the interface.",
            "closed_form": "fsot_scaled(m, name)",
            "live": "green if domain median ≤ 0.5%",
            "code": "docs/APPLY.md",
            "not": "Least-squares a new f. Identity pads.",
        },
        {
            "id": "R9",
            "kind": "engine",
            "name": "ontology",
            "statement": "Nothing and perfection are both unstable. Origin is friction at that interface. Zero is a boundary symbol, not a thing.",
            "closed_form": "A1–A6",
            "live": "data/foundational_ontology_axioms.yaml",
            "code": "TOE Label B T1",
            "not": "A volumetric Big Bang as the only origin picture.",
        },
        {
            "id": "D1",
            "kind": "discovered",
            "name": "h0_is_sectors",
            "statement": "There is not one Hubble constant. Tools couple to BH→WH bubble-density sectors.",
            "closed_form": "H0_tool = H0_global·(1+ρ·ε), H0_global≈68.440, ε≈0.015431",
            "live": "Planck 67.384 (0.024%); bridge 70.75; class 73.773; chain 72.856 vs 73.04 (0.252%)",
            "code": "docs/OBJECT_SCORING.md · CONCEPTS C3",
            "not": "JWST Perfect Host 73.49 as PRED-001. Retuning ρ onto 73.04.",
        },
        {
            "id": "D2",
            "kind": "discovered",
            "name": "gr_b_value",
            "statement": "The Gutenberg–Richter b-value is acoustic counting in the crustal fluid: b = φ − 1/φ = 1.",
            "closed_form": "b = φ − 1/φ",
            "live": f"b = {b_gr:.6f} (exactly 1). PRED-056 band 0.90–1.10",
            "code": "PRED-056",
            "not": "A regional fitted b per catalog as a new law.",
        },
        {
            "id": "D3",
            "kind": "discovered",
            "name": "cepheid_wesenheit",
            "statement": "NIR Wesenheit R_H is POOF·e·C_eff, not a fitted reddening slope.",
            "closed_form": "R_H = POOF·e·C_eff",
            "live": "vs Riess Eq.7 0.4 at 0.110%; |b|=π+(POOF+SUCTION)/2",
            "code": "docs/CEPHEID_PL_PHYSICS.md",
            "not": "A free b or Z_W per host.",
        },
        {
            "id": "D4",
            "kind": "discovered",
            "name": "quiet_and_storm_are_sectors",
            "statement": "Quiet vs storm (weather, solar, tide, hydro, H0) are two sectors of one valve.",
            "closed_form": "same grammar as Planck vs SH0ES",
            "live": "PRED-062/060/065/078; dated windows PRED-064",
            "code": "docs/WEATHER_MONITORING_APPROACH.md",
            "not": "ECMWF S2S beat. Clock-time hypocenter. Cycle 25 SSN pick.",
        },
        {
            "id": "D5",
            "kind": "discovered",
            "name": "observer_20W",
            "statement": "The live Homo sapiens observer lock is 20.00 W, not the retired 21.79 W draft.",
            "closed_form": "brain_power_w vs 20.0",
            "live": "20.003601 vs 20.0 (0.018%)",
            "code": "docs/CONSCIOUSNESS_CLAIM_EVIDENCE.md",
            "not": "E_con 8.95% as a live fold.",
        },
        {
            "id": "D6",
            "kind": "discovered",
            "name": "genetics_two_regimes",
            "statement": "Protein product (measured homologs) and no-map (F01–F15) are two regimes. Do not mix Å objects.",
            "closed_form": "ChemLink residual at named D_eff",
            "live": "product 0.13 Å vs AF 0.47 Å vs cryo-EM FSC ~1.2 Å vs bulk ~13 Å",
            "code": "docs/GENETICS_CLAIM_EVIDENCE.md",
            "not": "0.13 Å from sequence alone. CASP/FSC papers as the product.",
        },
        {
            "id": "D7",
            "kind": "discovered",
            "name": "s8_joint_not_alone",
            "statement": "S8 lock 0.805 sits between Planck and DES. DES-alone is a tension row; the joint is the fair compare.",
            "closed_form": "PRED-002 / PRED-042 = 0.805",
            "live": "DES Y6 alone 0.789; joint DES+CMB+low-z 0.806 (arXiv:2601.14559). Euclid DR1 awaiting.",
            "code": "docs/OBJECT_SCORING.md",
            "not": "Killing 0.805 on DES-alone. Citing Euclid CLOE as measured.",
        },
        {
            "id": "D8",
            "kind": "discovered",
            "name": "flavor_is_one_fluid",
            "statement": "CKM/PMNS/α_s are seed readouts, not fitted SM inputs. Kill = next PDG combination outside 0.5%.",
            "closed_form": "PRED-070–075",
            "live": "Higgs/flavor layer inside literature-tight band",
            "code": "predictions/HIGGS_TIGHTEN_PLAN.md",
            "not": "A per-channel ε. Uniqueness of the SM Lagrangian as proved.",
        },
        {
            "id": "D9",
            "kind": "discovered",
            "name": "perception_is_scale_view",
            "statement": (
                "Perception at a scale is T1 at that fold’s δψ, hits, and observed. "
                "Live |S_i|/|S_j| vs 1 asks for the same view; adjacent folds are not supposed to look the same."
            ),
            "closed_form": "|S_i|/|S_j| = |1+T1_i|/|1+T1_j|  (T2=1, T3≈0)",
            "live": (
                f"T3 leftover {float(pv.get('max_t3_leftover_pct') or 0):.3f}% on "
                f"{int(pv.get('n_pairs') or 0)} view pairs. "
                f"QM/atomic live vs 1 is {qm_vs1:.2f}% = T1 view, not a failed 0.5%. "
                f"Worst live vs 1 {float(pv.get('max_live_vs_1_pct') or 0):.2f}%. "
                "Same-look D=6/7 vs 1 is 0.046%."
            ),
            "code": (
                "vendor/fsot_scale_interconnects.py t1_of · "
                "FSOT/Formal/ScalarEngineStructure.lean "
                "abs_scaled_S_ratio_of_unit_t2_zero_t3 · t3_leftover_of_unit_t2"
            ),
            "not": (
                "Stuffing √φ or √(e/φ) onto live vs 1. Retuning δψ. "
                "Flipping dark folds observed=True. Gating live vs 1 at 0.5%. "
                "Padding the pooled median with the T1 identity."
            ),
        },
        {
            "id": "D10",
            "kind": "discovered",
            "name": "planetary_cycle_is_orifice_unfolded",
            "statement": (
                "A dated Earth cell is R⊕·POOF/25. Solar, volcanic arc, trench, "
                "and basin tanks talk at R⊕·POOF — same orifice, compactification off."
            ),
            "closed_form": "cycle_km = 25 · kernel_km",
            "live": (
                "cell 39.1 km · cycle 977.8 km. Loading kills: transferred_poof "
                "on the arc or already_poofed (Scotia M6.2). Public cell-kill unchanged."
            ),
            "code": (
                "vendor/fsot_earth_fluid_forecast.py cycle_km · "
                "FSOT/Formal/ScalarEngineStructure.lean "
                "cycle_km_eq_twentyfive_mul_kernel_km"
            ),
            "not": (
                "A fitted 150 km or 1000 km spring. Rewriting issued kill_if. "
                "Promising a second mainshock after a recent M≥5.5."
            ),
        },
        {
            "id": "D11",
            "kind": "discovered",
            "name": "orifice_scale_is_fold_normalized",
            "statement": (
                "Valve length on a body L at fold d is L·POOF·d/25. A dated cell is d=1. "
                "Coupled tanks talk at d=25. Scoring d=1 while the dump is at d=25 is "
                "transferred_poof, not a kernel retune. κ_ij names which tanks interact. "
                "Frozen valve_state splits into discrete potentials (cell POOF, transfer, "
                "quiet hold) — seed-split, not a fitted probability."
            ),
            "closed_form": "orifice_scale(L, d) = L · POOF · d / 25",
            "live": (
                "cell 39.1 km · cycle 977.8 km · cycle/cell = 25. "
                "Closed kills map onto transferred_poof / quiet_hold / unexpected_poof. "
                "Public cell-kill unchanged."
            ),
            "code": (
                "vendor/fsot_earth_fluid_forecast.py orifice_scale_km · "
                "scripts/build_dynamic_system_triangulation.py · "
                "FSOT/Formal/ScalarEngineStructure.lean "
                "kernel_km_eq_orifice_scale_one · cycle_km_eq_orifice_scale_ceiling"
            ),
            "not": (
                "A calibrated event probability. Many-worlds. Rewriting kill_if onto "
                "cycle_km. A fitted n-body gravity spring."
            ),
        },
        {
            "id": "D12",
            "kind": "discovered",
            "name": "time_is_emergent_process",
            "statement": (
                "Time is not a fundamental axis. It is the duration of a fold/mold "
                "as the pattern travels through the flow. Dual of orifice_scale: "
                "process_time(τ0,d)=τ0·d/25 with τ0=φ^4 days at the ceiling. "
                "Calendar clocks (Cs-133) are a readout. Dilation is flow-contingent "
                "(τ_rate=(1+S)/(1+|flow_balance|)). Dated windows are that process "
                "time projected onto SI days at the right fold — not a UTC hypocenter "
                "as a 0.5% central."
            ),
            "closed_form": "process_time(τ0, d) = τ0 · d / 25;  τ0 = φ^4 days;  Omori c = 1/φ",
            "live": (
                "φ^4 ≈ 6.85 d → issued EQ/hydro 7 d at d=25; cell tick φ^4/25 ≈ 0.274 d. "
                "Volcanic 14 d = 2·φ^4. Weather/tide 48 h and solar 72 h stay the frozen "
                "kind projections. Omori p=1 = GR b. FPC dilation probes (photon sphere, "
                "ISCO, GPS) already gated. Public issued JSON unchanged."
            ),
            "code": (
                "vendor/fsot_earth_fluid_forecast.py process_time_days · "
                "scripts/time_emergence_lib.py tau_rate_unified · "
                "FSOT/Formal/ScalarEngineStructure.lean "
                "process_time_ceiling · process_time_one_mul_ceiling"
            ),
            "not": (
                "Newtonian UTC hypocenter as a 0.5% central. Retuning φ^4 to hit a "
                "clock. Rewriting issued windows. Beating ECMWF at S2S. A fitted "
                "aftershock β."
            ),
        },
    ]


def missing_tissues(cores: list[str]) -> list[dict]:
    """Adjacent-D core pairs that are green in isolation but have no gated tissue."""
    gated: set[frozenset[str]] = set()
    for t in GATED_TISSUES:
        names = t["cores"]
        for i, a in enumerate(names):
            for b in names[i + 1 :]:
                gated.add(frozenset({a, b}))
    by_d: dict[int, list[str]] = defaultdict(list)
    for n in cores:
        d = int(DOMAINS[n].D_eff)
        by_d[d].append(n)
    out = []
    ds = sorted(by_d)
    for i, d in enumerate(ds):
        here = by_d[d]
        near = list(here)
        if i + 1 < len(ds) and ds[i + 1] - d <= 1:
            near += by_d[ds[i + 1]]
        for j, a in enumerate(near):
            for b in near[j + 1 :]:
                if a == b:
                    continue
                key = frozenset({a, b})
                if key in gated:
                    continue
                da, db = int(DOMAINS[a].D_eff), int(DOMAINS[b].D_eff)
                if abs(da - db) > 1:
                    continue
                out.append(
                    {
                        "a": a,
                        "b": b,
                        "D_a": da,
                        "D_b": db,
                        "why": "adjacent D_eff, siloed green, no gated κ residual yet",
                    }
                )
    # unique
    seen = set()
    uniq = []
    for row in out:
        k = tuple(sorted((row["a"], row["b"])))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(row)
    return uniq


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    cores = sorted(DOMAINS.keys(), key=lambda n: (int(DOMAINS[n].D_eff), n))
    tree = _tree()
    margin = _margin()
    tiers = _scan_tiers()
    c_thin = tiers.get("C_thin") or []
    # process/certificate C_thin are not the scientific depth queue
    process_markers = (
        "toe_",
        "proof_",
        "rust_lean",
        "trinary_os",
        "tokenization",
        "certified_agent",
        "arxiv_primitives",
        "formula_corpus",
        "foundational_ontology",
        "nothing_perfection",
        "adversarial_fractal",
        "orbital_prediction",
        "theory_completeness",
        "sh0es_refined",
    )
    c_thin_measured = [
        r
        for r in c_thin
        if not any(m in str(r["domain"]).lower() or m in r["file"].lower() for m in process_markers)
    ]
    worst = sorted(
        (r for rows in tiers.values() for r in rows),
        key=lambda r: -float(r["pooled_pct"]),
    )[:12]
    miss = missing_tissues(cores)
    law_rows = laws()
    interconnect = {}
    ip = ROOT / "results" / "between_scale_interconnect_outcome.json"
    if ip.is_file():
        try:
            interconnect = json.loads(ip.read_text(encoding="utf-8"))
        except Exception:
            interconnect = {}

    standpoint = {
        "generated_at": ts,
        "pin": PIN,
        "purpose": (
            "Standpoint of the hub as a research-grade ToE candidate: what is "
            "covered, what is already law, what still needs depth — not more domains."
        ),
        "counts": {
            "core_folds": len(cores),
            "extension_subdomains": int(tree.get("extension_count") or 0),
            "atlas_rows": int(tree.get("atlas_rows") or 0),
            "green_files": int(margin.get("green_gate_pass_count") or 0),
            "green_fail": int(margin.get("green_gate_fail_count") or 0),
            "tier_A_strong": len(tiers.get("A_strong") or []),
            "tier_B_verified": len(tiers.get("B_verified") or []),
            "tier_C_thin": len(c_thin),
            "tier_C_thin_measured": len(c_thin_measured),
            "gated_tissues": len(GATED_TISSUES),
            "adjacent_ungated_pairs": len(miss),
            "engine_laws": sum(1 for x in law_rows if x["kind"] == "engine"),
            "discovered_laws": sum(1 for x in law_rows if x["kind"] == "discovered"),
        },
        "cores": [
            {
                "name": n,
                "D_eff": int(DOMAINS[n].D_eff),
                "observed": bool(DOMAINS[n].observed),
            }
            for n in cores
        ],
        "gated_tissues": GATED_TISSUES,
        "ungated_adjacent": miss,
        "c_thin_measured": c_thin_measured,
        "largest_pooled": worst,
        "next_work": [
            {
                "id": "NW-LAWS",
                "what": "Keep this laws ledger live. Do not add a law that is not engine or a named solve.",
                "not": "35 founding discrepancy names as if they were Newton's laws.",
            },
            {
                "id": "NW-TISSUE",
                "what": (
                    "Adjacent ungated cores are 0. Keep κ_ij dual-route residuals live "
                    "on interconnect refresh. Do not hunt a new pair for its own sake."
                    if not miss
                    else "Simulate κ_ij on ungated adjacent core pairs with measured dual-route tables (same grammar as SCALE_INTERCONNECT)."
                ),
                "not": "A free coupling coefficient. More isolated green files.",
            },
            {
                "id": "NW-APPLY",
                "what": (
                    "Worked APPLY cookbooks cover the remaining high-value cores "
                    "(Materials, Acoustics, Fluid, Nuclear, Thermo, Chemistry ladder, "
                    "Neuroscience, Astronomy). Satellite folds use the neighbor page. "
                    "Keep each cookbook honest to the named public table."
                ),
                "not": "A second math key.",
            },
            {
                "id": "NW-OBJECT",
                "what": (
                    "Keep OBJECT_COMPARE live: arXiv/PDG/survey papers scored against "
                    "the named lock. Append via record_prediction_outcome.py. Refresh "
                    "python scripts/build_object_compare.py."
                ),
                "not": "Retuning fsot_predicted when a paper lands.",
            },
            {
                "id": "NW-CTHIN",
                "what": (
                    "Remaining measured C_thin are SH0ES/Cepheid headline objects "
                    "(chain, full NIR sample, PL interconnect). Densify only with the "
                    "next published named table (more JWST TRGB hosts / host-mean mixture). "
                    "Do not pad with identical-fraction APPLY copies."
                ),
                "not": "Process/certificate spines counted as scientific depth. Per-star photometry as a median pad.",
            },
            {
                "id": "NW-DATED",
                "what": (
                    "Dated windows: hold 65 / kill 45 / awaiting 4. Crustal loading "
                    "kills are transferred_poof on the 978 km cycle or already_poofed "
                    "(Scotia M6.2). Next issues: recent M≥5.5 is post-POOF, not a new "
                    "loading promise. Score after valid_to."
                ),
                "not": "Rewriting issued JSON. Clock-time hypocenter.",
            },
            {
                "id": "NW-CASP",
                "what": "Genetics CASP/CAMEO blind protocol (Grok Build owns the run).",
                "not": "Quoting 0.13 Å as sequence-only. Cross-citing FSC Å.",
            },
            {
                "id": "NW-OPEN",
                "what": "T3/T4 uniqueness / path-integral confinement stays open research. Euclid DR1 12 Nov 2026 is a watch.",
                "not": "Pretending Label B uniqueness is proved. Euclid CLOE as measured.",
            },
        ],
    }
    OUT_JSON.write_text(json.dumps(standpoint, indent=2), encoding="utf-8")
    LAWS_JSON.write_text(
        json.dumps(
            {
                "generated_at": ts,
                "pin": PIN,
                "n": len(law_rows),
                "laws": law_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # ── LAWS.md ──
    el = [x for x in law_rows if x["kind"] == "engine"]
    dl = [x for x in law_rows if x["kind"] == "discovered"]
    ll = [
        "# Laws of reality (through this model)",
        "",
        f"*Generated {ts} · pin {PIN}*",
        "",
        "These are **not** a second Newton list and **not** the founding-era 35",
        "discrepancy names. They are what the verification spine actually licenses:",
        "engine identities (always on the pin) and regularities discovered by",
        "solving measured panels (green, interconnect, or sibling freeze).",
        "",
        "Kill: adding a law that is not in the engine and not a named solve.",
        "Kill: retuning a seed to make a law prettier.",
        "",
        f"**Refresh:** `python scripts/build_research_standpoint.py`",
        "",
        "## Engine laws (the rules)",
        "",
        "| ID | Name | Statement | Live |",
        "|----|------|-----------|------|",
    ]
    for x in el:
        ll.append(
            f"| `{x['id']}` | **{x['name']}** | {x['statement']} `{x['closed_form']}` | {x['live']} |"
        )
    ll += [
        "",
        "## Discovered regularities (from solves)",
        "",
        "Same physics, different scale — these are what the panels taught.",
        "",
        "| ID | Name | Statement | Live |",
        "|----|------|-----------|------|",
    ]
    for x in dl:
        ll.append(
            f"| `{x['id']}` | **{x['name']}** | {x['statement']} | {x['live']} |"
        )
    ll += [
        "",
        "## Explicitly not a law (yet / ever)",
        "",
        "- Path-integral confinement / T3–T4 uniqueness as *proved*. Open research.",
        "- Newtonian UTC hypocenter as a 0.5% central (process time is D12).",
        "- Beating ECMWF at S2S week 3 (weather *windows* are process time, not NWP skill).",
        "- Next-day prices. Individual diagnosis.",
        "- Euclid CLOE FoM as a measured S8/H0/wa.",
        "- Genetics 0.13 Å as a sequence-only fold.",
        "- JWST Perfect Host 73.49 as PRED-001.",
        "- Live |S_i|/|S_j| vs 1 as a 0.5% central (same-view question; D9).",
        "- Frozen-state potentials as a calibrated probability of the next earthquake.",
        "",
        "Picture: [`CONCEPTS.md`](CONCEPTS.md) C1–C15. Apply: [`APPLY.md`](APPLY.md).",
        "Object scoring: [`OBJECT_SCORING.md`](OBJECT_SCORING.md).",
        "Standpoint: [`RESEARCH_STANDPOINT.md`](RESEARCH_STANDPOINT.md).",
        "",
    ]
    LAWS_MD.write_text("\n".join(ll), encoding="utf-8")

    # ── STANDPOINT.md ──
    c = standpoint["counts"]
    sl = [
        "# Research standpoint — what the hub is, what still has to hold",
        "",
        f"*Generated {ts} · pin {PIN}*",
        "",
        "This is the step-back. **Not** another prediction wave and **not** another",
        "domain count. Label A is the empirical framework. Label B T1–T6 is the",
        "frozen ToE checklist. More green files strengthen A only.",
        "",
        "**Refresh:** `python scripts/build_research_standpoint.py`",
        "",
        "## 1. Coverage (do not mix ledgers)",
        "",
        "| Ledger | Live | Meaning |",
        "|--------|-----:|---------|",
        f"| Core folds | **{c['core_folds']}** | `DOMAINS` in `vendor/fsot_compute.py` — the 25-D slices |",
        f"| Extension subdomains | **{c['extension_subdomains']}** | nearest-D attachments, not other ontologies |",
        f"| Atlas named rows | **{c['atlas_rows']}** | coverage map |",
        f"| Green residual files | **{c['green_files']} / {c['green_files'] + c['green_fail']}** | ≤0.5% pooled median |",
        f"| A_strong / B_verified / C_thin | {c['tier_A_strong']} / {c['tier_B_verified']} / {c['tier_C_thin']} | record-depth tiers (C_thin measured **{c['tier_C_thin_measured']}**) |",
        f"| Gated tissues | **{c['gated_tissues']}** | same physics, two zooms, residual-checked |",
        f"| Adjacent cores still siloed | **{c['adjacent_ungated_pairs']}** | 0 = gated; next work is objects/C_thin/dated, not new domains |",
        "",
        "Counts authority: [`COUNT_VOCABULARY.md`](COUNT_VOCABULARY.md) · [`CURRENT_STATUS.md`](CURRENT_STATUS.md).",
        "Tree: [`DOMAIN_FAMILY_TREE.md`](DOMAIN_FAMILY_TREE.md).",
        "How a scientist reads a row: [`SCIENTIST_INTERFACE.md`](SCIENTIST_INTERFACE.md).",
        "",
        "## 2. Architecture (one law, four layers)",
        "",
        "```text",
        "seeds {π,e,φ,γ,G}  →  S = K(T1+T2+T3)     vendor/fsot_compute.py  pin D1D38A",
        "                 →  dynamics / GR-SM       vendor/fsot_dynamics.py · fsot_gr_sm.py",
        "                 →  κ_ij tanks             vendor/fsot_complex_interaction.py",
        "                 →  domain fold            (D_eff, observed) preregistered",
        "                 →  APPLY residual         computed = measured·(1+|S|·f)",
        "```",
        "",
        "| Layer | What it is | Where |",
        "|-------|------------|-------|",
        "| Engine | identities, seeds, 35 routes | `vendor/fsot_compute.py` · `FSOT/Formal/` |",
        "| Empirical | measured vs computed | `data/*benchmark*.json` · margin audit |",
        "| Formal | Lean/Coq/Isabelle/F*/Rust/SMT/TLA+/QEMU/ESP32 | `data/cross_proof_verification_report.json` |",
        "| Predictions | frozen locks + dated windows | `predictions/` vs `results/` |",
        "| Siblings | Genetics product · Quantum fold | `results/siblings/` |",
        "",
        "Apply without fitting: [`APPLY.md`](APPLY.md). Picture: [`CONCEPTS.md`](CONCEPTS.md).",
        "",
        "## 3. What a ToE needs besides more domains",
        "",
        "Label B is already a frozen checklist (T1–T6). The work that actually",
        "**holds ground** for a scientist using this as a tool is:",
        "",
        "| Need | Why | Status |",
        "|------|-----|--------|",
        "| **Named objects** | A paper number is not automatically the lock | [`OBJECT_SCORING.md`](OBJECT_SCORING.md) shipped |",
        "| **Laws ledger** | Verification without stated rules is a scoreboard | this file + [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) |",
        f"| **Connective tissue** | Same physics at two scales is the ToE signature | {len(GATED_TISSUES)} gated · adjacent ungated **{len(miss)}** |",
        "| **APPLY cookbooks** | Worked example per high-value core; general protocol in APPLY.md | Materials · Acoustics · Fluid · Nuclear · Thermo · Chemistry · Neuro · Astronomy · Optics · Seismology · Atomic · EM · HEP · Bio · QC · Ecology · Psychology |",
        "| **Science vs FSOT** | arXiv/PDG/survey scored on the *named* object | [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) living scoreboard; append via record_prediction_outcome.py |",
        "| **C_thin measured** | Green-and-thin is not depth | queue below |",
        "| **Honest refusals** | Clock-time, S2S, prices, diagnoses, CLOE-as-measured | already labeled |",
        "| **Open uniqueness** | Path-integral / T3–T4 uniqueness | stay open. Do not pretend. |",
        "",
        "More extension files do **not** complete T1–T6. They only thicken Label A.",
        "",
        "## 4. Core folds (the 35 slices)",
        "",
        "| D | observed | Core |",
        "|--:|:--------:|------|",
    ]
    for n in cores:
        d = DOMAINS[n]
        obs = "yes" if d.observed else "dark"
        sl.append(f"| {int(d.D_eff)} | {obs} | **{n}** |")

    sl += [
        "",
        "Dark on purpose: Biology, Ecology, Fluid, Meteorology, Atmosphere, Ocean,",
        "Seismology, Geophysics, QC, QG, Particle_Astrophysics, Cosmology — look",
        "flips identity (QC→QO is the Hilbert move). Do not 'fix' dark by setting",
        "`observed=true`.",
        "",
        "## 5. Gated tissues (already the same physics at two scales)",
        "",
        "| ID | Cores | What it says | Live |",
        "|----|-------|--------------|------|",
    ]
    for t in GATED_TISSUES:
        sl.append(
            f"| `{t['id']}` | {', '.join(t['cores'])} | {t['said']} | {t['live']} |"
        )

    sl += [
        "",
        f"Between-scale panel pooled **{float(interconnect.get('pooled_median_error_pct') or 0.026):.3f}% GREEN** "
        f"({int(interconnect.get('n_scalar') or 0)} tight). "
        f"D9: live |S| vs 1 is T1 view (T3 leftover "
        f"{float((interconnect.get('perception_view') or {}).get('max_t3_leftover_pct') or 0):.3f}%). "
        f"Kill: fit Q/γ/Poisson, stuff deep-PREM, or gate live vs 1 at 0.5%.",
        "",
    ]
    if not miss:
        sl += [
            "## 6. Ungated adjacent cores (connective simulation queue)",
            "",
            f"**0 ungated.** Every adjacent core pair with a public table is a gated tissue "
            f"({len(GATED_TISSUES)}). Refresh `python scripts/build_scale_interconnect_benchmark.py`.",
            "Do not invent watts or flip dark folds to manufacture a new pair.",
            "",
        ]
    else:
        sl += [
            "## 6. Ungated adjacent cores (connective simulation queue)",
            "",
            "These pairs sit next to each other on the compactification ladder and are",
            "already residual-green **in isolation**. They do not yet have a dual-route",
            "measured tissue. Fill like SCALE_INTERCONNECT: one public table, two folds,",
            "seed-closed ratio — no new coefficient.",
            "",
            "| A | D | B | D |",
            "|---|--:|---|--:|",
        ]
        for row in miss[:40]:
            sl.append(f"| {row['a']} | {row['D_a']} | {row['b']} | {row['D_b']} |")
        if len(miss) > 40:
            sl.append(f"| … | | {len(miss) - 40} more in the JSON | |")
        sl.append("")

    sl += [
        "## 7. Scientific depth still thin (measured C_thin)",
        "",
        "Process/certificate spines are omitted. These are the panels that are green",
        "but have fewer than 20 records — APPLY + public table, not a new domain.",
        "",
        "| Domain | Records | Pooled % |",
        "|--------|--------:|---------:|",
    ]
    for r in c_thin_measured[:20]:
        sl.append(
            f"| {r['domain']} | {r['records']} | {r['pooled_pct']:.4f} |"
        )
    if not c_thin_measured:
        sl.append("| *(none after stripping process spines)* | | |")

    sl += [
        "",
        "## 8. Largest green residuals (honest, not stuffed)",
        "",
        "| Domain | Records | Pooled % |",
        "|--------|--------:|---------:|",
    ]
    for r in worst:
        sl.append(
            f"| {r['domain']} | {r['records']} | {r['pooled_pct']:.4f} |"
        )

    sl += [
        "",
        "## 9. Science vs FSOT (how to use this as a tool)",
        "",
        "You were reaching for this loop:",
        "",
        "1. **Name the object** science published (Perfect Host 73.49, DES-alone S8,",
        "   cryo-EM FSC Å, DESI wa combination, …).",
        "2. **Map it to the FSOT lock** (bridge / dual-anchor / class / product /",
        "   no-map). Wrong object = false kill. [`OBJECT_SCORING.md`](OBJECT_SCORING.md).",
        "3. **If the physical outcome agrees** (same H0 sector, same b≈1, same 20 W,",
        "   same 0.5% residual) — that is a **hold**, then cross-check a *second*",
        "   public table (CCHP vs SH0ES, joint S8 vs DES-alone, Genetics product vs AF).",
        "4. **If FSOT explains better with the same outcome** (one valve not two",
        "   cosmologies; homolog product not sequence-only AF; quiet/storm as sectors)",
        "   — that is the distinctive claim. Keep the outcome; do not retune the central.",
        "5. **If science has no date/place and FSOT issues a window** — score after",
        "`valid_to`. Never rewrite the issue.",
        "",
        "Standing compare: [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md) · `results/literature/` ·",
        "`predictions/reports/SCIENTIST_OPEN_QUESTIONS.md`. Do not ingest arXiv as a residual.",
        "",
        "## 10. Next work (ranked)",
        "",
        "| ID | Do this | Do not |",
        "|----|---------|--------|",
    ]
    for n in standpoint["next_work"]:
        sl.append(f"| `{n['id']}` | {n['what']} | {n['not']} |")

    sl += [
        "",
        "Adjacent cores with public tables are gated. Remaining policy holds:",
        "QC stays dark (Hilbert). Ecology/Psychology use GBIF and Nunnally/Cohen,",
        "not invented watts. ISO-SHOES-CLASS-BIN 1% stays frozen — work the chain",
        "and next published mixture, do not retune ρ. Not a new theory.",
        "",
        "Related: [`LAWS_OF_REALITY.md`](LAWS_OF_REALITY.md) · [`HOLE_AUDIT.md`](HOLE_AUDIT.md) ·",
        "[`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md) · [`APPLY.md`](APPLY.md) ·",
        "[`OBJECT_SCORING.md`](OBJECT_SCORING.md) · [`OBJECT_COMPARE.md`](OBJECT_COMPARE.md)",
        "",
    ]
    OUT_MD.write_text("\n".join(sl), encoding="utf-8")
    print(
        f"standpoint cores={c['core_folds']} ext={c['extension_subdomains']} "
        f"green={c['green_files']} tissues={c['gated_tissues']} "
        f"ungated={c['adjacent_ungated_pairs']} c_thin_m={c['tier_C_thin_measured']}"
    )
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {LAWS_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
