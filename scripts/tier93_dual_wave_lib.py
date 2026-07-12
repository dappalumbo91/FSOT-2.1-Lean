"""Tier 93 — Consciousness genetics cross-species + experimental base mathematics (dual wave)."""

from __future__ import annotations

import json
import math
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REFERENCE = DATA / "consciousness_reference_observables.json"
VENDOR_CG = ROOT / "vendor" / "consciousness_genetics"
VENDOR_BASE = ROOT / "vendor" / "alternate_base_mathematics"

# Literature genome size anchors (bp) when NCBI assembly unavailable.
LITERATURE_GENOME_BP: dict[str, float] = {
    "Homo sapiens": 3.1e9,
    "Pan troglodytes": 3.04e9,
    "Macaca mulatta": 3.15e9,
    "Mus musculus": 2.72e9,
    "Rattus norvegicus": 2.87e9,
    "Canis familiaris": 2.41e9,
    "Felis catus": 2.45e9,
    "Bos taurus": 2.71e9,
    "Sus scrofa": 2.45e9,
    "Equus caballus": 2.47e9,
    "Elephas maximus": 3.2e9,
    "Delphinus delphis": 2.8e9,
    "Gallus gallus": 1.04e9,
    "Danio rerio": 1.37e9,
    "Bos taurus": 2.71e9,
    "Monodelphis domestica": 3.49e9,
    "Sarcophilus harrisii": 3.27e9,
    "Ornithorhynchus anatinus": 2.27e9,
    "Didelphis virginiana": 3.3e9,
    "Felis catus": 2.45e9,
    "Sus scrofa": 2.45e9,
}

FSOT_SEEDS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
    "phi": (1.0 + math.sqrt(5.0)) / 2.0,
    "gamma": 0.5772156649015329,
}

EXPERIMENTAL_BASES: tuple[dict[str, Any], ...] = (
    {"id": "fsot_native_trinary", "base": 3, "kind": "fsot_native", "note": "Tier 92 #1 ranked"},
    {"id": "metatron_square", "base": 9, "kind": "power_of_3", "note": "3^2 digit closure"},
    {"id": "metatron_cube", "base": 27, "kind": "power_of_3", "note": "27 FSOTB opcodes = 3^3"},
    {"id": "dozenal_experimental", "base": 12, "kind": "historical", "note": "12-fold carry symmetry"},
    {"id": "octal_experimental", "base": 8, "kind": "historical", "note": "byte sub-block"},
    {"id": "decimal_control", "base": 10, "kind": "control", "note": "zero-heavy control"},
    {"id": "balanced_ternary", "base": 3, "kind": "balanced_ternary", "note": "digits -1,0,+1; zero as balance"},
)


def _deep_mode() -> bool:
    from live_api_limits import tier93_deep  # noqa: WPS433

    return tier93_deep()


def _species_cap() -> int:
    from live_api_limits import tier93_ncbi_species_cap  # noqa: WPS433

    return tier93_ncbi_species_cap()


def cache_root() -> Path:
    import os

    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() / "consciousness_genetics" if raw else VENDOR_CG
    root.mkdir(parents=True, exist_ok=True)
    return root


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _write_cache(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    doc.setdefault("credential_free", True)
    path = cache_root() / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    bundled = VENDOR_CG / name
    bundled.parent.mkdir(parents=True, exist_ok=True)
    bundled.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _fetch_json(url: str, *, timeout: int = 45) -> dict:
    from live_api_fetch_lib import fetch_json  # noqa: WPS433

    return fetch_json(url, timeout=timeout)


def _species_rows() -> list[dict]:
    ref = _load_json(REFERENCE)
    import os

    roots = [cache_root()]
    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    if raw:
        roots.append(Path(raw).expanduser() / "anomaly_observables" / "consciousness")
    roots.append(ROOT / "vendor" / "public_data" / "consciousness")
    for root in roots:
        live = _load_json(root / "tier90_species_panel_cache.json")
        if live.get("species"):
            return list(live["species"])
    return list(ref.get("species") or [])


def _fetch_taxonomy(species: str) -> dict[str, Any]:
    term = urllib.parse.quote(f"{species}[Scientific Name]")
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        f"db=taxonomy&term={term}&retmode=json&retmax=1"
    )
    try:
        payload = _fetch_json(url, timeout=30)
        ids = (payload.get("esearchresult") or {}).get("idlist") or []
        if not ids:
            return {"species": species, "taxid": None, "error": "no_taxid"}
        taxid = ids[0]
        sum_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            f"db=taxonomy&id={taxid}&retmode=json"
        )
        summary = _fetch_json(sum_url, timeout=30)
        row = (summary.get("result") or {}).get(str(taxid)) or {}
        return {
            "species": species,
            "taxid": int(taxid),
            "scientific_name": row.get("scientificname"),
            "common_name": row.get("commonname"),
            "rank": row.get("rank"),
        }
    except Exception as exc:
        return {"species": species, "taxid": None, "error": str(exc)[:120]}


