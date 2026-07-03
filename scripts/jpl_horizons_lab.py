"""JPL Horizons API helpers — planetary physical + orbital element parsing."""

from __future__ import annotations

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
    "Mars": ("499", "@10"),
    "Venus": ("299", "@10"),
}

# NASA Planetary Fact Sheet — Titan (Horizons lacks 1-bar atmosphere block for 606).
NASA_ATMOSPHERE_REFERENCE = {
    "Titan": {"pressure_bar": 1.476, "temperature_k": 93.7},
}

# NASA/JPL fact-sheet fallback when Horizons ELEMENTS block lacks mass/radius.
NASA_EXTENDED_PHYSICAL_REFERENCE = {
    "Eris": {"radius_km": 1163.0, "density_g_cm3": 2.43, "mass_kg": 1.6466e22},
    "Makemake": {"radius_km": 715.0, "density_g_cm3": 1.7, "mass_kg": 3.1e21},
    "Haumea": {"radius_km": 816.0, "density_g_cm3": 2.018, "mass_kg": 4.006e21},
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
    if mass is None:
        mass = _first_float(r"Mass\s*\(10\^20\s*kg\s*\)\s*=\s*([0-9.]+)", text)
        if mass is not None:
            mass_unit = 20
    if radius_km is None:
        radius_km = _first_float(r"Radius\s*\(km\)\s*=\s*([0-9.]+)", text)
    gm_km3 = _first_float(r"GM\s*\(km\^3/s\^2\)\s*=\s*([0-9.Ee+-]+)", text)
    if gm_km3 is None:
        gm_km3 = _first_float(r"GM\s*\(km\^3/s\^2\)\s*=\s*([0-9.]+)", text)
    mass_kg = None
    if mass is not None:
        mass_kg = float(mass) * (10.0 ** int(mass_unit))
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
        if phys.get("mass_kg") is None and ref.get("mass_kg") is not None:
            phys["mass_kg"] = ref["mass_kg"]
    return phys


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