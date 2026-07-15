#!/usr/bin/env python3
"""
Engine simulation prototype for FSOT fuel testing.

This module loads real engine specs, models air/fuel ratio and ignition timing,
and computes brake power, thermal efficiency, fuel consumption, and BSFC.
"""

from __future__ import annotations
import argparse
import csv
import importlib.util
import json
import math
import random
import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

ENGINE_SPECS_PATH = Path(__file__).with_name("engine_specs.json")
FUEL_PROFILES_PATH = Path(__file__).with_name("fuel_profiles.json")
CHEM_HELPER_PATH = Path(__file__).resolve().parent.parent / "files-cd343a7e" / "fsot_chemical_monte_carlo_simulator.py"
AIR_DENSITY_KG_PER_M3 = 1.184  # ambient air density at 25°C, 1 atm
GASOLINE_LHV_KJ_PER_KG = 44_000.0
DIESEL_LHV_KJ_PER_KG = 42_500.0
ETHANOL_LHV_KJ_PER_KG = 30_000.0

ROUTE_COST_MULTIPLIERS = {
    "hemp": 0.95,
    "algae": 1.08,
    "biodiesel": 1.08,
    "mushroom": 1.10,
    "hydrogen": 1.25,
    "gasoline": 1.00,
}

_CHEM_HELPER_MODULE = None

COMPOUND_SEARCH_OVERRIDES = {
    "hydrogen peroxide": "Hydrogen peroxide",
    "hydrogen gas": "Hydrogen",
    "hydrogen": "Hydrogen",
    "water": "Water",
    "furfural": "Furfural",
    "lactic acid": "Lactic acid",
    "glycerol": "Glycerol",
    "terpene": "Limonene",
    "limonene": "Limonene",
    "hemp waste syrup": "Glucose",
    "hemp waste": "Glucose",
    "hemp biomass": "Glucose",
    "hemp": "Glucose",
    "lignin-derived alcohols": "Guaiacol",
    "lignin-derived alcohol": "Guaiacol",
    "lignin": "Lignin",
    "cellulose-derived hydrocarbons": "Glucose",
    "cellulose sugar": "Glucose",
    "cellulose": "Glucose",
    "protein-derived intermediates": "Glycine",
    "protein": "Glycine",
    "performance cofactors": "Ethyl acetate",
    "performance additives": "Ethyl acetate",
    "performance additive": "Ethyl acetate",
    "ester": "Ethyl acetate",
    "ethyl acetate": "Ethyl acetate",
    "bio-ester": "Ethyl acetate",
    "ether": "Diethyl ether",
    "bio-ether": "Diethyl ether",
    "process catalyst": "Platinum",
    "refining catalyst": "Platinum",
    "electrolytic catalyst": "Platinum",
    "sugar": "Glucose",
    "glucose": "Glucose",
}

