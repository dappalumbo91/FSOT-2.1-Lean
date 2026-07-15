/**
 * FSOT 2.0 / 3.0 Core Engine — JavaScript Port
 * Faithful port of the complete Python/mpmath implementation from FSOT_Thesis_Edition
 * and Fsot3.0 code.py + math key.
 *
 * Zero free parameters. All constants derived from π, e, φ, γ, G (Catalan).
 * Scalar S = K · (T1 + T2 + T3)
 *
 * Ready for integration into compression, AI, simulation, or any program.
 */

const PI = Math.PI;
const E = Math.E;
const PHI = (1 + Math.sqrt(5)) / 2;
const GAMMA = 0.57721566490153286060651209;
const G_CAT = 0.91596559417721901505460351;

// =========================================================================
// LAYER 1 — PRIMARY DERIVED CONSTANTS (exact from thesis)
// =========================================================================
const ALPHA = Math.log(PI) / (E * Math.pow(PHI, 13));
const PSI_CON = 1 - Math.exp(-1);                    // (e-1)/e
const ETA_EFF = 1 / (PI - 1);
const BETA = 1 / Math.exp(Math.pow(PI, PI) + (E - 1));
const GAMMA_C = -Math.log(2) / PHI;
const OMEGA = Math.sin(PI / E) * Math.sqrt(2);
const THETA_S = Math.sin(PSI_CON * ETA_EFF);
const POOF = Math.exp( (-Math.log(PI) / E) / (ETA_EFF * Math.log(PHI)) );

// =========================================================================
// LAYER 2 — COMPOSITE DERIVED CONSTANTS
// =========================================================================
const C_EFF = (1 - POOF * Math.sin(THETA_S)) * (1 + 0.01 * G_CAT / (PI * PHI));
const A_BLEED = Math.sin(PI / E) * PHI / Math.sqrt(2);
const P_VAR = -Math.cos(THETA_S + PI);
const B_IN = C_EFF * (1 - Math.sin(THETA_S) / PHI);
const A_IN = A_BLEED * (1 + Math.cos(THETA_S) / PHI);
const SUCTION = POOF * (-Math.cos(THETA_S - PI));
const CHAOS = GAMMA_C / OMEGA;
const P_BASE = GAMMA / E;
const P_NEW = P_BASE * Math.sqrt(2);
const C_FACTOR = C_EFF * P_NEW;           // Consciousness Factor ≈ 0.2876
const K = PHI * (GAMMA / E) * Math.sqrt(2) / Math.log(PI) * 0.99; // ≈ 0.4202
const C_COSM = 1 / (PHI * 10);

// Cached master scalars (computed once)
let S_COSM = null;
let S_QUANT = null;

// =========================================================================
// SCALAR ENGINE
// =========================================================================

/**
 * ScalarInput — 24-parameter config for any domain or data chunk.
 * Matches the Ada/Python dataclass exactly.
 */
class ScalarInput {
  constructor(params = {}) {
    this.N = params.N ?? 1;
    this.P = params.P ?? 1;
    this.D_eff = params.D_eff ?? 25;
    this.psi_con = params.psi_con ?? PSI_CON;
    this.delta_psi = params.delta_psi ?? 1;
    this.recent_hits = params.recent_hits ?? 0;
    this.rho = params.rho ?? 1;
    this.B_in = params.B_in ?? B_IN;
    this.C_eff = params.C_eff ?? C_EFF;
    this.P_new = params.P_new ?? P_NEW;
    this.observed = params.observed ?? false;
    this.beta = params.beta ?? BETA;
    this.chaos = params.chaos ?? CHAOS;
    this.poof = params.poof ?? POOF;
    this.suction = params.suction ?? SUCTION;
    this.theta_s = params.theta_s ?? THETA_S;
    this.delta_theta = params.delta_theta ?? 1;
    this.A_bleed = params.A_bleed ?? A_BLEED;
    this.A_in = params.A_in ?? A_IN;
    this.P_var = params.P_var ?? P_VAR;
    this.scale = params.scale ?? 1;
    this.amplitude = params.amplitude ?? 1;
    this.trend_bias = params.trend_bias ?? 0;
    this.alpha = params.alpha ?? ALPHA;
  }
}

