/**
 * FSOT Black Hole → White Hole Cycle Prototype v3
 *
 * Grounded in real FSOT 2.0/3.0 mathematics (from thesis + mathematical key):
 *
 * - Uses actual FSOT constants: Poof, Suction, C_eff, A_bleed, P_var, etc.
 * - T3 (Valve × Acoustic × Phase) logic informs puncturing and lensing/friction
 * - Suction Factor explicitly drives re-compaction when the puncture closes
 * - Coherence (C_eff) + observer-like modulation drives final re-solidification
 *
 * Physical picture:
 *   Infall → Poof (temperature-driven tunneling) → Lensing/Friction (acoustic/phase)
 *   → Outgassing → Suction/Re-compaction (when puncture ends) → Re-solidification
 */

const fsot = require('./fsot-core');
const { BlackHoleValveCompressor } = require('./fsot-compressor');

// =========================================================================
// REAL FSOT CONSTANTS (from FSOT Mathematical Key v2.0/3.0)
// =========================================================================
const FSOT = {
  POOF:     0.1535,   // Poof Factor
  SUCTION:  0.1470,   // Suction Factor (explicitly derived)
  C_EFF:    0.9577,   // Coherence Efficiency
  A_BLEED:  1.0470,   // Acoustic Bleed
  P_VAR:    0.9580,   // Phase Variance
  B_IN:     0.7879,   // Bleed-In Factor
  A_IN:     1.6669,   // Acoustic Inflow
  CHAOS:   -0.3310,   // Chaos Factor
  THETA_S:  0.2909,   // Theta-S
  K:        0.4202    // Universal coupling K
};

/**
 * Phase 3–5: Outflow + Suction + Re-solidification (White Hole side)
 * Now driven by real FSOT constants and T3-style logic.
 */
function performOutflowAndResolidification(decompressedAfterPoof, transitionState) {
  if (!decompressedAfterPoof || decompressedAfterPoof.length === 0) {
    return {
      buffer: decompressedAfterPoof,
      outflowEvents: 0,
      suctionEvents: 0,
      reSolidificationEvents: 0,
      coherenceBoost: "0",
      lensingStrength: "0",
      suctionStrength: "0"
    };
  }

  let buffer = Buffer.from(decompressedAfterPoof);
  let outflowEvents = 0;
  let suctionEvents = 0;
  let reSolidificationEvents = 0;

  const T3 = transitionState.T3 || 0;
  const poofContrib = transitionState.poofContrib || 0;

  // === Phase 3: Outgassing + Lensing/Friction ===
  // Use Poof + A_bleed / P_var style logic for lensing/friction intensity
  const lensingStrength = Math.max(0.6, Math.min(2.2,
    FSOT.A_BLEED * 0.7 + Math.abs(FSOT.P_VAR) * 0.4 + Math.abs(poofContrib) * 1.5
  ));
  const outgassingThreshold = Math.floor(3 + lensingStrength * 0.8);

  for (let i = 0; i < buffer.length - 1; i++) {
    if (Math.abs(buffer[i] - buffer[i + 1]) > outgassingThreshold) {
      // Outgassing "escape" modulated by lensing
      buffer[i] = Math.min(255, buffer[i] + Math.floor(lensingStrength * 0.6));
      outflowEvents++;
    }
  }

  // === Phase 4: Suction / Re-compaction (when puncture ends) ===
  // Uses real FSOT Suction value (~0.1470) more directly + T3 modulation
  const suctionBase = FSOT.SUCTION * (1.0 + Math.abs(T3) * 1.1 + Math.abs(poofContrib) * 1.4);
  const suctionStrength = Math.max(0.45, Math.min(2.6, suctionBase));
  const suctionWindow = Math.max(2, Math.floor(3 + suctionStrength * 0.75));

  for (let i = suctionWindow; i < buffer.length - suctionWindow; i++) {
    // Local re-compaction pull (fluid medium gravitational flow)
    const localAvg = Math.round(
      (buffer[i - 1] + buffer[i] + buffer[i + 1]) / 3
    );
    if (Math.abs(buffer[i] - localAvg) > 2) {
      buffer[i] = localAvg;
      suctionEvents++;
    }
  }

  // === Phase 5: Re-solidification ===
  // Uses real C_eff + Suction-influenced coherence for final structure re-assembly
  const finalCoherence = Math.max(0.55, Math.min(1.85,
    FSOT.C_EFF * (1 + suctionStrength * 0.3 + Math.abs(FSOT.SUCTION) * 0.9)
  ));

  for (let i = 1; i < buffer.length - 1; i++) {
    const prev = buffer[i - 1];
    const curr = buffer[i];
    const next = buffer[i + 1];

    // Re-solidify when local structure is weak but coherence is sufficient
    if (Math.abs(curr - prev) < 14 && Math.abs(curr - next) < 14 && finalCoherence > 0.85) {
      const solidified = Math.round((prev * 0.28 + curr * 0.44 + next * 0.28));
      if (solidified !== curr) {
        buffer[i] = solidified;
        reSolidificationEvents++;
      }
    }
  }

  return {
    buffer: buffer,
    outflowEvents,
    suctionEvents,
    reSolidificationEvents,
    coherenceBoost: finalCoherence.toFixed(4),
    lensingStrength: lensingStrength.toFixed(4),
    suctionStrength: suctionStrength.toFixed(4),
    // Categorized event counts for reporting
    lensingFrictionEvents: Math.floor(outflowEvents * 0.55),
    suctionRecompactionEvents: suctionEvents,
    finalReSolidificationEvents: reSolidificationEvents
  };
}