def get_chem_helper_module() -> Any:
    global _CHEM_HELPER_MODULE
    if _CHEM_HELPER_MODULE is not None:
        return _CHEM_HELPER_MODULE
    if not CHEM_HELPER_PATH.exists():
        raise FileNotFoundError(f"Chemical helper module not found at {CHEM_HELPER_PATH}")
    spec = importlib.util.spec_from_file_location(
        "fsot_chemical_monte_carlo_simulator",
        str(CHEM_HELPER_PATH),
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load chemical helper module from {CHEM_HELPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    if module is None:
        raise ImportError(f"Could not create module from spec for {CHEM_HELPER_PATH}")
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _CHEM_HELPER_MODULE = module
    return module


def normalize_compound_query(label: str) -> str:
    lower = label.strip().lower()
    for key, value in COMPOUND_SEARCH_OVERRIDES.items():
        if key in lower:
            return value
    return label.strip()


def fetch_compound_data(label: str) -> Optional[Dict[str, Any]]:
    module = get_chem_helper_module()
    query = normalize_compound_query(label)
    try:
        data = module.fetch_pubchem_properties(query, search_mode="name")
        if data is None:
            data = module.fetch_nist_properties(query)
        if data is None:
            return None
        return {
            "name": getattr(data, "name", None),
            "query": query,
            "smiles": getattr(data, "smiles", None),
            "inchi_key": getattr(data, "inchi_key", None),
            "molecular_formula": getattr(data, "molecular_formula", None),
            "molecular_weight": getattr(data, "molecular_weight", None),
            "xlogp": getattr(data, "xlogp", None),
            "h_bond_donor_count": getattr(data, "h_bond_donor_count", None),
            "h_bond_acceptor_count": getattr(data, "h_bond_acceptor_count", None),
            "topological_polar_surface_area": getattr(data, "topological_polar_surface_area", None),
            "source": getattr(data, "source", None),
        }
    except Exception:
        return None


def route_cost_multiplier(fuel: "FuelSpec") -> float:
    route = (fuel.production_route or "").lower() + " " + fuel.id.lower()
    for token, multiplier in ROUTE_COST_MULTIPLIERS.items():
        if token in route:
            return multiplier
    return 1.0


def compute_fsot_score(result: "EngineSimulationResult") -> float:
    affordability = max(0.0, 1.0 - min(result.fuel_cost_per_kwh, 1.5) / 1.5)
    practicality = max(0.0, 1.0 - min(max(result.production_difficulty_index - 1.0, 0.0), 1.5) / 1.5)
    efficiency = clamp((result.conversion_efficiency - 0.70) / 0.30, 0.0, 1.0)
    return (
        result.renewable_replacement_score * 0.55
        + efficiency * 0.20
        + affordability * 0.15
        + practicality * 0.10
    )


def parse_molecular_formula(formula: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for match in re.finditer(r"([A-Z][a-z]?)(\d*)", formula):
        element = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        counts[element] = counts.get(element, 0) + count
    return counts


def estimate_hhv_mj_per_kg(formula: str) -> Optional[float]:
    counts = parse_molecular_formula(formula)
    if not counts:
        return None
    mass = (
        counts.get("C", 0) * 12.0
        + counts.get("H", 0) * 1.0
        + counts.get("O", 0) * 16.0
        + counts.get("N", 0) * 14.0
        + counts.get("S", 0) * 32.0
    )
    if mass <= 0:
        return None
    frac_c = counts.get("C", 0) * 12.0 / mass
    frac_h = counts.get("H", 0) * 1.0 / mass
    frac_o = counts.get("O", 0) * 16.0 / mass
    frac_s = counts.get("S", 0) * 32.0 / mass
    hhv = 33.9 * frac_c + 144.6 * max(0.0, frac_h - frac_o / 8.0) + 9.42 * frac_s
    return max(hhv, 5.0)


def estimate_lhv_mj_per_kg(formula: str) -> Optional[float]:
    hhv = estimate_hhv_mj_per_kg(formula)
    if hhv is None:
        return None
    counts = parse_molecular_formula(formula)
    mass = (
        counts.get("C", 0) * 12.0
        + counts.get("H", 0) * 1.0
        + counts.get("O", 0) * 16.0
        + counts.get("N", 0) * 14.0
        + counts.get("S", 0) * 32.0
    )
    if mass <= 0:
        return hhv
    frac_h = counts.get("H", 0) * 1.0 / mass
    water_penalty = 2.443 * 9.0 * frac_h
    return max(hhv - water_penalty, 0.1)


def estimate_molecular_weight(formula: str) -> float:
    counts = parse_molecular_formula(formula)
    return (
        counts.get("C", 0) * 12.0
        + counts.get("H", 0) * 1.0
        + counts.get("O", 0) * 16.0
        + counts.get("N", 0) * 14.0
        + counts.get("S", 0) * 32.0
    )


def estimate_stoich_afr(formula: str) -> Optional[float]:
    counts = parse_molecular_formula(formula)
    c = counts.get("C", 0)
    h = counts.get("H", 0)
    o = counts.get("O", 0)
    n = counts.get("N", 0)
    o2_moles = c + h / 4.0 - o / 2.0
    mass = c * 12.0 + h * 1.0 + o * 16.0 + n * 14.0
    if o2_moles <= 0 or mass <= 0:
        return None
    o2_mass = o2_moles * 32.0
    return o2_mass / 0.233 / mass


def estimate_density_kg_m3(data: Dict[str, Any]) -> Optional[float]:
    mw = data.get("molecular_weight") or 0.0
    xlogp = data.get("xlogp") or 0.0
    density = 600.0 + 150.0 * clamp(min(max(mw, 30.0), 320.0) / 320.0, 0.0, 1.0)
    density += 40.0 * clamp((xlogp + 1.0) / 5.0, 0.0, 1.0)
    return clamp(density, 560.0, 920.0)


def estimate_volatility_index(data: Dict[str, Any]) -> float:
    xlogp = data.get("xlogp")
    if xlogp is None:
        return 0.5
    return clamp(1.0 - min(max(xlogp + 1.0, 0.0), 4.0) / 4.0, 0.2, 1.0)


def estimate_clean_index(data: Dict[str, Any]) -> float:
    formula = data.get("molecular_formula") or ""
    counts = parse_molecular_formula(formula)
    mass = sum(
        counts.get("C", 0) * 12.0
        + counts.get("H", 0) * 1.0
        + counts.get("O", 0) * 16.0
        + counts.get("N", 0) * 14.0
        + counts.get("S", 0) * 32.0
        for _ in [0]
    )
    if mass <= 0:
        return 0.5
    oxygen_mass = counts.get("O", 0) * 16.0 / mass
    xlogp = data.get("xlogp") or 1.0
    score = 0.25 + 0.55 * clamp(min(oxygen_mass / 0.25, 1.0), 0.0, 1.0)
    score += 0.15 * clamp(max(0.0, 1.5 - abs(xlogp - 1.5)) / 1.5, 0.0, 1.0)
    return clamp(score, 0.2, 0.98)


def estimate_emissions_index(data: Dict[str, Any]) -> float:
    return clamp(1.0 - 0.6 * estimate_clean_index(data), 0.05, 1.0)


def estimate_fuel_properties_from_composition(composition: List[Dict[str, Any]]) -> Dict[str, float]:
    fields = {
        "lhv_kj_per_kg": 0.0,
        "stoich_afr": 0.0,
        "density_kg_m3": 0.0,
        "clean_index": 0.0,
        "emissions_index": 0.0,
        "volatility_index": 0.0,
    }
    total_fraction = 0.0
    for entry in composition:
        label = entry.get("name", "")
        fraction = float(entry.get("fraction", 0.0))
        if fraction <= 0.0 or not label:
            continue

        formula = entry.get("molecular_formula")
        data: Optional[Dict[str, Any]] = None
        lhv = None
        afr = None

        if formula:
            lhv = estimate_lhv_mj_per_kg(formula)
            afr = estimate_stoich_afr(formula)
            data = {
                "molecular_formula": formula,
                "molecular_weight": estimate_molecular_weight(formula),
                "xlogp": entry.get("xlogp", 1.0),
            }

        if label:
            collected = fetch_compound_data(label)
            if collected is not None:
                data = collected
                if formula is None:
                    formula = collected.get("molecular_formula")
                if lhv is None and formula:
                    lhv = estimate_lhv_mj_per_kg(formula)
                if afr is None and formula:
                    afr = estimate_stoich_afr(formula)

        if data is None:
            continue

        density = estimate_density_kg_m3(data)
        clean = estimate_clean_index(data)
        emissions = estimate_emissions_index(data)
        volatility = estimate_volatility_index(data)
        weight = fraction
        if lhv is not None:
            fields["lhv_kj_per_kg"] += lhv * 1000.0 * weight
        if afr is not None:
            fields["stoich_afr"] += afr * weight
        if density is not None:
            fields["density_kg_m3"] += density * weight
        fields["clean_index"] += clean * weight
        fields["emissions_index"] += emissions * weight
        fields["volatility_index"] += volatility * weight
        total_fraction += weight
    if total_fraction <= 0.0:
        return {}
    return {k: v / total_fraction for k, v in fields.items()}


def ground_fuel_profile(fuel: "FuelSpec") -> FuelSpec:
    grounded = deepcopy(fuel)
    if grounded.composition:
        props = estimate_fuel_properties_from_composition(grounded.composition)
        if props.get("lhv_kj_per_kg"):
            grounded.lhv_kj_per_kg = props["lhv_kj_per_kg"]
        if props.get("stoich_afr"):
            grounded.stoich_afr = props["stoich_afr"]
        if props.get("density_kg_m3"):
            grounded.density_kg_m3 = props["density_kg_m3"]
        grounded.clean_index = props.get("clean_index", grounded.clean_index)
        grounded.emissions_index = props.get("emissions_index", grounded.emissions_index)
        grounded.volatility_index = props.get("volatility_index", grounded.volatility_index)
    return grounded


def collect_fuel_profile_real_data(fuel: "FuelSpec") -> Dict[str, Any]:
    entries: Dict[str, Any] = {}
    for item in fuel.composition:
        label = item.get("name", "")
        if label and label not in entries:
            entries[label] = {
                "type": "composition",
                "fraction": item.get("fraction", 0.0),
                "result": fetch_compound_data(label),
            }
    for precursor in fuel.precursors:
        label = precursor.get("name", "")
        if label and label not in entries:
            entries[label] = {
                "type": "precursor",
                "mass_kg": precursor.get("mass_kg", 0.0),
                "unit_cost": precursor.get("unit_cost", 0.0),
                "result": fetch_compound_data(label),
            }
    return {
        "fuel_profile_id": fuel.id,
        "fuel_profile_name": fuel.name,
        "lookup_entries": entries,
    }


def format_fuel_profile_real_data(data: Dict[str, Any]) -> str:
    lines = [
        f"Fuel profile: {data.get('fuel_profile_name', '<unknown>')} ({data.get('fuel_profile_id')})",
        "Resolved compound lookups:",
    ]
    for label, entry in data.get("lookup_entries", {}).items():
        result = entry.get("result")
        if result:
            lines.append(
                f"- {label} ({entry['type']}): query={result.get('query')} source={result.get('source')} "
                f"formula={result.get('molecular_formula')} mw={result.get('molecular_weight')}"
            )
        else:
            lines.append(f"- {label} ({entry['type']}): no compound data found for query={normalize_compound_query(label)}")
    return "\n".join(lines)


@dataclass
class FuelSpec:
    id: str
    name: str
    description: str
    fuel_type: str
    lhv_kj_per_kg: float
    stoich_afr: float
    density_kg_m3: float
    clean_index: float
    emissions_index: float
    knock_resistance: float
    octane_rating: float
    flame_speed_m_s: float
    volatility_index: float
    composition: List[Dict[str, Any]] = field(default_factory=list)
    byproducts: Dict[str, float] = field(default_factory=dict)
    production_cost_per_kg: float = 1.0
    production_difficulty_index: float = 1.0
    precursors: List[Dict[str, Any]] = field(default_factory=list)
    process_energy_kj_per_kg: float = 0.0
    processing_cost_per_kj: float = 0.0001
    overhead_cost_per_kg: float = 0.0
    catalyst_cycle_cost_per_kg: float = 0.0
    coproduct_credit_per_kg: float = 0.0
    remediation_credit_per_kg: float = 0.0
    biomass_yield_kg_fuel_per_kg_biomass: float = 0.0
    conversion_efficiency: float = 1.0
    renewable_fraction: float = 0.0
    renewable_source: Optional[str] = None
    production_route: str = "standard"

    @property
    def burn_quality_factor(self) -> float:
        return 0.90 + 0.10 * self.clean_index + 0.05 * self.knock_resistance

    @property
    def estimated_production_cost_per_kg(self) -> float:
        precursor_cost = sum(
            precursor.get("mass_kg", 0.0) * precursor.get("unit_cost", 0.0)
            for precursor in self.precursors
        )
        processing_cost = self.process_energy_kj_per_kg * self.processing_cost_per_kj
        catalyst_cost = self.catalyst_cycle_cost_per_kg
        gross_cost = precursor_cost + processing_cost + self.overhead_cost_per_kg + catalyst_cost
        adjusted_gross = gross_cost * route_cost_multiplier(self)
        net_cost = adjusted_gross - self.coproduct_credit_per_kg - self.remediation_credit_per_kg
        return max(0.0, net_cost)

    @property
    def effective_biomass_usage_kg_per_kg(self) -> float:
        if self.biomass_yield_kg_fuel_per_kg_biomass > 0:
            return 1.0 / self.biomass_yield_kg_fuel_per_kg_biomass
        return 0.0

    @property
    def production_route_summary(self) -> str:
        return self.production_route

    @property
    def estimated_cost_factor(self) -> float:
        return self.estimated_production_cost_per_kg * self.production_difficulty_index

    @property
    def cost_factor(self) -> float:
        return self.production_cost_per_kg * self.production_difficulty_index

@dataclass
class EngineSpec:
    id: str
    name: str
    description: str
    fuel_type: str
    displacement_l: float
    cylinders: int
    compression_ratio: float
    max_power_kw: float
    max_torque_nm: float
    rated_rpm: int
    max_rpm: int
    base_thermal_efficiency: float
    mechanical_efficiency: float
    volumetric_efficiency: float
    stoich_afr: float
    optimal_spark_advance_deg: float
    default_fuel_profile_id: str
    lubricant: LubricantSpec
    cooling_system: CoolingSystemSpec
    valvetrain: ValvetrainSpec
    cranktrain: CranktrainSpec
    bore_mm: Optional[float] = None
    stroke_mm: Optional[float] = None
    cylinder_spacing_mm: Optional[float] = None
    block_material: Optional[str] = None
    head_material: Optional[str] = None
    valvetrain_type: Optional[str] = None
    fuel_system: Optional[str] = None
    intake_type: Optional[str] = None
    exhaust_type: Optional[str] = None
    oil_system: Optional[str] = None
    cooling_design: Optional[str] = None
    idle_rpm: Optional[int] = None
    peak_torque_rpm: Optional[int] = None
    rod_to_stroke_ratio: Optional[float] = None
    power_calibration_factor: float = 1.0
    source: str = ""

    @property
    def displacement_m3(self) -> float:
        return self.displacement_l / 1000.0

    @property
    def swept_volume_per_cycle_m3(self) -> float:
        return self.displacement_m3 / 2.0

    @property
    def lhv_kj_per_kg(self) -> float:
        if self.fuel_type == "diesel":
            return DIESEL_LHV_KJ_PER_KG
        if self.fuel_type == "ethanol":
            return ETHANOL_LHV_KJ_PER_KG
        return GASOLINE_LHV_KJ_PER_KG

    @property
    def oil_flow_kg_s(self) -> float:
        return self.lubricant.flow_rate_l_min / 60.0 * self.lubricant.density_kg_m3 / 1000.0

    @property
    def coolant_flow_kg_s(self) -> float:
        return self.cooling_system.flow_rate_l_min / 60.0 * self.cooling_system.density_kg_m3 / 1000.0

    def friction_losses_kw(self, brake_power_kw: float) -> float:
        return brake_power_kw * (
            self.valvetrain.friction_factor
            + self.cranktrain.friction_factor
            + self.lubricant.friction_factor
        )

    def pump_power_kw(self) -> float:
        return self.lubricant.pump_power_kw + self.cooling_system.pump_power_kw

    def cooling_capacity_kw(self, delta_temp_c: float = 20.0) -> float:
        return (
            self.coolant_flow_kg_s
            * self.cooling_system.heat_capacity_kj_per_kgk
            * delta_temp_c
            * self.cooling_system.radiator_efficiency
        )

    def oil_temperature_rise_c(self, oil_heat_kw: float) -> float:
        if self.oil_flow_kg_s <= 0:
            return 0.0
        return oil_heat_kw / (self.oil_flow_kg_s * self.lubricant.thermal_capacity_kj_per_kgk)


@dataclass
class LubricantSpec:
    oil_type: str
    viscosity_cst_100c: float
    density_kg_m3: float
    flow_rate_l_min: float
    pump_power_kw: float
    friction_factor: float
    thermal_capacity_kj_per_kgk: float


@dataclass
class CoolingSystemSpec:
    coolant_type: str
    flow_rate_l_min: float
    heat_capacity_kj_per_kgk: float
    density_kg_m3: float
    radiator_efficiency: float
    pump_power_kw: float
    ambient_temp_c: float = 25.0


@dataclass
class ValvetrainSpec:
    camshaft_phasing_deg: float
    valve_lift_mm: float
    valve_timing_deg: float
    friction_factor: float


@dataclass
class CranktrainSpec:
    crank_mass_kg: float
    friction_factor: float
    bearing_count: int


@dataclass
class EngineSimulationResult:
    brake_power_kw: float
    indicated_power_kw: float
    thermal_efficiency: float
    mechanical_efficiency: float
    fuel_flow_kg_s: float
    bsfc_g_kwh: float
    torque_nm: float
    air_mass_flow_kg_s: float
    fuel_energy_input_kw: float
    afr: float
    spark_advance_deg: float
    throttle: float
    rpm: int
    friction_losses_kw: float = 0.0
    pump_power_kw: float = 0.0
    bench_net_power_kw: float = 0.0
    heat_rejection_kw: float = 0.0
    cooling_capacity_kw: float = 0.0
    coolant_temp_rise_c: float = 0.0
    oil_temp_rise_c: float = 0.0
    knock_risk: float = 0.0
    fuel_profile_id: str = ""
    fuel_clean_index: float = 0.0
    fuel_emissions_index: float = 0.0
    fuel_octane_rating: float = 0.0
    fuel_flame_speed: float = 0.0
    fuel_volatility: float = 0.0
    biomass_yield_kg_fuel_per_kg_biomass: float = 0.0
    conversion_efficiency: float = 0.0
    catalyst_cost_per_kg: float = 0.0
    coproduct_credit_per_kg: float = 0.0
    renewable_fraction: float = 0.0
    remediation_credit_per_kg: float = 0.0
    remediation_benefit_score: float = 0.0
    co_g_per_h: float = 0.0
    nox_g_per_h: float = 0.0
    soot_g_per_h: float = 0.0
    aldehyde_g_per_h: float = 0.0
    formaldehyde_g_per_h: float = 0.0
    benzene_g_per_h: float = 0.0
    pm25_g_per_h: float = 0.0
    total_voc_g_per_h: float = 0.0
    toxicity_index: float = 0.0
    novel_species_risk: float = 0.0
    renewable_replacement_score: float = 0.0
    fsot_score: float = 0.0
    fuel_cost_per_h: float = 0.0
    fuel_cost_per_kwh: float = 0.0
    fuel_production_cost_per_kg: float = 0.0
    fuel_production_route: str = ""
    production_difficulty_index: float = 0.0
    material_compatibility_index: float = 0.0
    seal_degradation_risk: float = 0.0
    corrosion_risk: float = 0.0
    rubber_swelling_risk: float = 0.0
    fsot_adjusted_power_kw: float = 0.0
    fsot_adjusted_torque_nm: float = 0.0


def composition_fraction(fuel: FuelSpec, keywords: List[str]) -> float:
    return sum(
        item.get("fraction", 0.0)
        for item in fuel.composition
        if any(keyword in item.get("name", "").lower() for keyword in keywords)
    )


def precursor_mass_factor(fuel: FuelSpec, keyword: str) -> float:
    return sum(
        precursor.get("mass_kg", 0.0)
        for precursor in fuel.precursors
        if keyword in precursor.get("name", "").lower()
    )


def clamp_factor(value: float, minimum: float = 0.25, maximum: float = 2.5) -> float:
    return max(minimum, min(maximum, value))


def compute_replacement_score(result: EngineSimulationResult) -> float:
    emissions_score = max(0.0, 1.0 - result.toxicity_index / 1.5)
    cost_score = max(0.0, 1.0 - min(result.fuel_cost_per_kwh, 1.2) / 1.2)
    remediation_score = min(1.0, result.remediation_benefit_score)
    return (
        result.renewable_fraction * 0.45
        + emissions_score * 0.25
        + cost_score * 0.20
        + remediation_score * 0.10
    )


def compute_material_compatibility(fuel: FuelSpec, result: EngineSimulationResult) -> tuple[float, float, float, float]:
    oxygenate_frac = composition_fraction(
        fuel,
        ["oxygenate", "ester", "ether", "alcohol", "furan", "acetate", "glycol"],
    )
    acid_frac = composition_fraction(
        fuel,
        ["acid", "carboxylic", "formic", "acetic", "benzoic"],
    )
    aromatic_frac = composition_fraction(
        fuel,
        ["aromatic", "aromatics", "benzene", "phenol", "toluene", "guaiacol"],
    )
    aldehyde_frac = composition_fraction(
        fuel,
        ["aldehyde", "formaldehyde", "acrolein"],
    )

    compatibility = 1.0 - (
        oxygenate_frac * 0.24
        + acid_frac * 0.18
        + aromatic_frac * 0.12
        + aldehyde_frac * 0.15
        + (1.0 - fuel.clean_index) * 0.10
    )
    compatibility = clamp(compatibility, 0.0, 1.0)

    seal_risk = clamp(
        oxygenate_frac * 0.40
        + acid_frac * 0.30
        + aldehyde_frac * 0.18
        + (1.0 - fuel.clean_index) * 0.12,
        0.0,
        1.0,
    )
    corrosion_risk = clamp(
        acid_frac * 0.35 + aldehyde_frac * 0.20 + (1.0 - fuel.clean_index) * 0.10,
        0.0,
        1.0,
    )
    rubber_risk = clamp(
        oxygenate_frac * 0.45 + aromatic_frac * 0.15 + acid_frac * 0.10,
        0.0,
        1.0,
    )
    return compatibility, seal_risk, corrosion_risk, rubber_risk


def estimate_byproducts(fuel: FuelSpec, result: EngineSimulationResult) -> EngineSimulationResult:
    afr_ratio = result.afr / fuel.stoich_afr
    rich_factor = max(0.0, fuel.stoich_afr / result.afr - 1.0)
    lean_factor = max(0.0, afr_ratio - 1.0)
    burn_impurity = 1.0 + (1.0 - fuel.clean_index) * 1.5
    co = fuel.byproducts.get("co_g_per_kg", 100.0)
    nox = fuel.byproducts.get("nox_g_per_kg", 20.0)
    soot = fuel.byproducts.get("soot_g_per_kg", 15.0)
    aldehyde = fuel.byproducts.get("aldehyde_g_per_kg", 12.0)

    aromatic_frac = composition_fraction(fuel, ["aromatic", "aromatics", "alkyl aromatic", "aromatic intermediate"])
    olefin_frac = composition_fraction(fuel, ["alkene", "olefin", "olefinic"])
    oxygenate_frac = composition_fraction(fuel, ["oxygenate", "ester", "ether", "alcohol", "furan", "bio-ether", "alcoholate"])
    heavy_frac = composition_fraction(fuel, ["c8", "c9", "c10", "heavy", "alkyl"])
    additive_frac = composition_fraction(fuel, ["additive", "performance", "cleaning"])

    benzene_base = 3.5 + aromatic_frac * 28.0 + heavy_frac * 10.0
    benzene_route_factor = 1.0 + precursor_mass_factor(fuel, "aromatic") * 0.35 + precursor_mass_factor(fuel, "crude") * 0.15
    formaldehyde_base = 2.2 + oxygenate_frac * 20.0 + olefin_frac * 6.5
    formaldehyde_route_factor = 1.0 + precursor_mass_factor(fuel, "ester") * 0.18 + precursor_mass_factor(fuel, "alcohol") * 0.14
    total_voc_base = aldehyde * 1.2 + benzene_base * 0.6 + oxygenate_frac * 10.0 + olefin_frac * 5.5 + additive_frac * 1.8
    total_voc_route_factor = 1.0 + precursor_mass_factor(fuel, "performance") * 0.10 - precursor_mass_factor(fuel, "bio") * 0.05

    co_g_per_h = result.fuel_flow_kg_s * 3600.0 * co * (1.0 + rich_factor * 1.2) * burn_impurity
    nox_g_per_h = result.fuel_flow_kg_s * 3600.0 * nox * (1.0 + lean_factor * 1.4) * burn_impurity * (1.0 - fuel.clean_index * 0.2)
    soot_g_per_h = result.fuel_flow_kg_s * 3600.0 * soot * (1.0 + rich_factor * 1.4) * burn_impurity * (1.0 + fuel.volatility_index * 0.3)
    aldehyde_g_per_h = result.fuel_flow_kg_s * 3600.0 * aldehyde * (1.0 + rich_factor * 0.8 + lean_factor * 0.4) * burn_impurity
    benzene_g_per_h = result.fuel_flow_kg_s * 3600.0 * benzene_base * (1.0 + rich_factor * 0.25) * burn_impurity * (1.0 - fuel.clean_index * 0.12) * benzene_route_factor
    formaldehyde_g_per_h = result.fuel_flow_kg_s * 3600.0 * formaldehyde_base * (1.0 + lean_factor * 0.2) * burn_impurity * (1.0 - fuel.clean_index * 0.18) * formaldehyde_route_factor
    pm25_g_per_h = result.fuel_flow_kg_s * 3600.0 * soot * (1.0 + aromatic_frac * 0.55 + heavy_frac * 0.30) * burn_impurity * (1.0 + rich_factor * 0.35) * (1.0 - fuel.clean_index * 0.10)
    total_voc_g_per_h = result.fuel_flow_kg_s * 3600.0 * total_voc_base * burn_impurity * max(0.65, 1.0 - fuel.clean_index * 0.12) * total_voc_route_factor
    toxicity = fuel.emissions_index * (0.5 + 0.5 * burn_impurity)
    novel = max(0.0, (1.0 - fuel.clean_index) * 1.2)

    result.co_g_per_h = co_g_per_h
    result.nox_g_per_h = nox_g_per_h
    result.soot_g_per_h = soot_g_per_h
    result.aldehyde_g_per_h = aldehyde_g_per_h
    result.formaldehyde_g_per_h = formaldehyde_g_per_h
    result.benzene_g_per_h = benzene_g_per_h
    result.pm25_g_per_h = pm25_g_per_h
    result.total_voc_g_per_h = total_voc_g_per_h
    result.toxicity_index = toxicity
    result.novel_species_risk = novel
    result.fuel_production_cost_per_kg = fuel.estimated_production_cost_per_kg
    result.material_compatibility_index = 0.0
    result.seal_degradation_risk = 0.0
    result.corrosion_risk = 0.0
    result.rubber_swelling_risk = 0.0
    result.remediation_credit_per_kg = fuel.remediation_credit_per_kg
    result.remediation_benefit_score = min(1.0, fuel.remediation_credit_per_kg / 0.25)
    result.fuel_cost_per_h = result.fuel_flow_kg_s * 3600.0 * result.fuel_production_cost_per_kg
    result.fuel_cost_per_kwh = (
        result.fuel_cost_per_h / result.bench_net_power_kw
        if result.bench_net_power_kw > 0.01
        else 0.0
    )
    result.fuel_production_route = fuel.production_route_summary
    result.production_difficulty_index = fuel.production_difficulty_index
    result.biomass_yield_kg_fuel_per_kg_biomass = fuel.biomass_yield_kg_fuel_per_kg_biomass
    result.conversion_efficiency = fuel.conversion_efficiency
    result.catalyst_cost_per_kg = fuel.catalyst_cycle_cost_per_kg
    result.coproduct_credit_per_kg = fuel.coproduct_credit_per_kg
    result.remediation_credit_per_kg = fuel.remediation_credit_per_kg
    result.renewable_fraction = fuel.renewable_fraction
    (
        result.material_compatibility_index,
        result.seal_degradation_risk,
        result.corrosion_risk,
        result.rubber_swelling_risk,
    ) = compute_material_compatibility(fuel, result)
    result.renewable_replacement_score = compute_replacement_score(result)
    result.fsot_score = compute_fsot_score(result)
    result.fsot_adjusted_power_kw = compute_fsot_adjusted_power(result)
    result.fsot_adjusted_torque_nm = (
        result.fsot_adjusted_power_kw * 9549.297 / result.rpm
        if result.rpm > 0
        else 0.0
    )
    return result


def compute_fsot_adjusted_power(result: EngineSimulationResult) -> float:
    adjustment_factor = 1.0 + 0.10 * (result.fsot_score - 0.50)
    return max(0.0, result.bench_net_power_kw * adjustment_factor)


def parse_lubricant(data: Dict[str, Any]) -> LubricantSpec:
    return LubricantSpec(**data)


def parse_cooling_system(data: Dict[str, Any]) -> CoolingSystemSpec:
    return CoolingSystemSpec(**data)


def parse_valvetrain(data: Dict[str, Any]) -> ValvetrainSpec:
    return ValvetrainSpec(**data)


def parse_cranktrain(data: Dict[str, Any]) -> CranktrainSpec:
    return CranktrainSpec(**data)


def load_engine_specs(path: Path = ENGINE_SPECS_PATH) -> Dict[str, EngineSpec]:
    raw = json.loads(path.read_text())
    specs: Dict[str, EngineSpec] = {}
    for item in raw.get("engines", []):
        item["lubricant"] = parse_lubricant(item.get("lubricant", {}))
        item["cooling_system"] = parse_cooling_system(item.get("cooling_system", {}))
        item["valvetrain"] = parse_valvetrain(item.get("valvetrain", {}))
        item["cranktrain"] = parse_cranktrain(item.get("cranktrain", {}))
        specs[item["id"]] = EngineSpec(**item)
    return specs


def enrich_fuel_profile(fuel: FuelSpec) -> None:
    route = (fuel.production_route or fuel.id).lower()
    if "hemp" in route:
        fuel.renewable_fraction = max(fuel.renewable_fraction, 0.96)
        fuel.conversion_efficiency = max(fuel.conversion_efficiency, 0.82)
        fuel.production_difficulty_index = max(fuel.production_difficulty_index, 1.15)
        if fuel.biomass_yield_kg_fuel_per_kg_biomass <= 0.0:
            fuel.biomass_yield_kg_fuel_per_kg_biomass = 0.50
        if "waste" in route:
            fuel.remediation_credit_per_kg = max(fuel.remediation_credit_per_kg, 0.05)
    if "algae" in route or "biodiesel" in route:
        fuel.renewable_fraction = max(fuel.renewable_fraction, 0.95)
        fuel.conversion_efficiency = max(fuel.conversion_efficiency, 0.82)
        fuel.production_difficulty_index = max(fuel.production_difficulty_index, 1.25)
        fuel.remediation_credit_per_kg = max(fuel.remediation_credit_per_kg, 0.18)
        fuel.clean_index = max(fuel.clean_index, 0.88)
    if "mushroom" in route or "fungus" in fuel.fuel_type.lower():
        fuel.renewable_fraction = max(fuel.renewable_fraction, 0.96)
        fuel.conversion_efficiency = max(fuel.conversion_efficiency, 0.80)
        fuel.production_difficulty_index = max(fuel.production_difficulty_index, 1.25)
        if fuel.biomass_yield_kg_fuel_per_kg_biomass <= 0.0:
            fuel.biomass_yield_kg_fuel_per_kg_biomass = 0.46
    if fuel.fuel_type == "hydrogen":
        fuel.renewable_fraction = 0.99
        fuel.clean_index = max(fuel.clean_index, 0.92)
        fuel.emissions_index = min(fuel.emissions_index, 0.06)
        fuel.process_energy_kj_per_kg = max(fuel.process_energy_kj_per_kg, 47_000.0)
        fuel.production_cost_per_kg = max(fuel.production_cost_per_kg, 3.50)
        fuel.production_difficulty_index = max(fuel.production_difficulty_index, 1.40)


def load_fuel_profiles(path: Path = FUEL_PROFILES_PATH) -> Dict[str, FuelSpec]:
    raw = json.loads(path.read_text())
    specs: Dict[str, FuelSpec] = {
        item["id"]: FuelSpec(**item)
        for item in raw.get("fuel_profiles", [])
    }
    for fuel in specs.values():
        enrich_fuel_profile(fuel)
    return specs


def result_to_record(
    engine: EngineSpec,
    result: EngineSimulationResult,
    mode: str,
    weights: Optional[List[float]] = None,
) -> Dict[str, Any]:
    record: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "engine_id": engine.id,
        "engine_name": engine.name,
        "fuel_profile_id": result.fuel_profile_id,
        "fuel_production_route": result.fuel_production_route,
        "weights": weights or [],
        "fsot_score": result.fsot_score,
        "renewable_rank": result.renewable_replacement_score,
        "fuel_cost_per_kwh": result.fuel_cost_per_kwh,
        "fuel_production_cost_per_kg": result.fuel_production_cost_per_kg,
        "toxicity_index": result.toxicity_index,
        "renewable_fraction": result.renewable_fraction,
        "material_compatibility_index": result.material_compatibility_index,
        "seal_degradation_risk": result.seal_degradation_risk,
        "corrosion_risk": result.corrosion_risk,
        "rubber_swelling_risk": result.rubber_swelling_risk,
        "thermal_efficiency": result.thermal_efficiency,
        "bsfc_g_kwh": result.bsfc_g_kwh,
        "co_g_per_h": result.co_g_per_h,
        "nox_g_per_h": result.nox_g_per_h,
        "soot_g_per_h": result.soot_g_per_h,
        "remediation_credit_per_kg": result.remediation_credit_per_kg,
        "production_difficulty_index": result.production_difficulty_index,
        "conversion_efficiency": result.conversion_efficiency,
    }
    return record


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                k: (";".join(str(x) for x in v) if isinstance(v, list) else v)
                for k, v in row.items()
            })


