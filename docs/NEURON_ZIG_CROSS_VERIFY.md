# Neuron-zig mind → FSOT-2.1-Lean cross-verify

**Pin:** D1D38A · **free_params=0** · Hub green ≤ **0.5%** pooled median  
**Sibling:** [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig)  
**Related:** [`NEURON_ZIG_TO_OS_ROADMAP.md`](NEURON_ZIG_TO_OS_ROADMAP.md) · [`RELATED_EMBODIMENTS.md`](../RELATED_EMBODIMENTS.md)

---

## Intent

Hook the Zig neural mind into the **same residual + multiprover path** used for other FSOT domains:

1. Export a machine stamp from Zig (`FSOT_MIND_VERIFY_STAMP.json`)  
2. Build a residual **benchmark panel** in this hub  
3. Run **margin audit** (≤0.5% scalar green)  
4. Record **holes** (process debt / logic-application gaps) honestly  
5. Continue only when `overall_ok` (stamp + no blockers + green scalar)

This is **not** “LLM accuracy.” It is residual-gated process under one pin.

---

## Pipeline

```text
fsot-neuron-zig
  fsot_mind verify-stamp
       │
       ▼
  data/results/FSOT_MIND_VERIFY_STAMP.json
       │  (Desktop path auto-discovered, or copy into hub)
       ▼
FSOT-2.1-Lean
  python scripts/build_neuron_zig_mind_panel.py
       │
       ├─► data/neuron_zig_mind_panel_benchmark.json   (margin audit)
       └─► data/neuron_zig_cross_proof_closure.json    (overall_ok + holes)
       │
  python scripts/audit_all_benchmark_margins.py
  python scripts/run_cross_proof_verification.py   # full multiprover spine
```

### One-shot from hub (after stamp exists)

```powershell
cd path\to\FSOT-2.1-Lean
python scripts/build_neuron_zig_mind_panel.py
python scripts/audit_all_benchmark_margins.py
# optional full multiprover:
python scripts/run_cross_proof_verification.py
```

### One-shot from Zig (generate stamp)

```powershell
cd path\to\fsot-neuron-zig
zig build -Doptimize=ReleaseFast
.\zig-out\bin\fsot_mind.exe verify-stamp
# optional: copy stamp into hub for portable CI
# copy data\results\FSOT_MIND_VERIFY_STAMP.json ..\FSOT-2.1-Lean\data\neuron_zig_stamp\
```

**Stamp search order** (first hit wins):

1. `FSOT-2.1-Lean/vendor/neuron_zig/FSOT_MIND_VERIFY_STAMP.json`  
2. `FSOT-2.1-Lean/data/neuron_zig_stamp/FSOT_MIND_VERIFY_STAMP.json`  
3. `Desktop/fsot neuron family/fsot-neuron-zig/data/results/FSOT_MIND_VERIFY_STAMP.json`  
4. `I:\fsot-neuron-zig\data\results\FSOT_MIND_VERIFY_STAMP.json`  

---

## What is green-gated (≤0.5%)

| Record class | Examples |
|--------------|----------|
| Seed identity | π, φ residual 0 |
| Pin honesty | D1D38A, free_params=0 |
| Capacity IDs | regions=6, units=56, MAX_N=64 |
| Structure gates | stamp present, probe ok, history refusal, multi-hop bar |

Binary gates use error 0% / 100% so a single fail is visible without inventing free parameters.

---

## What is process debt (not 0.5% scalar poison)

Accuracy residuals vs perfect (e.g. atomic 0.60 → 40% residual vs perfect) are **process debt**:

- Tracked in `holes` / `process_debt`  
- **Not** used to force free-param fits  
- Fix by STEM extract/encode depth — **still no history corpus**

### Latest verified stamp (gap-fill)

| Metric | Value |
|--------|-------|
| Overall process / residual | **1.00** / **0.00** |
| Atomic / logic / multi / unknown | **1.00** / **1.00** / **1.00** / **1.00** |
| Hub pooled median | **0.0%** · max scalar **0.0%** |
| Closure | **`overall_ok: true`** · blockers **0** · process_debt **0** |

### Process debt

**Cleared** after STEM probe anchors + cue-hash normalize + extract widen (`do` / `goes from`) + anchor-win dedupe. Multi-hop and history refusal remain **1.0**.

---

## Closure semantics

`data/neuron_zig_cross_proof_closure.json`:

| Field | Meaning |
|-------|---------|
| `hub_green_pass` | scalar pooled median ≤ 0.5% |
| `stamp_ok` | Zig stamp present and `ok: true` |
| `blocker_count` | must be 0 |
| `process_debt_count` | refinements (may be >0) |
| `overall_ok` | green + stamp + no blockers |

**Continue the project when `overall_ok: true`.** Process debt can remain on the refinement list.

**Current:** `overall_ok: true` — multiprover catalog stamp includes mind panel.

---

## Multiprover

Mind panel is residual-gated in the **scientific catalog spine** (same path as other domains):

| Obligation id | Kind |
|---------------|------|
| `cat_neuron_zig_mind_panel_records_pos` | nat_pos (25) |
| `cat_neuron_zig_mind_panel_pooled_under_half_pct` | lt_half (0.0) |
| `cat_neuron_zig_mind_panel_pooled_lt_half_pure` | r_lt_lit_pure |
| `cat_neuron_zig_mind_panel_max_scalar_under_half_pct` | lt_half (0.0) |
| `cat_neuron_zig_mind_panel_green_flag` | eq_nat |

After panel build:

```powershell
python scripts/export_scientific_catalog_obligations.py
python scripts/generate_scientific_catalog_artifacts.py
python scripts/run_smt_catalog_bounds.py
# catalog Coq: verification/coq/ScientificCatalogSpine_*.v
python scripts/run_cross_proof_verification.py   # full multiprover spine
```

Verified on first mind ingest: **python 2032/2032**, **SMT z3 2032/2032**, **Coq ScientificCatalogSpine 17/17**.

OS path panel (ABI / bare-metal) remains:

```text
python scripts/build_neuron_zig_os_path_panel.py
→ data/neuron_zig_os_path_panel_benchmark.json
```

---

## Doctrine

- Same pin as hub — no second theory  
- STEM + logic experience only in the mind fold until later  
- Holes must be listed, not hidden  
- Green gate failures after clean stamp + audit = **kill / fix before expansion**
