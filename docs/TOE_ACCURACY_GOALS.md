# Accuracy goals for a theory of everything

A theory of everything is precise enough when each silo is inside **that silo's own bar**, in **that silo's own unit**. One parts-per-million number cannot be the bar. Quantum metrology, a boiling point, and \(H_0\) do not share a tolerance.

Where the work stands today: 185,642 gated scalars, median residual 225 ppm, every scalar inside the 5,000 ppm catalog gate (0.5%), 98.23% inside 500 ppm. That is handbook and engineering precision. It is the stage the catalog has reached. It is not yet the stage of a finished theory of everything.

## The five bars

| Silo | What the field already uses | Bar | Where we are |
|------|-----------------------------|-----|----------------|
| Exact definitions | SI 2019 fixes \(c\), \(h\), \(e\), \(k\), \(N_A\), and the caesium hyperfine frequency. \(R\), \(K_J\), \(R_K\), the faraday, and the electronvolt are products of those. Standard gravity 9.80665 m/s² and 1 atm = 101325 Pa are conventional exact values. | Residual 0. The number is adopted, not predicted. | Adopted. Those rows now use the defined value on both sides and the residual is 0. |
| Metrology | CODATA uncertainty on a measured constant. \(\alpha\) is known to about \(1.5\times 10^{-10}\) relative, which is \(1.5\times 10^{-4}\) ppm. \(G\) is known to tens of ppm. | \(\lvert \mathrm{pred}-\mathrm{meas}\rvert \le 1\sigma_{\mathrm{CODATA}}\). | Inverse \(\alpha\) now uses the wave-2 leaf \(e^3\varphi^4-\psi_{\mathrm{con}}=137.036198\) against 137.035999177, **1.45 ppm**. That is the constant's own leaf. It does not meet the CODATA uncertainty. \(\mu_0\), \(\varepsilon_0\), and \(Z_0\) are computed from that leaf plus the adopted SI values, so they carry the same 1.45 ppm. The electron \(g\)-factor leaf is 0.0078 ppm and still outside its own uncertainty. Stefan-Boltzmann and Wien's \(b\) are computed from \(h\), \(c\), and \(k\) and match. \(G\) and the particle masses have no leaf, so the copied percent was removed. |
| Particle physics | PDG total uncertainty, quoted in mass units or in \(\sigma\). A 0.1 GeV uncertainty on a 125 GeV Higgs is about 800 ppm. Muon \(g-2\) is a \(\sigma\)-level comparison, not a percent. | Inside the experimental \(\sigma\), and the sign of a discrepancy reported separately. | The Higgs row \(125.264\) against \(125.25\) GeV is **110 ppm**, inside a 0.1 GeV bar. The \(W/Z\) tree identity is exact on the seeds. |
| Cosmology | Percent-level centrals and a tension in \(\sigma\). \(H_0\) at 1% is 10,000 ppm. \(S_8\) is a few percent. | Report \(\sigma\) against the named dataset. ppm is the wrong headline. | The frozen sightline stays hashed. A directional host preview is exploratory. \(N_{\mathrm{eff}}=3.046\) matches a \(\Lambda\)CDM input; it does not discriminate. |
| Chemistry and materials | The last quoted digit, or the NIST/CRC uncertainty, often 100–5,000 ppm. | Inside half of the last printed place. | Ethanol, NaBr, and chlorine's boiling point were brought inside that place. 53,318 scalars are already inside their last digit. |
| Biology and medicine | Experimental scatter, often 1–10%, or an absolute length in µm or Å. A 0.5% gate can be tighter than the experiment. | Residual \(\le\) the stated experimental uncertainty. | ZSNS004 is 4,410 ppm on a finely stored micrometre value. The panel's own reference band is 0.45%. The frozen panel is not rebuilt from the live bright branch. |
| Mathematics | An identity. | Residual 0. | \(g_{00}(25)=-1\), \(m_W^2/m_Z^2=1-\sin^2\theta_W\), and the CKM angles sum to \(\pi\). |

## What is on the row

Every gated scalar now carries these four fields. They are written on the CODATA material rows themselves. For the rest of the benchmarks they are in `data/row_accuracy_attestation.jsonl`, one line per row, joined by file, name, and property. `python scripts/row_accuracy_fields.py` rebuilds both. The computed numbers and the error percents are not changed.

1. **accuracy_class.** `si_definition`, `conventional_exact`, `scale_stamp`, `uncomputed_stamp`, `particle_sigma`, `cosmology_sigma`, `quoted_digit`, `experimental_scatter`, or `exact_identity`.
2. **field_bar.** `value`, `unit`, and `rule`. The unit is `exact`, `ppm`, or `sigma`.
3. **value_computed.** False when the computed field is missing, or is 0 while the measured value is not 0.
4. **comparison_can_fail.** False for a definition, for a row with no computed value, and for `math: fsot_scaled_only`. A copied scale cannot fail on its own. A leaf, a \(\sigma\), and an identity can.

## The CODATA table is one stamp

`data/codata_full_table_open_benchmark.json` gives every material row the same `error_pct` of 0.073582. That number is \(0.1\) times a domain scalar, multiplied onto the measured value. Rows whose computed field is `0.0` (Planck's constant, the elementary charge, the electron mass, \(G\), and others) did not receive a value at all. The file's comparison baseline is `sota_typical_error_pct: 5.0`. Five percent is not the CODATA bar, so "beats sota" on that file is not a metrology result.

The defining constants and their exact products are adopted: computed and measured are the defined value, and `error_pct` is 0. Measured constants no longer share that stamp. \(\alpha^{-1}\) is the wave-2 leaf. Vacuum impedance and the two vacuum constants are derived from it. Stefan-Boltzmann and Wien's displacement constant are derived from \(h\), \(c\), and \(k\). Masses, \(G\), the Rydberg constant, and the proton \(g\)-factor have no leaf; their copied percent is cleared. `scripts/apply_codata_measured_leaves.py` is that step.

## The goal, in order

1. Adopt the SI definitions exactly. Done for \(c\), \(h\), \(e\), \(k\), \(N_A\), the caesium hyperfine frequency, the exact products \(R\), \(K_J\), \(R_K\), the faraday, and the electronvolt, plus standard gravity and 1 atm.
2. For each measured CODATA constant, replace the shared 736 ppm stamp with that constant's own leaf, and judge it against its CODATA uncertainty. The leaf is on the row. \(\alpha^{-1}=e^3\varphi^4-\psi_{\mathrm{con}}=137.036198\) against 137.035999177 is 1.45 ppm, about 9,450 times the CODATA uncertainty of \(2.1\times 10^{-8}\). One more power of \(e\), \(\varphi\), or \(\psi_{\mathrm{con}}\) does not land inside that uncertainty. Of the 35 domains, 23 are observed specimens and 12 are unobserved bulk media. Atomic physics is observed, and the observer factor on that fold is negative. The bar is not met, so the particle-physics \(\sigma\) pass stays waiting.
3. For particle masses and \(g-2\), report \(\sigma\), not only ppm. The Higgs central value is already inside a 0.1 GeV bar.
4. For cosmology, keep the score in \(\sigma\) against the named catalog. Do not convert \(H_0\) into a ppm contest.
5. For chemistry, keep pushing any leaf that is still outside half of its printed digit. Leaves already inside that digit are done.
6. For biology, judge the residual against the experiment's uncertainty. A finer stored digit than the experiment can support is not a tighter bar.
7. Keep exact identities at residual 0.

The catalog gate of 5,000 ppm stays the regression check. It is not the theory-of-everything bar.