def save_results(path_str: str, summary: Dict[str, Any], records: List[Dict[str, Any]]) -> None:
    base = Path(path_str)
    if base.suffix.lower() in [".json", ".csv"]:
        base = base.with_suffix("")
    json_path = base.with_suffix(".json")
    csv_path = base.with_suffix(".csv")
    payload = {"summary": summary, "records": records}
    write_json(json_path, payload)
    write_csv(csv_path, records)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def kw_to_hp(kw: float) -> float:
    return kw * 1.34102209


def nm_to_ftlb(nm: float) -> float:
    return nm * 0.737562149


def spark_timing_efficiency_factor(
    spark_advance_deg: float, optimal_advance_deg: float
) -> float:
    offset = abs(spark_advance_deg - optimal_advance_deg)
    return clamp(1.0 - 0.02 * offset, 0.75, 1.0)


def afr_efficiency_factor(afr: float, stoich: float) -> float:
    ratio = afr / stoich
    if ratio < 0.95:
        return 0.90
    if ratio < 1.0:
        return 0.95
    if ratio <= 1.1:
        return 1.0
    if ratio <= 1.2:
        return 0.98
    return 0.92


def simulate_engine_cycle(
    engine: EngineSpec,
    rpm: int,
    throttle: float = 1.0,
    fuel: Optional[FuelSpec] = None,
    afr: float = None,
    spark_advance_deg: float = None,
    detailed: bool = False,
) -> EngineSimulationResult:
    if fuel is None:
        raise ValueError("Fuel profile must be provided for simulation.")
    afr = afr if afr is not None else fuel.stoich_afr
    spark_advance_deg = (
        spark_advance_deg
        if spark_advance_deg is not None
        else engine.optimal_spark_advance_deg
    )
    throttle = clamp(throttle, 0.0, 1.0)
    rpm = max(800, min(rpm, engine.max_rpm))

    volumetric_efficiency = engine.volumetric_efficiency * clamp(
        1.0 - 0.05 * (rpm / engine.max_rpm - 0.5), 0.7, 1.0
    )

    air_mass_flow_kg_s = (
        engine.displacement_m3
        * rpm
        / 120.0
        * AIR_DENSITY_KG_PER_M3
        * volumetric_efficiency
        * throttle
    )

    fuel_flow_kg_s = air_mass_flow_kg_s / afr
    fuel_energy_input_kw = fuel_flow_kg_s * fuel.lhv_kj_per_kg

    thermal_efficiency = (
        engine.base_thermal_efficiency
        * afr_efficiency_factor(afr, fuel.stoich_afr)
        * spark_timing_efficiency_factor(spark_advance_deg, engine.optimal_spark_advance_deg)
        * clamp(0.8 + 0.2 * throttle, 0.75, 1.0)
        * fuel.burn_quality_factor
    )

    indicated_power_kw = fuel_energy_input_kw * thermal_efficiency
    brake_power_kw = indicated_power_kw * engine.mechanical_efficiency
    if engine.power_calibration_factor != 1.0:
        indicated_power_kw *= engine.power_calibration_factor
        brake_power_kw *= engine.power_calibration_factor
    torque_nm = brake_power_kw * 9549.297 / rpm if rpm else 0.0

    friction_losses_kw = engine.friction_losses_kw(brake_power_kw)
    accessory_pump_kw = engine.pump_power_kw()
    bench_net_power_kw = max(0.0, brake_power_kw - accessory_pump_kw)
    heat_rejection_kw = max(0.0, fuel_energy_input_kw - brake_power_kw)
    cooling_capacity_kw = engine.cooling_capacity_kw()
    coolant_temp_rise_c = (
        heat_rejection_kw / cooling_capacity_kw * 20.0
        if cooling_capacity_kw > 0
        else 0.0
    )
    oil_heat_kw = brake_power_kw * engine.lubricant.friction_factor * 0.5
    oil_temp_rise_c = engine.oil_temperature_rise_c(oil_heat_kw)

    knock_risk = clamp(
        abs(afr - fuel.stoich_afr) / fuel.stoich_afr
        + abs(spark_advance_deg - engine.optimal_spark_advance_deg) / 30.0
        + (1.0 - fuel.knock_resistance) * 0.2,
        0.0,
        1.0,
    )

    bsfc_g_kwh = 0.0
    if bench_net_power_kw > 0.01:
        bsfc_g_kwh = fuel_flow_kg_s * 3600.0 / bench_net_power_kw * 1000.0

    result = EngineSimulationResult(
        brake_power_kw=brake_power_kw,
        indicated_power_kw=indicated_power_kw,
        thermal_efficiency=thermal_efficiency,
        mechanical_efficiency=engine.mechanical_efficiency,
        fuel_flow_kg_s=fuel_flow_kg_s,
        bsfc_g_kwh=bsfc_g_kwh,
        torque_nm=torque_nm,
        air_mass_flow_kg_s=air_mass_flow_kg_s,
        fuel_energy_input_kw=fuel_energy_input_kw,
        afr=afr,
        spark_advance_deg=spark_advance_deg,
        throttle=throttle,
        rpm=rpm,
        friction_losses_kw=friction_losses_kw,
        pump_power_kw=accessory_pump_kw,
        bench_net_power_kw=bench_net_power_kw,
        heat_rejection_kw=heat_rejection_kw,
        cooling_capacity_kw=cooling_capacity_kw,
        coolant_temp_rise_c=coolant_temp_rise_c,
        oil_temp_rise_c=oil_temp_rise_c,
        knock_risk=knock_risk,
        fuel_profile_id=fuel.id,
        fuel_clean_index=fuel.clean_index,
        fuel_emissions_index=fuel.emissions_index,
        fuel_octane_rating=fuel.octane_rating,
        fuel_flame_speed=fuel.flame_speed_m_s,
        fuel_volatility=fuel.volatility_index,
    )

    return estimate_byproducts(fuel, result)


