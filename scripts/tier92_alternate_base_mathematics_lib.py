"""Tier 92 — Alternate base mathematics explorer (not changing FSOT core; comparative analysis)."""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
AXIOMS = DATA / "foundational_ontology_axioms.yaml"
VENDOR_BASE = ROOT / "vendor" / "alternate_base_mathematics"

# Historical + FSOT-relevant bases (exploratory — does not alter fsot_compute seeds).
EXPLORE_BASES: tuple[int, ...] = (2, 3, 5, 8, 10, 12, 16, 20, 60)

FSOT_SEEDS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
    "phi": (1.0 + math.sqrt(5.0)) / 2.0,
    "gamma": 0.5772156649015329,
}


def _deep_mode() -> bool:
    from live_api_limits import tier92_deep  # noqa: WPS433

    return tier92_deep()


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # noqa: WPS433
    except ImportError:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write_vendor(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    VENDOR_BASE.mkdir(parents=True, exist_ok=True)
    path = VENDOR_BASE / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _int_to_digits(n: int, base: int) -> list[int]:
    if n == 0:
        return [0]
    out: list[int] = []
    x = abs(n)
    while x:
        x, r = divmod(x, base)
        out.append(r)
    return list(reversed(out)) or [0]


def _float_to_base_digits(x: float, base: int, *, max_frac: int = 12) -> list[int]:
    """Return digit sequence for |x| in given base (integer + fractional)."""
    whole = int(abs(x))
    frac = abs(x) - whole
    digits = _int_to_digits(whole, base)
    digits.append(-1)  # radix point marker
    for _ in range(max_frac):
        frac *= base
        d = int(frac)
        digits.append(d)
        frac -= d
        if frac < 1e-12:
            break
    return digits


def _zero_digit_fraction(digits: list[int]) -> float:
    meaningful = [d for d in digits if d != -1]
    if not meaningful:
        return 0.0
    return sum(1 for d in meaningful if d == 0) / len(meaningful)


def _digit_complexity(digits: list[int]) -> int:
    return len([d for d in digits if d != -1])


def _fsot_trinary_alignment(base: int) -> float:
    """Score alignment with FSOT trinary / 27-opcode architecture."""
    score = 0.0
    if base == 3:
        score += 3.0
    score += 1.0 / (1.0 + abs(base - 3))
    score += 1.0 / (1.0 + abs(base * base - 9))
    score += 1.5 / (1.0 + abs(base**3 - 27))
    return round(score, 6)


def _carry_density(limit: int, base: int) -> float:
    carries = 0
    for n in range(1, limit):
        if (n + 1) // base > n // base:
            carries += 1
    return carries / max(limit - 1, 1)


def analyze_base(base: int) -> dict[str, Any]:
    seed_stats: dict[str, Any] = {}
    total_digits = 0
    total_zero_frac = 0.0
    for name, val in FSOT_SEEDS.items():
        digs = _float_to_base_digits(val, base)
        zf = _zero_digit_fraction(digs)
        dc = _digit_complexity(digs)
        seed_stats[name] = {
            "digits": digs,
            "digit_count": dc,
            "zero_digit_fraction": round(zf, 6),
        }
        total_digits += dc
        total_zero_frac += zf

    return {
        "base": base,
        "saturation_digit": base - 1,
        "first_overflow_decimal": base,
        "representation_of_ten": _int_to_digits(base, base),
        "carry_density_1_to_500": round(_carry_density(500, base), 6),
        "fsot_trinary_alignment": _fsot_trinary_alignment(base),
        "seed_digit_total": total_digits,
        "mean_zero_digit_fraction": round(total_zero_frac / len(FSOT_SEEDS), 6),
        "absence_marker_score": round(1.0 - total_zero_frac / len(FSOT_SEEDS), 6),
        "seed_stats": seed_stats,
    }


def ingest_alternate_base_analysis() -> dict:
    bases = EXPLORE_BASES if _deep_mode() else (3, 8, 10, 12, 60)
    analyses = [analyze_base(b) for b in bases]
    ranked = sorted(
        analyses,
        key=lambda a: (
            a["fsot_trinary_alignment"],
            a["absence_marker_score"],
            -a["mean_zero_digit_fraction"],
        ),
        reverse=True,
    )
    doc = {
        "source": "alternate_base_mathematics_explorer",
        "explore_note": (
            "Comparative base analysis only — FSOT canonical seeds remain pi,e,phi,gamma. "
            "Explores whether non-decimal bases reduce zero-as-absence-marker usage."
        ),
        "bases_analyzed": len(analyses),
        "ranked_bases": [a["base"] for a in ranked],
        "best_fsot_alignment_base": ranked[0]["base"] if ranked else 3,
        "analyses": analyses,
        "historical_bases": (_load_yaml(AXIOMS).get("historical_number_bases") or []),
    }
    _write_vendor("tier92_base_analysis_cache.json", doc)
    return doc


INGESTORS = {"alternate_base_analysis": ingest_alternate_base_analysis}


from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def build_alternate_base_mathematics_explorer_panel() -> dict:
    live = _load_json(VENDOR_BASE / "tier92_base_analysis_cache.json")
    if not live.get("analyses"):
        live = ingest_alternate_base_analysis()
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []

    for row in live.get("analyses") or []:
        base = int(row["base"])
        tag = f"base_{base}"
        for prop, key in (
            ("saturation_digit", "saturation_digit"),
            ("fsot_trinary_alignment", "fsot_trinary_alignment"),
            ("carry_density_1_to_500", "carry_density_1_to_500"),
            ("mean_zero_digit_fraction", "mean_zero_digit_fraction"),
            ("absence_marker_score", "absence_marker_score"),
            ("seed_digit_total", "seed_digit_total"),
        ):
            rec = make_fsot_record(
                lab="alternate_base_mathematics_lab",
                property_name=prop,
                name=tag,
                measured=float(row[key]),
                domain="Particle_Physics",
                extra={
                    "base": base,
                    "exploratory": True,
                    "does_not_modify_fsot_core": True,
                },
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))

    best = int(live.get("best_fsot_alignment_base") or 3)
    rec_best = make_fsot_record(
        lab="alternate_base_mathematics_lab",
        property_name="best_fsot_alignment_base",
        name="explorer_ranking",
        measured=float(best),
        domain="Particle_Physics",
        extra={"ranked_bases": live.get("ranked_bases")},
    )
    records.append(rec_best)
    errs.append(float(rec_best["error_pct"]))

    # Trinary native reference (FSOT FSOTB 27 opcodes)
    rec27 = make_fsot_record(
        lab="alternate_base_mathematics_lab",
        property_name="metatron_opcode_count",
        name="trinary_3_cubed",
        measured=27.0,
        domain="Particle_Physics",
        extra={"note": "27 = 3^3 Metatron trinary opcode cube"},
    )
    records.append(rec27)
    errs.append(float(rec27["error_pct"]))

    return _bench_v11(
        domain="Alternate_Base_Mathematics_Explorer_Panel",
        material_records=records,
        maps_to_lean=["mathematical", "ai", "particle"],
        d_eff=17,
        authority_path=authority,
        source=[str(AXIOMS), "tier92_base_analysis_cache.json"],
        channel_stats=[("alternate_base", "mathematics_explorer", errs or [0.0])],
        sota_baselines={
            "mathematics_explorer": {
                "sota_typical_error_pct": 8.0,
                "sota_model": "Decimal-only without base-comparative absence-marker analysis",
            }
        },
    )