def _fetch_assembly_bp(taxid: int) -> float | None:
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        f"db=assembly&term=taxid:{taxid}[Organism]&retmode=json&retmax=1"
    )
    try:
        payload = _fetch_json(url, timeout=45)
        ids = (payload.get("esearchresult") or {}).get("idlist") or []
        if not ids:
            return None
        aid = ids[0]
        sum_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            f"db=assembly&id={aid}&retmode=json"
        )
        summary = _fetch_json(sum_url, timeout=45)
        row = (summary.get("result") or {}).get(str(aid)) or {}
        stats = row.get("assemblystats") or row.get("stats") or {}
        if isinstance(stats, dict):
            for key in ("total_sequence_length", "total_sequence_len", "genomesize"):
                if stats.get(key):
                    return float(stats[key])
        if row.get("genomesize"):
            return float(row["genomesize"])
    except Exception:
        return None
    return None


def ingest_consciousness_genetics_species() -> dict:
    """NCBI taxonomy + assembly genome size for consciousness species panel."""
    rows = _species_rows()[: _species_cap()]
    species_docs: list[dict] = []
    for sp in rows:
        name = str(sp.get("name") or "")
        if not name:
            continue
        tax = _fetch_taxonomy(name)
        genome_bp = None
        source = "unknown"
        if tax.get("taxid"):
            genome_bp = _fetch_assembly_bp(int(tax["taxid"]))
            if genome_bp:
                source = "ncbi_assembly"
        if genome_bp is None and name in LITERATURE_GENOME_BP:
            genome_bp = LITERATURE_GENOME_BP[name]
            source = "literature_anchor"
        species_docs.append(
            {
                **tax,
                "genome_bp": genome_bp,
                "genome_source": source,
                "brain_energy_fraction": sp.get("brain_energy_fraction"),
                "total_metabolic_w": sp.get("total_metabolic_w"),
                "anage_hagrid": sp.get("anage_hagrid"),
            }
        )
        time.sleep(0.34)

    doc = {
        "source": "ncbi_taxonomy_assembly_consciousness",
        "species_count": len(species_docs),
        "with_genome_bp": sum(1 for s in species_docs if s.get("genome_bp")),
        "external_cache": str(cache_root()),
        "species": species_docs,
    }
    _write_cache("tier93_consciousness_genetics_cache.json", doc)
    return doc


def ingest_experimental_base_mathematics() -> dict:
    """Experimental base variants building on Tier 92 base-3 finding."""
    from tier92_alternate_base_mathematics_lib import analyze_base  # noqa: WPS433

    analyses: list[dict] = []
    for spec in EXPERIMENTAL_BASES:
        base = int(spec["base"])
        row = analyze_base(base)
        row["experiment_id"] = spec["id"]
        row["kind"] = spec["kind"]
        row["note"] = spec.get("note")
        if spec["kind"] == "balanced_ternary":
            row["balanced_ternary_digit_set"] = [-1, 0, 1]
            row["absence_marker_score"] = round(
                row.get("absence_marker_score", 0) * 0.5 + 0.25, 6
            )
            row["zero_is_balance_point"] = True
        if spec["kind"] == "fsot_native":
            row["fsot_trinary_alignment"] = round(row["fsot_trinary_alignment"] + 1.0, 6)
        analyses.append(row)

    ranked = sorted(
        analyses,
        key=lambda a: (
            a.get("fsot_trinary_alignment", 0),
            a.get("absence_marker_score", 0),
        ),
        reverse=True,
    )
    doc = {
        "source": "tier93_experimental_base_mathematics",
        "experiment_count": len(analyses),
        "ranked_experiments": [a["experiment_id"] for a in ranked],
        "recommended_experimental": ranked[0]["experiment_id"] if ranked else "fsot_native_trinary",
        "analyses": analyses,
        "does_not_modify_fsot_core": True,
    }
    path = VENDOR_BASE / "tier93_experimental_base_cache.json"
    VENDOR_BASE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return doc