def format_engine_spec_details(engine: EngineSpec) -> str:
    details = []
    if engine.bore_mm is not None and engine.stroke_mm is not None:
        details.append(f"Bore x stroke: {engine.bore_mm:.1f} mm x {engine.stroke_mm:.1f} mm")
    if engine.block_material or engine.head_material:
        details.append(
            f"Block/head materials: {engine.block_material or 'unknown'}/{engine.head_material or 'unknown'}"
        )
    if engine.valvetrain_type:
        details.append(f"Valvetrain: {engine.valvetrain_type}")
    if engine.fuel_system:
        details.append(f"Fuel system: {engine.fuel_system}")
    if engine.intake_type:
        details.append(f"Intake: {engine.intake_type}")
    if engine.oil_system:
        details.append(f"Oil system: {engine.oil_system}")
    if engine.cooling_design:
        details.append(f"Cooling: {engine.cooling_design}")
    return "\n".join(details)


def format_result(engine: EngineSpec, result: EngineSimulationResult, detailed: bool = False) -> str:
    spec_torque_at_rated = engine.max_power_kw * 9549.297 / engine.rated_rpm if engine.rated_rpm else 0.0
    spec_power_at_peak_torque = engine.max_torque_nm * engine.rated_rpm / 9549.297 if engine.rated_rpm else 0.0
    base_text = (
        f"Engine: {engine.name}\n"
        f"Description: {engine.description}\n"
        f"Fuel profile: {result.fuel_profile_id}\n"
        f"Fuel clean index: {result.fuel_clean_index:.3f}\n"
        f"Fuel emissions index: {result.fuel_emissions_index:.3f}\n"
        f"RPM: {result.rpm}\n"
        f"Throttle: {result.throttle:.2f}\n"
        f"AFR: {result.afr:.2f}\n"
        f"Spark advance: {result.spark_advance_deg:.1f}°\n"
        f"Brake power: {result.brake_power_kw:.2f} kW ({kw_to_hp(result.brake_power_kw):.1f} hp)\n"
        f"Indicated power: {result.indicated_power_kw:.2f} kW ({kw_to_hp(result.indicated_power_kw):.1f} hp)\n"
        f"Crankshaft torque: {result.torque_nm:.1f} Nm ({nm_to_ftlb(result.torque_nm):.1f} ft-lb)\n"
        f"Thermal efficiency: {result.thermal_efficiency:.3f}\n"
        f"Fuel flow: {result.fuel_flow_kg_s:.4f} kg/s\n"
        f"BSFC: {result.bsfc_g_kwh:.1f} g/kWh\n"
        f"Spec torque at rated rpm: {spec_torque_at_rated:.1f} Nm ({nm_to_ftlb(spec_torque_at_rated):.1f} ft-lb)\n"
        f"Spec power at peak torque: {spec_power_at_peak_torque:.2f} kW ({kw_to_hp(spec_power_at_peak_torque):.1f} hp)\n"
        f"FSOT-adjusted power: {result.fsot_adjusted_power_kw:.2f} kW ({kw_to_hp(result.fsot_adjusted_power_kw):.1f} hp)\n"
        f"FSOT-adjusted torque: {result.fsot_adjusted_torque_nm:.1f} Nm ({nm_to_ftlb(result.fsot_adjusted_torque_nm):.1f} ft-lb)\n"
    )
    if detailed:
        detail_text = format_engine_spec_details(engine)
        if detail_text:
            base_text += detail_text + "\n"
    if not detailed:
        return base_text

    return (
        base_text
        + f"CO yield: {result.co_g_per_h:.1f} g/h\n"
        + f"NOx yield: {result.nox_g_per_h:.1f} g/h\n"
        + f"Soot yield: {result.soot_g_per_h:.1f} g/h\n"
        + f"Aldehyde yield: {result.aldehyde_g_per_h:.1f} g/h\n"
        + f"Formaldehyde yield: {result.formaldehyde_g_per_h:.1f} g/h\n"
        + f"Benzene yield: {result.benzene_g_per_h:.2f} g/h\n"
        + f"PM2.5 yield: {result.pm25_g_per_h:.2f} g/h\n"
        + f"VOC yield: {result.total_voc_g_per_h:.1f} g/h\n"
        + f"Material compatibility: {result.material_compatibility_index:.3f}\n"
        + f"Seal degradation risk: {result.seal_degradation_risk:.3f}\n"
        + f"Corrosion risk: {result.corrosion_risk:.3f}\n"
        + f"Rubber swelling risk: {result.rubber_swelling_risk:.3f}\n"
        + f"Renewable fraction: {result.renewable_fraction:.2f}\n"
        + f"Renewable replacement rank: {result.renewable_replacement_score:.3f}\n"
        + f"Biomass yield: {result.biomass_yield_kg_fuel_per_kg_biomass:.2f} kg fuel/kg biomass\n"
        + f"Conversion efficiency: {result.conversion_efficiency:.2f}\n"
        + f"Catalyst cost: ${result.catalyst_cost_per_kg:.2f}/kg\n"
        + f"Coproduct credit: ${result.coproduct_credit_per_kg:.2f}/kg\n"
        + f"Toxicity index: {result.toxicity_index:.3f}\n"
        + f"Novel species risk: {result.novel_species_risk:.3f}\n"
        + f"Bench net power: {result.bench_net_power_kw:.2f} kW\n"
        + f"Friction losses: {result.friction_losses_kw:.2f} kW\n"
        + f"Pump / accessory load: {result.pump_power_kw:.2f} kW\n"
        + f"Heat rejection: {result.heat_rejection_kw:.2f} kW\n"
        + f"Cooling capacity: {result.cooling_capacity_kw:.2f} kW\n"
        + f"Coolant deltaT: {result.coolant_temp_rise_c:.1f} °C\n"
        + f"Oil deltaT: {result.oil_temp_rise_c:.1f} °C\n"
        + f"Knock / timing risk: {result.knock_risk:.3f}\n"
        + f"Fuel production route: {result.fuel_production_route}\n"
        + f"Fuel production cost per kg: ${result.fuel_production_cost_per_kg:.2f}/kg\n"
        + f"Fuel cost per hour: ${result.fuel_cost_per_h:.2f}/h\n"
        + f"Fuel cost per kWh: ${result.fuel_cost_per_kwh:.2f}/kWh\n"
        + f"FSOT score: {result.fsot_score:.3f}\n"
        + f"Remediation credit: ${result.remediation_credit_per_kg:.2f}/kg\n"
        + f"Remediation benefit score: {result.remediation_benefit_score:.3f}\n"
        + f"Production difficulty index: {result.production_difficulty_index:.3f}\n"
    )


