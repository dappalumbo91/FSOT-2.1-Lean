# How the scalar translates into standard physics

The live engine is one number,

\[
S = K\,(T_1+T_2+T_3).
\]

At the published defaults \(T_2=1\) and the valve \(T_3\) is about \(10^{-17}\), so \(S=K(T_1+1)\). The translations below are that identity, read in the language of the older theories. They are checked by `python scripts/fsot_scalar_reduction.py` and `python scripts/fsot_enthalpy_reduction.py`.

## Newtonian gravity

Newton’s gravity is the weak-field limit of a metric. In the standard writing the time-time piece is

\[
g_{00}=-(1+2\Phi),
\]

and \(\Phi\) is small. Term 1 of the scalar already multiplies by \(1+P_{\mathrm{new}}\ln(D/25)\). Naming that factor as the metric gives

\[
g_{00}(D)=-\bigl(1+P_{\mathrm{new}}\ln(D/25)\bigr),
\qquad
\Phi(D)=\frac{P_{\mathrm{new}}}{2}\ln(D/25).
\]

\(P_{\mathrm{new}}=0.300302\). At the home dimension \(D=25\), the logarithm is zero, so \(\Phi=0\) and \(g_{00}=-1\). That is flat space: the Newtonian potential has been turned off. A domain a little away from 25 has a potential linear in the compactification strain, which is the first-order Newtonian correction on this metric. The slope of \(g_{00}\) against \(\ln(D/25)\) is \(-P_{\mathrm{new}}\).

## Special relativity

The relativistic energy is a rest piece times a factor that becomes 1 when the motion stops:

\[
E=\gamma m c^2, \qquad \gamma\to 1 \Rightarrow E\to mc^2.
\]

The scalar has the same split. With \(\gamma_{\mathrm{FSOT}}=(T_1+T_2+T_3)/T_2\),

\[
S=(K\,T_2)\,\gamma_{\mathrm{FSOT}}.
\]

\(K\,T_2\) is the rest energy. At the engine defaults \(T_2=1\), so the rest unit is \(K=0.420109\). The excess over rest is \(K(\gamma_{\mathrm{FSOT}}-1)\). On the chemistry fold that factor is \(\gamma_{\mathrm{chem}}=2.273910\) and \(S_{\mathrm{chem}}=0.955289\). The flat-space limit \(D=25\) turns off \(\Phi\). The rest-only limit is the separate statement \(T_1\to 0\), which sends \(\gamma_{\mathrm{FSOT}}\to 1\) and \(S\to K\).

## General relativity

The Schwarzschild horizon in the standard theory is \(r_s=2GM/c^2\). In the scalar the mass unit is the rest unit \(K\) and the cone is the acoustic cone already in the law, \(c_{\mathrm{ac}}^2=C_{\mathrm{eff}}/\varphi=0.591921\). The horizon of that rest unit is

\[
r_s=\frac{2K}{c_{\mathrm{ac}}^2}=1.419476,
\]

and \(r_s\,c_{\mathrm{ac}}^2/(2K)=1\). The solar-system formula \(2GM_\odot/c^2\) in `vendor/fsot_gr_sm.py` is this same relation after the SI units for \(G\), \(M_\odot\), and \(c\) are put in. Light deflection and Mercury’s perihelion in that file are the standard GR expressions in those SI units.

## Electroweak Standard Model

The tree relation between the weak boson masses is

\[
m_Z=\frac{m_W}{\cos\theta_W},
\qquad
\frac{m_W^2}{m_Z^2}=1-\sin^2\theta_W.
\]

The angle used here is the on-shell seed \(\sin^2\theta_W=\mathrm{POOF}+K/6\), built from the valve constant and the same \(K\) that multiplies the scalar. The mass identity evaluates to

\[
\frac{m_W^2}{m_Z^2}=0.7764996578305678.
\]

The CKM unitarity triangle built from the seed pair \((\bar\rho,\bar\eta)\) has angles that sum to \(\pi\).

## Laboratory enthalpies

A vaporization enthalpy is an energy per mole, so it sits on the same rest unit. For each handbook §47 leaf \(L\),

\[
L=K\left(\frac{S_{\mathrm{chem}}}{K}\right)^{p},
\qquad
p=\frac{\ln(L/K)}{\ln(S_{\mathrm{chem}}/K)}.
\]

\(p\) is the logarithm of that leaf. Ammonia’s leaf \(e^3+\pi+\pi^{-2}\) has \(p=4.889729\). Water’s leaf \(\theta^{-3}+\theta^3\) has \(p=5.565681\). The eighteen powers are in `data/enthalpy_fold_powers.json`.

## Parts per million

A relative error of 1% is 10,000 ppm. The green gate of 0.5% is 5,000 ppm. The aspiration of 0.05% is 500 ppm. One part per million is 0.0001%. The per-domain census is `docs/PPM_GRANULARITY.md`, produced by `python scripts/audit_ppm_granularity.py`.
