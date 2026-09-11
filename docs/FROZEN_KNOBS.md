# No decimal knobs — identities

**Peer review:** out of scope.

“Zero free parameters” means the engine is **self-derived**. Assigned decimals (`0.99`, `0.01`, `10`, per-domain `0.85`…) were a drift. They are replaced by seed identities. A miss goes to [`../results/MISSES.md`](../results/MISSES.md). We do **not** put the decimals back to chase a residual.

## What the decimals were

| Knob | Was | Identity |
|------|-----|----------|
| \(K\) polish | \(0.99\) | \(1-\pi^{-4}\) |
| \(C_{\mathrm{eff}}\) polish | \(0.01\) | \(\pi^{-4}\) |
| \(C_{\mathrm{cosm}}\) | \(1/(\varphi\cdot 10)\) | \(1/(\varphi\cdot\pi^2)\) |
| Ledger B \(f_{\mathrm{domain}}\) | 0.0001–0.001 table | \(\alpha=\ln\pi/(e\varphi^{13})\) |
| \(\delta\psi\) table | 0.08, 0.85, 0.95, … | default \(1\); Atomic \(e/\pi\); HEP \(1-\mathrm{POOF}/\pi\) |
| `hits` table | 0–3 | default \(0\); HEP collision \(=1\) |

\(\pi^2\approx 9.87\) was being rounded to \(10\). \(\pi^{-4}\approx 0.01027\) was being rounded to \(0.01\). \(1-\pi^{-4}\approx 0.9897\) was being rounded to \(0.99\).

## \(D_{\mathrm{eff}}\) is derived

Not an integer written on the domain. The 25-D fluid has one nested-orifice chain (micro → macro). Look-splits share a generation \(g\). Then

\[
D_{\mathrm{eff}}(g)=\mathrm{round}\bigl(5\cdot 5^{g/(G-1)}\bigr)
\]

Five seeds → \(D=5\) at \(g=0\). Ceiling \(5^2=25\) at the last generation. You cannot move Chemistry to \(D=9\) to green a file; you would have to change the nest, which is a new edition.

`observed`: medium (dark) vs specimen (look). Ontology of the fold, not a per-row switch.

## Hash gate

`python scripts/audit_parameter_count.py` fails if these identities move without a new pin. Previous pin **D1D38A** held the rounded decimals. This edition is a new pin.