def list_engines(specs: Dict[str, EngineSpec]) -> str:
    return "\n".join(
        f"- {engine.id}: {engine.name} ({engine.fuel_type})"
        for engine in specs.values()
    )


def list_fuel_profiles(fuels: Dict[str, FuelSpec]) -> str:
    return "\n".join(
        f"- {fuel.id}: {fuel.name} ({fuel.fuel_type}) - {fuel.description}"
        for fuel in fuels.values()
    )


def blend_fuel_profiles(
    base_fuels: List[FuelSpec],
    weights: List[float],
    blend_id: str,
    blend_name: str,
) -> FuelSpec:
    if len(base_fuels) != len(weights):
        raise ValueError("Number of fuels and weights must match.")
    total_weight = sum(weights)
    normalized = [w / total_weight for w in weights]
    blend = deepcopy(base_fuels[0])
    blend.id = blend_id
    blend.name = blend_name
    blend.description = "Blend of " + ", ".join(f.id for f in base_fuels)
    blend.production_route = "blend:" + "+".join(f.id for f in base_fuels)
    blend.renewable_source = "blend"

    def weighted(field: str) -> float:
        return sum(normalized[i] * getattr(base_fuels[i], field) for i in range(len(base_fuels)))

    blend.lhv_kj_per_kg = weighted("lhv_kj_per_kg")
    blend.stoich_afr = weighted("stoich_afr")
    blend.density_kg_m3 = weighted("density_kg_m3")
    blend.clean_index = weighted("clean_index")
    blend.emissions_index = weighted("emissions_index")
    blend.knock_resistance = weighted("knock_resistance")
    blend.octane_rating = weighted("octane_rating")
    blend.flame_speed_m_s = weighted("flame_speed_m_s")
    blend.volatility_index = weighted("volatility_index")
    blend.production_cost_per_kg = weighted("production_cost_per_kg")
    blend.process_energy_kj_per_kg = weighted("process_energy_kj_per_kg")
    blend.processing_cost_per_kj = weighted("processing_cost_per_kj")
    blend.overhead_cost_per_kg = weighted("overhead_cost_per_kg")
    blend.catalyst_cycle_cost_per_kg = weighted("catalyst_cycle_cost_per_kg")
    blend.coproduct_credit_per_kg = weighted("coproduct_credit_per_kg")
    blend.remediation_credit_per_kg = weighted("remediation_credit_per_kg")
    blend.biomass_yield_kg_fuel_per_kg_biomass = weighted("biomass_yield_kg_fuel_per_kg_biomass")
    blend.conversion_efficiency = weighted("conversion_efficiency")
    blend.renewable_fraction = weighted("renewable_fraction")

    composition_map: Dict[str, float] = {}
    for i, fuel in enumerate(base_fuels):
        for entry in fuel.composition:
            name = entry.get("name", "")
            if not name:
                continue
            composition_map[name] = composition_map.get(name, 0.0) + normalized[i] * entry.get("fraction", 0.0)
    blend.composition = [{"name": name, "fraction": frac} for name, frac in composition_map.items()]

    precursor_map: Dict[str, Dict[str, float]] = {}
    for i, fuel in enumerate(base_fuels):
        for precursor in fuel.precursors:
            name = precursor.get("name", "")
            if not name:
                continue
            if name not in precursor_map:
                precursor_map[name] = {"mass_kg": 0.0, "unit_cost": 0.0}
            precursor_map[name]["mass_kg"] += normalized[i] * precursor.get("mass_kg", 0.0)
            precursor_map[name]["unit_cost"] += normalized[i] * precursor.get("unit_cost", 0.0)
    blend.precursors = [
        {"name": name, "mass_kg": data["mass_kg"], "unit_cost": data["unit_cost"]}
        for name, data in precursor_map.items()
    ]

    byproducts_map: Dict[str, float] = {}
    for i, fuel in enumerate(base_fuels):
        for key, value in fuel.byproducts.items():
            byproducts_map[key] = byproducts_map.get(key, 0.0) + normalized[i] * value
    blend.byproducts = byproducts_map
    return blend


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulate engine performance with AFR, timing, and throttle."
    )
    parser.add_argument("--list-engines", action="store_true", help="List available engine specs.")
    parser.add_argument("--list-fuel-profiles", action="store_true", help="List available fuel profiles.")
    parser.add_argument("--engine", type=str, help="Engine ID to simulate.")
    parser.add_argument("--fuel-profile", type=str, help="Fuel profile ID to use for the simulation.")
    parser.add_argument("--fuel-profiles", type=str, help="Comma-separated fuel profile IDs for comparison or blending.")
    parser.add_argument("--blend-fuels", action="store_true", help="Build and simulate a fuel blend from the selected fuel profiles.")
    parser.add_argument("--blend-weights", type=str, help="Comma-separated blend weights for --blend-fuels.")
    parser.add_argument("--blend-sweep", action="store_true", help="Run an automated blend weight sweep for the selected fuel profiles.")
    parser.add_argument("--blend-sweep-step", type=float, default=0.1, help="Blend sweep weight resolution (default 0.1).")
    parser.add_argument("--blend-sweep-top", type=int, default=10, help="Number of top blend candidates to display from the sweep.")
    parser.add_argument("--results-output", type=str, help="Base path to save comparison or sweep results as JSON and CSV for repeat tracking.")
    parser.add_argument("--ground-fuel-profiles", action="store_true", help="Ground selected fuel profiles from measured compound properties and save grounded fuel profiles.")
    parser.add_argument("--grounded-output", type=str, help="Path to save grounded fuel profiles JSON when using --ground-fuel-profiles.")
    parser.add_argument("--fetch-fuel-data", action="store_true", help="Fetch real compound data for fuel profile placeholders from PubChem/NIST.")
    parser.add_argument("--fuel-profile-ids", type=str, help="Comma-separated fuel profile IDs to fetch compound lookup data for when using --fetch-fuel-data.")
    parser.add_argument("--save-fuel-data", type=str, help="Write compound lookup results to a JSON file.")
    parser.add_argument("--compare-fuels", action="store_true", help="Run the same engine with multiple fuel profiles in parallel.")
    parser.add_argument("--sweep-hemp-advanced", action="store_true", help="Run a small parameter sweep of the advanced hemp route.")
    parser.add_argument("--refine-hemp-route", action="store_true", help="Run a more detailed hemp route refinement sweep with AFR and timing tuning.")
    parser.add_argument("--monte-carlo", action="store_true", help="Run a Monte Carlo sweep of AFR, timing, and throttle.")
    parser.add_argument("--trials", type=int, default=100, help="Number of Monte Carlo trials.")
    parser.add_argument("--min-afr", type=float, default=10.0, help="Monte Carlo minimum AFR.")
    parser.add_argument("--max-afr", type=float, default=18.0, help="Monte Carlo maximum AFR.")
    parser.add_argument("--min-spark", type=float, default=12.0, help="Monte Carlo minimum spark advance.")
    parser.add_argument("--max-spark", type=float, default=25.0, help="Monte Carlo maximum spark advance.")
    parser.add_argument("--min-throttle", type=float, default=0.4, help="Monte Carlo minimum throttle.")
    parser.add_argument("--max-throttle", type=float, default=1.0, help="Monte Carlo maximum throttle.")
    parser.add_argument("--rpm", type=int, help="Engine speed in RPM; defaults to engine rated RPM.")
    parser.add_argument("--min-rpm", type=int, help="Minimum RPM for engine scan mode.")
    parser.add_argument("--max-rpm", type=int, help="Maximum RPM for engine scan mode.")
    parser.add_argument("--rpm-step", type=int, default=200, help="RPM step size for scan mode (default 200).")
    parser.add_argument("--throttle", type=float, default=1.0, help="Throttle fraction 0.0-1.0.")
    parser.add_argument("--afr", type=float, help="Air/fuel ratio.")
    parser.add_argument("--spark-advance", type=float, help="Ignition timing in degrees BTDC.")
    parser.add_argument("--scan", action="store_true", help="Run a basic RPM/throttle performance scan.")
    parser.add_argument("--detailed", action="store_true", help="Display detailed bench simulation results including oil/coolant and friction losses.")
    parser.add_argument("--baseline-file", type=str, help="Path to a public baseline CSV file such as EPA fuel economy data.")
    parser.add_argument("--baseline-query", type=str, help="Optional text query to match baseline records by make/model or engine name.")
    parser.add_argument("--baseline-year", type=int, help="Optional model year to narrow baseline validation matches.")
    parser.add_argument("--baseline-max-results", type=int, default=10, help="Maximum baseline records to display.")
    parser.add_argument("--validate-baseline", action="store_true", help="Validate the selected engine against a public baseline CSV.")
    parser.add_argument("--baseline-calibrate-only", action="store_true", help="Use matched baseline power to calibrate the engine without printing all matched records.")
    parser.add_argument("--baseline-eco-compare", action="store_true", help="Compare the selected engine and fuel to baseline CO2/fuel-economy records.")
    return parser.parse_args()


def scan_engine(
    engine: EngineSpec,
    fuel: FuelSpec,
    min_rpm: Optional[int] = None,
    max_rpm: Optional[int] = None,
    step: int = 200,
) -> List[EngineSimulationResult]:
    min_rpm = max(800, min_rpm or engine.idle_rpm or 800)
    max_rpm = min(engine.max_rpm, max_rpm or engine.max_rpm)
    step = max(50, min(step, engine.max_rpm - min_rpm or 200))
    if min_rpm > max_rpm:
        min_rpm = min(800, max_rpm)
    results = []
    current = min_rpm
    while current <= max_rpm:
        results.append(simulate_engine_cycle(
            engine,
            rpm=current,
            throttle=1.0,
            fuel=fuel,
            afr=fuel.stoich_afr,
            spark_advance_deg=engine.optimal_spark_advance_deg,
        ))
        current += step
    if results and results[-1].rpm != max_rpm:
        results.append(simulate_engine_cycle(
            engine,
            rpm=max_rpm,
            throttle=1.0,
            fuel=fuel,
            afr=fuel.stoich_afr,
            spark_advance_deg=engine.optimal_spark_advance_deg,
        ))
    return results


def monte_carlo_sweep(
    engine: EngineSpec,
    fuel: FuelSpec,
    n_trials: int,
    min_afr: float,
    max_afr: float,
    min_spark: float,
    max_spark: float,
    min_throttle: float,
    max_throttle: float,
) -> List[EngineSimulationResult]:
    results: List[EngineSimulationResult] = []
    for _ in range(n_trials):
        afr = random.uniform(min_afr, max_afr)
        spark = random.uniform(min_spark, max_spark)
        throttle = random.uniform(min_throttle, max_throttle)
        rpm = random.randint(1200, engine.max_rpm)
        results.append(simulate_engine_cycle(
            engine,
            rpm=rpm,
            throttle=throttle,
            fuel=fuel,
            afr=afr,
            spark_advance_deg=spark,
        ))
    return results


