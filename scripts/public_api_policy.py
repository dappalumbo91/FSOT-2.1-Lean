"""FSOT public API policy — all live channels must be credential-free."""

from __future__ import annotations

CREDENTIAL_FREE_ONLY = True

# Channels that require API keys are excluded from FSOT live verification panels.
REQUIRES_API_KEY = frozenset(
    {
        "materials_project",
        "nasa_neows",
        "nasa_donki",
        "epa_airnow",
        "fred_stlouisfed",
    }
)