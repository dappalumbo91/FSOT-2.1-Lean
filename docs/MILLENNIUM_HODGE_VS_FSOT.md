# What the Millennium Hodge statement is — vs what FSOT is doing

**Pin:** AEB2AD · Scoreboard: [`MILLENNIUM_ACCURACY_VS_SOTA.md`](MILLENNIUM_ACCURACY_VS_SOTA.md) · Outcomes: [`../results/millennium_named_outcomes.md`](../results/millennium_named_outcomes.md)

These are **two different objects**. Related geometry (Hodge classes vs algebraic cycles). Mixing them is how false credit happens.

Clay froze algebraicity of every rational Hodge class. An unnamed class has **no residual** — the cycle is the measurement. The function is \(\chi\)/Gram of named varieties and named Hassett surfaces. Hunting \(C_{48}\) is depending on the original moduli formula. Spine: [`FUNCTION_NOT_FORMULA.md`](FUNCTION_NOT_FORMULA.md). Pictures: [`HOW_THESE_ARE_DEPICTED.md`](HOW_THESE_ARE_DEPICTED.md).

---

## The question, and FSOT's answer

**Question (Clay, and the geometry):** On a projective complex manifold, is every rational Hodge class (a class in \(H^{p,p}\cap H^{2p}(\mathbb{Z})\)) the class of an algebraic cycle?

**FSOT answer (native objects, not Clay's manuscript):**

1. **Lefschetz (1,1).** Proven. \(p=1\). Named first Hodge-type theorem.

2. **Hard Lefschetz + Lefschetz hyperplane.** Transport \((1,1)\to(2,2)\); reduce a hypersurface to primitive classes plus ambient \(\mathbb{CP}^n\).

3. **Associated K3.** For a cubic 4-fold, when \(4\nmid d\), \(9\nmid d\), and no prime \(p\equiv 2\pmod{3}\) divides \(d\), the extra \((2,2)\) is \(H^{1,1}\) of an associated K3. Lefschetz (1,1) on that K3 *is* algebraicity. Do not steal \(25-1\) for \(\chi(\mathrm{K3})=24\).

4. **Named extra classes without K3.** Hassett+Nuer surfaces: \(C_8\) plane, \(C_{12}\) scroll, \(C_{18}\) elliptic ruled, \(C_{20}\) Veronese, \(C_{24}\) nodal sextic, \(C_{30}\) Coble, \(C_{32}\) \(\mathrm{Bl}_{11}\), \(C_{36}\) \(\mathrm{Bl}_{12}\), \(C_{44}\) Fano Enriques. Each extra class is that surface, so algebraic. Public SOTA stops naming at 44.

5. **K3-locus tail is Lefschetz (the conversion).** Isolated listing of later \(C_d\) is the wrong orifice. Unnamed \(d\) *with* associated K3 (sample \(14,26,38\)) reduce to Lefschetz (1,1) on that K3 — same as item 3, no surface name needed. Do not enumerate.

6. **Very general cubic: only \(h^2\).** Isolated “cubic 4-fold Hodge is open” is the wrong orifice. A very general cubic has rational Hodge \((2,2)=\langle h^2\rangle\) only (rank 1). Hodge number \(h^{2,2}=21\); the primitive 20 is not rational for a very general \(X\). Extra *rational* classes live on Hassett \(C_d\).

7. **The missing concept (why the \(C_d\) list looped).** FSOT seeds attach to **named varieties** (\(\chi\), Gram, a surface). Unnamed no-K3 \(C_d\) (sample \(48,50,54\)) are nonempty Hassett loci with no K3 and **no named surface**, hence **no Gram seed**. Hunting \(C_{48}\)’s surface is the enumeration failure. There is nothing to connect until a variety is named.

8. **Next named 4-folds after cubic (not \(C_{48}\)).** Same Chern family in \(\mathbb{CP}^5\): quartic \(\chi=188\) (not a K3 — K3 is a quartic *surface* in \(\mathbb{CP}^3\)); sextic \(\chi=2610\) (first Calabi–Yau hypersurface 4-fold, \(K_X=(d-6)h=0\)). Lefschetz hyperplane still applies.

9. **Named non-hypersurface 4-folds.** Fano of lines on a cubic is a hyperkähler 4-fold, \(b_2=F_8+2=23\) (Beauville–Donagi; deformation equivalent to \(\mathrm{Hilb}^2(\mathrm{K3})\)). Lefschetz (1,1) on \(H^2(F)\). Abelian 4-fold \(\chi=0\).

10. **Clay algebraicity without a named cycle is not a measured function.** Chern/Euler and Hassett Gram are published for named varieties. Algebraicity of an unnamed class has no residual % — **the cycle is the measurement**. Isolated “prove Hodge” looks for a function that is not measured.

11. **\(\chi\) panel vs Chern.** Named varieties ( \(\mathbb{CP}^n\), products, Gr(2,4), cubic/quartic/sextic 4-folds, abelian \(\chi=0\) ) vs the Chern formula. Hit rate is the measured compare. Not Clay algebraicity.

**Remainder:** Clay’s algebraicity on a general 4-fold. Do not hunt \(C_{48}\). Do not steal \(25-1\) for \(\chi(\mathrm{K3})\).

Clay’s *proof object* (Hodge classes algebraic on every projective manifold) stays `OPEN_NOT_CLAIMED`. Native Lefschetz + named surfaces stay executable.

---

## The difference in one table

| | Clay Hodge | FSOT (this repo) |
|--|----------|------------------|
| Arena | All projective complex manifolds | Named 4-folds + Hassett cubic loci |
| Question | Hodge classes are algebraic cycles | Which extra \((2,2)\) classes are surfaces or K3 periods? |
| \(p=1\) | Lefschetz (1,1) | Named proven first object |
| Associated K3 | — | Extra class \(\cong H^{1,1}(\mathrm{K3})\); Lefschetz |
| Named no-K3 | — | \(C_8..C_{44}\) are the named surfaces |
| Unnamed with K3 | — | Same Lefschetz reduction; do not enumerate |
| Very general cubic | — | Rational Hodge \((2,2)=\langle h^2\rangle\) only |
| Unnamed no-K3 / general 4-folds | The theorem | Remainder |
| Status | Open prize problem | Named list **executable**; remainder **OPEN_NOT_CLAIMED** |

Forbidden: “we proved Millennium Hodge because nine Hassett surfaces match.” Allowed: Lefschetz + named surfaces + K3 reduction. Do not enumerate the tail. Do not steal \(25-1\) for K3.

Refresh: `python vendor/fsot_millennium_accuracy.py`
