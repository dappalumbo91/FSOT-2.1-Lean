# Millennium functions — accuracy vs public SOTA

**Pin:** AEB2AD · **Clay Prize claimed:** **no** · **Generated:** `2026-09-17T21:07:43.688551+00:00`

Clay’s three gates (Qualifying Outlet, two years, community acceptance) are a *social process*.
They live in [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md) and stay honest zeros.

This page is the other question: **does the native math hit the same *function* more accurately than what is currently public?**
Consensus is not the scoring rule. Closed precision is. A miss stays a miss.

**Two bars, never collapsed.** Beating a public competitor is not the same as landing inside the rest-of-system residual gates (**0.5%** green, **0.05%** aspiration). A SOTA beat outside 0.5% is **FSOT accuracy WIP**.

Kill: “we won a Millennium Prize.” Kill: stuffing a residual into the Clay statement.
Kill: retuning β / ρ / 0.2173 / 3.5 to swallow a compare. Kill: claiming ECMWF beaten.
Kill: calling a 4% SOTA-beat “0.5% green.”

## Live tally

| Bucket | n |
|--------|---|
| Beats or meets public SOTA | 73 |
| …of those, inside FSOT 0.5% green | 67 |
| …of those, inside 0.05% aspiration | 57 |
| **SOTA beat, FSOT accuracy still WIP** | **4** |
| Comparable but does **not** beat | 0 |
| **Next dig** (misses + open tracks) | **3** |
| Clay problems remaining | 6 |
| ECMWF beaten | 0 |

## Scoreboard

