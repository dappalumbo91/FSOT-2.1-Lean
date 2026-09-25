# Pin lineage — live vs freeze

**Live pin:** **AEB2AD** (`vendor/fsot_compute.py` SHA-256 prefix).  
**Paper 03 freeze pin:** **D1D38A** (2026-09-09, do not rewrite).

Same scalar law. A pin is the SHA of the authority file, not a second engine.
When `fsot_compute.py` gained nest / derived \(D_{\mathrm{eff}}\) / named look laws,
the prefix moved D1D38A → AEB2AD. Ledger A numbers that were frozen under
D1D38A stay in [`../predictions/LEDGER_A_FREEZE.yaml`](../predictions/LEDGER_A_FREEZE.yaml)
and Paper 03 [`FREEZE.yaml`](../papers/03-fsot-theory-of-everything-claim/FREEZE.yaml).

| Surface | Which pin |
|---------|-----------|
| Live docs, CURRENT_STATUS, uniqueness spine, millenium lab | **AEB2AD** |
| Issued dated-forecast JSON, toe_prereg_freeze, Paper 03 freeze, kaggle snapshot | **D1D38A** (historical freeze) |
| Ledger A misses (H0 class, geometric \(1/(e\pi)\), …) | Frozen under D1D38A; live object may be superseded — see [`../results/MISSES.md`](../results/MISSES.md) |

Forbidden: rewriting a freeze file to say AEB2AD so a miss looks closed.  
Allowed: live prose says AEB2AD; freeze files keep D1D38A and point here.

Confirm live: `python scripts/build_repo_status_snapshot.py` → `authority.pin_prefix`.

## Freeze file bytes

The prereg hashes for `predictions/h0_sightline_predictions.json` (`1e050028…ac27`) and `predictions/h0_multi_tool_predictions.json` (`298c71f1…15fc`) match the files as stored: Windows CRLF, and no extra final newline. An LF-normalized copy does not match. Do not rewrite those files to LF. That would change the hash without changing the numbers.
