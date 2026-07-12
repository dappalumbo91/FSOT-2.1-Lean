"""Centralized deep / mega-deep cohort limits for FSOT live API ingests."""

from __future__ import annotations

import os


def _flag(key: str) -> bool:
    return os.environ.get(key, "").strip().lower() in {"1", "true", "yes", "on"}


def mega_deep() -> bool:
    return _flag("FSOT_API_MEGA_DEEP")


def tier38_deep() -> bool:
    return _flag("FSOT_TIER38_DEEP") or mega_deep()


def tier60_deep() -> bool:
    return _flag("FSOT_TIER60_DEEP") or mega_deep()


def tier62_deep() -> bool:
    return _flag("FSOT_TIER62_DEEP") or mega_deep()


def tier68_deep() -> bool:
    return _flag("FSOT_TIER68_DEEP") or mega_deep()


def tier79_deep() -> bool:
    return _flag("FSOT_TIER79_DEEP") or mega_deep()


def gbif_occurrence_limit() -> int:
    if mega_deep():
        return 1000
    if tier38_deep():
        return 500
    return 120


def nasa_exoplanet_limit() -> int:
    if mega_deep():
        return 500
    if tier38_deep():
        return 250
    return 80


def openalex_per_page() -> int:
    if mega_deep():
        return 200
    if tier38_deep():
        return 150
    return 80


def simbad_top_limit() -> int:
    if mega_deep():
        return 250
    if tier60_deep():
        return 120
    return 35


def gaia_top_limit() -> int:
    if mega_deep():
        return 300
    if tier62_deep():
        return 150
    return 40


def wds_vizier_top_limit() -> int:
    if mega_deep():
        return 250
    if tier68_deep():
        return 120
    return 40


def mast_pagesize() -> int:
    if mega_deep():
        return 1000
    if tier79_deep():
        return 600
    return 200


def materials_project_api_limit() -> int:
    if mega_deep():
        return 100
    if tier68_deep():
        return 50
    return 20


def openneuro_graphql_pages() -> int:
    if mega_deep():
        return 40
    if tier68_deep():
        return 20
    return 6


def openneuro_page_size() -> int:
    if mega_deep():
        return 50
    if tier68_deep():
        return 25
    return 10


def openneuro_dataset_cap() -> int:
    if mega_deep():
        return 500
    if tier68_deep():
        return 200
    return 60


def cern_query_sizes() -> tuple[int, int, int]:
    if mega_deep():
        return (100, 80, 60)
    if tier38_deep():
        return (60, 50, 40)
    return (40, 30, 20)