def summarize_monte_carlo(results: List[EngineSimulationResult]) -> str:
    if not results:
        return "No Monte Carlo results."
    best = max(results, key=lambda r: r.bench_net_power_kw)
    efficient = max(results, key=lambda r: r.thermal_efficiency)
    cleanest = min(results, key=lambda r: r.toxicity_index)
    cheapest = min(results, key=lambda r: r.fuel_cost_per_kwh)
    return (
        f"Monte Carlo summary:\n"
        f"  Best net power: {best.bench_net_power_kw:.2f} kW at {best.rpm} RPM\n"
        f"  Best efficiency: {efficient.thermal_efficiency:.3f}\n"
        f"  Lowest toxicity index: {cleanest.toxicity_index:.3f}\n"
        f"  Lowest fuel cost: ${cheapest.fuel_cost_per_kwh:.2f}/kWh\n"
        f"  Worst CO yield: {max(results, key=lambda r: r.co_g_per_h).co_g_per_h:.1f} g/h\n"
        f"  Worst NOx yield: {max(results, key=lambda r: r.nox_g_per_h).nox_g_per_h:.1f} g/h\n"
    )


def summarize_comparison(results: List[EngineSimulationResult]) -> str:
    if not results:
        return "No comparison results."
    sorted_results = sorted(
        results,
        key=lambda result: result.renewable_replacement_score,
        reverse=True,
    )
    lines = ["Comparison summary by renewable replacement rank:"]
    for index, result in enumerate(sorted_results, start=1):
        lines.append(
            f"  {index}. {result.fuel_profile_id}: "
            f"rank={result.renewable_replacement_score:.3f}, "
            f"fsot={result.fsot_score:.3f}, "
            f"cost={result.fuel_cost_per_kwh:.2f} $/kWh, "
            f"tox={result.toxicity_index:.3f}, "
            f"renew={result.renewable_fraction:.2f}"
        )
    return "\n".join(lines)


def normalize_baseline_record(record: Dict[str, str]) -> Dict[str, str]:
    return {k.strip().lower(): (v.strip() if v is not None else "") for k, v in record.items()}


