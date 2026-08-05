# FSOT Reality OS — singular program over the complete engine

**Orientation:** One fluid spacetime, one seed engine, residual atlas, multiprover leaves, hardware path.  
Research tracks (confinement uniqueness, etc.) are **branches** — not the trunk.

## What this is

A **condensed runtime** so you are not navigating hundreds of scripts to run the fabric:

| Piece | Role |
|-------|------|
| `vendor/fsot_reality_os.py` | Library: S, residual predict, atlas, hierarchy, hardware status |
| `scripts/run_fsot_reality_os.py` | CLI entry |
| `data/fsot_atlas.sqlite` | Residuals **+** engine math **+** domain interfaces **+** connective edges |
| `verification/rust/fsot_scalar_kernel` | no_std scalar port → bare metal / QEMU |
| `scripts/run_fsot_hardware_bare_metal.py` | Hardware kit runner |

**Master formula (always):**

```text
S = K · (T1 + T2 + T3)
c = m · (1 + |S| · f)
```

## Commands

```powershell
# Rebuild full fabric (math audit → building-blocks sim → atlas DB → system audit)
python scripts/run_fsot_reality_os.py rebuild

# Boot banner
python scripts/run_fsot_reality_os.py boot

# Domain scalar / residual
python scripts/run_fsot_reality_os.py S Particle_Physics
python scripts/run_fsot_reality_os.py predict Planetary_Science 2.77

# Connective fabric
python scripts/run_fsot_reality_os.py interfaces --kind core --limit 35
python scripts/run_fsot_reality_os.py neighbors Cosmology
python scripts/run_fsot_reality_os.py hierarchy
python scripts/run_fsot_reality_os.py atlas-stats
python scripts/run_fsot_reality_os.py hardware
python scripts/run_fsot_reality_os.py audit
```

## Atlas DB formula tables

After rebuild, `data/fsot_atlas.sqlite` includes:

| Table | Content |
|-------|---------|
| `engine_seeds` | π, e, φ, γ, G |
| `engine_derived` | L1/L2 closed forms |
| `formula_branches` | T1/T2/T3 structure |
| `domain_interfaces` | All core+extension S, f, sign, band |
| `connective_edges` | Hierarchy + network strings |
| `domains` / `records` | Green residual panels |
| `formulas` | Per-record formula strings from benchmarks |

## Path to bare-metal “OS of reality”

```text
Host Reality OS (this CLI)
    ↓ same formula
Rust fsot_scalar_kernel (no_std)
    ↓
fsot_hardware_kernel / trinary_os
    ↓
QEMU / ESP32 bare metal
```

Do not invent a second physics in hardware — **port the same S**.

## Related

- Complete system audit: `docs/FSOT_COMPLETE_SYSTEM_AUDIT.md`
- Math key: `docs/FSOT_MATH_KEY.md`
- Building-blocks sim: `docs/REALITY_BUILDING_BLOCKS_SIMULATION.md`
- Mathematician how-to: `docs/FSOT_MATHEMATICIAN_HOWTO.md`
