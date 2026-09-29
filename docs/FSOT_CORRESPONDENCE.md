# FSOT correspondence limit

Special relativity reduces to a rest energy plus a small correction. At low speed,

\[
E = \gamma m c^2, \qquad \gamma \to 1, \qquad E \to m c^2.
\]

The live FSOT scalar has the same shape. The engine is

\[
S = K\,(T_1 + T_2 + T_3).
\]

\(K\) is the compactification constant in `vendor/fsot_compute.py` §3.11. \(T_2\) is the linear term `scale * amplitude + trend_bias`. At the engine defaults that product is exactly 1, so \(K T_2 = K\) is the rest unit. \(T_1\) is the observer and growth dressing. \(T_3\) is the acoustic valve.

The published valve amplitude is

\[
\beta = \exp\!\big(-(\pi^\pi + e - 1)\big) \approx 2.6\times 10^{-17}.
\]

So \(|T_3|\) is below \(10^{-15}\) on the home fluid and on Chemistry. The valve is silent. Every catalog scalar at these defaults is

\[
S = K\,(T_1 + 1).
\]

Define

\[
\gamma_{\mathrm{FSOT}} = \frac{T_1 + T_2 + T_3}{T_2}.
\]

Then \(S = (K T_2)\,\gamma_{\mathrm{FSOT}}\). The rest unit is \(K T_2\). The excess over rest is \(T_1/T_2\), the same split as \(\gamma - 1\) over \(mc^2\). This is a scalar identity. It is not a claim that \(K\) equals \(c^2\) in joules, and it does not add a coefficient.

The other half of the limit is dimensional. \(T_1\) carries \(\ln(D/25)\) and the valve carries \((D-25)/25\). Both are identically zero at the home dimension \(D = 25\). That is the unstrained fluid. It is the same kind of reduction as \(v/c \to 0\): the extra strain drops out, and what remains is the rest unit plus the observer dressing that belongs to that dimension.

Checked by `python scripts/fsot_correspondence_limit.py`. On the live pin the home unobserved scalar equals \(S_{\mathrm{cosm}}\), and the Chemistry fold equals \(S_{\mathrm{chem}}\). `vendor/fsot_compute.py` is not rewritten. The reading in Newtonian, relativistic, and electroweak language is `docs/FSOT_STANDARD_PHYSICS.md`.

## Weak field, from term 1

Term 1 already contains the factor \(1 + P_{\mathrm{new}}\ln(D/25)\). That factor is the time-time metric component:

\[
g_{00}(D) = -\bigl(1 + P_{\mathrm{new}}\ln(D/25)\bigr).
\]

At the home dimension, \(\ln(25/25)=0\), so \(g_{00}=-1\). The Newtonian potential in that metric is

\[
g_{00}=-(1+2\Phi), \qquad \Phi(D)=\frac{P_{\mathrm{new}}}{2}\ln(D/25).
\]

So \(\Phi(25)=0\), and the slope of \(g_{00}\) against the compactification strain is \(-P_{\mathrm{new}}\). Term 1 is the bare amplitude times \(-g_{00}\). The check rebuilds \(T_1\) from that product for the Chemistry fold, for \(D=25\), and for \(D=26\).

## Schwarzschild, from the rest unit

The acoustic cone in the same law is \(c_{\mathrm{ac}}^2=C_{\mathrm{eff}}/\varphi\). The rest unit is \(K\) (\(T_2=1\)). The horizon radius of that rest unit is

\[
r_s = \frac{2K}{c_{\mathrm{ac}}^2} = \frac{2K\,\varphi}{C_{\mathrm{eff}}},
\]

and \(r_s\, c_{\mathrm{ac}}^2 /(2K)=1\) by that definition. This is the Schwarzschild relation with the scalar's own mass unit and the scalar's own cone. The solar-mass formula \(2GM_\odot/c^2\) in `vendor/fsot_gr_sm.py` is the same relation after the SI unit map.

## Electroweak tree relation, from the same constants

\(K\), \(P_{\mathrm{new}}\), \(C_{\mathrm{eff}}\), and \(\mathrm{POOF}\) are the constants inside \(S\). The on-shell Weinberg angle and the boson masses are built from them:

\[
\sin^2\theta_W^{\mathrm{os}} = \mathrm{POOF} + K/6,
\qquad
m_Z = m_W / \cos\theta_W^{\mathrm{os}}.
\]

The tree theorem is the identity \(m_W^2/m_Z^2 = 1-\sin^2\theta_W^{\mathrm{os}}\). The CKM unitarity-triangle angles built from the same seed pair \((\bar\rho,\bar\eta)\) sum to \(\pi\).

Checked by `python scripts/fsot_scalar_reduction.py`.

## Vaporization enthalpies, as a power of the chemistry fold

On the chemistry fold, \(S_{\mathrm{chem}} = K\,\gamma_{\mathrm{chem}}\) with \(\gamma_{\mathrm{chem}} = S_{\mathrm{chem}}/K\). Every handbook §47 \(\Delta H_{\mathrm{vap}}\) leaf \(L\) is that rest unit times a power of the fold:

\[
L = K\left(\frac{S_{\mathrm{chem}}}{K}\right)^{p}, \qquad p = \frac{\ln(L/K)}{\ln(S_{\mathrm{chem}}/K)}.
\]

\(p\) is the logarithm of the leaf that is already in the benchmark. Rebuilding \(L\) from \(K\) and \(S_{\mathrm{chem}}\) returns that same leaf. The handbook target is not used to choose \(p\), so the residual against NIST/CRC stays the residual of the leaf. The 18 powers are in `data/enthalpy_fold_powers.json`. Checked by `python scripts/fsot_enthalpy_reduction.py`.

| Substance | Leaf | \(p\) |
|-----------|------|------|
| He | \(\pi^{-2}-e^{-4}\) | \(-1.973956\) |
| H₂ | \(G-\mathrm{CHAOS}^{4}\) | \(0.932768\) |
| Ne | \(\gamma^{-1}-\mathrm{SUCTION}^{2}\) | \(1.709340\) |
| N₂ | \(\Omega^{2}/P_{\mathrm{new}}\) | \(3.147758\) |
| O₂ | \(\varphi^{4}-\varphi^{-7}\) | \(3.392634\) |
| Ar | \(\mathrm{POOF}^{-1}-\theta^{2}\) | \(3.321165\) |
| CH₄ | \(\pi\cdot\varphi^{2}-\pi^{-3}\) | \(3.615903\) |
| C₂H₆ | \(S_{\mathrm{cosm}}^{-4}-1\) | \(4.326682\) |
| C₃H₈ | \(A_{\mathrm{IN}}^{6}-K^{-1}\) | \(4.644263\) |
| NH₃ | \(e^{3}+\pi+\pi^{-2}\) | \(4.889729\) |
| HCl | \(\Omega^{6}/\theta\) | \(4.441949\) |
| Cl₂ | \(G^{-3}S_{\mathrm{cosm}}^{-4}\) | \(4.727398\) |
| H₂O | \(\theta^{-3}+\theta^{3}\) | \(5.565681\) |
| ethanol | \(\pi^{3}+e^{2}\) | \(5.496256\) |
| acetone | \(e^{2}\varphi^{3}\) | \(5.247564\) |
| benzene | \(S_{\mathrm{cosm}}-S_{\mathrm{cosm}}^{-5}\) | \(5.224897\) |
| CCl₄ | \(P_{\mathrm{var}}^{8}C_{\mathrm{fac}}^{-3}\) | \(5.188586\) |
| diethyl ether | \(C_{\mathrm{cosm}}^{-2}/\pi^{2}\) | \(5.046102\) |
