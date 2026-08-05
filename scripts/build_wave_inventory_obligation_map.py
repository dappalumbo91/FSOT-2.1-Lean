#!/usr/bin/env python3
"""
Map fsot_compute wave1–wave10 Results → Lean modules → multiprover obligations.

Closes the atlas "orphan wave numbers" gap: every wave Result is an explicit
inventory row with formal-spine / catalog / residual links when available.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "vendor"))
sys.path.insert(0, str(ROOT / "scripts"))

OUT_JSON = ROOT / "data" / "wave_inventory_obligation_map.json"
OUT_MD = ROOT / "docs" / "WAVE_INVENTORY_OBLIGATION_MAP.md"
OUT_OBL = ROOT / "verification" / "obligations" / "wave_inventory_spine.json"
FORMAL = ROOT / "FSOT" / "Formal"
SPINE = ROOT / "verification" / "obligations" / "full_formal_spine.json"
CATALOG = ROOT / "verification" / "obligations" / "scientific_catalog_spine.json"
MARGIN = ROOT / "data" / "benchmark_margin_audit.json"

# Wave → primary Lean module(s) and residual/domain routing
WAVE_META: dict[int, dict] = {
    1: {
        "lean_modules": ["Cosmology", "CosmologyLab"],
        "lab_key": "cosmology_wave1_lab",
        "theme": "ΛCDM core (α_s, H0, T_CMB, n_s, Ω_b h²)",
        "domain_route": "cosmological",
    },
    2: {
        "lean_modules": ["Cosmology", "CosmologyLab", "CosmologyExtendedPriors"],
        "lab_key": "cosmology_wave2_lab",
        "theme": "Extended SM / dark-sector anchors",
        "domain_route": "cosmological",
    },
    3: {
        "lean_modules": ["Cosmology", "CosmologyLab", "CosmologyExtendedPriors"],
        "lab_key": "cosmology_wave3_lab",
        "theme": "CKM / age / acoustic-scale anchors",
        "domain_route": "particle",
    },
    4: {
        "lean_modules": ["CosmologyWave4Priors", "CosmologyWave4"],
        "lab_key": "cosmology_wave4_lab",
        "theme": "PMNS + CKM depth",
        "domain_route": "particle",
    },
    5: {
        "lean_modules": ["CosmologyWave5Priors"],
        "lab_key": "cosmology_wave5_lab",
        "theme": "Z-pole / electroweak precision",
        "domain_route": "particle",
    },
    6: {
        "lean_modules": ["CosmologyWave6Priors"],
        "lab_key": "cosmology_wave6_lab",
        "theme": "Mathematical constants (ζ, Levy, …)",
        "domain_route": "mathematical",
    },
    7: {
        "lean_modules": ["CosmologyWave7Priors"],
        "lab_key": "cosmology_wave7_lab",
        "theme": "Apéry / Soldner / number-theory constants",
        "domain_route": "mathematical",
    },
    8: {
        "lean_modules": ["CosmologyWave8Priors", "CosmologyHigherWavesPriors"],
        "lab_key": "cosmology_wave8_lab",
        "theme": "CKM unitarity + BR / mass ratios",
        "domain_route": "particle",
    },
    9: {
        "lean_modules": ["CosmologyWave9Priors", "CosmologyHigherWavesPriors"],
        "lab_key": "cosmology_wave9_lab",
        "theme": "Top / radiation / fractal geometry",
        "domain_route": "particle",
    },
    10: {
        "lean_modules": ["CosmologyWave10Priors", "CosmologyHigherWavesPriors"],
        "lab_key": "cosmology_wave10_lab",
        "theme": "Lepton moments / logistic / triple-point",
        "domain_route": "particle",
    },
}


def _load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _spine_by_module(spine: dict | None) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    if not spine:
        return out
    for ob in spine.get("obligations") or []:
        mod = str(ob.get("lean_module") or "").replace("FSOT.Formal.", "")
        out.setdefault(mod, []).append(
            {
                "id": ob.get("id"),
                "kind": ob.get("kind"),
                "provable": ob.get("provable"),
                "name": ob.get("name") or ob.get("theorem"),
            }
        )
    return out


def _catalog_domains(catalog: dict | None) -> set[str]:
    if not catalog:
        return set()
    domains: set[str] = set()
    for ob in catalog.get("obligations") or []:
        d = ob.get("domain") or ob.get("catalog_domain")
        if d:
            domains.add(str(d))
    return domains


def _margin_index(margin: dict | None) -> dict[str, dict]:
    """Map domain / file slug → green status."""
    idx: dict[str, dict] = {}
    if not margin:
        return idx
    for row in margin.get("rows") or margin.get("benchmarks") or []:
        domain = str(row.get("domain") or row.get("panel") or "")
        if not domain:
            continue
        idx[domain] = {
            "pooled_median_error_pct": row.get("official_pooled_median_error_pct")
            or row.get("pooled_median_error_pct"),
            "green": row.get("green_gate_pass")
            if row.get("green_gate_pass") is not None
            else (
                float(row.get("official_pooled_median_error_pct") or 99) <= 0.5
                if row.get("official_pooled_median_error_pct") is not None
                else None
            ),
            "file": row.get("file") or row.get("benchmark_file"),
        }
    return idx


def _err_pct(computed: float, measured: float) -> float:
    if measured == 0:
        return 0.0 if computed == 0 else 100.0
    return abs(computed - measured) / abs(measured) * 100.0


def collect_waves() -> list[dict]:
    import fsot_compute as fc  # noqa: WPS433

    waves: list[dict] = []
    for n in range(1, 11):
        fn = getattr(fc, f"wave{n}")
        results = fn()
        meta = WAVE_META[n]
        lean_paths = []
        for mod in meta["lean_modules"]:
            p = FORMAL / f"{mod}.lean"
            lean_paths.append(
                {
                    "module": mod,
                    "path": f"FSOT/Formal/{mod}.lean",
                    "exists": p.is_file(),
                }
            )
        items = []
        errs: list[float] = []
        for r in results:
            computed = float(r.computed)
            measured = float(r.measured)
            e = _err_pct(computed, measured)
            errs.append(e)
            items.append(
                {
                    "name": r.name,
                    "formula": r.formula_str,
                    "computed": computed,
                    "measured": measured,
                    "sigma": getattr(r, "sigma", None),
                    "error_pct": round(e, 6),
                    "within_half_pct": e <= 0.5,
                    "within_green": e <= 0.5,
                }
            )
        med = sorted(errs)[len(errs) // 2] if errs else None
        max_e = max(errs) if errs else None
        waves.append(
            {
                "wave": n,
                "fn": f"wave{n}",
                "theme": meta["theme"],
                "domain_route": meta["domain_route"],
                "lab_key": meta["lab_key"],
                "lean_modules": lean_paths,
                "observable_count": len(items),
                "median_error_pct": round(med, 6) if med is not None else None,
                "max_error_pct": round(max_e, 6) if max_e is not None else None,
                "all_within_half_pct": all(i["within_half_pct"] for i in items),
                "observables": items,
            }
        )
    return waves


def attach_obligations(waves: list[dict], by_mod: dict[str, list[dict]]) -> None:
    for w in waves:
        obl: list[dict] = []
        seen: set[str] = set()
        for lm in w["lean_modules"]:
            mod = lm["module"]
            for o in by_mod.get(mod, []):
                oid = str(o.get("id") or "")
                if oid and oid not in seen:
                    seen.add(oid)
                    obl.append(o)
        w["obligation_ids"] = [o.get("id") for o in obl if o.get("id")]
        w["obligation_count"] = len(obl)
        w["obligations_sample"] = obl[:12]
        w["lean_modules_missing"] = [
            lm["module"] for lm in w["lean_modules"] if not lm["exists"]
        ]


def build_obligation_export(waves: list[dict]) -> dict:
    """Lightweight spine for multiprover: wave counts + green flags."""
    obligations: list[dict] = []
    for w in waves:
        n = w["wave"]
        obligations.append(
            {
                "id": f"wave{n}_observable_count",
                "kind": "eq_nat",
                "wave": n,
                "claim": f"wave{n} has {w['observable_count']} Results",
                "value": w["observable_count"],
                "lean_module": (
                    WAVE_META[n]["lean_modules"][0]
                    if WAVE_META[n]["lean_modules"]
                    else None
                ),
                "provable": True,
            }
        )
        obligations.append(
            {
                "id": f"wave{n}_median_under_half",
                "kind": "r_lt_lit",
                "wave": n,
                "claim": f"wave{n} median error_pct < 0.5",
                "value": w["median_error_pct"],
                "threshold": 0.5,
                "holds": bool(w["median_error_pct"] is not None and w["median_error_pct"] < 0.5),
                "lean_module": (
                    WAVE_META[n]["lean_modules"][0]
                    if WAVE_META[n]["lean_modules"]
                    else None
                ),
                "provable": bool(
                    w["median_error_pct"] is not None and w["median_error_pct"] < 0.5
                ),
            }
        )
        obligations.append(
            {
                "id": f"wave{n}_max_under_green",
                "kind": "r_lt_lit",
                "wave": n,
                "claim": f"wave{n} max error_pct < 0.5 (strict green aspiration)",
                "value": w["max_error_pct"],
                "threshold": 0.5,
                "holds": bool(w["max_error_pct"] is not None and w["max_error_pct"] < 0.5),
                "note": "Some waves use sigma bands; max may exceed 0.5% while median is green",
                "lean_module": (
                    WAVE_META[n]["lean_modules"][0]
                    if WAVE_META[n]["lean_modules"]
                    else None
                ),
                "provable": bool(
                    w["max_error_pct"] is not None and w["max_error_pct"] < 0.5
                ),
            }
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "source": "scripts/build_wave_inventory_obligation_map.py",
        "wave_count": 10,
        "obligation_count": len(obligations),
        "obligations": obligations,
    }


def write_md(doc: dict) -> str:
    lines = [
        "# Wave inventory → obligation map",
        "",
        f"**Generated:** {doc['generated_at']}  ",
        f"**Status:** `{doc['status']}`  ",
        f"**Waves:** {doc['wave_count']} · **Observables:** {doc['total_observables']} · "
        f"**Linked obligations:** {doc['total_linked_obligations']}",
        "",
        "Every `fsot_compute.waveN()` Result is inventoried against Lean modules and "
        "multiprover obligation IDs so wave numbers are never orphan atlas entries.",
        "",
        "## Master formula",
        "",
        "`S = K·(T1+T2+T3)` · structure module: `FSOT/Formal/ScalarEngineStructure.lean`",
        "",
        "## Wave summary",
        "",
        "| Wave | n | median% | max% | half-pct | Lean modules | #obl | Theme |",
        "|-----:|--:|--------:|-----:|:--------:|--------------|-----:|-------|",
    ]
    for w in doc["waves"]:
        mods = ", ".join(
            ("✓ " if lm["exists"] else "✗ ") + lm["module"] for lm in w["lean_modules"]
        )
        half = "yes" if w["all_within_half_pct"] else "mixed"
        lines.append(
            f"| {w['wave']} | {w['observable_count']} | {w['median_error_pct']} | "
            f"{w['max_error_pct']} | {half} | {mods} | {w['obligation_count']} | {w['theme']} |"
        )
    lines += [
        "",
        "## Per-wave observables",
        "",
    ]
    for w in doc["waves"]:
        lines.append(f"### Wave {w['wave']} — `{w['fn']}`")
        lines.append("")
        lines.append(f"- **Theme:** {w['theme']}")
        lines.append(f"- **Domain route:** `{w['domain_route']}`")
        lines.append(f"- **Lab key:** `{w['lab_key']}`")
        lines.append(
            f"- **Obligations:** {w['obligation_count']} "
            f"(sample: {', '.join(str(x) for x in (w.get('obligation_ids') or [])[:6]) or '—'})"
        )
        if w.get("lean_modules_missing"):
            lines.append(
                f"- **Missing Lean modules:** {', '.join(w['lean_modules_missing'])}"
            )
        lines.append("")
        lines.append("| Observable | Formula | Error% | ≤0.5% |")
        lines.append("|------------|---------|-------:|:-----:|")
        for o in w["observables"]:
            flag = "✓" if o["within_half_pct"] else "·"
            formula = (o["formula"] or "").replace("|", "\\|")
            lines.append(
                f"| `{o['name']}` | `{formula}` | {o['error_pct']} | {flag} |"
            )
        lines.append("")
    lines += [
        "## Reproduction",
        "",
        "```bash",
        "python scripts/build_wave_inventory_obligation_map.py",
        "python -c \"import sys; sys.path.insert(0,'vendor'); import fsot_compute as f; "
        "print(sum(len(getattr(f,f'wave{i}')()) for i in range(1,11)))\"",
        "```",
        "",
        "## Artifacts",
        "",
        f"- `{OUT_JSON.relative_to(ROOT).as_posix()}`",
        f"- `{OUT_OBL.relative_to(ROOT).as_posix()}`",
        f"- `{OUT_MD.relative_to(ROOT).as_posix()}`",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    waves = collect_waves()
    spine = _load_json(SPINE)
    by_mod = _spine_by_module(spine if isinstance(spine, dict) else None)
    attach_obligations(waves, by_mod)

    total_obs = sum(w["observable_count"] for w in waves)
    total_obl = sum(w["obligation_count"] for w in waves)
    missing = [m for w in waves for m in w.get("lean_modules_missing") or []]
    orphans = [w for w in waves if w["obligation_count"] == 0]
    status = "MAPPED"
    if missing or orphans:
        status = "MAPPED_WITH_GAPS"

    spine_export = build_obligation_export(waves)
    OUT_OBL.parent.mkdir(parents=True, exist_ok=True)
    OUT_OBL.write_text(json.dumps(spine_export, indent=2), encoding="utf-8")

    doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0",
        "status": status,
        "master_formula": "S = K*(T1+T2+T3); c = m*(1+|S|*f)",
        "structure_module": "FSOT/Formal/ScalarEngineStructure.lean",
        "wave_count": len(waves),
        "total_observables": total_obs,
        "total_linked_obligations": total_obl,
        "missing_lean_modules": sorted(set(missing)),
        "orphan_waves": [w["wave"] for w in orphans],
        "waves": waves,
        "artifacts": {
            "json": str(OUT_JSON.relative_to(ROOT).as_posix()),
            "md": str(OUT_MD.relative_to(ROOT).as_posix()),
            "obligation_spine": str(OUT_OBL.relative_to(ROOT).as_posix()),
        },
        "commands": {
            "rebuild": "python scripts/build_wave_inventory_obligation_map.py",
            "regen_wave_priors": "python scripts/gen_cosmology_wave_lean.py",
            "cross_proof": "python scripts/run_cross_proof_verification.py",
        },
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(write_md(doc), encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_OBL}")
    print(f"  status={status} waves={len(waves)} observables={total_obs} linked_obl={total_obl}")
    if missing:
        print(f"  missing modules: {missing}")
    if orphans:
        print(f"  orphan waves (0 obligations): {[w['wave'] for w in orphans]}")
    return 0 if status == "MAPPED" else 0  # map always succeeds; gaps are informational


if __name__ == "__main__":
    raise SystemExit(main())
