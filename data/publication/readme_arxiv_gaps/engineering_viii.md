## VIII. Engineering Demonstrations

*These stacks show the seed engine can guide **grounded** engineering readouts — thermochemistry, molecular catalogs, and horizon-cycle proxies. They supplement the empirical spine; they are not its primary proof.*

### 8.1 FSOT-designed alternative fuels

Seven novel molecular states plus gasoline baseline:

- fsot_hemp_waste_grounded, fsot_hemp_waste_advanced, fsot_algae_oil_biodiesel  
- fsot_mushroom_spore_fuel, fsot_green_hydrogen, fsot_optimax, fsot_bio_spark  

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Fuel Lab | 366 | 0.039 |

Cross-referenced with grounded thermochemistry and Prius engine simulator outputs. Preregistered: **PRED-034**.

![Verified desktop fuels](data/figures/verified_desktop_fuels.png)

### 8.2 Machine, molecule, and horizon cycle

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| Machine & Molecule | 120 | 0.013 |
| Black-hole / white-hole cycle | 24 | 0.026 |

Species-scale molecular catalogs and information-cycle panels at the black-hole horizon — seed-scalar predictions cross-checked against simulator outputs, not post-hoc fits.

```bash
python scripts/reproduce_domain_panel.py --panel Machine_And_Molecule_Live_Panel --deep
python scripts/reproduce_domain_panel.py --panel BlackHole_WhiteHole_Cycle_Live_Panel --deep
```

Simulators: `vendor/verified_desktop/` (machine-and-molecule, fuel lab, horizon cycle).

### 8.3 Wet-lab & longevity genetics (Tier 94/95)

Cross-species longevity and zebrafish developmental wet-lab panels — measured biology (HAGR AnAge, NCBI, CZ Biohub) vs seed-scalar readouts, not post-hoc curve fits.

| Panel | Records | Pooled median % |
|-------|--------:|----------------:|
| AnAge catalog | 966 | 0.022 |
| MegaDeep NCBI | 1,746 | 0.018 |
| Consciousness coupling | 890 | 0.022 |
| Zebrafish cell tracking | 20 | 0.022 |
| Zebrafish developmental mechanics | 31 | 0.018 |
| Zebrafish longevity coupling | 24 | 0.014 |

**Full volume:** [`docs/WETLAB_LONGEVITY_DEPTH.md`](docs/WETLAB_LONGEVITY_DEPTH.md)

```bash
python scripts/build_wetlab_longevity_expansion_bundle.py
python scripts/verify_tier95_genetics_system.py
```