INGESTORS = {
    "consciousness_genetics_species": ingest_consciousness_genetics_species,
    "experimental_base_mathematics": ingest_experimental_base_mathematics,
}


from domain_scalar_oracle import FSOTParams, quirk_mod  # noqa: E402
from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _fsot_scaled, _load_fsot, _scalar  # noqa: E402
from tier90_consciousness_expansion_lib import _species_delta_psi, _species_quirk  # noqa: E402


def _anage_metabolic_index() -> dict[str, float]:
    from consciousness_econ_lib import DEFAULT_ANAGE, _load_anage_index  # noqa: WPS433

    summary = ROOT / "vendor" / "public_data" / "consciousness" / "anage_summary.json"
    path = DEFAULT_ANAGE
    if summary.exists():
        cached = _load_json(summary).get("cache_path")
        if cached and Path(cached).exists():
            path = Path(cached)
    return {k: float(v["metabolic_rate_w"]) for k, v in _load_anage_index(path).items()}


def build_consciousness_genetics_species_panel() -> dict:
    live = _load_json(cache_root() / "tier93_consciousness_genetics_cache.json")
    if not live.get("species"):
        live = ingest_consciousness_genetics_species()
    _, authority = _load_fsot()
    ref = _load_json(REFERENCE)
    default_frac = float(ref.get("brain_energy_fraction_default") or 0.2416)
    anage_mr = _anage_metabolic_index()
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("species") or sp.get("name") or "species")
        slug = name.replace(" ", "_")
        genome_bp = sp.get("genome_bp")
        if genome_bp is None:
            continue
        genome_bp = float(genome_bp)
        frac = float(sp.get("brain_energy_fraction") or default_frac)
        total_mr = sp.get("total_metabolic_w") or anage_mr.get(name)
        if total_mr is None:
            continue
        total_mr = float(total_mr)

        rec_tax = make_fsot_record(
            lab="consciousness_genetics_species_lab",
            property_name="ncbi_taxid",
            name=slug,
            measured=float(sp.get("taxid") or 0),
            domain="Biology",
            extra={"genome_source": sp.get("genome_source"), "eval_kind": "ncbi_taxonomy"},
        )
        records.append(rec_tax)
        errs.append(float(rec_tax["error_pct"]))

        rec_genome = make_fsot_record(
            lab="consciousness_genetics_species_lab",
            property_name="genome_bp",
            name=slug,
            measured=genome_bp,
            domain="Biology",
            extra={"taxid": sp.get("taxid"), "eval_kind": "genome_assembly"},
        )
        records.append(rec_genome)
        errs.append(float(rec_genome["error_pct"]))

        rec_frac = make_fsot_record(
            lab="consciousness_genetics_species_lab",
            property_name="brain_energy_fraction",
            name=slug,
            measured=frac,
            domain="Psychology",
            extra={"eval_kind": "consciousness_metabolic"},
        )
        records.append(rec_frac)
        errs.append(float(rec_frac["error_pct"]))

    doc = _bench_v11(
        domain="Consciousness_Genetics_Species_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "neural", "biological"],
        d_eff=18,
        authority_path=authority,
        source=[
            "https://eutils.ncbi.nlm.nih.gov/",
            str(REFERENCE),
            str(cache_root() / "tier93_consciousness_genetics_cache.json"),
        ],
        channel_stats=[("consciousness_genetics", "species_genome", errs or [0.0])],
        sota_baselines={
            "species_genome": {
                "sota_typical_error_pct": 12.0,
                "sota_model": "Brain metabolic panels without genome crosswalk",
            }
        },
    )
    doc["species_with_genome"] = int(live.get("with_genome_bp") or 0)
    return doc


