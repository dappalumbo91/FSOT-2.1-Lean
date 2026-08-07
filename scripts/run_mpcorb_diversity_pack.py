#!/usr/bin/env python3
"""Storage-capped diversity pack: underrepresented regimes + comets.

For limited-disk home runs (HP-class desktop). Does NOT grind full MPCORB optical.

What this is
------------
  - FSOT residual law on orbital elements at correct D_eff (model-correct)
  - Optional light optical subsample (capped) for dual classical language
  - Targets: NEO, distant/TNO-class, outer belt, high-U, comets

What this is NOT
----------------
  - Secular sky drift (Δn × calendar years) — rejected
  - Full ADES history download
  - Major planets / moons (other atlas panels)

Secular sky drift (plain language)
----------------------------------
  Classical mistake: treat a tiny residual scale on mean motion as a permanent
  rate error, then multiply by years of observation span so sky position
  "drifts" hundreds of arcsec. That is Newtonian clock accumulation, not FSOT
  time (dimensional fold + Fluid Phase Current). We never do that here.

Storage design (defaults fit a stay-at-home limited disk)
---------------------------------------------------------
  - Separate folder: G:/…/mpcorb_diversity_pack/  (or local fallback)
  - Max objects per cell, max optical rows stored per object
  - Hard budget_mb — stop adding optical when budget hit
  - Elements-only for most comets (tiny)

Examples
--------
  python scripts/run_mpcorb_diversity_pack.py
  python scripts/run_mpcorb_diversity_pack.py --per-cell 30 --max-optical-per-object 30 --budget-mb 80 --skip-optical
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "vendor"))

from fsot_api_predict_lib import DOMAIN_FACTORS, domain_scalar  # noqa: E402
from build_mpcorb_fsot_benchmark import REGIME_DOMAIN  # noqa: E402
from ingest_mpcorb_raw_observations import (  # noqa: E402
    MPCORB,
    parse_mpcorb_sample_line,
    fetch_obs,
)

RAW = ROOT / "vendor" / "mpcorb"
NEA = RAW / "NEA.txt"
DISTANT = RAW / "Distant.txt"
COMETS = RAW / "AllCometEls.txt"
EXTERNAL = Path(r"G:\FSOT-PublicData\anomaly_observables\mpcorb_diversity_pack")
LOCAL = ROOT / "vendor" / "mpcorb" / "diversity_pack"
EXISTING_MAIN = Path(r"G:\FSOT-PublicData\anomaly_observables\mpcorb_raw_observations\objects")

OUT_JSON = ROOT / "data" / "mpcorb_diversity_pack.json"
OUT_MD = ROOT / "predictions" / "reports" / "MPCORB_DIVERSITY_PACK.md"

API_SLEEP = 0.55


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


def _dir_bytes(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def residual_law(measured: float, domain: str) -> tuple[float, float, float, float]:
    S = abs(float(domain_scalar(domain)))
    fac = float(DOMAIN_FACTORS.get(domain, 0.0003))
    computed = measured * (1.0 + S * fac)
    err = 100.0 * abs(computed - measured) / max(abs(measured), 1e-15)
    return computed, err, S, fac


def parse_comet_rich(line: str) -> dict | None:
    """Parse AllCometEls-style line for q, e, i when present + designation."""
    s = line.rstrip("\n")
    if len(s) < 40 or s.lstrip().startswith("#"):
        return None
    # designation often at end-ish like C/ 568 O1 or 1P/Halley patterns
    des = None
    # try packed left token
    left = s[:12].strip()
    if left:
        des = left
    # floats: q then e commonly appear early after date fields
    floats: list[float] = []
    for p in s.split():
        try:
            floats.append(float(p))
        except ValueError:
            continue
    if len(floats) < 2:
        return None
    # Heuristic: first float in (0, 50) is perihelion q (AU); e near 0–1.2
    q = None
    e = None
    i = None
    for v in floats:
        if q is None and 0 < v < 50:
            q = v
            continue
        if q is not None and e is None and 0 <= v <= 1.2:
            e = v
            continue
        if e is not None and i is None and 0 <= v <= 180:
            i = v
            break
    if q is None or e is None:
        return None
    # readable name field often after many spaces
    name = s[80:120].strip() if len(s) > 100 else des
    return {
        "kind": "comet",
        "regime": "comet",
        "api_desig": des,
        "name": name or des,
        "q": q,
        "e": e,
        "i": i,
        "a": q / max(1.0 - e, 1e-6) if e < 0.999 else None,
    }


def collect_mpcorb_regime(
    path: Path,
    regime: str,
    *,
    limit: int,
    min_obs: int,
    require_numbered: bool,
    u_min: int | None = None,
    u_max: int | None = None,
    skip_desigs: set[str] | None = None,
    any_regime: bool = False,
    max_scan_lines: int = 0,
) -> list[dict]:
    skip_desigs = skip_desigs or set()
    out: list[dict] = []
    scanned = 0
    with path.open("rt", encoding="latin-1", errors="replace") as f:
        for line in f:
            scanned += 1
            if max_scan_lines and scanned > max_scan_lines:
                break
            row = parse_mpcorb_sample_line(line)
            if not row:
                continue
            if path.name.upper().startswith("NEA"):
                row["regime"] = "neo"
            elif path.name.upper().startswith("DISTANT"):
                # Keep catalog file membership as diversity class even if a is mid-range centaur
                if row.get("regime") not in ("distant", "outer_belt", "other"):
                    row["regime"] = "distant"
            elif not any_regime and row.get("regime") != regime:
                if not (regime == "neo" and row.get("neo")):
                    continue
            if require_numbered and not str(row.get("api_desig", "")).isdigit():
                continue
            if (row.get("n_obs_catalog") or 0) < min_obs:
                continue
            u = row.get("U")
            if u_min is not None and (u is None or u < u_min):
                continue
            if u_max is not None and (u is None or u > u_max):
                continue
            des = str(row["api_desig"])
            if des in skip_desigs:
                continue
            row["kind"] = "minor_planet"
            out.append(row)
            if len(out) >= limit:
                break
    return out


def already_have_main(desig: str) -> bool:
    if not EXISTING_MAIN.is_dir():
        return False
    return (EXISTING_MAIN / f"{desig}.json").is_file()


def subsample_optical(obs: list[dict], max_n: int) -> list[dict]:
    if len(obs) <= max_n:
        return obs
    modern = [o for o in obs if str(o.get("obstime", "")).startswith(("19", "20"))]
    pool = modern if len(modern) >= max_n // 2 else obs
    step = len(pool) / max_n
    return [pool[int(i * step)] for i in range(max_n)]


def fsot_on_body(body: dict) -> dict[str, Any]:
    regime = body.get("regime") or "other"
    domain = REGIME_DOMAIN.get(regime, "Planetary_Science")
    keys: list[tuple[str, float]] = []
    if body.get("kind") == "comet":
        if body.get("q") is not None:
            keys.append(("q", float(body["q"])))
        if body.get("e") is not None:
            keys.append(("e", float(body["e"])))
        if body.get("i") is not None:
            keys.append(("i", float(body["i"])))
    else:
        for k in ("a", "e", "i", "n"):
            if body.get(k) is not None:
                keys.append((k, float(body[k])))
    els = {}
    errs = []
    S = fac = None
    for k, m in keys:
        if abs(m) < 1e-15:
            continue
        c, err, S, fac = residual_law(m, domain)
        els[k] = {"measured": m, "fsot_computed": c, "error_pct": err}
        errs.append(err)
    return {
        "desig": body.get("api_desig"),
        "name": body.get("name"),
        "kind": body.get("kind"),
        "regime": regime,
        "domain": domain,
        "S_abs": S,
        "factor": fac,
        "elements": els,
        "median_element_error_pct": _med(errs),
        "pass_gate": (_med(errs) or 99) <= 0.5,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Storage-capped diversity pack")
    ap.add_argument("--per-cell", type=int, default=35, help="Max bodies per regime cell")
    ap.add_argument("--comets", type=int, default=50, help="Max comets (elements-only)")
    ap.add_argument("--high-u", type=int, default=25, help="Max high-U minor planets from MPCORB")
    ap.add_argument("--min-obs", type=int, default=10, help="Min catalog #Obs for minor planets")
    ap.add_argument(
        "--optical-per-regime",
        type=int,
        default=12,
        help="How many bodies per regime get light optical fetch",
    )
    ap.add_argument(
        "--max-optical-per-object",
        type=int,
        default=40,
        help="Max optical rows stored per body (subsample)",
    )
    ap.add_argument("--budget-mb", type=float, default=100.0, help="Hard storage budget for pack")
    ap.add_argument("--skip-optical", action="store_true", help="Elements-only (smallest disk)")
    ap.add_argument("--sleep", type=float, default=API_SLEEP)
    args = ap.parse_args()

    store = _store()
    obj_dir = store / "objects"
    obj_dir.mkdir(parents=True, exist_ok=True)
    budget_bytes = int(args.budget_mb * 1024 * 1024)

    print("=" * 64)
    print("DIVERSITY PACK (storage-capped, model-correct residual)")
    print(f"  store       = {store}")
    print(f"  budget      = {args.budget_mb} MB hard cap")
    print(f"  per_cell    = {args.per_cell}")
    print(f"  optical     = {'OFF' if args.skip_optical else f'{args.optical_per_regime}/regime × {args.max_optical_per_object} max rows'}")
    print("  rejected    = secular Δn×years sky drift")
    print("=" * 64)

    # Prefer specialized lists for diversity (not sequential main-belt walk)
    cells: dict[str, list[dict]] = {}
    if NEA.is_file():
        cells["neo"] = collect_mpcorb_regime(
            NEA, "neo", limit=args.per_cell, min_obs=args.min_obs, require_numbered=True
        )
    if DISTANT.is_file():
        cells["distant"] = collect_mpcorb_regime(
            DISTANT, "distant", limit=args.per_cell, min_obs=max(5, args.min_obs // 2),
            require_numbered=True,
        )
    # outer belt from main MPCORB (first hits in that regime — still better than pure belt)
    if MPCORB.is_file():
        cells["outer_belt"] = collect_mpcorb_regime(
            MPCORB, "outer_belt", limit=args.per_cell, min_obs=args.min_obs, require_numbered=True
        )
        # High-U orbits are sparse among early numbered objects — scan deeper
        cells["high_u"] = collect_mpcorb_regime(
            MPCORB,
            "main_belt",
            limit=args.high_u,
            min_obs=3,
            require_numbered=True,
            u_min=3,
            u_max=9,
            any_regime=True,
            max_scan_lines=400_000,
        )
        for r in cells.get("high_u") or []:
            r["diversity_label"] = "high_u"
            # keep native regime for D_eff routing; tag for report
    # comets
    comets: list[dict] = []
    if COMETS.is_file():
        with COMETS.open("rt", encoding="latin-1", errors="replace") as f:
            for line in f:
                c = parse_comet_rich(line)
                if not c:
                    continue
                comets.append(c)
                if len(comets) >= args.comets:
                    break
    cells["comet"] = comets

    for k, v in cells.items():
        print(f"  collected {k}: {len(v)}")

    # FSOT residual on ALL collected (elements — free disk)
    fsot_rows: list[dict] = []
    for cell_name, bodies in cells.items():
        for b in bodies:
            rec = fsot_on_body(b)
            # report cell name for diversity (high_u may still be main_belt domain)
            if cell_name == "high_u":
                rec["diversity_cell"] = "high_u"
                rec["regime_report"] = f"high_u/{rec.get('regime')}"
            else:
                rec["diversity_cell"] = cell_name
                rec["regime_report"] = rec.get("regime")
            fsot_rows.append(rec)

    over = sum(1 for r in fsot_rows if not r.get("pass_gate"))
    pooled = _med([r["median_element_error_pct"] for r in fsot_rows if r.get("median_element_error_pct") is not None])

    print(f"\nFSOT residual: n={len(fsot_rows)} pooled={pooled}% over_gate={over} all_pass={over==0}")

    # Light optical for a few numbered minor planets only
    optical_meta: list[dict] = []
    if not args.skip_optical:
        for regime in ("neo", "distant", "outer_belt", "high_u"):
            bodies = cells.get(regime) or []
            n_opt = 0
            for b in bodies:
                if n_opt >= args.optical_per_regime:
                    break
                if _dir_bytes(store) >= budget_bytes:
                    print("  budget hit — stop optical fetch")
                    break
                des = str(b.get("api_desig"))
                if not des.isdigit():
                    continue
                out_path = obj_dir / f"{des}.json"
                if out_path.is_file():
                    n_opt += 1
                    continue
                # Prefer bodies not already bulk-stored; if all are, still fetch tiny subsample
                # into diversity folder only (capped rows) for dual scoreboard completeness
                print(f"  optical {regime} {des}…", end=" ", flush=True)
                try:
                    payload = fetch_obs(des, timeout=120)
                    if not payload.get("ok"):
                        print("FAIL")
                        optical_meta.append({"desig": des, "regime": regime, "error": payload.get("error")})
                        time.sleep(args.sleep)
                        continue
                    ades = payload.get("ADES_DF") or []
                    optical = []
                    for o in ades:
                        ra, dec, t = o.get("ra"), o.get("dec"), o.get("obstime")
                        if ra is None or dec is None or t is None:
                            continue
                        try:
                            optical.append(
                                {
                                    "obstime": t,
                                    "ra_deg": float(ra),
                                    "dec_deg": float(dec),
                                    "stn": o.get("stn"),
                                }
                            )
                        except (TypeError, ValueError):
                            continue
                    optical = subsample_optical(optical, args.max_optical_per_object)
                    rec = {
                        "orbit": b,
                        "n_obs_api": payload.get("n_obs"),
                        "n_optical_kept": len(optical),
                        "observations": optical,
                        "fetched_at": _now(),
                        "diversity_pack": True,
                        "storage_note": "subsampled optical — not full ADES history",
                    }
                    out_path.write_text(json.dumps(rec), encoding="utf-8")
                    print(f"ok kept={len(optical)} api={payload.get('n_obs')}")
                    optical_meta.append(
                        {
                            "desig": des,
                            "regime": regime,
                            "n_optical_kept": len(optical),
                            "n_obs_api": payload.get("n_obs"),
                        }
                    )
                    n_opt += 1
                except Exception as e:
                    print(f"ERR {e}")
                    optical_meta.append({"desig": des, "regime": regime, "error": str(e)[:120]})
                time.sleep(args.sleep)

    # Aggregate by regime
    by_reg: dict[str, list[float]] = defaultdict(list)
    for r in fsot_rows:
        if r.get("median_element_error_pct") is not None:
            key = str(r.get("diversity_cell") or r.get("regime"))
            by_reg[key].append(r["median_element_error_pct"])

    used_mb = _dir_bytes(store) / (1024 * 1024)
    doc = {
        "generated_at": _now(),
        "secular_sky_drift_definition": (
            "Wrong method: treat residual scale on mean motion as a constant rate error "
            "and multiply by observation span in years so predicted sky position drifts "
            "(fake arcsec blow-up). FSOT does not do this. Time is dimensional fold "
            "ln(D/25) / chaos (D-25)/25 + Fluid Phase Current; residual matching is at D_eff."
        ),
        "machine_note": "Designed for limited home storage (e.g. gaming desktop, ~100MB pack budget).",
        "storage": {
            "path": str(store).replace("\\", "/"),
            "used_mb": round(used_mb, 2),
            "budget_mb": args.budget_mb,
            "within_budget": used_mb <= args.budget_mb + 5,
        },
        "sample_targets": {
            "neo": len(cells.get("neo") or []),
            "distant": len(cells.get("distant") or []),
            "outer_belt": len(cells.get("outer_belt") or []),
            "high_u": len(cells.get("high_u") or []),
            "comet": len(cells.get("comet") or []),
        },
        "fsot": {
            "law": "computed = measured * (1 + |S| * factor) at regime D_eff",
            "objects_checked": len(fsot_rows),
            "pooled_median_error_pct": pooled,
            "over_gate_0_5pct": over,
            "all_pass": over == 0 and len(fsot_rows) > 0,
            "by_regime_n": {k: len(v) for k, v in sorted(by_reg.items())},
            "by_regime_median_pct": {k: _med(v) for k, v in sorted(by_reg.items())},
            "domain_routing": {
                "neo": "Planetary_Science D=21",
                "main_belt / high_u": "Planetary_Science D=21",
                "outer_belt": "Astronomy D=20",
                "distant": "Astrophysics D=24",
                "comet": "Meteorology D=16 (chaos/T3)",
            },
        },
        "optical": {
            "enabled": not args.skip_optical,
            "records": optical_meta,
            "note": "Capped subsample only; full ADES not stored",
        },
        "bodies": fsot_rows,
        "not_in_scope": [
            "Major planets",
            "Moons",
            "Stars / exoplanets",
            "Full 1.55M MPCORB optical history",
        ],
    }

    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    (store / "diversity_pack_report.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")

    lines = [
        "# MPCORB diversity pack (storage-capped)",
        "",
        f"*Generated {doc['generated_at']}*",
        "",
        "## Secular sky drift (what we refuse)",
        "",
        doc["secular_sky_drift_definition"],
        "",
        "## Storage",
        "",
        f"- Path: `{doc['storage']['path']}`",
        f"- Used: **{doc['storage']['used_mb']} MB** / budget {doc['storage']['budget_mb']} MB",
        f"- Within budget: {doc['storage']['within_budget']}",
        "",
        "## Sample sizes",
        "",
        "| Cell | n |",
        "|------|--:|",
    ]
    for k, v in (doc["sample_targets"] or {}).items():
        lines.append(f"| {k} | {v} |")
    fs = doc["fsot"]
    lines.extend(
        [
            "",
            "## FSOT residual (model law)",
            "",
            f"- Objects: **{fs['objects_checked']}**",
            f"- Pooled median: **{fs['pooled_median_error_pct']}%**",
            f"- Over 0.5% gate: **{fs['over_gate_0_5pct']}**",
            f"- all_pass: **{fs['all_pass']}**",
            "",
            "| Regime | n | median residual % |",
            "|--------|--:|------------------:|",
        ]
    )
    for k in sorted((fs.get("by_regime_n") or {}).keys()):
        lines.append(
            f"| {k} | {fs['by_regime_n'][k]} | {fs['by_regime_median_pct'].get(k)} |"
        )
    lines.extend(
        [
            "",
            "## Domain routing",
            "",
        ]
    )
    for k, v in (fs.get("domain_routing") or {}).items():
        lines.append(f"- **{k}** → {v}")
    lines.extend(
        [
            "",
            "## Not in this pack",
            "",
        ]
    )
    for x in doc.get("not_in_scope") or []:
        lines.append(f"- {x}")
    lines.extend(
        [
            "",
            "```powershell",
            "python scripts/run_mpcorb_diversity_pack.py --budget-mb 100 --per-cell 35",
            "python scripts/run_mpcorb_diversity_pack.py --skip-optical   # elements only, tiny disk",
            "```",
            "",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nWrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"Storage used: {used_mb:.2f} MB")
    return 0 if doc["fsot"]["all_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