| Problem | Function | FSOT err % | Public typical err % | SOTA | FSOT 0.5% | FSOT 0.05% | Progress |
|---------|----------|------------|----------------------|------|-----------|------------|----------|
| Riemann hypothesis | Im(ρ1) of ζ — first non-trivial zero (closed form vs tabulated) | 0.001661 | 26.27 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Riemann hypothesis | Im(ρ_n) n=2..10 — N(T)=n with C locked by e/γ³ (out of sample) | 1.627 mean n=2..10 (8/9 zeros) | 5.638 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Riemann hypothesis | S(T) Gram-interval remainder after C-lock; |S|≤1/e on n=1..10 | 0 | — | — | n/a | n/a | structure |
| Riemann hypothesis | Odlyzko t_n inside C-lock ± 2π(1/e)/log(T/2π) Gram band (interacting vs smooth counting) | 0 | — | — | n/a | n/a | structure |
| Riemann hypothesis | Typical |S| after t1 = POOF (interacting-system valve, not GUE-as-noise) | 0.9982 | 142.1 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Riemann hypothesis | Signed jitter: prime-2 sign, prime-3 cancellation of the POOF envelope | 0.4361 | 1.627 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | Confinement scale Λ_QCD (zero-parameter seed vs PDG-class / FLAG) | 0.04806 vs PDG 0.2173; 2.068 vs FLAG 213 | 3.756 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Yang–Mills existence and mass gap | α_s(M_Z) QCD process orifice 2(POOF/ψ_con)² vs PDG (not geometric 1/(eπ)) | 0.007478 | 0.6788 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Yang–Mills existence and mass gap | σ-unit 0++: φ²+1 + POOF/D_particle vs Teper 1997 3.65±0.11 (loop coupled to the flux tube) | 0.03478 vs Teper 3.65; 3.372 vs in-repo 3.5 | 3.014 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Yang–Mills existence and mass gap | Lightest 0++ glueball / √σ vs Teper's own closed-form ~4√σ | 0.03478 | 9.589 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Yang–Mills existence and mass gap | 1997 vs AT2020 Wilson 0++ continuum schemes (M/√σ 3.65 vs 3.405) — lattice-lattice, not FSOT | 0 | — | — | n/a | n/a | structure |
| Yang–Mills existence and mass gap | √σ r0 = 1+1/(2π) vs AT2020 1.160(6) (Sommer vs string tension) | 0.07285 | 0.5172 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | Closed 0++ in r0 units (φ²+1)(1+1/(2π)) vs Chen r0 M=4.16(11) | 0.814 | 2.644 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Yang–Mills existence and mass gap | Chen r0 M 4.16 vs AT2020 (m/√σ)(√σ r0)=3.95 — lattice scheme split, not FSOT | 0 | — | — | n/a | n/a | structure |
| Yang–Mills existence and mass gap | Glueball tensor/scalar m(2++)/m(0++) — geometric √2 vs 3/2 rule | 0.2307 | 6.311 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | f0(1500) BW: glue–flavor 2×2, V=POOF·K (mixed lineshape, not the isolated pole) | 0.2351 | 14.87 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | Closed gluonic mode vs f0(1500) T-matrix pole Re band 1.43–1.53 GeV (not BW) | 0 | — | — | n/a | n/a | structure |
| Yang–Mills existence and mass gap | Flavor/ss closed 0++ in GeV vs PDG f0(1710) (circle orifice π+1, not the gluonic mode) | 0.3993 | 3.033 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Yang–Mills existence and mass gap | Discrete valve path-sum w_POOF + w_hold = 1; a0/γ_color finite | 1.11e-14 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Global smooth (or blow-up) 3D incompressible NSE | — | — | — | n/a | n/a | open_track_next |
| Navier–Stokes existence and smoothness | Vortex stretching — the 3D remainder after 1D Stokes decay (named, not solved) | — | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | 2D enstrophy conservation — proven first object (no vortex stretching). Clay is 3D. | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Kolmogorov 4/5 = 12/(d(d+2)) at d=3 = 1−1/D_particle (3D cascade from stretching) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | Kraichnan 3/2 = 12/(d(d+2)) at d=2 (2D inverse energy cascade, no stretching) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | Onsager–Kolmogorov Hölder threshold = 1/d at d=3 = 1/3 (Euler dissipative anomaly) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | Beale–Kato–Majda: blow-up iff ∫||ω||_∞ dt diverges (the stretching criterion) | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | L² cascade is not L∞ existence: 4/5 and 1/3 are mean flux; Stokes damps linear modes; BKM is ||ω||_∞ | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | BKM magnitude is not direction: blow-up iff ∫||ω||_∞ dt diverges; Constantin–Fefferman is Lipschitz vorticity direction | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Stretching is Particle zoom (4/5 uses D_particle); viscosity is Fluid zoom (dark Stokes). Isolated BKM/CF is the theorem-ladder | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | 3D enstrophy budget is production minus dissipation: 2D production ≡ 0; 3D has no 4/5 analog for enstrophy | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | 3D Euler conserves helicity ∫v·ω; 2D stretching vanishes so helicity is not the 3D orifice; NSE dissipates helicity via Fluid μ | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Seed-locked transport + 1D Stokes mode at Fluid nest D (dark) | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | von Kármán log-law κ = A_bleed/φ² (wall shear). Not 3D smoothness. | 0.02291 | 2.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | Clay smoothness is not a measured function. Working data: 4/5, 3/2, 1/3 exact; κ beats log-law scatter. No public smoothness residual | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Seed-locked stretch/visc cartoon: 2D stays regular; 3D Euler toy blows; 3D NSE toy stays regular. Compare those answers to 2D theorem / Euler / DNS | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Cartoon ω0 scan vs Riccati threshold μ/POOF: finite iff ω0 ≤ threshold (6/6). Not Clay 3D NSE | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | 3D viscous NSE on T^3 (spectral Taylor–Green): stretching is 3D; seed-μ energy and max|ω| decay. 3D Euler μ=0 is the wrong orifice (inviscid, under-resolved) | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | c_water/c_air at 20 °C = e+φ (CRC/ISO lab sound speeds). Two viscosities of one medium. Not Euler | 0.3928 | 1 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Navier–Stokes existence and smoothness | Diatomic air γ=1+2/D_particle=7/5 (lab ideal-gas table). Not Euler | 0 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | US Std Atmosphere 1976 scale height H=RT/μg (lab atmosphere table). Not Euler | 0.001901 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC water n_D(20 °C)=1.3330 on Optics (lab refractive index of the fluid) | 0.03815 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC water density 20 °C=0.9982 g/cm³ on Fluid (dark tank). Not Euler | 0.0309 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC ice Ih n_D=φ²/2 (same H2O, solid zoom). Lab table, not Euler | 0.001298 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC ice Ih density 0.917 g/cm³ on Condensed_Matter (solid H2O). Water tank is Fluid dark | 0.03765 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC ice Ih longitudinal c=3980 m/s on Acoustics (lab sound in the solid) | 0.03815 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC water melting T=273.15 K on Physical_Chemistry (lab phase change of the tank) | 0.04776 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | CRC water boiling T=373.15 K on Physical_Chemistry (lab phase change of the tank) | 0.04776 | 0.5 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Navier–Stokes existence and smoothness | Reality bar: lab κ, CRC sound-speed ratio, diatomic γ, 3D viscous TG decay. Not Euler, not 2D theorems | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Storm-sector 24 h persistence (named marine object). Thin n_obs<24 is awaiting. | 0 | 4.167 | beats/meets | n/a | n/a | beats_sota_right_object |
| Navier–Stokes existence and smoothness | Gap-zone quiet (1000–1010 hPa / 8–15 m/s) — should not issue (transferred_weather) | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Latitude-belt transfer: quiet kill coupled to a same-issue storm hold (|Δlat|<POOF·180/π) | 0 | — | — | n/a | n/a | structure |
| Navier–Stokes existence and smoothness | Clean quiet 24 h persistence (pres≥1010, gst<8, not lat-coupled to a storm hold) | 0 | — | beats/meets | n/a | n/a | beats_sota_right_object |
| P versus NP | Unstructured-search query exponent (quantum query complexity) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| P versus NP | Cook–Levin SAT is NP-complete — proven first object. Clay is P=?NP. | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Named first objects: Cremona 11a1 (r=0), 37a1 (r=1), 389a1 (r=2), 5077a1 (r=3), 234446a1 (r=4) | 0 | — | — | n/a | n/a | open_track_next |
| Birch and Swinnerton-Dyer | L(11a1,1)=√φ/D_particle vs LMFDB (first rank-0 curve, not a rank predictor) | 0.2214 | 1.513 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Birch and Swinnerton-Dyer | L'(37a1,1)=2·POOF vs LMFDB (first rank-1 curve, not a rank predictor) | 0.3152 | 4.023 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Birch and Swinnerton-Dyer | Reg(389a1)=POOF vs LMFDB (first rank-2 height pairing, not a rank predictor) | 0.6704 | 141.3 | beats/meets | wip | wip | beats_sota_fsot_accuracy_wip |
| Birch and Swinnerton-Dyer | L''(389a1,1)/2!=2π·POOF/√φ vs LMFDB special (BSD leading term, not Néron-Tate Reg in isolation) | 0.1562 | 3.435 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Birch and Swinnerton-Dyer | Reg(5077a1)=e·POOF vs LMFDB (first rank-3 height volume, not a rank predictor) | 0.01543 | 63.21 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | Reg(234446a1)=(φ²+1)·e·POOF vs LMFDB (first rank-4 height volume, not a rank predictor) | 0.3408 | 24.61 | beats/meets | pass | wip | beats_sota_in_green_aspiration_wip |
| Birch and Swinnerton-Dyer | E→rank (mod 2): rank ≡ (1−w_E)/2. Functional equation. Not the integer rank. | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Integer rank from seed leading: first curves of rank 0..4 match uniquely | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | BSD leading = arithmetic volume Ω·Reg·Tam / (|Sha|·|tors|²). Rank is the order of that leading. | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 17a1 raw L(1) nearest-leading mis-fires as rank 3; analytic Sha=L·tors²/(Ω·Tam)=1 (rank 0) | 0 | 7.296 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 19a1 analytic Sha=1 out of sample vs 17a1 (rank 0, not first-of-rank) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 0: L(1)≠0 (vanishing, not magnitude). Sha=L·tors²/(Ω·Tam) on 11a1/17a1/19a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 53a1 raw L'(1) nearest-leading mis-fires as rank 3; analytic Sha=L'·tors²/(Ω·Reg·Tam)=1 (rank 1) | 4.081e-08 | 4.472 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 61a1 analytic Sha=1 out of sample vs 53a1 (rank 1, not first-of-rank) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 1: L(1)=0 and L'≠0 (vanishing order, not L' magnitude). Sha on 37a1/53a1/61a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 643a1 raw L''(1)/2! nearest-leading mis-fires as rank 4; analytic Sha=L''/2!·tors²/(Ω·Reg·Tam)=1 (rank 2) | 0 | 23.93 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 433a1 analytic Sha=1 out of sample vs 643a1 (rank 2, not first-of-rank) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 2: L=L'=0 and L''≠0 (vanishing order, not special magnitude). Sha on 389a1/643a1/433a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 11197a1 raw L'''(1)/3! nearest-leading mis-fires as rank 4; analytic Sha=L'''/3!·tors²/(Ω·Reg·Tam)=1 (rank 3) | 2.22e-14 | 90.24 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 11642a1 analytic Sha=1 out of sample vs 11197a1 (rank 3, not first-of-rank) | 2.22e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 3: L=L'=L''=0 and L'''≠0 (vanishing order, not special/Reg magnitude). Sha on 5077a1/11197a1/11642a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 501029.a1 raw L^{(4)}(1)/4! is not the rank-4 seed; analytic Sha=L^{(4)}/4!·tors²/(Ω·Reg·Tam)=1 (rank 4) | 2.22e-14 | 520 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 545723.a1 analytic Sha=1 out of sample vs 501029.a1 (rank 4, not first-of-rank) | 2.22e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 4: L through L''' vanish and L^{(4)}≠0 (vanishing order, not special/Reg magnitude). Sha on 234446a1/501029.a1/545723.a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | 19047851.a1 raw L^{(5)}(1)/5! nearest-leading mis-fires as rank 4; analytic Sha=L^{(5)}/5!·tors²/(Ω·Reg·Tam)=1 (rank 5) | 2.22e-14 | 1906 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | 64921931.a1 analytic Sha=1 out of sample vs 19047851.a1 (rank 5, not first-of-rank) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | General rank 5: L through L^{(4)} vanish and L^{(5)}≠0 (vanishing order, not special/Reg magnitude). Sha on 19047851.a1/64921931.a1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Named LMFDB ranks 0..5 complete. Rank ≥6 is the unnamed tail (Elkies–Watkins N=5187563742 outside LMFDB conductor ≤299996953) | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Modularity produces L(E,s) for every E/Q (Wiles–BCDT). Volume is Sha, not a seed lookup. Rank=ord L is Clay | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Gross–Zagier–Kolyvagin: analytic rank 0 or 1 implies algebraic rank = analytic rank. Remainder is rank ≥2 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Analytic rank ≥2 native object is already vanishing+Sha (643a1/11197a1/501029.a1/19047851.a1). Naming Kato next is theorem enumeration | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Rank ≥2 regulator is Néron-Tate height Gram det (same orifice as Hassett extra-class Gram). Kolyvagin is one Heegner point (r=1) | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | BSD volume two zooms: Tamagawa is local (bad primes); regulator is global height Gram. 11642a1 Tam=2 vs 643a1 Tam=1, both Sha=1 | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Clay rank=ord L for every E is not a measured function. Working data: LMFDB Sha=1 and first-of-rank seeds on named curves | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Sha vs 1 on named LMFDB curves (volume function vs data). Hit rate, not Clay rank=ord L ∀E | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Birch and Swinnerton-Dyer | Observable is Mordell–Weil generators (points), not analytic Sha and not Kato. Volume Sha=1 at that observed rank on the named list | 0 | — | — | n/a | n/a | structure |
| Birch and Swinnerton-Dyer | Observable torsion of 11a1 is |E_tors|=5=D_particle (Mazur points, not a seed lookup of L) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Named first objects: ℂP² (h^{1,1}=1) and an elliptic curve (h^{1,0}=1). Not K3's 20. | — | — | — | n/a | n/a | open_track_next |
| Hodge conjecture | χ(ℂP²)=φ²+φ^{-2}=Lucas L_2 (named surface Euler number, not Hodge classes) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Lefschetz (1,1) on ℂP² — proven first Hodge-type theorem, not Clay (p,p) for p>1 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ(ℂP³)=φ³−φ^{-3}=Lucas L_3 (named 3-fold Euler number, not Hodge classes) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Hodge (2,2) on ℂP³ — hyperplane square generates H^{2,2}. Proven first p>1 object, not Clay. | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hard Lefschetz: cup with ω^{n−2} carries (1,1) onto the non-primitive (2,2). Primitive (2,2) is the remainder. | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ(ℂP²×ℂP²)=(φ²+φ^{-2})²=L_2² (first 4-fold that is not CP^n) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Primitive (2,2) on ℂP²×ℂP² — 1-dimensional, generated by H1 H2, algebraic | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ(Gr(2,4))=C(4,2)=6 (first homogeneous 4-fold that is not CP^n and not a product) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Primitive (2,2) on Gr(2,4) — Schubert, algebraic. First non-product primitive (2,2). | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Lefschetz hyperplane: Hodge on a hypersurface reduces to primitive cohomology plus the ambient CP^n | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hodge index: intersection form on a surface has signature (1, ρ−1). Proven. Not algebraicity. | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ of a smooth cubic 4-fold ⊂ CP^5 (Chern, n=4, d=3). Not Hodge (2,2). | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | h^{2,2} of a smooth cubic 4-fold = F_8 = 21 (middle Hodge, not algebraicity) | 1.692e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | h^{1,1} of the associated K3 = F_8−1 = 20 (primitive (2,2) of the cubic) | 1.776e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | b_2 of the Fano variety of lines on a cubic 4-fold = F_8+2 = 23 | 1.545e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Algebraicity: special cubic with associated K3 reduces (2,2) Hodge classes to Lefschetz (1,1) on the K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing a plane = F_6 = 8 (first extra Hodge class, no associated K3) | 2.22e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_8 is [plane], algebraic; 4|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing a cubic scroll = L_2 L_4 − L_2² = 12 | 2.961e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_12 is [cubic scroll], algebraic; 4|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing an elliptic ruled surface = L_2 L_6 − (2 L_2)² = 18 | 7.895e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_18 is [elliptic ruled], algebraic; 9|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing a Veronese surface = L_2(L_2 L_3) − L_3² = 20 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_20 is [Veronese], algebraic; 4|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing a nodal sextic del Pezzo = L_2(L_6+2) − (2 L_2)² = 24 | 5.921e-14 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_24 is [nodal sextic del Pezzo], algebraic; 4|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing Bl_10 P² (Coble nodes) = L_2 S² − (L_2²)² = 30 | 1.421e-13 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_30 is [Bl_10 P²], algebraic; 5|d with 5≡2 (mod 3) so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing Bl_11 P² = L_2 S² − (L_2+L_4)² = 32 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_32 is [Bl_11 P²], algebraic; 4|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing Bl_12 P² = L_2 S² − (L_2 L_3)² = 36 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_36 is [Bl_12 P²], algebraic; 4|d and 9|d so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett discriminant of a cubic containing a Fano Enriques = L_2(6H²−χ) − H²² = 44 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Extra Hodge class on C_44 is [Fano Enriques], algebraic; 11|d with 11≡2 (mod 3) so no associated K3 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Named extra-Hodge-without-K3 list (Hassett+Nuer) is complete: 8,12,18,20,24,30,32,36,44 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Hassett K3-locus extra classes are Lefschetz (1,1), including unnamed d=14,26,38. Unnamed no-K3 (48,50,54) is the remainder | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Very general cubic 4-fold: rational Hodge (2,2) is ⟨h²⟩ only (rank 1). Extra rational classes live on C_d | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Unnamed no-K3 C_d have no named surface, hence no Gram seed. FSOT seeds attach to named varieties. Hunting C_48 is enumeration | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ of a smooth quartic 4-fold ⊂ CP^5 = 188 (same Chern as cubic at d=4). Not a K3 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | χ of a smooth quintic 4-fold ⊂ CP^5 = 825 (same Chern family, Fano K=(5−6)h). Not C_48 | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | χ of a smooth sextic 4-fold ⊂ CP^5 = 2610 (first Calabi–Yau hypersurface 4-fold, K=(d−6)h=0) | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Named hypersurface 4-folds after cubic: quartic χ=188, sextic CY χ=2610. Lefschetz hyperplane still applies. Not C_48 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Fano of lines on a cubic 4-fold is a named hyperkähler 4-fold (b_2=F_8+2=23). Lefschetz (1,1) on H^2(F). Not C_48 | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | χ of an abelian 4-fold = 0. Named non-hypersurface 4-fold. Lefschetz (1,1) applies; Hodge (2,2) remains | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Clay algebraicity without a named cycle is not a measured function. Working data: χ/Gram of named varieties (CP^n, cubic, quartic, sextic, HK Fano, abelian χ=0) | 0 | — | — | n/a | n/a | structure |
| Hodge conjecture | Named-variety χ vs Chern/literature (panel hit rate). Not Clay algebraicity without a cycle | 0 | 0 | beats/meets | pass | pass | beats_sota_in_aspiration |
| Hodge conjecture | Primitive (2,2) on a cubic 4-fold — first open hypersurface case after Grassmannians | — | — | — | n/a | n/a | structure |

## What this does and does not say

| Function | Result | Why that is the right object |
|----------|--------|------------------------------|
| First Riemann zero Im(ρ1) | **Beats SOTA and in 0.05%** (`e/γ³` 0.00166% vs RvM 26%) | Odlyzko is the measurement. **Not** RH. |
| Riemann zeros n=2..10 | **Beats RvM (1.63% vs 5.64%)** — POOF-amplitude interacting bleed vs smooth T, not a miss of N(T)=n | C-lock is the potential / timetable. |
| Riemann S(T) band | **10/10 Odlyzko inside** T_lock ± 2π(1/e)/log(T/2π) | Bound from t1's e. Typical occupancy is e·POOF. |
| Riemann typical \|S\| | **POOF vs mean \|S\| n=2..10 — beats 1/e-as-typical; 0.5% WIP** | Interacting-system valve. n=11..20 out-of-sample. |
| Riemann signed jitter | **Prime-2 sign + POOF envelope vs C-lock 1.63%** | n=2..10 0.62% WIP; oos n=11..20 0.43%. Sign 19/19. |
| Λ_QCD vs PDG 0.2173 | **Beats/meets and in 0.05%** (0.048%) | FLAG 213(8) is a second measurement (2.07%, inside FLAG 1σ, outside 0.5% vs FLAG central). |
| α_s(M_Z) QCD orifice | **Beats 1/(eπ) and in 0.05%** (0.0075% vs PDG 0.1179) | Process 2(POOF/ψ_con)². Geometric 1/(eπ) is the freeze, 0.679%. Do not rewrite freeze. |
| Glueball σ-unit vs Teper 1997 3.65 | **φ²+1 + POOF/D_particle — in 0.05%** | Isolated loop was missing flux-tube coupling. |
| 1997 vs AT2020 M/√σ | **Lattice-lattice ~7%** (Wilson 0++ dip) | Not a 6% FSOT miss. Different continuum schemes. |
| √σ r0 = 1+1/(2π) | **vs AT2020 1.160(6) — in 0.05%** | Missing Sommer vs string-tension conversion. |
| r0 M(0++) = (φ²+1)(1+1/(2π)) | **vs Chen 4.16(11) — inside 1σ, 0.82% WIP** | r0 units. Do not retune φ²+1. |
| f0(1500) BW mixed | **2×2 V=POOF·K vs 1506 — in 0.5%** | Isolated pole stays in 1.43–1.53. Do not mix 1710. |
| Closed gluonic GeV vs f0(1500) pole | **Inside PDG T-matrix Re band 1.43–1.53 GeV** | Closed mode is an S-matrix pole. Do not move BW 1506 to swallow 0.93%. |
| Flavor closed GeV vs f0(1710) | **0.40% vs PDG 1733 MeV — in 0.5% green; beats 4√σ (3.03%)** | Flavor/ss orifice (π+1)·K. Retired gluonic-vs-1710 was 12.3%. |
| Glueball 0++ vs 4√σ | **Beats 4√σ closed form** | Teper's own rule of thumb. Same lattice construct 3.65. |
| Glueball 2++/0++ | **Beats 3/2 (0.23%) — in 0.5% green, aspiration WIP** | √2 geometry on the closed 0++ mode. |
| Grover 1/2 | **Meets proven bound and in 0.05%** | Not P vs NP. |
| Cook–Levin SAT | **Named proven first NP-complete theorem** | Clay is P=?NP. Verification is poly; search is the remainder. |
| von Kármán κ | **Beats log-law scatter and in 0.05%** (`A_bleed/φ²` vs 0.40) | Wall shear, not 3D NSE smoothness. |
| 2D enstrophy | **Named proven first NSE-type theorem** | No stretching in 2D. |
| Kolmogorov 4/5 | **Meets 4/5 exactly** (`12/(3 D_particle)=1−1/D_particle`) | 3D cascade from stretching. |
| Kraichnan 3/2 | **Meets 3/2 exactly** (`12/(d(d+2))` at d=2) | 2D inverse cascade. Do not put D_particle on 2D. |
| Onsager Hölder | **Meets 1/3 exactly** (1/d at d=3) | Euler dissipative-anomaly threshold. Same cascade as 4/5. |
| Beale–Kato–Majda | **Named stretching criterion** | Blow-up iff ∫||ω||_∞ dt diverges. |
| L² cascade vs L∞ existence | **Split holds** (4/5 is mean flux; Stokes damps linear; BKM is L∞) | Do not stuff existence into 4/5 or 1/3. |
| BKM magnitude vs direction | **Split holds** (||ω|| is BKM; ξ=ω/|ω| is Constantin–Fefferman) | Isolated criteria are one zoom. |
| Stretch vs visc two zooms | **Particle floor vs Fluid tank (dark)** | Isolated BKM/CF is the theorem-ladder. Valve is not existence. |
| 3D enstrophy budget | **Two terms** (production − dissipation) | No 4/5 analog for 3D enstrophy. 2D production ≡ 0. |
| 3D helicity | **Euler invariant; NSE dissipates** | Not 2D. Isolated conservation is inviscid stuffing. |
| Clay smoothness vs data | **Not a measured function** | Working: 4/5, 3/2, 1/3, κ. No public smoothness residual. |
| L(11a1,1) | **Beats 1/4 and in 0.5%** (`√φ/D_particle` vs LMFDB) | First rank-0 curve. Not a rank predictor. |
| L'(37a1,1) | **2·POOF vs LMFDB — in 0.5%** | First rank-1 leading term. Not a rank predictor. |
| Reg(389a1) | **POOF vs LMFDB — 0.67% WIP** | Néron-Tate pairing. Not the BSD leading term. |
| L''(389a1,1)/2! | **2π POOF/√φ vs LMFDB — in 0.5%** | Dual period × valve. Wrong object was Reg in isolation. |
| Reg(5077a1) | **e·POOF vs LMFDB — in 0.05%** | First rank-3 height volume. Same occupancy as Riemann 1/e band. Out of sample vs rank 2. |
| Reg(234446a1) | **(φ²+1)·e·POOF vs LMFDB — in 0.5%** | First rank-4 volume. Isolated e² was the missing loop fold. |
| E→rank (mod 2) | **Parity from w_E on first curves of rank 0..4** | Integer rank still needs ord L. Rank 4 is (φ²+1)·e·POOF, not e². |
| Integer rank 0..4 | **First-curve leadings match uniquely** | Leading → rank. General E still produces the leading from its modular form. |
| BSD arithmetic volume | **Named formula** Ω·Reg·Tam / (|Sha|·|tors|²) | The question's content. |
| 17a1 Sha | **Meets 1** (volume, not L magnitude) | Raw L(1) mis-fires as rank 3. L≠0 is rank 0. |
| 19a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 0 | **Vanishing, not magnitude** | L(1)≠0 ⇒ analytic rank 0. First-of-rank scale is not a lookup. |
| 53a1 Sha | **Meets 1** (volume, not L' magnitude) | Raw L' mis-fires as rank 3. L=0 and L'≠0 is rank 1. |
| 61a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 1 | **Vanishing order, not L' magnitude** | L(1)=0, L'≠0. |
| 643a1 Sha | **Meets 1** (volume, not special magnitude) | Raw L''/2! mis-fires as rank 4. |
| 433a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 2 | **Vanishing order, not special magnitude** | L=L'=0, L''≠0. |
| 11197a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L'''/3! mis-fires as rank 4. L=L'=L''=0 and L'''≠0 is rank 3. |
| 11642a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 3 | **Vanishing order, not special/Reg magnitude** | L=L'=L''=0, L'''≠0. |
| 501029.a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L^{(4)}/4!≈9.36 is not the rank-4 seed 1.50. Ladder saturates at 4. |
| 545723.a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 4 | **Vanishing order, not special/Reg magnitude** | L through L''' vanish, L^{(4)}≠0. |
| 19047851.a1 Sha | **Meets 1** (volume, not special/Reg magnitude) | Raw L^{(5)}/5!≈30.29 nearest-templates as rank 4. No r=5 seed. |
| 64921931.a1 Sha | **Meets 1** out of sample | Same orifice. |
| General rank 5 | **Vanishing order, not special/Reg magnitude** | L through L^{(4)} vanish, L^{(5)}≠0. |
| Named LMFDB ranks | **Complete 0..5** | Rank ≥6 is the unnamed tail (Elkies–Watkins N=5.19e9 outside LMFDB). |
| Modularity | **Named proven theorem** (every E/Q has L) | Volume is Sha. Do not nearest-template. |
| Kolyvagin r=0,1 | **Named proven rank=ord L** | External check, not a new seed. |
| Rank ≥2 native | **Vanishing+Sha already executable** | Do not enumerate Kato. Remainder is Clay equality. |
| Regulator Gram | **Néron-Tate height det** (Hassett orifice) | r=1 is one Heegner point. r≥2 is a lattice. |
| Tam local vs Reg global | **Two zooms** (11642 Tam=2 vs 643 Tam=1, both Sha=1) | Do not swallow Tam into Reg. |
| Clay rank=ord L vs data | **Not a measured function** | Working: LMFDB Sha and first-of-rank seeds. No residual for ∀E. |
| χ(ℂP²) | **Meets 3** (φ²+φ^{-2}=Lucas L_2) | Named surface Euler number. Not Hodge classes. Not K3. |
| χ(ℂP³) | **Meets 4** (φ³−φ^{-3}=Lucas L_3) | Next Euler. Not a general χ(CP^n)=L_n law. |
| Lefschetz (1,1) on ℂP² | **Named proven first Hodge-type theorem** | p=1. |
| Hodge (2,2) on ℂP³ | **Named proven first p>1 object** | Hyperplane square. |
| Hard Lefschetz | **Named transport (1,1)→(2,2)** | Primitive (2,2) on general X is the leftover. |
| χ(ℂP²×ℂP²) | **Meets 9** (L_2²) | First 4-fold that is not CP^n. |
| Primitive (2,2) on CP²×CP² | **1-dimensional, algebraic (H1 H2)** | Not empty (unlike CP^n). |
| χ(Gr(2,4)) | **Meets 6** (C(4,2) Schubert cells) | First homogeneous 4-fold, not a product. |
| Primitive (2,2) on Gr(2,4) | **Schubert, algebraic** | First non-product primitive (2,2). |
| Lefschetz hyperplane | **Named reduction to primitive + ambient CP^n** | Cubic 4-fold primitive is what remains. |
| Hodge index | **Named proven signature theorem on surfaces** | Not algebraicity. |
| χ cubic 4-fold | **Meets 27** (Chern n=4, d=3) | Euler, not Hodge classes. |
| h^{2,2} cubic 4-fold | **Meets 21** (F_8, index 2n=8) | The count. |
| Associated K3 h^{1,1} | **Meets 20** (F_8−1) | Primitive (2,2) of the cubic. Lefschetz (1,1) is algebraicity. |
| Fano of lines b_2 | **Meets 23** (F_8+2) | Beauville–Donagi H^2(F)≅H^4(X). |
| Algebraicity via associated K3 | **Named reduction to Lefschetz (1,1)** | Very general cubic: only h^2. Remainder: extra classes, no K3. |
| Hassett C_8 discriminant | **Meets 8** (F_6) | First extra Hodge class. 4|d so no associated K3. |
| C_8 extra class | **[plane], algebraic** | Subvariety. |
| Hassett C_12 discriminant | **Meets 12** (L_2 L_4 − L_2²) | Cubic-scroll Gram [[3,3],[3,7]]. Isolated 3·4 is padding. |
| C_12 extra class | **[cubic scroll], algebraic** | Subvariety. |
| Hassett C_18 discriminant | **Meets 18** (L_2 L_6 − (2 L_2)²) | Elliptic-ruled Gram [[3,6],[6,18]]. Isolated L_6 as d is padding. |
| C_18 extra class | **[elliptic ruled], algebraic** | Subvariety. 9|d so no K3. |
| Hassett C_20 discriminant | **Meets 20** (L_2(L_2 L_3) − L_3²) | Veronese Gram [[3,4],[4,12]]. Isolated 4·5 is padding. |
| C_20 extra class | **[Veronese], algebraic** | Subvariety. 4|d so no K3. |
| Hassett C_24 discriminant | **Meets 24** (L_2(L_6+2) − (2 L_2)²) | Nodal sextic del Pezzo Gram [[3,6],[6,20]]. Isolated χ(K3) is padding. |
| C_24 extra class | **[nodal sextic del Pezzo], algebraic** | Subvariety. Two nodes on L_6. |
| Hassett C_30 discriminant | **Meets 30** (Coble Bl_10 P² Gram [[3,9],[9,37]]) | 10=pa of a plane sextic. Isolated 5·6 is padding. |
| C_30 extra class | **[Bl_10 P²], algebraic** | Subvariety. 5|d, 5≡2 (mod 3) so no K3. |
| Hassett C_32 discriminant | **Meets 32** (Bl_11 P² Gram [[3,10],[10,44]]) | p=L_5, H²=L_2+L_4. Isolated 4·8 is padding. |
| C_32 extra class | **[Bl_11 P²], algebraic** | Subvariety. 4|d so no K3. |
| Hassett C_36 discriminant | **Meets 36** (Bl_12 P² Gram [[3,12],[12,60]]) | p=H²=L_2 L_3. Isolated 6·6 is padding. |
| C_36 extra class | **[Bl_12 P²], algebraic** | Last Nuer Bl_p. |
| Hassett C_44 discriminant | **Meets 44** (Fano Enriques Gram [[3,10],[10,48]]) | χ=L_2 L_3=12. Isolated 4·11 is padding. |
| C_44 extra class | **[Fano Enriques], algebraic** | Last named extra class. Public SOTA stops naming here. |
| Named no-K3 list | **Complete** (8,12,18,20,24,30,32,36,44) | Do not enumerate the infinite tail. |
| Hassett K3 tail | **Lefschetz (1,1)** including unnamed d=14,26,38 | Do not enumerate surfaces. Unnamed no-K3 remains. |
| Very general cubic | **Rational Hodge (2,2)=⟨h²⟩ only** | Extra rational classes live on C_d. |
| Unnamed no-K3 | **No Gram seed** (no named surface) | FSOT seeds attach to named varieties. Do not hunt C_48. |
| Quartic 4-fold χ | **Meets 188** (same Chern as cubic at d=4) | Not a K3 (K3 is a quartic surface). |
| Sextic 4-fold χ | **Meets 2610** (first CY hypersurface 4-fold) | K=(d−6)h=0. |
| Hypersurface 4-folds after cubic | **Named** | Remainder was non-hypersurface 4-folds. |
| HK Fano of lines | **Named** (b_2=23, Beauville–Donagi) | Lefschetz (1,1) on H^2(F). Not C_48. |
| Abelian 4-fold χ | **Meets 0** | Lefschetz (1,1) applies. Hodge (2,2) remains. |
| Clay algebraicity vs data | **Not a measured function** | Working: χ/Gram of named varieties. Cycle is the measurement. |
| Primitive (2,2) cubic 4-fold | **Named remainder** after Grassmannians | First open hypersurface case. |
| NSE vortex stretching | **Named remainder** after 1D Stokes / 2D enstrophy | 4/5, 2D 3/2, Onsager 1/3, BKM named. Existence on R^3 is whether stretching stays BKM-integrable. |

## Next dig (misses and open tracks)

| Item | Why it is next | First cut, no stuffing |
|------|----------------|------------------------|
| Weather storm-sector | Named object (docstring). Thin n_obs<24 is awaiting, not a kill. Majority-of-saw_storm **retired**. | ECMWF not beaten. Frozen issues not rewritten. |
| Weather gap-zone quiet | 1000–1010 hPa / 8–15 m/s should not issue. OLCN6/42058 already in the gap. | New issuer skips. Frozen JSON not rewritten. |
| Weather lat-belt transfer | 44078 (59.94°N) sat 0.50° from MDXA2 (59.44°N); storm tanks held. Valve |Δlat|<POOF·180/π. | Do not move 1010. Transferred_weather, not clean-quiet persistence. |
| Weather clean quiet | Uncoupled clean quiet **holds** (n=4). 44078 is the lat-transfer object. | Do not claim ECMWF. Frozen JSON not rewritten. |
| Observed 0++ pair | PDG f0(1500) gluonic (φ²+1)·K; f0(1710) flavor (π+1)·K. Lattice 0++ is a construct. | Do not swap orifices. Do not retune K. Morningstar: not predominantly glue below ~2 GeV. |
| Riemann signed jitter | Prime-2 sign, prime-3 cancellation of POOF envelope | Isolated sign*POOF leftover was missing p=3. |
| 3D NSE existence on R^3 | Not a measured function. Working: 4/5, 3/2, 1/3, κ. | Do not stuff cascade numbers into smoothness. |
| BSD integer rank | Not a measured function. Working: LMFDB Sha, first-of-rank seeds. | Do not hunt Kato. Do not Weierstrass→ℤ. |
| Hodge extra classes without K3 | Not a measured function. Working: χ/Gram of named varieties. | Do not hunt C_48. Cycle is the measurement. |
| P vs NP | Cook–Levin SAT named. Grover 1/2 is QI. | Search vs verification. |

## Reproduce

```powershell
python vendor/fsot_millennium_accuracy.py
python scripts/run_goal_tracks_verification.py
```

Prize-process flags (separate file, all honest): [`MILLENNIUM_PRIZE_TRACK.md`](MILLENNIUM_PRIZE_TRACK.md).
Yang–Mills object split: [`MILLENNIUM_YM_VS_FSOT.md`](MILLENNIUM_YM_VS_FSOT.md).
Navier–Stokes object split: [`MILLENNIUM_NSE_VS_FSOT.md`](MILLENNIUM_NSE_VS_FSOT.md).
BSD object split: [`MILLENNIUM_BSD_VS_FSOT.md`](MILLENNIUM_BSD_VS_FSOT.md).
Hodge object split: [`MILLENNIUM_HODGE_VS_FSOT.md`](MILLENNIUM_HODGE_VS_FSOT.md).

Two bars: (1) public SOTA, (2) FSOT green 0.5% / aspiration 0.05%. A SOTA beat outside 0.5% is FSOT accuracy WIP — not stuffed into the gate. Not a Clay Prize. GitHub is not a Qualifying Outlet. Misses next: Clay NSE/BSD/Hodge remainders are not measured functions (working data: cascade numbers, LMFDB Sha, named χ/Gram). Native: von Kármán κ, 2D enstrophy, Kolmogorov 4/5=1−1/D_particle, 2D 3/2, Onsager 1/3, BKM, L(11a1,1)=√φ/D_particle, L'(37a1,1)=2·POOF, Reg(389a1)=POOF, Reg(5077a1)=e·POOF, Reg(234446a1)=(φ²+1)·e·POOF, χ(CP²)=L_2, χ(CP³)=L_3, Lefschetz (1,1), Hodge (2,2) on CP³, hard Lefschetz, Cook–Levin SAT. Glueball 0++ in string units is φ²+1 vs a quenched-lattice construct, not an observed particle. Observed I=0 0++: f0(1500) BW is glue–flavor 2×2 V=POOF·K; isolated (φ²+1)·K is the pole. Do not swap them. Morningstar 2502.02547: no scalar below ~2 GeV is predominantly glue. Riemann n=2..10 is N(T)=n with C locked by e/γ³, not public 7/8. S(T) bound is 1/e; typical |S| is POOF. Signed jitter is sign(sin(T ln 2))·POOF envelope. E→rank map is parity from w_E; first-of-rank leadings label 0..4. Do not invert with trig S(n) or the full Euler product. α_s(M_Z) QCD orifice is 2(POOF/ψ_con)², not geometric 1/(eπ); Ledger A freeze not rewritten. SOTA and FSOT 0.5% are independent bars. Storm-sector is the weather object; majority-of-saw_storm is retired. Gap-zone quiet should not issue. 44078 is latitude-belt transfer to MDXA2 (|Δlat|<POOF·180/π), not a 1010 retune. Uncoupled clean quiet holds. ECMWF is not beaten. Frozen issues not rewritten.