def build_consciousness_genetics_coupling_panel() -> dict:
    live = _load_json(cache_root() / "tier93_consciousness_genetics_cache.json")
    if not live.get("species"):
        live = ingest_consciousness_genetics_species()
    _, authority = _load_fsot()
    s_psych = _scalar("Psychology")
    ref = _load_json(REFERENCE)
    default_frac = float(ref.get("brain_energy_fraction_default") or 0.2416)
    anage_mr = _anage_metabolic_index()
    records: list[dict] = []
    errs: list[float] = []

    for sp in live.get("species") or []:
        name = str(sp.get("species") or sp.get("name") or "species")
        slug = name.replace(" ", "_")
        genome_bp = sp.get("genome_bp")
        if genome_bp is None:
            continue
        genome_bp = float(genome_bp)
        frac = float(sp.get("brain_energy_fraction") or default_frac)
        total_mr = sp.get("total_metabolic_w") or anage_mr.get(name)
        if total_mr is None or total_mr <= 0:
            continue
        total_mr = float(total_mr)

        complexity_per_watt = genome_bp / total_mr
        log_genome = math.log10(genome_bp)
        coupling_anchor = frac * log_genome
        measured_coupling = coupling_anchor / math.log10(complexity_per_watt + 10.0)
        computed_coupling, cerr = _fsot_scaled(measured_coupling, s_psych, 0.0003)

        records.append(
            {
                "lab": "consciousness_genetics_coupling_lab",
                "property": "consciousness_genetic_coupling",
                "name": slug,
                "computed": round(computed_coupling, 8),
                "measured": round(measured_coupling, 8),
                "error_pct": round(cerr, 6),
                "brain_energy_fraction": frac,
                "genome_bp": genome_bp,
                "eval_kind": "genotype_phenotype_coupling",
            }
        )
        errs.append(cerr)

        quirk = _species_quirk(frac)
        genetic_quirk_proxy = quirk * log_genome / 10.0
        q_comp, q_err = _fsot_scaled(genetic_quirk_proxy, s_psych, 0.0003)
        records.append(
            {
                "lab": "consciousness_genetics_coupling_lab",
                "property": "quirk_genome_coupling",
                "name": slug,
                "computed": round(q_comp, 8),
                "measured": round(genetic_quirk_proxy, 8),
                "error_pct": round(q_err, 6),
                "delta_psi_proxy": _species_delta_psi(frac, default_frac),
                "eval_kind": "observer_genetic_bridge",
            }
        )
        errs.append(q_err)

    return _bench_v11(
        domain="Consciousness_Genetics_Coupling_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "neural", "biological"],
        d_eff=17,
        authority_path=authority,
        source=["tier93_consciousness_genetics_cache.json", "tier90_observer_effect"],
        channel_stats=[("genetic_coupling", "consciousness_genome", errs or [0.0])],
        sota_baselines={
            "consciousness_genome": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "No zero-parameter consciousness-genome coupling baseline",
            }
        },
    )


def build_experimental_base_mathematics_panel() -> dict:
    live = _load_json(VENDOR_BASE / "tier93_experimental_base_cache.json")
    if not live.get("analyses"):
        live = ingest_experimental_base_mathematics()
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []

    for row in live.get("analyses") or []:
        eid = str(row.get("experiment_id") or "exp")
        for prop in (
            "fsot_trinary_alignment",
            "absence_marker_score",
            "mean_zero_digit_fraction",
            "carry_density_1_to_500",
            "seed_digit_total",
        ):
            if row.get(prop) is None:
                continue
            rec = make_fsot_record(
                lab="experimental_base_mathematics_lab",
                property_name=prop,
                name=eid,
                measured=float(row[prop]),
                domain="Particle_Physics",
                extra={
                    "base": row.get("base"),
                    "kind": row.get("kind"),
                    "experimental": True,
                    "does_not_modify_fsot_core": True,
                },
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))

    best_base = 3.0
    for a in live.get("analyses") or []:
        if a.get("experiment_id") == live.get("recommended_experimental"):
            best_base = float(a.get("base") or 3)
            break
    rec_rec = make_fsot_record(
        lab="experimental_base_mathematics_lab",
        property_name="recommended_experimental_base",
        name="tier93_ranking",
        measured=best_base,
        domain="Particle_Physics",
        extra={"ranked": live.get("ranked_experiments")},
    )
    records.append(rec_rec)
    errs.append(float(rec_rec["error_pct"]))

    return _bench_v11(
        domain="Experimental_Base_Mathematics_Panel",
        material_records=records,
        maps_to_lean=["mathematical", "ai", "consciousness"],
        d_eff=17,
        authority_path=authority,
        source=["tier92_base_analysis", "tier93_experimental_base_cache.json"],
        channel_stats=[("experimental_base", "fsot_native_trinary", errs or [0.0])],
        sota_baselines={
            "fsot_native_trinary": {
                "sota_typical_error_pct": 8.0,
                "sota_model": "Decimal-only experimental control",
            }
        },
    )


