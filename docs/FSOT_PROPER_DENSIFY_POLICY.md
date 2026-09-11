# FSOT proper densify policy

**Rule:** densify only with **your formula** against **real measured data**.  
**After lock \(T_0\) (2026-09-09, pin D1D38A):** a miss is not a fold edit.

## Fold edits are not residual repair

New catalog rows may only use an **already-frozen** domain key.  
A miss goes to [`../results/MISSES.md`](../results/MISSES.md).  
Changing `DomainConfig` integers or \(K\) is a **new pin**, with a diff of every old Ledger A number.

Forbidden as a green-gate repair: “if it fails, change \(D_{\mathrm{eff}}\) first.” That is fitting with extra steps. See [`FROZEN_KNOBS.md`](FROZEN_KNOBS.md) · [`LEDGERS.md`](LEDGERS.md).

## Allowed

| Method | `computed` | `measured` |
|--------|------------|------------|
| Seed closed formula | `evaluate_formula(formula, seed_ctx)` | literature / NIST / lab target |
| Domain scalar route | `measured × (1 + \|S(D_eff)\| · f_domain)` | real anchor |
| Engine closed form (CKM, m_H, α, …) | seed expression | PDG / survey value |

## Forbidden (false densify)

- Seed identity pads (`φ = φ`, `θ = θ` as “records”)
- Process gates as empirical depth (`process_gate`, “source present”)
- Cross-domain **error copy** / `depth_relay_from` without recompute
- Literature identity (`measured = computed = published`) as padding
- Free parameters or residual gaming

## Code

- Library: `scripts/fsot_proper_densify_lib.py`
- Thin depth: `scripts/c_thin_depth_lib.py` (uses proper densify)
- Remediation: `scripts/remediate_false_densify.py`
- Green fix: `scripts/remediate_green_fail_panels.py`

```powershell
python scripts/remediate_false_densify.py
python scripts/audit_all_benchmark_margins.py
```