/**
 * Core FSOT Scalar Computation: S = K · (T1 + T2 + T3)
 * T1: Observer-Modulated Base (with growth, perceived adjust, quirk/collapse)
 * T2: Linear Modulation
 * T3: Valve-Acoustic-Phase (black-hole valves + acoustics)
 */
function computeScalar(input) {
  const s = input instanceof ScalarInput ? input : new ScalarInput(input);
  const N = s.N;
  const P = s.P;
  const D = s.D_eff;
  const dp = s.delta_psi;
  const dt = s.delta_theta;
  const hits = s.recent_hits;

  // Term 1: Observer-Modulated Base
  const growth = Math.exp(s.alpha * (1 - hits / N) * GAMMA / PHI);
  let base =
    (N * P / Math.sqrt(D)) *
    Math.cos((s.psi_con + dp) / ETA_EFF) *
    Math.exp(-s.alpha * hits / N + s.rho + s.B_in * dp) *
    (1 + growth * s.C_eff);

  let T1 = base * (1 + s.P_new * Math.log(D / 25));

  if (s.observed) {
    T1 = T1 * Math.exp(C_FACTOR * s.P_var) * Math.cos(dp + s.P_var);
  }

  // Term 2: Linear Modulation
  const T2 = s.scale * s.amplitude + s.trend_bias;

  // Term 3: Valve-Acoustic-Phase
  const valve =
    s.beta * Math.cos(dp) *
    (N * P / Math.sqrt(D)) *
    (1 + s.chaos * (D - 25) / 25) *
    (1 + s.poof * Math.cos(s.theta_s + PI) + s.suction * Math.sin(s.theta_s));

  const acoustic =
    1 +
    (s.A_bleed * Math.sin(dt) ** 2) / PHI +
    (s.A_in * Math.cos(dt) ** 2) / PHI;

  const phase = 1 + s.B_in * s.P_var;

  const T3 = valve * acoustic * phase;

  return K * (T1 + T2 + T3);
}

/**
 * Detailed breakdown for black-hole valve analysis.
 * Returns S + T1, T2, T3, and poof contribution.
 */
function computeScalarDetailed(input) {
  const s = input instanceof ScalarInput ? input : new ScalarInput(input);
  const N = s.N;
  const P = s.P;
  const D = s.D_eff;
  const dp = s.delta_psi;
  const dt = s.delta_theta;
  const hits = s.recent_hits;

  // Term 1
  const growth = Math.exp(s.alpha * (1 - hits / N) * GAMMA / PHI);
  let base =
    (N * P / Math.sqrt(D)) *
    Math.cos((s.psi_con + dp) / ETA_EFF) *
    Math.exp(-s.alpha * hits / N + s.rho + s.B_in * dp) *
    (1 + growth * s.C_eff);

  let T1 = base * (1 + s.P_new * Math.log(D / 25));

  if (s.observed) {
    T1 = T1 * Math.exp(C_FACTOR * s.P_var) * Math.cos(dp + s.P_var);
  }

  // Term 2
  const T2 = s.scale * s.amplitude + s.trend_bias;

  // Term 3 + poof contrib
  const valve =
    s.beta * Math.cos(dp) *
    (N * P / Math.sqrt(D)) *
    (1 + s.chaos * (D - 25) / 25) *
    (1 + s.poof * Math.cos(s.theta_s + PI) + s.suction * Math.sin(s.theta_s));

  const acoustic =
    1 +
    (s.A_bleed * Math.sin(dt) ** 2) / PHI +
    (s.A_in * Math.cos(dt) ** 2) / PHI;

  const phase = 1 + s.B_in * s.P_var;

  const T3 = valve * acoustic * phase;
  const poofContrib = s.poof * Math.cos(s.theta_s + PI);

  const S = K * (T1 + T2 + T3);

  // Explicit acoustic and phase sub-components (from thesis T3 valve-acoustic-phase)
  const acousticComponent = acoustic;
  const phaseComponent = phase;

  return {
    S,
    T1,
    T2,
    T3,
    poofContrib,
    acousticComponent,
    phaseComponent,
    components: {
      T1,
      T2,
      T3,
      poofContrib,
      acousticComponent,
      phaseComponent
    }
  };
}

