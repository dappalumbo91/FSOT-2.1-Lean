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


def tier80_deep() -> bool:
    return _flag("FSOT_TIER80_DEEP") or mega_deep()


def tier81_deep() -> bool:
    return _flag("FSOT_TIER81_DEEP") or mega_deep()


def tier82_deep() -> bool:
    return _flag("FSOT_TIER82_DEEP") or mega_deep()


def tier84_deep() -> bool:
    return _flag("FSOT_TIER84_DEEP") or mega_deep()


def tier85_deep() -> bool:
    return _flag("FSOT_TIER85_DEEP") or mega_deep()


def tier86_deep() -> bool:
    return _flag("FSOT_TIER86_DEEP") or mega_deep()


def tier87_deep() -> bool:
    return _flag("FSOT_TIER87_DEEP") or mega_deep()


def tier88_deep() -> bool:
    return _flag("FSOT_TIER88_DEEP") or mega_deep()


def tier89_deep() -> bool:
    return _flag("FSOT_TIER89_DEEP") or mega_deep()


def tier90_deep() -> bool:
    return _flag("FSOT_TIER90_DEEP") or mega_deep()


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


def nasa_neo_day_span() -> int:
    # NASA NeoWs feed hard-limits queries to 7 calendar days.
    return 7


def nasa_neo_limit() -> int:
    if mega_deep():
        return 200
    if tier80_deep():
        return 120
    return 40


def nasa_donki_day_span() -> int:
    if mega_deep():
        return 365
    if tier80_deep():
        return 180
    return 90


def nasa_donki_limit() -> int:
    if mega_deep():
        return 200
    if tier80_deep():
        return 100
    return 40


def clinicaltrials_limit() -> int:
    if mega_deep():
        return 200
    if tier80_deep():
        return 100
    return 30


def osti_record_limit() -> int:
    if mega_deep():
        return 100
    if tier80_deep():
        return 50
    return 20


def uap_document_limit() -> int:
    if mega_deep():
        return 158
    if tier80_deep():
        return 100
    return 40


def uap_figure_limit() -> int:
    if mega_deep():
        return 500
    if tier80_deep():
        return 250
    return 80


def noaa_goes_xray_limit() -> int:
    if mega_deep():
        return 716
    if tier80_deep():
        return 400
    return 120


def ncbi_gene_limit() -> int:
    if mega_deep():
        return 30
    if tier81_deep():
        return 24
    return 10


def crossref_limit() -> int:
    if mega_deep():
        return 200
    if tier81_deep():
        return 100
    return 30


def inaturalist_limit() -> int:
    if mega_deep():
        return 200
    if tier81_deep():
        return 100
    return 30


def ndbc_buoy_count() -> int:
    if mega_deep():
        return 8
    if tier81_deep():
        return 6
    return 3


def ndbc_rows_per_buoy() -> int:
    if mega_deep():
        return 40
    if tier81_deep():
        return 25
    return 10


def open_meteo_site_count() -> int:
    if mega_deep():
        return 8
    if tier81_deep():
        return 6
    return 3


def volcanology_limit() -> int:
    if mega_deep():
        return 20
    if tier82_deep():
        return 15
    return 8


def limnology_site_count() -> int:
    if mega_deep():
        return 6
    if tier82_deep():
        return 5
    return 3


def radio_source_limit() -> int:
    if mega_deep():
        return 25
    if tier82_deep():
        return 15
    return 8


def ethology_gbif_limit() -> int:
    if mega_deep():
        return 30
    if tier82_deep():
        return 20
    return 10


def toxicology_cid_limit() -> int:
    if mega_deep():
        return 10
    if tier82_deep():
        return 8
    return 5


def soilgrids_point_count() -> int:
    if mega_deep():
        return 6
    if tier82_deep():
        return 5
    return 3


def cartography_feature_limit() -> int:
    if mega_deep():
        return 20
    if tier82_deep():
        return 12
    return 8


def epidemiology_indicator_limit() -> int:
    if mega_deep():
        return 8
    if tier84_deep():
        return 6
    return 4


def virology_genome_limit() -> int:
    if mega_deep():
        return 8
    if tier84_deep():
        return 6
    return 4


def paleontology_occurrence_limit() -> int:
    if mega_deep():
        return 30
    if tier84_deep():
        return 20
    return 10


def arxiv_gw_paper_limit() -> int:
    if mega_deep():
        return 20
    if tier84_deep():
        return 12
    return 8


def tier84_gbif_limit() -> int:
    if mega_deep():
        return 30
    if tier84_deep():
        return 20
    return 10


def marine_obis_limit() -> int:
    if mega_deep():
        return 30
    if tier84_deep():
        return 20
    return 10


def immunology_cid_limit() -> int:
    if mega_deep():
        return 8
    if tier84_deep():
        return 6
    return 4


def tier85_world_bank_limit() -> int:
    if mega_deep():
        return 12
    if tier85_deep():
        return 8
    return 5


def tier85_paleoclimate_limit() -> int:
    if mega_deep():
        return 5
    if tier85_deep():
        return 5
    return 3


def tier85_usgs_limit() -> int:
    if mega_deep():
        return 5
    if tier85_deep():
        return 5
    return 3


def tier85_exoplanet_limit() -> int:
    if mega_deep():
        return 20
    if tier85_deep():
        return 12
    return 8


def tier85_crossref_limit() -> int:
    if mega_deep():
        return 20
    if tier85_deep():
        return 12
    return 8


def tier86_pubchem_limit() -> int:
    if mega_deep():
        return 12
    if tier86_deep():
        return 10
    return 6


def tier87_arxiv_limit() -> int:
    if mega_deep():
        return 20
    if tier87_deep():
        return 12
    return 6