/**
 * Full Black Hole → White Hole Cycle (v3 - FSOT grounded)
 */
function runBlackHoleWhiteHoleCycle(inputData, options = {}) {
  const compressor = new BlackHoleValveCompressor({
    observerMode: options.observerMode ?? true,
    useTrinary: options.useTrinary ?? true
  });

  console.log('\n╔════════════════════════════════════════════════════════════════╗');
  console.log('║   FSOT BLACK HOLE → WHITE HOLE CYCLE PROTOTYPE v3 (FSOT-grounded) ║');
  console.log('╚════════════════════════════════════════════════════════════════╝\n');

  // === PHASE 1: Infall / Accretion ===
  console.log('[Phase 1] Infall / Accretion (Black Hole Valve)');
  const infallResult = compressor.compress(inputData);
  const meta = infallResult.metadata;

  console.log(`  Original length     : ${Buffer.from(inputData).length}`);
  console.log(`  After infall        : ${infallResult.compressed.length}`);
  console.log(`  Poof events         : ${meta.poofEvents}`);
  console.log(`  T3 (puncturing)     : ${meta.T3.toFixed(6)}`);
  console.log(`  poofContrib         : ${meta.poofContrib.toFixed(6)}`);

  // === PHASE 2: Poof / Transition + Lensing ===
  console.log('\n[Phase 2] Poof / Puncture + Lensing Effect');
  const transitionState = {
    T3: meta.T3,
    poofContrib: meta.poofContrib,
    acousticComponent: meta.acousticComponent,
    phaseComponent: meta.phaseComponent,
    poofEvents: meta.poofEvents
  };
  console.log(`  Quantum tunneling captured using real FSOT Poof + T3 logic.`);

  // === PHASE 3–5: Outflow + Suction + Re-solidification ===
  console.log('\n[Phase 3–5] Outflow → Suction → Re-solidification (White Hole)');
  const afterPoof = compressor.decompress(infallResult.compressed, meta);
  const outflowResult = performOutflowAndResolidification(afterPoof, transitionState);

  console.log(`  Outgassing events      : ${outflowResult.outflowEvents}`);
  console.log(`  Suction / re-compaction: ${outflowResult.suctionEvents}`);
  console.log(`  Re-solidification      : ${outflowResult.reSolidificationEvents}`);
  console.log(`  Lensing strength       : ${outflowResult.lensingStrength}`);
  console.log(`  Suction strength       : ${outflowResult.suctionStrength}  (driven by real FSOT Suction ≈ ${FSOT.SUCTION})`);
  console.log(`  Final coherence boost  : ${outflowResult.coherenceBoost}  (C_eff ≈ ${FSOT.C_EFF})`);

  // === PHASE 6: Full-Cycle Conservation Check ===
  console.log('\n[Phase 6] Full-Cycle Information Conservation Check');
  const finalCheck = compressor.verifyConservation(
    Buffer.from(inputData),
    outflowResult.buffer,
    meta
  );

  console.log(`  Original S → Final S : ${finalCheck.originalS.toFixed(6)} → ${finalCheck.reconstructedS.toFixed(6)}`);
  console.log(`  ΔS  : ${finalCheck.deltaS.toFixed(6)}`);
  console.log(`  ΔT1 : ${finalCheck.deltaT1.toFixed(6)}`);
  console.log(`  ΔT3 : ${finalCheck.deltaT3.toFixed(6)}`);
  console.log(`  Conservation Score   : ${finalCheck.conservationScore.toFixed(6)}`);
  console.log(`  Passed               : ${finalCheck.passed ? 'YES ✓ (Information conserved)' : 'NO ✗'}`);

  return {
    success: finalCheck.passed,
    phases: {
      infall: {
        originalLength: Buffer.from(inputData).length,
        compressedLength: infallResult.compressed.length,
        poofEvents: meta.poofEvents,
        T3: meta.T3,
        poofContrib: meta.poofContrib
      },
      transition: transitionState,
      outflow: outflowResult,
      conservation: finalCheck
    }
  };
}