/**
 * Domain-aware helper (35 domains from thesis)
 */
const DOMAIN_DEFAULTS = {
  Particle_Physics:      { D_eff: 5,  hits: 0, delta_psi: 1.0,  observed: true },
  Quantum_Mechanics:     { D_eff: 6,  hits: 0, delta_psi: 1.0,  observed: true },
  Atomic_Physics:        { D_eff: 7,  hits: 0, delta_psi: 0.5,  observed: true },
  Physical_Chemistry:    { D_eff: 8,  hits: 0, delta_psi: 0.5,  observed: true },
  Chemistry:             { D_eff: 8,  hits: 0, delta_psi: 0.5,  observed: true },
  Electromagnetism:      { D_eff: 9,  hits: 0, delta_psi: 0.7,  observed: true },
  Molecular_Chemistry:   { D_eff: 9,  hits: 0, delta_psi: 0.4,  observed: true },
  Optics:                { D_eff: 10, hits: 0, delta_psi: 0.6,  observed: true },
  Acoustics:             { D_eff: 10, hits: 0, delta_psi: 0.3,  observed: true },
  Quantum_Computing:     { D_eff: 11, hits: 0, delta_psi: 1.0,  observed: true },
  Quantum_Optics:        { D_eff: 11, hits: 0, delta_psi: 0.6,  observed: true },
  Biology:               { D_eff: 12, hits: 0, delta_psi: 0.05, observed: false },
  Thermodynamics:        { D_eff: 13, hits: 0, delta_psi: 0.4,  observed: true },
  Biochemistry:          { D_eff: 13, hits: 0, delta_psi: 0.1,  observed: false },
  Neuroscience:          { D_eff: 14, hits: 1, delta_psi: 0.1,  observed: true },
  Condensed_Matter:      { D_eff: 14, hits: 0, delta_psi: 0.5,  observed: true },
  Fluid_Dynamics:        { D_eff: 15, hits: 1, delta_psi: 0.9,  observed: false },
  Nuclear_Physics:       { D_eff: 15, hits: 1, delta_psi: 1.0,  observed: true },
  Ecology:               { D_eff: 15, hits: 1, delta_psi: 0.2,  observed: false },
  Meteorology:           { D_eff: 16, hits: 2, delta_psi: 0.8,  observed: false },
  Materials_Science:     { D_eff: 16, hits: 0, delta_psi: 0.5,  observed: true },
  Psychology:            { D_eff: 16, hits: 1, delta_psi: 0.3,  observed: true },
  Atmospheric_Physics:   { D_eff: 17, hits: 2, delta_psi: 0.8,  observed: false },
  Oceanography:          { D_eff: 17, hits: 1, delta_psi: 0.7,  observed: false },
  Seismology:            { D_eff: 18, hits: 2, delta_psi: 1.2,  observed: false },
  Sociology:             { D_eff: 18, hits: 3, delta_psi: 1.5,  observed: true },
  High_Energy_Physics:   { D_eff: 19, hits: 1, delta_psi: 1.2,  observed: true },
  Geophysics:            { D_eff: 19, hits: 2, delta_psi: 1.0,  observed: false },
  Astronomy:             { D_eff: 20, hits: 1, delta_psi: 1.0,  observed: true },
  Economics:             { D_eff: 20, hits: 3, delta_psi: 1.5,  observed: true },
  Planetary_Science:     { D_eff: 21, hits: 1, delta_psi: 1.0,  observed: true },
  Quantum_Gravity:       { D_eff: 22, hits: 0, delta_psi: 1.0,  observed: false },
  Particle_Astrophysics: { D_eff: 23, hits: 1, delta_psi: 1.0,  observed: true },
  Astrophysics:          { D_eff: 24, hits: 1, delta_psi: 1.0,  observed: true },
  Cosmology:             { D_eff: 25, hits: 0, delta_psi: 1.0,  observed: false },
};

