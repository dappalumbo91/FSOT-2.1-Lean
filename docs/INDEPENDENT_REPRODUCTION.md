# Independent reproduction pack (anonymous)

Anyone with a clean machine can falsify or confirm FSOT **without** knowing who else has run it.  
This pack is intentionally **anonymous**: no personal names, no private channels — only public repo commands and artifacts.

**Sibling OS work** (kernel / QEMU) lives in the separate Reality OS repository; this pack covers the **FSOT-2.1-Lean monorepo** empirical + formal claim surface.

---

## What independent means here

| Requirement | How |
|-------------|-----|
| Clean clone | Fresh `git clone` of public GitHub, not a dirty worktree |
| Seed pin | Engine SHA must start with **D1D38A** |
| Zero free parameters | `parameter_count_audit.json` → **ZERO_FREE** |
| Green gate | `benchmark_margin_audit.json` → fail count **0** |
| Multi-prover | `cross_proof_verification_report.json` → `overall_ok: true` (when full stack installed) |
| Pre-data freeze | `toe_prereg_freeze.json` has `bundle_sha256` |
| No names needed | Publish only commands + hashes + JSON verdicts |

---

## 20-minute kill path

```powershell
git clone https://github.com/dappalumbo91/FSOT-2.1-Lean.git
cd FSOT-2.1-Lean
pip install -r requirements.txt

python scripts/build_repo_status_snapshot.py
python scripts/audit_all_benchmark_margins.py
python scripts/audit_parameter_count.py
```

**Pass criteria (machine-readable):**

1. `docs/CURRENT_STATUS.md` — pin D1D38A, `pin_match: true`  
2. `data/benchmark_margin_audit.json` — `green_gate_fail_count == 0`  
3. `data/parameter_count_audit.json` — ZERO_FREE class  

Optional deeper:

```powershell
python scripts/run_cross_proof_verification.py
python scripts/run_mathlib_rederivation_campaign.py
python scripts/build_toe_gap_closure.py
python scripts/build_contested_future_observation_ledger.py
```

Optional formal engine (Lean 4 + Mathlib toolchain):

```powershell
lake build FSOT.Formal.Bounds FSOT.Formal.Theorems
```

---

## Contested / pre-data (where models can disagree later)

| Artifact | Role |
|----------|------|
| `docs/PREDATA_RISK.md` | Discipline: freeze before surveys |
| `predictions/toe_prereg_freeze.json` | SHA-locked prediction slate |
| `data/contested_observables_closure.json` | 13 hard open-science observables |
| `predictions/contested_future_observation_ledger.json` | Future survey differentiators |
| `predictions/reports/CONTESTED_SECTOR_WATCH.md` | Living watch table |

Independent readers should **not** ask “who verified this?” — they should re-run the commands and publish their own `bundle_sha256` / green counts.

---

## What a serious independent report looks like

Publish (public gist, issue, or paper supplement):

1. Git commit SHA of the clone  
2. OS + Python version  
3. `pin_match` and engine SHA prefix  
4. `green_gate_pass_count` / `fail_count`  
5. Whether multiprover `overall_ok` was run  
6. Whether any kill criterion in `toe_prereg_freeze.json` failed against a **new** survey number  

Do **not** publish private identities of other reproducers. The claim stands or falls on **artifacts**, not testimonials.

---

## Related entry points

- Fast skeptic path: [`SKEPTIC_REPLICATION_KIT.md`](SKEPTIC_REPLICATION_KIT.md)  
- Plain ladder: [`CLEAR_PATH_FOR_INDEPENDENTS.md`](CLEAR_PATH_FOR_INDEPENDENTS.md)  
- Claim tiers: [`RESIDUAL_HONESTY_AND_CLAIM_TIERS.md`](RESIDUAL_HONESTY_AND_CLAIM_TIERS.md)  
- Label A/B freeze: [`TOE_CLAIM_BOUNDARIES.md`](TOE_CLAIM_BOUNDARIES.md)  
- Live stamp: [`CURRENT_STATUS.md`](CURRENT_STATUS.md)
