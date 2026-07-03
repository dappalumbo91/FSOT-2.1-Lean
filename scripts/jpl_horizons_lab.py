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
}

# Heliocentric semi-major axes (AU) — JPL SBDB reference for Kepler/perturbation checks.
SMALL_BODY_SEMI_MAJOR_AU = {
    "Ceres": 2.767,
    "Vesta": 2.362,
    "Eros": 1.458,
    "Halley": 17.834,
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


def parse_physical_block(text: str) -> dict[str, Any]:
    radius_km = _first_float(r"Vol\.\s*Mean\s*Radius\s*\(km\)\s*=\s*([0-9.]+)", text)
    if radius_km is None:
        radius_km = _first_float(r"Equat\.\s*radius,\s*km\s*=\s*([0-9.]+)", text)
    density = _first_float(r"Density\s*\(g/cm\^3\)\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Density\s*\(g\s*cm\^-3\)\s*=\s*([0-9.]+)", text)
    if density is None:
        density = _first_float(r"Density,\s*g/cm\^3\s*=\s*([0-9.]+)", text)
    mass = _first_float(r"Mass\s*x10\^23\s*\(kg\)\s*=\s*([0-9.]+)", text)
    if mass is None:
        mass = _first_float(r"Mass\s*x10\^24\s*\(kg\)\s*=\s*([0-9.]+)", text)
        mass_unit = 24
    else:
        mass_unit = 23
    if mass is None:
        mass = _first_float(r"Mass\s*x\s*10\^26\s*\(kg\)\s*=\s*([0-9.]+)", text)
        mass_unit = 26
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
        "period_days": period_days,
    }


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