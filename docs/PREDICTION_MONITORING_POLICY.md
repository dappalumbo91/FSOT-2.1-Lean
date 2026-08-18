# Prediction monitoring policy (WIP model)

## Principles

1. **Development does not freeze** while we wait for survey drops.  
2. **Git commit SHA + timestamp** is the preregistration clock for any prediction already on GitHub.  
3. When data lands, **log the outcome** against that SHA in **`results/`** — do not retune the predicted centrals in `predictions/`.  
4. New model work continues on `main` with new commits; outcomes go in the results scoreboard.  
5. Large raw datasets live on **external drive** (`G:/FSOT-PublicData/…` or `I:\FSOT-Physical-Archive\03_FSOT-PublicData`); monorepo keeps engines + predictions + results pointers.

## Closest calendar drops (update with ranker)

```powershell
python scripts/rank_nearest_data_drops.py
```

As of the 2026-08 session research:

| Priority | Event | Window |
|----------|--------|--------|
| **#1 hard date** | **Euclid DR1-Foundation** | **12 Nov 2026** (~3 months) |
| **#1 target cluster** | Rubin LSST EDP2 complete | Oct–Dec 2026 |
| Rolling | DESI BAO papers, JWST/CCHP/SH0ES host papers, CHIME FRB | continuous |
| Later | Euclid DR1 complete (WL/S8) | mid-2027 |

**Practical nearest formal monitor:** Euclid DR1-Foundation (12 Nov 2026) for cosmology catalog locks; **continuous** DESI/JWST papers can fire any week.

## Informal prior calls (context only)

Pre-formal public calls (e.g. Euclid characteristics before drop; I3 Atlas comet morphology/function months before JWST public data) may live on X highlights. Those are **historical context**, not the formal scoreboard. Formal claims use:

- Commit SHA on `dappalumbo91/FSOT-2.1-Lean`
- `predictions/domain_prediction_atlas.json` / H0 multi-tool / sightline / TRGB files
- Outcome log entries (below)

Being directionally right with residual outside a future 0.5% gate is still useful model information — it does not auto-break the engine unless a registered kill criterion fires.

## Outcome log (when a drop happens)

**Predictions stay in `predictions/`.**  
**Results go in `results/`.**

```powershell
python scripts/record_prediction_outcome.py `
  --pred-id PRED-042 `
  --survey Euclid-DR1-Foundation `
  --result hold `
  --notes "…"
```

Append-only file: `results/outcomes/prediction_outcome_log.jsonl`

```json
{"ts":"ISO-UTC","commit_sha":"…","pred_id":"PRED-042","survey":"Euclid-DR1-Foundation","result":"hold|kill|partial|awaiting|theory_rebase","notes":"…","measured":null}
```

Also write a dated pack under `results/literature/YYYY-MM-DD_crossref.md` and refresh `results/INDEX.md`.

Optional external mirror:

`G:/FSOT-PublicData/anomaly_observables/prediction_monitor_logs/`  
`I:\FSOT-Physical-Archive\03_FSOT-PublicData\` (same role on the physical archive)

## Separate predictions repository?

| Option | Pros | Cons |
|--------|------|------|
| **Stay in monorepo** (recommended default) | One pin D1D38A, one green gate, multiprover stays coupled | Bigger public surface |
| **Thin mirror repo** (`FSOT-Predictions`) | Clean public scoreboard; easy for skeptics | Must sync hashes carefully |
| **Fully separate only** | Isolation | Drift from engine; loses multiprover authority |

**Recommendation:** keep authority in monorepo; if you want a public-facing scoreboard later, add a **thin mirror** that only vendors prediction JSON + outcome log + README pointing at monorepo SHAs. Do not split the engine.

## Commands

```powershell
python scripts/build_cchp_trgb_sightline_predictions.py
python scripts/build_h0_sightline_predictions.py
python scripts/build_h0_multi_tool_predictions.py
python scripts/build_domain_prediction_atlas.py
python scripts/rank_nearest_data_drops.py
python scripts/run_prediction_monitor.py
python scripts/record_prediction_outcome.py --help
```