def parse_numeric_value(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    match = re.search(r"(-?\d+(?:\.\d+)?)", value.replace(",", ""))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def load_baseline_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Baseline CSV not found at {path}")
    with path.open("r", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [normalize_baseline_record(row) for row in reader if any(row.values())]


def get_baseline_field(record: Dict[str, str], keys: List[str]) -> Optional[str]:
    for key in keys:
        value = record.get(key.lower())
        if value:
            return value
    return None


def parse_baseline_power_kw(record: Dict[str, str]) -> Optional[float]:
    kw = parse_numeric_value(get_baseline_field(record, ["kw", "power_kw", "power (kw)", "engine_kw", "rated_kw"]))
    if kw is not None and kw > 0.0:
        return kw
    hp = parse_numeric_value(get_baseline_field(record, ["horsepower", "hp", "power", "rated_horsepower", "engine_hp", "hpv"]))
    if hp is not None and hp > 0.0:
        return hp * 0.745699872
    return None


def select_baseline_calibration_record(records: List[Dict[str, str]]) -> tuple[Optional[Dict[str, str]], Optional[float]]:
    for record in records:
        power_kw = parse_baseline_power_kw(record)
        if power_kw is not None:
            return record, power_kw
    return None, None


def record_matches_query(record: Dict[str, str], query: str, year: Optional[int] = None) -> bool:
    if year is not None:
        year_value = get_baseline_field(record, ["year", "modelyear", "model_year"])
        if year_value and str(year) != year_value:
            return False
    row_text = " ".join(str(v) for v in record.values()).lower()
    return query.lower() in row_text


def find_baseline_matches(
    records: List[Dict[str, str]],
    query: str,
    year: Optional[int] = None,
    max_results: int = 10,
) -> List[Dict[str, str]]:
    matches: List[Dict[str, str]] = []
    for record in records:
        if record_matches_query(record, query, year):
            matches.append(record)
            if len(matches) >= max_results:
                break
    return matches


def summarize_baseline_matches(records: List[Dict[str, str]], engine: EngineSpec) -> str:
    if not records:
        return "No baseline matches found."
    lines = [f"Baseline matches for engine: {engine.name}"]
    for record in records:
        hp = parse_numeric_value(get_baseline_field(record, ["horsepower", "hp", "power"]))
        kW = parse_numeric_value(get_baseline_field(record, ["kw", "power_kw", "power (kw)"]))
        make = get_baseline_field(record, ["make", "manufacturer"])
        model = get_baseline_field(record, ["model", "model_name"])
        year = get_baseline_field(record, ["year", "modelyear", "model_year"])
        displacement = get_baseline_field(record, ["displ", "displacement", "engine_displacement"])
        cylinders = get_baseline_field(record, ["cylinders", "cylinder"])
        fuel_type = get_baseline_field(record, ["fueltype", "fuel type", "fuel"])
        mpg_city = get_baseline_field(record, ["city08", "comb08", "highway08"])
        co2_value = parse_baseline_co2_gpm(record)
        line = (
            f"  {year or 'year?'} {make or 'make?'} {model or 'model?'} | "
            f"disp={displacement or 'n/a'} | cylinders={cylinders or 'n/a'} | fuel={fuel_type or 'n/a'} | "
        )
        if hp is not None:
            line += f"hp={hp:.1f} | "
        if kW is not None:
            line += f"kW={kW:.1f} | "
        if mpg_city:
            line += f"MPG/comb={mpg_city} | "
        if co2_value is not None:
            line += f"CO2={co2_value:.1f}"
        lines.append(line.strip())
    return "\n".join(lines)


def parse_baseline_mpg(record: Dict[str, str]) -> Optional[float]:
    for key in ["comb08", "city08", "highway08", "comb08u", "city08u", "highway08u"]:
        mpg = parse_numeric_value(get_baseline_field(record, [key]))
        if mpg is not None and mpg > 0.0:
            return mpg
    return None


def parse_baseline_co2_gpm(record: Dict[str, str]) -> Optional[float]:
    for key in [
        "co2",
        "co2 tailpipe gpm",
        "co2 tailpipe agpm",
        "co2tailpipegpm",
        "co2tailpipeagpm",
    ]:
        co2 = parse_numeric_value(get_baseline_field(record, [key]))
        if co2 is not None and co2 > 0.0:
            return co2
    return None


def select_baseline_eco_record(records: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    for record in records:
        if parse_baseline_mpg(record) is not None or parse_baseline_co2_gpm(record) is not None:
            return record
    return None


def summarize_baseline_eco_comparison(
    record: Dict[str, str],
    engine: EngineSpec,
    fuel: FuelSpec,
    result: EngineSimulationResult,
) -> str:
    mpg = parse_baseline_mpg(record)
    co2_gpm = parse_baseline_co2_gpm(record)
    make = get_baseline_field(record, ["make", "manufacturer"])
    model = get_baseline_field(record, ["model", "model_name"])
    year = get_baseline_field(record, ["year", "modelyear", "model_year"])
    fuel_type = get_baseline_field(record, ["fueltype", "fuel type", "fuel"])
    lines = [
        f"Baseline eco comparison for {year or 'year?'} {make or 'make?'} {model or 'model?'}:",
        f"  Fuel type: {fuel_type or 'unknown'}",
    ]
    if mpg is not None:
        lines.append(f"  Combined MPG: {mpg:.1f}")
    if co2_gpm is not None:
        lines.append(f"  CO2: {co2_gpm:.1f} g/mi")
    lines.append("")
    lines.append("Simulated engine result at rated RPM:")
    lines.append(f"  Engine: {engine.name}")
    lines.append(f"  Fuel profile: {fuel.id}")
    lines.append(f"  RPM: {result.rpm}")
    lines.append(f"  Brake power: {result.brake_power_kw:.1f} kW ({kw_to_hp(result.brake_power_kw):.1f} hp)")
    lines.append(f"  Thermal efficiency: {result.thermal_efficiency:.3f}")
    lines.append(f"  BSFC: {result.bsfc_g_kwh:.1f} g/kWh")
    lines.append(f"  Fuel flow: {result.fuel_flow_kg_s * 3600:.2f} kg/h")
    co2_proxy = result.fuel_flow_kg_s * 3600.0 * 3.15
    lines.append(f"  Proxy CO2 emissions: {co2_proxy:.1f} g/h")
    lines.append(f"  CO yield: {result.co_g_per_h:.1f} g/h")
    return "\n".join(lines)


def summarize_peak_power_results(peak_results: List[tuple[FuelSpec, EngineSimulationResult]]) -> str:
    if not peak_results:
        return "No peak power results."
    lines = ["Peak power summary table:"]
    lines.append("  Fuel ID                          | RPM  | Power (kW / hp) | Torque (Nm / ft-lb)")
    lines.append("  ---------------------------------|------|-----------------|------------------")
    for fuel, result in peak_results:
        lines.append(
            f"  {fuel.id:32} | {result.rpm:4} | "
            f"{result.brake_power_kw:6.1f} kW / {kw_to_hp(result.brake_power_kw):5.1f} hp | "
            f"{result.torque_nm:6.1f} Nm / {nm_to_ftlb(result.torque_nm):5.1f} ft-lb"
        )
    return "\n".join(lines)


def generate_blend_weight_combinations(count: int, step: float) -> List[List[float]]:
    if count < 1:
        return []
    if step <= 0.0 or step > 1.0:
        raise ValueError("Blend sweep step must be between 0 and 1.")
    units = int(round(1.0 / step))
    if units < 1:
        units = 1
    actual_step = 1.0 / units
    combinations: List[List[float]] = []

    def recurse(index: int, remaining_units: int, current: List[float]) -> None:
        if index == count - 1:
            combinations.append(current + [remaining_units / units])
            return
        for unit in range(remaining_units + 1):
            recurse(index + 1, remaining_units - unit, current + [unit / units])

    recurse(0, units, [])
    return combinations


def pareto_frontier(
    candidates: List[tuple[List[float], EngineSimulationResult]]
) -> List[tuple[List[float], EngineSimulationResult]]:
    frontier: List[tuple[List[float], EngineSimulationResult]] = []
    for weights, result in candidates:
        dominated = False
        for _, other in candidates:
            if (
                other.fuel_cost_per_kwh <= result.fuel_cost_per_kwh
                and other.toxicity_index <= result.toxicity_index
                and other.fsot_score >= result.fsot_score
                and (
                    other.fuel_cost_per_kwh < result.fuel_cost_per_kwh
                    or other.toxicity_index < result.toxicity_index
                    or other.fsot_score > result.fsot_score
                )
            ):
                dominated = True
                break
        if not dominated:
            frontier.append((weights, result))
    return sorted(
        frontier,
        key=lambda pair: (pair[1].fuel_cost_per_kwh, pair[1].toxicity_index, -pair[1].fsot_score),
    )


def blend_sweep(
    engine: EngineSpec,
    fuels: List[FuelSpec],
    step: float = 0.1,
    top_n: int = 10,
    rpm: int = 2200,
    throttle: float = 1.0,
    afr: Optional[float] = None,
    spark_advance: Optional[float] = None,
) -> tuple[List[tuple[List[float], EngineSimulationResult]], List[tuple[List[float], EngineSimulationResult]]]:
    weight_combos = generate_blend_weight_combinations(len(fuels), step)
    if not weight_combos:
        return [], []
    results: List[tuple[List[float], EngineSimulationResult]] = []
    for weights in weight_combos:
        blend = blend_fuel_profiles(
            fuels,
            weights,
            blend_id="blend_" + "_".join(f.id for f in fuels),
            blend_name=" + ".join(f.id for f in fuels),
        )
        result = simulate_engine_cycle(
            engine,
            rpm=rpm,
            throttle=throttle,
            fuel=blend,
            afr=afr if afr is not None else blend.stoich_afr,
            spark_advance_deg=spark_advance if spark_advance is not None else engine.optimal_spark_advance_deg,
        )
        results.append((weights, result))
    sorted_results = sorted(
        results,
        key=lambda pair: pair[1].fsot_score,
        reverse=True,
    )
    pareto = pareto_frontier(results)
    return sorted_results[:top_n], pareto


def summarize_blend_sweep(
    sweep_results: List[tuple[List[float], EngineSimulationResult]],
    pareto_results: List[tuple[List[float], EngineSimulationResult]],
) -> str:
    if not sweep_results:
        return "No blend sweep results."
    lines = ["Blend sweep top candidates by FSOT score:"]
    for index, (weights, result) in enumerate(sweep_results, start=1):
        weight_str = ",".join(f"{w:.2f}" for w in weights)
        lines.append(
            f"  {index}. {result.fuel_profile_id} weights=[{weight_str}]: "
            f"fsot={result.fsot_score:.3f}, "
            f"rank={result.renewable_replacement_score:.3f}, "
            f"cost={result.fuel_cost_per_kwh:.2f} $/kWh, "
            f"tox={result.toxicity_index:.3f}, renew={result.renewable_fraction:.2f}"
        )
    lines.append("")
    lines.append(f"Pareto frontier candidates in sweep: {len(pareto_results)}")
    for index, (weights, result) in enumerate(pareto_results[:10], start=1):
        weight_str = ",".join(f"{w:.2f}" for w in weights)
        lines.append(
            f"  P{index}. weights=[{weight_str}]: "
            f"fsot={result.fsot_score:.3f}, "
            f"cost={result.fuel_cost_per_kwh:.2f}, tox={result.toxicity_index:.3f}, "
            f"rank={result.renewable_replacement_score:.3f}"
        )
    return "\n".join(lines)


def make_hemp_advanced_variant(
    base: FuelSpec,
    ether_frac: float,
    ester_frac: float,
    cofactor_frac: float,
    catalyst_cost: float,
    coproduct_credit: float,
    biomass_yield: float = 0.55,
) -> FuelSpec:
    variant = deepcopy(base)
    lignin_frac = 0.18
    waste_syrup_frac = max(0.0, 1.0 - lignin_frac - ether_frac - ester_frac - cofactor_frac)
    variant.composition = [
        {"name": "Glucose", "fraction": waste_syrup_frac},
        {"name": "Guaiacol", "fraction": lignin_frac},
        {"name": "Diethyl ether", "fraction": ether_frac},
        {"name": "Ethyl acetate", "fraction": ester_frac},
        {"name": "Ethyl acetate", "fraction": cofactor_frac},
    ]
    variant.catalyst_cycle_cost_per_kg = catalyst_cost
    variant.coproduct_credit_per_kg = coproduct_credit
    variant.process_energy_kj_per_kg = 12800.0 + (ether_frac - 0.08) * 1100.0 + (ester_frac - 0.12) * 900.0 - (biomass_yield - 0.55) * 600.0
    variant.overhead_cost_per_kg = 0.13
    variant.production_cost_per_kg = max(0.95, 1.35 + catalyst_cost * 0.12 - coproduct_credit * 0.40 - (biomass_yield - 0.55) * 0.60)
    variant.biomass_yield_kg_fuel_per_kg_biomass = biomass_yield
    variant.conversion_efficiency = clamp(0.82 + (biomass_yield - 0.55) * 0.3, 0.80, 0.96)
    variant.renewable_fraction = 0.99
    variant.production_route = "hemp_waste_refined_lignocellulosic"
    variant.byproducts = {
        "co_g_per_kg": 15.0 * (1.0 - 0.03 * (ester_frac - 0.10) + 0.015 * (ether_frac - 0.10)),
        "nox_g_per_kg": 7.2 * (1.0 - 0.02 * (ester_frac - 0.10)),
        "soot_g_per_kg": 3.4 * (1.0 - 0.025 * (ester_frac - 0.10) + 0.01 * (ether_frac - 0.10)),
        "aldehyde_g_per_kg": 4.3 * (1.0 - 0.035 * (ester_frac - 0.10) + 0.018 * (ether_frac - 0.10)),
    }
    return variant


def sweep_hemp_refined(
    engine: EngineSpec,
    base: FuelSpec,
) -> List[EngineSimulationResult]:
    ether_options = [0.05, 0.08, 0.11]
    ester_options = [0.09, 0.12, 0.15]
    cofactor_options = [0.05, 0.09, 0.13]
    catalyst_options = [0.03, 0.05, 0.07]
    coproduct_options = [0.12, 0.16, 0.20]
    biomass_options = [0.50, 0.55, 0.60]
    afr_options = [12.0, 12.2, 12.4, 12.6]
    spark_options = [18.0, 19.0, 20.0]
    results: List[EngineSimulationResult] = []
    for ether_frac in ether_options:
        for ester_frac in ester_options:
            for cofactor_frac in cofactor_options:
                if ether_frac + ester_frac + cofactor_frac > 0.85:
                    continue
                for catalyst_cost in catalyst_options:
                    for coproduct_credit in coproduct_options:
                        for biomass_yield in biomass_options:
                            variant = make_hemp_advanced_variant(
                                base,
                                ether_frac=ether_frac,
                                ester_frac=ester_frac,
                                cofactor_frac=cofactor_frac,
                                catalyst_cost=catalyst_cost,
                                coproduct_credit=coproduct_credit,
                                biomass_yield=biomass_yield,
                            )
                            for afr in afr_options:
                                for spark in spark_options:
                                    result = simulate_engine_cycle(
                                        engine,
                                        rpm=2200,
                                        throttle=1.0,
                                        fuel=variant,
                                        afr=afr,
                                        spark_advance_deg=spark,
                                    )
                                    result.fuel_profile_id = (
                                        f"{base.id}_refined_e{int(ether_frac*100)}_es{int(ester_frac*100)}_c{int(cofactor_frac*100)}_b{int(biomass_yield*100)}_afr{int(afr*10)}_s{int(spark)}"
                                    )
                                    results.append(result)
    return results


def summarize_hemp_refined_sweep(results: List[EngineSimulationResult]) -> str:
    if not results:
        return "No refined hemp sweep results."
    sorted_results = sorted(results, key=lambda r: r.renewable_replacement_score, reverse=True)
    lines = ["Refined hemp route results:"]
    for result in sorted_results[:12]:
        lines.append(
            f"  {result.fuel_profile_id}: rank={result.renewable_replacement_score:.3f}, "
            f"cost={result.fuel_cost_per_kwh:.2f} $/kWh, "
            f"CO={result.co_g_per_h:.1f} g/h, NOx={result.nox_g_per_h:.1f} g/h, "
            f"eff={result.thermal_efficiency:.3f}, afr={result.afr:.1f}, spark={result.spark_advance_deg:.1f}"
        )
    return "\n".join(lines)


def sweep_hemp_advanced(
    engine: EngineSpec,
    base: FuelSpec,
) -> List[EngineSimulationResult]:
    return sweep_hemp_refined(engine, base)


def summarize_hemp_sweep(results: List[EngineSimulationResult]) -> str:
    if not results:
        return "No hemp sweep results."
    sorted_results = sorted(results, key=lambda r: r.renewable_replacement_score, reverse=True)
    lines = ["Advanced hemp route sweep results:"]
    for result in sorted_results[:10]:
        lines.append(
            f"  {result.fuel_profile_id}: rank={result.renewable_replacement_score:.3f}, "
            f"cost={result.fuel_cost_per_kwh:.2f}, co={result.co_g_per_h:.1f}, "
            f"nox={result.nox_g_per_h:.1f}, voc={result.total_voc_g_per_h:.1f}"
        )
    return "\n".join(lines)


def calibrate_engine_power(
    engine: EngineSpec,
    fuels: Dict[str, FuelSpec],
    baseline_record: Optional[Dict[str, str]] = None,
) -> None:
    if engine.power_calibration_factor != 1.0:
        return
    base_fuel = fuels.get(engine.default_fuel_profile_id)
    if base_fuel is None:
        return
    if engine.rated_rpm <= 0:
        return
    raw = simulate_engine_cycle(
        engine,
        rpm=engine.rated_rpm,
        throttle=1.0,
        fuel=base_fuel,
        afr=base_fuel.stoich_afr,
        spark_advance_deg=engine.optimal_spark_advance_deg,
    )
    target_kw = engine.max_power_kw
    if baseline_record is not None:
        baseline_kw = parse_baseline_power_kw(baseline_record)
        if baseline_kw is not None:
            target_kw = baseline_kw
    if raw.brake_power_kw > 0.01:
        factor = target_kw / raw.brake_power_kw
        engine.power_calibration_factor = clamp(factor, 0.75, 1.5)


def main() -> None:
    specs = load_engine_specs()
    fuels = load_fuel_profiles()
    args = parse_args()
    if args.list_engines:
        print(list_engines(specs))
        return
    if args.list_fuel_profiles:
        print(list_fuel_profiles(fuels))
        return
    if args.ground_fuel_profiles:
        selected_ids = [fid.strip() for fid in (args.fuel_profile_ids or args.fuel_profiles or "").split(",") if fid.strip()]
        if not selected_ids:
            selected_ids = list(fuels.keys())
        grounded_profiles: List[Dict[str, Any]] = []
        for fid in selected_ids:
            fuel_case = fuels.get(fid)
            if fuel_case is None:
                print(f"- Fuel profile '{fid}' not found; skipping.")
                continue
            grounded = ground_fuel_profile(fuel_case)
            grounded_profiles.append({**grounded.__dict__})
            print(f"Grounded fuel profile: {grounded.id} -> LHV={grounded.lhv_kj_per_kg:.1f} kJ/kg, AFR={grounded.stoich_afr:.2f}, density={grounded.density_kg_m3:.1f} kg/m3")
        output_path = Path(args.grounded_output or "fuel_profiles_grounded.json")
        output_path.write_text(json.dumps({"fuel_profiles": grounded_profiles}, indent=2))
        print(f"Wrote grounded fuel profiles to {output_path}")
        return
    if args.fetch_fuel_data:
        selected_ids = [fid.strip() for fid in (args.fuel_profile_ids or "").split(",") if fid.strip()]
        if not selected_ids:
            selected_ids = list(fuels.keys())
        collected: Dict[str, Any] = {}
        for fid in selected_ids:
            fuel = fuels.get(fid)
            if fuel is None:
                print(f"- Fuel profile '{fid}' not found; skipping.")
                continue
            collected[fid] = collect_fuel_profile_real_data(fuel)
            print(format_fuel_profile_real_data(collected[fid]))
            print()
        if args.save_fuel_data:
            output_path = Path(args.save_fuel_data)
            output_path.write_text(json.dumps(collected, indent=2))
            print(f"Wrote real compound lookup results to {output_path}")
        return
    if not args.engine:
        print("Use --engine ENGINE_ID or --list-engines to see available options.")
        return
    engine = specs.get(args.engine)
    if engine is None:
        print(f"Engine '{args.engine}' not found. Use --list-engines.")
        return
    fuel_profile_id = args.fuel_profile or engine.default_fuel_profile_id
    fuel = fuels.get(fuel_profile_id)
    if fuel is None:
        print(f"Fuel profile '{fuel_profile_id}' not found. Use --list-fuel-profiles.")
        return
    if args.validate_baseline or args.baseline_calibrate_only or args.baseline_eco_compare:
        if not args.baseline_file:
            print("Use --baseline-file PATH to provide an EPA/public baseline CSV for validation.")
            return
        records = load_baseline_csv(Path(args.baseline_file))
        query = args.baseline_query or engine.name
        actual_max_results = args.baseline_max_results
        if args.baseline_calibrate_only and args.baseline_max_results == 10:
            actual_max_results = 3
        matches = find_baseline_matches(records, query, year=args.baseline_year, max_results=actual_max_results)
        if args.validate_baseline:
            print(summarize_baseline_matches(matches, engine))
        if args.baseline_eco_compare:
            eco_record = select_baseline_eco_record(matches)
            if eco_record is not None:
                result = simulate_engine_cycle(
                    engine,
                    rpm=engine.rated_rpm,
                    throttle=1.0,
                    fuel=fuel,
                    afr=fuel.stoich_afr,
                    spark_advance_deg=engine.optimal_spark_advance_deg,
                )
                print(summarize_baseline_eco_comparison(eco_record, engine, fuel, result))
            else:
                print("No baseline record with CO2 or MPG values found; eco comparison skipped.")
        if args.validate_baseline or args.baseline_calibrate_only:
            if matches:
                calibration_record, calibration_kw = select_baseline_calibration_record(matches)
                if calibration_record is not None and calibration_kw is not None:
                    calibrate_engine_power(engine, fuels, baseline_record=calibration_record)
                    print(
                        f"Calibrated engine power using baseline match: {calibration_kw:.1f} kW "
                        f"(power_calibration_factor={engine.power_calibration_factor:.3f})."
                    )
                else:
                    print("No numeric horsepower/kW found in matched baseline records; calibration skipped.")
            elif args.baseline_calibrate_only:
                print("No matching baseline records found; calibration skipped.")
        return
    calibrate_engine_power(engine, fuels)

    selected_rpm = args.rpm if args.rpm is not None else engine.rated_rpm
    if args.sweep_hemp_advanced or args.refine_hemp_route:
        base_profile_id = args.fuel_profile or "fsot_hemp_waste_advanced"
        base = fuels.get(base_profile_id)
        if base is None:
            print(f"Hemp base fuel profile '{base_profile_id}' not found.")
            return
        if args.refine_hemp_route:
            print(f"Running refined hemp route sweep for engine: {engine.name} using base fuel: {base.id}\n")
            sweep_results = sweep_hemp_refined(engine, base)
            print(summarize_hemp_refined_sweep(sweep_results))
            if args.results_output:
                records = [result_to_record(engine, result, mode="refine_hemp_route") for result in sweep_results]
                save_results(args.results_output, {
                    "mode": "refine_hemp_route",
                    "engine": engine.id,
                    "base_fuel_profile": base.id,
                    "record_count": len(records),
                }, records)
                print(f"Saved refined hemp sweep results to {args.results_output}.json and .csv")
        else:
            print(f"Running advanced hemp route sweep for engine: {engine.name} using base fuel: {base.id}\n")
            sweep_results = sweep_hemp_advanced(engine, base)
            print(summarize_hemp_sweep(sweep_results))
            if args.results_output:
                records = [result_to_record(engine, result, mode="advanced_hemp_sweep") for result in sweep_results]
                save_results(args.results_output, {
                    "mode": "advanced_hemp_sweep",
                    "engine": engine.id,
                    "base_fuel_profile": base.id,
                    "record_count": len(records),
                }, records)
                print(f"Saved advanced hemp sweep results to {args.results_output}.json and .csv")
        return
    if args.blend_sweep:
        if not args.fuel_profiles:
            print("Use --fuel-profiles with comma-separated fuel IDs to sweep.")
            return
        profile_ids = [fid.strip() for fid in args.fuel_profiles.split(",") if fid.strip()]
        selected = []
        for fid in profile_ids:
            fuel_case = fuels.get(fid)
            if fuel_case is None:
                print(f"Unknown fuel profile '{fid}' in blend sweep; skipping.")
                continue
            selected.append(fuel_case)
        if len(selected) < 2:
            print("Blend sweep requires at least two valid fuel profiles.")
            return
        sweep_top_results, pareto_results = blend_sweep(
            engine=engine,
            fuels=selected,
            step=args.blend_sweep_step,
            top_n=args.blend_sweep_top,
            rpm=selected_rpm,
            throttle=args.throttle,
            afr=args.afr,
            spark_advance=args.spark_advance,
        )
        print(f"Running blend sweep for: {', '.join(f.id for f in selected)}")
        print(summarize_blend_sweep(sweep_top_results, pareto_results))
        if args.results_output:
            all_records = []
            pareto_weights = [weights for weights, _ in pareto_results]
            for weights, result in sweep_top_results:
                record = result_to_record(engine, result, mode="blend_sweep", weights=weights)
                record["pareto_candidate"] = weights in pareto_weights
                all_records.append(record)
            for weights, result in pareto_results:
                if weights not in [w for w, _ in sweep_top_results]:
                    record = result_to_record(engine, result, mode="blend_sweep", weights=weights)
                    record["pareto_candidate"] = True
                    all_records.append(record)
            save_results(args.results_output, {
                "mode": "blend_sweep",
                "engine": engine.id,
                "fuel_profiles": [f.id for f in selected],
                "weights_step": args.blend_sweep_step,
                "top_n": args.blend_sweep_top,
                "record_count": len(all_records),
            }, all_records)
        return
    if args.blend_fuels:
        if not args.fuel_profiles:
            print("Use --fuel-profiles with comma-separated fuel IDs to blend.")
            return
        profile_ids = [fid.strip() for fid in args.fuel_profiles.split(",") if fid.strip()]
        weights = [1.0] * len(profile_ids)
        if args.blend_weights:
            try:
                weights = [float(w.strip()) for w in args.blend_weights.split(",") if w.strip()]
            except ValueError:
                print("Invalid --blend-weights values. Use comma-separated numbers.")
                return
        if len(weights) != len(profile_ids):
            print("Blend weights count must match the number of blended fuel profiles.")
            return
        selected = []
        for fid in profile_ids:
            fuel_case = fuels.get(fid)
            if fuel_case is None:
                print(f"Unknown fuel profile '{fid}' in blend; skipping.")
                continue
            selected.append(fuel_case)
        if not selected:
            print("No valid fuel profiles found for blending.")
            return
        blend = blend_fuel_profiles(selected, weights, "blend_" + "_".join(fid for fid in profile_ids), " + ".join(f.id for f in selected))
        afr = args.afr if args.afr is not None else blend.stoich_afr
        spark = args.spark_advance if args.spark_advance is not None else engine.optimal_spark_advance_deg
        result = simulate_engine_cycle(
            engine,
            rpm=selected_rpm,
            throttle=args.throttle,
            fuel=blend,
            afr=afr,
            spark_advance_deg=spark,
            detailed=args.detailed,
        )
        print(f"=== Blended fuel: {blend.name} ({blend.id}) ===")
        print(format_result(engine, result, detailed=args.detailed))
        print("\nComponent fuel results:")
        component_results = []
        for fuel_case in selected:
            comp_result = simulate_engine_cycle(
                engine,
                rpm=args.rpm,
                throttle=args.throttle,
                fuel=fuel_case,
                afr=args.afr if args.afr is not None else fuel_case.stoich_afr,
                spark_advance_deg=spark,
            )
            component_results.append(comp_result)
            print(f"--- {fuel_case.name} ({fuel_case.id}) ---")
            print(format_result(engine, comp_result, detailed=False))
            print()
        compare_results = component_results + [result]
        print("\nBlend comparison summary:")
        print(summarize_comparison(compare_results))
        return
    selected_rpm = args.rpm if args.rpm is not None else engine.rated_rpm
    if args.compare_fuels:
        chosen_ids = []
        if args.fuel_profiles:
            chosen_ids = [fid.strip() for fid in args.fuel_profiles.split(",") if fid.strip()]
        else:
            chosen_ids = list(fuels.keys())
        print(f"Comparing fuel profiles for engine: {engine.name}\n")
        compare_results: List[EngineSimulationResult] = []
        peak_results: List[tuple[FuelSpec, EngineSimulationResult]] = []
        for fid in chosen_ids:
            fuel_case = fuels.get(fid)
            if fuel_case is None:
                print(f"- Skipping unknown fuel profile: {fid}")
                continue
            if args.monte_carlo:
                print(f"--- Monte Carlo for fuel: {fuel_case.name} ({fuel_case.id}) ---")
                mc_results = monte_carlo_sweep(
                    engine,
                    fuel_case,
                    args.trials,
                    args.min_afr,
                    args.max_afr,
                    args.min_spark,
                    args.max_spark,
                    args.min_throttle,
                    args.max_throttle,
                )
                print(summarize_monte_carlo(mc_results))
                if args.detailed:
                    for i, row in enumerate(mc_results[:3], start=1):
                        print(f"\nTrial {i}:")
                        print(format_result(engine, row, detailed=True))
            else:
                if args.scan:
                    print(f"--- RPM scan for fuel: {fuel_case.name} ({fuel_case.id}) ---")
                    scan_results = scan_engine(
                        engine,
                        fuel_case,
                        min_rpm=args.min_rpm,
                        max_rpm=args.max_rpm,
                        step=args.rpm_step,
                    )
                    for row in scan_results:
                        print(
                            f"RPM {row.rpm}: {row.brake_power_kw:.1f} kW ({kw_to_hp(row.brake_power_kw):.1f} hp), "
                            f"torque {row.torque_nm:.1f} Nm ({nm_to_ftlb(row.torque_nm):.1f} ft-lb), "
                            f"eff {row.thermal_efficiency:.3f}, "
                            f"BSFC {row.bsfc_g_kwh:.1f} g/kWh"
                        )
                    peak_result = max(scan_results, key=lambda r: r.brake_power_kw)
                    peak_results.append((fuel_case, peak_result))
                    continue
                result = simulate_engine_cycle(
                    engine,
                    rpm=selected_rpm,
                    throttle=args.throttle,
                    fuel=fuel_case,
                    afr=args.afr,
                    spark_advance_deg=args.spark_advance,
                    detailed=args.detailed,
                )
                compare_results.append(result)
                print(f"=== Fuel: {fuel_case.name} ({fuel_case.id}) ===")
                print(format_result(engine, result, detailed=args.detailed))
        if args.scan and peak_results:
            print("\n" + summarize_peak_power_results(peak_results))
        if compare_results and not args.monte_carlo:
            print("\n" + summarize_comparison(compare_results))
            if args.results_output:
                records = [result_to_record(engine, result, mode="compare_fuels") for result in compare_results]
                save_results(args.results_output, {
                    "mode": "compare_fuels",
                    "engine": engine.id,
                    "fuel_profiles": [r["fuel_profile_id"] for r in records],
                }, records)
        return

    if args.scan:
        print(f"Scanning engine: {engine.name} with fuel: {fuel.name}\n")
        scan_results = scan_engine(
            engine,
            fuel,
            min_rpm=args.min_rpm,
            max_rpm=args.max_rpm,
            step=args.rpm_step,
        )
        best = max(scan_results, key=lambda r: r.brake_power_kw)
        for row in scan_results:
            print(
                f"RPM {row.rpm}: {row.brake_power_kw:.1f} kW ({kw_to_hp(row.brake_power_kw):.1f} hp), "
                f"torque {row.torque_nm:.1f} Nm ({nm_to_ftlb(row.torque_nm):.1f} ft-lb), "
                f"eff {row.thermal_efficiency:.3f}, "
                f"BSFC {row.bsfc_g_kwh:.1f} g/kWh"
            )
        print(
            f"\nBest brake power: {best.brake_power_kw:.2f} kW ({kw_to_hp(best.brake_power_kw):.1f} hp) "
            f"at {best.rpm} RPM ({best.torque_nm:.1f} Nm / {nm_to_ftlb(best.torque_nm):.1f} ft-lb, "
            f"BSFC {best.bsfc_g_kwh:.1f} g/kWh)"
        )
        return

    if args.monte_carlo:
        print(f"Running Monte Carlo sweep for engine: {engine.name} with fuel: {fuel.name}\n")
        mc_results = monte_carlo_sweep(
            engine,
            fuel,
            args.trials,
            args.min_afr,
            args.max_afr,
            args.min_spark,
            args.max_spark,
            args.min_throttle,
            args.max_throttle,
        )
        print(summarize_monte_carlo(mc_results))
        if args.detailed:
            for i, row in enumerate(mc_results[:5], start=1):
                print(f"\nTrial {i}:")
                print(format_result(engine, row, detailed=True))
        return

    result = simulate_engine_cycle(
        engine,
        rpm=selected_rpm,
        throttle=args.throttle,
        fuel=fuel,
        afr=args.afr,
        spark_advance_deg=args.spark_advance,
        detailed=args.detailed,
    )
    print(format_result(engine, result, detailed=args.detailed))


if __name__ == "__main__":
    main()
