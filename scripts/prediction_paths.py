"""Canonical paths for the monorepo ``predictions/`` folder.

All prediction manifests, freezes, atlases, and human reports live under:

    predictions/
      *.json / *.yaml     — machine artifacts
      reports/            — human-readable MD tables

Large raw catalogs stay on external drive G:/FSOT-PublicData (see external_data_pointers.json).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT / "predictions"
REPORTS = PRED / "reports"

# Core manifests
PREREG_MANIFEST = PRED / "preregistered_predictions_manifest.yaml"
MONITOR_REGISTRY = PRED / "prediction_monitor_registry.yaml"
SECTOR_H0_SEED = PRED / "sector_h0_seed.json"
EXTERNAL_POINTERS = PRED / "external_data_pointers.json"
TOE_PREREG_FREEZE = PRED / "toe_prereg_freeze.json"
CONTESTED_FUTURE_LEDGER = PRED / "contested_future_observation_ledger.json"

# Generated prediction products
DOMAIN_ATLAS = PRED / "domain_prediction_atlas.json"
H0_MULTI_TOOL = PRED / "h0_multi_tool_predictions.json"
H0_SIGHTLINE = PRED / "h0_sightline_predictions.json"
H0_TRGB = PRED / "cchp_trgb_sightline_predictions.json"
NEAREST_DROPS = PRED / "nearest_data_drop_ranking.json"
MONITOR_REPORT = PRED / "prediction_monitor_report.json"

# Reports (markdown)
REPORT_MONITOR = REPORTS / "PREDICTION_MONITOR.md"
REPORT_ATLAS = REPORTS / "DOMAIN_PREDICTION_ATLAS.md"
REPORT_H0_MULTI = REPORTS / "H0_MULTI_TOOL_PREDICTIONS.md"
REPORT_H0_SIGHT = REPORTS / "H0_SIGHTLINE_PREDICTIONS.md"
REPORT_H0_TRGB = REPORTS / "CCHP_TRGB_SIGHTLINE_PREDICTIONS.md"
REPORT_NEAREST = REPORTS / "NEAREST_DATA_DROPS.md"
REPORT_CONTESTED_FUTURE = REPORTS / "CONTESTED_FUTURE_OBSERVATION_LEDGER.md"
REPORT_CONTESTED_WATCH = REPORTS / "CONTESTED_SECTOR_WATCH.md"


def ensure_dirs() -> None:
    PRED.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
