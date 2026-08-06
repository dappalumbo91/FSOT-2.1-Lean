#!/usr/bin/env python3
"""MPCORB baseline epoch run — ~30–60 min autonomous local training-style loop.

Like LLM epochs: each epoch = expand queue → fetch batch → FSOT residual verify
→ limited Horizons O–C → checkpoint. Soft wall-clock stop so we get a solid
baseline before a full multi-hour/day run.

Does **not** push to GitHub. Write results locally; push only when you ask.

Model discipline (do not regress):
  - FSOT residual = computed = measured*(1+|S|*factor) at regime D_eff
  - NOT secular Δn × calendar years
  - Fail residual gate → halt before more throttle

Examples:
  # default ~45–50 min baseline (4 epochs × open throttle)
  python scripts/run_mpcorb_epoch_baseline.py

  # shorter smoke (~20 min)
  python scripts/run_mpcorb_epoch_baseline.py --max-minutes 20 --epochs 2 --fetch-per-epoch 40 --oc-per-epoch 15

  # stop gracefully: create the stop file
  #   G:/FSOT-PublicData/anomaly_observables/mpcorb_raw_observations/STOP_EPOCHS
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_mpcorb_raw_pipeline import (  # noqa: E402
    _load_state,
    _save_state,
    _store,
    expand_queue_sequential,
    load_queue,
    run_fetch,
    run_oc,
    verify_fsot_per_object,
)

STOP_NAME = "STOP_EPOCHS"
EPOCH_LOG = "epoch_log.jsonl"
EPOCH_STATUS = "epoch_status.json"
EPOCH_REPORT = "epoch_baseline_report.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_status(store: Path, doc: dict) -> None:
    (store / EPOCH_STATUS).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    # slim mirror for repo (not auto-committed)
    slim_path = ROOT / "data" / "mpcorb_epoch_status.json"
    slim_path.parent.mkdir(parents=True, exist_ok=True)
    slim_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def _append_log(store: Path, row: dict) -> None:
    with (store / EPOCH_LOG).open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def _stop_requested(store: Path) -> bool:
    return (store / STOP_NAME).is_file()


def _elapsed_min(t0: float) -> float:
    return (time.time() - t0) / 60.0


def main() -> int:
    ap = argparse.ArgumentParser(description="MPCORB baseline epoch runner (~30–60 min)")
    ap.add_argument("--epochs", type=int, default=4, help="Max epochs this baseline run")
    ap.add_argument(
        "--max-minutes",
        type=float,
        default=50.0,
        help="Soft wall-clock budget in minutes (default 50 ≈ half hour to hour)",
    )
    ap.add_argument("--fetch-per-epoch", type=int, default=60, help="MPC fetch cap per epoch")
    ap.add_argument("--oc-per-epoch", type=int, default=25, help="New Horizons O–C cap per epoch")
    ap.add_argument(
        "--queue-add-per-epoch",
        type=int,
        default=80,
        help="Grow queue by this many NEW objects each epoch (sequential catalog walk)",
    )
    ap.add_argument("--min-obs", type=int, default=15, help="Min catalog #Obs to enqueue")
    ap.add_argument("--sleep", type=float, default=0.55, help="API sleep seconds (rate-limit cushion)")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--numbered-only", action="store_true", default=True)
    ap.add_argument("--allow-provisional", action="store_true", help="Include non-numbered desigs")
    ap.add_argument("--skip-oc", action="store_true", help="Fetch + FSOT only (faster baseline)")
    args = ap.parse_args()

    numbered_only = not args.allow_provisional
    store = _store()
    store.mkdir(parents=True, exist_ok=True)
    state = _load_state(store)
    catalog_line = int(state.get("catalog_walk_line") or 0)
    t0 = time.time()

    print("=" * 64)
    print("MPCORB BASELINE EPOCH RUN (local, no git push)")
    print(f"  store          = {store}")
    print(f"  epochs         = {args.epochs}")
    print(f"  max_minutes    = {args.max_minutes}")
    print(f"  fetch/epoch    = {args.fetch_per_epoch}")
    print(f"  oc/epoch       = {args.oc_per_epoch}")
    print(f"  queue_add/ep   = {args.queue_add_per_epoch} (sequential walk)")
    print(f"  catalog_line   = {catalog_line}")
    print(f"  sleep          = {args.sleep}s")
    print(f"  stop file      = {store / STOP_NAME}")
    print("  FSOT law       = residual at D_eff (NOT Δn×calendar Δt)")
    print("=" * 64)

    run_meta = {
        "started_at": _now(),
        "mode": "baseline_epochs",
        "budget_minutes": args.max_minutes,
        "epochs_planned": args.epochs,
        "fetch_per_epoch": args.fetch_per_epoch,
        "oc_per_epoch": args.oc_per_epoch,
        "sleep_s": args.sleep,
        "epochs_completed": 0,
        "halted": None,
        "epochs": [],
    }
    _write_status(
        store,
        {
            "phase": "starting",
            "run": run_meta,
            "elapsed_min": 0.0,
            "message": "baseline epoch run started",
            "updated_at": _now(),
        },
    )

    final_verify = None
    rc = 0

    try:
        for ep in range(1, args.epochs + 1):
            if _stop_requested(store):
                run_meta["halted"] = "stop_file"
                print(f"\n[epoch {ep}] STOP file present — graceful halt.")
                break
            if _elapsed_min(t0) >= args.max_minutes:
                run_meta["halted"] = "max_minutes"
                print(f"\n[epoch {ep}] Hit max_minutes={args.max_minutes} — soft stop.")
                break

            ep_t0 = time.time()
            print(f"\n{'─'*64}\nEPOCH {ep}/{args.epochs}  elapsed={_elapsed_min(t0):.1f} min\n{'─'*64}")
            _write_status(
                store,
                {
                    "phase": f"epoch_{ep}",
                    "run": run_meta,
                    "elapsed_min": round(_elapsed_min(t0), 2),
                    "message": f"running epoch {ep}",
                    "updated_at": _now(),
                },
            )

            # 1) Expand queue via sequential catalog walk (can cover full dataset)
            q = load_queue(store)
            print(
                f"  expand queue (sequential): have {len(q)} · "
                f"add up to {args.queue_add_per_epoch} · catalog_line={catalog_line}"
            )
            exp = expand_queue_sequential(
                store,
                max_add=args.queue_add_per_epoch,
                min_obs=args.min_obs,
                numbered_only=numbered_only,
                start_line=catalog_line,
            )
            catalog_line = int(exp.get("new_start_line") or catalog_line)
            state = _load_state(store)
            state["catalog_walk_line"] = catalog_line
            state["last_queue_expand"] = exp
            _save_state(store, state)
            added = int(exp.get("added") or 0)
            q_after = len(load_queue(store))
            print(
                f"  queue added {added} (size now {q_after}) · "
                f"scanned={exp.get('scanned')} · next_line={catalog_line} · "
                f"exhausted={exp.get('catalog_exhausted')}"
            )
            if exp.get("catalog_exhausted") and added == 0:
                print("  catalog walk exhausted — no more objects to enqueue under filters")

            # 2) Fetch batch
            state = _load_state(store)
            run_fetch(
                store,
                state,
                sleep_s=args.sleep,
                timeout=args.timeout,
                limit=args.fetch_per_epoch,
            )

            # 3) FSOT residual verify (model gate — halt if bad)
            verify = verify_fsot_per_object(store)
            final_verify = verify
            if not verify.get("all_pass"):
                run_meta["halted"] = "fsot_gate_fail"
                print("  HALT: FSOT residual gate failed — fix before full run.")
                rc = 2
                ep_row = {
                    "epoch": ep,
                    "at": _now(),
                    "elapsed_min": round(_elapsed_min(t0), 2),
                    "epoch_min": round((time.time() - ep_t0) / 60.0, 2),
                    "queue_size": q_after,
                    "queue_added": added,
                    "fsot": {
                        "objects_checked": verify.get("objects_checked"),
                        "pooled_median_error_pct": verify.get("pooled_median_error_pct"),
                        "all_pass": False,
                        "objects_over_gate": verify.get("objects_over_gate"),
                    },
                    "oc_ran": False,
                    "halted": "fsot_gate_fail",
                }
                run_meta["epochs"].append(ep_row)
                _append_log(store, ep_row)
                break

            # 4) Horizons O–C (standard clock layer; rate-limited)
            oc_rc = 0
            if not args.skip_oc:
                # leave a few minutes of budget for last O–C if near wall
                remaining = args.max_minutes - _elapsed_min(t0)
                if remaining < 2.0:
                    print("  skip O–C this epoch — under 2 min budget remaining")
                else:
                    oc_rc = run_oc(
                        oc_limit=args.oc_per_epoch,
                        sleep_s=args.sleep,
                        resume=True,
                    )

            ep_row = {
                "epoch": ep,
                "at": _now(),
                "elapsed_min": round(_elapsed_min(t0), 2),
                "epoch_min": round((time.time() - ep_t0) / 60.0, 2),
                "queue_size": q_after,
                "queue_added": added,
                "catalog_walk_line": catalog_line,
                "queue_expand": exp,
                "fsot": {
                    "objects_checked": verify.get("objects_checked"),
                    "pooled_median_error_pct": verify.get("pooled_median_error_pct"),
                    "all_pass": verify.get("all_pass"),
                    "objects_over_gate": verify.get("objects_over_gate"),
                },
                "oc_ran": not args.skip_oc,
                "oc_rc": oc_rc,
            }
            run_meta["epochs"].append(ep_row)
            run_meta["epochs_completed"] = ep
            _append_log(store, ep_row)
            print(
                f"  epoch {ep} done in {ep_row['epoch_min']:.1f} min · "
                f"FSOT n={verify.get('objects_checked')} "
                f"pooled={verify.get('pooled_median_error_pct')}% all_pass={verify.get('all_pass')}"
            )

            state = _load_state(store)
            state["last_epoch"] = ep_row
            _save_state(store, state)

            if _elapsed_min(t0) >= args.max_minutes:
                run_meta["halted"] = "max_minutes"
                print("  Soft stop after epoch (max_minutes).")
                break

    except KeyboardInterrupt:
        run_meta["halted"] = "keyboard_interrupt"
        print("\nInterrupted — checkpoint already on disk.")
        rc = 130
    except Exception as e:
        run_meta["halted"] = f"error:{e}"
        print(f"\nERROR: {e}")
        traceback.print_exc()
        rc = 1

    # Final summary
    store = _store()
    state = _load_state(store)
    idx = {}
    idx_path = store / "sample_index.json"
    if idx_path.is_file():
        try:
            idx = json.loads(idx_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    oc_summary = {}
    oc_path = ROOT / "data" / "mpcorb_raw_oc_residuals.json"
    if oc_path.is_file():
        try:
            oc = json.loads(oc_path.read_text(encoding="utf-8"))
            oc_summary = {
                "objects_with_oc": (oc.get("sample") or {}).get("objects_with_oc"),
                "median_oc_arcsec": (oc.get("raw_oc_summary_arcsec") or {}).get(
                    "median_of_object_medians"
                ),
                "fsot_pooled_from_scoreboard": (oc.get("triple_scoreboard") or {}).get(
                    "fsot_pooled_median_error_pct"
                ),
            }
        except Exception:
            pass

    run_meta["finished_at"] = _now()
    run_meta["elapsed_min"] = round(_elapsed_min(t0), 2)
    if run_meta.get("halted") is None:
        run_meta["halted"] = "completed_all_epochs"

    report = {
        "generated_at": _now(),
        "run": run_meta,
        "final_index": {
            "fetched_ok": idx.get("fetched_ok"),
            "sample_size": idx.get("sample_size"),
            "total_optical_observations": idx.get("total_optical_observations"),
            "queue_size": len(load_queue(store)),
        },
        "final_fsot_verify": {
            "objects_checked": (final_verify or {}).get("objects_checked"),
            "pooled_median_error_pct": (final_verify or {}).get("pooled_median_error_pct"),
            "all_pass": (final_verify or {}).get("all_pass"),
            "objects_over_gate": (final_verify or {}).get("objects_over_gate"),
        },
        "final_oc": oc_summary,
        "push_when_ready": (
            "Do not auto-push. When baseline looks good, ask to commit/push: "
            "data/mpcorb_* epoch status, O–C, verify, sample index, reports."
        ),
        "next_full_run_hint": (
            "python scripts/run_mpcorb_epoch_baseline.py "
            "--max-minutes 720 --epochs 40 --fetch-per-epoch 80 --oc-per-epoch 30 --sleep 0.55"
        ),
    }
    (store / EPOCH_REPORT).write_text(json.dumps(report, indent=2), encoding="utf-8")
    (ROOT / "data" / "mpcorb_epoch_baseline_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    _write_status(
        store,
        {
            "phase": "finished",
            "run": run_meta,
            "elapsed_min": run_meta["elapsed_min"],
            "message": f"baseline finished: {run_meta['halted']}",
            "report": report,
            "updated_at": _now(),
        },
    )

    print("\n" + "=" * 64)
    print("BASELINE EPOCH RUN FINISHED")
    print(f"  elapsed        = {run_meta['elapsed_min']} min")
    print(f"  epochs done    = {run_meta['epochs_completed']}")
    print(f"  halt reason    = {run_meta['halted']}")
    print(f"  fetched_ok     = {idx.get('fetched_ok')}")
    print(f"  optical obs    = {idx.get('total_optical_observations')}")
    print(f"  FSOT all_pass  = {(final_verify or {}).get('all_pass')}")
    print(f"  FSOT pooled %  = {(final_verify or {}).get('pooled_median_error_pct')}")
    print(f"  O–C objects    = {oc_summary.get('objects_with_oc')}")
    print(f"  O–C median ″   = {oc_summary.get('median_oc_arcsec')}")
    print(f"  report         = {store / EPOCH_REPORT}")
    print(f"  status         = {store / EPOCH_STATUS}")
    print("  git            = NOT pushed (ask when ready)")
    print("=" * 64)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
