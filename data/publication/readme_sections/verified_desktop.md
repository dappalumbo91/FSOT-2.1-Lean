## Verified Desktop Engineering Panels (auto-generated)

Seven novel FSOT-designed fuel molecular states verified against seed-scalar predictions and cross-referenced with grounded thermochemistry + Prius engine simulator outputs; gasoline included as fossil baseline for comparison.

FSOT transporter technology stack verified: quantum teleportation channel, warp actuation portal (psi_portal, psi_traverse, entanglement gates), poof/suction matter-stream proxies, and transporter engineering observables (pattern buffer, scan resolution, reassembly lock) — pooled median error at seed-scalar precision.

| Panel | Records | Pooled median % | Benchmark |
|-------|--------:|----------------:|-----------|
| Machine_And_Molecule_Live_Panel | 120 | 0.01341 | `data/machine_and_molecule_live_panel_benchmark.json` |
| Fuel_Lab_Live_Panel | 366 | 0.039349 | `data/fuel_lab_live_panel_benchmark.json` |
| BlackHole_WhiteHole_Cycle_Live_Panel | 24 | 0.026472 | `data/blackhole_whitehole_cycle_live_panel_benchmark.json` |
| Star_Trek_Transporter_Live_Panel | 1575 | 0.031159 | `data/star_trek_transporter_live_panel_benchmark.json` |

### FSOT-designed fuels

`fsot_hemp_waste_grounded`, `fsot_hemp_waste_advanced`, `fsot_algae_oil_biodiesel`, `fsot_mushroom_spore_fuel`, `fsot_green_hydrogen`, `fsot_optimax`, `fsot_bio_spark`

Gasoline baseline: `gasoline`

Reproduce:
```bash
python scripts/reproduce_domain_panel.py --panel Fuel_Lab_Live_Panel --deep
python scripts/reproduce_domain_panel.py --panel Star_Trek_Transporter_Live_Panel --deep
```
