"""JPL Horizons API helpers — planetary physical + orbital element parsing."""

from __future__ import annotations

import math
import re
import urllib.parse
import urllib.request
from typing import Any

HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

# Major planets (JPL NAIF IDs)
SMALL_BODY_COMMANDS = {
    "Moon": ("301", "@399"),
    "Ceres": ("1;", "@10"),
    "Vesta": ("4;", "@10"),
    "Eros": ("433", "@10"),
    "Halley": ("90000022", "@10"),
    "Pluto": ("999", "@10"),
    "Eris": ("136199", "@10"),
    "Makemake": ("136472", "@10"),
    "Haumea": ("136108", "@10"),
    "Pallas": ("2;", "@10"),
    "Juno": ("3;", "@10"),
    "Hygiea": ("10;", "@10"),
}

# Heliocentric semi-major axes (AU) — JPL SBDB reference for Kepler/perturbation checks.
SMALL_BODY_SEMI_MAJOR_AU = {
    "Ceres": 2.767,
    "Vesta": 2.362,
    "Eros": 1.458,
    "Halley": 17.834,
    "Pluto": 39.482,
    "Eris": 67.669,
    "Makemake": 45.791,
    "Haumea": 43.131,
    "Pallas": 2.773,
    "Juno": 2.668,
    "Hygiea": 3.139,
}

# Moon-Earth orbit (geocentric reference)
MOON_ORBIT_DAYS = 27.321582
MOON_SEMI_MAJOR_KM = 384400.0

PLANET_COMMANDS = {
    "Mercury": "199",
    "Venus": "299",
    "Earth": "399",
    "Mars": "499",
    "Jupiter": "599",
    "Saturn": "699",
    "Uranus": "799",
    "Neptune": "899",
}

# Dwarf planets + major moons (command, Horizons center) for extended planetary structure ingest.
EXTENDED_BODY_COMMANDS = {
    "Pluto": ("999", "@10"),
    "Eris": ("136199", "@10"),
    "Makemake": ("136472", "@10"),
    "Haumea": ("136108", "@10"),
    "Io": ("501", "@599"),
    "Europa": ("502", "@599"),
    "Ganymede": ("503", "@599"),
    "Callisto": ("504", "@599"),
    "Titan": ("606", "@699"),
    "Triton": ("801", "@899"),
    "Phobos": ("401", "@499"),
    "Deimos": ("402", "@499"),
}

ATMOSPHERE_BODY_COMMANDS = {
    "Mercury": ("199", "@10"),
    "Venus": ("299", "@10"),
    "Mars": ("499", "@10"),
    "Jupiter": ("599", "@10"),
    "Saturn": ("699", "@10"),
    "Uranus": ("799", "@10"),
    "Neptune": ("899", "@10"),
    "Pluto": ("999", "@10"),
}

# NASA Planetary Fact Sheets — authoritative pressure/temperature anchors.
NASA_ATMOSPHERE_REFERENCE = {
    "Mercury": {"pressure_bar": 1.0e-15, "temperature_k": 440.0},
    "Venus": {"pressure_bar": 92.0, "temperature_k": 737.0},
    "Earth": {"pressure_bar": 1.013, "temperature_k": 288.0},
    "Mars": {"pressure_bar": 0.00636, "temperature_k": 210.0},
    "Jupiter": {"pressure_bar": 1.0, "temperature_k": 165.0},
    "Saturn": {"pressure_bar": 1.0, "temperature_k": 134.0},
    "Uranus": {"pressure_bar": 1.0, "temperature_k": 76.0},
    "Neptune": {"pressure_bar": 1.0, "temperature_k": 72.0},
    "Pluto": {"pressure_bar": 1.1e-5, "temperature_k": 44.0},
    "Titan": {"pressure_bar": 1.476, "temperature_k": 93.7},
    "Europa": {"pressure_bar": 1.0e-12, "temperature_k": 102.0},
    "Io": {"pressure_bar": 1.0e-8, "temperature_k": 130.0},
    "Triton": {"pressure_bar": 1.4e-5, "temperature_k": 38.0},
    "Enceladus": {"pressure_bar": 1.0e-6, "temperature_k": 75.0},
}

# Bodies without Horizons atmosphere blocks — NASA fact-sheet ingest only.
NASA_ATMOSPHERE_ONLY_BODIES = [
    "Earth",
    "Titan",
    "Europa",
    "Io",
    "Triton",
    "Enceladus",
]