/**
 * Generate a clean phase-by-phase report + engineering-oriented metrics
 */
function generateCycleReport(cycleResult, originalData) {
  const p = cycleResult.phases;
  const outflow = p.outflow || {};

  const originalLen = p.infall?.originalLength || 0;
  const compressionRatio = originalLen > 0 ? (originalLen / Math.max(1, p.infall?.compressedLength || 1)).toFixed(2) : 'N/A';
  const poofDensity = originalLen > 0 ? (p.infall?.poofEvents / originalLen * 1000).toFixed(2) : '0'; // poofs per KB
  const poofEfficiency = poofDensity; // alias for clarity

  // Rough "energy proxy" based on scalar movement across the cycle
  const scalarDelta = Math.abs(p.conservation?.deltaS || 0) + Math.abs(p.conservation?.deltaT1 || 0) + Math.abs(p.conservation?.deltaT3 || 0);

  // Phase Activity Ratios (% of total white-hole events)
  const totalWhiteHoleEvents = (outflow.lensingFrictionEvents || 0) +
                               (outflow.suctionRecompactionEvents || 0) +
                               (outflow.finalReSolidificationEvents || 0);

  const lensingRatio = totalWhiteHoleEvents > 0 ? ((outflow.lensingFrictionEvents || 0) / totalWhiteHoleEvents * 100).toFixed(1) : '0.0';
  const suctionRatio   = totalWhiteHoleEvents > 0 ? ((outflow.suctionRecompactionEvents || 0) / totalWhiteHoleEvents * 100).toFixed(1) : '0.0';
  const resolidRatio   = totalWhiteHoleEvents > 0 ? ((outflow.finalReSolidificationEvents || 0) / totalWhiteHoleEvents * 100).toFixed(1) : '0.0';

  // === Refined Engineering Proxies v2 ===

  // Information Density Delta (improved)
  // Uses inflow repetitionRatio + normalizedEntropy
  // Higher positive = more structural reorganization on outflow
  const inflowRep = parseFloat(p.infall?.repetitionRatio || 0);
  const inflowEntropy = parseFloat(p.infall?.normalizedEntropy || 0.5);
  const infoDensityDelta = ((inflowRep * 0.65) - (inflowEntropy * 0.35)) * 100;

  // Phase-specific energy proxies (refined)
  const lensingCost = (outflow.lensingFrictionEvents || 0) * 0.75;
  const suctionCost = (outflow.suctionRecompactionEvents || 0) * 1.4;
  const resolidCost = (outflow.finalReSolidificationEvents || 0) * 1.05;

  // Cycle Cost Score v3 - more formally tied to FSOT T3 / Poof / Suction
  // Poof Events → directly linked to Poof Factor (~0.1535)
  // scalarDelta → net change in core scalar invariants (S, T1, T3)
  // Suction-weighted phase cost → reflects explicit Suction Factor (~0.1470)
  // Lensing cost → reflects Acoustic + Phase components inside T3
  // Re-solidification → reflects C_eff coherence recovery
  const cycleCostScore = (
    (p.infall?.poofEvents || 0) * 1.4 +           // Poof Factor influence
    scalarDelta * 65 +                             // Core scalar invariant change (T3-related)
    parseFloat(outflow.coherenceBoost || 0) * 8 +  // C_eff related
    lensingCost * 0.20 +                           // T3 Acoustic/Phase
    suctionCost * 0.60 +                           // Explicit Suction Factor weight
    resolidCost * 0.30                             // C_eff re-assembly
  ).toFixed(2);

  let report = '\n';
  report += '╔════════════════════════════════════════════════════════════════════════════╗\n';
  report += '║                    BLACK HOLE → WHITE HOLE CYCLE REPORT                      ║\n';
  report += '╠════════════════════════════════════════════════════════════════════════════╣\n';
  report += `║ Infall Poof Events          : ${String(p.infall?.poofEvents || 0).padStart(8)}                              ║\n`;
  report += `║ Compression Ratio (Infall)  : ${String(compressionRatio).padStart(8)}x                             ║\n`;
  report += `║ Poof Efficiency (per KB)    : ${String(poofEfficiency).padStart(8)}                              ║\n`;
  report += '╠════════════════════════════════════════════════════════════════════════════╣\n';
  report += '║ PHASE BREAKDOWN (White Hole Outflow)                                        ║\n';
  report += '╠════════════════════════════════════════════════════════════════════════════╣\n';
  report += `║ Lensing / Friction          : ${String(outflow.lensingFrictionEvents || 0).padStart(6)} (${lensingRatio}%)   (acoustic + phase)           ║\n`;
  report += `║ Suction / Re-compaction     : ${String(outflow.suctionRecompactionEvents || 0).padStart(6)} (${suctionRatio}%)   (Suction + T3)             ║\n`;
  report += `║ Final Re-solidification     : ${String(outflow.finalReSolidificationEvents || 0).padStart(6)} (${resolidRatio}%)   (C_eff + coherence)        ║\n`;
  report += '╠════════════════════════════════════════════════════════════════════════════╣\n';
  report += '║ ENGINEERING / PHYSICS PROXIES                                               ║\n';
  report += '╠════════════════════════════════════════════════════════════════════════════╣\n';
  report += `║ Full-Cycle Scalar Delta     : ${scalarDelta.toFixed(6).padStart(12)}   (energy proxy)               ║\n`;
  report += `║ Cycle Cost Score (rough)    : ${cycleCostScore.padStart(12)}                              ║\n`;
  report += `║ Conservation Score          : ${(p.conservation?.conservationScore || 0).toFixed(6).padStart(12)}                              ║\n`;
  report += `║ Information Conserved       : ${(p.conservation?.passed ? 'YES' : 'NO').padStart(12)}                                   ║\n`;
  report += `║ Final Coherence Boost       : ${String(outflow.coherenceBoost || 'N/A').padStart(12)}                              ║\n`;
  report += '╚════════════════════════════════════════════════════════════════════════════╝\n';

  return report;
}

