# Repo sync & expansion checklist

**Purpose:** When we deepen FSOT (new panels, densify, multiprover, hardware), update **every surface** that still shows old numbers or omits new work — not only the new JSON.

**Authoritative live stamp:** [`CURRENT_STATUS.md`](CURRENT_STATUS.md) · `data/repo_status_snapshot.json`  
**Regenerate:** `python scripts/build_repo_status_snapshot.py`

---

## After every expansion batch

### 1. Science / math (required)

| Step | Command / artifact |
|------|-------------------|
| Build new panels | domain `build_*.py` / bridge libs |
| Proper densify only | `docs/FSOT_PROPER_DENSIFY_POLICY.md` + `fsot_proper_densify_lib` |
| Margin audit | `python scripts/audit_all_benchmark_margins.py` |
| Authority pin | `vendor/fsot_compute.py` still **D1D38A** |
| Status snapshot | `python scripts/build_repo_status_snapshot.py` |

### 2. Formal / multiprover (when batch is “public-ready”)

| Step | Command / artifact |
|------|-------------------|
| Lean priors | `gen_*_lean.py` or extension template for new panels |
| Full multiprover | `python scripts/run_cross_proof_verification.py` |
| Confirm | `overall_ok` / `github_ready` in `data/cross_proof_verification_report.json` |
| Debt language | `docs/MULTIPROVER_DESIGN_DEBT_CLARIFIED.md` (0 true margin violations) |

### 3. Documents to touch (if numbers or capabilities changed)

| Doc | What to update |
|-----|----------------|
| [`CURRENT_STATUS.md`](CURRENT_STATUS.md) | Auto via snapshot script |
| [`README.md`](../README.md) | Edition date + **headline** green count + links to new spines |
| [`FSOT_MATH_KEY.md`](FSOT_MATH_KEY.md) | Green count / edition |
| [`FSOT_MATH_KEY_ONEPAGER.md`](FSOT_MATH_KEY_ONEPAGER.md) | Green count |
| [`CLEAR_PATH_FOR_INDEPENDENTS.md`](CLEAR_PATH_FOR_INDEPENDENTS.md) | Expect green N/N |
| [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md) | Only if kill path changed |
| Domain-specific docs | Hardware, QCE, Dzhanibekov, etc. when that domain moved |
| [`verification/README.md`](../verification/README.md) | Pass bar if multiprover shape changed |
| Paper scaffolds under `papers/` | Only when freezing a preprint |

### 4. Do **not** hand-maintain

- Per-domain residual tables that regenerate from JSON  
- Multiprover chunk listings (export scripts own them)  
- Local-only `SESSION_STATUS_AND_GAP_FILL.md` (gitignored)

### 5. Commit message habit

Include: green N/N · pin D1D38A · multiprover overall_ok if re-run · which domains deepened.

---

## Expansion depth rules (while growing)

1. **Formula + real measured only** — no process/identity padding (`FSOT_PROPER_DENSIFY_POLICY.md`).  
2. **Wrong residual → D_eff / route first** — never free params (`FSOT_MATH_KEY.md`).  
3. **Flagship domains** get skeleton depth (defining laws + non-trivial prediction + falsifier).  
4. **Repo sync** is part of the batch — not a later cleanup.

---

## Quick “are we in sync?” check

```powershell
python scripts/build_repo_status_snapshot.py
# Compare green count to README headline
# Confirm pin_match true and overall_ok true in data/repo_status_snapshot.json
```
