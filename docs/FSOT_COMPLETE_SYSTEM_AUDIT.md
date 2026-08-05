# FSOT complete system audit

**Status:** `COHERENT`  
**Generated:** 2026-08-05T20:57:03.337801+00:00

Full FSOT fabric: one fluid spacetime engine, residual atlas, multiprover, hardware path. Research tracks (uniqueness, etc.) are leaves — not the trunk.

**Master formula:** `S = K*(T1+T2+T3); c = m*(1+|S|*f)`

## Layers

### L0_engine — Scalar engine (authority) [ok]

core_domains=35 S_particle=0.9504134401245242 S_cosmo=-0.5024559462100433

- `{"path": "vendor/fsot_compute.py", "role": "S=K(T1+T2+T3) seeds L0\u2013L2, 35 cores"}`
- `{"path": "vendor/fsot_compute_AUTHORITY_PIN.json", "role": "pin", "data": {"repinned_at": "2026-07-18T17:29:54.179057+00:00", "authority_sha256": "D1D38A185487B452E470AC68ECE2EB45AEB1CA9CE25FC9BF9564C`
- `{"path": "vendor/fsot_dynamics.py", "role": "T2 fluid continuum"}`
- `{"path": "vendor/fsot_gr_sm.py", "role": "GR/SM force package"}`
- `{"path": "vendor/fsot_seed_flavor.py", "role": "CKM/mass seed ladder"}`
- `{"path": "vendor/fsot_ckm_pmns.py", "role": "CKM/PMNS suite"}`
- `{"path": "scripts/fsot_api_predict_lib.py", "role": "fsot_scaled residual law"}`
- `{"path": "verification/rust/fsot_scalar_kernel", "role": "no_std Rust scalar port"}`

### L1_interfaces — Domain interfaces (core + expansion) [ok]

{'core_domains': 35, 'extension_domains': 371, 'total_domain_interfaces': 406, 'atlas_rows': 403, 'green_benchmark_panels': 470, 'benchmark_files': 470}

- `{"path": "data/fsot_system_math_audit.json", "role": "live S all interfaces"}`
- `{"path": "data/extension_domains_manifest.yaml", "role": "371 extensions"}`
- `{"path": "data/publication/domain_atlas.csv", "role": "publication atlas"}`
- `{"path": "data/fsot_building_block_hierarchy.json", "role": "hierarchy graph"}`
- `{"path": "data/fsot_domain_formula_network.json", "role": "network strings"}`

### L2_residual_atlas — Empirical residual atlas (green gates) [ok]

- `{"path": "data/benchmark_margin_audit.json", "green": 470, "files": 470, "fails": 0}`
- `{"path": "data/fsot_atlas.sqlite", "role": "queryable atlas DB"}`
- `{"path": "data/*benchmark*.json", "count": 474}`

### L3_formal — Multiprover / formal spines [ok]

- `{"path": "data/cross_proof_verification_report.json", "overall_ok": true, "github_ready": true}`
- `{"path": "data/gr_sm_ckm_verification_report.json", "overall_ok": true}`
- `{"path": "data/uniqueness_research_verification_report.json", "overall_ok": true, "note": "one research spine among many \u2014 not the whole ToE"}`
- `{"path": "verification/obligations/", "role": "exported spines"}`
- `{"path": "FSOT/Formal/", "lean_count": 559}`

### L4_buried_waves — Seed derivation waves in fsot_compute (must stay connected) [ok]

Waves are formula inventory — residual panels should map back so nothing stays orphaned.

- `{"function": "wave1", "path": "vendor/fsot_compute.py"}`
- `{"function": "wave2", "path": "vendor/fsot_compute.py"}`
- `{"function": "wave3", "path": "vendor/fsot_compute.py"}`
- `{"function": "wave10", "path": "vendor/fsot_compute.py"}`
- `{"function": "validation_suite", "path": "vendor/fsot_compute.py"}`
- `{"function": "lepton_ratios", "path": "vendor/fsot_compute.py"}`
- `{"function": "chemistry_electronegativity", "path": "vendor/fsot_compute.py"}`
- `{"function": "dynamical_systems", "path": "vendor/fsot_compute.py"}`
- `{"role": "already_surfaced_panels", "examples": ["eta_baryon_photon \u2192 matter_antimatter", "Omega_b_h2 \u2192 matter_antimatter + cosmology", "alpha_s / H0 / T_CMB \u2192 wave1 cosmology residual `