# NASA/JPL fact-sheet fallback when Horizons ELEMENTS block lacks mass/radius.
def _mass_kg_from_density_radius(density_g_cm3: float, radius_km: float) -> float:
    """Self-consistent mass from published bulk density and mean radius."""
    r_m = radius_km * 1000.0
    vol_m3 = (4.0 / 3.0) * math.pi * (r_m**3)
    return float(density_g_cm3) * 1000.0 * vol_m3


NASA_EXTENDED_PHYSICAL_REFERENCE = {
    "Venus": {
        "radius_km": 6051.8,
        "density_g_cm3": 5.204,
        "mass_kg": _mass_kg_from_density_radius(5.204, 6051.8),
    },
    "Eris": {
        "radius_km": 1163.0,
        "density_g_cm3": 2.43,
        "mass_kg": _mass_kg_from_density_radius(2.43, 1163.0),
    },
    "Makemake": {
        "radius_km": 715.0,
        "density_g_cm3": 1.7,
        "mass_kg": _mass_kg_from_density_radius(1.7, 715.0),
    },
    "Haumea": {
        "radius_km": 816.0,
        "density_g_cm3": 2.018,
        "mass_kg": _mass_kg_from_density_radius(2.018, 816.0),
    },
    "Phobos": {
        "radius_km": 11.266,
        "density_g_cm3": 1.9,
        "mass_kg": _mass_kg_from_density_radius(1.9, 11.266),
    },
    "Deimos": {
        "radius_km": 6.2,
        "density_g_cm3": 1.76,
        "mass_kg": _mass_kg_from_density_radius(1.76, 6.2),
    },
}

G_SI = 6.67430e-11

# NASA Planetary Fact Sheet semi-major axes (AU) — ephemeris reference for Kepler checks.
NASA_SEMI_MAJOR_AU = {
    "Mercury": 0.387,
    "Venus": 0.723,
    "Earth": 1.0,
    "Mars": 1.524,
    "Jupiter": 5.203,
    "Saturn": 9.537,
    "Uranus": 19.191,
    "Neptune": 30.069,
    "Pluto": 39.482,
    "Eris": 67.669,
    "Makemake": 45.791,
    "Haumea": 43.131,
}


def fetch_horizons(*, command: str, ephem_type: str = "ELEMENTS", center: str = "@10") -> str:
    data = urllib.parse.urlencode(
        {
            "format": "json",
            "COMMAND": f"'{command}'",
            "EPHEM_TYPE": ephem_type,
            "CENTER": center,
            "START_TIME": "2024-01-01",
            "STOP_TIME": "2024-01-02",
            "STEP_SIZE": "1d",
        }
    )
    req = urllib.request.Request(
        HORIZONS_URL,
        data=data.encode(),
        headers={"User-Agent": "FSOT-2.1-Lean/jpl", "Content-Type": "application/x-www-form-urlencoded"},
    )
    doc = __import__("json").loads(urllib.request.urlopen(req, timeout=60).read())
    return str(doc.get("result") or "")


def _horizons_supplementary_exponent(text: str, value_end: int) -> int:
    """Parse Horizons parenthetical supplementary exponent e.g. ``1.08 (10^-4)`` → -4."""
    tail = text[value_end : value_end + 32]
    m = re.search(r"\(\s*10\s*\^\s*([+-]?\d+)\s*\)", tail, re.IGNORECASE)
    return int(m.group(1)) if m else 0


def _triaxial_radius_km(text: str) -> float | None:
    """Equivalent-sphere radius from Horizons ``a x b x c`` triaxial notation."""
    m = re.search(
        r"Radius\s*\(km\)\s*=\s*([0-9.]+)\s*x\s*([0-9.]+)\s*x\s*([0-9.]+)",
        text,
        re.IGNORECASE,
    )
    if not m:
        return None
    a, b, c = (float(m.group(i)) for i in range(1, 4))
    return (a * b * c) ** (1.0 / 3.0)


def _first_float(pattern: str, text: str) -> float | None:
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1).split("+-")[0].split("±")[0].strip()
    try:
        return float(raw)
    except ValueError:
        sub = re.search(r"[-+]?\d*\.\d+|\d+", raw)
        return float(sub.group(0)) if sub else None