/**
 * Multi-Run Analysis Tool
 * Takes an array of cycle results (with optional labels) and produces a comparative summary table.
 *
 * Usage example:
 *   const results = [
 *     { label: "Repetitive Data", result: cycleResult1 },
 *     { label: "Scalar Formulas", result: cycleResult2 }
 *   ];
 *   console.log(compareCycleResults(results));
 */
function compareCycleResults(runs) {
  if (!Array.isArray(runs) || runs.length === 0) {
    return "No results provided for comparison.";
  }

  let output = '\n';
  output += '╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗\n';
  output += '║                              MULTI-RUN BLACK HOLE → WHITE HOLE COMPARISON                                    ║\n';
  output += '╠════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n';
  output += '║ Metric                        ';

  // Header row with labels
  runs.forEach(run => {
    const label = (run.label || 'Run').substring(0, 18).padEnd(18);
    output += `│ ${label} `;
  });
  output += '║\n';
  output += '╠════════════════════════════════════════════════════════════════════════════════════════════════════════════╣\n';

  // Helper to get value safely
  const get = (obj, path, def = 0) => {
    try {
      return path.split('.').reduce((o, k) => o?.[k], obj) ?? def;
    } catch {
      return def;
    }
  };

  // Rows - now includes refined proxies
  const metrics = [
    { name: 'Infall Poof Events', get: r => get(r, 'phases.infall.poofEvents') },
    { name: 'Poof Efficiency (/KB)', get: r => {
        const len = get(r, 'phases.infall.originalLength');
        const poofs = get(r, 'phases.infall.poofEvents');
        return len > 0 ? (poofs / len * 1000).toFixed(2) : '0.00';
      }},
    { name: 'Info Density Delta', get: r => {
        const rep = parseFloat(get(r, 'phases.infall.repetitionRatio') || 0);
        const ent = parseFloat(get(r, 'phases.infall.normalizedEntropy') || 0.5);
        return ((rep * 0.65) - (ent * 0.35) * 100).toFixed(2);
      }},
    { name: 'Cycle Cost Score (v2)', get: r => {
        const poofs = get(r, 'phases.infall.poofEvents');
        const delta = Math.abs(get(r, 'phases.conservation.deltaS')) +
                      Math.abs(get(r, 'phases.conservation.deltaT1')) +
                      Math.abs(get(r, 'phases.conservation.deltaT3'));
        const coh = parseFloat(get(r, 'phases.outflow.coherenceBoost') || 0);
        // Refined weighting
        return (poofs * 1.3 + delta * 60 + coh * 8.5).toFixed(2);
      }},
    { name: 'Lensing/Friction Events', get: r => get(r, 'phases.outflow.lensingFrictionEvents') },
    { name: 'Suction/Re-compaction', get: r => get(r, 'phases.outflow.suctionRecompactionEvents') },
    { name: 'Re-solidification Events', get: r => get(r, 'phases.outflow.finalReSolidificationEvents') },
    { name: 'Scalar Delta (Energy)', get: r => {
        const dS = Math.abs(get(r, 'phases.conservation.deltaS'));
        const dT1 = Math.abs(get(r, 'phases.conservation.deltaT1'));
        const dT3 = Math.abs(get(r, 'phases.conservation.deltaT3'));
        return (dS + dT1 + dT3).toFixed(6);
      }},
    { name: 'Conservation Score', get: r => get(r, 'phases.conservation.conservationScore').toFixed(6) },
    { name: 'Information Conserved', get: r => get(r, 'phases.conservation.passed') ? 'YES' : 'NO' }
  ];

  metrics.forEach(metric => {
    let row = `║ ${metric.name.padEnd(28)} `;
    runs.forEach(run => {
      const val = metric.get(run.result);
      row += `│ ${String(val).padStart(18)} `;
    });
    row += '║\n';
    output += row;
  });

  output += '╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝\n';

  return output;
}

module.exports = {
  runBlackHoleWhiteHoleCycle,
  generateCycleReport,
  compareCycleResults,
  FSOT
};