### L5_sectors — Scientific + hardware sectors (balanced inventory) [ok]

All sectors matter equally for the reality OS — no single research track owns the ToE.

- `{"sector": "particle_sm", "present": 3, "total": 3, "status": "ok", "paths": ["data/particle_physics_benchmark.json", "data/pdg_particle_properties_benchmark.json", "data/toe_ckm_pmns_benchmark.json"]`
- `{"sector": "matter_antimatter", "present": 2, "total": 2, "status": "ok", "paths": ["data/matter_antimatter_benchmark.json", "docs/MATTER_ANTIMATTER.md"]}`
- `{"sector": "cosmology", "present": 2, "total": 2, "status": "ok", "paths": ["data/cosmology_extended_benchmark.json", "data/toe_contested_sector_refresh.json"]}`
- `{"sector": "gr_sm", "present": 2, "total": 2, "status": "ok", "paths": ["data/toe_gr_sm_deep_benchmark.json", "data/toe_limit_recovery_benchmark.json"]}`
- `{"sector": "open_science", "present": 2, "total": 2, "status": "ok", "paths": ["data/open_frontier_wave1_report.json", "docs/OPEN_SCIENCE_NEW_FRONTIERS.md"]}`
- `{"sector": "intelligence", "present": 1, "total": 1, "status": "ok", "paths": ["data/intelligence_compression_benchmark.json"]}`
- `{"sector": "hardware", "present": 7, "total": 7, "status": "ok", "paths": ["verification/rust/fsot_scalar_kernel", "verification/rust/fsot_hardware_kernel", "verification/qemu", "vendor/trinary_os", "`
- `{"sector": "dynamics_fluid", "present": 2, "total": 2, "status": "ok", "paths": ["vendor/fsot_dynamics.py", "data/toe_dynamics_benchmark.json"]}`

### L6_atlas_db — SQLite atlas (must hold residuals AND engine math) [ok]

Rebuild with scripts/build_fsot_atlas_sqlite.py after math audit so engine_seeds/interfaces exist.

- `{"exists": true, "tables": ["meta", "domains", "sqlite_sequence", "records", "formulas", "citations", "open_sources", "high_value_gaps", "fts_domains", "fts_domains_data", "fts_domains_idx", "fts_doma`

### L7_reality_os — Singular runtime (condense the mess) [ok]

Goal: one program that runs the complete engine + atlas connectives, path to OS of reality.

- `{"path": "scripts/run_fsot_reality_os.py", "role": "single CLI entry"}`
- `{"path": "vendor/fsot_reality_os.py", "role": "library core"}`
- `{"path": "verification/rust/fsot_scalar_kernel", "role": "bare-metal scalar path"}`
- `{"path": "verification/qemu", "role": "QEMU hardware verification"}`
- `{"path": "data/reality_building_blocks_simulation.json", "role": "hierarchy sim state"}`

## Connectives OK

- Seeds → domain_scalar → fsot_scaled → green benchmarks
- Extension folds → core factors
- GR/SM multiprover + scientific catalog multiprover
- Fluid dynamics T2 + cosmology S damping + particle S emergence
- Matter/antimatter duals + η/Ω_b seeds
- Rust scalar kernel + QEMU/hardware path
- Hierarchy network + building-blocks simulation

## Gaps / connective work

- **medium** `wave_inventory_connection`: Ensure fsot_compute wave* Results are either residual panels or explicit inventory rows in atlas formulas — avoid orphan wave numbers.

## Commands

- **math_audit:** `python scripts/build_fsot_system_math_audit.py`
- **atlas_rebuild:** `python scripts/build_fsot_atlas_sqlite.py`
- **reality_os:** `python scripts/run_fsot_reality_os.py`
- **margins:** `python scripts/audit_all_benchmark_margins.py`
- **building_blocks_sim:** `python scripts/run_reality_building_blocks_simulation.py`
