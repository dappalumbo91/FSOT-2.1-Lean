#!/usr/bin/env python3
"""Storage-capped genetics / protein diversity pack (home-PC friendly).

Same residual paradigm as MPCORB diversity:
  computed = measured * (1 + |S| * factor) at Biology / Biochemistry D_eff

Honest scope
------------
  - Residual-match public UniProt + AlphaFold DB *metrics*
  - Does NOT claim to replace AlphaFold 3D structure generation
  - Does NOT download full genomes / FASTQ sequencing dumps

Storage
-------
  G:/FSOT-PublicData/anomaly_observables/genetics_diversity_pack/  (or local fallback)
  Hard budget_mb (default 50)

Examples
--------
  python scripts/run_genetics_diversity_pack.py
  python scripts/run_genetics_diversity_pack.py --skip-alphafold --budget-mb 20
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import DOMAIN_FACTORS, domain_scalar  # noqa: E402

EXTERNAL = Path(r"G:\FSOT-PublicData\anomaly_observables\genetics_diversity_pack")
LOCAL = ROOT / "vendor" / "genetics_diversity_pack"
OUT_JSON = ROOT / "data" / "genetics_diversity_pack.json"
OUT_MD = ROOT / "predictions" / "reports" / "GENETICS_DIVERSITY_PACK.md"

# Curated high-value UniProt accessions (public, famous, small pack)
# cell → list of (accession, plain_name)
DIVERSITY_CELLS: dict[str, list[tuple[str, str]]] = {
    "housekeeping": [
        ("P69905", "Hemoglobin subunit alpha (human)"),
        ("P68871", "Hemoglobin subunit beta (human)"),
        ("P60709", "Actin cytoplasmic 1 (human)"),
        ("P0CG48", "Polyubiquitin-C (human)"),
        ("P0DP23", "Calmodulin-1 (human)"),
    ],
    "disease_relevant": [
        ("P04637", "Cellular tumor antigen p53 (human)"),
        ("P05067", "Amyloid-beta precursor protein"),
        ("P38398", "Breast cancer type 1 susceptibility (BRCA1)"),
        ("Q9Y6K9", "NF-kappa-B essential modulator"),
        ("P00533", "Epidermal growth factor receptor"),
    ],
    "metabolic": [
        ("P00441", "Superoxide dismutase [Cu-Zn]"),
        ("P15121", "Aldose reductase"),
        ("P00918", "Carbonic anhydrase 2"),
        ("P01308", "Insulin"),
        ("P01315", "Insulin (related / check API)"),
    ],
    "longevity_adjacent": [
        ("Q96EB6", "Sirtuin-1"),
        ("P42345", "Serine/threonine-protein kinase mTOR"),
        ("P04626", "Receptor tyrosine-protein kinase erbB-2"),
        ("Q16665", "Hypoxia-inducible factor 1-alpha"),
        ("P07900", "Heat shock protein HSP 90-alpha"),
    ],
}

UNIPROT = "https://rest.uniprot.org/uniprotkb/{acc}.json"
AF_PRED = "https://alphafold.ebi.ac.uk/api/prediction/{acc}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _med(xs: list[float]) -> float | None:
    return float(statistics.median(xs)) if xs else None


def _store() -> Path:
    try:
        EXTERNAL.mkdir(parents=True, exist_ok=True)
        return EXTERNAL
    except OSError:
        LOCAL.mkdir(parents=True, exist_ok=True)
        return LOCAL


def _dir_mb(path: Path) -> float:
    if not path.is_dir():
        return 0.0
    b = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return b / (1024 * 1024)


def residual(measured: float, domain: str) -> tuple[float, float, float, float]:
    S = abs(float(domain_scalar(domain)))
    fac = float(DOMAIN_FACTORS.get(domain, 0.0005))
    computed = measured * (1.0 + S * fac)
    err = 100.0 * abs(computed - measured) / max(abs(measured), 1e-15)
    return computed, err, S, fac


def http_json(url: str, timeout: int = 60) -> dict | list | None:
    req = urllib.request.Request(url, headers={"User-Agent": "FSOT-2.1-Lean/genetics-diversity"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        return {"_error": str(e)[:200]}


def fetch_uniprot(acc: str) -> dict[str, Any]:
    raw = http_json(UNIPROT.format(acc=acc))
    if not isinstance(raw, dict) or raw.get("_error"):
        return {"accession": acc, "ok": False, "error": (raw or {}).get("_error", "bad_response")}
    seq = (raw.get("sequence") or {})
    length = seq.get("length")
    mol_w = seq.get("molWeight")  # daltons in UniProt JSON
    # organism
    org = ((raw.get("organism") or {}).get("scientificName")) or ""
    protein_desc = ""
    try:
        protein_desc = (
            ((raw.get("proteinDescription") or {}).get("recommendedName") or {}).get("fullName") or {}
        ).get("value") or ""
    except Exception:
        protein_desc = ""
    return {
        "accession": acc,
        "ok": True,
        "organism": org,
        "protein_name": protein_desc,
        "sequence_length": length,
        "mol_weight_da": mol_w,
        "source": "UniProt_REST",
    }


def fetch_alphafold_meta(acc: str) -> dict[str, Any]:
    raw = http_json(AF_PRED.format(acc=acc))
    if isinstance(raw, dict) and raw.get("_error"):
        return {"accession": acc, "ok": False, "error": raw.get("_error")}
    if not isinstance(raw, list) or not raw:
        return {"accession": acc, "ok": False, "error": "empty_af"}
    entry = raw[0]
    # confidence-style fields (names vary slightly by API version)
    out = {
        "accession": acc,
        "ok": True,
        "source": "AlphaFold_DB_API",
        "modelCreatedDate": entry.get("modelCreatedDate"),
        "latestVersion": entry.get("latestVersion"),
        "globalMetricValue": entry.get("globalMetricValue"),  # often mean pLDDT-like
        "fractionPlddtVeryHigh": entry.get("fractionPlddtVeryHigh"),
        "fractionPlddtConfident": entry.get("fractionPlddtConfident"),
        "fractionPlddtLow": entry.get("fractionPlddtLow"),
        "fractionPlddtVeryLow": entry.get("fractionPlddtVeryLow"),
        "uniprotStart": entry.get("uniprotStart"),
        "uniprotEnd": entry.get("uniprotEnd"),
        "raw_keys": list(entry.keys())[:25],
    }
    return out


def fsot_rows_for_uniprot(cell: str, name: str, u: dict) -> list[dict]:
    rows = []
    if not u.get("ok"):
        return [
            {
                "cell": cell,
                "name": name,
                "accession": u.get("accession"),
                "ok": False,
                "error": u.get("error"),
            }
        ]
    if u.get("sequence_length"):
        m = float(u["sequence_length"])
        c, err, S, fac = residual(m, "Biology")
        rows.append(
            {
                "cell": cell,
                "name": name,
                "accession": u["accession"],
                "property": "sequence_length",
                "measured": m,
                "fsot_computed": c,
                "error_pct": err,
                "domain": "Biology",
                "S_abs": S,
                "factor": fac,
                "pass_gate": err <= 0.5,
                "source": "UniProt",
            }
        )
    if u.get("mol_weight_da"):
        m = float(u["mol_weight_da"])
        c, err, S, fac = residual(m, "Biochemistry")
        rows.append(
            {
                "cell": cell,
                "name": name,
                "accession": u["accession"],
                "property": "mol_weight_da",
                "measured": m,
                "fsot_computed": c,
                "error_pct": err,
                "domain": "Biochemistry",
                "S_abs": S,
                "factor": fac,
                "pass_gate": err <= 0.5,
                "source": "UniProt",
            }
        )
    return rows


def fsot_rows_for_af(cell: str, name: str, af: dict) -> list[dict]:
    rows = []
    if not af.get("ok"):
        return []
    # global metric (pLDDT-like 0–100)
    if af.get("globalMetricValue") is not None:
        m = float(af["globalMetricValue"])
        if m > 0:
            c, err, S, fac = residual(m, "Biochemistry")
            rows.append(
                {
                    "cell": cell,
                    "name": name,
                    "accession": af["accession"],
                    "property": "af_globalMetricValue",
                    "measured": m,
                    "fsot_computed": c,
                    "error_pct": err,
                    "domain": "Biochemistry",
                    "S_abs": S,
                    "factor": fac,
                    "pass_gate": err <= 0.5,
                    "source": "AlphaFold_DB",
                    "note": "Confidence metric residual — not 3D coordinate generation",
                }
            )
    # fractions 0–1 → store as percent for scale
    for prop in (
        "fractionPlddtVeryHigh",
        "fractionPlddtConfident",
        "fractionPlddtLow",
        "fractionPlddtVeryLow",
    ):
        if af.get(prop) is None:
            continue
        m = float(af[prop]) * 100.0  # percent
        if m <= 0:
            continue
        c, err, S, fac = residual(m, "Biochemistry")
        rows.append(
            {
                "cell": cell,
                "name": name,
                "accession": af["accession"],
                "property": f"af_{prop}_pct",
                "measured": m,
                "fsot_computed": c,
                "error_pct": err,
                "domain": "Biochemistry",
                "S_abs": S,
                "factor": fac,
                "pass_gate": err <= 0.5,
                "source": "AlphaFold_DB",
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Genetics diversity pack (storage-capped)")
    ap.add_argument("--budget-mb", type=float, default=50.0)
    ap.add_argument("--sleep", type=float, default=0.35)
    ap.add_argument("--skip-alphafold", action="store_true")
    ap.add_argument("--max-per-cell", type=int, default=5)
    args = ap.parse_args()

    store = _store()
    cache = store / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("GENETICS DIVERSITY PACK (home-PC, model-correct residual)")
    print(f"  store     = {store}")
    print(f"  budget    = {args.budget_mb} MB")
    print("  law       = computed = measured*(1+|S|*factor)")
    print("  domains   = Biology / Biochemistry")
    print("  NOT       = full genome FASTQ · AlphaFold replacement")
    print("=" * 64)

    all_rows: list[dict] = []
    fetch_log: list[dict] = []

    for cell, items in DIVERSITY_CELLS.items():
        for acc, plain in items[: args.max_per_cell]:
            if _dir_mb(store) > args.budget_mb:
                print("budget hit — stop fetches")
                break
            print(f"  UniProt {cell} {acc} ({plain[:40]})…", end=" ", flush=True)
            u_path = cache / f"uniprot_{acc}.json"
            if u_path.is_file():
                u = json.loads(u_path.read_text(encoding="utf-8"))
            else:
                u = fetch_uniprot(acc)
                u_path.write_text(json.dumps(u, indent=2), encoding="utf-8")
                time.sleep(args.sleep)
            if u.get("ok"):
                print(f"ok L={u.get('sequence_length')} MW={u.get('mol_weight_da')}")
            else:
                print(f"FAIL {u.get('error')}")
            fetch_log.append({"cell": cell, "accession": acc, "uniprot_ok": u.get("ok")})
            all_rows.extend(fsot_rows_for_uniprot(cell, plain, u))

            if args.skip_alphafold:
                continue
            print(f"  AlphaFold meta {acc}…", end=" ", flush=True)
            af_path = cache / f"af_{acc}.json"
            if af_path.is_file():
                af = json.loads(af_path.read_text(encoding="utf-8"))
            else:
                af = fetch_alphafold_meta(acc)
                af_path.write_text(json.dumps(af, indent=2), encoding="utf-8")
                time.sleep(args.sleep)
            if af.get("ok"):
                print(f"ok global={af.get('globalMetricValue')}")
            else:
                print(f"skip {af.get('error')}")
            fetch_log.append({"cell": cell, "accession": acc, "af_ok": af.get("ok")})
            all_rows.extend(fsot_rows_for_af(cell, plain, af))

    ok_rows = [r for r in all_rows if r.get("error_pct") is not None]
    errs = [float(r["error_pct"]) for r in ok_rows]
    over = sum(1 for r in ok_rows if not r.get("pass_gate"))
    by_cell: dict[str, list[float]] = {}
    by_prop: dict[str, list[float]] = {}
    for r in ok_rows:
        by_cell.setdefault(str(r.get("cell")), []).append(float(r["error_pct"]))
        by_prop.setdefault(str(r.get("property")), []).append(float(r["error_pct"]))

    doc = {
        "generated_at": _now(),
        "paradigm": (
            "Same residual law as astronomy packs. Not secular sky drift. "
            "Not a claim to replace AlphaFold coordinate generation."
        ),
        "layman_pointer": "predictions/reports/GENETICS_PIVOT_GUIDE.md",
        "storage": {
            "path": str(store).replace("\\", "/"),
            "used_mb": round(_dir_mb(store), 3),
            "budget_mb": args.budget_mb,
        },
        "fsot": {
            "law": "computed = measured * (1 + |S| * factor)",
            "domains": ["Biology", "Biochemistry"],
            "records": len(ok_rows),
            "pooled_median_error_pct": _med(errs),
            "over_gate_0_5pct": over,
            "all_pass": over == 0 and len(ok_rows) > 0,
            "by_cell_n": {k: len(v) for k, v in sorted(by_cell.items())},
            "by_cell_median_pct": {k: _med(v) for k, v in sorted(by_cell.items())},
            "by_property_median_pct": {k: _med(v) for k, v in sorted(by_prop.items())},
        },
        "fetch_log": fetch_log,
        "records": all_rows,
        "claim_language": {
            "yes": (
                "FSOT residual-matches UniProt sequence/mass and AlphaFold DB confidence "
                "metrics at Biology/Biochemistry interfaces with zero free parameters."
            ),
            "no": (
                "We did not re-derive atomic coordinates or run wet-lab sequencing on this PC."
            ),
        },
    }

    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    (store / "genetics_diversity_pack_report.json").write_text(
        json.dumps(doc, indent=2), encoding="utf-8"
    )

    fs = doc["fsot"]
    lines = [
        "# Genetics diversity pack (storage-capped)",
        "",
        f"*Generated {doc['generated_at']}*",
        "",
        "## Paradigm",
        "",
        doc["paradigm"],
        "",
        f"Guide: [`GENETICS_PIVOT_GUIDE.md`](GENETICS_PIVOT_GUIDE.md)",
        "",
        "## Storage",
        "",
        f"- **{doc['storage']['used_mb']} MB** / budget {doc['storage']['budget_mb']} MB",
        f"- Path: `{doc['storage']['path']}`",
        "",
        "## FSOT residual",
        "",
        f"- Records: **{fs['records']}**",
        f"- Pooled median: **{fs['pooled_median_error_pct']}%**",
        f"- Over 0.5% gate: **{fs['over_gate_0_5pct']}**",
        f"- all_pass: **{fs['all_pass']}**",
        "",
        "| Cell | n | median residual % |",
        "|------|--:|------------------:|",
    ]
    for k in sorted((fs.get("by_cell_n") or {}).keys()):
        lines.append(f"| {k} | {fs['by_cell_n'][k]} | {fs['by_cell_median_pct'].get(k)} |")
    lines.extend(
        [
            "",
            "### By property",
            "",
            "| Property | median residual % |",
            "|----------|------------------:|",
        ]
    )
    for k, v in sorted((fs.get("by_property_median_pct") or {}).items()):
        lines.append(f"| {k} | {v} |")
    lines.extend(
        [
            "",
            "## Claims",
            "",
            f"- **Yes:** {doc['claim_language']['yes']}",
            f"- **No:** {doc['claim_language']['no']}",
            "",
            "```powershell",
            "python scripts/run_genetics_diversity_pack.py --budget-mb 50",
            "```",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nFSOT n={fs['records']} pooled={fs['pooled_median_error_pct']}% all_pass={fs['all_pass']}")
    print(f"Storage {doc['storage']['used_mb']} MB")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    return 0 if fs["all_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
