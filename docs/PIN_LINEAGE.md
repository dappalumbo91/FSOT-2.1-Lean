# Pin lineage — live vs freeze

**Live pin:** **2C9442** (`vendor/fsot_compute.py` SHA-256 prefix).  
New authority `2C9442B7295A1D39928C5C7CCB81280B443210681FAA74C4D8D4DF37D43A23D2` (owner decisions OD-1/OD-2 + Γ_Z/M_Z target fix, 2026-10-02); previous AEB2AD.  
**Paper 03 freeze pin:** **D1D38A** (2026-09-09, do not rewrite).

Same scalar law. A pin is the SHA of the authority file, not a second engine.
When `fsot_compute.py` gained nest / derived \(D_{\mathrm{eff}}\) / named look laws,
the prefix moved D1D38A → AEB2AD. On 2026-10-02 the prefix moved AEB2AD → 2C9442 for OD-1, OD-2, and the \(\Gamma_Z/M_Z\) target ([`OWNER_DECISIONS.md`](OWNER_DECISIONS.md)). Ledger A numbers that were frozen under
D1D38A stay in [`../predictions/LEDGER_A_FREEZE.yaml`](../predictions/LEDGER_A_FREEZE.yaml)
and Paper 03 [`FREEZE.yaml`](../papers/03-fsot-theory-of-everything-claim/FREEZE.yaml).

| Surface | Which pin |
|---------|-----------|
| Live docs, CURRENT_STATUS, uniqueness spine, millenium lab | **2C9442** |
| Issued dated-forecast JSON, toe_prereg_freeze, Paper 03 freeze, kaggle snapshot | **D1D38A** (historical freeze) |
| Ledger A misses (H0 class, geometric \(1/(e\pi)\), …) | Frozen under D1D38A; live object may be superseded — see [`../results/MISSES.md`](../results/MISSES.md) |

Forbidden: rewriting a freeze file to say AEB2AD so a miss looks closed.  
Allowed: live prose says 2C9442; earlier live prose may say AEB2AD; freeze files keep their own pins and point here.

Confirm live: `python scripts/build_repo_status_snapshot.py` → `authority.pin_prefix`.

The Ledger A yaml is unchanged. Its SHA-256 is recorded in [`../predictions/LEDGER_A_FREEZE_SHA256.json`](../predictions/LEDGER_A_FREEZE_SHA256.json). The domain mapping frozen at pin AEB2AD stays hashed in [`../predictions/domain_freezes/AEB2AD_mapping.json`](../predictions/domain_freezes/AEB2AD_mapping.json). That freeze was not rewritten for 2C9442. `predictions/toe_prereg_freeze.json` stays the D1D38A preregistration. The date gap, and the two `w_a` values, are in [`FREEZE_HYGIENE.md`](FREEZE_HYGIENE.md).

## Freeze file bytes

The prereg hashes for `predictions/h0_sightline_predictions.json` (`1e050028…ac27`) and `predictions/h0_multi_tool_predictions.json` (`298c71f1…15fc`) match the files as stored: Windows CRLF, and no extra final newline. An LF-normalized copy does not match. Do not rewrite those files to LF. That would change the hash without changing the numbers.