def parse_atmosphere_block(text: str) -> dict[str, Any]:
    pressure = _first_float(r"Atmos\.\s*pressure\s*\(bar\)\s*=\s*([0-9.]+)", text)
    if pressure is None:
        pressure = _first_float(r"Atmos\.\s*pressure\s*\(bar\)\s*=\s*([0-9.Ee+-]+)", text)
    temp = _first_float(r"Mean\s+[Tt]emperature\s*\(K\)\s*=\s*([0-9.]+)", text)
    if temp is None:
        temp = _first_float(r"Atmos\.\s*temp\.\s*\(1\s*bar\)\s*=\s*([0-9.]+)", text)
    return {"pressure_bar": pressure, "temperature_k": temp}


def parse_physical_block(text: str) -> dict[str, Any]:
    mass_unit = 23
    radius_km = _first_float(r"Vol\.\s*mean\s*radius\s*\(km\)\s*=\s*([0-9.]+)", text)
    if radius_km is None:
        radius_km = _first_float(r"Vol\.\s*Mean\s*Radius\s*\(km\)\s*=\s*([0-9.]+)", text)
    if radius_km is None:
        radius_km = _first_float(r"Mean\s+[Rr]adius\s*\(km\)\s*=\s*([0-9.]+)", text)
    if radius_km is None:
        radius_km = _first_float(r"Equat\.\s*radius,\s*km\s*=\s*([0-9.]+)", text)
    density = _first_float(r"Density\s*\(g/cm\^3\)\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Density\s*\(g\s*cm\^-3\)\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Density,\s*g/cm\^3\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Density\s*\([^)]*\)\s*=\s*([0-9.]+)\s*g/cm\^3", text)
    if density is None:
        density = _first_float(r"Density\s*\(g/cm\^3\)\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Mean\s+dens\s*\(g\s*cm\^-3\)\s*=\s*([0-9.]+)", text)
    mass = _first_float(r"Mass\s*x10\^22\s*\(kg\)\s*=\s*([0-9.]+)", text)
    if mass is not None:
        mass_unit = 22
    if mass is None:
        mass = _first_float(r"Mass\s*x10\^23\s*\(kg\)\s*=\s*([0-9.]+)", text)
        if mass is not None:
            mass_unit = 23
    if mass is None:
        mass = _first_float(r"Mass\s*x10\^24\s*\(kg\)\s*=\s*([0-9.]+)", text)
        if mass is not None:
            mass_unit = 24
    if mass is None:
        mass = _first_float(r"Mass\s*\(10\^19\s*kg\)\s*=\s*([0-9.]+)", text)
        if mass is not None:
            mass_unit = 19
    if mass is None:
        mass = _first_float(r"Mass\s*x\s*10\^26\s*\(kg\)\s*=\s*([0-9.]+)", text)
        if mass is not None:
            mass_unit = 26
    mass_supp = 0
    if mass is None:
        m20 = re.search(
            r"Mass\s*\(10\^20\s*kg\s*\)\s*=\s*([0-9.]+)",
            text,
            re.IGNORECASE,
        )
        if m20:
            mass = float(m20.group(1))
            mass_unit = 20
            mass_supp = _horizons_supplementary_exponent(text, m20.end())
    if radius_km is None:
        radius_km = _triaxial_radius_km(text)
    if radius_km is None:
        radius_km = _first_float(r"Radius\s*\(km\)\s*=\s*([0-9.]+)", text)
    gm_km3 = _first_float(r"GM\s*\(km\^3/s\^2\)\s*=\s*([0-9.Ee+-]+)", text)
    if gm_km3 is None:
        gm_km3 = _first_float(r"GM\s*\(km\^3/s\^2\)\s*=\s*([0-9.]+)", text)
    mass_kg = None
    if mass is not None:
        mass_kg = float(mass) * (10.0 ** int(mass_supp)) * (10.0 ** int(mass_unit))
    elif gm_km3 is not None:
        mass_kg = float(gm_km3) * 1.0e9 / G_SI
    period_days = _first_float(r"Orbit\s+period\s*=\s*([0-9.]+)\s*d", text)
    if period_days is None:
        period_days = _first_float(r"Sidereal\s+orbit\s+period\s*=\s*([0-9.]+)\s*d", text)
    if period_days is None:
        period_days = _first_float(r"Sidereal\s+orb\.\s+per\.,\s*d\s*=\s*([0-9.]+)", text)
    if period_days is None:
        period_days = _first_float(r"Sidereal\s+orb\.\s+per\.\s*=\s*([0-9.]+)\s*d", text)
    if period_days is None:
        period_days = _first_float(r"Mean\s+sidereal\s+orb\s+per\s*=\s*([0-9.]+)\s*d", text)
    if period_days is None:
        years = _first_float(r"Sidereal\s+orb\s+period\s*=\s*([0-9.]+)\s*y", text)
        if years is None:
            years = _first_float(r"Sidereal\s+orbit\s+period\s*=\s*([0-9.]+)\s*y", text)
        if years is None:
            years = _first_float(r"Mean\s+sidereal\s+orb\s+per\s*=\s*([0-9.]+)\s*y", text)
        if years is not None:
            period_days = years * 365.256
    return {
        "radius_km": radius_km,
        "density_g_cm3": density,
        "mass_value": mass,
        "mass_exponent": mass_unit,
        "mass_kg": mass_kg,
        "period_days": period_days,
    }