function computeForDomain(domainName, overrides = {}) {
  const base = DOMAIN_DEFAULTS[domainName] || DOMAIN_DEFAULTS.Cosmology;
  const params = { ...base, ...overrides };
  return computeScalar(params);
}

// Initialize cached master scalars
function initMasterScalars() {
  if (S_COSM === null) S_COSM = computeForDomain("Cosmology");
  if (S_QUANT === null) S_QUANT = computeForDomain("Quantum_Mechanics");
  return { S_COSM, S_QUANT };
}

// =========================================================================
// UTILITIES FOR COMPRESSION / DATA ANALYSIS
// =========================================================================

/**
 * Treat a data buffer/string as a "fluid" and compute FSOT scalar.
 * Simple mapping: byte stats → N/P (activity), D_eff (complexity/entropy estimate),
 * recent_hits (changes), observed (if we "measure" it).
 */
function dataToScalar(data) {
  if (typeof data === 'string') data = new TextEncoder().encode(data);
  if (data.length === 0) return 0;

  const len = data.length;
  let sum = 0, changes = 0, unique = new Set();
  for (let i = 0; i < len; i++) {
    sum += data[i];
    unique.add(data[i]);
    if (i > 0 && data[i] !== data[i-1]) changes++;
  }
  const mean = sum / len;
  const entropyProxy = unique.size / 256;           // crude entropy
  const activity = Math.min(10, 1 + changes / (len / 10));
  const complexity = Math.max(4, Math.min(25, Math.floor(4 + entropyProxy * 21)));

  const si = new ScalarInput({
    N: Math.max(1, activity),
    P: 1,
    D_eff: complexity,
    delta_psi: 0.5 + entropyProxy * 0.5,
    recent_hits: Math.min(5, Math.floor(changes / (len / 20))),
    observed: true,                    // we are "observing" the data
    rho: 1 + (mean - 128) / 256,       // slight bias from mean byte
  });
  return computeScalar(si);
}

/**
 * Quick compressibility score using FSOT.
 * Higher positive or specific range often indicates more structure (compressible).
 */
function fsotCompressibilityScore(data) {
  const s = dataToScalar(data);
  // Example heuristic (we will test and refine relentlessly)
  return Math.abs(s) * (s > 0 ? 1.2 : 0.8); // favor emergence or damped?
}

// Export everything
module.exports = {
  // Constants
  PI, E, PHI, GAMMA, G_CAT,
  ALPHA, PSI_CON, ETA_EFF, BETA, GAMMA_C, OMEGA, THETA_S, POOF,
  C_EFF, A_BLEED, P_VAR, B_IN, A_IN, SUCTION, CHAOS,
  P_BASE, P_NEW, C_FACTOR, K, C_COSM,
  // Engine
  ScalarInput,
  computeScalar,
  computeForDomain,
  initMasterScalars,
  // Data tools
  dataToScalar,
  fsotCompressibilityScore,
  DOMAIN_DEFAULTS,
  computeScalarDetailed,
};

console.log("FSOT 2.0/3.0 Core loaded. K ≈", K.toFixed(6));
console.log("Example Cosmology S:", computeForDomain("Cosmology").toFixed(6));
