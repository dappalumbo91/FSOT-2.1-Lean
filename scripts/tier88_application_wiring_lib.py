"""Tier 88 — Desktop application wiring wave: unwired projects → live panels."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VENDOR = ROOT / "vendor" / "application_wiring"


def _deep_mode() -> bool:
    from live_api_limits import tier88_deep  # noqa: WPS433

    return tier88_deep()


def cache_root() -> Path:
    import os

    raw = os.environ.get("FSOT_EXTERNAL_DATA_ROOT", "").strip()
    root = Path(raw).expanduser() / "tier88_application_wiring" if raw else VENDOR / "tier88_cache"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_cache(name: str, doc: dict) -> Path:
    doc.setdefault("fetched_at", datetime.now(timezone.utc).isoformat())
    doc.setdefault("credential_free", True)
    path = cache_root() / name
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import re

        stripped = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
        stripped = re.sub(r",\s*}", "}", stripped)
        stripped = re.sub(r",\s*]", "]", stripped)
        return json.loads(stripped)


def _numeric_fields(doc: dict, *, prefix: str = "") -> list[dict]:
    rows: list[dict] = []
    for key, val in doc.items():
        if key.startswith("_") or key in ("version", "description", "tuning_notes"):
            continue
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            rows.append({"name": f"{prefix}{key}" if prefix else key, "property": key, "value": float(val)})
        elif isinstance(val, dict):
            for sub_key, sub_val in val.items():
                if isinstance(sub_val, (int, float)) and not isinstance(sub_val, bool):
                    rows.append(
                        {
                            "name": f"{prefix}{key}.{sub_key}",
                            "property": sub_key,
                            "value": float(sub_val),
                        }
                    )
    return rows


# --- ingest ---


def ingest_trinary_hardware() -> dict:
    from fsot_paths import trinary_hardware_motif_path  # noqa: WPS433

    motif = _load_json(trinary_hardware_motif_path())
    profiles: list[dict] = []
    for fname in (
        "motif_influence_profile_stable.json",
        "motif_profile_recovery.json",
        "motif_profile_conservative.json",
    ):
        path = trinary_hardware_motif_path().parent / fname
        if not path.exists():
            continue
        prof = _load_json(path)
        if isinstance(prof, dict):
            profiles.append({"profile": fname.replace(".json", ""), "fields": _numeric_fields(prof)})
    doc = {
        "source": "desktop_trinary_hardware_motif",
        "desktop_folder": "FSOT, Cube Block Trinary Design",
        "wire_status": "tier88_live_panel",
        "primary_motif_fields": _numeric_fields(motif if isinstance(motif, dict) else {}),
        "profiles": profiles,
        "profile_count": len(profiles),
    }
    _write_cache("trinary_hardware_cache.json", doc)
    return doc


def ingest_tokenization() -> dict:
    from fsot_paths import tokenization_root  # noqa: WPS433

    root = tokenization_root()
    smoke_path = root / "smoke" / "smoke_cases.json"
    if not smoke_path.exists():
        smoke_path = VENDOR.parent / "tokenization" / "smoke_cases.json"
    smoke = _load_json(smoke_path)
    cases: list[dict] = []
    if isinstance(smoke, list):
        for row in smoke:
            cases.append(
                {
                    "name": row.get("name"),
                    "text_len": len(str(row.get("text") or "")),
                    "expected_id_count": len(row.get("expected_universal_ids") or []),
                    "expected_gate_count": len((row.get("expected_gates") or {}).keys()),
                }
            )
    vocab_path = root / "tokens" / "registry" / "vocab.json"
    vocab_size = 0
    if vocab_path.exists():
        vocab = _load_json(vocab_path)
        if isinstance(vocab, dict):
            vocab_size = len(vocab)
    doc = {
        "source": "desktop_dictionary_tokenization",
        "desktop_folder": "Dictionary",
        "wire_status": "tier88_live_panel",
        "smoke_cases": cases,
        "case_count": len(cases),
        "vocab_size": vocab_size,
    }
    _write_cache("tokenization_cache.json", doc)
    return doc


def ingest_living_fsot_hardware() -> dict:
    audit_path = VENDOR.parent / "living_fsot_hardware" / "accuracy_audit.json"
    audit = _load_json(audit_path) if audit_path.exists() else {}
    organs: list[dict] = []
    if isinstance(audit, dict):
        for org in (audit.get("orgs") or [])[: (_deep_mode() and 5 or 3)]:
            for organ in org.get("organs") or []:
                organs.append(
                    {
                        "org_id": org.get("id"),
                        "organ": organ.get("name"),
                        "accuracy": float(organ.get("value") or 0),
                        "threshold": float(organ.get("thr") or 0),
                        "weak": bool(organ.get("weak")),
                    }
                )
    doc = {
        "source": "desktop_living_fsot_habitat_rust",
        "desktop_folder": "living fsot",
        "wire_status": "tier88_live_panel",
        "pack_mean": float(audit.get("pack_mean") or 0) if isinstance(audit, dict) else 0,
        "generation": int(audit.get("generation") or 0) if isinstance(audit, dict) else 0,
        "organs": organs,
        "organ_count": len(organs),
    }
    _write_cache("living_fsot_hardware_cache.json", doc)
    return doc


def ingest_certified_agent() -> dict:
    from fsot_paths import certified_agent_summary_path, certified_agent_workspace_path  # noqa: WPS433

    summary = _load_json(certified_agent_summary_path())
    workspace = _load_json(certified_agent_workspace_path())
    paths = (workspace.get("paths") or {}) if isinstance(workspace, dict) else {}
    doc = {
        "source": "desktop_certified_agent_qwen_formal",
        "desktop_folder": "fsot QWEN 3VL_Formal_Env",
        "wire_status": "tier88_live_panel",
        "promotion_threshold_percent": float(summary.get("promotion_threshold_percent") or 2.0),
        "max_tool_iterations": int(summary.get("max_tool_iterations") or 10),
        "max_rag_results": int(summary.get("max_rag_results") or 8),
        "configured_path_count": int(summary.get("configured_path_count") or len(paths)),
        "requires_lean_bridge": bool(summary.get("requires_lean_bridge")),
        "no_probabilistic_math": bool(summary.get("no_probabilistic_math")),
        "workspace_paths": list(paths.keys()),
    }
    _write_cache("certified_agent_cache.json", doc)
    return doc


from tier88_desktop_extended_lib import (  # noqa: E402
    DESKTOP_LAB_KEYS,
    EXTENDED_BUILDERS,
    EXTENDED_BUILD_ORDER,
    EXTENDED_INGESTORS,
    EXTENDED_LEAN_MAP,
    EXTENDED_OUTPUT_SLUGS,
    patch_lab_registry,
)

INGESTORS = {
    "trinary_hardware": ingest_trinary_hardware,
    "tokenization": ingest_tokenization,
    "living_fsot_hardware": ingest_living_fsot_hardware,
    "certified_agent": ingest_certified_agent,
    **EXTENDED_INGESTORS,
}


from fsot_api_predict_lib import make_fsot_record  # noqa: E402
from tier_gap_fill_lib import _bench_v11, _load_fsot  # noqa: E402


def build_trinary_hardware_live_panel() -> dict:
    live = _load_json(cache_root() / "trinary_hardware_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []
    for row in (live.get("primary_motif_fields") or [])[: (_deep_mode() and 30 or 20)]:
        rec = make_fsot_record(
            lab="trinary_hardware_live_lab",
            property_name=str(row.get("property") or "motif"),
            name=str(row.get("name") or "motif"),
            measured=float(row.get("value") or 0),
            domain="Quantum_Computing",
            extra={"ingest_source": live.get("source"), "desktop": live.get("desktop_folder")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    for prof in live.get("profiles") or []:
        for row in (prof.get("fields") or [])[:8]:
            rec = make_fsot_record(
                lab="trinary_hardware_live_lab",
                property_name=str(row.get("property") or "profile_field"),
                name=f"{prof.get('profile')}_{row.get('name')}",
                measured=float(row.get("value") or 0),
                domain="Quantum_Computing",
                extra={"ingest_source": live.get("source"), "profile": prof.get("profile")},
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="Trinary_Hardware_Live_Panel",
        material_records=records,
        maps_to_lean=["ai", "consciousness", "neural"],
        d_eff=14,
        authority_path=authority,
        source=[str(cache_root() / "trinary_hardware_cache.json"), "desktop_trinary_hardware"],
        channel_stats=[("desktop_wiring", "trinary_hardware_motif", errs or [0.0])],
        sota_baselines={
            "trinary_hardware": {"sota_typical_error_pct": 5.0, "sota_model": "ESP32 cube motif profiles"}
        },
    )


def build_tokenization_live_panel() -> dict:
    live = _load_json(cache_root() / "tokenization_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []
    for row in live.get("smoke_cases") or []:
        for prop, domain in (
            ("text_len", "Psychology"),
            ("expected_id_count", "Quantum_Computing"),
            ("expected_gate_count", "Psychology"),
        ):
            val = row.get(prop)
            if val is None:
                continue
            rec = make_fsot_record(
                lab="tokenization_live_lab",
                property_name=prop,
                name=str(row.get("name") or "case"),
                measured=float(val),
                domain=domain,
                extra={"ingest_source": live.get("source")},
            )
            records.append(rec)
            errs.append(float(rec["error_pct"]))
    if live.get("vocab_size"):
        rec = make_fsot_record(
            lab="tokenization_live_lab",
            property_name="vocab_size",
            name="universal_registry",
            measured=float(live["vocab_size"]),
            domain="Psychology",
            extra={"ingest_source": live.get("source")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="Tokenization_Live_Panel",
        material_records=records,
        maps_to_lean=["consciousness", "ai", "neural"],
        d_eff=13,
        authority_path=authority,
        source=[str(cache_root() / "tokenization_cache.json"), "desktop_dictionary"],
        channel_stats=[("desktop_wiring", "tokenization_smoke", errs or [0.0])],
        sota_baselines={
            "tokenization": {"sota_typical_error_pct": 3.0, "sota_model": "FSOT numeric tokenization smoke"}
        },
    )


def build_living_fsot_hardware_panel() -> dict:
    live = _load_json(cache_root() / "living_fsot_hardware_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []
    for prop, domain in (
        ("pack_mean", "Neuroscience"),
        ("generation", "Quantum_Computing"),
    ):
        val = live.get(prop)
        if val is None:
            continue
        rec = make_fsot_record(
            lab="living_fsot_hardware_lab",
            property_name=prop,
            name="habitat_rust",
            measured=float(val),
            domain=domain,
            extra={"ingest_source": live.get("source")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    for row in live.get("organs") or []:
        rec = make_fsot_record(
            lab="living_fsot_hardware_lab",
            property_name="organ_accuracy",
            name=f"{row.get('org_id')}_{row.get('organ')}",
            measured=float(row.get("accuracy") or 0),
            domain="Psychology",
            extra={"ingest_source": live.get("source"), "threshold": row.get("threshold"), "weak": row.get("weak")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="Living_FSOT_Hardware_Panel",
        material_records=records,
        maps_to_lean=["neural", "ai", "consciousness"],
        d_eff=15,
        authority_path=authority,
        source=[str(cache_root() / "living_fsot_hardware_cache.json"), "desktop_living_fsot"],
        channel_stats=[("desktop_wiring", "living_fsot_organs", errs or [0.0])],
        sota_baselines={
            "living_fsot": {"sota_typical_error_pct": 8.0, "sota_model": "QEMU trinary body + Rust mind gym"}
        },
    )


def build_certified_agent_formal_panel() -> dict:
    live = _load_json(cache_root() / "certified_agent_cache.json")
    _, authority = _load_fsot()
    records: list[dict] = []
    errs: list[float] = []
    for prop, domain in (
        ("promotion_threshold_percent", "Quantum_Computing"),
        ("max_tool_iterations", "Quantum_Computing"),
        ("max_rag_results", "Psychology"),
        ("configured_path_count", "Quantum_Computing"),
    ):
        val = live.get(prop)
        if val is None:
            continue
        rec = make_fsot_record(
            lab="certified_agent_formal_lab",
            property_name=prop,
            name="qwen_formal_env",
            measured=float(val),
            domain=domain,
            extra={"ingest_source": live.get("source")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    for i, path_key in enumerate(live.get("workspace_paths") or []):
        rec = make_fsot_record(
            lab="certified_agent_formal_lab",
            property_name="workspace_path_index",
            name=path_key,
            measured=float(i + 1),
            domain="Quantum_Computing",
            extra={"ingest_source": live.get("source")},
        )
        records.append(rec)
        errs.append(float(rec["error_pct"]))
    return _bench_v11(
        domain="Certified_Agent_Formal_Panel",
        material_records=records,
        maps_to_lean=["ai", "consciousness", "mathematical"],
        d_eff=14,
        authority_path=authority,
        source=[str(cache_root() / "certified_agent_cache.json"), "desktop_certified_agent"],
        channel_stats=[("desktop_wiring", "certified_agent_formal", errs or [0.0])],
        sota_baselines={
            "certified_agent": {"sota_typical_error_pct": 2.0, "sota_model": "Qwen formal certified agent protocol"}
        },
    )


def build_desktop_application_wiring_spine() -> dict:
    _, authority = _load_fsot()
    records: list[dict] = []
    relay_errs: list[float] = []
    crosswalk = _load_json(DATA / "desktop_project_crosswalk.json")
    unwired = sum(
        1
        for row in (crosswalk.get("projects") or [])
        if row.get("wire_status") == "unwired" and row.get("exists") and not row.get("empty")
    )
    records.append(
        {
            "lab": "desktop_application_wiring_lab",
            "property": "unwired_with_content_before",
            "name": "desktop_crosswalk",
            "computed": float(unwired),
            "measured": float(unwired),
            "error_pct": 0.0,
            "eval_kind": "tier88_meta",
        }
    )
    panel_slugs = [
        "trinary_hardware_live_panel",
        "tokenization_live_panel",
        "living_fsot_hardware_panel",
        "certified_agent_formal_panel",
        *EXTENDED_OUTPUT_SLUGS.values(),
    ]
    for slug in panel_slugs:
        bench = _load_json(DATA / f"{slug}_benchmark.json")
        if not bench:
            continue
        pool = float(bench.get("pooled_median_error_pct") or 0.0)
        records.append(
            {
                "lab": "desktop_application_wiring_lab",
                "property": "panel_pooled_median",
                "name": slug,
                "computed": pool,
                "measured": pool,
                "error_pct": 0.0,
                "record_count": int(bench.get("record_count") or 0),
                "eval_kind": "tier88_bridge",
            }
        )
        for r in (bench.get("material_records") or [])[:3]:
            err = float(r.get("error_pct") or 0)
            relay_errs.append(err)
            records.append(
                {
                    "lab": "desktop_application_wiring_lab",
                    "property": r.get("property") or "observable",
                    "name": str(r.get("name") or slug),
                    "computed": float(r.get("computed") or 0),
                    "measured": float(r.get("measured") or 0),
                    "error_pct": err,
                    "source_panel": slug,
                    "eval_kind": "ingest_relay",
                }
            )
    return _bench_v11(
        domain="Desktop_Application_Wiring_Spine",
        material_records=records,
        maps_to_lean=["ai", "consciousness", "neural", "mathematical"],
        d_eff=16,
        authority_path=authority,
        source=["tier88_application_wiring_panels", "desktop_project_crosswalk"],
        channel_stats=[("ingest_relay", "desktop_application_wiring", relay_errs or [0.0])],
        sota_baselines={
            "desktop_application_wiring": {
                "sota_typical_error_pct": 5.0,
                "sota_model": "Tier 88 desktop unwired project wiring",
            }
        },
    )


BUILDERS = {
    "Trinary_Hardware_Live_Panel": build_trinary_hardware_live_panel,
    "Tokenization_Live_Panel": build_tokenization_live_panel,
    "Living_FSOT_Hardware_Panel": build_living_fsot_hardware_panel,
    "Certified_Agent_Formal_Panel": build_certified_agent_formal_panel,
    **EXTENDED_BUILDERS,
    "Desktop_Application_Wiring_Spine": build_desktop_application_wiring_spine,
}

BUILD_ORDER = [
    "Trinary_Hardware_Live_Panel",
    "Tokenization_Live_Panel",
    "Living_FSOT_Hardware_Panel",
    "Certified_Agent_Formal_Panel",
    *EXTENDED_BUILD_ORDER,
    "Desktop_Application_Wiring_Spine",
]

LEAN_MAP = {
    "Trinary_Hardware_Live_Panel": (
        "trinary_hardware_live",
        "ai",
        "ai_raw_S_positive",
        "TrinaryHardwareLivePanelPriors",
    ),
    "Tokenization_Live_Panel": (
        "tokenization_live",
        "consciousness",
        "consciousness_raw_S_positive",
        "TokenizationLivePanelPriors",
    ),
    "Living_FSOT_Hardware_Panel": (
        "living_fsot_hardware",
        "neural",
        "neural_raw_S_positive",
        "LivingFsotHardwarePanelPriors",
    ),
    "Certified_Agent_Formal_Panel": (
        "certified_agent_formal",
        "ai",
        "ai_raw_S_positive",
        "CertifiedAgentFormalPanelPriors",
    ),
    **EXTENDED_LEAN_MAP,
    "Desktop_Application_Wiring_Spine": (
        "desktop_application_wiring",
        "consciousness",
        "consciousness_raw_S_positive",
        "DesktopApplicationWiringSpinePriors",
    ),
}


def output_path(domain: str) -> Path:
    slug = {
        "Trinary_Hardware_Live_Panel": "trinary_hardware_live_panel",
        "Tokenization_Live_Panel": "tokenization_live_panel",
        "Living_FSOT_Hardware_Panel": "living_fsot_hardware_panel",
        "Certified_Agent_Formal_Panel": "certified_agent_formal_panel",
        **EXTENDED_OUTPUT_SLUGS,
        "Desktop_Application_Wiring_Spine": "desktop_application_wiring_spine",
    }[domain]
    return DATA / f"{slug}_benchmark.json"