def resolve_body_physical(name: str, text: str) -> dict[str, Any]:
    """Merge Horizons parse with NASA fact-sheet fallback for incomplete bodies."""
    phys = parse_physical_block(text)
    ref = NASA_EXTENDED_PHYSICAL_REFERENCE.get(name)
    if ref:
        if phys.get("radius_km") is None:
            phys["radius_km"] = ref.get("radius_km")
        if phys.get("density_g_cm3") is None:
            phys["density_g_cm3"] = ref.get("density_g_cm3")
    radius = phys.get("radius_km") or (ref or {}).get("radius_km")
    density = phys.get("density_g_cm3") or (ref or {}).get("density_g_cm3")
    if radius and density:
        # Published bulk density + mean radius is the self-consistent JPL anchor.
        phys["mass_kg"] = _mass_kg_from_density_radius(float(density), float(radius))
    elif phys.get("mass_kg") is None and ref and ref.get("mass_kg") is not None:
        phys["mass_kg"] = ref["mass_kg"]
    return phys


def resolve_semi_major_axis_au(
    name: str,
    text: str,
    *,
    table: dict[str, float] | None = None,
    prefer_soe: bool = False,
) -> float | None:
    """Semi-major axis AU — NASA mean elements unless dwarf-body SOE is requested."""
    lookup = table if table is not None else NASA_SEMI_MAJOR_AU
    if prefer_soe:
        soe = parse_soe_elements(text)
        a_au = soe.get("semi_major_axis_au")
        if a_au is not None:
            return float(a_au)
    ref = lookup.get(name)
    if ref is not None:
        return float(ref)
    soe = parse_soe_elements(text)
    a_au = soe.get("semi_major_axis_au")
    return float(a_au) if a_au is not None else None


def parse_soe_elements(text: str) -> dict[str, float | None]:
    """Parse osculating EC/QR from JPL Horizons $$SOE block."""
    if "$$SOE" not in text:
        return {"eccentricity": None, "perihelion_km": None, "semi_major_axis_au": None}
    block = text.split("$$SOE")[1].split("$$EOE")[0]
    ecc = _first_float(r"EC=\s*([0-9.Ee+-]+)", block)
    qr_km = _first_float(r"QR=\s*([0-9.Ee+-]+)", block)
    sma_au = None
    if ecc is not None and qr_km is not None and ecc < 1.0:
        sma_km = qr_km / (1.0 - ecc)
        sma_au = sma_km / 149597870.7
    return {
        "eccentricity": ecc,
        "perihelion_km": qr_km,
        "semi_major_axis_au": sma_au,
    }


def parse_orbital_elements(text: str) -> dict[str, float | None]:
    semi_major_km = _first_float(r"Semi-major\s+axis[^=]*=\s*([0-9.Ee+-]+)\s*km", text)
    period_sec = _first_float(r"Sidereal\s+orbit\s+period\s*\(sec\)\s*=\s*([0-9.Ee+-]+)", text)
    if semi_major_km is None:
        soe = text.split("$$SOE")
        block = soe[-1].split("$$EOE")[0] if len(soe) > 1 else text
        nums = re.findall(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+", block)
        floats = [float(x) for x in nums]
        if len(floats) >= 4:
            semi_major_km = floats[2]
            period_sec = period_sec or floats[3]
    return {"semi_major_axis_km": semi_major_km, "period_sec": period_sec}


def density_from_mass_radius(mass_kg: float, radius_km: float) -> float:
    r_m = radius_km * 1000.0
    vol_m3 = (4.0 / 3.0) * 3.141592653589793 * (r_m**3)
    return (mass_kg / vol_m3) / 1000.0  # g/cm^3


def mass_to_kg(mass_value: float, exponent: int) -> float:
    return mass_value * (10.0**exponent)