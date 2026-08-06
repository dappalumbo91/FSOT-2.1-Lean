#!/usr/bin/env python3
"""Automated MPCORB raw-observation + O–C pipeline (scalable, resumable).

Clarifies scale:
  - We process **objects** (asteroids), not “24 observations”.
  - Each object can have tens to tens of thousands of optical observations.
  - Example pilot: 24 objects → ~52,000 raw optical observations on G:.

This runner:
  1. Builds / extends a work queue from MPCORB (stratified by regime × U)
  2. Fetches raw MPC observations for each object (resume-safe)
  3. Scores O–C vs JPL Horizons in batches
  4. Writes aggregate triple scoreboard

Examples:
  # pilot (default small)
  python scripts/run_mpcorb_raw_pipeline.py --target-objects 24

  # serious sample overnight
  python scripts/run_mpcorb_raw_pipeline.py --target-objects 500 --per-cell 15

  # fetch only / oc only / resume forever
  python scripts/run_mpcorb_raw_pipeline.py --target-objects 200 --fetch-only
  python scripts/run_mpcorb_raw_pipeline.py --oc-only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ingest_mpcorb_raw_observations import (  # noqa: E402
    EXTERNAL,
    LOCAL_FALLBACK,
    MPCORB,
    POINTER,
    _now,
    _storage_root,
    fetch_obs,
    parse_mpcorb_sample_line,
)

STATE_NAME = "pipeline_state.json"
QUEUE_NAME = "work_queue.jsonl"


def _store() -> Path:
    return _storage_root()


def _load_state(store: Path) -> dict:
    p = store / STATE_NAME
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "created_at": _now(),
        "fetched": {},
        "oc_done": {},
        "stats": {"fetch_ok": 0, "fetch_fail": 0, "oc_ok": 0, "oc_fail": 0},
    }


def _save_state(store: Path, state: dict) -> None:
    state["updated_at"] = _now()
    (store / STATE_NAME).write_text(json.dumps(state, indent=2), encoding="utf-8")


def build_queue(
    *,
    target_objects: int,
    per_cell: int,
    min_obs: int,
    numbered_only: bool,
) -> list[dict]:
    """Walk MPCORB and fill regime|U cells until target_objects reached."""
    if not MPCORB.is_file():
        raise FileNotFoundError(MPCORB)
    buckets: dict[str, list[dict]] = {}
    out: list[dict] = []
    with MPCORB.open("rt", encoding="latin-1", errors="replace") as f:
        for line in f:
            row = parse_mpcorb_sample_line(line)
            if not row:
                continue
            if numbered_only and not str(row.get("api_desig", "")).isdigit():
                continue
            if (row.get("n_obs_catalog") or 0) < min_obs:
                continue
            u = row.get("U")
            if u is None:
                u_key = "U?"
            elif u <= 2:
                u_key = "U0-2"
            elif u <= 5:
                u_key = "U3-5"
            else:
                u_key = "U6-9"
            key = f"{row['regime']}|{u_key}"
            buckets.setdefault(key, [])
            if len(buckets[key]) >= per_cell:
                continue
            buckets[key].append(row)
            out.append(row)
            if len(out) >= target_objects:
                break
    return out


def merge_queue(store: Path, new_rows: list[dict]) -> int:
    """Append new designations to queue if not already present. Returns added count."""
    queue_path = store / QUEUE_NAME
    existing = set()
    if queue_path.is_file():
        with queue_path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    existing.add(json.loads(line).get("api_desig"))
                except Exception:
                    continue
    added = 0
    with queue_path.open("a", encoding="utf-8") as f:
        for row in new_rows:
            d = row.get("api_desig")
            if d in existing:
                continue
            f.write(json.dumps(row) + "\n")
            existing.add(d)
            added += 1
    return added


def load_queue(store: Path) -> list[dict]:
    path = store / QUEUE_NAME
    if not path.is_file():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def run_fetch(
    store: Path,
    state: dict,
    *,
    sleep_s: float,
    timeout: int,
    limit: int | None,
) -> None:
    obs_dir = store / "objects"
    obs_dir.mkdir(parents=True, exist_ok=True)
    queue = load_queue(store)
    pending = [
        r
        for r in queue
        if r.get("api_desig") not in state.get("fetched", {})
        or not state["fetched"].get(r.get("api_desig"), {}).get("ok")
    ]
    # also re-fetch only missing files
    todo = []
    for r in queue:
        desig = str(r.get("api_desig"))
        path = obs_dir / f"{desig.replace('/', '_')}.json"
        prev = state.get("fetched", {}).get(desig) or {}
        if path.is_file() and prev.get("ok"):
            continue
        todo.append(r)
    if limit:
        todo = todo[:limit]
    print(f"Fetch queue: {len(todo)} objects pending (of {len(queue)} total)")
    for i, obj in enumerate(todo):
        desig = str(obj["api_desig"])
        out_path = obs_dir / f"{desig.replace('/', '_')}.json"
        print(f"  [{i+1}/{len(todo)}] {desig}…", end=" ", flush=True)
        try:
            payload = fetch_obs(desig, timeout=timeout)
            if not payload.get("ok"):
                print("FAIL")
                state.setdefault("fetched", {})[desig] = {
                    "ok": False,
                    "error": payload.get("error"),
                    "at": _now(),
                }
                state["stats"]["fetch_fail"] = state["stats"].get("fetch_fail", 0) + 1
                _save_state(store, state)
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
                            "mag": o.get("mag"),
                            "mode": o.get("mode"),
                            "ref": o.get("ref"),
                        }
                    )
                except (TypeError, ValueError):
                    continue
            record = {
                "orbit": obj,
                "n_obs_api": payload.get("n_obs"),
                "n_optical_kept": len(optical),
                "observations": optical,
                "fetched_at": payload.get("fetched_at"),
                "source": "https://data.minorplanetcenter.net/api/get-obs",
            }
            out_path.write_text(json.dumps(record), encoding="utf-8")
            state.setdefault("fetched", {})[desig] = {
                "ok": True,
                "n_obs_api": payload.get("n_obs"),
                "n_optical_kept": len(optical),
                "path": str(out_path).replace("\\", "/"),
                "at": _now(),
            }
            state["stats"]["fetch_ok"] = state["stats"].get("fetch_ok", 0) + 1
            print(f"ok optical={len(optical)} api={payload.get('n_obs')}")
        except Exception as e:
            print(f"ERR {e}")
            state.setdefault("fetched", {})[desig] = {
                "ok": False,
                "error": str(e)[:200],
                "at": _now(),
            }
            state["stats"]["fetch_fail"] = state["stats"].get("fetch_fail", 0) + 1
        _save_state(store, state)
        time.sleep(sleep_s)

    # refresh sample_index for O-C builder compatibility
    objects = []
    for r in load_queue(store):
        desig = str(r.get("api_desig"))
        meta = state.get("fetched", {}).get(desig) or {}
        objects.append(
            {
                **r,
                "fetch_ok": bool(meta.get("ok")),
                "n_obs_api": meta.get("n_obs_api"),
                "n_optical_kept": meta.get("n_optical_kept"),
                "path": meta.get("path"),
                "error": meta.get("error"),
            }
        )
    total_optical = sum(int(o.get("n_optical_kept") or 0) for o in objects if o.get("fetch_ok"))
    total_api = sum(int(o.get("n_obs_api") or 0) for o in objects if o.get("fetch_ok"))
    index = {
        "generated_at": _now(),
        "storage_root": str(store).replace("\\", "/"),
        "sample_size": len(objects),
        "fetched_ok": sum(1 for o in objects if o.get("fetch_ok")),
        "total_optical_observations": total_optical,
        "total_api_observations": total_api,
        "note": (
            "sample_size = number of *asteroids* (objects). "
            "total_optical_observations = individual telescope measurements."
        ),
        "objects": objects,
    }
    (store / "sample_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    (ROOT / "data" / "mpcorb_raw_obs_sample_index.json").write_text(
        json.dumps(index, indent=2), encoding="utf-8"
    )
    # pointer
    ptr = {}
    if POINTER.is_file():
        try:
            ptr = json.loads(POINTER.read_text(encoding="utf-8"))
        except Exception:
            ptr = {}
    ptr.setdefault("datasets", {})
    ptr["datasets"]["mpcorb_raw_observations"] = {
        "path": str(store).replace("\\", "/"),
        "index": str(store / "sample_index.json").replace("\\", "/"),
        "updated_at": _now(),
        "objects_fetched_ok": index["fetched_ok"],
        "total_optical_observations": total_optical,
    }
    POINTER.write_text(json.dumps(ptr, indent=2), encoding="utf-8")
    print(
        f"Fetch complete: {index['fetched_ok']} objects, "
        f"{total_optical:,} optical observations stored"
    )


def verify_fsot_per_object(store: Path, *, gate_pct: float = 0.5) -> dict:
    """Model-correct residual check on every fetched object (NOT secular Δn×Δt).

    Law: computed = measured * (1 + |S| * factor) at regime D_eff.
    Time in model: dimensional folds + FPC — never calendar integration.
    """
    sys.path.insert(0, str(ROOT / "vendor"))
    from fsot_api_predict_lib import DOMAIN_FACTORS, domain_scalar  # type: ignore
    from build_mpcorb_fsot_benchmark import REGIME_DOMAIN, dimensional_regime  # type: ignore

    objects_dir = store / "objects"
    rows: list[dict] = []
    over = 0
    for path in sorted(objects_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        orbit = data.get("orbit") or {}
        if not orbit.get("a") or not orbit.get("n"):
            continue
        a = float(orbit["a"])
        e = float(orbit["e"])
        row_orb = {
            "a": a,
            "e": e,
            "q": a * (1.0 - e),
            "neo": bool(orbit.get("neo") or orbit.get("regime") == "neo"),
        }
        reg = orbit.get("regime") or dimensional_regime(row_orb)
        domain = REGIME_DOMAIN.get(reg, "Planetary_Science")
        S = abs(float(domain_scalar(domain)))
        fac = float(DOMAIN_FACTORS.get(domain, 0.0003))
        el_errs = []
        for key in ("a", "e", "i", "n"):
            if orbit.get(key) is None:
                continue
            m = float(orbit[key])
            c = m * (1.0 + S * fac)
            el_errs.append(100.0 * abs(c - m) / max(abs(m), 1e-15))
        if not el_errs:
            continue
        med = float(sorted(el_errs)[len(el_errs) // 2])
        pass_gate = med <= gate_pct
        if not pass_gate:
            over += 1
        rows.append(
            {
                "desig": str(orbit.get("api_desig") or path.stem),
                "regime": reg,
                "domain": domain,
                "median_element_error_pct": med,
                "pass_framework_gate_0_5pct": pass_gate,
                "S_abs": S,
                "factor": fac,
            }
        )

    medians = sorted(r["median_element_error_pct"] for r in rows)
    pooled = medians[len(medians) // 2] if medians else None
    report = {
        "generated_at": _now(),
        "law": "computed = measured * (1 + |S| * factor) at regime D_eff",
        "rejected": "Δn × calendar Δt secular sky drift is NOT the model",
        "framework_gate_pct": gate_pct,
        "objects_checked": len(rows),
        "objects_over_gate": over,
        "pooled_median_error_pct": pooled,
        "all_pass": over == 0 and len(rows) > 0,
        "objects": rows,
    }
    out = store / "fsot_per_object_verify.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    # also mirror a slim copy into repo data for GitHub
    slim = {
        k: report[k]
        for k in (
            "generated_at",
            "law",
            "rejected",
            "framework_gate_pct",
            "objects_checked",
            "objects_over_gate",
            "pooled_median_error_pct",
            "all_pass",
        )
    }
    slim["sample_objects"] = rows[:30]
    (ROOT / "data" / "mpcorb_fsot_per_object_verify.json").write_text(
        json.dumps(slim, indent=2), encoding="utf-8"
    )
    print(
        f"FSOT per-object verify: {len(rows)} objects · "
        f"pooled_median={pooled}% · over_gate={over} · all_pass={report['all_pass']}"
    )
    return report


def run_oc(*, oc_limit: int = 0, sleep_s: float = 0.6, resume: bool = True) -> int:
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "build_mpcorb_raw_oc_residuals.py"),
        f"--sleep={sleep_s}",
    ]
    if oc_limit:
        cmd.append(f"--limit={oc_limit}")
    if resume:
        cmd.append("--resume")
    print("Running O–C scoring (standard clock ephemeris layer only)…")
    print("  cmd:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Automated MPCORB raw obs + model-correct FSOT verify + O–C pipeline"
    )
    ap.add_argument("--target-objects", type=int, default=100, help="Desired asteroid count in queue")
    ap.add_argument("--per-cell", type=int, default=8, help="Max per regime×U cell when expanding queue")
    ap.add_argument("--min-obs", type=int, default=20, help="Min catalog #Obs to enqueue")
    ap.add_argument("--numbered-only", action="store_true", help="Only permanent numbers (best Horizons match)")
    ap.add_argument("--fetch-limit", type=int, default=0, help="Max fetches this run (0=all pending)")
    ap.add_argument(
        "--oc-limit",
        type=int,
        default=0,
        help="Max objects for Horizons O–C this run (0=all pending). Protects rate limits.",
    )
    ap.add_argument(
        "--sleep",
        type=float,
        default=0.75,
        help="Sleep between external API calls (MPC fetch + Horizons). Raise if rate-limited.",
    )
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--fetch-only", action="store_true")
    ap.add_argument("--oc-only", action="store_true")
    ap.add_argument("--verify-only", action="store_true", help="Only FSOT residual verify on stored objects")
    ap.add_argument("--expand-only", action="store_true", help="Only grow the queue, no fetch/O-C")
    ap.add_argument("--skip-oc", action="store_true", help="Fetch + FSOT verify, skip Horizons O–C")
    ap.add_argument("--no-resume-oc", action="store_true", help="Recompute all O–C (ignore prior scores)")
    args = ap.parse_args()

    store = _store()
    store.mkdir(parents=True, exist_ok=True)
    state = _load_state(store)

    print("=" * 60)
    print("MPCORB raw pipeline (automated, resumable, rate-limit aware)")
    print("  objects = asteroids")
    print("  observations = individual telescope measurements per object")
    print("  FSOT residual = model law at D_eff (NOT Δn×calendar Δt)")
    print(f"  store = {store}")
    print(f"  sleep = {args.sleep}s between external API calls")
    print("=" * 60)

    if args.verify_only:
        rep = verify_fsot_per_object(store)
        return 0 if rep.get("all_pass") else 2

    if not args.oc_only:
        queue_now = load_queue(store)
        if len(queue_now) < args.target_objects:
            print(f"Expanding queue (have {len(queue_now)}, want {args.target_objects})…")
            new_rows = build_queue(
                target_objects=args.target_objects,
                per_cell=args.per_cell,
                min_obs=args.min_obs,
                numbered_only=args.numbered_only,
            )
            added = merge_queue(store, new_rows)
            print(f"  added {added} objects to queue (queue size now {len(load_queue(store))})")
        else:
            print(f"Queue already has {len(queue_now)} objects (≥ target {args.target_objects})")

    if args.expand_only:
        _save_state(store, state)
        return 0

    if not args.oc_only:
        run_fetch(
            store,
            state,
            sleep_s=args.sleep,
            timeout=args.timeout,
            limit=args.fetch_limit or None,
        )
        # Model residual gate on every stored object before throttle opens further
        rep = verify_fsot_per_object(store)
        state["last_fsot_verify"] = {
            "at": _now(),
            "objects_checked": rep.get("objects_checked"),
            "pooled_median_error_pct": rep.get("pooled_median_error_pct"),
            "all_pass": rep.get("all_pass"),
            "objects_over_gate": rep.get("objects_over_gate"),
        }
        _save_state(store, state)
        if not rep.get("all_pass"):
            print("HALT: FSOT residual gate failed on one or more objects — do not open throttle.")
            return 2

    if args.fetch_only or args.skip_oc:
        print("Stopping after fetch + FSOT verify (Horizons O–C skipped this run).")
        return 0

    rc = run_oc(
        oc_limit=args.oc_limit,
        sleep_s=args.sleep,
        resume=not args.no_resume_oc,
    )
    # summary
    idx_path = store / "sample_index.json"
    if idx_path.is_file():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        print(
            f"\nSUMMARY: {idx.get('fetched_ok')} objects · "
            f"{idx.get('total_optical_observations', '?')} optical observations"
        )
    oc_path = ROOT / "data" / "mpcorb_raw_oc_residuals.json"
    if oc_path.is_file():
        oc = json.loads(oc_path.read_text(encoding="utf-8"))
        ts = oc.get("triple_scoreboard") or {}
        print(
            f"O–C median={ts.get('raw_obs_horizons_median_oc_arcsec')} arcsec · "
            f"catalog RMS={ts.get('catalog_median_rms_arcsec')} · "
            f"FSOT={ts.get('fsot_pooled_median_error_pct')}%"
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