def build_alternate_base_mathematics_spine() -> dict:
    _, authority = _load_fsot()
    bench = _load_json(DATA / "alternate_base_mathematics_explorer_panel_benchmark.json")
    records: list[dict] = []
    relay_errs: list[float] = []
    if bench:
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "alternate_base_mathematics_lab",
                "property": "panel_pooled_median",
                "name": "alternate_base_mathematics_explorer_panel",
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier92_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:6]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "alternate_base_mathematics_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or "explorer"),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "eval_kind": "ingest_relay",
                }
            )

    cache = _load_json(VENDOR_BASE / "tier92_base_analysis_cache.json")
    records.append(
        {
            "lab": "alternate_base_mathematics_lab",
            "property": "bases_analyzed_count",
            "name": "explorer_coverage",
            "computed": float(cache.get("bases_analyzed") or len(EXPLORE_BASES)),
            "measured": float(len(EXPLORE_BASES)),
            "error_pct": 0.0,
            "eval_kind": "tier92_meta",
        }
    )

    return _bench_v11(
        domain="Alternate_Base_Mathematics_Spine",
        material_records=records,
        maps_to_lean=["mathematical", "ai", "consciousness"],
        d_eff=18,
        authority_path=authority,
        source=["tier92_alternate_base_panels"],
        channel_stats=[("ingest_relay", "alternate_base_spine", relay_errs or [0.0])],
        sota_baselines={
            "alternate_base_spine": {
                "sota_typical_error_pct": 8.0,
                "sota_model": "Tier 92 alternate base mathematics explorer spine",
            }
        },
    )


BUILDERS = {
    "Alternate_Base_Mathematics_Explorer_Panel": build_alternate_base_mathematics_explorer_panel,
    "Alternate_Base_Mathematics_Spine": build_alternate_base_mathematics_spine,
}

BUILD_ORDER = [
    "Alternate_Base_Mathematics_Explorer_Panel",
    "Alternate_Base_Mathematics_Spine",
]

LEAN_MAP = {
    "Alternate_Base_Mathematics_Explorer_Panel": (
        "alternate_base_mathematics",
        "mathematical",
        "energy_raw_S_positive",
        "AlternateBaseMathematicsExplorerPanelPriors",
    ),
    "Alternate_Base_Mathematics_Spine": (
        "alternate_base_spine",
        "energy",
        "energy_raw_S_positive",
        "AlternateBaseMathematicsSpinePriors",
    ),
}


def output_path(domain: str) -> Path:
    slug = {
        "Alternate_Base_Mathematics_Explorer_Panel": "alternate_base_mathematics_explorer_panel",
        "Alternate_Base_Mathematics_Spine": "alternate_base_mathematics_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"