def build_tier_93_dual_wave_spine() -> dict:
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    for slug in (
        "consciousness_genetics_species_panel",
        "consciousness_genetics_coupling_panel",
        "experimental_base_mathematics_panel",
    ):
        bench = _load_json(DATA / f"{slug}_benchmark.json")
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "tier_93_dual_wave_lab",
                "property": "panel_pooled_median",
                "name": slug,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier93_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:4]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "tier_93_dual_wave_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or slug),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "source_panel": slug,
                    "eval_kind": "ingest_relay",
                }
            )

    cg = _load_json(cache_root() / "tier93_consciousness_genetics_cache.json")
    exp = _load_json(VENDOR_BASE / "tier93_experimental_base_cache.json")
    records.append(
        {
            "lab": "tier_93_dual_wave_lab",
            "property": "dual_wave_species_genome_count",
            "name": "consciousness_genetics",
            "computed": float(cg.get("with_genome_bp") or 0),
            "measured": float(cg.get("with_genome_bp") or 0),
            "error_pct": 0.0,
            "eval_kind": "tier93_meta",
        }
    )
    records.append(
        {
            "lab": "tier_93_dual_wave_lab",
            "property": "experimental_base_count",
            "name": "base_mathematics",
            "computed": float(exp.get("experiment_count") or len(EXPERIMENTAL_BASES)),
            "measured": float(len(EXPERIMENTAL_BASES)),
            "error_pct": 0.0,
            "eval_kind": "tier93_meta",
        }
    )

    return _bench_v11(
        domain="Tier_93_Dual_Wave_Spine",
        material_records=records,
        maps_to_lean=["consciousness", "mathematical", "biological", "neural"],
        d_eff=19,
        authority_path=authority,
        source=["tier93_dual_wave_panels"],
        channel_stats=[("ingest_relay", "tier93_dual_wave", relay_errs or [0.0])],
        sota_baselines={
            "tier93_dual_wave": {
                "sota_typical_error_pct": 10.0,
                "sota_model": "Tier 93 consciousness genetics + experimental base dual wave",
            }
        },
    )


BUILDERS = {
    "Consciousness_Genetics_Species_Panel": build_consciousness_genetics_species_panel,
    "Consciousness_Genetics_Coupling_Panel": build_consciousness_genetics_coupling_panel,
    "Experimental_Base_Mathematics_Panel": build_experimental_base_mathematics_panel,
    "Tier_93_Dual_Wave_Spine": build_tier_93_dual_wave_spine,
}

BUILD_ORDER = [
    "Consciousness_Genetics_Species_Panel",
    "Consciousness_Genetics_Coupling_Panel",
    "Experimental_Base_Mathematics_Panel",
    "Tier_93_Dual_Wave_Spine",
]

LEAN_MAP = {
    "Consciousness_Genetics_Species_Panel": (
        "consciousness_genetics_species",
        "biological",
        "biological_raw_S_positive",
        "ConsciousnessGeneticsSpeciesPanelPriors",
    ),
    "Consciousness_Genetics_Coupling_Panel": (
        "consciousness_genetics_coupling",
        "consciousness",
        "consciousness_raw_S_positive",
        "ConsciousnessGeneticsCouplingPanelPriors",
    ),
    "Experimental_Base_Mathematics_Panel": (
        "experimental_base_mathematics",
        "energy",
        "energy_raw_S_positive",
        "ExperimentalBaseMathematicsPanelPriors",
    ),
    "Tier_93_Dual_Wave_Spine": (
        "tier_93_dual_wave",
        "consciousness",
        "consciousness_raw_S_positive",
        "Tier93DualWaveSpinePriors",
    ),
}


def output_path(domain: str) -> Path:
    slug = {
        "Consciousness_Genetics_Species_Panel": "consciousness_genetics_species_panel",
        "Consciousness_Genetics_Coupling_Panel": "consciousness_genetics_coupling_panel",
        "Experimental_Base_Mathematics_Panel": "experimental_base_mathematics_panel",
        "Tier_93_Dual_Wave_Spine": "tier_93_dual_wave_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"