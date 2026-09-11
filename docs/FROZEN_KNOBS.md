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

## What is still a named orifice, not a fit

\(D_{\mathrm{eff}}\): five seeds → Particle at \(D=5\), ceiling \(5^2=25\). Each domain is a rung on that compactification ladder (which slice of the fluid you are looking through). That is a coordinate chart, not a residual dial. Changing a rung to green a file is forbidden.

`observed`: medium (dark) vs specimen (look). Ontology of the fold, not a per-row switch.

## Hash gate

`python scripts/audit_parameter_count.py` fails if these identities move without a new pin. Previous pin **D1D38A** held the rounded decimals. This edition is a new pin.
