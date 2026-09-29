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

Checked by `python scripts/fsot_correspondence_limit.py`. On the live pin the home unobserved scalar equals \(S_{\mathrm{cosm}}\), and the Chemistry fold equals \(S_{\mathrm{chem}}\). `vendor/fsot_compute.py` is not rewritten.

Chemistry leaves such as ammonia \(\Delta H_{\mathrm{vap}}\) are separate seed evaluations in kJ/mol. They use this same \(e\), \(\pi\), and \(K\). They are not a second law.
